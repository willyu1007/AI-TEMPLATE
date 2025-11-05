#!/usr/bin/env python3
"""
从 OpenAPI 3.0 规范生成 TypeScript 类型定义

工作流程：
1. 读取 tools/openapi.json
2. 解析 OpenAPI 规范
3. 生成 TypeScript 类型定义到 frontend/ 或 frontends/
"""
import json
import pathlib
import sys
from typing import Dict, Any, Optional, List


def openapi_type_to_ts(openapi_type: str, format: Optional[str] = None) -> str:
    """将 OpenAPI 类型转换为 TypeScript 类型"""
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
    """将 OpenAPI Schema 转换为 TypeScript 类型定义"""
    indent_str = "  " * indent
    
    if "$ref" in schema:
        # 处理引用
        ref_name = schema["$ref"].split("/")[-1]
        return ref_name
    
    schema_type = schema.get("type", "object")
    
    if schema_type == "object":
        # 对象类型
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
        # 数组类型
        items = schema.get("items", {})
        item_type = schema_to_ts_type(items, indent)
        return f"{item_type}[]"
    
    elif schema_type in ["string", "integer", "number", "boolean"]:
        # 基本类型
        ts_type = openapi_type_to_ts(schema_type, schema.get("format"))
        
        # 处理枚举
        if "enum" in schema:
            enum_values = " | ".join([f'"{v}"' if isinstance(v, str) else str(v) for v in schema["enum"]])
            return enum_values
        
        return ts_type
    
    else:
        return "unknown"


def generate_request_types(openapi_doc: Dict[str, Any]) -> List[str]:
    """生成请求类型定义"""
    types = []
    
    for path, methods in openapi_doc.get("paths", {}).items():
        for method, operation in methods.items():
            if method.lower() == "post":
                operation_id = operation.get("operationId", "")
                tag = operation.get("tags", [""])[0] if operation.get("tags") else ""
                
                # 获取请求 body
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
    """生成响应类型定义"""
    types = []
    
    for path, methods in openapi_doc.get("paths", {}).items():
        for method, operation in methods.items():
            if method.lower() == "post":
                operation_id = operation.get("operationId", "")
                tag = operation.get("tags", [""])[0] if operation.get("tags") else ""
                
                # 获取成功响应（200）
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
    """查找前端目录"""
    frontend_dirs = []
    
    # 检查 frontend/
    frontend_dir = workspace_root / "frontend"
    if frontend_dir.exists() and frontend_dir.is_dir():
        frontend_dirs.append(frontend_dir)
    
    # 检查 frontends/
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
    """为单个前端目录生成类型文件"""
    # 生成类型定义
    request_types = generate_request_types(openapi_doc)
    response_types = generate_response_types(openapi_doc)
    
    # 构建类型文件内容
    lines = [
        "// 自动生成的 TypeScript 类型定义",
        "// 此文件由 scripts/generate_frontend_types.py 自动生成，请勿手动编辑",
        "",
        "// ==================== 请求类型 ====================",
    ]
    lines.extend(request_types)
    lines.append("")
    lines.append("// ==================== 响应类型 ====================")
    lines.extend(response_types)
    lines.append("")
    
    # 确定输出路径
    # 优先使用 src/types/api.d.ts，否则使用 types/api.d.ts
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
        # 创建目录
        output_dir = types_dirs[0]
        output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "api.d.ts"
    
    # 写入文件
    content = "\n".join(lines)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"[OK] 已生成: {output_file}")
    return True


def main():
    """主函数"""
    workspace_root = pathlib.Path(__file__).parent.parent
    openapi_file = workspace_root / "tools" / "openapi.json"
    
    print("[INFO] 生成前端 TypeScript 类型...")
    
    # 检查 OpenAPI 文件是否存在
    if not openapi_file.exists():
        print(f"[ERROR] OpenAPI 文件不存在: {openapi_file}")
        print("[INFO] 请先运行: make generate_openapi")
        sys.exit(1)
    
    # 读取 OpenAPI 规范
    try:
        with open(openapi_file, "r", encoding="utf-8") as f:
            openapi_doc = json.load(f)
    except Exception as e:
        print(f"[ERROR] 无法读取 OpenAPI 文件: {e}")
        sys.exit(1)
    
    # 查找前端目录
    frontend_dirs = find_frontend_dirs(workspace_root)
    
    if not frontend_dirs:
        print("[WARN] 未找到前端目录（frontend/ 或 frontends/）")
        print("[INFO] 跳过类型生成")
        return
    
    print(f"[INFO] 找到 {len(frontend_dirs)} 个前端目录")
    
    # 为每个前端目录生成类型
    success_count = 0
    for frontend_dir in frontend_dirs:
        print(f"[INFO] 处理: {frontend_dir.name}")
        if generate_types_file(frontend_dir, openapi_doc):
            success_count += 1
    
    if success_count > 0:
        print(f"[OK] 成功生成 {success_count} 个类型文件")
    else:
        print("[WARN] 未生成任何类型文件")
        sys.exit(1)


if __name__ == "__main__":
    main()

