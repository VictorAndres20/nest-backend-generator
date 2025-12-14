import os

from src.controllers.clean_generated_modules import clean_generated_modules
from src.controllers.generate_module_code import generate_module
from dotenv import dotenv_values

config = dotenv_values(".env")

models_path = config["MODELS_OUTPUT_PATH"]
model_file_path = config["MODELS_INPUT_PATH"]
model_file_name = config["MODELS_FILE_NAME"]

db_schema = config["DB_SCHEMA"] if "DB_SCHEMA" in config.keys() else None
db_schema = db_schema.strip().lower() if db_schema is not None and db_schema != '' else None

generate_foreign_keys = config["GENERATE_FOREIGN_KEYS"] if "GENERATE_FOREIGN_KEYS" in config.keys() else None
generate_foreign_keys = True if config["GENERATE_FOREIGN_KEYS"] is not None else False

log_model_loaded = config["LOG_MODEL_LOADED"] if "LOG_MODEL_LOADED" in config.keys() else None
log_model_loaded = True if log_model_loaded is not None and log_model_loaded != '' else False


def execute():
    clean_generated_modules(models_path)
    generate_module(models_path, os.path.join(model_file_path, model_file_name), db_schema, generate_foreign_keys, log_model_loaded)


if __name__ == '__main__':
    execute()
