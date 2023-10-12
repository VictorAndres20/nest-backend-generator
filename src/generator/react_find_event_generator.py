class ReactFindEventGenerator:

    def __init__(self):
        self.imports = ""
        self.content = ""

    def build_additional_imports(self, module_name: str, entity_name: str):
        self.content += "import {\n" +\
                        "    findAll" + entity_name + ",\n" +\
                        "    find" + entity_name + "ById,\n" +\
                        "    findAll" + entity_name + "Paged,\n" +\
                        "} from '../../_services/" + module_name + ".service';\n\n"

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
        self.content += "export const findAll" + entity_name + "Event = async () => {\n" + \
                        "    return await findAll" + entity_name + "();" + \
                        "\n}\n\n"
        self.content += "export const find" + dict_class["name"] + "ByIdEvent = async (id) => {\n" + \
                        "    return await find" + entity_name + "ById(id);" + \
                        "\n}\n\n"
        self.content += "export const findAll" + dict_class["name"] + "PagedEvent = async (page, limit = 8) => {\n" + \
                        "    return await findAll" + entity_name + "Paged(page, limit);" + \
                        "\n}\n\n"

    def build_close(self):
        self.content += ""
