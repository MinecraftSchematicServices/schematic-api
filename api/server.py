import os
from dataclasses import dataclass

from sanic import Sanic
from sanic.response import file, json
from registering.registering import get_available_generators, generators_to_json
import traceback

import mcschematic


if not os.path.exists("generated_schems"):
    os.mkdir("generated_schems")

app = Sanic("schematic-api")

generators = get_available_generators()

def validate_request(request): 
    errors = []
    if "generator_name" not in request.json:
        errors.append("generator_name is missing")
    if "schematic_name" not in request.json:
        errors.append("schematic_name is missing")
    if "generator_args" not in request.json:
        errors.append("generator_args is missing")
        
    if errors:
        return False, errors
    
    if not isinstance(request.json["generator_name"], str):
        errors.append("generator_name is not a string")
    if not isinstance(request.json["schematic_name"], str):
        errors.append("schematic_name is not a string")
    if not isinstance(request.json["generator_args"], dict):
        errors.append("generator_args is not a dictionary")
        
    if errors:
        return False, errors
    
    if request.json["generator_name"] not in generators:    
        return False, [f"generator_name '{request.json['generator_name']}' is not a valid generator"]
    
    return True, []
        
    


@app.post("/api/get-schematic/")
async def get_schematic(request):
    valid, errors = validate_request(request)
    if not valid:
        print(errors)
        return json({"errors": errors}, status=400)
    args = request.json.get("generator_args", {})
    generator = generators[request.json["generator_name"]]
    try:
        schem = generator.generate(**args)
    except Exception as e:
        print(e)
        traceback.print_exc()
        return json({"error": str(e)}, status=400)
    name = request.json["schematic_name"]
    schem.save("./generated_schems", name, mcschematic.Version.JE_1_19)
    return await file("./generated_schems/" + name + ".schem", filename=name + ".schem",
                      mime_type="application/octet-stream")
    # schem = generator(**args)    
    # name = request.json["schematic_name"] 
    # schem.save("./generated_schems", name, mcschematic.Version.JE_1_19)
    # return await file("./generated_schems/" + name+ ".schem", filename=name+ ".schem", mime_type="application/octet-stream")
    
    
@app.get("/api/get-generators/")
async def get_generators(request):
    return json(generators_to_json(generators))
    
    
#     # name = "test.schem"
#     # schem = mcschematic.MCSchematic()
#     # schem.setBlock((0, -1, 0), "minecraft:stone")
#     # schem.save(".", name, mcschematic.Version.JE_1_19)
#     # return await file(name, filename=name, mime_type="application/octet-stream")
