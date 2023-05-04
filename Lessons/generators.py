import os

def populate_file(filename):
    values_to_write = ['Hello', 'line2','line2','line4']
    with open(filename, "w") as out:
        for value_to_write in values_to_write:
            out.write(value_to_write)
            out.write('\n')


def read_file(filename):
    with open(filename,'r') as in_file:
        for line in in_file:
            yield line


filename = 'sample.txt'
# populate_file('sample.txt')


file_contents = read_file(filename)

print(file_contents)

for line in file_contents:
    print(line)


file_contents = (line for line in open(filename, 'r'))

print(file_contents)

print(next(file_contents))