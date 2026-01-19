import socket
import datetime
import time
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 443, 993, 995, 3389, 8080]
PORT_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 443: "HTTPS", 993: "IMAPS", 995: "POP3S",
    3389: "RDP", 8080: "HTTP-Alt"}
def scan_port(host, port , timeout=2):
    sock= socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((host,port))
    sock.close()
    return result == 0


def scan_host(host):
    print(f"\n🔍 Scanning {host}...")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    open_ports= []
    for port in COMMON_PORTS :
        if scan_port(host, port):
            service= PORT_SERVICES.get(port, "Ukknown")
            print(f"✅ {port:5} {service:<10} OPEN")
            open_ports.append(port)
            with open('open_port.log', 'a') as f:
                f.write(f"[{now}],  {port:5} {service:<10} OPEN\n")
        else:   
            print(f"❌ {port:5} DOWN")
    print(f"{host}: {len(open_ports)} : open ports\n")
    with open('open_port.log', 'a') as f:
        f.write(f">>>> TOTAL PORTS FOR {host}: {len(open_ports)} : open ports\n")
    
    



if __name__ == "__main__" :
    host="127.0.0.1"
    scan_host(host)