from src.generator.api_module_generator import ApiModuleGenerator
from src.generator.controller_generator import ControllerGenerator
from src.generator.entity_generator import EntityGenerator
from src.generator.entity_module_generator import EntityModuleGenerator
from src.generator.index_api_generator import IndexApiGenerator
from src.generator.react_create_event_generator import ReactCreateEventGenerator
from src.generator.react_find_event_generator import ReactFindEventGenerator
from src.generator.react_model_generator import ReactModelGenerator
from src.generator.react_service_generator import ReactServiceGenerator
from src.generator.service_generator import ServiceGenerator
from src.generator.sql_generator import SQLGenerator
from src.helpers.copy_files import copy_essential_files, copy_react_essential_files, copy_react_essential_appjs_files
from src.helpers.drawdb_reader import build_list_modules_from_draw_db_io
from src.helpers.excel_reader import read_excel_to_list_dict
from src.helpers.folder_handler import create_folder, copy_essentials, copy_react
from src.helpers.write_file import write_code


def generate_module(models_path: str, file_path: str, db_schema: str, generate_sql_relations: bool = False):

    # Create base folders

    create_folder(models_path + "nest")
    create_folder(models_path + "nest/src")
    create_folder(models_path + "nest/src/api")

    create_folder(models_path + "db")

    create_folder(models_path + "react")
    create_folder(models_path + "react/src")
    create_folder(models_path + "react/src/_services")
    create_folder(models_path + "react/src/_events")

    # First copy React
    copy_react(models_path + "react/src/")

    ddl = ''

    list_modules = build_list_modules_from_draw_db_io(file_path) if file_path.endswith(".json") else read_excel_to_list_dict(file_path)
    # print(list_modules)

    entity_generator = EntityGenerator()
    service_generator = ServiceGenerator()
    controller_generator = ControllerGenerator()
    sql_generator = SQLGenerator()
    sql_generator.schema = db_schema
    react_service_generator = ReactServiceGenerator()
    react_model_generator = ReactModelGenerator()
    react_find_event_generator = ReactFindEventGenerator()
    react_create_event_generator = ReactCreateEventGenerator()

    modules = []
    module_names = []
    for i in list_modules:
        module_name = list(i.keys())[0]
        list_attr = i[module_name]
        class_dict = list_attr[0]
        module_names.append(module_name)
        modules.append({"class": class_dict["name"], "module": module_name})
        pk_dict = list_attr[1]

        # Create Nest entity folders

        create_folder(models_path + "nest/src/api/" + module_name)
        create_folder(models_path + "nest/src/api/" + module_name + "/entity")
        create_folder(models_path + "nest/src/api/" + module_name + "/service")
        create_folder(models_path + "nest/src/api/" + module_name + "/controller")

        # Generate Nest entity with DTO

        entity_generator.clean()
        entity_generator.build_class(list_attr)
        write_code(models_path + "nest/src/api/" + module_name + "/entity/" + module_name + ".entity.ts",
                   entity_generator.content, False)
        write_code(models_path + "nest/src/api/" + module_name + "/entity/" + module_name + ".dto.ts",
                   entity_generator.dto_content, False)

        # Generate and write Nest service

        service_generator.clean()
        service_generator.build_class(module_name, class_dict, pk_dict, list_attr)
        write_code(models_path + "nest/src/api/" + module_name + "/service/" + module_name + ".service.ts",
                   service_generator.content, False)

        # Generate and write Nest controller

        controller_generator.clean()
        controller_generator.build_class(module_name, class_dict, pk_dict)
        write_code(models_path + "nest/src/api/" + module_name + "/controller/" + module_name + ".controller.ts",
                   controller_generator.content, False)

        # Generate and write Nest Module

        entity_module_generator = EntityModuleGenerator(class_dict["name"])
        entity_module_generator.build(module_name, class_dict["name"])
        entity_module_generator.build_class()
        write_code(models_path + "nest/src/api/" + module_name + "/" + module_name + ".module.ts",
                   entity_module_generator.content, False)

        # Generate DB DDL code

        sql_generator.build_class(list_attr, class_dict)
        ddl += sql_generator.content
        sql_generator.clean()

        # Generate and write React JS entity service
        react_service_generator.clean()
        react_service_generator.build_class(module_name, class_dict, pk_dict)
        write_code(models_path + "react/src/_services/" + module_name + ".service.js",
                   react_service_generator.content, False)

        # Create React JS event folder

        create_folder(models_path + "react/src/_events/" + module_name)

        # Generate and write React JS entity model

        react_model_generator.clean()
        react_model_generator.build_class(list_attr)
        write_code(models_path + "react/src/_events/" + module_name + "/model.js",
                   react_model_generator.content, False)

        # Generate and write React JS entity find event

        react_find_event_generator.clean()
        react_find_event_generator.build_class(module_name, class_dict)
        write_code(models_path + "react/src/_events/" + module_name + "/find.event.js",
                   react_find_event_generator.content, False)

        # Generate and write React JS entity create event

        react_create_event_generator.clean()
        react_create_event_generator.build_class(module_name, class_dict)
        write_code(models_path + "react/src/_events/" + module_name + "/create.event.js",
                   react_create_event_generator.content, False)

        # Create React JS hooks folder

        create_folder(models_path + "react/src/_hooks/" + module_name)

    # ######### After iterate all entities operations:

    # Generate and write Nest API module

    api_module_generator = ApiModuleGenerator()
    api_module_generator.build(modules)
    api_module_generator.build_class()
    write_code(models_path + "nest/src/api/api.module.ts", api_module_generator.content, False)

    # Generate and write Nest index.ts for modules exports

    index_api_generator = IndexApiGenerator(module_names)
    index_api_generator.build_class()
    write_code(models_path + "nest/src/api/index.ts", index_api_generator.content, False)

    # Copy Nest essentials

    copy_essentials(models_path + "nest/src/")
    copy_essential_files(models_path + "nest/src/")

    # Generate DB relations

    if generate_sql_relations:
        ddl += "\n--- Foreign Keys\n"
        sql_generator = SQLGenerator()
        sql_generator.schema = db_schema
        for i in list_modules:
            module_name = list(i.keys())[0]
            list_attr = i[module_name]
            class_dict = list_attr[0]
            sql_generator.build_foriegn(list_attr, class_dict)
            ddl += sql_generator.content
            sql_generator.clean()

    # Write DB DDL

    write_code(models_path + "db/ddl.sql", ddl, True)

    # Copy React JS essentials

    copy_react_essential_files(models_path + "react/src/_services/")
    copy_react_essential_appjs_files(models_path + "react/src/")
