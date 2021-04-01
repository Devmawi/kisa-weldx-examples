import requests
import base64
import importlib
from inspect import isfunction, getmembers, getmodule
import asdf


def analyze_module(module):
    module_functions = [m[1] for m in getmembers(module) if isfunction(m[1]) and m[1].__module__ == module.__name__]
    filtered_functions = []
    
    for f in module_functions:
        annotations = f.__annotations__
        has_right_parameter = annotations.get("file", {}) == asdf.AsdfFile
        has_right_return_type = annotations.get("return",{}) == asdf.AsdfFile
        
        print("has_right_parameter: {0}".format(has_right_parameter))
        print("has_right_return_type: {0}".format(has_right_return_type))
        
        if(has_right_parameter and has_right_return_type):
            filtered_functions.append(f)
   
    return filtered_functions


if __name__ == "__main__":

    r = requests.get('https://api.github.com/repos/Devmawi/kisa-weldx-examples/contents/weldx_processors.py?ref=master')
    print(r.status_code)
    json_obj = r.json()
    base64_string = json_obj["content"]
    module_content = base64.b64decode(base64_string)

    spec = importlib.util.spec_from_loader('processor_module', loader=None)
    processor_module = importlib.util.module_from_spec(spec)
    exec(module_content, processor_module.__dict__)

    processor_functions = analyze_module(processor_module)

    for p in processor_functions:
        display_name = getattr(p, "display_name", p.__name__)
        print(display_name)

    print("finished ...")