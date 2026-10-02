import pytesseract
from PIL import Image, UnidentifiedImageError

def ocr_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        if not text.strip():
            return "No text found in the image."
        return text
    
    except FileNotFoundError:
        return "Error: Image file not found."
    
    except UnidentifiedImageError:
        return "Error: File is not a valid image."

    except Exception as e:
        return f"Error while performing OCR: {e}"

def main():
    print("Input image path:")
    path = input().strip()
    ocr_result = ocr_image(path)
    print("OCR Result: " + ocr_result)


if __name__ == "__main__":
    main()