import subprocess
import platform
import time
import datetime

def send_alert(host , status ) :
    alert_file = "alert_file.txt"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert = f"[{timestamp}] {host} is {status}\n"
    with open(alert_file, 'a') as f:
        f.write(alert + "\n")





def get_gatway():
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


hosts= ['8.8.8.8','google.com','1.1.1.1','127.0.0.1']
gateway= get_gatway()
if gateway :
    hosts.insert(0,gateway)
 
user_input = input("add a host? (y/n) ")
if user_input.strip().lower() == "y":
    new_host = input("write the host IP/domaine: ")
    if new_host:
        hosts.append(new_host)
        print(f"{new_host} Added")

        
def ping_host(host):
    parm= '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', parm ,'4' , host]
    result= subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.returncode == 0
try:
    while True:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        last_status = {host: None for host in hosts}
        for host in hosts:
            status = "UP" if ping_host(host) else "DOWN"
            if host not in last_status or last_status[host] is None:
                last_status[host] = "UP"
            if status != last_status[host] :
                last_status[host] = status
                send_alert(host, last_status[host]) 
            log_entry= f"[{now}],{host}, {status}\n"
            print(log_entry.strip())
            with open('monitor.log','a') as f:
                f.write(log_entry)
        print("=====")
        time.sleep(30)
        with open('monitor.log','a') as f:
                f.write("******updated after 30 seconds******\n")
except KeyboardInterrupt:
    print("\nmonitor stopped ")
    with open('monitor.log','a') as f:
        f.write(f"=====monitor stopped by user {datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")} =====\n") 
