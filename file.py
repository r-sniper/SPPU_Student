import getpass
import os

if getpass.getuser() == 'rsniper':
    # return HttpResponse("Please don't use this URL just yet")
    print("hi")
osdir = os.walk('codes/')
added_subjects = []
added_programs = []
every_directory = set((), )
for root, dirs, files in osdir:
    if root.count('/') == 3 and files:
        # print(root)
        # print(files)
        line = root.split('/')
        for f in files:
            temp = (line[1], line[2], line[3], f)
            every_directory.add(temp)
            print(temp)
