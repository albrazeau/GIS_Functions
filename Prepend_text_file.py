```
# To add line to the top of a txt file
# Used to add the json header
# Args are the file you are writing to, the string you are prepending to the top

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)
        f.close()
```
