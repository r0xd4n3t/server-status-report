import psutil
import subprocess
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import humanfriendly

def get_uptime():
    uptime = subprocess.check_output("uptime").decode()
    return uptime

def get_running_processes():
    running_processes = ""
    for process in psutil.process_iter(['pid', 'name']):
        running_processes += str(process.info) + "\n"
    return running_processes

def get_logs():
    logs = subprocess.check_output("tail -n 50 /var/log/auth.log", shell=True).decode()
    return logs
	
def get_osx():
    osx = subprocess.check_output("lsb_release -s -d", shell=True).decode()
    return osx

def report_server_status():
    hostname = subprocess.check_output(['hostname']).decode()
    osx = get_osx()
    cpu_percent = psutil.cpu_percent()
    virtual_memory = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    net_io_counters = psutil.net_io_counters()
    human_readable_net_io_counters =  "Bytes sent: " + humanfriendly.format_size(net_io_counters.bytes_sent) + " Bytes received: " + humanfriendly.format_size(net_io_counters.bytes_recv)
    boot_time = psutil.boot_time()
    human_readable_boot_time = datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')
    uptime = get_uptime()
    who = subprocess.check_output(['w']).decode()
    last_login = subprocess.check_output("last | head -n 10", shell=True).decode()
    open_port = subprocess.check_output("netstat -antu | grep LISTEN", shell=True).decode()
    logs = get_logs()
    running_processes = get_running_processes()
    today = datetime.now()
    date = today.strftime("%d/%m/%Y")

    message = """\
    <html>
        <body>
<table cellspacing="0" style="border-collapse:collapse; height:400px; width:800px">
	<tbody>
		<tr>
			<td colspan="2" style="background-color:#9bc2e6; border-bottom:1px solid black; border-left:1px solid black; border-right:1px solid black; border-top:1px solid black; height:19px; text-align:center; vertical-align:bottom; white-space:nowrap; width:327px"><span style="font-size:15px"><span style="color:white"><strong><span style="font-family:Calibri,sans-serif">Server Uptime Report</span></strong></span></span></td>
		</tr>
		<tr>
			<td style="border-color:currentcolor black black; border-style:none solid solid; border-width:medium 1px 1px; height:19px; vertical-align:bottom; white-space:nowrap; width:135px">Hostname:</td>
			<td style="border-color:currentcolor black black currentcolor; border-style:none solid solid none; border-width:medium 1px 1px medium; vertical-align:bottom; white-space:nowrap; width:507px"><span style="font-size:15px"><span style="color:black"><span style="font-family:Calibri,sans-serif">&nbsp;</span></span></span>{}</td>
		</tr>
		<tr>
			<td style="border-color:currentcolor black black; border-style:none solid solid; border-width:medium 1px 1px; height:19px; vertical-align:bottom; white-space:nowrap; width:135px">OS:</td>
			<td style="border-color:currentcolor black black currentcolor; border-style:none solid solid none; border-width:medium 1px 1px medium; vertical-align:bottom; white-space:nowrap; width:507px"><span style="font-size:15px"><span style="color:black"><span style="font-family:Calibri,sans-serif">&nbsp;</span></span></span>{}</td>
		</tr>
		<tr>
			<td style="border-color:currentcolor black black; border-style:none solid solid; border-width:medium 1px 1px; height:19px; vertical-align:bottom; white-space:nowrap; width:135px">CPU Usage:</td>
			<td style="border-color:currentcolor black black currentcolor; border-style:none solid solid none; border-width:medium 1px 1px medium; vertical-align:bottom; white-space:nowrap; width:507px"><span style="font-size:15px"><span style="color:black"><span style="font-family:Calibri,sans-serif">&nbsp;</span></span></span>{}%</td>
		</tr>
		<tr>
			<td style="border-color:currentcolor black black; border-style:none solid solid; border-width:medium 1px 1px; height:19px; vertical-align:bottom; white-space:nowrap; width:135px">Virtual Memory Usage:</td>
			<td style="border-color:currentcolor black black currentcolor; border-style:none solid solid none; border-width:medium 1px 1px medium; vertical-align:bottom; white-space:nowrap; width:507px"><span style="font-size:15px"><span style="color:black"><span style="font-family:Calibri,sans-serif">&nbsp;</span></span></span>{}</td>
		</tr>
		<tr>
			<td style="border-color:currentcolor black black; border-style:none solid solid; border-width:medium 1px 1px; height:19px; vertical-align:bottom; white-space:nowrap; width:135px">Disk Usage:</td>
			<td style="border-color:currentcolor black black currentcolor; border-style:none solid solid none; border-width:medium 1px 1px medium; vertical-align:bottom; white-space:nowrap; width:507px"><span style="font-size:15px"><span style="color:black"><span style="font-family:Calibri,sans-serif">&nbsp;</span></span></span>{}</td>
		</tr>
		<tr>
			<td style="border-color:currentcolor black black; border-style:none solid solid; border-width:medium 1px 1px; height:19px; vertical-align:bottom; white-space:nowrap; width:135px">Network IO counters:</td>
			<td style="border-color:currentcolor black black currentcolor; border-style:none solid solid none; border-width:medium 1px 1px medium; vertical-align:bottom; white-space:nowrap; width:507px"><span style="font-size:15px"><span style="color:black"><span style="font-family:Calibri,sans-serif">&nbsp;</span></span></span>{}</td>
		</tr>
		<tr>
			<td style="border-color:currentcolor black black; border-style:none solid solid; border-width:medium 1px 1px; height:19px; vertical-align:bottom; white-space:nowrap; width:135px">Boot time:</td>
			<td style="border-color:currentcolor black black currentcolor; border-style:none solid solid none; border-width:medium 1px 1px medium; vertical-align:bottom; white-space:nowrap; width:507px"><span style="font-size:15px"><span style="color:black"><span style="font-family:Calibri,sans-serif">&nbsp;</span></span></span>{}</td>
		</tr>
		<tr>
			<td style="border-color:currentcolor black black; border-style:none solid solid; border-width:medium 1px 1px; height:19px; vertical-align:bottom; white-space:nowrap; width:135px">Uptime:</td>
			<td style="border-color:currentcolor black black currentcolor; border-style:none solid solid none; border-width:medium 1px 1px medium; vertical-align:bottom; white-space:nowrap; width:507px"><span style="font-size:15px"><span style="color:black"><span style="font-family:Calibri,sans-serif">&nbsp;</span></span></span>{}</td>
		</tr>
		<tr>
			<td style="border-color:currentcolor black black; border-style:none solid solid; border-width:medium 1px 1px; height:19px; vertical-align:bottom; white-space:nowrap; width:135px">Who:</td>
			<td style="border-color:currentcolor black black currentcolor; border-style:none solid solid none; border-width:medium 1px 1px medium; vertical-align:bottom; white-space:nowrap; width:507px"><pre style='font-family: "Courier New", Courier, monospace;'>{}</pre></td>
		</tr>
		<tr>
			<td style="border-color:currentcolor black black; border-style:none solid solid; border-width:medium 1px 1px; height:19px; vertical-align:bottom; white-space:nowrap; width:135px">Last Login:</td>
			<td style="border-color:currentcolor black black currentcolor; border-style:none solid solid none; border-width:medium 1px 1px medium; vertical-align:bottom; white-space:nowrap; width:507px"><pre style='font-family: "Courier New", Courier, monospace;'>{}</pre></td>
		</tr>
		<tr>
			<td style="border-color:currentcolor black black; border-style:none solid solid; border-width:medium 1px 1px; height:19px; vertical-align:bottom; white-space:nowrap; width:135px">Open Port:</td>
			<td style="border-color:currentcolor black black currentcolor; border-style:none solid solid none; border-width:medium 1px 1px medium; vertical-align:bottom; white-space:nowrap; width:507px"><pre style='font-family: "Courier New", Courier, monospace;'>{}</pre></td>
		</tr>
		<tr>
			<td style="border-color:currentcolor black black; border-style:none solid solid; border-width:medium 1px 1px; height:19px; vertical-align:bottom; white-space:nowrap; width:135px">Running Processes:</td>
			<td style="border-color:currentcolor black black currentcolor; border-style:none solid solid none; border-width:medium 1px 1px medium; vertical-align:bottom; white-space:nowrap; width:507px"><pre style='font-family: "Courier New", Courier, monospace;'>{}</pre></td>
		</tr>
		<tr>
			<td style="border-color:currentcolor black black; border-style:none solid solid; border-width:medium 1px 1px; height:19px; vertical-align:bottom; white-space:nowrap; width:135px">Auth Logs:</td>
			<td style="border-color:currentcolor black black currentcolor; border-style:none solid solid none; border-width:medium 1px 1px medium; vertical-align:bottom; white-space:nowrap; width:507px"><pre style='font-family: "Courier New", Courier, monospace;'>{}</pre></td>
		</tr>
	</tbody>
</table>
        </body>
    </html>
    """.format(hostname,osx,cpu_percent, 
               humanfriendly.format_size(virtual_memory.used, binary=True),
               humanfriendly.format_size(disk_usage.used, binary=True),
               human_readable_net_io_counters,human_readable_boot_time,
               uptime,who,last_login,open_port,running_processes,logs)

    msg = MIMEMultipart('related')
    msg['Subject'] = 'Performance Update - {}'.format(date)
    msg['From'] = "your@email.com"
    msg['To'] = "your@email.com"

    body = MIMEText(message, 'html')
    msg.attach(body)

    server = smtplib.SMTP('your-smtp-here', 587)
    server.starttls()
    server.login("your@email.com", "your-pass-here")
    server.send_message(msg)
    server.quit()

report_server_status()
