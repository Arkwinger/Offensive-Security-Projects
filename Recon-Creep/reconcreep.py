#!/usr/bin/env python3

import socket
import sys
import requests
import whois
import dns.resolver

def banner_grab(ip, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, port))
        s.send(b'HEAD / HTTP/1.0\r\n\r\n')
        banner = s.recv(1024).decode()
        print(f"\n[+] Banner on {ip}:{port}:\n{banner}")
    except:
        print(f"[!] Failed to connect to {ip}:{port}")
    finally:
        s.close()

def dns_lookup(domain):
    print(f"\n[+] DNS Lookup for {domain}")
    try:
        answers = dns.resolver.resolve(domain, 'A')
        for rdata in answers:
            print(f" - A Record: {rdata}")
    except Exception as e:
        print(f" [!] DNS Error: {e}")

def whois_lookup(domain):
    print(f"\n[+] WHOIS Lookup for {domain}")
    try:
        domain_info = whois.whois(domain)
        print(f" - Registrar: {domain_info.registrar}")
        print(f" - Creation Date: {domain_info.creation_date}")
        print(f" - Expiration Date: {domain_info.expiration_date}")
    except Exception as e:
        print(f" [!] WHOIS Error: {e}")

def header_inspect(domain):
    print(f"\n[+] HTTP Header Inspection for {domain}")
    try:
        headers = requests.get(f"http://{domain}", timeout=5).headers
        for key, value in headers.items():
            print(f" - {key}: {value}")
    except Exception as e:
        print(f" [!] Header Error: {e}")

def port_scan(ip):
    print(f"\n[+] Port Scan on {ip}")
    common_ports = [21, 22, 80, 443, 8080]
    for port in common_ports:
        try:
            s = socket.socket()
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            status = "Open" if result == 0 else "Closed/Filtered"
            print(f" - Port {port}: {status}")
            s.close()
        except Exception as e:
            print(f" [!] Error on port {port}: {e}")

def main():
    print("=== ReconCreep — Simulated Recon Toolkit ===")
    target = input("Enter target domain or IP: ").strip()
    
    print("\nSelect Module:")
    print(" [1] Banner Grab")
    print(" [2] DNS Lookup")
    print(" [3] WHOIS Info")
    print(" [4] HTTP Headers")
    print(" [5] Port Scan")
    choice = input("\nEnter module number: ").strip()

    if choice == "1":
        for port in [21, 22, 80, 443, 8080]:
            banner_grab(target, port)
    elif choice == "2":
        dns_lookup(target)
    elif choice == "3":
        whois_lookup(target)
    elif choice == "4":
        header_inspect(target)
    elif choice == "5":
        port_scan(target)
    else:
        print("\n[!] Invalid selection. Please try again.")

if __name__ == "__main__":
    
