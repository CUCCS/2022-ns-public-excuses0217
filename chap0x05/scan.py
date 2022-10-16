#! /usr/bin/python

from scapy.all import *
import argparse


def tcp_connect(dst_ip, dst_port, timeout):
    pkts = sr1(IP(dst=dst_ip)/TCP(dport=dst_port, flags="S"), timeout=timeout)
    if (pkts is None):
        print("The target port " + dst_ip + ":" +
              str(dst_port) + "/TCP is Filtered")
    elif (pkts.haslayer(TCP)):
        if (pkts.getlayer(TCP).flags == 0x12):  # Flags: 0x012 (SYN, ACK)
            send_rst = sr(IP(dst=dst_ip)/TCP(dport=dst_port,
                          flags="AR"), timeout=timeout)
            print("The target port " + dst_ip +
                  ":" + str(dst_port) + "/TCP is Open")
        elif (pkts.getlayer(TCP).flags == 0x14):  # Flags: 0x014 (RST, ACK)
            print("The target port " + dst_ip +
                  ":" + str(dst_port) + "/TCP is Closed")
    elif (pkts.haslayer(ICMP)):  # ICMP error packets sent by firewall
        if (int(pkts.getlayer(ICMP).type) == 3 and int(pkts.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]):
            print("The target port " + dst_ip + ":" +
                  str(dst_port) + "/TCP is Filtered")


def tcp_stealth(dst_ip, dst_port, timeout):
    pkts = sr1(IP(dst=dst_ip)/TCP(dport=dst_port, flags="S"), timeout=10)
    if (pkts is None):
        print("The target port " + dst_ip + ":" +
              str(dst_port) + "/TCP is Filtered")
    elif (pkts.haslayer(TCP)):
        if (pkts.getlayer(TCP).flags == 0x12):
            send_rst = sr(IP(dst=dst_ip) /
                          TCP(dport=dst_port, flags="R"), timeout=10)
            print("The target port " + dst_ip +
                  ":" + str(dst_port) + "/TCP is Open")
        elif (pkts.getlayer(TCP).flags == 0x14):  # Flags: 0x014 (RST, ACK)
            print("The target port " + dst_ip +
                  ":" + str(dst_port) + "/TCP is Closed")
    elif (pkts.haslayer(ICMP)):  # ICMP error packets sent by firewall
        if (int(pkts.getlayer(ICMP).type) == 3 and int(pkts.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]):
            print("The target port " + dst_ip + ":" +
                  str(dst_port) + "/TCP is Filtered")


def tcp_xmas(dst_ip, dst_port, timeout):
    pkts = sr1(IP(dst=dst_ip)/TCP(dport=dst_port, flags="FPU"), timeout=10)
    if (pkts is None):
        print("The target port " + dst_ip +
              ":" + str(dst_port) + "/TCP is Open or Filtered")
    elif (pkts.haslayer(TCP)):
        if (pkts.getlayer(TCP).flags == 0x14):  # Flags: 0x014 (RST, ACK)
            print("The target port " + dst_ip +
                  ":" + str(dst_port) + "/TCP is Closed")
    elif (pkts.haslayer(ICMP)):  # ICMP error packets sent by firewall
        if (int(pkts.getlayer(ICMP).type) == 3 and int(pkts.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]):
            print("The target port " + dst_ip + ":" +
                  str(dst_port) + "/TCP is Filtered")


def tcp_fin(dst_ip, dst_port, timeout):
    pkts = sr1(IP(dst=dst_ip)/TCP(dport=dst_port, flags="F"), timeout=10)
    if (pkts is None):
        print("The target port " + dst_ip +
              ":" + str(dst_port) + "/TCP is Open or Filtered")
    elif (pkts.haslayer(TCP)):
        if (pkts.getlayer(TCP).flags == 0x14):  # Flags: 0x014 (RST, ACK)
            print("The target port " + dst_ip +
                  ":" + str(dst_port) + "/TCP is Closed")
    elif (pkts.haslayer(ICMP)):  # ICMP error packets sent by firewall
        if (int(pkts.getlayer(ICMP).type) == 3 and int(pkts.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]):
            print("The target port " + dst_ip + ":" +
                  str(dst_port) + "/TCP is Filtered")


def tcp_null(dst_ip, dst_port, timeout):
    pkts = sr1(IP(dst=dst_ip)/TCP(dport=dst_port, flags=""), timeout=10)
    if (pkts is None):
        print("The target port " + dst_ip +
              ":" + str(dst_port) + "/TCP is Open or Filtered")
    elif (pkts.haslayer(TCP)):
        if (pkts.getlayer(TCP).flags == 0x14):  # Flags: 0x014 (RST, ACK)
            print("The target port " + dst_ip +
                  ":" + str(dst_port) + "/TCP is Closed")
    elif (pkts.haslayer(ICMP)):  # ICMP error packets sent by firewall
        if (int(pkts.getlayer(ICMP).type) == 3 and int(pkts.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]):
            print("The target port " + dst_ip + ":" +
                  str(dst_port) + "/TCP is Filtered")


def udp_scan(dst_ip, dst_port, dst_timeout):
    resp = sr1(IP(dst=dst_ip)/UDP(dport=dst_port), timeout=dst_timeout)
    if (resp is None):
        print("The target port " + dst_ip +
              ":" + str(dst_port) + "/UDP is Open or Filtered")
    elif (resp.haslayer(UDP)):
        print("The target port " + dst_ip + ":" +
              str(dst_port) + "/UDP is Open")
    elif (resp.haslayer(ICMP)):  # ICMP error packets sent by firewall
        if (int(resp.getlayer(ICMP).type) == 3 and int(resp.getlayer(ICMP).code) == 3):
            print("The target port " + dst_ip +
                  ":" + str(dst_port) + "/UDP is Closed")
        elif (int(resp.getlayer(ICMP).type) == 3 and int(resp.getlayer(ICMP).code) in [1, 2, 9, 10, 13]):
            print("The target port " + dst_ip + ":" +
                  str(dst_port) + "/UDP is Filtered")
        elif (resp.haslayer(IP) and resp.getlayer(IP).proto == IP_PROTOS.udp):
            print("The target port " + dst_ip +
                  ":" + str(dst_port) + "/UDP is Open")


parser = argparse.ArgumentParser(
    description='This is a script that scans the status of the destination port.')
parser.add_argument('-s', '--scantype', type=str, help='methods to scan the port', required=True,
                    choices=['tcp_connect', 'tcp_stealth', 'tcp_xmas', 'tcp_fin', 'tcp_null', 'udp_scan'])
parser.add_argument('-i', '--dstip', type=str,
                    help='destination IP address', required=True)
parser.add_argument('-p', '--dstport', type=int,
                    help='destination port number', required=True)
parser.add_argument('-t', '--timeout', type=int,
                    help='timeout, default=10', default=10)
args = parser.parse_args()

if __name__ == '__main__':
    try:
        print(args.scantype + " scanning...")
        if (args.scantype == 'tcp_connect'):
            tcp_connect(args.dstip, args.dstport, args.timeout)
        elif (args.scantype == 'tcp_stealth'):
            tcp_stealth(args.dstip, args.dstport, args.timeout)
        elif (args.scantype == 'tcp_xmas'):
            tcp_xmas(args.dstip, args.dstport, args.timeout)
        elif (args.scantype == 'tcp_fin'):
            tcp_fin(args.dstip, args.dstport, args.timeout)
        elif (args.scantype == 'tcp_null'):
            tcp_null(args.dstip, args.dstport, args.timeout)
        elif (args.scantype == 'udp_scan'):
            udp_scan(args.dstip, args.dstport, args.timeout)
    except Exception as e:
        print(e)
