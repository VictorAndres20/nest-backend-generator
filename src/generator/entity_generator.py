from typing import List


def is_column_null(dict_class: dict):
    if dict_class["null"] == '':
        return True

    return False


def check_nullish_operator(dict_class: dict):
    if is_column_null(dict_class):
        return "?"

    return "!"


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
                self.class_imports += "import { " + dict_attr["foreign_entity"] + " } from '../../" + \
                                      dict_attr["fe_module"] + "/entity/" + \
                                      dict_attr["fe_module"] + ".entity'\n"

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
                    if foreign_type == "foreign":
                        self.build_main_content_many_to_one(dict_attr)
                        self.build_dto_main_content(dict_attr, dict_attr["fe_pk_type"])
                    elif foreign_type == "foreign_ref":
                        self.build_main_content_one_to_many(dict_attr)
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
        self.content += "    " + dict_class["name"] + check_nullish_operator(dict_class) + ": " + dict_class["type"] + ";\n\n"

    def build_main_content_many_to_one(self, dict_class: dict):
        self.content += "    " + self.decorator + "ManyToOne(() => " + dict_class["foreign_entity"] + ", e => e." + \
                        dict_class["fe_property"] + ", {" + "\n"
        self.content += "        " + 'onDelete: "CASCADE",' + "\n"
        self.content += "        " + 'eager: true,' + "\n    })\n"
        self.content += "    " + self.decorator + 'JoinColumn({ name: "' + dict_class["name"] + '" })\n'
        self.content += "    " + dict_class["name"] + check_nullish_operator(dict_class) + ": " + dict_class["type"]  + ";\n\n"

    def build_main_content_one_to_many(self, dict_class: dict):
        self.content += "    " + self.decorator + 'OneToMany(() => ' + dict_class["foreign_entity"] + ', e => e.' + \
                        dict_class["fe_property"] + ')\n'
        self.content += "    " + dict_class["name"] + "?: " + dict_class["type"] + ";\n\n"

    def build_close(self):
        self.content += "}"

    def build_class_name(self, dict_class: dict):
        self.content += self.decorator + dict_class["column"] + "({name:'" + dict_class["table_name"] + "'})\n"
        self.content += "export class " + dict_class["name"] + "{\n\n"

    def build_dto_class(self, dict_class: dict):
        self.dto_content += "export class " + dict_class["name"] + "DTO {"
        self.dto_content += "\n"

    def build_dto_main_content(self, dict_class: dict, type_name: str):
        self.dto_content += "    readonly " + dict_class["name"] + "?: " + type_name + ";\n"

    def build_dto_close(self):
        self.dto_content += "}"
