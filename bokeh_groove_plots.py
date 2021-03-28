import weldx
from weldx import Q_ # pint quantity from the weldx package
from weldx.asdf.extension import WeldxAsdfExtension, WeldxExtension
from weldx.welding.groove.iso_9692_1 import get_groove, IsoBaseGroove, _create_test_grooves
from weldx.geometry import Shape, LineSegment

from bokeh.plotting import figure, show, Figure, output_file
from bokeh.models.tools import HoverTool, ResetTool, WheelZoomTool
from bokeh.layouts import row, column

from typing import List

def create_bokeh_figure(groove: IsoBaseGroove):
    """ Helper function for creating a generic bokeh figure """
    p: Figure = figure(height=400, width=800)
    profile = groove.to_profile()
    raster_data = profile.rasterize(0.5)
    shape: Shape
    for shape in profile.shapes:
            for s in shape.segments:
                if(s.__class__ == LineSegment):
                    p.line(s.points[0], s.points[1], line_width=2)

    p.circle_dot(raster_data[0], raster_data[1])
    pstr = ", ".join(groove.param_strings())
    p.title = groove.__class__.__name__ + ", " + pstr
    return p

def create_example_grooves()->List[IsoBaseGroove]:
    """ Create one example groove for each class """
    groove_sub_classes = [cls for cls in IsoBaseGroove.__subclasses__()]
    groove_sub_class_names = [cls.__name__ for cls in groove_sub_classes]
    test_grooves = list(_create_test_grooves().values())
    sub_class_examples = [[item[0] for item in  test_grooves if item[0].__class__.__name__ == sub_class] for sub_class in groove_sub_class_names]
    sub_class_examples = [item[0] for item in sub_class_examples if len(item) > 0]

    return sub_class_examples

if __name__ == "__main__":

    print("start plotting")

    example_grooves = create_example_grooves()
    plot_list = []
    for groove in example_grooves:
        type_name = groove.__class__.__name__
        plot = create_bokeh_figure(groove)
        plot_list.append(row(plot))       
    groove_plots = column(*plot_list)
    output_file("plot.html")
    show(groove_plots)

    input("Press Enter to continue...")