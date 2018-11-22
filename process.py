import os

# This is just a quick and dirty script. Does it's job for now but requires a lot of clean up

if os.path.isfile('meta'):
    with open('meta', 'r') as meta:
        index = int(meta.read())
else:
    index = 0

if not os.path.isdir('img'):
    os.mkdir('img')

for file in os.listdir('.'):
    if file.endswith('.jpg') or file.endswith('.jpeg'):
        os.rename(file, "img/" + str(index) + ".jpg")
        index += 1

with open('meta', 'w+') as meta:
    meta.write(str(index))

