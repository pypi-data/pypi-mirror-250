#!/usr/bin/python3

from file_handler import file_handler
from pathlib import Path

src_path = Path("/home/simsjo-a")
src_file = src_path/"server.list"

des_path = Path("/home/simsjo-a/tabs")
des_file = des_path/"batch"

default_batch_size = 6

# print(list(src_path.glob("**/*")))

if __name__ == "__main__":

    file_obj = file_handler.FileHandler
    file_dict = file_obj.file_to_dict(src_file)
    
    print(file_dict.values())
    print(len(file_dict))

    default_batch_size = len(file_dict)

    file_dict = {host: file_obj.text_transform(file_dict[host], "ssh") for host in file_dict}

    for item in file_dict.values():
        file_obj.insert_into_file(des_file, item)

    for item in file_dict.items():
        print(item)
    # TODO: need to check this prior to appending to file so that it can be incremented 
    # print(file_handler.check_if_file(des_file))