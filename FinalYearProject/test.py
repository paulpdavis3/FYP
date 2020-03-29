import re

txt = "paul@gmail.com"
x = re.search("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", txt)

if(x):
    print("yup")
else:
    print("shart")
