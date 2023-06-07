from typing import List


class ServiceGenerator:

    def __init__(self):
        self.imports = "import { Injectable } from '@nestjs/common';\n" \
                       "import { BasicCrudService } from '../../../commons/services/crud.service';\n" \
                       "import { InjectRepository } from '@nestjs/typeorm';\nimport { Repository } from 'typeorm';\n"
        self.class_imports = ""
        self.content = ""

    def build_additional_imports(self, module_name: str, entity_name: str):
        self.imports += "import { " + entity_name + " } from '../entity/" + module_name + ".entity';\n"
        self.imports += "import { " + entity_name + "DTO } from '../entity/" + module_name + ".dto';\n"

    def clean(self):
        self.imports = "import { Injectable } from '@nestjs/common';\n" \
                       "import { BasicCrudService } from '../../../commons/services/crud.service';\n" \
                       "import { InjectRepository } from '@nestjs/typeorm';\nimport { Repository } from 'typeorm';\n"
        self.class_imports = ""
        self.content = ""

    def build_class_imports(self, list_attr: List):
        for i in range(len(list_attr)):
            dict_attr = list_attr[i]
            if str(dict_attr["column"]).startswith("foreign"):
                foreign_parts = str(dict_attr["column"]).split("=")
                foreign_entity_module = foreign_parts[1]
                foreign_entity_module_parts = foreign_entity_module.split(",")
                self.class_imports += "import { " + foreign_entity_module_parts[0] + " } from 'src/api/" + \
                                      foreign_entity_module_parts[3] + "/entity/" + \
                                      foreign_entity_module_parts[3] + ".entity'\n"

    def build_class(self, module_name: str, entity_dict: dict, pk_dict: dict, list_attr: List):
        self.build_additional_imports(module_name, entity_dict["name"])
        self.build_headers(list_attr)
        self.build_class_name(entity_dict, pk_dict)
        self.build_find_id_function(entity_dict, pk_dict)
        self.build_base_creation_function(entity_dict, list_attr)
        self.build_validation_before_creation_function(entity_dict)
        self.build_base_edition_function(entity_dict, pk_dict, list_attr)
        self.build_validation_before_edition_function(entity_dict)
        self.build_close()
        return self.content

    def build_headers(self, list_attr: List):
        self.build_class_imports(list_attr)
        self.content += self.imports
        self.content += self.class_imports
        self.content += "\n"

    def build_class_name(self, dict_class: dict, pk_dict: dict):
        self.content += "@Injectable()\n"
        self.content += "export class " + dict_class["name"] + "Service extends BasicCrudService<" + \
                        dict_class["name"] + ", " + pk_dict["type"] + ", " + dict_class["name"] + "DTO>{\n\n"
        self.content += "    constructor(\n"
        self.content += "        @InjectRepository(" + dict_class["name"] + ")\n"
        self.content += "        protected repo: Repository<" + dict_class["name"] + ">,\n"
        self.content += "    ) {super();}\n\n"

    def build_find_id_function(self, dict_class: dict, pk_dict: dict):
        self.content += "    findById(id: " + pk_dict["type"] + "): Promise<" + dict_class["name"] + ">{\n"
        self.content += "        try{\n"
        self.content += "            return this.findOne({where: {" + pk_dict["name"] + ":id}});\n"
        self.content += "        } catch(err){\n            throw new Error(err.message);\n        }\n    }\n\n"

    def build_base_creation_function(self, dict_class: dict, list_attr: List):
        self.content += "    buildBaseCreation(dto: " + dict_class["name"] + "DTO): " + dict_class["name"] + "{\n"
        self.content += "        //Validations data\n"
        self.content += "        if(! dto) throw new Error('DTO empty');\n\n"
        self.content += "        //Assign data\n"
        self.content += "        let entity = new " + dict_class["name"] + "();\n"
        for i in range(2, len(list_attr)):
            attr_dict = list_attr[i]
            col = str(attr_dict["column"])
            if not col.startswith("foreign_ref"):
                if col.startswith("foreign="):
                    foreign_parts = col.split("=")
                    foreign_entity_module = foreign_parts[1]
                    foreign_entity_module_parts = foreign_entity_module.split(",")
                    self.content += "        let " + foreign_entity_module_parts[3] + " = new " + \
                                    foreign_entity_module_parts[0] + "();\n"
                    self.content += "        " + foreign_entity_module_parts[3] + "." + foreign_entity_module_parts[4]\
                                    + " = dto." + attr_dict["name"] + ";\n"
                    self.content += "        entity." + attr_dict["name"] + " = " + \
                                    foreign_entity_module_parts[3] + ";\n"
                else:
                    self.content += "        entity." + attr_dict["name"] + " = dto." + attr_dict["name"] + ";\n"
        self.content += "        return entity;\n    }\n\n"

    def build_validation_before_creation_function(self, dict_class: dict):
        self.content += "    async dataValidationBeforeCreate(dto: " + dict_class["name"] + "DTO): Promise<void> {\n"
        self.content += "        // Input validations for null values that are required\n"
        self.content += "        // For example validate if not exists for specific(s) properties\n"
        self.content += "        // Example same login, same email, same cod, same nit\n"
        self.content += "    }\n\n"

    def build_base_edition_function(self, dict_class: dict, pk_dict: dict, list_attr: List):
        self.content += "    buildBaseEdition(entity: " + dict_class["name"] + ", dto: " + \
                        dict_class["name"] + "DTO): " + dict_class["name"] + "{\n"
        self.content += "        //Validations data\n"
        self.content += "        if(! dto) throw new Error('DTO empty');\n"
        self.content += "        if(! dto." + pk_dict["name"] + ") throw new Error('Entity id null');\n\n"
        self.content += "        //Assign data\n"
        for i in range(2, len(list_attr)):
            attr_dict = list_attr[i]
            col = str(attr_dict["column"])
            if not col.startswith("foreign_ref"):
                if col.startswith("foreign="):
                    foreign_parts = col.split("=")
                    foreign_entity_module = foreign_parts[1]
                    foreign_entity_module_parts = foreign_entity_module.split(",")
                    self.content += "        let " + foreign_entity_module_parts[3] + " = new " + \
                                    foreign_entity_module_parts[0] + "();\n"
                    self.content += "        " + foreign_entity_module_parts[3] + "." + foreign_entity_module_parts[4] \
                                    + " = dto." + attr_dict["name"] + ";\n"
                    self.content += "        entity." + attr_dict["name"] + " = dto." + attr_dict["name"] + \
                                    " ? " + foreign_entity_module_parts[3] + " : entity." + attr_dict["name"] + ";\n"
                else:
                    self.content += "        entity." + attr_dict["name"] + " = dto." + attr_dict["name"] + \
                                    " ? dto." + attr_dict["name"] + " : entity." + attr_dict["name"] + ";\n"
        self.content += "        return entity;\n    }\n\n"

    def build_validation_before_edition_function(self, dict_class: dict):
        self.content += "    async dataValidationBeforeEdit(dto: " + dict_class["name"] + "DTO): Promise<void> {\n"
        self.content += "        // Input validations for null values that are required\n"
        self.content += "        // For example validate if not exists for specific(s) properties\n"
        self.content += "        // Example same login, same email, same cod, same nit\n"
        self.content += "    }\n\n"

    def build_close(self):
        self.content += "}"
