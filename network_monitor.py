import subprocess
import platform
import time
import datetime

def ping_host(host):
    parm= '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', parm ,'4' , host]
    result= subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.returncode == 0

hosts= ['8.8.8.8','google.com','1.1.1.1']
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

print (ping_host("google.com"))