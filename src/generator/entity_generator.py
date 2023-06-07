from typing import List


class EntityGenerator:

    def __init__(self):
        self.imports = "import { Entity, Column, PrimaryGeneratedColumn, PrimaryColumn, OneToMany," \
                       " ManyToOne, JoinColumn } from 'typeorm';\n"
        self.class_imports = ""
        self.decorator = "@"
        self.content = ""
        self.dto_content = ""

    def clean(self):
        self.class_imports = ""
        self.content = ""
        self.dto_content = ""

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

    def build_class(self, list_attr: List):
        self.build_headers(list_attr)
        for i in range(len(list_attr)):
            dict_attr = list_attr[i]
            if dict_attr["type"] == "entity":
                self.build_class_name(dict_attr)
                self.build_dto_class(dict_attr)
            else:
                if str(dict_attr["column"]).startswith("foreign"):
                    foreign_parts = str(dict_attr["column"]).split("=")
                    foreign_type = foreign_parts[0]
                    foreign_entity_module = foreign_parts[1]
                    foreign_entity_module_parts = foreign_entity_module.split(",")
                    if foreign_type == "foreign":
                        self.build_main_content_many_to_one(dict_attr, foreign_entity_module_parts)
                        self.build_dto_main_content(dict_attr, foreign_entity_module_parts[2])
                    elif foreign_type == "foreign_ref":
                        self.build_main_content_one_to_many(dict_attr, foreign_entity_module_parts)
                else:
                    self.build_main_content(dict_attr)
                    self.build_dto_main_content(dict_attr, dict_attr["type"])
        self.build_close()
        self.build_dto_close()

    def build_headers(self, list_attr: List):
        self.build_class_imports(list_attr)
        self.content += self.imports
        self.content += self.class_imports
        self.content += "\n"

    def build_main_content(self, dict_class: dict):
        self.content += "    " + self.decorator + dict_class["column"] + "\n"
        self.content += "    " + dict_class["name"] + ": " + dict_class["type"] + ";\n\n"

    def build_main_content_many_to_one(self, dict_class: dict, foreign_entity_module: list):
        self.content += "    " + self.decorator + "ManyToOne(() => " + foreign_entity_module[0] + ", e => e." + \
                        foreign_entity_module[1] + ", {" + "\n"
        self.content += "        " + 'onDelete: "CASCADE",' + "\n"
        self.content += "        " + 'eager: true,' + "\n    })\n"
        self.content += "    " + self.decorator + 'JoinColumn({ name: "' + dict_class["name"] + '" })\n'
        self.content += "    " + dict_class["name"] + ": " + dict_class["type"] + ";\n\n"

    def build_main_content_one_to_many(self, dict_class: dict, foreign_entity_module: list):
        self.content += "    " + self.decorator + 'OneToMany(() => ' + foreign_entity_module[0] + ', e => e.' + \
                        foreign_entity_module[1] + ')\n'
        self.content += "    " + dict_class["name"] + ": " + dict_class["type"] + ";\n\n"

    def build_close(self):
        self.content += "}"

    def build_class_name(self, dict_class: dict):
        self.content += self.decorator + dict_class["column"] + "\n"
        self.content += "export class " + dict_class["name"] + "{\n\n"

    def build_dto_class(self, dict_class: dict):
        self.dto_content += "export class " + dict_class["name"] + "DTO {"
        self.dto_content += "\n"

    def build_dto_main_content(self, dict_class: dict, type_name: str):
        self.dto_content += "    readonly " + dict_class["name"] + ": " + type_name + ";\n"

    def build_dto_close(self):
        self.dto_content += "}"


