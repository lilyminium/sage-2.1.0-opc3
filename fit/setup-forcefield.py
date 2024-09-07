import pathlib

import click


from rdkit import Chem
from openff.toolkit.typing.engines.smirnoff import ForceField

@click.command()
@click.option(
    "--input",
    "input_forcefield",
    type=str,
    default="openff-2.1.0.offxml",
    help="The input forcefield file",
)
@click.option(
    "--water",
    "water_forcefield",
    type=str,
    default="opc3.offxml",
    help="The water forcefield file",
)
@click.option(
    "--output",
    "output_forcefield",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
    default="forcefield/force-field.offxml",
    help="The output forcefield file",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Print verbose output",
)
def main(
    input_forcefield: str = "openff-2.1.0.offxml",
    water_forcefield: str = "opc3.offxml",
    output_forcefield: str = "forcefield/force-field.offxml", 
    verbose: bool = False,
):
    forcefield = ForceField(input_forcefield)

    # remove tip3p parameters if they exist
    for parameter_handler in forcefield._parameter_handlers.values():
        to_remove = []
        for parameter in parameter_handler.parameters:
            if "tip3p" in parameter.id:
                to_remove.append(parameter)
                if verbose:
                    print(f"Removing {parameter.id} with pattern {parameter.smirks}")
        for parameter in to_remove:
            parameter_handler.parameters.remove(parameter)

    # just remove library charges as they're all ions or waters
    forcefield.deregister_parameter_handler("LibraryCharges")

    # remove vdW ions. All charged atoms are the metal ions
    handler = forcefield.get_parameter_handler("vdW")
    to_remove = []
    for parameter in handler.parameters:
        rdmol = Chem.MolFromSmarts(parameter.smirks)
        rdatom = next(atom for atom in rdmol.GetAtoms() if atom.GetAtomMapNum() == 1)
        if rdatom.GetFormalCharge() != 0:
            to_remove.append(parameter)
            if verbose:
                print(f"Removing {parameter.id} with pattern {parameter.smirks}")
    for parameter in to_remove:
        handler.parameters.remove(parameter)

    # now add new water model
    forcefield.parse_sources([water_forcefield])

    # add parameterization options
    PARAMETERS_TO_OPTIMIZE = [
        "[#16:1]",
        "[#17:1]",
        "[#1:1]-[#6X3]",
        "[#1:1]-[#6X3](~[#7,#8,#9,#16,#17,#35])~[#7,#8,#9,#16,#17,#35]",
        "[#1:1]-[#6X3]~[#7,#8,#9,#16,#17,#35]",
        "[#1:1]-[#6X4]",
        "[#1:1]-[#6X4]-[#7,#8,#9,#16,#17,#35]",
        "[#1:1]-[#7]",
        "[#1:1]-[#8]",
        "[#35:1]",
        "[#6:1]",
        "[#6X4:1]",
        "[#7:1]",
        "[#8:1]",
        "[#8X2H0+0:1]",
        "[#8X2H1+0:1]",
    ]
    for smirks in PARAMETERS_TO_OPTIMIZE:
        parameter = handler[smirks]
        parameter.add_cosmetic_attribute("parameterize", "epsilon, rmin_half")

    # write out to file
    output_file = pathlib.Path(output_forcefield)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    forcefield.to_file(output_forcefield)
    print(f"Forcefield written to {output_forcefield}")


if __name__ == "__main__":
    main()