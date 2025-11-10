#!/usr/bin/env python3
"""
 contract.json (JSON Schema)  OpenAPI 3.0 


1.  tools/*/contract.json
2.  JSON Schema  OpenAPI 3.0 
3.  API  openapi.json 
"""
import json
import pathlib
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def json_schema_to_openapi_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    """ JSON Schema  OpenAPI Schema """
    # OpenAPI 3.0  JSON Schema 
    openapi_schema = {}
    
    # 
    if "type" in schema:
        openapi_schema["type"] = schema["type"]
    
    # 
    if "properties" in schema:
        openapi_schema["properties"] = {}
        for prop_name, prop_schema in schema["properties"].items():
            openapi_schema["properties"][prop_name] = json_schema_to_openapi_schema(prop_schema)
    
    # 
    if "required" in schema:
        openapi_schema["required"] = schema["required"]
    
    # 
    if "description" in schema:
        openapi_schema["description"] = schema["description"]
    
    # 
    if "default" in schema:
        openapi_schema["default"] = schema["default"]
    
    # 
    if "enum" in schema:
        openapi_schema["enum"] = schema["enum"]
    
    # 
    if schema.get("type") == "array" and "items" in schema:
        openapi_schema["items"] = json_schema_to_openapi_schema(schema["items"])
    
    # 
    if "format" in schema:
        openapi_schema["format"] = schema["format"]
    
    # /
    if "minLength" in schema:
        openapi_schema["minLength"] = schema["minLength"]
    if "maxLength" in schema:
        openapi_schema["maxLength"] = schema["maxLength"]
    
    # /
    if "minimum" in schema:
        openapi_schema["minimum"] = schema["minimum"]
    if "maximum" in schema:
        openapi_schema["maximum"] = schema["maximum"]
    
    return openapi_schema


def contract_to_openapi_path(
    api_name: str,
    contract_path: pathlib.Path,
    contract_data: Dict[str, Any]
) -> Dict[str, Any]:
    """ contract.json  OpenAPI path """
    # 
    title = contract_data.get("title", api_name)
    version = contract_data.get("version", "1.0.0")
    description = contract_data.get("description", f"{title} API")
    
    #  schema
    request_schema = json_schema_to_openapi_schema(contract_data)
    
    #  schema
    response_schema = {
        "type": "object",
        "properties": {
            "result": {
                "type": "string",
                "description": ""
            },
            "status": {
                "type": "string",
                "enum": ["success", "error"],
                "description": ""
            },
            "error_code": {
                "type": "string",
                "description": ""
            },
            "metadata": {
                "type": "object",
                "properties": {
                    "duration_ms": {"type": "number"},
                    "version": {"type": "string"}
                }
            }
        },
        "required": ["result", "status"]
    }
    
    #  OpenAPI path
    # /api/{api_name}
    path = f"/api/{api_name}"
    
    openapi_path = {
        "post": {
            "summary": description,
            "description": description,
            "operationId": f"{api_name}_post",
            "tags": [api_name],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": request_schema
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "",
                    "content": {
                        "application/json": {
                            "schema": response_schema
                        }
                    }
                },
                "400": {
                    "description": "",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "error": {"type": "string"},
                                    "error_code": {"type": "string"}
                                }
                            }
                        }
                    }
                },
                "500": {
                    "description": "",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "error": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    return {path: openapi_path}


def scan_contracts(tools_dir: pathlib.Path) -> List[Dict[str, Any]]:
    """ contract.json """
    contracts = []
    
    if not tools_dir.exists():
        return contracts
    
    for contract_file in tools_dir.rglob("contract.json"):
        try:
            with open(contract_file, "r", encoding="utf-8") as f:
                contract_data = json.load(f)
            
            #  API 
            api_name = contract_file.parent.name
            contracts.append({
                "name": api_name,
                "path": contract_file,
                "data": contract_data
            })
        except Exception as e:
            print(f"[WARN]  {contract_file}: {e}", file=sys.stderr)
    
    return contracts


def generate_openapi(output_path: pathlib.Path, tools_dir: pathlib.Path) -> bool:
    """ OpenAPI 3.0 """
    print("[INFO]  OpenAPI 3.0 ...")
    
    # 
    contracts = scan_contracts(tools_dir)
    
    if not contracts:
        print("[WARN]  contract.json ")
        return False
    
    print(f"[INFO]  {len(contracts)}  API ")
    
    #  OpenAPI 
    openapi_doc = {
        "openapi": "3.0.0",
        "info": {
            "title": "API Specification",
            "version": "1.0.0",
            "description": " contract.json  OpenAPI 3.0 ",
            "contact": {
                "name": "API Support"
            }
        },
        "servers": [
            {
                "url": "http://localhost:8000",
                "description": ""
            },
            {
                "url": "https://api.example.com",
                "description": ""
            }
        ],
        "paths": {},
        "components": {
            "schemas": {}
        }
    }
    
    # 
    for contract in contracts:
        api_name = contract["name"]
        contract_data = contract["data"]
        
        print(f"   : {api_name}")
        
        #  OpenAPI path
        paths = contract_to_openapi_path(api_name, contract["path"], contract_data)
        openapi_doc["paths"].update(paths)
        
        #  schema
        schema_name = f"{api_name}Request"
        openapi_doc["components"]["schemas"][schema_name] = json_schema_to_openapi_schema(contract_data)
    
    # 
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(openapi_doc, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] OpenAPI : {output_path}")
    print(f"[INFO]  {len(openapi_doc['paths'])} ")
    
    return True


def main():
    """"""
    workspace_root = pathlib.Path(__file__).parent.parent
    tools_dir = workspace_root / "tools"
    output_path = workspace_root / "tools" / "openapi.json"
    
    success = generate_openapi(output_path, tools_dir)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()

