
# Plagiarism Detector (Plago)

A brief description of what this project does and who it's for

# Steps to Setup the project.


### Software/IDE for setting up the project

Visual Studio Code ( Preferred ), PyCharm, Sublime Text.

### Step - 1

Extract the zip file present in the CD disk in D drive inside a folder by name "Final Year project".

### Step - 2

* Open the folder inside the IDE.
* Create a virtual environment using virtual environment a python package. 
* Install virtual environment using the commmand "pip install virtualenv"

### Step - 3

Create a virtual environment by typing the command inside the terminal.

### Step - 4

Run the command inside the terminal "pip install -r requirements. txt" to install the all the packages required for the project.

### Step - 5
run the commands in the terminal to launch the web app;

### Activate the virtual environment
".\fastPlagEnv\Scripts\activate"

### move to "project" folder
"cd project"

### launch web app
"uvicorn main:app --reload"

# Input 

Step - 1: Chooose the type of input from the selector (File/Text).
Step - 2: After selecting the input type, 
if input type is "Text" copy paste the content to checked for Plagiarism inside the Textarea provided.
if input type is "File" select the file from the file selector pop-up.
Step - 3: Press the Check Plagiarism button given.

### Output
After the input is evaulated for Plagiarism, results are obtained and shown in a table.
The user is given a choice to download the Plagiarism Report.


# Conditions on input

* Input if its is Text pasted into the Textarea it must be atleast 3 characters without stop words. 