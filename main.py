from src.controllers.generate_module_code import generate_module
from dotenv import dotenv_values

config = dotenv_values(".env")

models_path = config["MODELS_PATH"]
file_path = models_path + config["MODELS_FILE"]

db_schema = config["DB_SCHEMA"]

generate_foreign_keys = True if config["GENERATE_FOREIGN_KEYS"] is not None else False


def execute():
    generate_module(models_path, file_path, db_schema, generate_foreign_keys)


if __name__ == '__main__':
    execute()
