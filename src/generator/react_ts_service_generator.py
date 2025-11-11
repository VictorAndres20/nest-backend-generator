REACT_TS_SERVICE_BASE_IMPORTS = "import {\n  handleFetch,\n  GET_OPTIONS,\n  POST_OPTIONS,\n  PUT_OPTIONS\n} " \
                       "from './_commons/base.service';\n\n"


class ReactTSServiceGenerator:

    def __init__(self):
        self.imports = REACT_TS_SERVICE_BASE_IMPORTS
        self.content = ""

    def build_additional_imports(self, module_name: str, entity_name: str):
        pass

    def clean(self):
        self.imports = REACT_TS_SERVICE_BASE_IMPORTS
        self.content = ""

    def build_class(self, module_name: str, entity_dict: dict, pk_dict: dict):
        self.build_headers()
        self.build_class_name(module_name, entity_dict, pk_dict)
        self.build_close()
        return self.content

    def build_headers(self):
        self.content += self.imports
        self.content += "\n"

    def build_class_name(self, module_name: str, dict_class: dict, pk_dict: dict):
        endpoint = module_name.replace("_", "-")
        self.content += "const BASE_PATH = '/" + endpoint + "';\n\n"
        self.content += "export const findAll" + dict_class["name"] + " = async () => {\n" + \
                        "  return await handleFetch(`${BASE_PATH}/all`, GET_OPTIONS);" + \
                        "\n};\n\n"
        self.content += "export const find" + dict_class["name"] + "ById = async (id: string) => {\n" + \
                        "  return await handleFetch(`${BASE_PATH}/id/${id}`, GET_OPTIONS);" + \
                        "\n};\n\n"
        self.content += "export const create" + dict_class["name"] + " = async (body) => {\n" + \
                        "  return await handleFetch(`${BASE_PATH}/create`, POST_OPTIONS, body);" + \
                        "\n};\n\n"
        self.content += "export const edit" + dict_class["name"] + " = async (id, body) => {\n" + \
                        "  return await handleFetch(`${BASE_PATH}/edit/${id}`, PUT_OPTIONS, body);" + \
                        "\n};\n\n"
        self.content += "export const findAll" + dict_class["name"] + "Paged = async (page, limit) => {\n" + \
                        "  return await handleFetch(`${BASE_PATH}/all-paged/${page}/${limit}`, GET_OPTIONS);" + \
                        "\n};\n\n"

    def build_close(self):
        self.content += ""
