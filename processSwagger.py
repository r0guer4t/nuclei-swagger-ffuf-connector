import json
import os
import re
from urllib.parse import urljoin


SWAGGER_DIR = "swagger-jsons"  
OUTPUT_FILE = "ffufFUZZ.txt"  
BASE_URL_FILE = "swaggerVuln.txt"  

def load_swagger_file(swagger_file):
    with open(swagger_file, "r") as f:
        return json.load(f)

def extract_endpoints(schema):
    paths = schema.get("paths", {})
    endpoints = []

    for path, methods in paths.items():
        for method in methods.keys():
            endpoints.append({"method": method, "path": path})

    return endpoints

def replace_parameters_with_fuzz(endpoint):
    if '{culture}' in endpoint:
        endpoint = endpoint.replace('{culture}', 'en')
    return re.sub(r"\{[^}]*\}", "FUZZ", endpoint)

def process_swagger_files():
    if not os.path.exists(SWAGGER_DIR):
        print(f"Directory '{SWAGGER_DIR}' does not exist.")
        return

    with open(OUTPUT_FILE, "w") as output_file:
        for swagger_file in os.listdir(SWAGGER_DIR):
            if swagger_file.endswith(".json"):
                swagger_path = os.path.join(SWAGGER_DIR, swagger_file)
                print(f"Processing: {swagger_path}")

                # Load the Swagger JSON schema
                try:
                    schema = load_swagger_file(swagger_path)
                    endpoints = extract_endpoints(schema)
                except Exception as e:
                    print(f"Failed to process {swagger_file}: {e}")
                    continue

                # Derive base URL from the swagger filename
                base_url = swagger_file.replace(
                    "swagger24.50.0.58557swagger.json.json", ""
                ).replace(
                    "swagger24.43.0.56349swagger.json.json", ""
                ).replace(
                    "_swagger.json", ""
                ).replace(
                    "_", "/"
                ).replace(
                    "swagger24.45.1.51994swagger.json.json", ""
                ).replace(
                    "swagger24.40.0.22953swagger.json.json", ""
                ).replace(
                    "swagger24.46.0.19625swagger.json.json", ""
                ).replace(
                    "swagger24.47.0.34226swagger.json.json", ""
                )
                base_url = f"https://{base_url}"  # Assuming HTTPS for reconstructed base URL

                # Process each endpoint
                for endpoint in endpoints:
                    clean_endpoint = replace_parameters_with_fuzz(endpoint["path"])
                    full_url = urljoin(base_url, clean_endpoint)
                    output_file.write(f"{endpoint['method'].upper()} {full_url}\n")

                print(f"Added endpoints from {swagger_file} to {OUTPUT_FILE}")

    print(f"Processing complete! Endpoints written to: {OUTPUT_FILE}")

if __name__ == "__main__":
    process_swagger_files()