import pywifi
from pywifi import PyWiFi, const
from scapy.all import *
from scapy.all import IP, TCP, UDP, ICMP
import pandas as pd
import threading
import time

# Global flag to stop threads
stop_threads = False

# Global traffic statistics
packet_count = 0
total_data = 0
protocol_counts = {"TCP": 0, "UDP": 0, "ICMP": 0, "Other": 0}

def scan_wifi():
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]
    
    iface.scan()
    scan_results = iface.scan_results()
    
    for network in scan_results:
        print(f'SSID: {network.ssid}, Signal: {network.signal}, Auth: {network.auth}')

def packet_callback(packet):
    global packet_count, total_data, protocol_counts

    # Increment packet count and total data
    packet_count += 1
    total_data += len(packet)

    # Determine packet type and increment corresponding counter
    if packet.haslayer(TCP):
        protocol_counts["TCP"] += 1
    elif packet.haslayer(UDP):
        protocol_counts["UDP"] += 1
    elif packet.haslayer(ICMP):
        protocol_counts["ICMP"] += 1
    else:
        protocol_counts["Other"] += 1

    # Print basic packet summary
    print(packet.summary())

    # Print detailed packet information
    print(f"Packet Size: {len(packet)} bytes")
    if packet.haslayer(IP):
        ip_layer = packet.getlayer(IP)
        print(f"Source IP: {ip_layer.src}")
        print(f"Destination IP: {ip_layer.dst}")
    if packet.haslayer(TCP):
        tcp_layer = packet.getlayer(TCP)
        print(f"Source Port: {tcp_layer.sport}")
        print(f"Destination Port: {tcp_layer.dport}")
    if packet.haslayer(UDP):
        udp_layer = packet.getlayer(UDP)
        print(f"Source Port: {udp_layer.sport}")
        print(f"Destination Port: {udp_layer.dport}")
    print("\n")

def capture_traffic(interface):
    global stop_threads
    print(f"Starting packet capture on {interface}")
    while not stop_threads:
        sniff(iface=interface, prn=packet_callback, store=0, timeout=1)

def optimize_wifi():
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]
    
    iface.scan()
    scan_results = iface.scan_results()
    
    channels = {}
    for network in scan_results:
        channel = network.freq  # Frequency in MHz
        if channel not in channels:
            channels[channel] = 0
        channels[channel] += 1
    
    least_used_channel = min(channels, key=channels.get)
    print(f'Least used channel: {least_used_channel // 1000} MHz')

    for channel, usage in sorted(channels.items()):
        print(f'Channel: {channel // 1000} MHz, Usage: {usage}')
    
    print("\nTo optimize your Wi-Fi, consider changing to the least used channel listed above.")

def print_traffic_stats():
    global packet_count, total_data, protocol_counts
    
    data = {
        "Metric": ["Total Packets", "Total Data (bytes)", "TCP Packets", "UDP Packets", "ICMP Packets", "Other Packets"],
        "Value": [packet_count, total_data, protocol_counts["TCP"], protocol_counts["UDP"], protocol_counts["ICMP"], protocol_counts["Other"]]
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Print DataFrame as table
    print(df.to_string(index=False))

if __name__ == "__main__":
    interface = "Wi-Fi"  # Use the Wi-Fi interface name
    
    try:
        # Start Wi-Fi scan
        scan_wifi()
        
        # Start traffic capture in a separate thread
        capture_thread = threading.Thread(target=capture_traffic, args=(interface,))
        capture_thread.start()
        
        # Optimize Wi-Fi
        optimize_wifi()
        
        # Simulate running for 10 seconds
        time.sleep(10)
    finally:
        # Stop the traffic capture thread
        stop_threads = True
        capture_thread.join()
        print("Stopped packet capture")
        
        # Print traffic statistics in a table
        print_traffic_stats()
