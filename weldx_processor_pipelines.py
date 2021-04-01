from weldx_processors import *
import asdf
import weldx
from weldx.welding.groove.iso_9692_1 import _create_test_grooves

def run_pipeline(file:asdf.AsdfFile, steps):

    tmp_file = file
    for step in steps:
        tmp_file = step(tmp_file)

    return tmp_file

if __name__ == "__main__":

    example_groove = list(_create_test_grooves().values())[0][0]
    tree = {"workpiece": {"groove": example_groove}}
    file = asdf.AsdfFile(tree)

    new_file = run_pipeline(file, steps=[add_seam_length, add_pulse_ui, add_process_spray])
    print(new_file.tree)