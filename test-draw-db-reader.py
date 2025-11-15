import os
from src.helpers.drawdb_reader import build_list_modules_from_draw_db_io
from dotenv import dotenv_values

config = dotenv_values(".env")

model_file_path = config["MODELS_INPUT_PATH"]
model_file_name = config["MODELS_FILE_NAME"]

if __name__ == '__main__':
    list_modules2 = build_list_modules_from_draw_db_io(os.path.join(model_file_path, model_file_name))
    print(list_modules2)