#!/usr/bin/env python3
"""
从 contract.json (JSON Schema) 生成 OpenAPI 3.0 规范

工作流程：
1. 扫描所有 tools/*/contract.json
2. 将 JSON Schema 转换为 OpenAPI 3.0 格式
3. 合并所有 API 到一个 openapi.json 文件
"""
import json
import pathlib
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime


def json_schema_to_openapi_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    """将 JSON Schema 转换为 OpenAPI Schema 格式"""
    # OpenAPI 3.0 使用 JSON Schema 的子集，大部分可以直接使用
    openapi_schema = {}
    
    # 基本类型映射
    if "type" in schema:
        openapi_schema["type"] = schema["type"]
    
    # 属性
    if "properties" in schema:
        openapi_schema["properties"] = {}
        for prop_name, prop_schema in schema["properties"].items():
            openapi_schema["properties"][prop_name] = json_schema_to_openapi_schema(prop_schema)
    
    # 必填字段
    if "required" in schema:
        openapi_schema["required"] = schema["required"]
    
    # 描述
    if "description" in schema:
        openapi_schema["description"] = schema["description"]
    
    # 默认值
    if "default" in schema:
        openapi_schema["default"] = schema["default"]
    
    # 枚举
    if "enum" in schema:
        openapi_schema["enum"] = schema["enum"]
    
    # 数组
    if schema.get("type") == "array" and "items" in schema:
        openapi_schema["items"] = json_schema_to_openapi_schema(schema["items"])
    
    # 字符串格式
    if "format" in schema:
        openapi_schema["format"] = schema["format"]
    
    # 最小/最大长度
    if "minLength" in schema:
        openapi_schema["minLength"] = schema["minLength"]
    if "maxLength" in schema:
        openapi_schema["maxLength"] = schema["maxLength"]
    
    # 最小/最大值
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
    """将单个 contract.json 转换为 OpenAPI path 定义"""
    # 读取契约文件
    title = contract_data.get("title", api_name)
    version = contract_data.get("version", "1.0.0")
    description = contract_data.get("description", f"{title} API")
    
    # 构建请求 schema
    request_schema = json_schema_to_openapi_schema(contract_data)
    
    # 构建响应 schema
    response_schema = {
        "type": "object",
        "properties": {
            "result": {
                "type": "string",
                "description": "处理结果"
            },
            "status": {
                "type": "string",
                "enum": ["success", "error"],
                "description": "状态"
            },
            "error_code": {
                "type": "string",
                "description": "错误代码（仅错误时）"
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
    
    # 构建 OpenAPI path
    # 默认路径：/api/{api_name}
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
                    "description": "成功响应",
                    "content": {
                        "application/json": {
                            "schema": response_schema
                        }
                    }
                },
                "400": {
                    "description": "参数验证失败",
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
                    "description": "服务器错误",
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
    """扫描所有 contract.json 文件"""
    contracts = []
    
    if not tools_dir.exists():
        return contracts
    
    for contract_file in tools_dir.rglob("contract.json"):
        try:
            with open(contract_file, "r", encoding="utf-8") as f:
                contract_data = json.load(f)
            
            # 获取 API 名称（从目录名）
            api_name = contract_file.parent.name
            contracts.append({
                "name": api_name,
                "path": contract_file,
                "data": contract_data
            })
        except Exception as e:
            print(f"[WARN] 无法读取 {contract_file}: {e}", file=sys.stderr)
    
    return contracts


def generate_openapi(output_path: pathlib.Path, tools_dir: pathlib.Path) -> bool:
    """生成 OpenAPI 3.0 规范文件"""
    print("[INFO] 生成 OpenAPI 3.0 规范...")
    
    # 扫描所有契约
    contracts = scan_contracts(tools_dir)
    
    if not contracts:
        print("[WARN] 未找到任何 contract.json 文件")
        return False
    
    print(f"[INFO] 找到 {len(contracts)} 个 API 契约")
    
    # 构建 OpenAPI 文档
    openapi_doc = {
        "openapi": "3.0.0",
        "info": {
            "title": "API Specification",
            "version": "1.0.0",
            "description": "从 contract.json 自动生成的 OpenAPI 3.0 规范",
            "contact": {
                "name": "API Support"
            }
        },
        "servers": [
            {
                "url": "http://localhost:8000",
                "description": "开发环境"
            },
            {
                "url": "https://api.example.com",
                "description": "生产环境"
            }
        ],
        "paths": {},
        "components": {
            "schemas": {}
        }
    }
    
    # 合并所有路径
    for contract in contracts:
        api_name = contract["name"]
        contract_data = contract["data"]
        
        print(f"   处理: {api_name}")
        
        # 转换为 OpenAPI path
        paths = contract_to_openapi_path(api_name, contract["path"], contract_data)
        openapi_doc["paths"].update(paths)
        
        # 添加 schema（可选）
        schema_name = f"{api_name}Request"
        openapi_doc["components"]["schemas"][schema_name] = json_schema_to_openapi_schema(contract_data)
    
    # 写入文件
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(openapi_doc, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] OpenAPI 规范已生成: {output_path}")
    print(f"[INFO] 包含 {len(openapi_doc['paths'])} 个路径")
    
    return True


def main():
    """主函数"""
    workspace_root = pathlib.Path(__file__).parent.parent
    tools_dir = workspace_root / "tools"
    output_path = workspace_root / "tools" / "openapi.json"
    
    success = generate_openapi(output_path, tools_dir)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()

