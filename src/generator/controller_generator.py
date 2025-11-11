BASE_IMPORTS = "import {\n  Controller,\n  // Get,\n  // Post,\n  // Body,\n  // HttpException,\n  // Param,\n  // UseGuards,\n} " \
                       "from '@nestjs/common';\n// import { HttpResponse } " \
                       "from '../../../commons/responses/http-response';" \
                       "\nimport { BasicRestController } from '../../../commons/controllers/rest.controller';" \
                       "\n// import { AuthGuard } from '@nestjs/passport';\n"


class ControllerGenerator:

    def __init__(self):
        self.imports = BASE_IMPORTS
        self.content = ""

    def build_additional_imports(self, module_name: str, entity_name: str):
        self.imports += "import { " + entity_name + " } from '../entity/" + module_name + ".entity';\n"
        self.imports += "import { " + entity_name + "DTO } from '../entity/" + module_name + ".dto';\n"
        self.imports += "import { " + entity_name + "Business } from '../service/" + module_name + ".business';\n"

    def clean(self):
        self.imports = BASE_IMPORTS
        self.content = ""

    def build_class(self, module_name: str, entity_dict: dict, pk_dict: dict):
        self.build_additional_imports(module_name, entity_dict["name"])
        self.build_headers()
        self.build_class_name(module_name, entity_dict, pk_dict)
        self.build_close()
        return self.content

    def build_headers(self):
        self.content += self.imports
        self.content += "\n"

    def build_class_name(self, module_name: str, dict_class: dict, pk_dict: dict):
        endpoint = module_name.replace("_", "-")
        self.content += "@Controller('" + endpoint + "')\n"
        self.content += "export class " + dict_class["name"] + "Controller extends BasicRestController<\n  " + \
                        dict_class["name"] + ",\n  " + pk_dict["type"] + ",\n  " + dict_class["name"] + "DTO\n> {\n"
        self.content += "  constructor(override readonly service: " + dict_class["name"] + \
                        "Business) {\n    super();\n  }\n\n  // Some new custom endpoints can be placed here\n"

    def build_close(self):
        self.content += "}"
