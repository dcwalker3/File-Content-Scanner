import PyPDF2 # Reads PDFs
from openpyxl import load_workbook # Loads Excel Workbooks
import textract # Docx and Doc Scanner
import re # Regular Expression

class Scanner:
    def __init__(self, fileList, extensionList, searchTerms, scanForSensitiveData=False):
        self.fileList = fileList
        self.extensionList = extensionList
        self.searchTerms = searchTerms

        if(scanForSensitiveData):
            self.searchTerms.append("\d{3}-\d{2}-\d{4}") # SSN
            self.searchTerms.append("\d{3}-\d{3}-\d{4}") # Phone Number
            self.searchTerms.append("\d{4}-\d{4}-\d{4}-\d{4}") # Credit Card Type 1
            self.searchTerms.append("\d{4}-\d{6}-\d{5}") # Credit Card Type 2

        self.comprimisedFiles = {}

    def scanAppropiateExtension(self):
        for file in self.fileList:
            if(file.endswith(".txt") and ".txt" in self.extensionList):
                self.scanTxt(file)
            elif(file.endswith(".pdf") and ".pdf" in self.extensionList):
                self.scanPDF(file)
            elif(file.endswith(".csv") and ".csv" in self.extensionList):
                self.scanCSV(file)
            elif((file.endswith(".xlsx") and ".xlsx" in self.extensionList) or (file.endswith(".xls") and ".xls" in self.extensionList)):
                self.scanExcel(file)
            elif((file.endswith(".docx") and ".docx" in self.extensionList) or (file.endswith(".doc") and ".doc" in self.extensionList)):
                self.scanDocx(file)
    
    def scanTxt(self, file):
        try:
            with open(file, "r") as text:
                for line in text:
                    for term in self.searchTerms:
                        if self.regexMatch(term, line):
                            self.comprimisedFiles[self.file]["comprimisedText"].append(line)
                            self.comprimisedFiles[self.file]["Terms Matched"].append(term)
        except UnicodeDecodeError:
            print("UnicodeDecodeError: " + file)
        except PermissionError:
            print("Did not have proper permission to scan file: " + file)
        except FileNotFoundError:
            print("File Was Unable to Be Found: " + file)
        except:
            print("Unexpected Error: " + file)
        
    def scanPDF(self, file):
        # Scan PDF files for the search terms.
        # file: The file to scan.
        try:
            with open(file, "rb") as pdf:
                pdfReader = PyPDF2.PdfFileReader(pdf)
                for page in range(pdfReader.numPages):
                    pageObj = pdfReader.getPage(page)
                    text = pageObj.extractText()
                    for term in self.searchTerms:
                        if self.regexMatch(term, text):
                            self.comprimisedFiles[self.file]["comprimisedText"].append(text)
                            self.comprimisedFiles[self.file]["Terms Matched"].append(term)
        except PermissionError:
            print("Did not have proper permission to scan file: " + file)
        except FileNotFoundError:
            print("File Was Unable to Be Found: " + file)
        except:
            print("Unexpected Error: " + file)

    def scanCSV(self, file):
        # Scan CSV files for the search terms.
        # file: The file to scan.
        try:
            with open(file, "r") as csv:
                for line in csv:
                    for term in self.searchTerms:
                        if self.regexMatch(term, line):
                            self.comprimisedFiles[self.file]["comprimisedText"].append(line)
                            self.comprimisedFiles[self.file]["Terms Matched"].append(term)
        except PermissionError:
            print("Did not have proper permission to scan file: " + file)
        except FileNotFoundError:
            print("File Was Unable to Be Found: " + file)
        except:
            print("Unexpected Error: " + file)

    def scanExcel(self, file):
        # Scan .xlsx files for the search terms.
        # file: The file to scan.
        try:
            wb = load_workbook(file)
            for sheet in wb:
                for row in sheet:
                    for cell in row:
                        for term in self.searchTerms:
                            if self.regexMatch(term, cell.value):
                                self.comprimisedFiles[self.file]["comprimisedText"].append(cell.value)
                                self.comprimisedFiles[self.file]["Terms Matched"].append(term)
        except PermissionError:
            print("Did not have proper permission to scan file: " + file)
        except FileNotFoundError:
            print("File Was Unable to Be Found: " + file)
        except:
            print("Unexpected Error: " + file)
    
    def scanDocx(self, file):
        # Scan .docx files for the search terms.
        # file: The file to scan.
        try:
            text = textract.process(file)
            for term in self.searchTerms:
                if self.regexMatch(term, text):
                    self.comprimisedFiles[self.file]["comprimisedText"].append(text)
                    self.comprimisedFiles[self.file]["Terms Matched"].append(term)
        except PermissionError:
            print("Did not have proper permission to scan file: " + file)
        except FileNotFoundError:
            print("File Was Unable to Be Found: " + file)
        except:
            print("Unexpected Error: " + file)
        
            
    def regexMatch(self, pattern, string):
        # Check if the pattern is in the string.
        # pattern: The regex pattern to search for.
        # string: The string to search in.
        return re.search(pattern, string)

