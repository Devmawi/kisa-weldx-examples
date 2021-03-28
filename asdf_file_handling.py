import asdf

import weldx
import weldx.asdf
from weldx import Q_ # pint quantity from the weldx package
from weldx.asdf.extension import WeldxAsdfExtension, WeldxExtension
from weldx.welding.groove.iso_9692_1 import get_groove, IsoBaseGroove, _create_test_grooves, FFGroove
from weldx.geometry import Shape, LineSegment

import io


if __name__ == "__main__":

    example_groove = list(_create_test_grooves().values())[0][0]
    seam_length = Q_(300, "mm")
    tree = {"workpiece": {"groove": example_groove, "length": Q_(seam_length, "mm") }}

    # use asdf directly
    asdf_file = asdf.AsdfFile(tree)
    asdf_file.write_to("vgroove.asdf")
    new_asdf_file = asdf.open("vgroove.asdf")
    print(new_asdf_file.tree)
    # see more under https://asdf.readthedocs.io/en/stable/asdf/overview.html#creating-files

    # some manipulation
    new_asdf_file.tree["workpiece"]["length"] = Q_(400, "mm")

    # use BytesIO object
    memory_buffer = weldx.asdf.util.write_buffer(new_asdf_file.tree)
    with open("vgroove_2.asdf", "wb") as open_asdf_file:
        open_asdf_file.write(memory_buffer.getbuffer())

    with io.open("vgroove_2.asdf", "rb") as open_asdf_file:
        file_bytes = open_asdf_file.read()
        new_memory_buffer = io.BytesIO(file_bytes)
   
    new_asdf_tree = weldx.asdf.util.read_buffer(new_memory_buffer)
    new_asdf_file = asdf.AsdfFile(new_asdf_tree)
    print(new_asdf_file.tree)

    # some actions with the memory stream
    yaml_header = weldx.asdf.util.get_yaml_header(new_memory_buffer)
    print(yaml_header)