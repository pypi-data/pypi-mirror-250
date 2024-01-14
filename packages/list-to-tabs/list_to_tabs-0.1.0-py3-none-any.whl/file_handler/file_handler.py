from pathlib import Path
from dataclasses import dataclass
import tempfile

class FileHandler():
    def __init__():
        pass

    def file_to_dict(file_path: Path)->dict():
        temp_dict = dict()
        with open(file_path, "r") as file:
            for line_num, line_content in enumerate(file):
                temp_dict[line_num] = str(line_content).strip()
        return temp_dict
    
    def create_new_file(file_path: Path)->Path:
        if (not file_path.exists and not file_path.is_dir()):
            open(file_path, 'a')
        else:
            pass
        return Path("/home/simsjo-a/")#TODO: make this into a recursive function so that if filename exists, subfix w/ num
        

    def insert_into_file(file_path: Path, insert_text: str):
        with open(file_path, "a") as file:
            file.write(insert_text)

    def text_transform(insert_text: str, insert_command: str)->str:
        return f"title: {insert_text};; command: {insert_command} {insert_text}\n"

    # def get_subdirs(file_path: Path):
    #     list_of_dirs = [x for x in file_path.iterdir() if x.is_dir()]
    #     print(list_of_dirs)


def check_if_file(file_path: Path)->bool:
    return file_path.exists and not file_path.is_dir()


def print_contents(file_path: Path):
    with open(file_path) as file:
        for line_num, line_content in enumerate(file):
            print(line_num, line_content)




