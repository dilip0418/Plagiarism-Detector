from pdfminer.high_level import extract_text
import docx2txt
from PIL import Image
from pytesseract import pytesseract
import requests
import textPreProcessesion as TP


def word_to_txt(file):
    try:
        text = docx2txt.process(file)
        print(' '.join(text.split()))
        return (text)
        # print(result)

    except:
        return ''


def pdf_to_txt(file):
    try:
        text = extract_text(file)
        # print("pdf\n", ' '.join(text.split()))
        return (text)
    except:
        return ''


def png_to_txt(file):
    try:
        # Defining the path to the tesseract exe file
        path_to_tesseract = r"D:\Final Year project\Tesseract-OCR\tesseract.exe"

        # Define path to image
        path_to_image = file

        # Point tessaract_cmd to tessaract.exe
        pytesseract.tesseract_cmd = path_to_tesseract

        # Open image with PIL
        img = Image.open(path_to_image)

        # Extract text from Image
        text = pytesseract.image_to_string(img)

        print('Img\n', ' '.join(text.split()))
        return (text)
    except:
        return ''


def download_pdf(url, file_name):
    try:
        # Send GET request
        response = requests.get(url)
        pdf_text = ''
        # Save the PDF
        if response.status_code == 200:
            with open(file_name, "wb") as f:
                f.write(response.content)
                pdf_text = pdf_to_txt(file_name)
        return pdf_text
    except:
        return ''
