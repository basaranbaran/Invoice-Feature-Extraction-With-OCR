import os
import cv2
import pytesseract
import numpy as np
import time
from PIL import Image
from pytesseract import Output

# Tesseract ayarlari
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"

# 1. DPI arttirma (optimize)
def set_image_dpi(img, scale_factor=2):  # 6 -> 2 olarak dusuruldu
    height, width = img.shape[:2]
    new_height = int(height * scale_factor)
    new_width = int(width * scale_factor)
    return cv2.resize(img, (new_width, new_height))

# 2. Guvenli Normalizasyon
def normalize_image(img):
    if img is None or img.size == 0:
        raise ValueError("normalize_image: Gorsel yuklene medi veya bozuk.")
    norm_img = np.zeros(img.shape, np.uint8)
    return cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)

# 3. Gurultu azaltma
def remove_noise(img):
    return cv2.fastNlMeansDenoisingColored(img, None, 3, 3, 7, 15)

# 4. Gri tonlama
def get_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 5. Threshold
def thresholding(img):
    return cv2.threshold(img, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Preprocessing pipeline
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Gorsel okunamadi veya bozuk: {image_path}")

    img = set_image_dpi(img)
    img = normalize_image(img)
    img = remove_noise(img)
    img = get_grayscale(img)
    img = thresholding(img)

    temp_path = "temp_preprocessed.png"
    cv2.imwrite(temp_path, img)
    return temp_path

# OCR islemi
def ocr_yap(image_path, dil="tur+eng"):
    try:
        start = time.time()
        print("[OCR] OCR islemi basladi...")

        preprocessed_path = preprocess_image(image_path)
        img = cv2.imread(preprocessed_path)
        if img is None:
            raise ValueError(f"On islenmis gorsel okunamadi: {preprocessed_path}")

        config = r"--oem 3 --psm 6"  # Daha kararli
        raw_text = pytesseract.image_to_string(img, lang=dil, config=config)

        if os.path.exists(preprocessed_path):
            os.remove(preprocessed_path)

        print(f"[OCR] OCR tamamlandi. Sure: {round(time.time() - start, 2)} saniye")
        return raw_text.strip()
    except Exception as e:
        print(f"[ERROR] OCR HATASI: {e}")
        return ""

# Test modu
if __name__ == "__main__":
    path = "ornek_fatura.png"
    sonuc = ocr_yap(path)
    print("\n[OCR] OCR Sonucu:\n" + "="*40)
    print(sonuc)
    print("="*40)
