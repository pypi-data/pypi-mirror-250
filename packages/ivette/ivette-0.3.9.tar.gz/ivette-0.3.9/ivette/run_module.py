"""
This module contains functions for running calculations using different packages.
It provides functions for running calculations with GAMESS US and NWChem.
The module also includes functions for handling job status, file upload, and cleanup.
"""
import os
from telnetlib import STATUS
import time
import logging
import subprocess

import psutil
from ivette.decorators import main_process

from ivette.file_io_module import (
    convert_xyz_to_sdf,
    extract_geometries,
    generate_nwchem_input_from_sdf,
    get_step_data,
    get_thermo_data,
    get_total_dft_energy
)
from .utils import print_color
from ivette.types import StoppableThread, ThermoData

from .IO_module import (
    get_cpu_core_count,
    setUp,
    cleanUp,
    check_gamess_installation,
    is_nwchem_installed,
    system_info,
    waiting_message
)

from .supabase_module import (
    downloadFile,
    get_dep_jobs,
    get_job_data,
    insert_step,
    update_job,
    uploadFile,
    insert_species,
    upsert_server
)

# Info disabling
logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("aiohttp").setLevel(logging.CRITICAL)
logging.getLogger("gql").setLevel(logging.CRITICAL)

# Classes
class CommandRunner:
    def __init__(self):
        self.process = None

    def run_command(self, command, job_id):
        with open(f"tmp/{job_id}.out", "w", encoding='utf-8') as output_file:
            self.process = subprocess.Popen(
                command,
                stdout=output_file,
                stderr=subprocess.STDOUT,
                shell=True,
            )

    def stop(self):
        if self.process is not None:
            try:
                parent = psutil.Process(self.process.pid)
                # or parent.children() for recursive=False
                for child in parent.children(recursive=True):
                    child.terminate()
                parent.terminate()
            except psutil.NoSuchProcess:
                pass

    def wait_until_done(self):
        if self.process is not None:
            # Wait for the process to terminate
            self.process.wait()

            # Wait for all child processes
            while True:
                try:
                    pid, _ = os.waitpid(-1, os.WNOHANG)
                except ChildProcessError:
                    # No more child processes
                    break
                if pid == 0:
                    # No child process is ready to reap
                    break

# Create a flag to signal when the job is done
job_done = False
job_failed = False
OPERATION = None
exit_status = None
exit_code = None
command_runner = CommandRunner()
step_thread = StoppableThread()


def run_rungms(job_id, nproc):  # deprecated
    """
    Run the 'rungms' command with the given id and number of processors.

    Args:
        id (str): The id of the command.
        nproc (int): The number of processors to use.

    Raises:
        subprocess.CalledProcessError: If the 'rungms' command returns a non-zero exit code.

    Returns:
        None
    """

    print("GAMESS US module is deprecated, expect bugs and errors.")
    global job_done
    global job_failed

    command = ["rungms tmp/" + job_id + " 00 " +
               str(nproc)]  # The last one is ncores

    with open(f"tmp/{job_id}.out", "w", encoding='utf-8') as output_file:
        try:

            # Run the 'rungms' command and wait for it to complete
            subprocess.run(
                command,
                stdout=output_file,
                stderr=subprocess.STDOUT,
                shell=True,
                check=True,  # This will raise an error if the command returns a non-zero exit code
            )

            uploadFile(f"{job_id}.out", job_id, bucketName="Outputs", localDir="tmp/")
            update_job(job_id, nproc=0)
            job_done = True

        except subprocess.CalledProcessError as e:
            if not e.returncode == -2:

                update_job(job_id, "failed", nproc=0)
                uploadFile(f"{job_id}.out", job_id, bucketName='Outputs', localDir="tmp/")

            cleanUp(job_id)
            print(f"\n Job failed with exit code {e.returncode}.")
            job_done = True
            job_failed = True


def handle_optimize_operation(job_id, nproc):
    # Create a new species for the optimized geometry
    species_id = insert_species(f'{job_id} opt')

    # Extract the optimized geometry from the output file
    extract_geometries(
        f"tmp/{job_id}.out", f"tmp/{species_id}.xyz")
    convert_xyz_to_sdf(
        f"tmp/{species_id}.xyz", f"tmp/{species_id}.sdf")

    # Generate input file

    jobs = get_dep_jobs(job_id)

    for job in jobs:
        generate_nwchem_input_from_sdf(
            f"tmp/{species_id}.sdf",
            job.get('basisSet'),
            job.get('charge'),
            job.get('id'),
            functional=job.get('functional'),
            multiplicity=job.get('multiplicity'),
            operation="energy" if (job.get('operation').upper() ==
                                   'COSMO') else job.get('operation'),
            cosmo=True if (job.get('operation').upper() == 'COSMO') else False
        )

        uploadFile(f"tmp/{species_id}.nw",
                   job.get('id'), bucketName='Inputs')

    # Upload the optimized geometry
    uploadFile(f"{species_id}.sdf", species_id,
               bucketName='Species', localDir='tmp/')
    uploadFile(f"{job_id}.out", job_id, bucketName="Outputs", localDir="tmp/")

    # Set step data
    step_data = get_step_data(f"tmp/{job_id}.out")

    # Upload data from the current job
    thermo_data = ThermoData(
        energy=step_data.energy if step_data is not None else None)
    update_job(job_id, "done", nproc=0, species_id=species_id,
               thermo_data=thermo_data)


def handle_other_operations(job_id, nproc):
    # Create a new species for the optimized geometry
    jobs = get_dep_jobs(job_id)
    current_job = get_job_data(job_id)

    # Extract the optimized geometry from the output file
    extract_geometries(
        f"tmp/{job_id}.out", f"tmp/{current_job.get('inputSpeciesId')}.xyz")
    convert_xyz_to_sdf(
        f"tmp/{current_job.get('inputSpeciesId')}.xyz", f"tmp/{current_job.get('inputSpeciesId')}.sdf")

    # Generate input file
    for job in jobs:

        generate_nwchem_input_from_sdf(
            f"tmp/{current_job.get('inputSpeciesId')}.sdf",
            job.get('basisSet'),
            job.get('charge'),
            job.get('id'),
            functional=job.get('functional'),
            multiplicity=job.get('multiplicity'),
            operation="energy" if (job.get('operation').upper() ==
                                   'COSMO') else job.get('operation'),
            cosmo=True if (job.get('operation').upper()
                           == 'COSMO') else False
        )

        uploadFile(f"tmp/{current_job.get('inputSpeciesId')}.nw",
                   job.get('id'), bucketName='Inputs')

    # Upload the output file
    uploadFile(f"{job_id}.out", job_id, bucketName="Outputs", localDir="tmp/")

    # Upload data from the current job
    if current_job.get('operation').upper() in ['ENERGY', 'COSMO', 'FREQ']:

        thermo_data = ThermoData(
            energy=get_total_dft_energy(f"tmp/{job_id}.out"))

        if current_job.get('operation').upper() == 'FREQ':

            thermo_data = get_thermo_data(f"tmp/{job_id}.out", thermo_data=thermo_data)
            update_job(job_id, "done", nproc=0, thermo_data=thermo_data)

        else:

            update_job(job_id, "done", nproc=0, thermo_data=thermo_data)


def run_nwchem(job_id, nproc):
    """
    Run the calculation
    """

    global job_done
    global job_failed
    global exit_status
    global exit_code
    global command_runner

    if nproc:
        command = [
            f"mpirun -np {nproc} --use-hwthread-cpus --allow-run-as-root /usr/bin/nwchem tmp/{job_id}"]
    else:
        command = [
            f"mpirun -map-by core --use-hwthread-cpus --allow-run-as-root /usr/bin/nwchem tmp/{job_id}"]

    try:
        # Use the instance to run the command
        command_runner.run_command(command, job_id=job_id)
        command_runner.wait_until_done()

        if not exit_status:

            if OPERATION and OPERATION.upper() == "OPTIMIZE":
                handle_optimize_operation(job_id, nproc)
            else:
                handle_other_operations(job_id, nproc)

        job_done = True

    except subprocess.CalledProcessError as e:
        if not e.returncode == -2:
            update_job(job_id, "failed", nproc=0)
            uploadFile(f"{job_id}.out", job_id,
                       bucketName='Outputs', localDir="tmp/")
        job_done = True
        job_failed = True
        exit_code = e.returncode
        raise SystemExit from e


@main_process('\nRun module has been stooped.')
def run_job(nproc=None):
    """
    Run the job based on the specified package and number of processors.

    Args:
        nproc (int, optional): Number of processors to use. Defaults to None.

    Raises:
        SystemExit: If the job is interrupted by the user.

    Returns:
        None
    """
    global job_done
    global OPERATION
    global job_failed
    global exit_status
    global command_runner
    JOB_ID = None
    PACKAGE = None
    OPERATION = None
    print("Press Ctrl + C at any time to exit.")
    SERVER_ID = upsert_server(system_info(), "online").get('id')  # type: ignore
    print(f"Running server: {SERVER_ID}")

    # Loop over to run the queue
    while True:

        JOB_ID, PACKAGE, OPERATION = setUp(SERVER_ID)
        downloadFile(JOB_ID, dir='tmp/', bucket_name="Inputs")

        if PACKAGE in ["GAMESS US", "NWChem"] and (check_gamess_installation if PACKAGE == "GAMESS US" else is_nwchem_installed):
            if not nproc:
                nproc = get_cpu_core_count()

            # Create a thread to run the command
            run_thread = StoppableThread(
                target=run_rungms if PACKAGE == "GAMESS US" else run_nwchem, args=(JOB_ID, nproc))

            # Create a thread to run the function
            step_thread = StoppableThread(
                target=periodical_updates, args=(f'tmp/{JOB_ID}.out', JOB_ID, SERVER_ID))
            step_thread.daemon = True

            try:
                update_job(JOB_ID, "in progress",
                           nproc if nproc else get_cpu_core_count())  # type: ignore

                print(f">  Job Id: {JOB_ID}")
                run_thread.start()  # Start the command thread
                step_thread.start()

                while not job_done:
                    waiting_message(PACKAGE)

                    if exit_status:
                        print(f"{exit_status.upper()} requested interrupting job...",
                              flush=True)
                        raise Exception(exit_status)

                run_thread.join()  # Wait for the command thread to finish
                step_thread.stop()
                cleanUp(JOB_ID)

                if not job_failed:
                    print_color("✓ Job completed successfully.", "32")
                else:
                    print(f"\n\n Job failed with exit code {exit_code}.")

                job_done = False
                job_failed = False

            except KeyboardInterrupt as exc:

                exit_status = "turn off"
                run_thread.stop()
                print(' Exit requested.          ', flush=True)
                print('Waiting for all running processes to finish...', flush=True)
                update_job(JOB_ID, "interrupted", nproc=0)
                upsert_server(system_info(), "offline", server_id=SERVER_ID)
                run_thread.join()  # Wait for the command thread to finish
                step_thread.stop()
                cleanUp(JOB_ID)
                print_color("Job interrupted.       ", "34")
                raise SystemExit from exc

            except Exception as exc:

                if str(exc) == "turn off":

                    command_runner.stop()  # Also stop child processes
                    run_thread.stop()  # Unkown effect
                    step_thread.stop()
                    print('Waiting for all running processes to finish...', flush=True)
                    run_thread.join()

                    update_job(JOB_ID, "interrupted", nproc=0)
                    upsert_server(system_info(), "offline", server_id=SERVER_ID)
                    cleanUp(JOB_ID)
                    print_color("Server turned off", "34")
                    raise SystemExit from exc
                
                elif str(exc) == "skip":

                    command_runner.stop()
                    run_thread.stop()
                    step_thread.stop()
                    print('Waiting for all running processes to finish...', flush=True)
                    run_thread.join()

                    update_job(JOB_ID, "skipped", nproc=0)
                    upsert_server(system_info(), "offline", server_id=SERVER_ID)
                    cleanUp(JOB_ID)
                    print_color("Job skipped", "34")
                    exit_status = None

                elif str(exc) == "cancel":

                    command_runner.stop()
                    run_thread.stop()
                    step_thread.stop()
                    print('Waiting for all running processes to finish...', flush=True)
                    run_thread.join()

                    update_job(JOB_ID, "canceled", nproc=0)
                    upsert_server(system_info(), "offline", server_id=SERVER_ID)
                    cleanUp(JOB_ID)
                    print_color("Job canceled", "34")
                    exit_status = None

        else:

            print(f"No package called: {PACKAGE}. Contact support.")
            raise SystemExit


def periodical_updates(file, JOB_ID, server_id):
    global OPERATION
    global exit_status
    last_step = None
    last_index = -1

    while True:

        # Update server status and check for orders
        if not exit_status:

            status = upsert_server(
                        system_info(),
                        "online",
                        server_id=server_id
                    ).get('status')  # type: ignore

            if status == "turn off":
                exit_status = "turn off"
            elif status == "skip":
                exit_status = "skip"
            elif status == "cancel":
                exit_status = "cancel"

        if step_thread.stopped():
            break

        # Get step data
        try:
            step_data = get_step_data(file, last_index + 1)
            while step_data is not None:
                # If operation is optimize and it's a new step, insert step
                if OPERATION == 'optimize' and step_data != last_step:
                    insert_step(JOB_ID, step_data)
                    last_step = step_data
                last_index += 1
                step_data = get_step_data(file, last_index + 1)
        except FileNotFoundError:
            time.sleep(5)
            continue

        # Sleep for a period of time (e.g., 5 seconds)
        time.sleep(5)
