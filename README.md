# RPAL_Project

## Introduction

This project is an implementation of an interpreter for the RPAL (Right-reference Programming Algorithmic Language) language. It was developed as part of the CS3513 - Programming Languages course by Anuja Kalhara and Pulindu Ranaweera.

## How to Run

1. **Clone or Download the Repository**
   - Ensure all project files are in a single directory.

2. **Compile the project to an exe and run *(Step 4)* or directly run the python interpriter *(Step 5)***

3. **Use already built .exe**
   - Open a terminal in the project directory.
     ```
     .\RPALProject.exe <switches -ast -st or none> <filepath>
     ```

2. **Compile the Project**
   - Open a terminal in the project directory.
   - Compile the source code using make compiler:
     ```
     make env
     ```
     or create python enviornment and activate it

     ```
     make install
     ```
     or install pyinstaller

     ```
     make build
     ```
     same can be achieved by running below command.
     **You do not need to run below command if you have already run make build.**
     ```
     python -m PyInstaller --onefile --name RPALProject myrpal.py
     ```

   - Run make help to see commands
     ```
     make help
     ```
   - .exe file will be inside dist
     ```
     .\dist\RPALProject.exe <switches -ast -st or none> <filepath>
     ```

3. **Run the Interpreter**
   - Open a terminal in the project directory.
   - Execute the myrpal.py class :
     ```
     python .\myrpal.py <switches -ast -st or none> <filepath>
     ```
   - `<filepath>` should be a text file containing valid RPAL code.

## Project Structure

- Source files are located in the root directory.
- Input RPAL programs should be provided as text files.

## Notes

- Ensure you have Python installed
- For any issues or questions, please contact the authors.
