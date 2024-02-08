from typing import List, Optional


class SQLGenerator:

    def __init__(self):
        self.default = "DEFAULT"
        self.not_null = "NOT NULL"
        self.content = ""
        self.schema: Optional[str] = None

    def clean(self):
        self.content = ""

    def build_class(self, list_attr: List, dict_class: dict):
        self.build_class_name(dict_class)
        filter_attr = list(filter(lambda x: (str(x["type"]) != "entity" and str(x["column"]) != 'foreign_ref'),
                                  list_attr))
        for i in range(len(filter_attr)):
            dict_attr = filter_attr[i]
            self.build_main_content(dict_attr, i, len(filter_attr))
        self.build_close(list_attr, dict_class)

    def build_main_content(self, dict_class: dict, idx: int, total_data: int):
        self.content += f"    {dict_class['name']} {dict_class['db_type']}"
        if dict_class["default_value"] != '':
            self.content += f" {self.default} {dict_class['default_value']}"
        if dict_class["null"] == '':
            self.content += f" {self.not_null}"
        if total_data != (idx + 1):
            self.content += ","
        self.content += "\n"

    def build_close(self, list_attr: List, dict_class: dict):
        self.content += ");\n"
        pks = filter(lambda item: item['column'].startswith('Primary'), list_attr)
        for i in pks:
            self.content += f"ALTER TABLE {self.schema + '.' if self.schema is not None else ''}" \
                            f"{dict_class['table_name']} ADD CONSTRAINT " \
                            f"pk_{dict_class['table_name']} PRIMARY KEY({i['name']});\n"
        self.content += "\n"
        
    def build_foriegn(self, list_attr: List, dict_class: dict):
        foreign_keys = filter(lambda item: item['column'] == 'foreign', list_attr)
        for i in foreign_keys:
            self.content += f"ALTER TABLE {self.schema + '.' if self.schema is not None else ''}" \
                            f"{dict_class['table_name']} ADD CONSTRAINT " \
                            f"fk_{dict_class['table_name']}_{i['name']} FOREIGN KEY({i['name']}) " \
                            f"REFERENCES {self.schema + '.' if self.schema is not None else ''}{i['fe_module']}({i['fe_pk']});\n"
        self.content += "\n"

    def build_class_name(self, dict_class: dict):
        self.content += f"CREATE TABLE {self.schema + '.' if self.schema is not None else ''}" \
                        f"{dict_class['table_name']}(\n"
