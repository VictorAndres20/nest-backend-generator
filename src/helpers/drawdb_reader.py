import json
from src.helpers.find_index import find_index_by_key, find_index
from src.helpers.tp_pascal_case import to_pascal_case

string_types = [
    "VARCHAR",
    "TEXT",
    "CHAR"
]

number_types = [
    "SMALLINT",
    "INTEGER",
    "DECIMAL",
    "NUMBER",
    "SERIAL",
]

data_types = [
    "DATE",
    "TIMESTAMP",
    "TIMESTAMPTZ"
]

boolean_types = [
    "BOOLEAN"
]


def get_enum_normalized_name(enum_name: str) -> str:
    return enum_name.upper()


def get_enum_pascal_name(enum_name: str) -> str:
    return to_pascal_case(enum_name)


def get_is_not_autoincrement_by_type(field_type: str | None):
    if field_type is None or field_type == '':
        return None

    return True if field_type != 'SERIAL' else False


def get_type_orm_type(table_field_type: str, is_enum: bool):
    if table_field_type in string_types:
        return "string"

    if table_field_type in number_types:
        return "number"

    if table_field_type in data_types:
        return "Date"

    if table_field_type in boolean_types:
        return "boolean"

    if is_enum:
        return to_pascal_case(table_field_type)

    raise Exception(f"type {table_field_type} is not supported")


def get_column_definition(table_field_default: str, is_primary: bool, is_not_increment_field: bool):
    if not is_primary:
        return "Column"

    if (table_field_default is None or table_field_default == '') and is_not_increment_field:
        return "PrimaryColumn"

    return "PrimaryGeneratedColumn"


def build_list_modules_from_draw_db_io(path: str):
    with open(path, 'r') as file:
        data = json.load(file)

    list_modules = []

    field_relationships = data["relationships"]
    enums = data["enums"] if "enums" in data else []
    enum_normalized_names = [get_enum_normalized_name(enum["name"]) for enum in enums]

    table_ids_dictionary = {}

    for table in data["tables"]:
        table_id = table["id"]
        table_name = table["name"]
        table_fields = table["fields"]

        table_ids_dictionary[table_id] = {"name": table_name, "field_ids": {}}

        module_dict = {table_name: [
            {
                'name': to_pascal_case(table_name),
                "is_primary_key": False,
                'type': "entity",
                'isEnum': False,
                'column': "Entity",
                'table_name': table_name,
                'foreign_entity': "",
                'fe_property': "",
                'fe_pk_type': "",
                'fe_pk': "",
                'fe_module': "",
                'db_type': "",
                'default_value': "",
                'null': "",
            }
        ]}

        for table_field in table_fields:
            table_field_id = table_field["id"]
            table_field_name = table_field["name"]
            table_field_type = table_field["type"]
            table_field_size = table_field["size"]
            table_field_default = table_field["default"]
            is_primary_field = table_field["primary"]
            is_not_null_field = table_field["notNull"]

            is_not_increment_field_by_type = get_is_not_autoincrement_by_type(table_field_type)
            is_not_increment_field = is_not_increment_field_by_type if is_not_increment_field_by_type is not None \
                else table_field["increment"]

            is_enum = True if table_field_type in enum_normalized_names else False

            orm_type = get_type_orm_type(table_field_type, is_enum)

            table_ids_dictionary[table_id]["field_ids"][table_field_id] = {"name": table_field_name, "type": orm_type}

            if is_primary_field:
                table_ids_dictionary[table_id]["primary"] = table_field_name

            module_dict[table_name].append(
                {
                    'name': table_field_name,
                    "is_primary_key": is_primary_field,
                    'type': orm_type,
                    'isEnum': is_enum,
                    'column': get_column_definition(table_field_default, is_primary_field, is_not_increment_field),
                    'table_name': table_name,
                    'foreign_entity': "",
                    'fe_property': "",
                    'fe_pk_type': "",
                    'fe_pk': "",
                    'fe_module': table_field_type,
                    'db_type': table_field_type if table_field_size == '' else f"{table_field_type}({table_field_size})",
                    'default_value': table_field_default,
                    'null': "x" if not is_not_null_field else "",
                }
            )

        list_modules.append(module_dict)

    for relation in field_relationships:
        cardinality = relation["cardinality"]

        origin_start_table_id = relation["startTableId"]
        origin_start_field_id = relation["startFieldId"]
        origin_end_table_id = relation["endTableId"]
        origin_end_field_id = relation["endFieldId"]

        start_table_id = origin_start_table_id if cardinality == "many_to_one" else origin_end_table_id
        start_field_id = origin_start_field_id if cardinality == "many_to_one" else origin_end_field_id
        end_table_id = origin_end_table_id if cardinality == "many_to_one" else origin_start_table_id
        end_field_id = origin_end_field_id if cardinality == "many_to_one" else origin_start_field_id

        parent_table_dict = table_ids_dictionary[end_table_id]
        child_table_dict = table_ids_dictionary[start_table_id]

        parent_table_name = parent_table_dict["name"]
        child_table_name = child_table_dict["name"]

        child_field_dict = table_ids_dictionary[start_table_id]['field_ids'][start_field_id]
        child_field_name = child_field_dict["name"]

        parent_field_dict = table_ids_dictionary[end_table_id]['field_ids'][end_field_id]
        parent_field_name = parent_field_dict["name"]

        module_idx = find_index_by_key(child_table_name, list_modules)
        if module_idx != -1:
            child_field_idx = find_index('name', child_field_name,list_modules[module_idx][child_table_name])
            if child_field_idx != -1:
                list_modules[module_idx][child_table_name][child_field_idx]["column"] = "foreign"
                list_modules[module_idx][child_table_name][child_field_idx]["foreign_entity"] = to_pascal_case(parent_table_name)
                list_modules[module_idx][child_table_name][child_field_idx]["fe_property"] = f"{child_table_name}_list"
                list_modules[module_idx][child_table_name][child_field_idx]["fe_pk_type"] = parent_field_dict["type"]
                list_modules[module_idx][child_table_name][child_field_idx]["fe_pk"] = parent_field_name
                list_modules[module_idx][child_table_name][child_field_idx]["fe_module"] = parent_table_name
                # print(list_modules[module_idx][child_table_name][child_field_idx])

        module_idx = find_index_by_key(parent_table_name, list_modules)
        if module_idx != -1:
            new_list = list_modules[module_idx][parent_table_name]
            new_list.append(
                {
                    'name': f"{child_table_name}_list",
                    "is_primary_key": False,
                    'type': f"{to_pascal_case(child_table_name)}[]",
                    'isEnum': False,
                    'column': "foreign_ref",
                    'table_name': parent_table_name,
                    'foreign_entity': to_pascal_case(child_table_name),
                    'fe_property': child_field_name,
                    'fe_pk_type': child_field_dict["type"],
                    'fe_pk': child_table_dict["primary"],
                    'fe_module': child_table_name,
                    'db_type': "",
                    'default_value': "",
                    'null': "",
                }
            )
            list_modules[module_idx][parent_table_name] = new_list

    return list_modules, enums
