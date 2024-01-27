import argparse
import subprocess

def get_argument():
    parser = argparse.ArgumentParser(description='Change the MAC address of a network interface')
    parser.add_argument('-i', '--interface', dest='interface', required=True, help='interface to change its MAC address')
    parser.add_argument('-m', '--mac', dest='new_mac', required=True, help='new MAC address')
    args = parser.parse_args()
    return args

def change_mac(interface, new_mac):
    print("[+] changing MAC address for {} to {}".format(interface, new_mac))
    subprocess.run(["ifconfig", interface, "down"])
    subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.run(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode('utf-8')
    mac_address_search_result = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(1)
    else:
        print("[-] could not read mac address")

args = get_argument()
current_mac = get_current_mac(args.interface)
print("current mac = {}".format(current_mac))
change_mac(args.interface, args.new_mac)
current_mac = get_current_mac(args.interface)

if current_mac == args.new_mac:
    print("[+] MAC address was successfully changed to {}".format(current_mac))
else:
    print("[-] MAC address did not change")