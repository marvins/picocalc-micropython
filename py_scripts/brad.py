"""
brad.py - Simple helper functions for WiFi on Raspberry Pi Pico 2 W
"""
import network
import time
import socket
import json
import os

# Global variable to store the WLAN object
wlan = None

def save_wifi(ssid, password):
    """Save WiFi credentials to a file"""
    config = {
        "ssid": ssid,
        "password": password
    }
    with open('wifi.json', 'w') as f:
        json.dump(config, f)
    print(f"Saved credentials for {ssid}")

def load_wifi():
    """Load WiFi credentials from file"""
    try:
        with open('wifi.json', 'r') as f:
            config = json.load(f)
        return config.get("ssid", ""), config.get("password", "")
    except:
        return "", ""

def connect(ssid=None, password=None):
    """Connect to WiFi with given or saved credentials"""
    global wlan
    
    # If no credentials provided, try to load saved ones
    if not ssid or not password:
        ssid, password = load_wifi()
        if not ssid or not password:
            print("No WiFi credentials found!")
            print("Usage: brad.connect('your_ssid', 'your_password')")
            return None
    else:
        # Save the credentials for future use
        save_wifi(ssid, password)
    
    # Create and activate the network interface
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Check if already connected
    if wlan.isconnected():
        print(f"Already connected to {ssid}")
        print(f"IP: {wlan.ifconfig()[0]}")
        return wlan
    
    print(f"Connecting to {ssid}...")
    wlan.connect(ssid, password)
    
    # Wait for connection with timeout
    timeout = 10
    while timeout > 0 and not wlan.isconnected():
        print(".", end="")
        time.sleep(1)
        timeout -= 1
    print()
    
    if wlan.isconnected():
        print(f"Connected to {ssid}!")
        print(f"IP: {wlan.ifconfig()[0]}")
        return wlan
    else:
        print("Connection failed!")
        print("Check your credentials or signal strength")
        return None

def status():
    """Check WiFi connection status"""
    global wlan
    
    if not wlan:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
    
    if wlan.isconnected():
        ip, subnet, gateway, dns = wlan.ifconfig()
        ssid = wlan.config('essid')
        print(f"Connected to: {ssid}")
        print(f"IP address: {ip}")
        print(f"Gateway: {gateway}")
        print(f"DNS: {dns}")
        return True
    else:
        print("Not connected to WiFi")
        return False

def scan():
    """Scan for available WiFi networks"""
    global wlan
    
    if not wlan:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
    
    print("Scanning for networks...")
    networks = wlan.scan()
    
    print("\nAvailable Networks:")
    print("-" * 45)
    print("SSID                     | Channel | Signal | Security")
    print("-" * 45)
    
    for ssid, bssid, channel, rssi, security, hidden in networks:
        ssid = ssid.decode('utf-8') if isinstance(ssid, bytes) else ssid
        
        # Convert RSSI to a readable signal strength
        signal_strength = "Weak"
        if rssi > -67:
            signal_strength = "Excellent"
        elif rssi > -70:
            signal_strength = "Good"
        elif rssi > -80:
            signal_strength = "Fair"
        
        # Convert security to readable format
        security_types = ["Open", "WEP", "WPA-PSK", "WPA2-PSK", "WPA/WPA2-PSK", "WPA3"]
        security_str = security_types[security] if security < len(security_types) else "Unknown"
        
        print(f"{ssid:<25} | {channel:^7} | {signal_strength:<7} | {security_str}")
    
    return networks

def scan_no_show():
    """Scan for available WiFi networks"""
    global wlan
    
    if not wlan:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
    
    networks = wlan.scan()
    
    for ssid, bssid, channel, rssi, security, hidden in networks:
        ssid = ssid.decode('utf-8') if isinstance(ssid, bytes) else ssid
        
        # Convert RSSI to a readable signal strength
        signal_strength = "Weak"
        if rssi > -67:
            signal_strength = "Excellent"
        elif rssi > -70:
            signal_strength = "Good"
        elif rssi > -80:
            signal_strength = "Fair"
        
        # Convert security to readable format
        security_types = ["Open", "WEP", "WPA-PSK", "WPA2-PSK", "WPA/WPA2-PSK", "WPA3"]
        security_str = security_types[security] if security < len(security_types) else "Unknown"
        
        # print(f"{ssid:<25} | {channel:^7} | {signal_strength:<7} | {security_str}")
    
    return networks

def disconnect():
    """Disconnect from WiFi"""
    global wlan
    
    if not wlan:
        wlan = network.WLAN(network.STA_IF)
    
    if wlan.isconnected():
        wlan.disconnect()
        print("Disconnected from WiFi")
    else:
        print("Not connected to WiFi")

def ping(host="8.8.8.8"):
    """Test internet connectivity by pinging a host"""
    if not status():
        return False
        
    try:
        print(f"Pinging {host}...")
        ip = socket.getaddrinfo(host, 80)[0][-1][0]
        print(f"Success! Host {host} is reachable at {ip}")
        return True
    except Exception as e:
        print(f"Ping failed: {e}")
        return False

# Print a helpful message when importing the module
# print("Brad loaded! Available commands:")
# print("  brad.status() - Check connection status")
# print("  brad.scan() - Scan for networks")
# print("  brad.disconnect() - Disconnect from WiFi")
# print("  brad.ping() - Test internet connectivity")