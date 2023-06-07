from src.generator.api_module_generator import ApiModuleGenerator
from src.generator.controller_generator import ControllerGenerator
from src.generator.entity_generator import EntityGenerator
from src.generator.entity_module_generator import EntityModuleGenerator
from src.generator.service_generator import ServiceGenerator
from src.helpers.copy_files import copy_essential_files
from src.helpers.excel_reader import read_excel_to_list_dict
from src.helpers.folder_handler import create_folder, copy_essentials
from src.helpers.write_file import write_code


def generate_module(models_path: str, excel_path: str):
    create_folder(models_path + "src")
    create_folder(models_path + "src/api")
    list_modules = read_excel_to_list_dict(excel_path)
    print(list_modules)
    entity_generator = EntityGenerator()
    service_generator = ServiceGenerator()
    controller_generator = ControllerGenerator()
    modules = []
    for i in list_modules:
        module_name = list(i.keys())[0]
        list_attr = i[module_name]
        class_dict = list_attr[0]
        modules.append({"class": class_dict["name"], "module": module_name})
        pk_dict = list_attr[1]
        create_folder(models_path + "src/api/" + module_name)
        create_folder(models_path + "src/api/" + module_name + "/entity")
        create_folder(models_path + "src/api/" + module_name + "/service")
        create_folder(models_path + "src/api/" + module_name + "/controller")
        entity_generator.clean()
        entity_generator.build_class(list_attr)
        write_code(models_path + "src/api/" + module_name + "/entity/" + module_name + ".entity.ts",
                   entity_generator.content)
        write_code(models_path + "src/api/" + module_name + "/entity/" + module_name + ".dto.ts",
                   entity_generator.dto_content)
        service_generator.clean()
        service_generator.build_class(module_name, class_dict, pk_dict, list_attr)
        write_code(models_path + "src/api/" + module_name + "/service/" + module_name + ".service.ts",
                   service_generator.content)
        controller_generator.clean()
        controller_generator.build_class(module_name, class_dict, pk_dict)
        write_code(models_path + "src/api/" + module_name + "/controller/" + module_name + ".controller.ts",
                   controller_generator.content)
        entity_module_generator = EntityModuleGenerator(class_dict["name"])
        entity_module_generator.build(module_name, class_dict["name"])
        entity_module_generator.build_class()
        write_code(models_path + "src/api/" + module_name + "/" + module_name + ".module.ts",
                   entity_module_generator.content)

    api_module_generator = ApiModuleGenerator()
    api_module_generator.build(modules)
    api_module_generator.build_class()
    write_code(models_path + "src/api/api.module.ts", api_module_generator.content)
    copy_essentials(models_path + "src/")
    copy_essential_files(models_path + "src/")
