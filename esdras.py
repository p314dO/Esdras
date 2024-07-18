#!/usr/bin/env python3

import os
import sys
import subprocess
import re

# Define the directory structure
directory_structure = {
    "Pre-Engagement": {},
    "Linux": {
        "Information-Gathering": {},
        "Vulnerability-Assessment": {},
        "Exploitation": {},
        "Post-Exploitation": {},
        "Lateral-Movement": {}
    },
    "Windows": {
        "Information-Gathering": {},
        "Vulnerability-Assessment": {},
        "Exploitation": {},
        "Post-Exploitation": {},
        "Lateral-Movement": {}
    },
    "Reporting": {},
    "Results": {
        "Scan-Folder": {},
        "Discovered-Information": {
            "New-IPs": {},
            "Usernames": {},
            "Passwords": {},
            "Source-Code": {}
        }
    }
}

# Function to create directories
def create_directories(base_path, structure):
    for directory, subdirs in structure.items():
        path = os.path.join(base_path, directory)
        os.makedirs(path, exist_ok=True)
        create_directories(path, subdirs)

# Function to extract open ports from initial_scan file
def extract_open_ports(scan_file):
    with open(scan_file, 'r') as file:
        content = file.read()
    ports = re.findall(r'(\d+)/open', content)
    return ",".join(ports)

# Main function
def main():

    if len(sys.argv) != 3:
        print("Usage: python create_pentest_dir_and_scan.py <name> <IP>")
        sys.exit(1)

    print("")
    print("")
    print("   ▄████████    ▄████████ ████████▄     ▄████████    ▄████████    ▄████████      ")
    print("  ███    ███   ███    ███ ███   ▀███   ███    ███   ███    ███   ███    ███      ")
    print("  ███    █▀    ███    █▀  ███    ███   ███    ███   ███    ███   ███    █▀       ")
    print(" ▄███▄▄▄       ███        ███    ███  ▄███▄▄▄▄██▀   ███    ███   ███             ")
    print("▀▀███▀▀▀     ▀███████████ ███    ███ ▀▀███▀▀▀▀▀   ▀███████████ ▀███████████      ")
    print("  ███    █▄           ███ ███    ███ ▀███████████   ███    ███          ███      ")
    print("  ███    ███    ▄█    ███ ███   ▄███   ███    ███   ███    ███    ▄█    ███      ")
    print("  ██████████  ▄████████▀  ████████▀    ███    ███   ███    █▀   ▄████████▀       ")
    print("                                       ███    ███                                ")
    print("                                                                  by p314dO")
    print("")
    print("")

    pentest_name = sys.argv[1]
    ip_address = sys.argv[2]
    base_path = f"Pentest-{pentest_name}"

    # Create the directory structure
    create_directories(base_path, directory_structure)

    # Path to the Scan-Folder directory
    scan_folder_path = os.path.join(base_path, "Results", "Scan-Folder")

    # Change to the Scan-Folder directory
    os.chdir(scan_folder_path)

    # Run the initial nmap scan
    initial_scan_file = "initial_scan"
    print("Starting initial Nmap scan...")
    nmap_command = ["nmap", "-p-", "--open", "--min-rate=1000", "-oG", initial_scan_file, ip_address, "-Pn", "-n"]
    with open(os.devnull, 'wb') as null_file:
        subprocess.run(nmap_command, stdout=null_file, stderr=null_file)
    print("Initial Nmap scan completed.")

    # Extract open ports from the initial scan
    open_ports = extract_open_ports(initial_scan_file)

    if open_ports:
        # Execute the second nmap command
        print("Starting second Nmap scan...")
        nmap_second_result_file = "nmap_second_result.txt"
        with open(nmap_second_result_file, 'w') as result_file:
            subprocess.run(["nmap", "-sC", "-sV", f"-p{open_ports}", ip_address, "-Pn"], stdout=result_file, stderr=subprocess.STDOUT)
        print("Second Nmap scan completed.")

        # Read the result from the file
        with open(nmap_second_result_file, 'r') as file:
            nmap_second_result = file.read()

        # Generate HTML report
        html_content = f"""
        <html>
        <head>
            <link rel='stylesheet' type='text/css' href='scan_result.css'>
        </head>
        <body>
            <br>
            <h1 style='text-align:center;'>Esdras Report</h1>
            <div style='display: block; margin-left: auto; width: 80%;'>
                <pre>{nmap_second_result}</pre>
            </div>
        </body>
        </html>
        """

        # Save HTML report
        with open("scan_result.html", "w") as html_file:
            html_file.write(html_content)

        # Generate CSS for HTML report
        css_file = "scan_result.css"
        with open(css_file, "w") as css_file:
            css_file.write("pre { font-family: monospace; white-space: pre-wrap; }")

        # Show result in the browser
        print("Displaying the result in the browser...")
        subprocess.run(["xdg-open", "scan_result.html"])

        print(f"Second Nmap scan completed successfully on ports: {open_ports}")
    else:
        print("No open ports detected in the initial scan.")

    print(f"Directory structure '{base_path}' created and Nmap scans completed successfully.")

if __name__ == "__main__":
    main()
