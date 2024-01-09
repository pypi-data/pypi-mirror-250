# success

from rdkit import Chem


def read_sdf_coordinates(sdf_file):
    """
    Read molecular coordinates from an SDF file.

    Parameters:
    - sdf_file (str): Path to the SDF file.

    Returns:
    - str: XYZ coordinates of the molecular geometry.
    """
    mol_supplier = Chem.SDMolSupplier(sdf_file)
    mol = next(mol_supplier)
    if mol is not None:
        # Extract atomic coordinates
        coordinates = []
        for atom in mol.GetAtoms():
            pos = mol.GetConformer().GetAtomPosition(atom.GetIdx())
            coordinates.append(
                f"  {atom.GetSymbol()} {pos.x:.8f} {pos.y:.8f} {pos.z:.8f}"
            )

        return "\n".join(coordinates)


def generate_nwchem_input_from_sdf(
    sdf_file,
    basis_set,
    title="Hartree-Fock Calculation",
    method="dft",
    functional="b3lyp",
    multiplicity=1,  # Default to singlet (closed-shell)
    frequency=True,
):
    """
    Generate NWChem input file for a DFT calculation with an option for a frequency calculation using coordinates from an SDF file.

    Parameters:
    - sdf_file (str): Path to the SDF file containing molecular coordinates.
    - basis_set (str): Basis set to be used in the calculation.
    - title (str): Title for the NWChem input file.
    - method (str): NWChem calculation method (e.g., "scf", "dft", etc.).
    - functional (str): DFT functional to be used in the calculation.
    - multiplicity (int): Multiplicity of the system (1 for singlet, 2 for doublet, etc.).
    - frequency (bool): Whether to include a frequency calculation in the input file.
    """
    molecule = read_sdf_coordinates(sdf_file)

    if molecule is None:
        print("Error: Unable to read molecular coordinates from SDF file.")
        return

    input_content = f"""
start {method}
title "{title}"

geometry units au
{molecule}
end

basis
 * library {basis_set}
end

{method}
  xc {functional}
  mult {multiplicity}
end
"""

    if frequency:
        input_content += f"""
task {method} freq
"""

    with open(sdf_file.replace(".sdf", ".nw"), "w") as file:
        file.write(input_content)


# Example usage:
if __name__ == "__main__":
    generate_nwchem_input_from_sdf(
        "molecule.sdf",
        "6-31G*",
        title="DFT Frequency Calculation",
        method="dft",
        functional="b3lyp",
        multiplicity=2,
        frequency=True,
    )
