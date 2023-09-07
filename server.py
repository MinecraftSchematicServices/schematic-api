import os
from dataclasses import dataclass

from sanic import Sanic
from sanic.response import file, json

import mcschematic

def get_generators():
    generators = {}
    for filename in os.listdir("generators"):
        if filename.endswith(".py"):
            name = filename[:-3]
            generators[name] = {}
            for func in getattr(__import__("generators." + name), name).__dict__.values():
                if callable(func):
                    generators[name][func.__name__] = func
    return generators

generators = get_generators()

def get_generator_docstrings():
    generator_docstrings = {}
    for name, generator_dict in generators.items():
        generator_docstrings[name] = {}
        for generator_name, generator in generator_dict.items():
            generator_docstrings[name][generator_name] = generator.__doc__
    return generator_docstrings



app = Sanic("schematic-api")
    
def get_schematic_request_validity(request):
    validation_dict = {
        "schematic_name": lambda x: (isinstance(x, str), "schematic_name must be a string."),
        "generator_type": lambda x: (isinstance(x, str) and x in generators, "Invalid generator_type."),
        "generator_name": lambda x: (isinstance(x, str) and x in generators.get(request.get("generator_type", ""), []), "Invalid generator_name."),
        "generator_args": lambda x: (isinstance(x, dict), "generator_args must be a dict."),
    }
    
    optional_keys = ["generator_args"]

    for key, validator in validation_dict.items():
        if key not in request:
            if key in optional_keys:
                continue
            return False, f"Missing key: {key}"
        is_valid, error_message = validator(request.get(key, None))
        if not is_valid:
            return False, error_message
    if request.get("generator_type") not in generators:
        return False, "Invalid generator_type."
    if request.get("generator_name") not in generators.get(request.get("generator_type", ""), []):
        return False, "Invalid generator_name."
    return True, None


@app.post("/api/get-schematic/")
async def get_schematic(request):
    is_valid, error_message = get_schematic_request_validity(request.json)
    if not is_valid:
        return json({"error": error_message}, status=400)
    args = request.json.get("generator_args", {})
    generator = generators[request.json["generator_type"]][request.json["generator_name"]]
    print("got args", args)
    schem = generator(**args)    
    name = request.json["schematic_name"] 
    schem.save("./generated_schems/", name, mcschematic.Version.JE_1_19)
    return await file("./generated_schems/" + name+ ".schem", filename=name+ ".schem", mime_type="application/octet-stream")
    
    
@app.get("/api/get-generators/")
async def get_generators(request):
    return json(get_generator_docstrings())
    
    
#     # name = "test.schem"
#     # schem = mcschematic.MCSchematic()
#     # schem.setBlock((0, -1, 0), "minecraft:stone")
#     # schem.save(".", name, mcschematic.Version.JE_1_19)
#     # return await file(name, filename=name, mime_type="application/octet-stream")

