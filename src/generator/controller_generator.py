class ControllerGenerator:

    def __init__(self):
        self.imports = "import { Controller, Get, Post, Body, HttpException, Param, UseGuards } " \
                       "from '@nestjs/common';\nimport { HttpResponse } " \
                       "from '../../../commons/responses/http_response';" \
                       "\nimport { BasicRestController } from '../../../commons/controllers/rest.controller';" \
                       "\nimport { AuthGuard } from '@nestjs/passport';\n"
        self.content = ""

    def build_additional_imports(self, module_name: str, entity_name: str):
        self.imports += "import { " + entity_name + " } from '../entity/" + module_name + ".entity';\n"
        self.imports += "import { " + entity_name + "DTO } from '../entity/" + module_name + ".dto';\n"
        self.imports += "import { " + entity_name + "Service } from '../service/" + module_name + ".service';\n"

    def clean(self):
        self.imports = "import { Controller, Get, Post, Body, HttpException, Param, UseGuards } " \
                       "from '@nestjs/common';\nimport { HttpResponse } " \
                       "from '../../../commons/responses/http_response';" \
                       "\nimport { BasicRestController } from '../../../commons/controllers/rest.controller';" \
                       "\nimport { AuthGuard } from '@nestjs/passport';\n"
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
        self.content += "@Controller('" + module_name + "')\n"
        self.content += "export class " + dict_class["name"] + "Controller extends BasicRestController<" + \
                        dict_class["name"] + ", " + pk_dict["type"] + ", " + dict_class["name"] + "DTO>{\n\n"
        self.content += "    constructor(protected service: " + dict_class["name"] + "Service){super();}\n\n"

    def build_close(self):
        self.content += "}"
