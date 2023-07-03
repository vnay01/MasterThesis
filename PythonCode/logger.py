import sys
import os 
class Logger:
 
    def __init__(self, filename):
        self.console = sys.stdout
        file=self.create_file_if_not_exists(filename)
        self.file = open(file, 'w')
 
    def write(self, message):
        self.console.write(message)
        self.file.write(message)
 
    def flush(self):
        self.console.flush()
        self.file.flush()
    
    def create_file_if_not_exists(file_name):
        if not os.path.exists(file_name):
            with open(file_name,'w') as file:
                print(f"Created file: (file_path)")
        else:
            print(f"File already exists: (file_path)")
 
path = os.getcwd()
sys.stdout = Logger(path)
print('Hello, World')