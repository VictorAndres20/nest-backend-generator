from typing import List

from src.helpers.folder_handler import get_module_name


def is_column_null(dict_class: dict):
    if dict_class["null"] == '':
        return False

    return True


def check_nullish_operator(dict_class: dict, is_pk_null: bool = False):
    column = dict_class["column"]
    if is_column_null(dict_class) or (is_pk_null and column == 'PrimaryGeneratedColumn'):
        return "?"

    return ""


def check_null_type(dict_class: dict):
    if is_column_null(dict_class):
        return " | null"

    return ""


class ReactTSEntityTypesGenerator:

    def __init__(self):
        self.imports = ""
        self.class_imports = ""
        self.content = ""
        self.dto_imports = ""
        self.dto_content = ""
        self.query_content = ""
        self.paged_query_content = ""

    def clean(self):
        self.class_imports = ""
        self.content = ""
        self.dto_content = ""
        self.query_content = ""
        self.paged_query_content = ""

    def build_class_imports(self, list_attr: List):
        for i in range(len(list_attr)):
            dict_attr = list_attr[i]

            # First ENUMS

            if bool(dict_attr["isEnum"]):
                fe_entity = dict_attr["type"]
                fe_module = get_module_name(dict_attr["fe_module"])
                enum_import = "import { type " + fe_entity + " } from './" + \
                              fe_module + ".type';\n"
                self.class_imports += enum_import

            if str(dict_attr["column"]).startswith("foreign") or str(dict_attr["column"]).startswith("many_to_many"):
                fe_module = get_module_name(dict_attr["fe_module"])
                self.class_imports += "import {\n  type " + dict_attr["foreign_entity"] + "EntityQuery,\n  type " + dict_attr["foreign_entity"] + "EntityType,\n} from './" + \
                                      fe_module + ".types';\n"

    def build_class(self, list_attr: List):
        self.build_headers(list_attr)
        for i in range(len(list_attr)):
            dict_attr = list_attr[i]
            if dict_attr["type"] == "entity":
                self.build_class_name(dict_attr)
                self.build_dto_class(dict_attr)
                self.build_query_class(dict_attr)
                self.build_paged_query_class(dict_attr)
            else:
                if str(dict_attr["column"]).startswith("foreign"):
                    foreign_parts = str(dict_attr["column"]).split("=")
                    foreign_type = foreign_parts[0]
                    if foreign_type == "foreign":
                        self.build_main_content_many_to_one(dict_attr)
                        self.build_dto_main_content(dict_attr, dict_attr["fe_pk_type"])
                        self.build_query_main_content_many_to_one(dict_attr)
                    elif foreign_type == "foreign_ref":
                        self.build_main_content_one_to_many(dict_attr)
                        self.build_query_main_content_one_to_many(dict_attr)
                elif str(dict_attr["column"]) == "many_to_many_owner":
                    self.build_main_content_many_to_many(dict_attr)
                    self.build_dto_main_content(dict_attr, dict_attr["fe_pk_type"])
                    self.build_query_main_content_many_to_many(dict_attr)
                elif str(dict_attr["column"]) == "many_to_many":
                    self.build_main_content_many_to_many(dict_attr)
                    self.build_query_main_content_many_to_many(dict_attr)
                else:
                    self.build_main_content(dict_attr)
                    self.build_dto_main_content(dict_attr, dict_attr["type"])
                    self.build_query_main_content(dict_attr)

        self.build_paged_query_main_content()

        self.build_close()
        self.build_dto_close()
        self.build_query_close()
        self.build_paged_query_close()

    def build_headers(self, list_attr: List):
        self.build_class_imports(list_attr)
        self.content += self.imports
        self.content += self.class_imports
        self.content += "\n"

    def build_main_content(self, dict_class: dict):
        self.content += "  " + dict_class["name"] + check_nullish_operator(dict_class) + ": " + dict_class["type"] + check_null_type(dict_class) + ";\n"

    def build_main_content_many_to_one(self, dict_class: dict):
        self.content += "  " + dict_class["name"] + "_id" + check_nullish_operator(dict_class) + ": " + dict_class["fe_pk_type"] + check_null_type(dict_class) + ";\n"
        self.content += "  " + dict_class["name"] + check_nullish_operator(dict_class) + ": " + dict_class["foreign_entity"] + "EntityType" + check_null_type(dict_class) + ";\n"

    def build_main_content_many_to_many(self, dict_class: dict):
        self.content += "  " + dict_class["name"] + "?: " + dict_class["foreign_entity"] + "EntityType[];\n"

    def build_main_content_one_to_many(self, dict_class: dict):
        self.content += "  " + dict_class["name"] + "?: " + dict_class["foreign_entity"] + "EntityType[];\n"

    def build_close(self):
        self.content += "}"

    def build_class_name(self, dict_class: dict):
        self.content += "export interface " + dict_class["name"] + "EntityType {\n"

    def build_dto_class(self, dict_class: dict):
        self.dto_content += "export interface " + dict_class["name"] + "DTO {\n"

    def build_dto_main_content(self, dict_class: dict, type_name: str):
        if dict_class["column"] == "foreign":
            self.dto_content += "  " + dict_class["name"] + "_id" + check_nullish_operator(dict_class, True) + ": " + type_name + ";\n"
        elif dict_class["column"] == "foreign_ref":
            # self.dto_content += "  " + dict_class["name"] + "_id_list" + "?: " + type_name + "[];\n"
            pass
        else:
            self.dto_content += "  " + dict_class["name"] + check_nullish_operator(dict_class, True) + ": " + type_name + ";\n"

    def build_dto_close(self):
        self.dto_content += "}"

    def build_query_class(self, dict_class: dict):
        self.query_content += "export interface " + dict_class["name"] + "EntityQuery {\n"

    def build_query_main_content(self, dict_class: dict):
        self.query_content += "  " + dict_class["name"] + "?: " + dict_class["type"] + ";\n"

    def build_query_main_content_many_to_one(self, dict_class: dict):
        self.query_content += "  " + dict_class["name"] + "_id" + check_nullish_operator(dict_class) + ": " + dict_class["fe_pk_type"] + check_null_type(dict_class) + ";\n"
        self.query_content += "  " + dict_class["name"] + "?: " + dict_class["foreign_entity"] + "EntityQuery" + ";\n"

    def build_query_main_content_one_to_many(self, dict_class: dict):
        self.query_content += "  " + dict_class["name"] + "?: " + dict_class["foreign_entity"] + "EntityQuery[];\n"

    def build_query_main_content_many_to_many(self, dict_class: dict):
        self.query_content += "  " + dict_class["name"] + "?: " + dict_class["foreign_entity"] + "EntityQuery[];\n"

    def build_query_close(self):
        self.query_content += "}"

    def build_paged_query_class(self, dict_class: dict):
        self.paged_query_content += "export interface " + dict_class["name"] + "EntityPagedQuery extends " + dict_class["name"] + "EntityQuery {\n"

    def build_paged_query_main_content(self):
        self.paged_query_content += "  page: number;\n"
        self.paged_query_content += "  limit?: number | null;\n"

    def build_paged_query_close(self):
        self.paged_query_content += "}"
