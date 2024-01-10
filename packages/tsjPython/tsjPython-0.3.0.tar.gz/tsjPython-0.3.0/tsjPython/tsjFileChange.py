from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove
import re

# https://stackoverflow.com/questions/39086/search-and-replace-a-line-in-a-file-in-python
def replaceOneLine(file_path, pattern, subst):
    #Create temp file
    # ic(subst)
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                # new_file.write(line.replace(pattern, subst))
                if re.match(pattern,line):
                    new_file.write(subst)
                else:
                    new_file.write(line)
    #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)
    
def addOneLine(file_path, add_line):
    with open(file_path, 'a') as f:
        f.write(add_line)
        
def oneString2file(file_path, one_string):
    with open(file_path,"w") as f:
        f.writelines(one_string)
        
def file2oneString(file_path):
    with open(file_path,"r") as f:
        return f.readlines()
        
def regexHeadNLine(file_path, pattern, line_number_limit):
    ic(f"regexHeadNLine {file_path} finding...")
    with open(file_path,"r") as f:
        i = 0
        while i < line_number_limit:
            line = f.readline()
            regex_result = re.match(pattern, line)
            if regex_result:
                return regex_result
            i+=1
    ic(f"file {file_path} failed to find a match of {pattern} before {line_number_limit} lines")
    return None

def regexPattern(file_path, pattern):
    ic(f"regexPattern {file_path} finding...")
    with open(file_path,"r") as f:
        line = f.readline()
        while line:
            regex_result = re.match(pattern, line)
            if regex_result:
                return regex_result
            line = f.readline()
    ic(f"file {file_path} failed to find a match of {pattern}!")
    return None

def regexPatternList(file_path, pattern):
    ic(f"regexPattern {file_path} finding...")
    result_list = []
    with open(file_path,"r") as f:
        line = f.readline()
        while line:
            regex_result = re.match(pattern, line)
            if regex_result:
                result_list.append(regex_result)
            line = f.readline()
    ic(f"file {file_path} failed to find a match of {pattern}!")
    return result_list

def getLineNumberOfFile(file_path):
    with open(file_path, 'r') as file:
        line_count = len(file.readlines())

    # print(f"Number of lines in the file: {line_count}")
    return line_count
