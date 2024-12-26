import pytesseract
from PIL import Image
import cv2

def extract_text_from_image(image_path):
    return pytesseract.image_to_string(Image.open(image_path))

def preprocess_image(image_path):
    img = cv2.imread(image_path, 0)
    _, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return img_bin
