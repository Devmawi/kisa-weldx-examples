""" Base64 encoding and decoding is useful if you want to interop with other languages,
for example C# or transfer a WelDX file by an api request """

import asdf

import weldx
import weldx.asdf
from weldx import Q_ # pint quantity from the weldx package
from weldx.asdf.extension import WeldxAsdfExtension, WeldxExtension
from weldx.welding.groove.iso_9692_1 import get_groove, IsoBaseGroove, _create_test_grooves, FFGroove
from weldx.geometry import Shape, LineSegment

import io
import base64


def base64_encode():

    example_groove = list(_create_test_grooves().values())[0][0]
    seam_length = Q_(300, "mm")
    tree = {"workpiece": {"groove": example_groove, "length": Q_(seam_length, "mm") }}
    file_buffer = weldx.asdf.util._write_buffer(tree)
    base64_string = base64.b64encode(file_buffer.getvalue()).decode()
    return base64_string


def base64_decode(base64_string:str):

    asdf_buffer = io.BytesIO(base64.b64decode(base64_string))
    asdf_tree = weldx.asdf.util._read_buffer(asdf_buffer)    
    return asdf_tree


if __name__ == "__main__":

    base64_string = base64_encode()
    asdf_tree = base64_decode(base64_string)
    workpiece: dict = asdf_tree["workpiece"]
    groove = workpiece["groove"]
    seam_length: Q_ = workpiece["length"]

    print(groove)
    
    
