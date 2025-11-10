#!/usr/bin/env python3
"""
 OpenAPI 3.0  TypeScript 


1.  tools/openapi.json
2.  OpenAPI 
3.  TypeScript  frontend/  frontends/
"""
import json
import pathlib
import sys
from typing import Dict, Any, Optional, List

# Windows UTF-8 support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def openapi_type_to_ts(openapi_type: str, format: Optional[str] = None) -> str:
    """ OpenAPI  TypeScript """
    type_map = {
        "string": "string",
        "integer": "number",
        "number": "number",
        "boolean": "boolean",
        "array": "unknown[]",
        "object": "Record<string, unknown>"
    }
    
    if format == "int64" or format == "int32":
        return "number"
    
    return type_map.get(openapi_type, "unknown")


def schema_to_ts_type(schema: Dict[str, Any], indent: int = 0) -> str:
    """ OpenAPI Schema  TypeScript """
    indent_str = "  " * indent
    
    if "$ref" in schema:
        # 
        ref_name = schema["$ref"].split("/")[-1]
        return ref_name
    
    schema_type = schema.get("type", "object")
    
    if schema_type == "object":
        # 
        lines = ["{"]
        if "properties" in schema:
            for prop_name, prop_schema in schema["properties"].items():
                prop_type = schema_to_ts_type(prop_schema, indent + 1)
                required = schema.get("required", [])
                optional = "" if prop_name in required else "?"
                lines.append(f"{indent_str}  {prop_name}{optional}: {prop_type};")
        else:
            lines.append(f"{indent_str}  [key: string]: unknown;")
        lines.append(f"{indent_str}}}")
        return "\n".join(lines)
    
    elif schema_type == "array":
        # 
        items = schema.get("items", {})
        item_type = schema_to_ts_type(items, indent)
        return f"{item_type}[]"
    
    elif schema_type in ["string", "integer", "number", "boolean"]:
        # 
        ts_type = openapi_type_to_ts(schema_type, schema.get("format"))
        
        # 
        if "enum" in schema:
            enum_values = " | ".join([f'"{v}"' if isinstance(v, str) else str(v) for v in schema["enum"]])
            return enum_values
        
        return ts_type
    
    else:
        return "unknown"


def generate_request_types(openapi_doc: Dict[str, Any]) -> List[str]:
    """"""
    types = []
    
    for path, methods in openapi_doc.get("paths", {}).items():
        for method, operation in methods.items():
            if method.lower() == "post":
                operation_id = operation.get("operationId", "")
                tag = operation.get("tags", [""])[0] if operation.get("tags") else ""
                
                #  body
                request_body = operation.get("requestBody", {})
                if request_body:
                    content = request_body.get("content", {})
                    json_content = content.get("application/json", {})
                    schema = json_content.get("schema", {})
                    
                    if schema:
                        type_name = f"{tag.capitalize()}Request" if tag else f"{operation_id}Request"
                        ts_type = schema_to_ts_type(schema)
                        types.append(f"export type {type_name} = {ts_type};")
    
    return types


def generate_response_types(openapi_doc: Dict[str, Any]) -> List[str]:
    """"""
    types = []
    
    for path, methods in openapi_doc.get("paths", {}).items():
        for method, operation in methods.items():
            if method.lower() == "post":
                operation_id = operation.get("operationId", "")
                tag = operation.get("tags", [""])[0] if operation.get("tags") else ""
                
                # 200
                responses = operation.get("responses", {})
                success_response = responses.get("200", {})
                
                if success_response:
                    content = success_response.get("content", {})
                    json_content = content.get("application/json", {})
                    schema = json_content.get("schema", {})
                    
                    if schema:
                        type_name = f"{tag.capitalize()}Response" if tag else f"{operation_id}Response"
                        ts_type = schema_to_ts_type(schema)
                        types.append(f"export type {type_name} = {ts_type};")
    
    return types


def find_frontend_dirs(workspace_root: pathlib.Path) -> List[pathlib.Path]:
    """"""
    frontend_dirs = []
    
    #  frontend/
    frontend_dir = workspace_root / "frontend"
    if frontend_dir.exists() and frontend_dir.is_dir():
        frontend_dirs.append(frontend_dir)
    
    #  frontends/
    frontends_dir = workspace_root / "frontends"
    if frontends_dir.exists() and frontends_dir.is_dir():
        for app_dir in frontends_dir.iterdir():
            if app_dir.is_dir():
                frontend_dirs.append(app_dir)
    
    return frontend_dirs


def generate_types_file(
    frontend_dir: pathlib.Path,
    openapi_doc: Dict[str, Any]
) -> bool:
    """"""
    # 
    request_types = generate_request_types(openapi_doc)
    response_types = generate_response_types(openapi_doc)
    
    # 
    lines = [
        "//  TypeScript ",
        "//  scripts/generate_frontend_types.py ",
        "",
        "// ====================  ====================",
    ]
    lines.extend(request_types)
    lines.append("")
    lines.append("// ====================  ====================")
    lines.extend(response_types)
    lines.append("")
    
    # 
    #  src/types/api.d.ts types/api.d.ts
    types_dirs = [
        frontend_dir / "src" / "types",
        frontend_dir / "types"
    ]
    
    output_dir = None
    for td in types_dirs:
        if td.exists():
            output_dir = td
            break
    
    if output_dir is None:
        # 
        output_dir = types_dirs[0]
        output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "api.d.ts"
    
    # 
    content = "\n".join(lines)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"[OK] : {output_file}")
    return True


def main():
    """"""
    workspace_root = pathlib.Path(__file__).parent.parent
    openapi_file = workspace_root / "tools" / "openapi.json"
    
    print("[INFO]  TypeScript ...")
    
    #  OpenAPI 
    if not openapi_file.exists():
        print(f"[ERROR] OpenAPI : {openapi_file}")
        print("[INFO] : make generate_openapi")
        sys.exit(1)
    
    #  OpenAPI 
    try:
        with open(openapi_file, "r", encoding="utf-8") as f:
            openapi_doc = json.load(f)
    except Exception as e:
        print(f"[ERROR]  OpenAPI : {e}")
        sys.exit(1)
    
    # 
    frontend_dirs = find_frontend_dirs(workspace_root)
    
    if not frontend_dirs:
        print("[WARN] frontend/  frontends/")
        print("[INFO] ")
        return
    
    print(f"[INFO]  {len(frontend_dirs)} ")
    
    # 
    success_count = 0
    for frontend_dir in frontend_dirs:
        print(f"[INFO] : {frontend_dir.name}")
        if generate_types_file(frontend_dir, openapi_doc):
            success_count += 1
    
    if success_count > 0:
        print(f"[OK]  {success_count} ")
    else:
        print("[WARN] ")
        sys.exit(1)


if __name__ == "__main__":
    main()

