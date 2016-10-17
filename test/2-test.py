import csv
import os

with open('test.txt') as f:
    reader = csv.reader(f)
    d = list(reader)

mylist = d[0]
mylist.append('?\n')

os.remove('test.txt')

with open("test.txt", "w") as text_file:
    text_file.write(' '.join(mylist))

print 'Modified the file...'
