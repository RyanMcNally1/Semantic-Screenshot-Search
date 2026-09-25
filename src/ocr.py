import pytesseract
from PIL import Image

def ocr_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def main():
    print("Input image path:")
    path = input().strip()
    ocr_result = ocr_image(path)
    print("OCR Result: " + ocr_result)


if __name__ == "__main__":
    main()