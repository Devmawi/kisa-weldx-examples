""" This example shows, what a module for 
providing dynamic weldx functions like parameter calculations, e.g. could look like """

import asdf
import weldx
import weldx.asdf
from weldx import Q_ # pint quantity from the weldx package
from weldx.asdf.extension import WeldxAsdfExtension, WeldxExtension
from weldx.welding.groove.iso_9692_1 import get_groove, IsoBaseGroove, _create_test_grooves
from weldx.core import TimeSeries as TS
from weldx.welding.processes import GmawProcess

def add_seam_length(file: asdf.AsdfFile)->asdf.AsdfFile:

    new_file = asdf.AsdfFile(file.tree) # make a copy
    new_file.tree["workpiece"]["length"] = Q_(700, "mm") # in a real case, add some error handling!
    return new_file
    

def add_process_spray(file:asdf.AsdfFile)->asdf.AsdfFile:
    """ https://weldx.readthedocs.io/en/latest/tutorials/GMAW_process.html """
    
    new_file = asdf.AsdfFile(file.tree) # make a copy
    # Note: For some reasons, using integers in Q_ fails upon ASDF reading !
    params_spray = dict(
        wire_feedrate=Q_(10.0, "m/min"),
        voltage=TS(data=Q_([40.0,20.0], "V"),time=Q_([0.0,10.0],"s")),
        impedance=Q_(10.0, "percent"),
        characteristic=Q_(5,"V/A"),
    )
    process_spray = GmawProcess(
        "spray", "CLOOS", "Quinto", params_spray, tag="CLOOS/spray_arc"
    )
    new_file.tree["spray"] = process_spray
    return new_file

def add_pulse_ui(file:asdf.AsdfFile)->asdf.AsdfFile:

    new_file = asdf.AsdfFile(file.tree)
    params_pulse = dict(
        wire_feedrate=Q_(10.0, "m/min"),
        pulse_voltage=Q_(40.0, "V"),
        pulse_duration=Q_(5.0, "ms"),
        pulse_frequency=Q_(100.0, "Hz"),
        base_current=Q_(60.0, "A"),
    )
    process_pulse = GmawProcess(
        "pulse",
        "CLOOS",
        "Quinto",
        params_pulse,
        tag="CLOOS/pulse",
        meta={"modulation": "UI"},
    )
    new_file.tree["pulse_UI"] = process_pulse
    return new_file

if __name__ == "__main__":

    example_groove = list(_create_test_grooves().values())[0][0]
    tree = {"workpiece": {"groove": example_groove}}
    file = asdf.AsdfFile(tree)

    file_step_1 = add_seam_length(file)
    file_step_1_buffer =  weldx.asdf.util.write_buffer(file_step_1.tree)
    file_step_1_yaml_header = weldx.asdf.util.get_yaml_header(file_step_1_buffer)
    print(file_step_1_yaml_header)

    file_step_2 = add_process_spray(file_step_1)
    file_step_2_buffer =  weldx.asdf.util.write_buffer(file_step_2.tree)
    file_step_2_yaml_header = weldx.asdf.util.get_yaml_header(file_step_2_buffer)
    print(file_step_2_yaml_header)

    file_step_3 = add_pulse_ui(file_step_2)
    file_step_3_buffer =  weldx.asdf.util.write_buffer(file_step_3.tree)
    file_step_3_yaml_header = weldx.asdf.util.get_yaml_header(file_step_3_buffer)
    print(file_step_3_yaml_header)