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

print(Fore.CYAN + Style.BRIGHT + welcome + Fore.RESET)

parser = argparse.ArgumentParser()
parser.add_argument("-t", dest="target", help="target url", type=str)
parser.add_argument("-p", dest="proxy", help="tor socks5 proxy", type=str)
parser.set_defaults(target="")
parser.set_defaults(proxy="9050")

args = parser.parse_args()


ipcheck_url = 'http://canihazip.com/s'

# The tor browser will accept requests 
# made to these ports on localhost

proxies = {
    'http' : 'socks5://127.0.0.1:' + args.proxy,
    'https': 'socks5://127.0.0.1:' + args.proxy
}

try:

    # First try to get the ip that tor is using
    # to make sure the connection is succesful

    old_ip = requests.get(ipcheck_url)
    old_ip = str(old_ip.text)

    tor_ip = requests.get(ipcheck_url, proxies=proxies)
    tor_ip = str(tor_ip.text)

    print(Fore.GREEN + Style.BRIGHT + "Succesfully connected with tor!" + Fore.RESET)
    print(Fore.WHITE + Style.BRIGHT + "Old IP = " + Fore.BLUE + old_ip + Fore.RESET)
    print(Fore.WHITE + Style.BRIGHT + "New IP = " + Fore.BLUE + tor_ip + Fore.RESET)

    # When a connection is made send a request to 
    # the target and print the http code
    
    if args.target != "":
        print(Fore.WHITE + Style.BRIGHT + "Sending request to: " + Fore.BLUE + args.target + Fore.RESET)
        httpcode = str(requests.get(args.target))
        print(Fore.GREEN + Style.BRIGHT + "Got http code: " + Fore.BLUE + httpcode + Fore.RESET)
    else:
        print(Fore.RED + Style.BRIGHT + "No target specified." + Fore.RESET)

except requests.exceptions.ConnectionError as e:
    print(Fore.RED + Style.BRIGHT + "Connection Error!" + Fore.RESET)
    print(Fore.WHITE + Style.BRIGHT + "Make sure the tor browser / service is running and the proxy is correct." + Fore.RESET)
    print(Fore.WHITE + Style.BRIGHT + "Set the proxy with -p. for example \"-p 9050\"\n" + Fore.RESET)

    print(Fore.BLUE + Style.BRIGHT + "Currently set Proxies: ")
    for proxy in proxies:
        print(Fore.WHITE + Style.BRIGHT + proxy + " - " + proxies.get(proxy) + Fore.RESET)

    print("\n")
    print(Fore.MAGENTA + Style.BRIGHT + "Traceback: " + Fore.RESET)
    print(e)
    sys.exit(0)

except requests.exceptions.RequestException as e:
    print(Fore.RED + Style.BRIGHT + e + Fore.RESET)
    sys.exit(0)

sys.exit(0)
