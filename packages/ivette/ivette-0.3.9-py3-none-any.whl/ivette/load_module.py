"""Module for handling input/output operations."""
import itertools
import logging
from tqdm import tqdm

from .utils import print_color

from .IO_module import (
    create_charge_multiplicity_array,
    create_string_array,
    file_exists,
    get_valid_input,
    verify_file_extension,
    exists,
    cleanUp
)

from .file_io_module import (
    generate_nwchem_input_from_sdf,
    convert_xyz_to_sdf,
    get_files_with_extension,
    get_word_at_position,
    nwchem_to_xyz,
    replace_start_directive
)

from .supabase_module import (
    insert_species,
    uploadFile,
    insert_job,
    update_job
)

logging.getLogger("httpx").setLevel(logging.CRITICAL)

# Available packages:
available_packages = ['NWChem']


def load_job(filename: str):
    """
    Load a job from a file.

    Args:
        filename (str): The name of the file.

    Raises:
        SystemExit: If the file does not exist or the package is not supported.
    """
    if file_exists(filename, "./"):

        if verify_file_extension(filename, ['.sdf']):

            print("The file is recognized as a .sdf")
            print("An .nw input file will be created.")

            # Argument input
            JOB_NAME = input('Enter the job name: ')
            JOB_DESCRIPTION = input('Enter a description: ')
            package = available_packages[get_valid_input(
                f"Software available:\n1 - {available_packages[0]}\nSelect a package: ", 1, 2) - 1]

            if package == available_packages[0]:

                # Argument input
                basis = input("Enter a valid basis set: ")
                functional = input("Enter a valid functional: ")
                charge = int(input("Enter the system charge: "))
                multiplicity = int(input("Enter the system multiplicity: "))
                operation = input("Operation: ")
                # Add maxiter, maxcycle, etc.

                # Insert job and species
                JOB_ID = insert_job(JOB_NAME, package, operation, JOB_DESCRIPTION)
                SPECIES_ID = insert_species(filename)
                if SPECIES_ID is None:
                    raise ValueError("Failed to insert species")
                print("Job id:", JOB_ID)

                generate_nwchem_input_from_sdf(
                    filename,
                    basis,
                    charge,
                    JOB_ID,
                    functional=functional,
                    multiplicity=multiplicity,
                    operation="freq" if (operation.upper() ==
                                       'COSMO') else operation,
                    cosmo=True if (operation.upper() == 'COSMO') else False
                )

                # Upload files
                print(f"Loading job: {filename.replace('.sdf', '.nw')}")
                uploadFile(filename.replace('.sdf', '.nw'), JOB_ID, bucketName='Inputs')
                uploadFile(filename, SPECIES_ID, bucketName='Species')

                # Update job status
                update_job(JOB_ID, 'pending', species_id=SPECIES_ID)
                print("Job loaded successfully")

            else:
                print("Currently, we don't have support for the selected package.")
                raise SystemExit

        elif verify_file_extension(filename, ['.nw']):

            # Argument input
            JOB_NAME = input('Enter the job name: ')
            JOB_DESCRIPTION = input('Enter the job description: ')
            package = available_packages[0]
            operation = get_word_at_position(filename, 'task', 2)

            # Insert job and species
            print("Loading job:", filename)
            JOB_ID = insert_job(JOB_NAME, package, operation, JOB_DESCRIPTION)
            SPECIES_ID = insert_species(f"{JOB_ID}.sdf")
            print("Job id:", JOB_ID)
            replace_start_directive(filename, JOB_ID)

            # Convert nwchem to xyz and then to sdf
            nwchem_to_xyz(filename, f"{JOB_ID}.xyz")
            convert_xyz_to_sdf(f"{JOB_ID}.xyz", f"{JOB_ID}.sdf")

            # Upload files
            uploadFile(filename, JOB_ID, bucketName='Inputs')
            uploadFile(f"{JOB_ID}.sdf", SPECIES_ID, bucketName='Species')

            # Update job status
            update_job(JOB_ID, 'pending', species_id=SPECIES_ID)

            # Clean up
            cleanUp(JOB_ID)
            cleanUp(SPECIES_ID)
            print("Job loaded successfully")

        else:

            print("The file extension is not supported.")
            raise SystemExit

    else:

        print(f"The file {filename} does not exist.")
        raise SystemExit


def load_project(directory: str, extension='.sdf'):
    """
    Load a project from a directory.

    Args:
        directory (str): The directory path.
        extension (str, optional): The file extension to filter. Defaults to '.sdf'.

    Raises:
        SystemExit: If the directory does not exist or the package is not supported.
    """
    if not directory.endswith('/'):
        directory += '/'

    if exists(directory):
        name = input('Enter the project name: ')
        description = input('Enter the project description: ')
        packages = create_string_array("Enter the packages (q to quit): ")

        for package in packages:
            if not check_packages([package], available_packages):
                print(
                    f"Currently, we don't have support for the {package} package.")
                raise SystemExit

        files = get_files_with_extension(directory, extension)
        print("Files with extension", extension,
              "in directory", directory, ":", files)
        basis_sets = create_string_array("Enter basis sets (q to quit): ")
        functionals = create_string_array("Enter functionals (q to quit): ")
        # Warning the multiplicity is sytem dependent, modify it
        charge_multiplicities = create_charge_multiplicity_array(
            "Enter charge and then multiplicity (q to quit): ")
        operations = create_string_array(
            "Enter operations in the order required (q to quit): ")

        required_Job = None

        total_iterations = len(packages) * len(basis_sets) * len(functionals) * len(charge_multiplicities) * len(files) * len(operations)
        progress_bar = tqdm(total=total_iterations, desc="Processing")

        for package in packages:
            if package == available_packages[0]:
                for basis, functional, charge_multiplicity in itertools.product(basis_sets, functionals, charge_multiplicities):
                    for file in files:
                        for operation in operations:
                            charge, multiplicity = charge_multiplicity
                            path = directory + file

                            job_id = insert_job(
                                file,
                                package,
                                operation,
                                f"{file} - {charge_multiplicity} - {functional}{basis} - {operation}",
                                charge=charge,
                                multiplicity=multiplicity,
                                functional=functional,
                                basisSet=basis,
                                requiredJobId=required_Job  # type: ignore
                            )

                            if required_Job is None:

                                # Generate input file
                                generate_nwchem_input_from_sdf(
                                    path,
                                    basis,
                                    charge,
                                    job_id,
                                    functional=functional,
                                    multiplicity=multiplicity,
                                    operation="freq" if (operation.upper() ==
                                                           'COSMO') else operation,
                                    cosmo=True if (
                                        operation.upper() == 'COSMO') else False
                                )

                                # Upload input file
                                uploadFile(path.replace('.sdf', '.nw'),
                                           job_id, bucketName='Inputs')

                                # Insert species
                                species_id = insert_species(path)
                                uploadFile(path, species_id, bucketName='Species')

                                # Update job status
                                update_job(job_id, 'pending',
                                           species_id=species_id)  # type: ignore
                            else:
                                update_job(job_id, 'pending')

                            required_Job = job_id

                            # Update progress bar
                            progress_bar.update(1)

                        required_Job = None

        progress_bar.close()

        print_color("Project loaded successfully", '34')

    else:
        print(f"The directory {directory} does not exist.")
        raise SystemExit


def check_packages(packages: list, available_packages: list) -> bool:
    """
    Check if a list of packages is supported.

    Args:
        packages (list): The list of packages to check.
        available_packages (list): The list of available packages.

    Returns:
        bool: True if all packages are supported, False otherwise.
    """
    return all(package in available_packages for package in packages)
