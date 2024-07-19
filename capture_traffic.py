import pydivert
import csv
import time

def packet_handler(packet):
    # Extract relevant details from the packet
    packet_details = {
        'src_ip': packet.src_addr,
        'dst_ip': packet.dst_addr,
        'src_port': packet.src_port,
        'dst_port': packet.dst_port,
        'protocol': packet.protocol,
        'length': len(packet.raw)  # Use the raw attribute to get the length
    }
    # Append packet details to CSV
    with open('captured_traffic.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=packet_details.keys())
        writer.writerow(packet_details)

try:
    print("Starting packet capture...")
    # Open CSV file and write the header
    with open('captured_traffic.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['src_ip', 'dst_ip', 'src_port', 'dst_port', 'protocol', 'length'])
        writer.writeheader()

    # Set the capture duration in seconds
    capture_duration = 30  # Capture for 30 seconds
    # Set the number of packets to capture
    packet_limit = 100  # Capture up to 100 packets

    start_time = time.time()
    packet_count = 0

    with pydivert.WinDivert() as w:
        while True:
            for packet in w:
                packet_handler(packet)
                w.send(packet)
                packet_count += 1
                if time.time() - start_time > capture_duration or packet_count >= packet_limit:
                    break
            if time.time() - start_time > capture_duration or packet_count >= packet_limit:
                break

    print("Packet capture completed.")
except Exception as e:
    print(f"Error: {e}")
