import os

print(os.getcwd())
#os.chdir('Desktop/python/ittransition/Tango')

input_file_name = input('What is the name of file>>>')
input_string = input('What you wish to store>>>')

with open(f'{input_file_name}.txt', 'w+') as f:
    f.write(input_string)
with open(f'{input_file_name}.txt', 'r+') as f:
    print(f.read())
