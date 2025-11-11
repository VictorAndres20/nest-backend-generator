class ReactTSCreateEventGenerator:

    def __init__(self):
        self.imports = ""
        self.content = ""

    def build_additional_imports(self, module_name: str, entity_name: str):
        self.content += "import {\n" +\
                        "  create" + entity_name + ",\n" +\
                        "  edit" + entity_name + ",\n" +\
                        "} from '../../_services/" + module_name + ".service';\n"
        self.content += "import { validate" + entity_name + "DTO } from './model';\n\n"

    def clean(self):
        self.imports = ""
        self.content = ""

    def build_class(self, module_name: str, entity_dict: dict):
        self.build_headers()
        self.build_additional_imports(module_name, entity_dict["name"])
        self.build_class_name(entity_dict)
        self.build_close()
        return self.content

    def build_headers(self):
        self.content += self.imports

    def build_class_name(self, dict_class: dict):
        entity_name = dict_class["name"]
        self.content += "export const create" + entity_name + "Event = async (body) => {\n" + \
                        "  validate" + entity_name + "DTO(body);\n\n" +\
                        "  return await create" + entity_name + "(body);" + \
                        "\n};\n\n"
        self.content += "export const edit" + entity_name + "Event = async (id, body) => {\n" + \
                        "  validate" + entity_name + "DTO(body);\n\n" + \
                        "  return await edit" + entity_name + "(id, body);" + \
                        "\n};\n\n"

    def build_close(self):
        self.content += ""
