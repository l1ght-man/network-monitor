import subprocess
import platform
import time
import datetime
def get_getway():
    result= subprocess.run(['ipconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
    output= result.stdout.lower()
    lines= output.split('\n')
    for line in lines:
        if 'default gateway' in line and '.' in line and "1" in line:
            parts = line.split(':')
            if len(parts) > 1 :
                gateway = parts[1].strip().split()[0]
                if gateway.startswith('192.') or gateway.startswith('10.') or gateway.startswith('172.') : return gateway
    return None 


gateway= get_getway()
if gateway :
    hosts= ['8.8.8.8',gateway,'google.com','1.1.1.1','127.0.0.1']
else: 
    hosts= ['8.8.8.8','google.com','1.1.1.1','127.0.0.1']

def ping_host(host):
    parm= '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', parm ,'4' , host]
    result= subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.returncode == 0

while True:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    for host in hosts:
        status = "UP" if ping_host(host) else "DOWN"
        log_entry= f"[{now}],{host}, {status}\n"
        print(log_entry.strip())
        with open('monitor.log','a') as f:
            f.write(log_entry)
    print("=====")
    time.sleep(30)
    with open('monitor.log','a') as f:
            f.write("=====updated after 30 seconds=====\n")

