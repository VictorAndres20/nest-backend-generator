from src.generator.module_generator import ModuleGenerator


class EntityModuleGenerator(ModuleGenerator):

    def __init__(self, name):
        super().__init__(name)

    def build(self, module_name: str, entity_class_name: str):
        self.main_imports.append("import { TypeOrmModule } from '@nestjs/typeorm';")
        self.main_imports.append("import { " + entity_class_name + " } from './entity/"
                                 + module_name + ".entity';")
        self.main_imports.append("import { " + entity_class_name + "Service } from './service/"
                                 + module_name + ".service';")
        self.main_imports.append("import { " + entity_class_name + "Controller } from './controller/"
                                 + module_name + ".controller';")
        self.imports.append("TypeOrmModule.forFeature([" + entity_class_name + "])")
        self.controllers.append(entity_class_name + "Controller")
        self.providers.append(entity_class_name + "Service")
        self.exports.append(entity_class_name + "Service")
