import os
import time
import ScrapContent
import unicodedata
from docx2pdf import convert as conv
from datetime import date
from docxtpl import DocxTemplate
import textPreProcessesion as TP
from plagCheck import Plagiarism_Detector as Plag
from convert import pdf_to_txt, png_to_txt, word_to_txt


def read_files(path):
    # get a list of all the files in the directory
    files = os.listdir(path)
    file_content = ''
    # iterate over each file in the directory
    for file in files:
        # check if the file is a file (not a directory)
        if os.path.isfile(os.path.join(path, file)):
            # read the contents of the file
            if file.endswith('.docx'):
                print('d')
                file_content += word_to_txt(path+file)
                file_content = unicodedata.normalize('NFKD', file_content)
            elif file.endswith('.pdf'):
                print('d1')
                file_content += pdf_to_txt(path+file)
            elif file.endswith('.jpg') or file.endswith('.png') or file.endswith('jpeg') or file.endswith('.bmp'):
                print('d2')
                file_content += png_to_txt(path+file)
    file_content = ' '.join(file_content.split())
    print(file_content)
    return file_content


def drive(suspiciousDoc):
    # print(suspiciousDoc)
    fileContents = []
    fileContents.append(TP.preprpcess(suspiciousDoc).lower())

    result_links = ScrapContent.get_urls(suspiciousDoc)
    if result_links[0] == 'This search query yielded No matching results':
        print('The document is unique since it has no matching results online so there is no act of plagiarism.')
        return {"data": "This document is Unique"}

    print(result_links)
    print('\n\n')

    link_contents = ScrapContent.get_content(result_links)

    # print(link_contents)

    for text in link_contents:
        # fileContents.append(TP.preprpcess(text))
        if len(text) == 0:
            continue
        else:
            string = TP.string_matching(TP.preprpcess(
                suspiciousDoc), TP.preprpcess(text))
            if string == 'no match':
                print(string)
                print('\n\n')
            else:
                print(string)
                print('\n\n')
            fileContents.append(string)

    res_count = len(fileContents) - 1

    files = ['local']
    for i in result_links:
        files.append(i)

    p = Plag()
    # print(files)

    # print(p.check_plagiarize(fileContents, files))
    results = p.check_plagiarize(fileContents, files)
    finalRes = []
    # print(results)
    for res in results:
        if res[1] == 'local':
            # print(res)
            finalRes.append(res)
    # print(finalRes)
    dict_data = []
    for tup in finalRes:
        dict_data.append({'source': tup[0], 'match': tup[2]})

    return dict_data


def clean_folder(folder_path):
    try:
        # Check if the folder exists
        if not os.path.exists(folder_path):
            raise FileNotFoundError("Folder not found")

        # Iterate over all files in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # Check if the path is a file
            if os.path.isfile(file_path):
                # Delete the file
                os.remove(file_path)
                print(f"Deleted file: {file_path}")

        print("All files in the folder deleted successfully")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


def generate_report(results):
    REPORT_SAVE_LOCATION = 'D:/Final Year project/x/project/Plagiarism_Reports/'
    path = 'D:/Final Year project/x/project/templates/report_template.docx'
    path1 = 'D:/Final Year project/x/project/templates/report_template1.docx'
    # Load the template file
    doc = DocxTemplate(path)

    maxk = ''
    maxv = 0
    for i in results:
        # print(i)
        if i['match'] > maxv:
            maxv = i['match']
            maxk = i['source']

    # Create a context dictionary to hold the data
    context = {
        'plag_index': maxv,
        'plag_source': maxk,
        'Current_Date': date.today(),
        'rows': results
    }
    # Fill in the table in the template with the data
    doc.render(context)

    # Save the filled-in document to a new file
    doc.save(path1)

    temp_pdf = 'filled_template.pdf'
    conv(path1, temp_pdf)

    # Remove the temporary .docx file
    os.remove(path1)

    # Generating the name for the report file
    fileName = REPORT_SAVE_LOCATION+('_'.join(('report ' + time.ctime() + '.pdf').split())
                                     ).replace(':', '-')
    # Rename the PDF file to the desired name
    os.rename(temp_pdf, fileName)
