import os
import time
import subprocess

#print values into the console
def disp(value):
    print(value)


#shutdown operations with time
def shutdownt(time):
    os.system(f'shutdown /s /t {time}')
def restartt(time):
    os.system(f'shutdown /r /t {time}')
#shutdown operations without time
def shutdown():
    os.system(f'shutdown /s /t 0')
def restart():
    os.system(f'shutdown /r /t 0')
#forced shutdown operations with time
def fshutdownt(time):
    os.system(f'shutdown /s /f /t {time}')
def frestartt(time):
    os.system(f'shutdown /r /f /t {time}')
#forced shutdown operations without time
def fshutdown():
    os.system(f'shutdown /s /f /t 0')
def frestart():
    os.system(f'shutdown /r /f /t 0')

#delete files
def delete(file_name):
    os.remove(f'{file_name}')
#rename files
def rename(old_file_name, new_file_name):
    os.rename(old_file_name, new_file_name)

#scan and print text files
def scan(file_name):
    try:
        start_time = time.time()
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(content)
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(f"Search took {elapsed_time:.5f} seconds")
    except FileNotFoundError:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Search took {elapsed_time:.5f} seconds")
        print("Error: The file could not be found.")
        print("Consider the following debugs:")
        print("  - Check the file path.")
        print("  - Ensure all slashes are forward slashes, not backslashes.")
        print("  - It must be a text file.")
        print(f'  - File name: {file_name}')



#open command prompt
def cmd():
    subprocess.run(["cmd", "/c", "start cmd.exe"])

#run a command in command prompt
def cmdrun(code_to_execute):
    subprocess.run(["cmd", "/c", f"{code_to_execute}"])


#