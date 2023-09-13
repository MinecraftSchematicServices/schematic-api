import os
from dataclasses import dataclass

from sanic import Sanic
from sanic.response import file, json
from registering.registering import get_available_generators

import mcschematic


if not os.path.exists("generated_schems"):
    os.mkdir("generated_schems")

app = Sanic("schematic-api")
    
def get_schematic_request_validity(request):
    return True, None


@app.post("/api/get-schematic/")
async def get_schematic(request):
    return json({"error": "Not implemented yet"}, status=501)
    # is_valid, error_message = get_schematic_request_validity(request.json)
    # if not is_valid:
    #     return json({"error": error_message}, status=400)
    # args = request.json.get("generator_args", {})
    # generator = generators[request.json["generator_type"]][request.json["generator_name"]]
    # print("got args", args)
    # schem = generator(**args)    
    # name = request.json["schematic_name"] 
    # schem.save("./generated_schems", name, mcschematic.Version.JE_1_19)
    # return await file("./generated_schems/" + name+ ".schem", filename=name+ ".schem", mime_type="application/octet-stream")
    
    
@app.get("/api/get-generators/")
async def get_generators(request):
    return json(get_available_generators())
    
    
#     # name = "test.schem"
#     # schem = mcschematic.MCSchematic()
#     # schem.setBlock((0, -1, 0), "minecraft:stone")
#     # schem.save(".", name, mcschematic.Version.JE_1_19)
#     # return await file(name, filename=name, mime_type="application/octet-stream")

