from pathlib import Path
from ocr import ocr_image
import json


def scan_folder(folder_path):
    folder = Path(folder_path)
    supported_extensions = {".png", ".jpg", ".jpeg"}
    index = []

    for file in folder.iterdir():
        if file.suffix.lower() in supported_extensions:
            file_txt = ocr_image(file)
            if file_txt is not None:
                record = {
                    "filename": file.name,
                    "path": str(file),
                    "text": file_txt
                }
                index.append(record)
    return index


def save_index(index):
    with open("index.json", "w") as file:
        json.dump(index, file, indent=4)


def main():
    print("Input folder path: ")
    path_input = input().strip()
    folder_index = scan_folder(path_input)
    save_index(folder_index)
    print(f"{len(folder_index)} screenshots indexed.")


if __name__ == "__main__":
    main()