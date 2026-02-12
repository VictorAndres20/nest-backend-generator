from typing import List

from src.helpers.folder_handler import get_module_name
from src.helpers.to_upper_snake_case import to_upper_snake_case

REACT_TS_SERVICE_BASE_IMPORTS = "import {\n  handleFetch,\n  GET_OPTIONS,\n  POST_OPTIONS,\n  PUT_OPTIONS\n} " \
                       "from './_commons/base.service';\n\n"


class ReactTSServiceGenerator:

    def __init__(self):
        self.imports = REACT_TS_SERVICE_BASE_IMPORTS
        self.class_imports = ""
        self.content = ""

    def build_additional_imports(self, module_name: str, entity_name: str):
        pass

    def clean(self):
        self.imports = REACT_TS_SERVICE_BASE_IMPORTS
        self.class_imports = ""
        self.content = ""

    def build_class_imports(self, list_attr: List):
        class_name = list_attr[0]["name"]
        entity_module = get_module_name(list_attr[0]["table_name"])
        self.class_imports += "import {\n  type " + class_name + "DTO,\n  type " + class_name + "EntityType,\n  type " + \
                              class_name + "EntityQuery,\n  type " + class_name + "EntityPagedQuery,\n} from '../_types/" + \
                              entity_module + ".types';\n"
        self.class_imports += "import { type HttpResponse } from './_commons/base.types';\n"

    def build_class(self, module_name: str, entity_dict: dict, pk_dict: dict, list_attr: List):
        self.build_headers(list_attr)
        self.build_class_name(module_name, entity_dict, pk_dict)
        self.build_close()
        return self.content

    def build_headers(self, list_attr: List):
        self.build_class_imports(list_attr)
        self.content += self.imports
        self.content += self.class_imports
        self.content += "\n"

    def build_class_name(self, module_name: str, dict_class: dict, pk_dict: dict):
        endpoint = module_name.replace("_", "-")
        pk_name = pk_dict["name"]
        class_name = dict_class["name"]
        dto_name = f"{class_name}DTO"
        entity_type_name = f"{class_name}EntityType"
        query_name = f"{class_name}EntityQuery"
        paged_query_name = f"{class_name}EntityPagedQuery"

        base_path = "BASE_PATH_" + to_upper_snake_case(endpoint)

        self.content += "export const " + base_path + " = '/" + endpoint + "';\n\n"

        self.content += "export const findAll" + class_name + " = async (): Promise<\n"
        self.content += "  HttpResponse<" + entity_type_name + "[]>\n"
        self.content += "> => {\n"
        self.content += "  return await handleFetch<" + entity_type_name + "[], undefined>(\n"
        self.content += "    `${" + base_path + "}/all`,\n"
        self.content += "    GET_OPTIONS\n"
        self.content += "  );\n"
        self.content += "};\n\n"

        self.content += "export const find" + class_name + "ById = async ({\n"
        self.content += "  " + pk_name + ",\n"
        self.content += "}: " + query_name + "): Promise<\n"
        self.content += "  HttpResponse<" + entity_type_name + ">\n"
        self.content += "> => {\n"
        self.content += "  return await handleFetch<" + entity_type_name + ", undefined>(\n"
        self.content += "    `${" + base_path + "}/id/${" + pk_name + "}`,\n"
        self.content += "    GET_OPTIONS\n"
        self.content += "  );\n"
        self.content += "};\n\n"

        self.content += "export const create" + class_name + " = async (\n"
        self.content += "  body: " + dto_name + "\n"
        self.content += "): Promise<HttpResponse<" + entity_type_name + ">> => {\n"
        self.content += "  return await handleFetch<" + entity_type_name + ", " + dto_name + ">(\n"
        self.content += "    `${" + base_path + "}/create`,\n"
        self.content += "    POST_OPTIONS,\n"
        self.content += "    body\n"
        self.content += "  );\n"
        self.content += "};\n\n"

        self.content += "export const update" + class_name + " = async (\n"
        self.content += "  { " + pk_name + " }: " + query_name + ",\n"
        self.content += "  body: " + dto_name + "\n"
        self.content += "): Promise<HttpResponse<" + entity_type_name + ">> => {\n"
        self.content += "  return await handleFetch<" + entity_type_name + ", " + dto_name + ">(\n"
        self.content += "    `${" + base_path + "}/edit/${" + pk_name + "}`,\n"
        self.content += "    PUT_OPTIONS,\n"
        self.content += "    body\n"
        self.content += "  );\n"
        self.content += "};\n\n"

        self.content += "export const findAll" + class_name + "Paged = async ({\n"
        self.content += "  page,\n"
        self.content += "  limit = 8,\n"
        self.content += "}: " + paged_query_name + "): Promise<\n"
        self.content += "  HttpResponse<" + entity_type_name + "[]>\n"
        self.content += "> => {\n"
        self.content += "  return await handleFetch<" + entity_type_name + "[], undefined>(\n"
        self.content += "    `${" + base_path + "}/all-paged/${page}/${limit}`,\n"
        self.content += "    GET_OPTIONS\n"
        self.content += "  );\n"
        self.content += "};\n"

    def build_close(self):
        self.content += ""
