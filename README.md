# Go_Daddy_DDNS
Python Dynamic DNS for Machines Hosted on Go Daddy

Make this run as often as you'd like by making it a cron job.

```
crontab -e

# In your crontab file:
MAILTO=<youremail>
5 0 * * * /usr/local/bin/ddns.py
5 11 * * * /usr/local/bin/ddns.py
```
