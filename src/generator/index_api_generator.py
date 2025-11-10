BASE_INDEX_API_IMPORTS = "export * from './api.module';"


class IndexApiGenerator:

    def __init__(self, module_list: list):
        self.module_list = module_list
        self.main_export = BASE_INDEX_API_IMPORTS
        self.content = ""

    def clean(self):
        self.main_export = BASE_INDEX_API_IMPORTS
        self.content = ""

    def build_class(self):
        self.build_main_export()
        self.build_module_exports()

    def build_main_export(self):
        self.content += self.main_export
        self.content += "\n"

    def build_module_exports(self):
        for i in self.module_list:
            self.content += "export * from './" + i + "/controller/" + i + ".controller';\n"
            self.content += "export * from './" + i + "/service/" + i + ".service';\n"
            self.content += "export * from './" + i + "/entity/" + i + ".entity';\n"
            self.content += "export * from './" + i + "/entity/" + i + ".dto';\n"
            self.content += "export * from './" + i + "/" + i + ".module';\n"
