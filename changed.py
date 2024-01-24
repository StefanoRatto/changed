#!/usr/bin/env python3

__author__ = "raste"
__version__ = "0.1.0"
__org__ = "team7"

import argparse
import hashlib
import os
import time
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from urllib.request import urlopen, Request

def main(args):

    sender_email = "@gmail.com"
    receiver_email = "@gmail.com"
    password = "aaaa bbbb cccc dddd"

    print(f"[{datetime.now().astimezone().isoformat()}] Running with PID {os.getpid()}, Ctrl-C to exit.")

    data = {}

    with open(args.targets_file) as tfile:
        
        for line in tfile:
            target = line.rstrip("\n")

            try:
                url = Request(target, headers={'User-Agent': 'Mozilla/5.0'})
                response = urlopen(url).read()
                currentHash = hashlib.sha224(response).hexdigest()
                data[target] = currentHash
            except Exception as e:
                print(f"[{datetime.now().astimezone().isoformat()}] [PID:{os.getpid()}] [{target}] {e}, SKIPPING...")

    while True:
        
        time.sleep(300)
        
        for target, currentHash in data.items():

            url = Request(target, headers={'User-Agent': 'Mozilla/5.0'})

            try:
                response = urlopen(url).read()
                newHash = hashlib.sha224(response).hexdigest()

                if newHash == currentHash:
                    print(f"[{datetime.now().astimezone().isoformat()}] [PID:{os.getpid()}] [{target}] Not changed...")
                    continue

                else:
                    print(f"[{datetime.now().astimezone().isoformat()}] [PID:{os.getpid()}] [{target}] Has CHANGED!")
                    
                    try:
                        body= f"[{datetime.now().astimezone().isoformat()}] [PID:{os.getpid()}] [{target}] has CHANGED!"
                        message = MIMEText(f"{body} Please check it out...", 'plain')
                        message['From'] = "@gmail.com"
                        message['To'] = "@gmail.com"
                        message['Subject'] = body
                        server = smtplib.SMTP('smtp.gmail.com', 587) 
                        server.starttls()
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, message.as_string())
                    except Exception as e:
                        print(f"[{datetime.now().astimezone().isoformat()}] [PID:{os.getpid()}] [{target}] {e}")
                    finally:
                        server.quit()

                data[target] = newHash

            except Exception as e:
                print(f"[{datetime.now().astimezone().isoformat()}] [PID:{os.getpid()}] [{target}] {e}")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", dest="targets_file", required=True)

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    args = parser.parse_args()

    main(args)
