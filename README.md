# Auto Generate Endpoint modules for API Automation Framework #

This Endpoint generator project helps automate creating API automation tests using <a href="https://qxf2.com">Qxf2's</a> <a href="https://qxf2.com/blog/easily-maintainable-api-test-automation-framework/">API Automation framework</a>. It generates Endpoint modules—an abstraction for endpoints in the application under test from an <a href="https://learn.openapis.org/introduction.html">OpenAPI specification</a>.

## Qxf2's API Automation Framework workflow

```
+-------------------+
|     API Test      |
+-------------------+
          |
          v
+-------------------+
|    APIPlayer      |  <-- Maintains test scenarios
+-------------------+
          |
          v
+-------------------+
|   APIInterface    |  <-- Composed of all endpoint modules
+-------------------+
          |
          v
+-------------------------------------------------------------+
|                  Endpoint Modules                           |
|  +------------------------+  +------------------------+     |
|  | Endpoint Module 1      |  | Endpoint Module 2      | ... |
|  |   (uses Base API)      |  |   (uses Base API)      |     |
|  +------------------------+  +------------------------+     |  <-- Abstactions for endpoints in the API App
|  +------------------------+                                 |
|  | Endpoint Module 3      |                                 |
|  |   (uses Base API)      |                                 |
|  +------------------------+                                 |
+-------------------------------------------------------------+
```

The **API Test** calls methods on **APIPlayer**, which is where the test logic resides. **APIPlayer** interacts with **APIInterface** to access all endpoint modules. **APIInterface** is composed of all **Endpoint Modules**, which serve as abstractions for the endpoints in the API application. Each endpoint module inherits from and uses the **Base API** for HTTP operations, and the **Base API** leverages the [`requests`](https://requests.readthedocs.io/en/latest/) library to make.

This project will help you automatically create the `Endpoint Module 1`, `Endpoint Module 2`, `Endpoint Module 3`, and any additional endpoint modules required for your API application. By parsing your OpenAPI specification, it automatically generates these modules, saving time and ensuring consistency across your API automation framework.

## Requirements

- An OpenAPI v3.x.x specification for your API app.
- The spec file can be a `JSON` or `YAML` file.
- Install dependencies with:
  ```sh
  pip install -r requirements.txt
  ```

## How to run the script

### 1. Validate the OpenAPI specification

```sh
python api_auto_generator/endpoint_module_generator.py --spec <OpenAPI_spec_file_location>
```

This command checks if the OpenAPI spec can be used to generate Endpoint files. It will raise an exception for invalid or incomplete specs.

### 2. Generate the Endpoint module(s)

```sh
python api_auto_generator/endpoint_module_generator.py --spec <OpenAPI_spec_file_location> --generate-endpoints
```

This command generates `<endpoint_name>_endpoint.py` modules in the `endpoints` directory.

## How does the project work?

```
+----------------------------+
|   OpenAPI Spec (YAML/JSON) |
+-------------+--------------+
              |
              v
+----------------------------+
| openapi_spec_parser.py     |
| - Validates and parses     |
|   OpenAPI spec             |
| - For each path, uses      |
|   OpenAPIPathParser        |
+-------------+--------------+
              |
              v
+----------------------------+
| endpoint_name_generator.py |
| - Generates consistent     |
|   module, class, and       |
|   method names             |
|   from endpoint URLs       |
+-------------+--------------+
              |
              v
+----------------------------+
| endpoint_module_generator  |
| - Entry point script       |
| - Parses CLI args          |
| - Uses parsed spec & names |
| - Renders endpoint files   |
|   using Jinja2 templates   |
+-------------+--------------+
              |
              v
+----------------------------+
|   Endpoint Modules         |
| (Python files, one per     |
|  endpoint, in /endpoints)  |
+----------------------------+
```

The OpenAPI spec is parsed and validated by the `openapi_spec_parser.py` module. The  names are generated for modules/classes/methods by the `endpoint_name_generator.py` module and the main script - `endpoint_module_generator.py` orchestrates the process, uses the above modules, and finally renders the endpoint modules using Jinja2.

## Project Structure

- `endpoint_module_generator.py`: Main script to generate endpoint files from the OpenAPI spec.
- `openapi_spec_parser.py`: Parses and validates the OpenAPI spec, extracts endpoint and parameter details.
- `endpoint_name_generator.py`: Generates consistent names for modules, classes, and methods.
- `templates/endpoint_template.jinja2`: Jinja2 template for generating endpoint Python files.
- `endpoints/`: (Created at runtime) Output directory for generated endpoint modules.
- `requirements.txt`: Lists all required Python packages with pinned versions.

## Limitations & Constraints

### Invalid OpenAPI spec

- The script validates the OpenAPI spec at the start. Invalid specs will trigger an exception.
- JSON Schema validation is also performed. If you encounter confusing schema errors, try replacing the failing schema with `{}` to proceed.

### Minimal spec

- For minimal specs, run the script with only the `--spec` parameter to check if endpoint files can be generated.
- If no issues are reported, you can proceed to use the `--generate-endpoints` parameter.

## Troubleshooting

- **TemplateNotFound:** Ensure the `endpoint_template.jinja2` file exists in the `templates` directory.
- **Output Directory:** The script creates endpoint files in an `endpoints` directory at the project root. Make sure this directory exists or is writable.
- **Logging:** The script uses `loguru` for logging. Check the console output for detailed error messages.

## Example

 To generate endpoint modules for `specs/api.yaml`:

```sh
python api_auto_generator/endpoint_module_generator.py --spec specs/api.yaml --generate-endpoints
```

This will create Python files for each endpoint in the `endpoints/` directory.
