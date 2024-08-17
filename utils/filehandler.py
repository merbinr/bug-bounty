import os



def create_dir(path: str):
    os.makedirs(path, exist_ok=True)



def write_lines_to_file(data: list[str], path:str):
    with open(path, "w") as f:
        f.write("\n".join(data))
    
