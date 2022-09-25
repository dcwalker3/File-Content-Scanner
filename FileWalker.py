import os

class FileWalker():
    def __init__(self, dirPath):
        self.dirPath = dirPath
        self.fileList = []
        self.dirList = []
        self.fileStructure = []

        self.walk()

    def walk(self):
        for root, dirs, files in os.walk(self.dirPath):
            for name in files:
                filePath = os.path.join(root, name).replace("\\", "/")
                self.fileList.append(filePath)
                self.fileStructure.append(filePath)
            for name in dirs:
                dirPath = os.path.join(root, name).replace("\\", "/")
                self.dirList.append(dirPath)
                self.fileStructure.append(dirPath)
    
    def printPrettyFileStructure(self, path, level=0):
        # Print the file structure in a pretty way.
        # path: The path to the directory to print.
        # level: The level of the directory in the file structure.
        #        0 is the root directory.
        #        1 is the first level of subdirectories.
        #        2 is the second level of subdirectories.
        #        etc.
        for root, dirs, files in os.walk(path):
            print("\t" * level + os.path.basename(root) + "/")
            subLevel = level + 1
            for f in files:
                print("\t" * subLevel + f)
            for d in dirs:
                self.printPrettyFileStructure(os.path.join(root, d), subLevel)

    
    