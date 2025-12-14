from typing import List

from src.helpers.tp_pascal_case import to_camel_case

SERVICE_BASE_IMPORTS = "import { Injectable } from '@nestjs/common';\n" \
                       "import { BasicCrudService } from '../../../_commons/services/crud.service';\n" \
                       "import { InjectRepository } from '@nestjs/typeorm';\nimport { Repository } from 'typeorm';\n"


class ServiceGenerator:

    def __init__(self):
        self.imports = SERVICE_BASE_IMPORTS
        self.class_imports = ""
        self.content = ""

    def build_additional_imports(self, module_name: str, entity_name: str):
        self.imports += "import { " + entity_name + " } from '../../../_entities/" + module_name + ".entity';\n"
        self.imports += "import { " + entity_name + "DTO } from '../model/" + module_name + ".dto';\n"

    def clean(self):
        self.imports = SERVICE_BASE_IMPORTS
        self.class_imports = ""
        self.content = ""

    def build_class_imports(self, list_attr: List):
        # Not necessary to import foreign modules since we use now RelationId decorator in entity
        pass
        #for i in range(len(list_attr)):
        #    dict_attr = list_attr[i]
        #    if str(dict_attr["column"]) == "foreign":
        #        fe_module = get_module_name(dict_attr["fe_module"])
        #        self.class_imports += "import { " + dict_attr["foreign_entity"] + " } from '../../" + \
        #                              fe_module + "/entity/" + \
        #                              fe_module + ".entity';\n"

    def build_class(self, module_name: str, entity_dict: dict, pk_dict: dict, list_attr: List):
        self.build_additional_imports(module_name, entity_dict["name"])
        self.build_headers(list_attr)
        self.build_class_name(entity_dict, pk_dict)
        self.build_find_id_function(entity_dict, pk_dict)
        self.build_base_creation_function(entity_dict, list_attr)
        self.build_validation_before_creation_function(entity_dict)
        self.build_base_edition_function(entity_dict, pk_dict, list_attr)
        self.build_validation_before_edition_function(entity_dict)
        self.build_transformation_before_create_function(entity_dict)
        self.build_transformation_before_edit_function(entity_dict)
        self.build_close()
        return self.content

    def build_headers(self, list_attr: List):
        self.build_class_imports(list_attr)
        self.content += self.imports
        self.content += self.class_imports
        self.content += "\n"

    def build_class_name(self, dict_class: dict, pk_dict: dict):
        self.content += "@Injectable()\n"
        self.content += "export class " + dict_class["name"] + "Service extends BasicCrudService<\n  " + \
                        dict_class["name"] + ",\n  " + pk_dict["type"] + ",\n  " + dict_class["name"] + "DTO\n> {\n"
        self.content += "  constructor(\n"
        self.content += "    @InjectRepository(" + dict_class["name"] + ")\n"
        self.content += "    protected override repo: Repository<" + dict_class["name"] + ">,\n"
        self.content += "  ) {\n    super();\n  }\n\n"

    def build_find_id_function(self, dict_class: dict, pk_dict: dict):
        self.content += "  override findById(" + pk_dict["name"] + "?: " + pk_dict["type"] + " | null): Promise<" + dict_class["name"] + " | null> {\n"
        self.content += "    if( " + pk_dict["name"] + " == null ) return Promise.resolve(null);\n\n"
        self.content += "    try{\n"
        self.content += "      return this.findOne({where: { " + pk_dict["name"] + " } });\n"
        self.content += "    } catch(err){\n      throw new Error((err as Error).message);\n    }\n  }\n\n"

    def build_base_creation_function(self, dict_class: dict, list_attr: List):
        self.content += "  override buildBaseEntityToCreate(dto: " + dict_class["name"] + "DTO): " + dict_class["name"] + " {\n"
        self.content += "    // Data integrity validations\n"
        self.content += "    if(! dto) throw new Error('DTO empty');\n"
        self.content += "\n"
        self.content += "    //Create entity and assign data\n"
        self.content += "    const entity = this.repo.create({\n"
        for i in range(2, len(list_attr)):
            attr_dict = list_attr[i]
            col = str(attr_dict["column"])
            if col != "foreign_ref":
                if col == "foreign":
                    foreign_variable_name = attr_dict["fe_module"] + "_id"
                    self.content += "      " + foreign_variable_name + ": dto." + foreign_variable_name + ",\n"
                else:
                    self.content += "      " + attr_dict["name"] + ": dto." + attr_dict["name"] + ",\n"
        self.content += "    });\n\n"
        self.content += "    return entity;\n  }\n\n"

    def build_validation_before_creation_function(self, dict_class: dict):
        self.content += "  override async dataValidationBeforeCreate(\n"
        self.content += "    // eslint-disable-next-line @typescript-eslint/no-unused-vars\n"
        self.content += "    dto: " + dict_class["name"] + "DTO\n"
        self.content += "  ): Promise<void> {\n"
        self.content += "    // Input validations for null values that are required\n"
        self.content += "    // For example validate if not exists for specific(s) properties\n"
        self.content += "    // Example same login, same email, same cod, same nit\n"
        self.content += "  }\n\n"

    def build_base_edition_function(self, dict_class: dict, pk_dict: dict, list_attr: List):
        self.content += "  override buildBaseEntityToUpdate(entity: " + dict_class["name"] + ", dto: " + \
                        dict_class["name"] + "DTO): " + dict_class["name"] + "{\n"
        self.content += "    //Validations data\n"
        self.content += "    if(! dto) throw new Error('DTO empty');\n"
        self.content += "    if(! dto." + pk_dict["name"] + ") throw new Error('Entity id null');\n\n"
        self.content += "    //Assign data\n"
        for i in range(2, len(list_attr)):
            attr_dict = list_attr[i]
            col = str(attr_dict["column"])
            if col != "foreign_ref":
                if col == "foreign":
                    foreign_variable_name = attr_dict["fe_module"] + "_id"
                    self.content += "    entity." + foreign_variable_name + " = dto." + foreign_variable_name + \
                                    " ?? " + " entity." + foreign_variable_name + ";\n"
                else:
                    self.content += "    entity." + attr_dict["name"] + " = dto." + attr_dict["name"] + \
                                    " ?? " + " entity." + attr_dict["name"] + ";\n"
        self.content += "\n    return entity;\n  }\n\n"

    def build_validation_before_edition_function(self, dict_class: dict):
        self.content += "  override async dataValidationBeforeUpdate(\n"
        self.content += "    // eslint-disable-next-line @typescript-eslint/no-unused-vars\n"
        self.content += "    entity: " + dict_class["name"] + ",\n"
        self.content += "    // eslint-disable-next-line @typescript-eslint/no-unused-vars\n"
        self.content += "    dto: " + dict_class["name"] + "DTO\n"
        self.content += "  ): Promise<void> {\n"
        self.content += "    // Input validations for null values that are required\n"
        self.content += "    // For example validate if not exists for specific(s) properties\n"
        self.content += "    // Example same login, same email, same cod, same nit\n"
        self.content += "  }\n\n"

    def build_transformation_before_create_function(self, dict_class: dict):
        self.content += "  override dtoTransformBeforeCreate(dto: " + dict_class["name"] + "DTO): " + dict_class["name"] + "DTO {\n"
        self.content += "    // Use this function to do transformation on dto for safe data\n"
        self.content += "    // Example:\n"
        self.content += "    // return { ...dto, name:  dto.name?.trim() };\n"
        self.content += "    return dto;\n"
        self.content += "  }\n\n"

    def build_transformation_before_edit_function(self, dict_class: dict):
        self.content += "  override dtoTransformBeforeUpdate(dto: " + dict_class["name"] + "DTO): " + dict_class["name"] + "DTO {\n"
        self.content += "    // Use this function to do transformation on dto for safe data\n"
        self.content += "    // Example:\n"
        self.content += "    // return { ...dto, name:  dto.name?.trim() };\n"
        self.content += "    return this.dtoTransformBeforeCreate(dto);\n"
        self.content += "  }\n\n"

    def build_close(self):
        self.content += "}"
