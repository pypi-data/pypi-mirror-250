from urllib import response
import httpcore
import httpx

from typing import Optional
from supabase.client import create_client, Client
from dotenv import load_dotenv
from ivette.decorators import http_request
from ivette.file_io_module import trim_file
from ivette.types import Step, SystemInfo, ThermoData

# Create Client
load_dotenv()

# url: str = os.getenv("SUPABASE_URL")
# key: str = os.getenv("SUPABASE_KEY")
# supabase: Client = create_client(url, key)

url: str = 'https://fqvgwdjfezlvwmikqapp.supabase.co'
key: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZxdmd3ZGpmZXpsdndtaWtxYXBwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDAyMjg3NTgsImV4cCI6MjAxNTgwNDc1OH0.7BJ0rKe8ZvOfw9h4h5-LbKuvBYgnZoMGJYuM_QmKmlY'
supabase: Client = create_client(url, key)


@http_request
def downloadFile(filename: str, dir='', bucketDir='', bucket_name='ivette', *, extension=''):
    """
    Download a file from a remote storage bucket and save it locally.

    Args:
        filename (str): The name of the file to be downloaded.
        dir (str, optional): The local directory where the file will be saved (default is 'pyDir').
        bucketDir (str, optional): The directory in the storage bucket where the file is located (default is 'JobQueue/').

    Returns:
        None

    Note:
    - This function is designed to download a file from a remote storage bucket (e.g., Supabase) and save it locally.
    - The 'filename' argument specifies the name of the file to be downloaded.
    - The 'dir' argument (defaulting to 'tmp/') specifies the local directory where the downloaded file will be saved.
    - The 'bucketDir' argument (defaulting to 'JobQueue/') specifies the directory in the remote storage bucket where
      the file is located.
    - The function constructs the full local path and downloads the file, saving it locally in binary mode ('wb+').
    - Make sure to have the appropriate access and credentials to access the remote storage bucket.

    Example Usage:
    downloadApi('example_file', dir='myLocalDir/', bucketDir='CustomBucket/')

    Details:
    - This function is used to download files from a remote storage bucket and is often used to retrieve files for
      local processing.
    - The 'dir' argument allows you to specify a different local directory where the downloaded file should be saved.
    - The 'bucketDir' argument allows you to specify a different directory within the storage bucket where the file
      is located.
    """
    # Construct the full path to save the downloaded file locally
    path = dir + filename

    # Open a file for writing in binary mode ('wb+')
    with open(path+extension, 'wb+') as f:
        # Download the file from the remote storage bucket (e.g., Supabase)
        res = supabase.storage.from_(bucket_name).download(bucketDir + filename)

        # Write the downloaded content to the local file
        f.write(res)


@http_request
def uploadFile(filename: str, id: str, bucketDir='', bucketName='ivette', localDir='./', *, size_MB=1):
    """
    Upload a local file to a remote storage bucket.

    Args:
        filename (str): The name of the local file to be uploaded.
        id (str): The unique identifier associated with the file (e.g., job ID).
        bucketDir (str): The directory in the storage bucket where the file will be stored.
        bucketName (str, optional): The name of the remote storage bucket (default is 'ivette-bucket').
        localDir (str, optional): The local directory where the file is located (default is 'tmp/').

    Returns:
        None

    Note:
    - This function is used to upload a local file to a remote storage bucket (e.g., Supabase).
    - The 'filename' argument specifies the name of the local file to be uploaded.
    - The 'id' argument specifies a unique identifier associated with the file, often used for naming within the bucket.
    - The 'bucketDir' argument specifies the directory in the storage bucket where the file will be stored.
    - The 'bucketName' argument (defaulting to 'ivette-bucket') specifies the name of the remote storage bucket.
    - The 'localDir' argument (defaulting to 'tmp/') specifies the local directory where the file is located.
    - The function reads the local file, creates a path in the remote storage bucket, and uploads the file.

    Example Usage:
    uploadFile('A1.log', 'clod1k4zd0000d2rh3z5l3dt1', 'Calculations/', 'my-storage-bucket', 'myLocalDir/')

    Details:
    - This function is often used to upload files to remote storage for sharing, archiving, or processing.
    - The 'bucketName' and 'localDir' arguments allow you to specify the target storage bucket and local file directory.
    - The 'bucketPath' is constructed using 'bucketDir' and 'id' to specify the exact location within the storage bucket.
    - The file is read in binary mode ('rb') and uploaded to the specified path in the remote storage bucket.
    - Ensure that you have the necessary access and credentials to upload to the remote storage bucket.
    """
    filepath = localDir + filename
    bucketPath = bucketDir + id

    # Trim the file to the specified size
    trim_file(filepath, size_MB)

    # Open the local file for reading in binary mode ('rb')
    with open(filepath, 'rb') as f:
        # Upload the file to the specified path in the remote storage bucket
        supabase.storage.from_(bucketName).upload(
            file=f, path=bucketPath, file_options={"content-type": "text/html"})


@http_request
def get_job_data(id: str):
    response = supabase.table(
        'Job'
    ).select(
        '*'
    ).eq(
        'id', id
    ).execute()

    return response.data[0]


@http_request
def get_dep_jobs(id: str):
    response = supabase.table(
        'Job'
    ).select(
        '*'
    ).eq(
        'requiredJobId', id
    ).execute()

    return response.data


@http_request
def get_next_job(server_id=None):

    try:

        done_jobs = supabase.table(
                'Job'
            ).select(
                'id'
            ).eq(
                'status', 'done'
            ).execute()

        # Extract 'id' values from dictionaries in doneJobs.data
        done_job_ids = [item['id'] for item in done_jobs.data]

        # First query to get jobs with 'pending' or 'interrupted' status
        response = supabase.table(
                'Job'
            ).select(
                '*'
            ).in_(
                'status', ['pending', 'interrupted']
            ).execute()

        # Filter the results based on 'requiredJobId'
        response = [job for job in response.data if job.get('requiredJobId') in done_job_ids]

        if len(response) == 0:

            response = supabase.table(
                'Job'
            ).select(
                '*'
            ).in_(
                'status', ['pending', 'interrupted']
            ).is_(
                'requiredJobId', 'null'
            ).execute().data

            if len(response) == 0:

                # First query to get jobs with 'skipped' status
                response = supabase.table(
                        'Job'
                    ).select(
                        '*'
                    ).eq(
                        'status', 'skipped'
                    ).execute()

                # Filter the results based on 'requiredJobId'
                response = [job for job in response.data if job.get('requiredJobId') in done_job_ids]

                if len(response) == 0:

                    response = supabase.table(
                        'Job'
                    ).select(
                        '*'
                    ).eq(
                        'status', 'skipped'
                    ).is_(
                        'requiredJobId', 'null'
                    ).execute().data

        supabase.table(
                'Job'
            ).update({
                'status': 'setting up',
                'serverId': server_id
            }).eq(
                'id', response[0].get('id')
            ).execute().data

        response = (
            response[0].get('id'),
            response[0].get('package'),
            response[0].get('operation')
        )

        return response

    except IndexError:
        return None

    # Handle connection errors
    except httpx.ConnectTimeout:
        print("Connection timeout trying again...")
    except httpx.ReadTimeout:
        print("Read timeout trying again...")
    except httpx.ConnectError:
        print("Connection error trying again...")
    except httpcore.RemoteProtocolError:
        print("Server disconnected without sending a response. Trying again...")


@http_request
def insert_job(
    name: str,
    package: str,
    operation: str,
    description='No description',
    status='loading',
    user='guest',
    charge=0,
    multiplicity=1,
    functional='b3lyp',
    basisSet='6-31G',
    requiredJobId=None
):
    response = supabase.table(
            'Job'
        ).insert({
            "name": name,
            "package": package,
            "operation": operation,
            "description": description,
            "status": status,
            "user": user,
            "charge": charge,
            "multiplicity": multiplicity,
            "functional": functional,
            "basisSet": basisSet,
            "requiredJobId": requiredJobId
        }).execute()

    return response.data[0].get('id')


@http_request
def update_job(job_id: str,
    status='done',
    nproc=0,
    species_id=None,
    *,
    thermo_data: Optional[ThermoData] = None,
):
    job_table = supabase.table('Job')
    server_table = supabase.table('Server')
    job_dict = {'status': status, 'nproc': nproc}

    # Insert thermo data if avaible
    if thermo_data and thermo_data.temp:
        thermo_data_table = supabase.table('ThermoData')
        thermo_data_dict = {
            'temp': thermo_data.temp,
            'freqScale': thermo_data.freq_scale,
            'zpe': thermo_data.zpe,
            'te': thermo_data.te,
            'th': thermo_data.th,
            'ts': thermo_data.ts,
            'tsTrans': thermo_data.ts_trans,
            'tsRot': thermo_data.ts_rot,
            'tsVib': thermo_data.ts_vib,
            'cv': thermo_data.cv,
            'cvTrans': thermo_data.cv_trans,
            'cvRot': thermo_data.cv_rot,
            'cvVib': thermo_data.cv_vib,
            'jobId': job_id
        }
        thermo_data_table.insert(thermo_data_dict).execute()

    if status == 'pending' and species_id:
        job_dict['inputSpeciesId'] = species_id

    elif status == 'done':
        if species_id:
            job_dict['outputSpeciesId'] = species_id
            job_dict['energy'] = thermo_data.energy if thermo_data else None
            job_table.update({'inputSpeciesId': species_id}).eq(
                'requiredJobId', job_id).execute()
        else:
            response = job_table.select(
                'inputSpeciesId').eq('id', job_id).execute()
            job_dict['outputSpeciesId'] = response.data[0].get(
                'inputSpeciesId')
            job_dict['energy'] = thermo_data.energy if thermo_data else None
            job_table.update({'inputSpeciesId': response.data[0].get(
                'inputSpeciesId')}).eq('requiredJobId', job_id).execute()

    elif status in ['failed', 'canceled', 'skipped']:
        def get_dependent_job_ids(id: str):
            job_ids = [id]

            def get_dependents(job_id):
                responses = job_table.select('id').eq(
                    'requiredJobId', job_id).execute().data
                for response in responses:
                    job_ids.append(response.get('id'))
                    get_dependents(response.get('id'))

            get_dependents(id)
            return job_ids

        response = job_table.select('status, serverId').eq('id', job_id).execute()
        if response.data[0].get('status') == 'in progress':
            if status == 'canceled':
                server_table.update({'status': 'cancel'}).eq('id', response.data[0].get('serverId')).execute()
            elif status == 'skipped':
                server_table.update({'status': 'skip'}).eq('id', response.data[0].get('serverId')).execute()

        job_table.update({'status': status}).in_(
            'id', get_dependent_job_ids(job_id)).execute()
        return

    elif status == 'interrupted':
        response = job_table.select(
            'status').eq('id', job_id).execute()
        if response.data[0].get('status') == 'in progress':
            job_table.update({'status': status}).eq('id', job_id).execute()
            return
        else:
            return

    job_table.update(job_dict).eq('id', job_id).execute()


@http_request
def insert_species(name: str, description='no description'):
    response = supabase.table(
            'Species'
        ).insert({
            "name": name,
            "description": description,
        }).execute()

    return response.data[0].get('id')


@http_request
def cancel_all_jobs():
    while True:
        user_input = input("Please type 'Cancel all pending jobs.' to confirm the cancellation:\n")
        if user_input == "Cancel all pending jobs.":
            response = supabase.table(
                'Job'
            ).select(
                'id'
            ).in_(
                'status', ['pending', 'interrupted', 'setting up']
            ).execute()

            # Extract 'id' values from dictionaries in doneJobs.data
            job_ids = [item['id'] for item in response.data]
            # Update the status of all undone jobs to 'canceled'
            for job_id in job_ids:
                update_job(job_id, status='canceled')
        else:
            print("Incorrect input. Please try again.")
            raise SystemExit


@http_request
def insert_step(jobId: str, step: Step):

        response = supabase.table(
            'Step'
        ).insert({
            'number': step.step,
            'energy': step.energy,
            'delta_e': step.delta_e,
            'gMax': step.gmax,
            'gRms': step.grms,
            'xRms': step.xrms,
            'xMax': step.xmax,
            'walltime': step.walltime,
            'jobId': jobId
        }).execute()

        return response.data[0].get('id')


@http_request
def upsert_server(
    system_info: SystemInfo,
    status: str,
    *,
    server_id=None
):

    try:

        if server_id:

            response = supabase.table(
                'Server'
            ).update({
                'lastTime': "now()"
            }).eq(
                'id', server_id
            ).execute().data[0]

            if response.get('status') == 'turn off':

                supabase.table(
                    'Server'
                ).update({
                    'status': 'turning off',
                    'lastTime': "now()"
                }).eq(
                    'id', server_id
                ).execute()

            else:

                supabase.table(
                    'Server'
                ).update({
                    'status': status,
                    'lastTime': "now()"
                }).eq(
                    'id', server_id
                ).execute().data[0]

        else:

            response = supabase.table(
                'Server'
            ).upsert({
                'id': system_info.system_id,
                'system': system_info.system,
                'node': system_info.node,
                'release': system_info.release,
                'version': system_info.version,
                'machine': system_info.machine,
                'processor': system_info.processor,
                'ntotal': system_info.ntotal,
                'lastTime': "now()"
            }).execute().data[0]

        return response

    except IndexError:
        return


@http_request
def server_switch(serverId: str, status: str):
    response = supabase.table(
        'Server'
    ).update({
        'status': status,
        'lastTime': "now()"
    }).eq(
        'id', serverId
    ).execute().data[0]

    return response.get('id')
