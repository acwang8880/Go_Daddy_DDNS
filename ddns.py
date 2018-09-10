#!/usr/bin/python3

# TODO: Write config file for filling in options and encrypt that blah blah
# - Maybe make it in YAML?

# Workflow:
# ask what public ip is
# check if it is the same as cached ip
# if different:
#	update cached ip
#	update dns records

# cron job to call this script every 1 hr
# script -> /usr/local/bin
#

import requests
import json
from subprocess import check_output
import smtplib
from email.message import EmailMessage

send_to = "<your email>"

def sendemail(rec_address, subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = "server@<you host machine name>"
    msg['To'] = "<your email>"
    msg.set_content("Public IP changed to: {}".format(body))
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login('<your gmail login>', '<gmail password>')
    s.send_message(msg)
    s.quit()
    
try:
    newIP = check_output(["dig", "+short", "myip.opendns.com", "@resolver3.opendns.com"]).strip().decode("utf-8")
    with open("/path/to/your/ip_cache.txt", "r+") as f:
        oldIP = f.readlines()[0]
        if newIP != oldIP:
            f.seek(0)
            f.write(newIP)
            f.truncate()
            data = [{"type":"A","name":"<host name>","data":newIP,"ttl":3600}]
            headers = {"Content-Type":"application/json", "Authorization": "sso-key <Go Daddy API Key prod>"}
            # make go daddy post to update dns
            r = requests.put("https://api.godaddy.com/v1/domains/<your domain name>/records/A/<host name>", json=data, headers=headers)

            if r.status_code == 200:
                sendemail(send_to, "[SUCCESS] <host name> DNS Change", newIP)
            else:
                sendemail(send_to, "[FAILURE] <host name> DNS Change", newIP)

except Exception as e:
    print("Problem with updating DNS records")
    print(e)
    sendemail(send_to, "[Failure] <host name> Dns change", newIP)
