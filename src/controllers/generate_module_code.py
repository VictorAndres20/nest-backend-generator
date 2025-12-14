from src.generator.api_module_generator import ApiModuleGenerator
from src.generator.business_generator import BusinessGenerator
from src.generator.controller_generator import ControllerGenerator
from src.generator.entity_generator import EntityGenerator
from src.generator.entity_module_generator import EntityModuleGenerator
from src.generator.enums_generator import EnumsGenerator
from src.generator.index_api_generator import IndexApiGenerator
from src.generator.react_create_event_generator import ReactCreateEventGenerator
from src.generator.react_find_event_generator import ReactFindEventGenerator
from src.generator.react_model_generator import ReactModelGenerator
from src.generator.react_service_generator import ReactServiceGenerator
from src.generator.react_ts_entity_types_generator import ReactTSEntityTypesGenerator
from src.generator.react_ts_model_generator import ReactTSModelGenerator
from src.generator.react_ts_service_generator import ReactTSServiceGenerator
from src.generator.service_generator import ServiceGenerator
from src.generator.sql_generator import SQLGenerator
from src.helpers.copy_files import copy_essential_files, copy_react_essential_files, copy_react_essential_appjs_files, \
    copy_nest_essential_env_files, copy_react_ts_essential_files, copy_react_ts_essential_app_files, \
    copy_react_ts_essential_root_files
from src.helpers.drawdb_reader import build_list_modules_from_draw_db_io
from src.helpers.file_handler import create_empty_file
from src.helpers.folder_handler import create_folder, copy_essentials, copy_react, get_module_name, copy_react_ts, \
    copy_react_ts_api_client
from src.helpers.write_file import write_code


NEST_ROOT_PATH = "nest"
NEST_SRC_PATH = f"{NEST_ROOT_PATH}/src"
NEST_SRC_ENTITIES_PATH = f"{NEST_SRC_PATH}/_entities"
NEST_SRC_ENUMS_PATH = f"{NEST_SRC_PATH}/_enums"
NEST_SRC_API_PATH = f"{NEST_SRC_PATH}/api"
NEST_SRC_ASSETS_PATH = f"{NEST_SRC_PATH}/assets"

DB_PATH = "db"

REACT_JS_ROOT_PATH = "react-js"
REACT_JS_SRC_PATH = f"{REACT_JS_ROOT_PATH}/src"
REACT_JS_SRC_SERVICES_PATH = f"{REACT_JS_SRC_PATH}/_services"
REACT_JS_SRC_EVENTS_PATH = f"{REACT_JS_SRC_PATH}/_events"
REACT_JS_SRC_HOOKS_PATH = f"{REACT_JS_SRC_PATH}/_hooks"


REACT_TS_ROOT_PATH = "react-ts"
REACT_TS_SRC_PATH = f"{REACT_TS_ROOT_PATH}/src"
REACT_TS_SRC_API_CLIENT_PATH = f"{REACT_TS_SRC_PATH}/_api-client"
REACT_TS_SRC_TYPES_PATH = f"{REACT_TS_SRC_API_CLIENT_PATH}/_types"
REACT_TS_SRC_SERVICES_PATH = f"{REACT_TS_SRC_API_CLIENT_PATH}/_services"
REACT_TS_SRC_HELPERS_PATH = f"{REACT_TS_SRC_API_CLIENT_PATH}/_helpers"
REACT_TS_SRC_HOOKS_PATH = f"{REACT_TS_SRC_API_CLIENT_PATH}/_hooks"
REACT_TS_SRC_SERVICES_COMMONS_PATH = f"{REACT_TS_SRC_SERVICES_PATH}/_commons"


def generate_module(models_path: str, file_path: str, db_schema: str, generate_sql_relations: bool = False, print_model_loaded: bool = False):
    models_path += "/" if not models_path.endswith("/") else ""

    # Create base Nest folders

    create_folder(models_path + NEST_ROOT_PATH)
    create_folder(models_path + NEST_SRC_PATH)
    create_folder(models_path + NEST_SRC_ENTITIES_PATH)
    create_folder(models_path + NEST_SRC_ENUMS_PATH)
    create_folder(models_path + NEST_SRC_API_PATH)
    create_folder(models_path + NEST_SRC_ASSETS_PATH)
    create_empty_file(models_path + NEST_SRC_ASSETS_PATH + "/.gitkeep")

    # Create base DB folders

    create_folder(models_path + DB_PATH)

    # Create base React JS folders

    create_folder(models_path + REACT_JS_ROOT_PATH)
    create_folder(models_path + REACT_JS_SRC_PATH)
    create_folder(models_path + REACT_JS_SRC_SERVICES_PATH)
    create_folder(models_path + REACT_JS_SRC_EVENTS_PATH)

    # Create base React TS folders

    create_folder(models_path + REACT_TS_ROOT_PATH)
    create_folder(models_path + REACT_TS_SRC_PATH)
    create_folder(models_path + REACT_TS_SRC_API_CLIENT_PATH)
    create_folder(models_path + REACT_TS_SRC_TYPES_PATH)
    create_folder(models_path + REACT_TS_SRC_SERVICES_PATH)
    create_folder(models_path + REACT_TS_SRC_HELPERS_PATH)
    create_folder(models_path + REACT_TS_SRC_SERVICES_COMMONS_PATH)

    # First copy React JS and React TS
    copy_react(models_path + f"{REACT_JS_SRC_PATH}/")
    copy_react_ts(models_path + f"{REACT_TS_SRC_PATH}/")
    copy_react_ts_api_client(models_path + f"{REACT_TS_SRC_API_CLIENT_PATH}/")

    ddl = ''

    if not file_path.endswith(".json"):
        raise Exception(f"File {file_path} should be a JSON file from DrawDB.io")

    list_modules, enums = build_list_modules_from_draw_db_io(file_path)

    if print_model_loaded:
        print("MODULES:")
        print(list_modules)
        write_code("./modules.py", str(list_modules), False)

        print("ENUMS:")
        print(enums)
        write_code("./enums.py", str(enums), False)

    # Nest generators
    enums_generator = EnumsGenerator()
    entity_generator = EntityGenerator()
    service_generator = ServiceGenerator()
    business_generator = BusinessGenerator()
    controller_generator = ControllerGenerator()

    # SQL generator
    sql_generator = SQLGenerator()
    sql_generator.schema = db_schema

    # React JS generators
    react_service_generator = ReactServiceGenerator()
    react_model_generator = ReactModelGenerator()
    react_find_event_generator = ReactFindEventGenerator()
    react_create_event_generator = ReactCreateEventGenerator()

    # React TS generators
    react_ts_entity_types_generator = ReactTSEntityTypesGenerator()
    react_ts_service_generator = ReactTSServiceGenerator()
    react_ts_model_generator = ReactTSModelGenerator()

    # ***** Generate Enums

    for enum in enums:
        enums_generator.clean()
        enums_generator.build_class(enum)

        enum_file_name = get_module_name(enum["name"])

        # Write Nest enum
        write_code(models_path + f"{NEST_SRC_ENUMS_PATH}/" + enum_file_name + ".enum.ts",
                   enums_generator.content, False)

        # Write React TS enum type
        write_code(models_path + f"{REACT_TS_SRC_TYPES_PATH}/" + enum_file_name + ".type.ts",
                   enums_generator.content, False)

        # Add DDL to variable
        ddl += f"CREATE TYPE \"{enum["name"]}\" AS ENUM(\n"
        for i in range(0, len(enum["values"])):
            value = enum["values"][i]
            ddl += f"    '{value}'"
            if i < len(enum["values"]) - 1:
                ddl += ","
            ddl += "\n"
        ddl += f");\n\n"

    # ***** Add schema to DDL if there is any

    if db_schema is not None or db_schema != '':
        ddl += f"CREATE SCHEMA {db_schema};\n\n"

    # ***** Generate Modules

    modules = []
    module_names = []
    for i in list_modules:
        module_name = list(i.keys())[0]

        list_attr = i[module_name]
        class_dict = list_attr[0]

        # Generate DB DDL code

        sql_generator.build_class(list_attr, class_dict)
        ddl += sql_generator.content
        sql_generator.clean()

        # Rename module_name
        module_name = get_module_name(module_name)

        module_names.append(module_name)
        modules.append({"class": class_dict["name"], "module": module_name})

        # PK row should be first row
        pk_dict = list_attr[1]
        if not pk_dict["is_primary_key"]:
            raise Exception(f"{module_name} has no primary key or is not it first field in the model")

        # Create Nest entity folders

        create_folder(models_path + f"{NEST_SRC_API_PATH}/" + module_name)
        create_folder(models_path + f"{NEST_SRC_API_PATH}/" + module_name + "/model")
        create_folder(models_path + f"{NEST_SRC_API_PATH}/" + module_name + "/service")
        create_folder(models_path + f"{NEST_SRC_API_PATH}/" + module_name + "/controller")

        # Generate Nest entity with DTO

        entity_generator.clean()
        entity_generator.build_class(list_attr)
        write_code(models_path + f"{NEST_SRC_ENTITIES_PATH}/" + module_name + ".entity.ts",
                   entity_generator.content, False)
        write_code(models_path + f"{NEST_SRC_API_PATH}/" + module_name + "/model/" + module_name + ".dto.ts",
                   entity_generator.dto_content, False)

        # Generate and write Nest service

        service_generator.clean()
        service_generator.build_class(module_name, class_dict, pk_dict, list_attr)
        write_code(models_path + f"{NEST_SRC_API_PATH}/" + module_name + "/service/_" + module_name + ".service.ts",
                   service_generator.content, False)

        # Generate and write Nest business file

        business_generator.clean()
        business_generator.build_class(module_name, class_dict, pk_dict, list_attr)
        write_code(models_path + f"{NEST_SRC_API_PATH}/" + module_name + "/service/" + module_name + ".business.ts",
                   business_generator.content, False)

        # Generate and write Nest controller

        controller_generator.clean()
        controller_generator.build_class(module_name, class_dict, pk_dict)
        write_code(models_path + f"{NEST_SRC_API_PATH}/" + module_name + "/controller/" + module_name + ".controller.ts",
                   controller_generator.content, False)

        # Generate and write Nest Module

        entity_module_generator = EntityModuleGenerator(class_dict["name"])
        entity_module_generator.build(module_name, class_dict["name"])
        entity_module_generator.build_class()
        write_code(models_path + f"{NEST_SRC_API_PATH}/" + module_name + "/" + module_name + ".module.ts",
                   entity_module_generator.content, False)

        # Generate and write React JS entity service
        react_service_generator.clean()
        react_service_generator.build_class(module_name, class_dict, pk_dict)
        write_code(models_path + f"{REACT_JS_SRC_SERVICES_PATH}/" + module_name + ".service.js",
                   react_service_generator.content, False)

        # Create React JS event folder

        create_folder(models_path + f"{REACT_JS_SRC_EVENTS_PATH}/" + module_name)

        # Generate and write React JS entity model

        react_model_generator.clean()
        react_model_generator.build_class(list_attr)
        write_code(models_path + f"{REACT_JS_SRC_EVENTS_PATH}/" + module_name + "/model.js",
                   react_model_generator.content, False)

        # Generate and write React JS entity find event

        react_find_event_generator.clean()
        react_find_event_generator.build_class(module_name, class_dict)
        write_code(models_path + f"{REACT_JS_SRC_EVENTS_PATH}/" + module_name + "/find.event.js",
                   react_find_event_generator.content, False)

        # Generate and write React JS entity create event

        react_create_event_generator.clean()
        react_create_event_generator.build_class(module_name, class_dict)
        write_code(models_path + f"{REACT_JS_SRC_EVENTS_PATH}/" + module_name + "/create.event.js",
                   react_create_event_generator.content, False)

        # Create React JS hooks folder

        create_folder(models_path + f"{REACT_JS_SRC_HOOKS_PATH}/" + module_name)

        # Generate and write React TS entity service

        react_ts_service_generator.clean()
        react_ts_service_generator.build_class(module_name, class_dict, pk_dict, list_attr)
        write_code(models_path + f"{REACT_TS_SRC_SERVICES_PATH}/" + module_name + ".service.ts",
                   react_ts_service_generator.content, False)

        # Generate and write React TS entity model

        react_ts_model_generator.clean()
        react_ts_model_generator.build_class(list_attr)
        write_code(models_path + f"{REACT_TS_SRC_HELPERS_PATH}/" + module_name + ".helper.ts",
                   react_ts_model_generator.content, False)

        # Generate and write React TS entity types

        react_ts_entity_types_generator.clean()
        react_ts_entity_types_generator.build_class(list_attr)
        react_ts_entity_types_content = f"{react_ts_entity_types_generator.content}\n\n{react_ts_entity_types_generator.query_content}"
        react_ts_entity_types_content += f"\n\n{react_ts_entity_types_generator.paged_query_content}\n\n{react_ts_entity_types_generator.dto_content}"
        write_code(models_path + f"{REACT_TS_SRC_TYPES_PATH}/" + module_name + ".types.ts", react_ts_entity_types_content, False)

    # ######### After iterate all entities operations:

    # Generate and write Nest API module

    api_module_generator = ApiModuleGenerator()
    api_module_generator.build(modules)
    api_module_generator.build_class()
    write_code(models_path + f"{NEST_SRC_API_PATH}/api.module.ts", api_module_generator.content, False)

    # Generate and write Nest index.ts for modules exports

    index_api_generator = IndexApiGenerator(module_names)
    index_api_generator.build_class()
    write_code(models_path + f"{NEST_SRC_API_PATH}/index.ts", index_api_generator.content, False)

    # Copy Nest essentials

    copy_essentials(models_path + f"{NEST_SRC_PATH}/")
    copy_essential_files(models_path + f"{NEST_SRC_PATH}/")
    copy_nest_essential_env_files(models_path + f"{NEST_ROOT_PATH}/")

    # Generate DB relations

    if generate_sql_relations:
        ddl += "\n--- Foreign Keys\n"
        sql_generator = SQLGenerator()
        sql_generator.schema = db_schema
        for i in list_modules:
            module_name = list(i.keys())[0]
            list_attr = i[module_name]
            class_dict = list_attr[0]
            sql_generator.build_foreign(list_attr, class_dict)
            ddl += sql_generator.content
            sql_generator.clean()

    # Write DB DDL

    write_code(models_path + f"{DB_PATH}/ddl.sql", ddl, True)

    # Copy React JS essentials

    copy_react_essential_files(models_path + f"{REACT_JS_SRC_SERVICES_PATH}/")
    copy_react_essential_appjs_files(models_path + f"{REACT_JS_SRC_PATH}/")

    # Copy React TS essentials

    copy_react_ts_essential_files(models_path + f"{REACT_TS_SRC_SERVICES_COMMONS_PATH}/")
    copy_react_ts_essential_app_files(models_path + f"{REACT_TS_SRC_PATH}/")
    copy_react_ts_essential_root_files(models_path + f"{REACT_TS_ROOT_PATH}/")
