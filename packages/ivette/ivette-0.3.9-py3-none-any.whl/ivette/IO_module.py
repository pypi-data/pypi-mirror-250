import re
import os
import shutil
import time
import platform
import uuid

from ivette.supabase_module import get_next_job, update_job
from ivette.types import SystemInfo


def file_exists(filename: str, directory="/"):
    """
    Check if a file exists at the given file path.

    ## Args:
    - file_path (str): The path to the file.

    ## Returns:
    - bool: True if the file exists, False otherwise.

    ## Example:
    if file_exists(args):
        print(f"The file '{args}' exists.")
    else:
        print(f"The file '{args}' does not exist.")
    """

    file_path = directory + filename
    return os.path.exists(file_path)


def check_gamess_installation():
    try:
        # Check if the 'rungms' executable is in the system's PATH
        if shutil.which("rungms") is not None:
            return True
        else:
            print("GAMESS is not installed on the system.")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def setUp(server_id = None):
    "returns id and package"
    JOB = None
    INTERVAL = 30  # seconds
    print(f"\n>  Checking for jobs every {INTERVAL} seconds.", end="\r", flush=True)

    while True:

        try:

            JOB = get_next_job(server_id)

        except KeyboardInterrupt:
            if JOB:
                cleanUp(JOB[0])
                update_job(JOB[0], "interrupted", nproc=0)
                raise SystemExit
            else:
                print("No job to interrupt.            ")
                continue

        if JOB is None:
            for remaining in range(INTERVAL, 0, -1):
                print(
                    f">  No jobs due. Checking again in {remaining} seconds.",
                    end="\r",
                )
                time.sleep(1)
                # Clear the countdown timer
                print(
                    " "
                    * len(
                        f">  No jobs due. Checking again in {remaining} seconds."
                    ),
                    end="\r",
                )
        else:
            id, package, operation = JOB
            break

    # Create a new folder
    folder_name = "tmp"
    if not exists(folder_name):
        # If it doesn't exist, create the folder
        os.mkdir(folder_name)

    return (id, package, operation)


def exists(path):
    """
    Verifies if a path exists.

    Args:
        path (str): The path to be verified.

    Returns:
        bool: True if the path exists, False otherwise.
    """
    return os.path.exists(path)


def cleanUp(prefix):
    for filename in os.listdir():
        if filename.startswith(prefix):
            os.remove(filename)

    # Check if the "tmp" subdirectory exists and then remove it
    tmp_dir = os.path.join(os.getcwd(), "tmp")
    if os.path.exists(tmp_dir) and os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)

    # Check if the "cosmo.xyz" file exists and then remove it
    cosmo_file = os.path.join(os.getcwd(), "cosmo.xyz")
    if os.path.exists(cosmo_file):
        os.remove(cosmo_file)


def validate_filename(filename, allowed_extensions=[".inp"]):
    """
    Validates a filename to ensure it ends with one of the allowed extensions.

    Args:
        filename (str): The filename to be validated.
        allowed_extensions (list): A list of allowed file extensions. Default is ['.log', '.out', '.txt', '.inp'].

    Returns:
        str: The valid filename.

    Raises:
        None

    This function checks whether the provided 'filename' ends with one of the 'allowed_extensions'. If the
    'filename' is valid, it returns the filename. If not, it repeatedly prompts the user to enter a valid
    filename until a valid one is provided.

    Example usage:
    >>> filename = validate_filename(input("Enter a filename: "))
    >>> print(f"Valid filename: {filename}")

    Note:
    - The function uses regular expressions to perform a case-insensitive check on the file extension.
    - If the 'filename' provided by the user does not end with a valid extension, the user will be prompted
      to provide a valid filename until a valid one is given.
    - The list of 'allowed_extensions' determines the file extensions that are considered valid. By default,
      the function allows '.log', '.out', '.txt', and '.inp' extensions, but you can customize this list
      by providing your own list of allowed extensions.
    """
    while True:
        # Use regular expressions to check if the filename ends with a valid extension (case-insensitive)
        if re.search(r"\.(log|out|txt|inp)$", filename, re.IGNORECASE):
            return filename
        else:
            print(f"Invalid extension. Please use one of {allowed_extensions}")
        filename = input("Enter a valid filename: ")


def get_cpu_core_count():
    """
    Determine the number of CPU cores available on the system.

    Returns:
        int: The number of CPU cores available.

    Raises:
        None

    This function attempts to retrieve the number of CPU cores available on the system using the
    `os.cpu_count()` function. If successful, it returns the actual number of CPU cores. If there is an issue
    with determining the core count (e.g., due to an AttributeError or NotImplementedError), the function
    returns a reasonable default value of 4.

    Note:
    - The number of CPU cores is a significant factor in parallel computing and multi-threaded applications.
    - The default value of 4 is returned as a reasonable assumption when the core count cannot be determined.
    """
    try:
        return os.cpu_count()
    except (AttributeError, NotImplementedError):
        # If the number of CPU cores cannot be determined, return a reasonable default value
        return 4


def validate_cpu_core_input(input_str):
    """
    Validate user input for selecting the number of CPU cores.

    Args:
        input_str (str): The user's input as a string.

    Returns:
        int: The validated number of CPU cores if it falls within the allowed range, or None if the input is invalid.

    Raises:
        None

    This function attempts to validate the user's input for selecting the number of CPU cores. It first tries to
    convert the input string to an integer. If successful, it checks whether the input is within the allowed range
    (from 1 to the number of available CPU cores, inclusive). If the input is valid, it returns the selected number
    of CPU cores. If the input is outside the allowed range, an error message is displayed, and None is returned.
    If the input is not a valid integer, another error message is displayed, and None is returned.

    Note:
    - The function relies on the `get_cpu_core_count()` function to determine the number of available CPU cores on
      the system.
    - The user is guided to enter a valid integer within the appropriate range, and error messages are displayed to
      provide feedback in case of input errors.
    """
    try:
        # Attempt to convert the input string to an integer
        input_value = int(input_str)
        cpu_core_count = get_cpu_core_count()  # Get the number of available CPU cores

        # Check if the input is within the valid range (1 to the number of CPU cores)
        if cpu_core_count is not None and 1 <= input_value <= cpu_core_count:
            return input_value  # Return the selected core count
        else:
            if cpu_core_count is None:
                print("Unable to determine the number of CPU cores.")
            else:
                print(f"Please enter an integer between 1 and {cpu_core_count}.")
            return None
    except ValueError:
        print("Please enter a valid integer.")
        return None


def setCPU():
    cpu_core_count = get_cpu_core_count()
    print(f"Your computer has {cpu_core_count} CPU core(s).")

    while True:
        user_input = input("Enter the number of CPU cores to use: ")
        validated_input = validate_cpu_core_input(user_input)

        if validated_input is not None:
            return validated_input


def get_valid_input(prompt, n, m):
    while True:
        try:
            user_input = int(input(prompt))
            if n <= user_input <= m:
                return user_input
            else:
                print(f"Please enter an integer between {n} and {m}.\n")
        except ValueError:
            print("Invalid input. Please enter a valid integer.\n")


def is_nwchem_installed():
    return shutil.which("nwchem") is not None


def waiting_message(process: str):
    # Create an animated "Waiting" message using Braille characters
    waiting_message = "⣾⣷⣯⣟⡿⢿⣻⣽"  # Customize this as needed

    for braille_char in waiting_message:
        print(f"   Running {process} Job {braille_char}", end="\r", flush=True)
        time.sleep(0.1)


def verify_file_extension(filename, allowed_extensions):
    """
    Verify if the given filename has an allowed extension.

    Parameters:
    - filename (str): The name of the file to be verified.
    - allowed_extensions (list): A list of allowed extensions (e.g., ['.txt', '.jpg', '.png']).

    Returns:
    - bool: True if the file has an allowed extension, False otherwise.
    """
    # Get the file extension
    _, file_extension = os.path.splitext(filename)

    # Check if the file extension is in the list of allowed extensions
    return file_extension.lower() in allowed_extensions


def create_string_array(prompt: str) -> list:
    """
    Create a list of strings from user input.

    Args:
        prompt (str): The prompt message.

    Returns:
        list: A list of strings.
    """
    string_array = []
    while True:
        string = input(prompt)
        if string == 'q':
            break
        string_array.append(string)
    return string_array


def create_charge_multiplicity_array(prompt: str) -> list:
    """
    Create a list of charge-multiplicity pairs from user input.

    Args:
        prompt (str): The prompt message.

    Returns:
        list: A list of charge-multiplicity pairs.
    """
    charge_multiplicity_array = []
    while True:
        charge = input("Enter charge (q to quit): ")
        if charge == 'q':
            break
        multiplicity = input("Enter multiplicity: ")
        charge_multiplicity_array.append([charge, multiplicity])
    return charge_multiplicity_array


def system_info():
    info = SystemInfo(
        system_id=str(uuid.getnode()),
        system=platform.system(),
        node=platform.node(),
        release=platform.release(),
        version=platform.version(),
        machine=platform.machine(),
        processor=platform.processor(),
        ntotal=get_cpu_core_count() or 0  # Assign a default value of 0 if get_cpu_core_count() returns None
    )
    return info
