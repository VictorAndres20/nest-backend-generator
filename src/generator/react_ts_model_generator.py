from typing import List


class ReactTSModelGenerator:

    def __init__(self):
        self.imports = ""
        self.content = ""

    def clean(self):
        self.imports = ""
        self.content = ""

    def build_class(self, list_attr: List):
        self.build_headers()
        self.build_validate_function(list_attr)
        self.build_transform_function(list_attr)
        self.build_empty_function(list_attr)

    def build_headers(self):
        self.content += self.imports

    def build_validate_function(self, list_attr: List):
        self.content += "export const validate" + list_attr[0]["name"] + "DTO = (body) => {\n" +\
                        "  //const {  } = body;\n" +\
                        "};\n\n"

    def build_transform_function(self, list_attr: List):
        self.content += "export const transform" + list_attr[0]["name"] + "Entity = (entity) => {\n"
        self.content += "  let newEnt = {...entity}\n"
        for i in range(len(list_attr)):
            dict_attr = list_attr[i]
            if str(dict_attr["column"]) == "foreign":
                self.content += "  newEnt." + dict_attr["name"] + " = newEnt." +\
                                 dict_attr["name"] + "?." + dict_attr["fe_pk"] + ";\n"
        self.content += "  return newEnt;\n"
        self.content += "};\n\n"

    def build_empty_function(self, list_attr: List):
        self.content += "export const buildEmpty" + list_attr[0]["name"] + "Entity = () => {\n"
        self.content += "  return {\n"
        for i in range(len(list_attr)):
            dict_attr = list_attr[i]
            if dict_attr["type"] != "entity" and not str(dict_attr["column"]).startswith("foreign_ref"):
                self.content += "    " + dict_attr["name"] + ": '',\n"
        self.content += "  };\n"
        self.content += "};\n\n"
