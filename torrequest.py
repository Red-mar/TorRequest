import colorama
import sys
import argparse
import requests
from colorama import Fore, Style

colorama.init(Style.BRIGHT)

welcome = """
        -----=====-----

This application will try to make 
a request through the tor network

Please make sure the tor browser 
is running and the socks5 port is
correct.

        -----=====-----
"""

print(Fore.RED + Style.BRIGHT + welcome + Fore.RESET)

parser = argparse.ArgumentParser()
parser.add_argument("-t", dest="target", help="target url", type=str)
parser.set_defaults(target="")

args = parser.parse_args()


ipcheck_url = 'http://canihazip.com/s'

# The tor browser will accept requests 
# made to these ports on localhost

proxies = {
    'http': 'socks5h://127.0.0.1:9150',
    'https': 'socks5h://127.0.0.1:9150'
}

try:

    # First try to get the ip that tor is using
    # to make sure the connection is succesful

    tor_ip = requests.get(ipcheck_url, proxies=proxies)
    tor_ip = str(tor_ip.text)

    print(Fore.GREEN + Style.BRIGHT + "Succesfully connected with tor!" + Fore.RESET)
    print(Fore.WHITE + Style.BRIGHT + "New IP = " + Fore.BLUE + tor_ip + Fore.RESET)

    # When a connection is made send a request to 
    # the target and print the http code
    
    if args.target != "":
        print(Fore.WHITE + Style.BRIGHT + "Sending request to: " + Fore.BLUE + args.target + Fore.RESET)
        httpcode = str(requests.get(args.target))
        print(Fore.GREEN + Style.BRIGHT + "Got http code: " + Fore.BLUE + httpcode + Fore.RESET)
    else:
        print(Fore.RED + Style.BRIGHT + "No target specified." + Fore.RESET)

except requests.exceptions.RequestException as e:
    print(Fore.RED + Style.BRIGHT + e + Fore.RESET)
    sys.exit(0)

sys.exit(0)
