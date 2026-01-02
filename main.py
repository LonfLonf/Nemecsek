import argparse
import subprocess
import auxiliar
import requests
from auxiliar import packet

def print_banner():
    print ("""
    ███╗   ██╗███████╗███╗   ███╗███████╗ ██████╗███████╗███████╗██╗  ██╗   
    ████╗  ██║██╔════╝████╗ ████║██╔════╝██╔════╝██╔════╝██╔════╝██║ ██╔╝    
    ██╔██╗ ██║█████╗  ██╔████╔██║█████╗  ██║     ███████╗█████╗  █████╔╝    
    ██║╚██╗██║██╔══╝  ██║╚██╔╝██║██╔══╝  ██║     ╚════██║██╔══╝  ██╔═██╗    
    ██║ ╚████║███████╗██║ ╚═╝ ██║███████╗╚██████╗███████║███████╗██║  ██╗  
    ╚═╝  ╚═══╝╚══════╝╚═╝     ╚═╝╚══════╝ ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝
    """)

def nmap(host):
    command = "sudo nmap -sV -sC --min-parallelism 10 --max-parallelism 100 --open -oX nmapScan.xml " + host
    subprocess.run(command, shell=True, capture_output=False, text=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    packets = auxiliar.parser_xml2packet("nmapScan.xml")
    return packets

def ffuf(host, port):
    command = (
        f"ffuf -u http://{host}:{port}/FUZZ "
        f"-w ./raft-medium-directories.txt "
        f"-mc 200,301,302,403 " 
        f"-t 100 "
        f"-fc 404 "
        f"-of json "
        f"-o ./out.json"
    )     
    subprocess.run(command, shell=True, capture_output=False, text=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def crawlers(host, port):
    baseurl = f"http://{host}:{port}/"
    targets = {"robots.txt", "sitemap.xml"}
    results = []
        
    for target in targets:
        url = f"{baseurl}/{target}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            results.append(response.text)
    print(results)

    
def main():
    print_banner()

    parser = argparse.ArgumentParser(
        prog='ProgramName',
        description='What the program does',
        epilog='Text at the bottom of help'
    )
    
    parser.add_argument('-host', '-H', type=str)
    parser.add_argument('-port', '-p', type=str)
    args = parser.parse_args()

    print(f"Starting scan on host: {args.host}")
    packets = nmap(args.host)
    print("Nmap scan completed. Results:")
    auxiliar.print_objs(packets)
    for packet in packets:
        if packet.name == "http":
            print(f"Running additional scans on {args.host}:{packet.port}")
            
            print("Running ffuf...")
            ffuf(args.host, packet.port)
            print("ffuf completed. Results saved to out.json")
            
            print("Running crawlers...")
            crawlers(args.host, packet.port)
            print("Crawlers completed.")
            
            
    auxiliar.print_objs(packets)


if __name__ == "__main__":
    main()