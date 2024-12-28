from driver import *
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Form, UploadFile, File

app = FastAPI()
templates = Jinja2Templates(directory="templates")
# Mount the static folder to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit")
async def submit(request: Request, input_type: str = Form(...), input: str = Form(None), file: UploadFile = File(None)):
    path = 'D:/Final Year project/x/project/UPF/'
    print(input_type)
    if input_type == "text":
        # Process text input
        suspiciousDoc = input
    elif input_type == "file":
        # Process file input
        file_name = file.filename
        contents = await file.read()

        print('file has been read')

        # Write the uploaded file's content into a local file
        with open(path+file_name, 'wb') as outfile:
            outfile.write(contents)

        suspiciousDoc = read_files(path)
    # Delete the file after extracting the text from it
    clean_folder(path)

    # Compute the Plagiarims results
    json_data = drive(suspiciousDoc)

    # Test the whether the results have been obtained or not
    for item in json_data:
        print(item)

    generate_report(json_data)

    return templates.TemplateResponse("results.html", {"request": request, "json_data": json_data})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
