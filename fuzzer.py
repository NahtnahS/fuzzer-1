#!/usr/bin/python

# 5-line fuzzer below is from Charlie Miller's
# "Babysitting an Army of Monkeys":
# Part 1 - http://www.youtube.com/watch?v=Xnwodi2CBws
# Part 2 - http://www.youtube.com/watch?v=lK5fgCvS2N

# List of files to use as initial seed
file_list=[
    "pdf_files_samples\cert_DD.pdf",
    "pdf_files_samples\LEA_certifikat.pdf",
    "pdf_files_samples\ST115_iCOM_Logging_Instructions.pdf",
    "pdf_files_samples\ST015.x_iCOM_SDK_CApCom_rev5.pdf"
    ]

# List of applications to test (vymazal som jednu dalsiu, pouzivam iba jednu a upravil som to dalej v kode)
apps = [
    "\Program Files\Foxit Software\Foxit Reader\FoxitReader.exe"
    ]

fuzz_output = "fuzz.pdf"

FuzzFactor = 244
num_tests = 10000

########### end configuration ##########

import math
import random
import string
import subprocess
import time

for i in range(num_tests):
    file_choice = random.choice(file_list)
    #app = random.choice(apps)

    buf = bytearray(open(file_choice, 'r+b').read())

    # start Charlie Miller code
    numwrites=random.randrange(math.ceil((float(len(buf)) / FuzzFactor)))+1

    for j in range(numwrites):
        rbyte = random.randrange(256)
        rn = random.randrange(len(buf))
        buf[rn] = "%c"%(rbyte)
    #end Charlie Miller code

    open(fuzz_output, 'w+b').write(buf)

    process = subprocess.Popen([apps, fuzz_output])

    time.sleep(1)
    crashed = process.poll()
    if not crashed:
        process.terminate()