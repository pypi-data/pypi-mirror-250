import os
import sys
import socket
import requests




def check_internet():
    websites = ["http://www.google.com", "http://www.github.com", "http://pypi.org"]
    for website in websites:
        try:
            response = requests.get(website)
            print(website, 'response status code:', response.status_code)
        except requests.exceptions.RequestException as err:
            print ("CANNOT CONNET TO INTERNET! : ",err)
            # internetを繋がらないとerrorを出す
            break
# i like just ping           
# for website in websites:
#     response = os.system("ping -c 1 " + website)
#     if response == 0:
#         print(website, 'is up!')
#     else:
#         print(website, 'is down!')

def get_public_ip():
    response = requests.get('https://api.ipify.org')
    return response.text   #とあるIPを示すwebsite 

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))   # Google Public DNSのIP
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def check_ports(ip, start_port, end_port):
    # window11 power shell--->>>netstat -ano
    open_ports = []
    for port in range(start_port, end_port+1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return ip, open_ports
    #print(check_ports("127.0.0.1", 6000, 6006),'port')
    #print(check_ports("192.168.0.1", 1, 80),'port')
    #print(check_ports("192.168.112.113", 1, 80),'port')
def main():
    check_internet()
    print(get_host_ip())
    print(get_public_ip())
    n=len(sys.argv)
    if n !=3:
        sys.exit()
    else:
        print('The occupied port number') #占有しているport番号は
        print(check_ports(sys.argv[0],sys.argv[1],sys.argv[2]),'port')    

if __name__ == "__main__":
    main()