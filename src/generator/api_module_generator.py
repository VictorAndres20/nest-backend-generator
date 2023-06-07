from typing import List

from src.generator.module_generator import ModuleGenerator


class ApiModuleGenerator(ModuleGenerator):

    def __init__(self, name="Api"):
        super().__init__(name)

    def build(self, modules: List):
        for i in modules:
            entity_class_name = i["class"]
            module_name = i["module"]
            self.main_imports.append("import { " + entity_class_name + "Module } from './" + module_name + "/"
                                     + module_name + ".module';")
            self.imports.append(entity_class_name + "Module")
