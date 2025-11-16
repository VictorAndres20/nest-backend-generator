from src.helpers.to_upper_snake_case import to_upper_snake_case
from src.helpers.tp_pascal_case import to_pascal_case


class EnumsGenerator:

    def __init__(self):
        self.imports = ""
        self.class_imports = ""
        self.content = ""

    def clean(self):
        self.class_imports = ""
        self.content = ""

    def build_class_imports(self, enum: dict):
        pass

    def build_class(self, enum: dict):
        self.build_headers(enum)
        values = enum["values"]

        for value in values:
            self.content += f"  {to_upper_snake_case(value)} = '{value}', \n"

        self.build_close()

    def build_headers(self, enum: dict):
        self.content += self.imports
        self.content += self.class_imports
        self.build_class_name(enum)
        # self.content += "\n"

    def build_close(self):
        self.content += "}"

    def build_class_name(self, dict_class: dict):
        self.content += "export enum " + to_pascal_case(dict_class["name"]) + " {\n"
