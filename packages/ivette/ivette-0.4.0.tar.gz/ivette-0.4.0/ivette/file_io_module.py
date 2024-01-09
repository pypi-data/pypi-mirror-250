"""
This module provides functions for reading and manipulating molecular geometry files.
"""

import os
import re
from openbabel import pybel
from rdkit import Chem

from ivette.types import Step, ThermoData


def read_sdf_coordinates(sdf_file):
    """
    Read molecular coordinates from an SDF file.

    Parameters:
    - sdf_file (str): Path to the SDF file.

    Returns:
    - str: XYZ coordinates of the molecular geometry.

    This function reads molecular coordinates from an SDF file using RDKit.

    Parameters:
    - sdf_file (str): The path to the SDF file.

    Returns:
    - str: A string containing XYZ coordinates of the molecular geometry.

    Example:
    >>> sdf_file_path = 'molecule.sdf'
    >>> coordinates = read_sdf_coordinates(sdf_file_path)
    >>> print(coordinates)
    C 0.00000000 0.00000000 0.00000000
    H 1.00000000 0.00000000 0.00000000
    ...

    Note:
    The function uses RDKit's Chem module to read the SDF file and extract atomic coordinates.
    It returns a formatted string with XYZ coordinates for each atom.

    """  # Up to date
    # Use RDKit to read the SDF file and obtain a molecule object
    mol_supplier = Chem.SDMolSupplier(sdf_file, removeHs=False) # type: ignore
    mol = next(mol_supplier)

    # Check if a molecule is successfully obtained
    if mol is not None:
        # Extract atomic coordinates
        coordinates = [
            f"  {atom.GetSymbol()} {pos.x:.8f} {pos.y:.8f} {pos.z:.8f}"
            for atom in mol.GetAtoms()
            for pos in [mol.GetConformer().GetAtomPosition(atom.GetIdx())]
        ]

        return "\n".join(coordinates)

    return "Error: Unable to read molecular coordinates from SDF file."


def nwchem_to_xyz(nw_filename, xyz_filename):
    """
    Convert NWChem input file to XYZ file.

    Parameters:
    - nw_filename (str): Path to the NWChem input file.
    - xyz_filename (str): Path to the output XYZ file.

    This function reads atomic coordinates from an NWChem input file and writes them to an XYZ file.

    Parameters:
    - nw_filename (str): The path to the NWChem input file.
    - xyz_filename (str): The path to the output XYZ file.

    Example:
    >>> nwchem_input_path = 'input.nw'
    >>> xyz_output_path = 'output.xyz'
    >>> nwchem_to_xyz(nwchem_input_path, xyz_output_path)

    Note:
    The function searches for atomic coordinates in the NWChem input file 
    between 'geometry' and 'end' keywords.
    It then writes the atomic coordinates to the specified XYZ file.

    """  # Up to date
    # Read NWChem input file
    with open(nw_filename, 'r', encoding='utf-8') as nw_file:
        nw_lines = nw_file.readlines()

    # Extract atomic coordinates
    atomic_coordinates = []
    start_reading_coordinates = False
    for line in nw_lines:
        if 'geometry' in line.lower():
            start_reading_coordinates = True
        elif 'end' in line.lower() and start_reading_coordinates:
            break
        elif start_reading_coordinates:
            tokens = line.split()
            if len(tokens) >= 4:
                element, x, y, z = tokens[:4]
                atomic_coordinates.append(
                    (element, float(x), float(y), float(z)))

    # Write XYZ file
    with open(xyz_filename, 'w') as xyz_file:
        xyz_file.write(f"{len(atomic_coordinates)}\n")
        xyz_file.write("Converted from NWChem input file\n")
        for atom in atomic_coordinates:
            xyz_file.write(
                f"{atom[0]} {atom[1]:.6f} {atom[2]:.6f} {atom[3]:.6f}\n")


def convert_xyz_to_sdf(input_file, output_file):
    """
    Convert a NWChem input file to a .sdf file using Open Babel.

    Parameters:
    - input_file (str): Path to the input NWChem file.
    - output_file (str): Path to the output .sdf file.
    """
    # Create an Open Babel molecule object
    mol_generator = pybel.readfile("xyz", input_file)
    mol = next(mol_generator)

    # Output the molecule to a .sdf file
    with open(output_file, 'w') as sdf_file:
        sdf_file.write(mol.write("sdf")) # type: ignore


def generate_nwchem_input_from_sdf(
    sdf_file,
    basis_set,
    charge=0,  # Default to neutral charge
    title="Hartree-Fock Calculation",
    mem="200 MB",
    method="dft",
    functional="b3lyp",
    multiplicity=1,  # Default to singlet (closed-shell)
    operation='energy',
    ncycles='200',
    maxiter='200',
    *,
    cosmo=False
):
    """
    Generate NWChem input file for a DFT calculation with an option for a frequency calculation using coordinates from an SDF file.

    Parameters:
    - sdf_file (str): Path to the SDF file containing molecular coordinates.
    - basis_set (str): Basis set to be used in the calculation.
    - charge (int): Charge of the system.
    - title (str): Title for the NWChem input file.
    - method (str): NWChem calculation method (e.g., "scf", "dft", etc.).
    - functional (str): DFT functional to be used in the calculation.
    - multiplicity (int): Multiplicity of the system (1 for singlet, 2 for doublet, etc.).
    - mem (str): Memory to be used per thread.
    """
    molecule = read_sdf_coordinates(sdf_file)

    if molecule is None:
        print("Error: Unable to read molecular coordinates from SDF file.")
        return

    input_content = f"""
start {title}
title "{title}"

memory total {mem}

charge {charge}

geometry
{molecule}
end

basis
 * library {basis_set}
end

{method}
  xc {functional}
  mult {multiplicity}
  iterations {ncycles}
end

cosmo
    {"" if cosmo else "off"}
end

driver
  {"loose" if charge != 0 or multiplicity != 1 else "tight"}
  maxiter {maxiter}
end

task {method} {operation}
"""

    with open(sdf_file.replace(".sdf", ".nw"), "w") as file:
        file.write(input_content)


def replace_start_directive(file_path, new_start_directive):
    try:
        # Read the content of the file
        with open(file_path, 'r') as file:
            content = file.read()

        # Find the start directive using a regular expression
        pattern = re.compile(r'^\s*start\s+\S+', re.MULTILINE)
        match = pattern.search(content)

        if match:
            # Replace the start directive with the new string
            updated_content = content[:match.start(
            )] + f"start {new_start_directive}" + content[match.end():]

            # Write the updated content back to the file
            with open(file_path, 'w') as file:
                file.write(updated_content)

        else:
            print("No start directive found in the file.")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")


def get_files_with_extension(directory: str, extension: str):
    """
    Get a list of files with a specific extension in a directory.

    Args:
        directory (str): The directory path.
        extension (str): The file extension.

    Returns:
        list: A list of file names.
    """
    files = [file for file in os.listdir(
        directory) if file.endswith(extension)]
    return files


def get_word_at_position(file_path, keyword, position):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if keyword in line:
                    # Split the line into words and get the word at the specified position
                    words = line.strip().split()
                    if len(words) > position:
                        return words[position]
                    else:
                        return f"Not enough words in the line for position {position}."

            return f"No '{keyword}' line found in the file."

    except FileNotFoundError:
        return f"File '{file_path}' not found."


def extract_geometries(file_path, output_xyz_file, geometry_index=-1):
    with open(file_path, 'r') as file:
        content = file.read()

        # Define the start and end patterns
        start_pattern = r"Output coordinates in angstroms \(scale by  1\.889725989 to convert to a\.u\.\)"
        end_pattern = r"Effective nuclear repulsion energy \(a\.u\.\)"

        # Find all geometry sections in the content using regex
        geometry_patterns = re.finditer(
            f"{start_pattern}(.*?){end_pattern}", content, re.DOTALL)

        geometries = []

        for geometry_match in geometry_patterns:
            geometry_content = geometry_match.group(1)

            # Extract rows from the geometry section
            rows = re.findall(
                r"\s+(\d+)\s+(\S+)\s+([\d.-]+)\s+([\d.-]+)\s+([\d.-]+)\s+([\d.-]+)", geometry_content)

            # Convert rows to a list of dictionaries
            geometry_data = []
            for row in rows:
                geometry_data.append({
                    "Atom_No": int(row[0]),
                    "Atom_Tag": row[1],
                    "Charge": float(row[2]),
                    # Conversion of units is carried in this step
                    "X": float(row[3]),
                    "Y": float(row[4]),
                    "Z": float(row[5]),
                })

            geometries.append(geometry_data)

    if geometries:
        # Check if the specified geometry index is within range
        if geometry_index >= -len(geometries) and geometry_index < len(geometries):
            selected_geometry = geometries[geometry_index]

            # Write the selected geometry to an XYZ file
            with open(output_xyz_file, 'w') as file:
                # Write the number of atoms
                file.write(f"{len(selected_geometry)}\n")

                # Write a comment line
                file.write("Generated by NWChem Geometry Extractor\n")

                # Write atom coordinates
                for row in selected_geometry:
                    file.write(
                        f"{row['Atom_Tag']} {row['X']} {row['Y']} {row['Z']}\n")

        else:
            print("Invalid geometry index.")
    else:
        print("No geometries found in the NWChem output file.")


def get_total_dft_energy(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if 'Total DFT energy' in line:  # replace 'energy' with the actual keyword
                # assumes the energy value is after an '=' sign
                energy = float(line.split('=')[-1].strip())
                return energy


def get_step_data(filepath, step_index=-1):
    # Validate that the file exists
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"The file {filepath} does not exist.")

    with open(filepath, 'r') as file:
        content = file.read()

    matches = re.findall(
        r'^@\s*(\d+)\s*([-+]?\d+(\.\d+)?(D|e)?[-+]?\d*)\s*([-+]?\d+(\.\d+)?(D|e)?[-+]?\d*)\s*([-+]?\d+(\.\d+)?(D|e)?[-+]?\d*)\s*([-+]?\d+(\.\d+)?(D|e)?[-+]?\d*)\s*([-+]?\d+(\.\d+)?(D|e)?[-+]?\d*)\s*([-+]?\d+(\.\d+)?(D|e)?[-+]?\d*)\s*([-+]?\d+(\.\d+)?(D|e)?[-+]?\d*)',
        content, re.MULTILINE)

    if matches:
        if step_index < 0:
            step_index = len(matches) + step_index
        if step_index >= len(matches) or step_index < 0:
            return None

        step = int(matches[step_index][0])
        energy = float(matches[step_index][1].replace('D', 'e'))
        delta_e = float(matches[step_index][4].replace('D', 'e'))
        gmax = float(matches[step_index][7].replace('D', 'e'))
        grms = float(matches[step_index][10].replace('D', 'e'))
        xrms = float(matches[step_index][13].replace('D', 'e'))
        xmax = float(matches[step_index][16].replace('D', 'e'))
        walltime = float(matches[step_index][19].replace('D', ''))

        return Step(step, energy, delta_e, gmax, grms, xrms, xmax, walltime)

    return None


def get_thermo_data(file_path, *, thermo_data=ThermoData()):
    # flag to check if 'cv (constant volume heat capacity)' line has passed
    cv_passed = False
    with open(file_path, 'r') as file:
        for line in file:
            line = line.lower().strip()  # convert line to lower case and strip spaces
            if 'temperature' in line:
                thermo_data.temp = float(
                    line.split('=')[1].split('k')[0].strip())
            elif 'frequency scaling parameter' in line:
                thermo_data.freq_scale = float(line.split('=')[1].strip())
            elif 'zero-point correction to energy' in line:
                thermo_data.zpe = float(line.split(
                    '=')[1].split('kcal')[0].strip())
            elif 'thermal correction to energy' in line:
                thermo_data.te = float(line.split(
                    '=')[1].split('kcal')[0].strip())
            elif 'thermal correction to enthalpy' in line:
                thermo_data.th = float(line.split(
                    '=')[1].split('kcal')[0].strip())
            elif 'total entropy' in line:
                thermo_data.ts = float(line.split(
                    '=')[1].split('cal')[0].strip())
            elif '- translational' in line and not cv_passed:
                thermo_data.ts_trans = float(
                    line.split('=')[1].split('cal')[0].strip())
            elif '- rotational' in line and not cv_passed:
                thermo_data.ts_rot = float(
                    line.split('=')[1].split('cal')[0].strip())
            elif '- vibrational' in line and not cv_passed:
                thermo_data.ts_vib = float(
                    line.split('=')[1].split('cal')[0].strip())
            elif 'cv (constant volume heat capacity)' in line:
                thermo_data.cv = float(line.split(
                    '=')[1].split('cal')[0].strip())
                # set the flag to True after 'cv (constant volume heat capacity)' line
                cv_passed = True
            # only check for translational, rotational, and vibrational Cv values after 'cv (constant volume heat capacity)' line
            elif cv_passed:
                if '- translational' in line:
                    thermo_data.cv_trans = float(
                        line.split('=')[1].split('cal')[0].strip())
                elif '- rotational' in line:
                    thermo_data.cv_rot = float(
                        line.split('=')[1].split('cal')[0].strip())
                elif '- vibrational' in line:
                    thermo_data.cv_vib = float(
                        line.split('=')[1].split('cal')[0].strip())
    return thermo_data


def trim_file(filename, desired_size_mb):
    # Calculate the number of lines in the file
    with open(filename, 'r') as file:
        lines = file.readlines()
    total_lines = len(lines)

    # Calculate the current size of the file in MB
    current_size_mb = os.path.getsize(filename) / (1024 * 1024)

    # If the current size is less than or equal to the desired size, do nothing
    if current_size_mb <= desired_size_mb:
        return

    # Calculate the number of lines to keep based on the desired size
    lines_to_keep = int(total_lines * desired_size_mb / current_size_mb)

    # Calculate the number of lines to keep from the beginning and the end
    start_lines = lines_to_keep // 2
    end_lines = lines_to_keep - start_lines

    # Get the lines to keep
    new_lines = lines[
        :start_lines
    ] + [
        '\n\n... this file was trimmed to reduce size\n\n'
    ] + lines[
        -end_lines:
    ]

    # Write the new lines back to the file
    with open(filename, 'w') as file:
        file.writelines(new_lines)
