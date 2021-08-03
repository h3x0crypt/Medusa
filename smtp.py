#!/usr/local/bin/python3

'''
-------------------------------------------------------------------------------
PROJECT:    Medusa Mail Access checker
AUTHOR:     h3x0crypt @ GitHub.com

-------------------------------------------------------------------------------
INFO:       SMTP checker / SMTP cracker for mailpass combolists 
            You are only allowed to use the following code for educational
            purposes!

'''

# Python modules

import os, sys, smtplib, ssl, socket, time, math, signal
from multiprocessing import Pool
from multiprocessing import freeze_support
from email.mime.text import MIMEText
from email.header import Header
from numpy import random

# Colors

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def quit(signum, frame):
    print('\n\nExiting ... Bye!')
    sys.exit(0)

if __name__ == "__main__":
    ## SIGINT Terminate process Interrupt process
    signal.signal(signal.SIGINT, quit)

#banner

def banner():

    print(f"""{bcolors.HEADER}
    _  _ ____ ___  _  _ ____ ____ 
    |\/| |___ |  \ |  | [__  |__| 
    |  | |___ |__/ |__| ___] |  | 
                              
        project: Mail Access checker
        Author : h3x0
        Github : https://github.com/h3x0crypt
    """)

#Reading combo file

def readFile(filename):

    if(os.path.isfile(str(filename)) == True):
        content = open(filename, 'r').read()
        return True, content
    else:
        return False, None

#Args List

def Argv():
    global ListFile
    global UseMulti
    global Threads
    global OutputFile

    OutputFile = str(input('List File : '))

    while True:
        try:
            UseMulti = str(input('Use MultiProcessing (y/n) ? :'))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if UseMulti == 'y':
            try:
                Threads = int(input('Number of threads : '))
            except ValueError:
                print("Sorry, I didn't understand that.")
                continue
            break
        elif UseMulti == 'n':
            Threads = None
        else:
            print("Sorry, your response must be (y/n).")
            continue

    OutputFile = str(input('Output File : '))

banner()
Argv()




