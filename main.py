from src.controllers.generate_module_code import generate_module
from dotenv import dotenv_values

config = dotenv_values(".env")

models_path = config["MODELS_PATH"]
excel_path = models_path + config["MODELS_FILE"]

# db_schema = None
db_schema = 'ks'
generate_foreign_keys = True


def execute():
    generate_module(models_path, excel_path, db_schema, generate_foreign_keys)


if __name__ == '__main__':
    execute()
