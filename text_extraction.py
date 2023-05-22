import re

samples = []

with open('usb_test_nFlattened.dot') as myfile:
    for line in myfile.readlines():
        if re.search(r'octagon', line): 
            if re.search(r'label', line):               
                samples.append(line)

# print('SAMPLES: ', samples)

with open("file2.txt", "w") as myfile2:
    for s in samples:
        myfile2.write(s)