# Schematic-API

A simple API for generating Minecraft schematics using custom generators.

## Features

- Dynamic loading of schematic generators from Python files
- RESTful API for generating schematics
- Validates input arguments against generator requirements

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Endpoints](#endpoints)
4. [Contributing](#contributing)
5. [License](#license)

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/schematic-api.git
```
Install required Python packages:
```bash
pip install -r requirements.txt
```
Run the sanic server:
```bash
python3 -m sanic server:app --host=0.0.0.0 --port=8080 --debug --reload
```
## Usage

### Adding Generators

1. Add your generator python script inside the `generators` directory.
2. Each callable function inside the script will be automatically registered as a generator.

### API

Send a POST request to `/api/get-schematic/` with the required JSON payload.

Example payload:

```json
{
  "schematic_name": "my_schematic",
  "generator_type": "basic",
  "generator_name": "house",
  "generator_args": {
    "width": 10,
    "height": 10
  }
}
```

## Endpoints

- POST `/api/get-schematic/`: Generates a Minecraft schematic based on the supplied parameters.


