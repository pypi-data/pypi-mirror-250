"""Design tools.
"""

from pyaedt.modules.MaterialLib import Materials


def import_materials(materials: Materials, material: str | list[str]) -> None:
    """Import materials from the system lib.

    :param pyaedt.modules.MaterialLib.Materials materials: AEDT material database
    :param str | list[str] material: The name of materials to be imported
    """
    if not isinstance(material, list):
        material = [material]
    for mat in material:
        materials.checkifmaterialexists(mat)
