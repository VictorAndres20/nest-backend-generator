from typing import List


BUSINESS_BASE_IMPORTS = "import { Injectable } from '@nestjs/common';\n"


class BusinessGenerator:

    def __init__(self):
        self.imports = BUSINESS_BASE_IMPORTS
        self.class_imports = ""
        self.content = ""

    def build_additional_imports(self, module_name: str, entity_name: str):
        self.imports += "import { " + entity_name + "Service } from './_" + module_name + ".service';\n"

    def clean(self):
        self.imports = BUSINESS_BASE_IMPORTS
        self.class_imports = ""
        self.content = ""

    def build_class(self, module_name: str, entity_dict: dict, pk_dict: dict, list_attr: List):
        self.build_additional_imports(module_name, entity_dict["name"])
        self.build_headers()
        self.build_class_name(entity_dict, pk_dict)
        self.build_close()
        return self.content

    def build_headers(self):
        self.content += self.imports
        self.content += self.class_imports
        self.content += "\n"

    def build_class_name(self, dict_class: dict, pk_dict: dict):
        self.content += "@Injectable()\n"
        self.content += "export class " + dict_class["name"] + "Business extends " + dict_class["name"] + "Service {\n"
        self.content += "  // Override or create new custom functions here\n"

    def build_close(self):
        self.content += "}"
