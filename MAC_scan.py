from scapy.all import Ether, ARP, srp
import os
import time
import platform
import subprocess

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_connected_devices(subnet):
    # Send ARP requests within the subnet to discover connected devices
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=subnet), timeout=2, verbose=False)
    connected_devices = {}
    for sent, received in ans:
        mac = received.hwsrc
        ip = received.psrc
        connected_devices[mac] = ip
    return connected_devices

def print_connected_devices(connected_devices):
    print('Connected Devices:')
    for mac, ip in connected_devices.items():
        print(f"IP Address: {ip}, MAC Address: {mac}")

def remove_device_from_router(mac_address):
    if platform.system() == 'Windows':
        powershell_script = f"""
        $macAddress = "{mac_address}"
        $networkAdapters = Get-WmiObject Win32_NetworkAdapter | Where-Object {{ $_.MACAddress -eq $macAddress }}
        foreach ($adapter in $networkAdapters) {{
            $adapter.Disable()
            Write-Output "Disabled network adapter with MAC address $macAddress"
        }}
        """
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", powershell_script], capture_output=True, text=True)

def menu():
    clear_screen()
    router_ip = input("Enter the IP address of your Wi-Fi router (e.g., 192.168.1.1): ")
    subnet = '.'.join(router_ip.split('.')[:-1]) + '.1/24'  # Adjust subnet to scan the whole network
    while True:
        men_u = input('''
| ## Connected Devices Management ##
|
| 1. Scan Connected Devices
| 2. Remove Device
| 3. Exit
| >> ''')
        if men_u == '1':
            clear_screen()
            time.sleep(1)
            connected_devices = get_connected_devices(subnet)
            print_connected_devices(connected_devices)
        elif men_u == '2':
            mac_to_remove = input("Enter the MAC address of the device to remove: ")
            if not mac_to_remove:
                print("No MAC address entered. Please try again.")
                time.sleep(1)
                clear_screen()
                continue
            remove_device_from_router(mac_to_remove)
            print(f"Device with MAC address {mac_to_remove} removed from router.")
            time.sleep(1)
        elif men_u == '3':
            clear_screen()
            print('Exiting...')
            time.sleep(1)
            break
        else:
            clear_screen()
            print('Invalid option. Please try again.')

if __name__ == "__main__":
    menu()
