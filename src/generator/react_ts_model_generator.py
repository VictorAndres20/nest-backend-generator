from typing import List

from src.helpers.find_index import find_index
from src.helpers.folder_handler import get_module_name


def get_empty_value(dict_attr: dict):
    if dict_attr["column"] == 'PrimaryGeneratedColumn':
        return "undefined"

    return "''"


class ReactTSModelGenerator:

    def __init__(self):
        self.imports = ""
        self.class_imports = ""
        self.content = ""

    def clean(self):
        self.imports = ""
        self.class_imports = ""
        self.content = ""

    def build_class_imports(self, list_attr: List):
        class_name = list_attr[0]["name"]
        entity_module = get_module_name(list_attr[0]["table_name"])
        self.class_imports += "import {\n  " + class_name + "DTO,\n  " + class_name + "EntityType,\n} from '../_types/" + \
                              entity_module + ".types';\n"


    def build_class(self, list_attr: List):
        self.build_headers(list_attr)
        self.build_transform_function(list_attr)
        self.build_empty_function(list_attr)

    def build_headers(self, list_attr: List):
        self.build_class_imports(list_attr)
        self.content += self.imports
        self.content += self.class_imports
        self.content += "\n"

    def build_transform_function(self, list_attr: List):
        self.content += "export const transform" + list_attr[0]["name"] + "EntityToDTO = (\n"
        self.content += "  entity: " + list_attr[0]["name"] + "EntityType\n"
        self.content += "): " + list_attr[0]["name"] + "DTO => {\n"
        foreign_index = find_index("column", "foreign", list_attr)
        if foreign_index == -1:
            self.content += "  return { ...entity } as " + list_attr[0]["name"] + "DTO;\n"
        else:
            foreign_destructuring = ""
            for i in range(len(list_attr)):
                dict_attr = list_attr[i]
                if str(dict_attr["column"]) == "foreign":
                    foreign_destructuring += f"{dict_attr["name"]}, "

            self.content += "  const { " + foreign_destructuring + "...rest } = entity;\n"
            self.content += "  const newEnt:" + list_attr[0]["name"] +"DTO = rest as " + list_attr[0]["name"] +"DTO;\n"
            for i in range(len(list_attr)):
                dict_attr = list_attr[i]
                if str(dict_attr["column"]) == "foreign":
                    self.content += "  newEnt." + dict_attr["name"] + " = " +\
                                     dict_attr["name"] + "?." + dict_attr["fe_pk"] + ";\n"
            self.content += "  return newEnt;\n"
        self.content += "};\n\n"

    def build_empty_function(self, list_attr: List):
        self.content += "export const buildEmpty" + list_attr[0]["name"] + "DtoStringShape = () => {\n"
        self.content += "  return {\n"
        for i in range(len(list_attr)):
            dict_attr = list_attr[i]
            if dict_attr["type"] != "entity" and not str(dict_attr["column"]).startswith("foreign_ref"):
                self.content += "    " + dict_attr["name"] + ": " + get_empty_value(dict_attr) + ",\n"
        self.content += "  };\n"
        self.content += "};\n\n"
