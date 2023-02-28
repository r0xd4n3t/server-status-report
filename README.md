<a id="top"></a>

#

<h1 align="center">
Server Status Report
</h1>

<p align="center"> 
  <kbd>
<img src="https://raw.githubusercontent.com/r0xd4n3t/server-status-report/main/img/report.png"></img>
  </kbd>
</p>

<p align="center">
<img src="https://img.shields.io/github/last-commit/r0xd4n3t/server-status-report?style=flat">
<img src="https://img.shields.io/github/stars/r0xd4n3t/server-status-report?color=brightgreen">
<img src="https://img.shields.io/github/forks/r0xd4n3t/server-status-report?color=brightgreen">
</p>

# 📜 Introduction

This code is a Python script that gathers information about a server's status and sends it in an email report. The report contains information such as the server's hostname, CPU usage, memory usage, disk usage, network I/O counters, uptime, currently running processes, and system logs.

To use this script, you need to have the following Python modules installed:

-   psutil: for getting information about system utilization (CPU, memory, disks, network)
-   smtplib: for sending emails
-   email.mime: for creating email messages
-   humanfriendly: for formatting data sizes in a human-readable format

The script also uses subprocess to execute some shell commands and get their output.

## 📝 Modify the following variables:

To use the script, you need to modify the following variables in the code:

-   EMAIL_FROM: the email address from which the report will be sent
-   EMAIL_TO: the email address to which the report will be sent
-   SMTP_SERVER: the address of the SMTP server to use for sending the email
-   SMTP_PORT: the port number of the SMTP server
-   SMTP_USERNAME: the username for authenticating with the SMTP server (if required)
-   SMTP_PASSWORD: the password for authenticating with the SMTP server (if required)

You may also need to modify the following shell commands in the code to match your system:

-   "tail -n 50 /var/log/auth.log": the command for getting the system logs
-   "netstat -antu | grep LISTEN": the command for getting the open ports

## 🕹️ Run

To run the script, simply execute it using the Python interpreter:
```python server-status.py```

The script will generate an HTML email report and send it to the specified email address. The report will be sent once and then the script will exit. To run the script periodically, you can set up a cron job or use a task scheduler.

**cron job**: Server Performance Update : Every day @8am

```0 8 * * * /usr/bin/python3 /root/status/server-status.py```
