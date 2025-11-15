from src.controllers.generate_module_code import generate_module
from dotenv import dotenv_values
import os

config = dotenv_values(".env")

models_path = config["MODELS_OUTPUT_PATH"]
model_file_path = config["MODELS_INPUT_PATH"]
model_file_name = config["MODELS_FILE_NAME"]

db_schema = config["DB_SCHEMA"]
db_schema = db_schema.strip().lower() if db_schema is not None and db_schema != '' else None

generate_foreign_keys = True if config["GENERATE_FOREIGN_KEYS"] is not None else False


def execute():
    generate_module(models_path, os.path.join(model_file_path, model_file_name), db_schema, generate_foreign_keys)


if __name__ == '__main__':
    execute()
