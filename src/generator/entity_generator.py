from typing import List

from src.helpers.folder_handler import get_module_name
from src.helpers.tp_pascal_case import to_pascal_case


def is_column_null(dict_class: dict):
    if dict_class["null"] == '':
        return False

    return True


def check_nullish_operator(dict_class: dict, is_pk_null: bool = False):
    column = dict_class["column"]
    if is_column_null(dict_class) or (is_pk_null and column == 'PrimaryGeneratedColumn'):
        return "?"

    return "!"


def check_null_column_definition(dict_class: dict):
    if is_column_null(dict_class):
        return "?"

    return "!"


def check_null_type(dict_class: dict):
    if is_column_null(dict_class):
        return " | null"

    return ""


def check_column_decorator_config(dict_class: dict):
    if dict_class["column"] != "Column":
        return ""

    is_enum = bool(dict_class["isEnum"])

    db_type = dict_class["db_type"]
    db_type_formated = db_type.split("(")[0]
    db_type_formated = 'enum' if is_enum else str(db_type_formated).lower()

    column_decorator_config = "{ type: '" + db_type_formated + "'"

    if db_type_formated == 'NUMERIC':
        column_decorator_config += ", scale: 2, precision: 10"

    if is_column_null(dict_class):
        column_decorator_config += ", nullable: true"

    if is_enum:
        column_decorator_config += ", enum: " + to_pascal_case(db_type)

    column_decorator_config += " }"

    return column_decorator_config


class EntityGenerator:

    def __init__(self):
        self.imports = ""
        self.class_imports = ""
        self.decorator = "@"
        self.content = ""
        self.dto_imports = ""
        self.dto_content = ""

    def clean(self):
        self.class_imports = ""
        self.content = ""
        self.dto_imports = ""
        self.dto_content = ""

    def build_class_imports(self, list_attr: List):
        has_one_to_many = False
        has_many_to_one = False
        has_pk_generated = False
        has_pk = False
        for i in range(len(list_attr)):
            dict_attr = list_attr[i]

            # First ENUMS

            if bool(dict_attr["isEnum"]):
                fe_entity = dict_attr["type"]
                fe_module = get_module_name(dict_attr["fe_module"])
                enum_import = "import { " + fe_entity + " } from '../../../_enums/" + \
                                      fe_module + ".enum';\n"
                self.class_imports += enum_import
                self.dto_imports += enum_import

            # Second FOREIGN ENTITIES

            if str(dict_attr["column"]).startswith("foreign"):
                if str(dict_attr["column"]).endswith("ref"):
                    has_one_to_many = True
                else:
                    has_many_to_one = True
                fe_module = get_module_name(dict_attr["fe_module"])
                self.class_imports += "import { " + dict_attr["foreign_entity"] + " } from '../../" + \
                                      fe_module + "/entity/" + \
                                      fe_module + ".entity';\n"

            # Third PK TYPE
            if bool(dict_attr["is_primary_key"]):
                if str(dict_attr["column"]).endswith("GeneratedColumn"):
                    has_pk_generated = True
                else:
                    has_pk = True

        self.class_imports += "import {\n  Entity,\n  Column,\n"
        if has_pk:
            self.class_imports += "  PrimaryColumn,\n"
        if has_pk_generated:
            self.class_imports += "  PrimaryGeneratedColumn,\n"
        if has_many_to_one:
            self.class_imports += "  ManyToOne,\n  JoinColumn,\n"
            self.class_imports += "  RelationId,\n"
        if has_one_to_many:
            self.class_imports += "  OneToMany,\n"
        self.class_imports += "} from 'typeorm';\n"

    def build_class(self, list_attr: List):
        self.build_headers(list_attr)
        for i in range(len(list_attr)):
            dict_attr = list_attr[i]
            if dict_attr["type"] == "entity":
                self.build_class_name(dict_attr)
                self.build_dto_class(dict_attr)
            else:
                # Entity Properties

                # Foreign properties
                if str(dict_attr["column"]).startswith("foreign"):
                    foreign_parts = str(dict_attr["column"]).split("=")
                    foreign_type = foreign_parts[0]
                    if foreign_type == "foreign":
                        self.build_main_content_many_to_one(dict_attr)
                        self.build_dto_main_content(dict_attr, dict_attr["fe_pk_type"])
                    elif foreign_type == "foreign_ref":
                        self.build_main_content_one_to_many(dict_attr)
                        self.build_dto_main_content(dict_attr, dict_attr["fe_pk_type"])
                elif bool(dict_attr["isEnum"]):
                    self.build_main_content_enum(dict_attr)
                    self.build_dto_main_content(dict_attr, dict_attr["type"])
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
        self.content += "  " + self.decorator + dict_class["column"] + "(" + check_column_decorator_config(dict_class) +")\n"
        self.content += "  " + dict_class["name"] + check_nullish_operator(dict_class) + ": " + dict_class["type"] + check_null_type(dict_class) + ";\n\n"

    def build_main_content_enum(self, dict_class: dict):
        self.content += "  " + self.decorator + dict_class["column"] + "(" + check_column_decorator_config(dict_class) +")\n"
        self.content += "  " + dict_class["name"] + check_nullish_operator(dict_class) + ": " + dict_class["type"] + check_null_type(dict_class) + ";\n\n"

    def build_main_content_many_to_one(self, dict_class: dict):
        self.content += "  " + self.decorator + "ManyToOne(() => " + dict_class["foreign_entity"] + ", e => e." + \
                        dict_class["fe_property"] + ", {" + "\n"
        self.content += "    nullable: true,\n" if is_column_null(dict_class) else ""
        self.content += "    " + 'onDelete: "CASCADE",' + "\n"
        self.content += "    " + 'eager: true,' + "\n  })\n"
        self.content += "  " + self.decorator + 'JoinColumn({ name: "' + dict_class["name"] + '" })\n'
        self.content += "  " + dict_class["name"] + check_nullish_operator(dict_class) + ": " + dict_class["foreign_entity"] + check_null_type(dict_class) + ";\n\n"
        # Add RelationId decorator
        self.content += "  " + self.decorator + 'RelationId((entity: ' + to_pascal_case(
            dict_class["table_name"]) + ') => entity.' + dict_class["name"] + ')\n'
        if dict_class["is_primary_key"]:
            self.content += "  @PrimaryColumn()\n"

        self.content += f"  {dict_class["name"]}_id{check_nullish_operator(dict_class)}: {dict_class["fe_pk_type"] + check_null_type(dict_class)}\n"
        self.content += "\n"

    def build_main_content_one_to_many(self, dict_class: dict):
        self.content += "  " + self.decorator + 'OneToMany(() => ' + dict_class["foreign_entity"] + ', (e) => e.' + \
                        dict_class["fe_property"] + ')\n'
        self.content += "  " + dict_class["name"] + "?: " + dict_class["foreign_entity"] + ";\n\n"

    def build_close(self):
        self.content += "}"

    def build_class_name(self, dict_class: dict):
        self.content += self.decorator + dict_class["column"] + "({ name: '" + dict_class["table_name"] + "' })\n"
        self.content += "export class " + dict_class["name"] + " {\n"

    def build_dto_class(self, dict_class: dict):
        self.dto_content += self.dto_imports
        self.dto_content += "\n"
        self.dto_content += "export class " + dict_class["name"] + "DTO {"
        self.dto_content += "\n"

    def build_dto_main_content(self, dict_class: dict, type_name: str):
        if dict_class["column"] == "foreign":
            self.dto_content += "  " + dict_class["name"] + "_id" + check_nullish_operator(dict_class, True) + ": " + type_name + ";\n"
        elif dict_class["column"] == "foreign_ref":
            # self.dto_content += "  " + dict_class["name"] + "_id_list" + "?: " + type_name + "[];\n"
            pass
        else:
            self.dto_content += "  " + dict_class["name"] + check_nullish_operator(dict_class,True) + ": " + type_name + ";\n"

    def build_dto_close(self):
        self.dto_content += "}"
