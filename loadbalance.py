#
# FRP Loadbalance Configuration Script
# Author: github.com/Azumi67
# This is for educational use and my own learning, please provide me with feedback if possible
# There maybe some erros , please forgive me as i have worked on it while i was studying.
# This script is designed to simplify the configuration of FRP tunnel and loadbalance.
#
# Tested on: Ubuntu 20, Debian 12
#
# Usage:
#   - Run the script with root privileges.
#   - Follow the on-screen prompts to install, configure, or uninstall the tunnel.
#
#
# Disclaimer:
# This script comes with no warranties or guarantees. Use it at your own risk.
import sys
import os
import time
import colorama
from colorama import Fore, Style
import subprocess
from time import sleep
import readline
import netifaces as ni
import shutil
import signal
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', errors='replace')

if os.geteuid() != 0:
    print("\033[91mThis script must be run as root. Please use sudo -i.\033[0m")
    sys.exit(1)


def display_progress(total, current):
    width = 40
    percentage = current * 100 // total
    completed = width * current // total
    remaining = width - completed

    print('\r[' + '=' * completed + '>' + ' ' * remaining + '] %d%%' % percentage, end='')


def display_checkmark(message):
    print('\u2714 ' + message)


def display_error(message):
    print('\u2718 Error: ' + message)


def display_notification(message):
    print('\u2728 ' + message)


def display_loading():
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    delay = 0.1
    duration = 5  

    end_time = time.time() + duration

    while time.time() < end_time:
        for frame in frames:
            print('\r[' + frame + '] Loading...  ', end='')
            time.sleep(delay)
            print('\r[' + frame + ']             ', end='')
            time.sleep(delay)

def delete_cron7():
    entries_to_delete = [
        "0 * * * * /etc/res.sh",
        "0 */2 * * * /etc/res.sh",
        "0 */3 * * * /etc/res.sh",
        "0 */4 * * * /etc/res.sh",
        "0 */5 * * * /etc/res.sh",
        "0 */6 * * * /etc/res.sh",
        "0 */7 * * * /etc/res.sh",
        "0 */8 * * * /etc/res.sh",
        "0 */9 * * * /etc/res.sh",
        "0 */10 * * * /etc/res.sh",
        "0 */11 * * * /etc/res.sh",
        "0 */12 * * * /etc/res.sh",
        "0 */13 * * * /etc/res.sh",
        "0 */14 * * * /etc/res.sh",
        "0 */15 * * * /etc/res.sh",
        "0 */16 * * * /etc/res.sh",
        "0 */17 * * * /etc/res.sh",
        "0 */18 * * * /etc/res.sh",
        "0 */19 * * * /etc/res.sh",
        "0 */20 * * * /etc/res.sh",
        "0 */21 * * * /etc/res.sh",
        "0 */22 * * * /etc/res.sh",
        "0 */23 * * * /etc/res.sh",
    ]

    existing_crontab = ""
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        display_error("\033[91mNo existing cron found!\033[0m")
        return

    new_crontab = existing_crontab
    for entry in entries_to_delete:
        if entry in existing_crontab:
            new_crontab = new_crontab.replace(entry, "")

    if new_crontab != existing_crontab:
        subprocess.call(f"echo '{new_crontab}' | crontab -", shell=True)
        display_notification("\033[92mDeleting Previous Crons..\033[0m")
    else:
        print("\033[91mNothing Found, moving on..!\033[0m") 

def delete_cron8():
    entries_to_delete = [
        "*/1 * * * * /etc/res.sh",  
        "*/2 * * * * /etc/res.sh",  
        "*/3 * * * * /etc/res.sh",  
        "*/4 * * * * /etc/res.sh",  
        "*/5 * * * * /etc/res.sh",  
        "*/6 * * * * /etc/res.sh",
        "*/7 * * * * /etc/res.sh",
        "*/8 * * * * /etc/res.sh",
        "*/9 * * * * /etc/res.sh",
        "*/10 * * * * /etc/res.sh",  
        "*/11 * * * * /etc/res.sh",  
        "*/12 * * * * /etc/res.sh", 
        "*/13 * * * * /etc/res.sh",
        "*/14 * * * * /etc/res.sh",
        "*/15 * * * * /etc/res.sh",
        "*/16 * * * * /etc/res.sh",
        "*/17 * * * * /etc/res.sh",
        "*/18 * * * * /etc/res.sh",
        "*/19 * * * * /etc/res.sh",
        "*/20 * * * * /etc/res.sh",
        "*/21 * * * * /etc/res.sh",
        "*/22 * * * * /etc/res.sh",
        "*/23 * * * * /etc/res.sh",
        "*/24 * * * * /etc/res.sh",
        "*/25 * * * * /etc/res.sh",
        "*/26 * * * * /etc/res.sh",
        "*/27 * * * * /etc/res.sh",
        "*/28 * * * * /etc/res.sh",
        "*/29 * * * * /etc/res.sh",
        "*/30 * * * * /etc/res.sh",
        "*/31 * * * * /etc/res.sh",
        "*/32 * * * * /etc/res.sh",
        "*/33 * * * * /etc/res.sh",
        "*/34 * * * * /etc/res.sh",
        "*/35 * * * * /etc/res.sh",
        "*/36 * * * * /etc/res.sh",
        "*/37 * * * * /etc/res.sh",
        "*/38 * * * * /etc/res.sh",
        "*/39 * * * * /etc/res.sh",
        "*/40 * * * * /etc/res.sh",
        "*/41 * * * * /etc/res.sh",
        "*/42 * * * * /etc/res.sh",
        "*/43 * * * * /etc/res.sh",
        "*/44 * * * * /etc/res.sh",
        "*/45 * * * * /etc/res.sh",
        "*/46 * * * * /etc/res.sh",
        "*/47 * * * * /etc/res.sh",
        "*/48 * * * * /etc/res.sh",
        "*/49 * * * * /etc/res.sh",
        "*/50 * * * * /etc/res.sh",
        "*/51 * * * * /etc/res.sh",
        "*/52 * * * * /etc/res.sh",
        "*/53 * * * * /etc/res.sh",
        "*/54 * * * * /etc/res.sh",
        "*/55 * * * * /etc/res.sh",
        "*/56 * * * * /etc/res.sh",
        "*/57 * * * * /etc/res.sh",
        "*/58 * * * * /etc/res.sh",
        "*/59 * * * * /etc/res.sh",
        
        
    ]

    existing_crontab = ""
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing cron found!\033[0m")
        return

    new_crontab = existing_crontab
    for entry in entries_to_delete:
        if entry in existing_crontab:
            new_crontab = new_crontab.replace(entry, "")

    if new_crontab != existing_crontab:
        subprocess.call(f"echo '{new_crontab}' | crontab -", shell=True)
        display_notification("\033[92mDeleting Previous Crons..\033[0m")
    else:
        print("\033[91mCron doesn't exist, moving on..!\033[0m")        
	
def delete_cron9():
    entries_to_delete = [
        "0 * * * * /etc/resd.sh",
        "0 */2 * * * /etc/resd.sh",
        "0 */3 * * * /etc/resd.sh",
        "0 */4 * * * /etc/resd.sh",
        "0 */5 * * * /etc/resd.sh",
        "0 */6 * * * /etc/resd.sh",
        "0 */7 * * * /etc/resd.sh",
        "0 */8 * * * /etc/resd.sh",
        "0 */9 * * * /etc/resd.sh",
        "0 */10 * * * /etc/resd.sh",
        "0 */11 * * * /etc/resd.sh",
        "0 */12 * * * /etc/resd.sh",
        "0 */13 * * * /etc/resd.sh",
        "0 */14 * * * /etc/resd.sh",
        "0 */15 * * * /etc/resd.sh",
        "0 */16 * * * /etc/resd.sh",
        "0 */17 * * * /etc/resd.sh",
        "0 */18 * * * /etc/resd.sh",
        "0 */19 * * * /etc/resd.sh",
        "0 */20 * * * /etc/resd.sh",
        "0 */21 * * * /etc/resd.sh",
        "0 */22 * * * /etc/resd.sh",
        "0 */23 * * * /etc/resd.sh",
    ]

    existing_crontab = ""
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        display_error("\033[91mNo existing cron found!\033[0m")
        return

    new_crontab = existing_crontab
    for entry in entries_to_delete:
        if entry in existing_crontab:
            new_crontab = new_crontab.replace(entry, "")

    if new_crontab != existing_crontab:
        subprocess.call(f"echo '{new_crontab}' | crontab -", shell=True)
        display_notification("\033[92mDeleting Previous Crons..\033[0m")
    else:
        print("\033[91mNothing Found, moving on..!\033[0m") 

def delete_cron10():
    entries_to_delete = [
        "*/1 * * * * /etc/resd.sh",  
        "*/2 * * * * /etc/resd.sh",  
        "*/3 * * * * /etc/resd.sh",  
        "*/4 * * * * /etc/resd.sh",  
        "*/5 * * * * /etc/resd.sh",  
        "*/6 * * * * /etc/resd.sh",
        "*/7 * * * * /etc/resd.sh",
        "*/8 * * * * /etc/resd.sh",
        "*/9 * * * * /etc/resd.sh",
        "*/10 * * * * /etc/resd.sh",  
        "*/11 * * * * /etc/resd.sh",  
        "*/12 * * * * /etc/resd.sh", 
        "*/13 * * * * /etc/resd.sh",
        "*/14 * * * * /etc/resd.sh",
        "*/15 * * * * /etc/resd.sh",
        "*/16 * * * * /etc/resd.sh",
        "*/17 * * * * /etc/resd.sh",
        "*/18 * * * * /etc/resd.sh",
        "*/19 * * * * /etc/resd.sh",
        "*/20 * * * * /etc/resd.sh",
        "*/21 * * * * /etc/resd.sh",
        "*/22 * * * * /etc/resd.sh",
        "*/23 * * * * /etc/resd.sh",
        "*/24 * * * * /etc/resd.sh",
        "*/25 * * * * /etc/resd.sh",
        "*/26 * * * * /etc/resd.sh",
        "*/27 * * * * /etc/resd.sh",
        "*/28 * * * * /etc/resd.sh",
        "*/29 * * * * /etc/resd.sh",
        "*/30 * * * * /etc/resd.sh",
        "*/31 * * * * /etc/resd.sh",
        "*/32 * * * * /etc/resd.sh",
        "*/33 * * * * /etc/resd.sh",
        "*/34 * * * * /etc/resd.sh",
        "*/35 * * * * /etc/resd.sh",
        "*/36 * * * * /etc/resd.sh",
        "*/37 * * * * /etc/resd.sh",
        "*/38 * * * * /etc/resd.sh",
        "*/39 * * * * /etc/resd.sh",
        "*/40 * * * * /etc/resd.sh",
        "*/41 * * * * /etc/resd.sh",
        "*/42 * * * * /etc/resd.sh",
        "*/43 * * * * /etc/resd.sh",
        "*/44 * * * * /etc/resd.sh",
        "*/45 * * * * /etc/resd.sh",
        "*/46 * * * * /etc/resd.sh",
        "*/47 * * * * /etc/resd.sh",
        "*/48 * * * * /etc/resd.sh",
        "*/49 * * * * /etc/resd.sh",
        "*/50 * * * * /etc/resd.sh",
        "*/51 * * * * /etc/resd.sh",
        "*/52 * * * * /etc/resd.sh",
        "*/53 * * * * /etc/resd.sh",
        "*/54 * * * * /etc/resd.sh",
        "*/55 * * * * /etc/resd.sh",
        "*/56 * * * * /etc/resd.sh",
        "*/57 * * * * /etc/resd.sh",
        "*/58 * * * * /etc/resd.sh",
        "*/59 * * * * /etc/resd.sh",
        
        
    ]

    existing_crontab = ""
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing cron found!\033[0m")
        return

    new_crontab = existing_crontab
    for entry in entries_to_delete:
        if entry in existing_crontab:
            new_crontab = new_crontab.replace(entry, "")

    if new_crontab != existing_crontab:
        subprocess.call(f"echo '{new_crontab}' | crontab -", shell=True)
        display_notification("\033[92mDeleting Previous Crons..\033[0m")
    else:
        print("\033[91mCron doesn't exist, moving on..!\033[0m")            


def delete_cron11():
    entries_to_delete = [
        "0 * * * * /etc/resq.sh",
        "0 */2 * * * /etc/resq.sh",
        "0 */3 * * * /etc/resq.sh",
        "0 */4 * * * /etc/resq.sh",
        "0 */5 * * * /etc/resq.sh",
        "0 */6 * * * /etc/resq.sh",
        "0 */7 * * * /etc/resq.sh",
        "0 */8 * * * /etc/resq.sh",
        "0 */9 * * * /etc/resq.sh",
        "0 */10 * * * /etc/resq.sh",
        "0 */11 * * * /etc/resq.sh",
        "0 */12 * * * /etc/resq.sh",
        "0 */13 * * * /etc/resq.sh",
        "0 */14 * * * /etc/resq.sh",
        "0 */15 * * * /etc/resq.sh",
        "0 */16 * * * /etc/resq.sh",
        "0 */17 * * * /etc/resq.sh",
        "0 */18 * * * /etc/resq.sh",
        "0 */19 * * * /etc/resq.sh",
        "0 */20 * * * /etc/resq.sh",
        "0 */21 * * * /etc/resq.sh",
        "0 */22 * * * /etc/resq.sh",
        "0 */23 * * * /etc/resq.sh",
    ]

    existing_crontab = ""
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        display_error("\033[91mNo existing cron found!\033[0m")
        return

    new_crontab = existing_crontab
    for entry in entries_to_delete:
        if entry in existing_crontab:
            new_crontab = new_crontab.replace(entry, "")

    if new_crontab != existing_crontab:
        subprocess.call(f"echo '{new_crontab}' | crontab -", shell=True)
        display_notification("\033[92mDeleting Previous Crons..\033[0m")
    else:
        print("\033[91mNothing Found, moving on..!\033[0m")  
		
def delete_cron12():
    entries_to_delete = [
        "*/1 * * * * /etc/resq.sh",  
        "*/2 * * * * /etc/resq.sh",  
        "*/3 * * * * /etc/resq.sh",  
        "*/4 * * * * /etc/resq.sh",  
        "*/5 * * * * /etc/resq.sh",  
        "*/6 * * * * /etc/resq.sh",
        "*/7 * * * * /etc/resq.sh",
        "*/8 * * * * /etc/resq.sh",
        "*/9 * * * * /etc/resq.sh",
        "*/10 * * * * /etc/resq.sh",  
        "*/11 * * * * /etc/resq.sh",  
        "*/12 * * * * /etc/resq.sh", 
        "*/13 * * * * /etc/resq.sh",
        "*/14 * * * * /etc/resq.sh",
        "*/15 * * * * /etc/resq.sh",
        "*/16 * * * * /etc/resq.sh",
        "*/17 * * * * /etc/resq.sh",
        "*/18 * * * * /etc/resq.sh",
        "*/19 * * * * /etc/resq.sh",
        "*/20 * * * * /etc/resq.sh",
        "*/21 * * * * /etc/resq.sh",
        "*/22 * * * * /etc/resq.sh",
        "*/23 * * * * /etc/resq.sh",
        "*/24 * * * * /etc/resq.sh",
        "*/25 * * * * /etc/resq.sh",
        "*/26 * * * * /etc/resq.sh",
        "*/27 * * * * /etc/resq.sh",
        "*/28 * * * * /etc/resq.sh",
        "*/29 * * * * /etc/resq.sh",
        "*/30 * * * * /etc/resq.sh",
        "*/31 * * * * /etc/resq.sh",
        "*/32 * * * * /etc/resq.sh",
        "*/33 * * * * /etc/resq.sh",
        "*/34 * * * * /etc/resq.sh",
        "*/35 * * * * /etc/resq.sh",
        "*/36 * * * * /etc/resq.sh",
        "*/37 * * * * /etc/resq.sh",
        "*/38 * * * * /etc/resq.sh",
        "*/39 * * * * /etc/resq.sh",
        "*/40 * * * * /etc/resq.sh",
        "*/41 * * * * /etc/resq.sh",
        "*/42 * * * * /etc/resq.sh",
        "*/43 * * * * /etc/resq.sh",
        "*/44 * * * * /etc/resq.sh",
        "*/45 * * * * /etc/resq.sh",
        "*/46 * * * * /etc/resq.sh",
        "*/47 * * * * /etc/resq.sh",
        "*/48 * * * * /etc/resq.sh",
        "*/49 * * * * /etc/resq.sh",
        "*/50 * * * * /etc/resq.sh",
        "*/51 * * * * /etc/resq.sh",
        "*/52 * * * * /etc/resq.sh",
        "*/53 * * * * /etc/resq.sh",
        "*/54 * * * * /etc/resq.sh",
        "*/55 * * * * /etc/resq.sh",
        "*/56 * * * * /etc/resq.sh",
        "*/57 * * * * /etc/resq.sh",
        "*/58 * * * * /etc/resq.sh",
        "*/59 * * * * /etc/resq.sh",
        
        
    ]

    existing_crontab = ""
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing cron found!\033[0m")
        return

    new_crontab = existing_crontab
    for entry in entries_to_delete:
        if entry in existing_crontab:
            new_crontab = new_crontab.replace(entry, "")

    if new_crontab != existing_crontab:
        subprocess.call(f"echo '{new_crontab}' | crontab -", shell=True)
        display_notification("\033[92mDeleting Previous Crons..\033[0m")
    else:
        print("\033[91mCron doesn't exist, moving on..!\033[0m") 
              
def display_logo2():
    colorama.init()
    logo2 = colorama.Style.BRIGHT + colorama.Fore.GREEN + """
     _____       _     _      
    / ____|     (_)   | |     
   | |  __ _   _ _  __| | ___ 
   | | |_ | | | | |/ _` |/ _ \\
   | |__| | |_| | | (_| |  __/
    \_____|\__,_|_|\__,_|\___|
""" + colorama.Style.RESET_ALL
    print(logo2)
    
def display_logo():
    colorama.init()  
    logo = """ 
\033[1;96m          
                 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⢀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⡀⠤⠒⠊⠉⠀⠀⠀⠀⠈⠁⠢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀\033[1;93m⠀⢀⠔⠉⠀⠀⠀⠀⢀⡠⠤⠐⠒⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⣀⡠⠤⠤⠀⠀⠂⠐\033[1;96m⠀⠠⢤⠎⢑⡭⣽⣳⠶⣖⡶⣤⣖⣬⡽⡭⣥⣄\033[1;93m⠒⠒⠀⠐⠁⠑⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⢀⠴⠊⠁⠀⠀⠀⠀⡀⠀\033[1;96m⣠⣴⡶⣿⢏⡿⣝⡳⢧⡻⣟⡻⣞⠿⣾⡽⣳⣯⣳⣞⡻⣦⡀⠀⠀\033[1;93m⠀⠈⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⢨⠀⠀⠀⢀⠤⠂⠁\033[1;96m⢠⣾⡟⣧⠿⣝⣮⣽⢺⣝⣳⡽⣎⢷⣫⡟⡵⡿⣵⢫⡷⣾⢷⣭⢻⣦⡄\033[1;93m⠤⡸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠘⡄⠀⠀⠓⠂⠀\033[1;96m⣴⣿⢷⡿⣝⣻⣏⡷⣾⣟⡼⣣⢟⣼⣣⢟⣯⢗⣻⣽⣏⡾⡽⣟⣧⠿⡼⣿⣦\033[1;93m⣃⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⢀⠇⠀⠀⠀⠀\033[1;96m⣼⣿⢿⣼⡻⣼⡟⣼⣧⢿⣿⣸⡧⠿⠃⢿⣜⣻⢿⣤⣛⣿⢧⣻⢻⢿⡿⢧⣛⣿⣧⠀\033[1;93m⠛⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⢸⠁⠀⠀⠀⠀\033[1;96m⣼⣻⡿⣾⣳⡽⣾⣽⡷⣻⣞⢿⣫⠕⣫⣫⣸⢮⣝⡇⠱⣏⣾⣻⡽⣻⣮⣿⣻⡜⣞⡿⣷\033[1;93m⢀⠀⠀⠑⠢⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠘⣧⠀⠀⠀\033[1;96m⣼⣳⢯⣿⣗⣿⣏⣿⠆⣟⣿⣵⢛⣵⡿⣿⣏⣟⡾⣜⣻⠀⢻⡖⣷⢳⣏⡶⣻⡧⣟⡼⣻⡽⣇\033[1;93m⠁⠢⡀⠠⡀⠑⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠈⢦⠀\033[1;96m⣰⣯⣟⢯⣿⢾⣹⢾⡟⠰⣏⡾⣾⣟⡷⣿⣻⣽⣷⡶⣟⠿⡆⠀⢻⣝⣯⢷⣹⢧⣿⢧⡻⣽⣳⢽⡀\033[1;93m⠀⠈⠀⠈⠂⡼⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⡀⢵\033[1;96m⣟⣾⡟⣾⣿⣻⢽⣺⠇⠀⣿⡱⢿⡞⣵⡳⣭⣿⡜⣿⣭⣻⣷⠲⠤⢿⣾⢯⢯⣛⢿⣳⡝⣾⣿⢭⡇⠀\033[1;93m⠀⠀⠀⡰⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⢀⠤⠊⠀\033[1;96m⣼⢻⣿⢞⣯⢿⡽⣸⣹⡆⠀⢷⣏⢯⣿⣧⣛⠶⣯⢿⣽⣷⣧⣛⣦⠀⠀⠙⢿⣳⣽⣿⣣⢟⡶⣿⣫⡇⠀⠀\033[1;93m⠀⠰⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⣠⠖⠁⠀⠀⡄\033[1;96m⡿⣯⣷⣻⡽⣞⡟⣿⣿⣟⠉⠈⢯⣗⣻⣕⢯⣛⡞⣯⢮⣷⣭⡚⠓⠋⠀⠀⠀⠈⠉⣿⡽⣎⠷⡏⡷⣷⠀⠀⠀\033[1;93m⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠐⣇⠀⠀⢀⠊\033[1;96m⣼⣇⣿⡗⣿⣽⣷⡿⣿⣱⡿⣆⠀⠀⠙⠒⠛⠓⠋⠉⠉⠀⠀⠀\033[1;91m⢠⣴⣯⣶⣶⣤⡀\033[1;96m ⠀⣿⣟⡼⣛⡇⣟⣿⡆\033[1;93m⡀⠀⢀⠇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠘⢤⠀⠃⠌\033[1;96m⣸⣿⢾⡽⣹⣾⠹⣞⡵⣳⣽⡽⣖⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;91m⣤⣖⣻⣾⣝⢿⡄\033[1;96m ⢸⣯⢳⣏⡿⣏⣾⢧\033[1;93m⠈⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠘⠀⠈⠀\033[1;96m⡿⣿⣻⡽⣽⣿⢧⠌⠉\033[1;91m⠉⣴⣿⣿⣫⣅⡀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣛⠿⠿⢟⢙⡄⠙\033[1;96m ⠘⣯⢳⣞⡟⣯⢾⣻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⡇⠀⠀⠀\033[1;96m⡿⣿⣿⢵⣫⣿⣆⠁⠂\033[1;91m⣼⡿⢹⣿⡿⠽⠟⢢⠀⠀⠀⠀⠀⠀⠀⢹⠀⢄⢀⠀⡿⠀⠀\033[1;96m ⢰⣯⢷⣺⣏⣯⢻⡽⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⡇⠀⢀⠠\033[1;96m⣿⣿⢾⣛⡶⣽⠈⢓⠀\033[1;91m⢻⠁⢸⠇⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠑⠠⠤⠔⠂⠀⠀\033[1;96m ⢸⣿⢮⣽⠿⣜⣻⡝⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠑⠊⠁\033[1;96m⢠⡷⡇⣿⣿⢼⣹⡀⠀⠑⢄⠀\033[1;91m⠀⠃⠌⣁⠦⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠂⠀⠀\033[1;96m⢀⣿⢾⡝⣾⡽⣺⢽⣹⣽⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣻⢽⣻⡟⣮⣝⡷⢦⣄⣄⣢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣯⢿⡺⣟⢷⡹⢾⣷⡞⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣟⡿⣎⢿⡽⣳⢮⣿⣹⣾⣯⡝⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⠀⠀⠀⠀⣀⣴⡟⣿⢧⣏⢷⡟⣮⠝⢿⣹⣯⡽⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣯⡷⣏⣾⡳⣽⢺⣷⡹⣟⢶⡹⣾⡽⣷⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠔⣾⢯⣷⡇⣿⢳⣎⢿⡞⣽⢦⣼⡽⣧⢻⡽⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣟⢾⡷⣭⣿⢳⣭⢻⣷⡻⣜⣻⡵⣻⡼⣿⠾⠫\033[1;96m⣽⣟⣶⣶⣶⠒⠒⠂⠉⠀\033[1;96m⢸⣽⢺⡷⣷⣯⢗⣮⣟⢾⢧⣻⠼⡿⣿⢣⡟⣼⣆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⣝⣾⢳⢧⣟⡳⣎⣿⣿⣱⢏⣾⣽⣳⠟\033[1;92m⠁⠀⡌⠈\033[1;96m⢹⡯⠟⠛⠀⠀⠀⠀⠀⠈\033[1;96m⣷⢻⣼⣽⣿⡾⣼⣏⣾⣻⡜⣯⣷⢿⣟⣼⡳⣞⣦⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⢿⡸⣎⠿⣾⡏⣷⣉⣷⣿⢹⣎⡿\033[1;92m⠎⡎⠀⠀⠀⡇⠀⣾⠱⡀⠀⠀⠀⠀⠀⠀⠀⠈⣹⠉⡏⠀\033[1;96m⠹⣾⣏⢹⣶⢹⣶⢿⡾⣿⢶⣿⣸⠾⣇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣾⢫⣞⡽⣯⢿⣹⡟⣶⣹⢷⣻\033[1;92m⡷⠊⠀⡜⠀⠀⠀⠀⢱⠀⣿⡀⠈⠢⢀⣀⣀⠠⠄⠒⢈⡏⡰⠀⠀⠀\033[1;96m⠀⣿⡜⣮⢟⡼⣻⡵⣻⣗⠾⣟⣯⢻⣆⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣴⣿⢣⣟⡾⣽⣯⢳⣿⡹⣖⣿⡳\033[1;92m⠋⠀⠀⡸⠀⠀⠀⠀⠀⢸⠀⢺⢂⠀⠀⠀⠀⠀⠀⠀⢠⡺⡱⠁⠀⠀⠀⠀\033[1;96m⢹⣧⣻⢮⡳⣝⡷⢧⣻⢯⢿⣻⣳⢞⡆⠀⠀⠀
⠀⠀⠀⠀⢀⡾⣽⣣⡿⣼⣏⡿⣼⣳⡯⢷⣹⣯⠇\033[1;92m⠀⠀⢠⠁⠀⠀⠀⠀⠀⠈⡆⠈⢹⡰⠤⡀⠀⠀⠀⢠⡼⢱⠁⠀⠀⠀⠀⠀⠀\033[1;96m⠹⣿⣿⣱⣻⣼⣏⢷⣯⣿⡳⣿⣎⢿⡀⠀⠀
⠀⠀⠀⠀⣾⣽⠷⣿⣵⡿⣼⡟⣭⣷⡟⣿⢯⡏⠀\033[1;92m⠀⠀⠘⠀⠀⠒⠈⢡⠀⠀⢗⢄⠀⠃⠀⠺⢁⢈⠥⠋⣀⠇⠀⠀⠀⠀⠀⠀⡀⠀\033[1;96m⠈⠙⢿⣳⢞⣽⢯⣞⣾⣯⡝⣿⡾⡇⠀ ⠀⠀
           \033[96m __    \033[1;94m  ________  \033[1;92m ____  ____ \033[1;93m ___      ___  \033[1;91m __     
      \033[96m     /""\   \033[1;94m ("      "\ \033[1;92m("  _||_ " |\033[1;93m|"  \    /"  | \033[1;91m|" \    
      \033[96m    /    \   \033[1;94m \___/   :)\033[1;92m|   (  ) : |\033[1;93m \   \  //   | \033[1;91m||  |   
      \033[96m   /' /\  \   \033[1;94m  /  ___/ \033[1;92m(:  |  | . )\033[1;93m /\   \/.    |\033[1;91m |:  |   
     \033[96m   //  __'  \  \033[1;94m //  \__  \033[1;92m \  \__/  / \033[1;93m|: \.        | \033[1;91m|.  |   
      \033[96m  /  /  \   \ \033[1;94m(:   / "\ \033[1;92m /\  __  /\ \033[1;93m|.  \    /:  |\033[1;91m /\  |\  
      \033[96m(___/    \___) \033[1;94m\_______)\033[1;92m(__________)\033[1;93m|___|\__/|___|\033[1;91m(__\_|_) \033[1;92mAuthor: github.com/Azumi67  \033[1;96m 
"""
    print(logo)
def main_menu():
    try:
        while True:
            display_logo()
            border = "\033[93m+" + "="*70 + "+\033[0m"
            content = "\033[93m║            ▌║█║▌│║▌│║▌║▌█║ \033[92mMain Menu\033[93m  ▌│║▌║▌│║║▌█║▌                  ║"
            footer = " \033[92m            Join Opiran Telegram \033[34m@https://t.me/OPIranClub\033[0m "

            border_length = len(border) - 2
            centered_content = content.center(border_length)

            print(border)
            print(centered_content)
            print(border)


            print(border)
            print(footer)
            print(border)
            print("0. \033[91mSTATUS Menu\033[0m")
            print("1. \033[96mEdit\033[93m Reset Timer \033[0m")
            print("2. \033[92mInstallation\033[0m")
            print("3. \033[93mFRP TCP Tunnel\033[0m")
            print("4. \033[92mFRP KCP Tunnel\033[0m")
            print("5. \033[93mFRP Quic Tunnel\033[0m")
            print("6. \033[96mLoadBalancer \033[93m[1]\033[36m Kharej \033[93m[1]\033[36m IRAN\033[0m")
            print("7. \033[93mLoadBalancer \033[92m[10]\033[93m Kharej \033[92m[1]\033[93m IRAN\033[0m")
            print("8. \033[92mLoadBalancer \033[93m[1]\033[92m Kharej \033[93m[3]\033[92m IRAN\033[0m")        
            print("9. \033[91mStop\033[93m |\033[92m Restart\033[93m Service \033[0m")
            print("10. \033[91mUninstall\033[0m")
            print("q. Exit")
            print("\033[93m╰─────────────────────────────────────────────────────────────────────╯\033[0m")

            choice = input("\033[5mEnter your choice Please: \033[0m")
            print("choice:", choice)
            if choice == '0':
                status_menu()
            elif choice == '2':
                install_menu()
            elif choice == '3':
                tcp_menu()
            elif choice == '4':
                kcp_local()
            elif choice == '5':
                quic_local()
            elif choice == '6':
                single_load_menu()
            elif choice == '7':
                i3kharej_1iran_load()
            elif choice == '8':
                i1kharej_3iran()
            elif choice == '1':
                timez()
            elif choice == '9':
                start_menu()
            elif choice == '10':
                remove_menu()
            elif choice == 'q':
                print("Exiting...")
                sys.exit()
            else:
                print("Invalid choice.")

            input("Press Enter to continue...")

    except KeyboardInterrupt:
        display_error("\033[91m\nProgram interrupted. Exiting...\033[0m")
        sys.exit()
        
def quic_local():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   )  \033[96m Quic\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mIRAN\033[0m')
    print('2. \033[91mKharej\033[92m [1]\033[0m')
    print('3. \033[93mKharej\033[92m [2]\033[0m')
    print('4. \033[96mKharej\033[92m [3]\033[0m')
    print('5. \033[97mKharej\033[92m [4]\033[0m')
    print('6. \033[93mKharej\033[92m [5]\033[0m')
    print('0. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            iran_quic()
            break
        elif server_type == '2':
            kharej1_quic()
            break
        elif server_type == '3':
            kharej2_quic()
            break
        elif server_type == '4':
            kharej3_quic()
            break
        elif server_type == '5':
            kharej4_quic()
            break
        elif server_type == '6':
            kharej5_quic()
            break
        elif server_type == '0':
            os.system('clear')
            main_menu()
            break
        else:
            print('Invalid choice.') 
            
def iran_quic():            
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIRAN Menu  \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mConfiguring IRAN...\033[0m")
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m") 

    local_ports = input("\033[93mEnter the \033[92mlocal\033[93m ports : \033[0m")
    remote_ports = input("\033[93mEnter the \033[92mremote\033[93m ports : \033[0m")

    local_ports_list = local_ports.replace(" ", ",").split(",")
    remote_ports_list = remote_ports.replace(" ", ",").split(",")

    local_ports_list = [port.strip() for port in local_ports_list]
    remote_ports_list = [port.strip() for port in remote_ports_list]

    num_instances = len(local_ports_list)

    if os.path.exists("frp/frpsq.toml"):
        os.remove("frp/frpsq.toml")

    with open("frp/frpsq.toml", "w") as f:
        f.write("[common]\n")
        kcpbind_port = input("\033[93mEnter \033[92mQuic Port\033[93m: \033[0m")
        f.write("bind_port = {}\n".format(kcpbind_port))
        f.write("quicBindPort = {}\n".format(kcpbind_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m: \033[0m")
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")
        f.write("\n")
        f.write("[v2ray]\n")  
        f.write("type = udp\n")
        f.write("local_port = {}\n".format(",".join(local_ports_list)))
        f.write("remote_port = {}\n".format(",".join(remote_ports_list)))
        f.write("use_encryption = true\n")

    display_checkmark("\033[92mIRAN configuration generated. Yours Truly, Azumi.\033[0m")

    
    service_name = "azumifrps_quic"
    frps_path = "/root/frp/frpsq.toml"

    service_content = f'''[Unit]
Description=frps service
After=network.target

[Service]
ExecStart=/root/frp/./frps -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)
    display_notification("\033[93mStarting FRP service...\033[0m")
    time.sleep(1)
    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    time.sleep(1)
    res_iq()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

def kharej1_quic():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej Server \033[92m[1]\033[93m \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mConfiguring Kharej[1]...\033[0m")
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m")
    
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")

    if os.path.exists("frp/frpcq.toml"):
        os.remove("frp/frpcq.toml")

    with open("frp/frpcq.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mQuic port\033[93m : \033[0m")
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m: \033[0m")
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("transport.protocol = quic\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * 1)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        v2ray_number = starting_v2ray_number

        with open("frp/frpcq.toml", "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(v2ray_number))
            f.write("type = udp\n")
            f.write("local_ip = 127.0.0.1\n")
            f.write("local_port = {}\n".format(local_port))
            f.write("remote_port = {}\n".format(remote_port))
            f.write("group = Azumi{}\n".format(group_number))
            f.write("group_key = azumichwan\n")
            f.write("health_check_type = tcp\n")
            f.write("health_check_timeout_s = 3\n")
            f.write("health_check_max_failed = 3\n")
            f.write("health_check_interval_s = 10\n")
            f.write("use_encryption = true\n")

    time.sleep(1)

    service_name = "azumifrpc_quic"
    frps_path = "/root/frp/frpcq.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_kq()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = len(groups)
    last_v2ray_number = start_number + num_v2ray_instances 

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")

def kharej2_quic():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej Server \033[92m[2]\033[93m \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mConfiguring Kharej[2]...\033[0m")
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m") 
    
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")

    if os.path.exists("frp/frpcq.toml"):
        os.remove("frp/frpcq.toml")
    with open("frp/frpcq.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92m/Quic port\033[93m: \033[0m")
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m: \033[0m")
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("transport.protocol = quic\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * 1)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        v2ray_number = starting_v2ray_number

        with open("frp/frpcq.toml", "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(v2ray_number))
            f.write("type = udp\n")
            f.write("local_ip = 127.0.0.1\n")
            f.write("local_port = {}\n".format(local_port))
            f.write("remote_port = {}\n".format(remote_port))
            f.write("group = Azumi{}\n".format(group_number))
            f.write("group_key = azumichwan\n")
            f.write("health_check_type = tcp\n")
            f.write("health_check_timeout_s = 3\n")
            f.write("health_check_max_failed = 3\n")
            f.write("health_check_interval_s = 10\n")
            f.write("use_encryption = true\n")

    time.sleep(1)

    service_name = "azumifrpc_quic"
    frps_path = "/root/frp/frpcq.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_kq()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = len(groups)
    last_v2ray_number = start_number + num_v2ray_instances 

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")
	
def kharej3_quic():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej Server \033[92m[3]\033[93m \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mConfiguring Kharej[3]...\033[0m")
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m") 
    
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")

    if os.path.exists("frp/frpcq.toml"):
        os.remove("frp/frpcq.toml")

    with open("frp/frpcq.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mQuic port\033[93m: \033[0m")
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m: \033[0m")
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("transport.protocol = quic\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * 1)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        v2ray_number = starting_v2ray_number

        with open("frp/frpcq.toml", "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(v2ray_number))
            f.write("type = udp\n")
            f.write("local_ip = 127.0.0.1\n")
            f.write("local_port = {}\n".format(local_port))
            f.write("remote_port = {}\n".format(remote_port))
            f.write("group = Azumi{}\n".format(group_number))
            f.write("group_key = azumichwan\n")
            f.write("health_check_type = tcp\n")
            f.write("health_check_timeout_s = 3\n")
            f.write("health_check_max_failed = 3\n")
            f.write("health_check_interval_s = 10\n")
            f.write("use_encryption = true\n")

    time.sleep(1)

    service_name = "azumifrpc_quic"
    frps_path = "/root/frp/frpcq.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_kq()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = len(groups)
    last_v2ray_number = start_number + num_v2ray_instances 

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")
	
def kharej4_quic():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej Server \033[92m[4]\033[93m \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mConfiguring Kharej[4]...\033[0m")
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m") 
    
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")

    if os.path.exists("frp/frpcq.toml"):
        os.remove("frp/frpcq.toml")

    with open("frp/frpcq.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92m/Quic port\033[93m: \033[0m")
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m: \033[0m")
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("transport.protocol = quic\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * 1)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        v2ray_number = starting_v2ray_number

        with open("frp/frpcq.toml", "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(v2ray_number))
            f.write("type = udp\n")
            f.write("local_ip = 127.0.0.1\n")
            f.write("local_port = {}\n".format(local_port))
            f.write("remote_port = {}\n".format(remote_port))
            f.write("group = Azumi{}\n".format(group_number))
            f.write("group_key = azumichwan\n")
            f.write("health_check_type = tcp\n")
            f.write("health_check_timeout_s = 3\n")
            f.write("health_check_max_failed = 3\n")
            f.write("health_check_interval_s = 10\n")
            f.write("use_encryption = true\n")

    time.sleep(1)

    service_name = "azumifrpc_quic"
    frps_path = "/root/frp/frpcq.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_kq()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = len(groups)
    last_v2ray_number = start_number + num_v2ray_instances 

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")
	
def kharej5_kcp():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej Server \033[92m[5]\033[93m \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mConfiguring Kharej[5]...\033[0m")
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m") 
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")

    if os.path.exists("frp/frpcq.toml"):
        os.remove("frp/frpcq.toml")

    with open("frp/frpcq.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mQuic port\033[93m: \033[0m")
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m: \033[0m")
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("transport.protocol = quic\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * 1)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        v2ray_number = starting_v2ray_number

        with open("frp/frpcq.toml", "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(v2ray_number))
            f.write("type = udp\n")
            f.write("local_ip = 127.0.0.1\n")
            f.write("local_port = {}\n".format(local_port))
            f.write("remote_port = {}\n".format(remote_port))
            f.write("group = Azumi{}\n".format(group_number))
            f.write("group_key = azumichwan\n")
            f.write("health_check_type = tcp\n")
            f.write("health_check_timeout_s = 3\n")
            f.write("health_check_max_failed = 3\n")
            f.write("health_check_interval_s = 10\n")
            f.write("use_encryption = true\n")

    time.sleep(1)

    service_name = "azumifrpc_quic"
    frps_path = "/root/frp/frpcq.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_kq()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = len(groups)
    last_v2ray_number = start_number + num_v2ray_instances 

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")        
def kcp_local():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92m Kharej \033[96m KCP\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mIRAN\033[0m')
    print('2. \033[91mKharej\033[92m [1]\033[0m')
    print('3. \033[93mKharej\033[92m [2]\033[0m')
    print('4. \033[96mKharej\033[92m [3]\033[0m')
    print('5. \033[97mKharej\033[92m [4]\033[0m')
    print('6. \033[93mKharej\033[92m [5]\033[0m')
    print('0. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            iran_kcp()
            break
        elif server_type == '2':
            kharej1_kcp()
            break
        elif server_type == '3':
            kharej2_kcp()
            break
        elif server_type == '4':
            kharej3_kcp()
            break
        elif server_type == '5':
            kharej4_kcp()
            break
        elif server_type == '6':
            kharej5_kcp()
            break
        elif server_type == '0':
            os.system('clear')
            main_menu()
            break
        else:
            print('Invalid choice.') 
            
def delete_cron5():
    entries_to_delete = [
        "0 * * * * /bin/bash /etc/resq.sh",
        "0 */2 * * * /bin/bash /etc/resq.sh",
        "0 */3 * * * /bin/bash /etc/resq.sh",
        "0 */4 * * * /bin/bash /etc/resq.sh",
        "0 */5 * * * /bin/bash /etc/resq.sh",
        "0 */6 * * * /bin/bash /etc/resq.sh",
        "0 */7 * * * /bin/bash /etc/resq.sh",
        "0 */8 * * * /bin/bash /etc/resq.sh",
        "0 */9 * * * /bin/bash /etc/resq.sh",
        "0 */10 * * * /bin/bash /etc/resq.sh",
        "0 */11 * * * /bin/bash /etc/resq.sh",
        "0 */12 * * * /bin/bash /etc/resq.sh",
        "0 */13 * * * /bin/bash /etc/resq.sh",
        "0 */14 * * * /bin/bash /etc/resq.sh",
        "0 */15 * * * /bin/bash /etc/resq.sh",
        "0 */16 * * * /bin/bash /etc/resq.sh",
        "0 */17 * * * /bin/bash /etc/resq.sh",
        "0 */18 * * * /bin/bash /etc/resq.sh",
        "0 */19 * * * /bin/bash /etc/resq.sh",
        "0 */20 * * * /bin/bash /etc/resq.sh",
        "0 */21 * * * /bin/bash /etc/resq.sh",
        "0 */22 * * * /bin/bash /etc/resq.sh",
        "0 */23 * * * /bin/bash /etc/resq.sh",
    ]

    existing_crontab = ""
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        display_error("\033[91mNo existing cron found!\033[0m")
        return

    new_crontab = existing_crontab
    for entry in entries_to_delete:
        if entry in existing_crontab:
            new_crontab = new_crontab.replace(entry, "")

    if new_crontab != existing_crontab:
        subprocess.call(f"echo '{new_crontab}' | crontab -", shell=True)
        display_notification("\033[92mDeleting Previous Crons..\033[0m")
    else:
        print("\033[91mNothing Found, moving on..!\033[0m")  
        
def delete_cron3():
    entries_to_delete = [
        "0 * * * * /bin/bash /etc/resd.sh",
        "0 */2 * * * /bin/bash /etc/resd.sh",
        "0 */3 * * * /bin/bash /etc/resd.sh",
        "0 */4 * * * /bin/bash /etc/resd.sh",
        "0 */5 * * * /bin/bash /etc/resd.sh",
        "0 */6 * * * /bin/bash /etc/resd.sh",
        "0 */7 * * * /bin/bash /etc/resd.sh",
        "0 */8 * * * /bin/bash /etc/resd.sh",
        "0 */9 * * * /bin/bash /etc/resd.sh",
        "0 */10 * * * /bin/bash /etc/resd.sh",
        "0 */11 * * * /bin/bash /etc/resd.sh",
        "0 */12 * * * /bin/bash /etc/resd.sh",
        "0 */13 * * * /bin/bash /etc/resd.sh",
        "0 */14 * * * /bin/bash /etc/resd.sh",
        "0 */15 * * * /bin/bash /etc/resd.sh",
        "0 */16 * * * /bin/bash /etc/resd.sh",
        "0 */17 * * * /bin/bash /etc/resd.sh",
        "0 */18 * * * /bin/bash /etc/resd.sh",
        "0 */19 * * * /bin/bash /etc/resd.sh",
        "0 */20 * * * /bin/bash /etc/resd.sh",
        "0 */21 * * * /bin/bash /etc/resd.sh",
        "0 */22 * * * /bin/bash /etc/resd.sh",
        "0 */23 * * * /bin/bash /etc/resd.sh",
    ]

    existing_crontab = ""
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        display_error("\033[91mNo existing cron found!\033[0m")
        return

    new_crontab = existing_crontab
    for entry in entries_to_delete:
        if entry in existing_crontab:
            new_crontab = new_crontab.replace(entry, "")

    if new_crontab != existing_crontab:
        subprocess.call(f"echo '{new_crontab}' | crontab -", shell=True)
        display_notification("\033[92mDeleting Previous Crons..\033[0m")
    else:
        print("\033[91mNothing Found, moving on..!\033[0m")             
def delete_cron1():
    entries_to_delete = [
        "0 * * * * /bin/bash /etc/res.sh",
        "0 */2 * * * /bin/bash /etc/res.sh",
        "0 */3 * * * /bin/bash /etc/res.sh",
        "0 */4 * * * /bin/bash /etc/res.sh",
        "0 */5 * * * /bin/bash /etc/res.sh",
        "0 */6 * * * /bin/bash /etc/res.sh",
        "0 */7 * * * /bin/bash /etc/res.sh",
        "0 */8 * * * /bin/bash /etc/res.sh",
        "0 */9 * * * /bin/bash /etc/res.sh",
        "0 */10 * * * /bin/bash /etc/res.sh",
        "0 */11 * * * /bin/bash /etc/res.sh",
        "0 */12 * * * /bin/bash /etc/res.sh",
        "0 */13 * * * /bin/bash /etc/res.sh",
        "0 */14 * * * /bin/bash /etc/res.sh",
        "0 */15 * * * /bin/bash /etc/res.sh",
        "0 */16 * * * /bin/bash /etc/res.sh",
        "0 */17 * * * /bin/bash /etc/res.sh",
        "0 */18 * * * /bin/bash /etc/res.sh",
        "0 */19 * * * /bin/bash /etc/res.sh",
        "0 */20 * * * /bin/bash /etc/res.sh",
        "0 */21 * * * /bin/bash /etc/res.sh",
        "0 */22 * * * /bin/bash /etc/res.sh",
        "0 */23 * * * /bin/bash /etc/res.sh",
    ]

    existing_crontab = ""
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        display_error("\033[91mNo existing cron found!\033[0m")
        return

    new_crontab = existing_crontab
    for entry in entries_to_delete:
        if entry in existing_crontab:
            new_crontab = new_crontab.replace(entry, "")

    if new_crontab != existing_crontab:
        subprocess.call(f"echo '{new_crontab}' | crontab -", shell=True)
        display_notification("\033[92mDeleting Previous Crons..\033[0m")
    else:
        print("\033[91mNothing Found, moving on..!\033[0m") 
        
def timez():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[96mReset Timer\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('1. \033[93mHour \033[0m')
    print('2. \033[92mMinutes \033[0m')
    print('0. \033[34mBack to main menu \033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            hourz()
            break
        elif server_type == '2':
            minutes()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.') 

def hourz():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[96mReset Timer based on Hours \033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('1. \033[93mTCP | Loadbalance \033[0m')
    print('2. \033[96mKCP \033[0m')
    print('3. \033[92mQuic \033[0m')
    print('0. \033[34mBack to main menu \033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            hourz1()
            break
        elif server_type == '2':
            hourz2()
            break
        elif server_type == '3':
            hourz3()
            break
        elif server_type == '0':
            os.system("clear")
            timez()
            break
        else:
            print('Invalid choice.') 

def minutes():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[96mReset Timer based on minutes \033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('1. \033[93mTCP | Loadbalance \033[0m')
    print('2. \033[92mKCP \033[0m')
    print('3. \033[96mQuic \033[0m')
    print('0. \033[34mBack to main menu \033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            minutes1()
            break
        elif server_type == '2':
            minutes2()
            break
        elif server_type == '3':
            minutes3()
            break
        elif server_type == '0':
            os.system("clear")
            timez()
            break
        else:
            print('Invalid choice.') 
            
def hourz1():
    hours = int(input("\033[93mEnter the \033[92mReset Timer\033[93m [in hours]:\033[0m "))
    delete_cron1()
    delete_cron2()

    if hours == 1:
        cron_entry = "0 * * * * /bin/bash /etc/res.sh"
    else:
        cron_entry = f"0 */{hours} * * * /bin/bash /etc/res.sh"

    try:
        process = subprocess.run('crontab -l', shell=True, capture_output=True, text=True)
        existing_crontab = process.stdout

        if existing_crontab.strip() != "":
            new_crontab = f"{existing_crontab.rstrip()}\n{cron_entry}"
        else:
            new_crontab = cron_entry

        new_crontab += '\n'

        process = subprocess.run('crontab -', shell=True, input=new_crontab, text=True, capture_output=True)

        if process.returncode == 0:
            display_checkmark("\033[92mCron entry added successfully!\033[0m")
        else:
            display_error(f"Failed to add cron entry. Error: {process.stderr}")
    except Exception as e:
        display_error(f"Error: {e}") 
        
def hourz2():
    hours = int(input("\033[93mEnter the \033[92mReset Timer\033[93m [in hours]:\033[0m "))
    delete_cron3()
    delete_cron4()

    if hours == 1:
        cron_entry = "0 * * * * /bin/bash /etc/resd.sh"
    else:
        cron_entry = f"0 */{hours} * * * /bin/bash /etc/resd.sh"

    try:
        process = subprocess.run('crontab -l', shell=True, capture_output=True, text=True)
        existing_crontab = process.stdout

        if existing_crontab.strip() != "":
            new_crontab = f"{existing_crontab.rstrip()}\n{cron_entry}"
        else:
            new_crontab = cron_entry

        new_crontab += '\n'

        process = subprocess.run('crontab -', shell=True, input=new_crontab, text=True, capture_output=True)

        if process.returncode == 0:
            display_checkmark("\033[92mCron entry added successfully!\033[0m")
        else:
            display_error(f"Failed to add cron entry. Error: {process.stderr}")
    except Exception as e:
        display_error(f"Error: {e}")
        

        
def hourz3():
    hours = int(input("\033[93mEnter the \033[92mReset Timer\033[93m [in hours]:\033[0m "))
    delete_cron5()
    delete_cron6()

    if hours == 1:
        cron_entry = "0 * * * * /bin/bash /etc/resq.sh"
    else:
        cron_entry = f"0 */{hours} * * * /bin/bash /etc/resq.sh"

    try:
        process = subprocess.run('crontab -l', shell=True, capture_output=True, text=True)
        existing_crontab = process.stdout

        if existing_crontab.strip() != "":
            new_crontab = f"{existing_crontab.rstrip()}\n{cron_entry}"
        else:
            new_crontab = cron_entry

        new_crontab += '\n'

        process = subprocess.run('crontab -', shell=True, input=new_crontab, text=True, capture_output=True)

        if process.returncode == 0:
            display_checkmark("\033[92mCron entry added successfully!\033[0m")
        else:
            display_error(f"Failed to add cron entry. Error: {process.stderr}")
    except Exception as e:
        display_error(f"Error: {e}")
        
def minutes1():
    minutes = int(input("\033[93mEnter the \033[92mReset Timer\033[93m [in minutes]:\033[0m "))
    delete_cron1()
    delete_cron2()

    cron_entry = f"*/{minutes} * * * * /bin/bash /etc/res.sh"

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        existing_crontab = ""

    new_crontab = f"{existing_crontab.rstrip()}\n{cron_entry}\n"

    try:
        subprocess.check_output(f'echo "{new_crontab}" | crontab -', shell=True)
        display_checkmark("\033[92mCron entry added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        display_error(f"Failed to add cron entry. Error: {e}")

def minutes2():
    minutes = int(input("\033[93mEnter the \033[92mReset Timer\033[93m [in minutes]:\033[0m "))
    delete_cron3()
    delete_cron4()

    cron_entry = f"*/{minutes} * * * * /bin/bash /etc/resd.sh"

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing cron found!\033[0m")

    new_crontab = f"{existing_crontab.rstrip()}\n{cron_entry}"
    try:
        subprocess.check_output(f'echo "{new_crontab}" | crontab -', shell=True)
        display_checkmark("\033[92mCron entry added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        display_error(f"Failed to add cron entry. Error: {e}")   
        
def minutes3():
    minutes = int(input("\033[93mEnter the \033[92mReset Timer\033[93m [in minutes]:\033[0m "))
    delete_cron5()
    delete_cron6()

    cron_entry = f"*/{minutes} * * * * /bin/bash /etc/resq.sh"

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing cron found!\033[0m")

    new_crontab = f"{existing_crontab.rstrip()}\n{cron_entry}"
    try:
        subprocess.check_output(f'echo "{new_crontab}" | crontab -', shell=True)
        display_checkmark("\033[92mCron entry added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        display_error(f"Failed to add cron entry. Error: {e}") 

def delete_cron6():
    entries_to_delete = [
        "*/1 * * * * /bin/bash /etc/resq.sh",  
        "*/2 * * * * /bin/bash /etc/resq.sh",  
        "*/3 * * * * /bin/bash /etc/resq.sh",  
        "*/4 * * * * /bin/bash /etc/resq.sh",  
        "*/5 * * * * /bin/bash /etc/resq.sh",  
        "*/6 * * * * /bin/bash /etc/resq.sh",
        "*/7 * * * * /bin/bash /etc/resq.sh",
        "*/8 * * * * /bin/bash /etc/resq.sh",
        "*/9 * * * * /bin/bash /etc/resq.sh",
        "*/10 * * * * /bin/bash /etc/resq.sh",  
        "*/11 * * * * /bin/bash /etc/resq.sh",  
        "*/12 * * * * /bin/bash /etc/resq.sh", 
        "*/13 * * * * /bin/bash /etc/resq.sh",
        "*/14 * * * * /bin/bash /etc/resq.sh",
        "*/15 * * * * /bin/bash /etc/resq.sh",
        "*/16 * * * * /bin/bash /etc/resq.sh",
        "*/17 * * * * /bin/bash /etc/resq.sh",
        "*/18 * * * * /bin/bash /etc/resq.sh",
        "*/19 * * * * /bin/bash /etc/resq.sh",
        "*/20 * * * * /bin/bash /etc/resq.sh",
        "*/21 * * * * /bin/bash /etc/resq.sh",
        "*/22 * * * * /bin/bash /etc/resq.sh",
        "*/23 * * * * /bin/bash /etc/resq.sh",
        "*/24 * * * * /bin/bash /etc/resq.sh",
        "*/25 * * * * /bin/bash /etc/resq.sh",
        "*/26 * * * * /bin/bash /etc/resq.sh",
        "*/27 * * * * /bin/bash /etc/resq.sh",
        "*/28 * * * * /bin/bash /etc/resq.sh",
        "*/29 * * * * /bin/bash /etc/resq.sh",
        "*/30 * * * * /bin/bash /etc/resq.sh",
        "*/31 * * * * /bin/bash /etc/resq.sh",
        "*/32 * * * * /bin/bash /etc/resq.sh",
        "*/33 * * * * /bin/bash /etc/resq.sh",
        "*/34 * * * * /bin/bash /etc/resq.sh",
        "*/35 * * * * /bin/bash /etc/resq.sh",
        "*/36 * * * * /bin/bash /etc/resq.sh",
        "*/37 * * * * /bin/bash /etc/resq.sh",
        "*/38 * * * * /bin/bash /etc/resq.sh",
        "*/39 * * * * /bin/bash /etc/resq.sh",
        "*/40 * * * * /bin/bash /etc/resq.sh",
        "*/41 * * * * /bin/bash /etc/resq.sh",
        "*/42 * * * * /bin/bash /etc/resq.sh",
        "*/43 * * * * /bin/bash /etc/resq.sh",
        "*/44 * * * * /bin/bash /etc/resq.sh",
        "*/45 * * * * /bin/bash /etc/resq.sh",
        "*/46 * * * * /bin/bash /etc/resq.sh",
        "*/47 * * * * /bin/bash /etc/resq.sh",
        "*/48 * * * * /bin/bash /etc/resq.sh",
        "*/49 * * * * /bin/bash /etc/resq.sh",
        "*/50 * * * * /bin/bash /etc/resq.sh",
        "*/51 * * * * /bin/bash /etc/resq.sh",
        "*/52 * * * * /bin/bash /etc/resq.sh",
        "*/53 * * * * /bin/bash /etc/resq.sh",
        "*/54 * * * * /bin/bash /etc/resq.sh",
        "*/55 * * * * /bin/bash /etc/resq.sh",
        "*/56 * * * * /bin/bash /etc/resq.sh",
        "*/57 * * * * /bin/bash /etc/resq.sh",
        "*/58 * * * * /bin/bash /etc/resq.sh",
        "*/59 * * * * /bin/bash /etc/resq.sh",
        
        
    ]

    existing_crontab = ""
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing cron found!\033[0m")
        return

    new_crontab = existing_crontab
    for entry in entries_to_delete:
        if entry in existing_crontab:
            new_crontab = new_crontab.replace(entry, "")

    if new_crontab != existing_crontab:
        subprocess.call(f"echo '{new_crontab}' | crontab -", shell=True)
        display_notification("\033[92mDeleting Previous Crons..\033[0m")
    else:
        print("\033[91mCron doesn't exist, moving on..!\033[0m") 
        
def delete_cron4():
    entries_to_delete = [
        "*/1 * * * * /bin/bash /etc/resd.sh",  
        "*/2 * * * * /bin/bash /etc/resd.sh",  
        "*/3 * * * * /bin/bash /etc/resd.sh",  
        "*/4 * * * * /bin/bash /etc/resd.sh",  
        "*/5 * * * * /bin/bash /etc/resd.sh",  
        "*/6 * * * * /bin/bash /etc/resd.sh",
        "*/7 * * * * /bin/bash /etc/resd.sh",
        "*/8 * * * * /bin/bash /etc/resd.sh",
        "*/9 * * * * /bin/bash /etc/resd.sh",
        "*/10 * * * * /bin/bash /etc/resd.sh",  
        "*/11 * * * * /bin/bash /etc/resd.sh",  
        "*/12 * * * * /bin/bash /etc/resd.sh", 
        "*/13 * * * * /bin/bash /etc/resd.sh",
        "*/14 * * * * /bin/bash /etc/resd.sh",
        "*/15 * * * * /bin/bash /etc/resd.sh",
        "*/16 * * * * /bin/bash /etc/resd.sh",
        "*/17 * * * * /bin/bash /etc/resd.sh",
        "*/18 * * * * /bin/bash /etc/resd.sh",
        "*/19 * * * * /bin/bash /etc/resd.sh",
        "*/20 * * * * /bin/bash /etc/resd.sh",
        "*/21 * * * * /bin/bash /etc/resd.sh",
        "*/22 * * * * /bin/bash /etc/resd.sh",
        "*/23 * * * * /bin/bash /etc/resd.sh",
        "*/24 * * * * /bin/bash /etc/resd.sh",
        "*/25 * * * * /bin/bash /etc/resd.sh",
        "*/26 * * * * /bin/bash /etc/resd.sh",
        "*/27 * * * * /bin/bash /etc/resd.sh",
        "*/28 * * * * /bin/bash /etc/resd.sh",
        "*/29 * * * * /bin/bash /etc/resd.sh",
        "*/30 * * * * /bin/bash /etc/resd.sh",
        "*/31 * * * * /bin/bash /etc/resd.sh",
        "*/32 * * * * /bin/bash /etc/resd.sh",
        "*/33 * * * * /bin/bash /etc/resd.sh",
        "*/34 * * * * /bin/bash /etc/resd.sh",
        "*/35 * * * * /bin/bash /etc/resd.sh",
        "*/36 * * * * /bin/bash /etc/resd.sh",
        "*/37 * * * * /bin/bash /etc/resd.sh",
        "*/38 * * * * /bin/bash /etc/resd.sh",
        "*/39 * * * * /bin/bash /etc/resd.sh",
        "*/40 * * * * /bin/bash /etc/resd.sh",
        "*/41 * * * * /bin/bash /etc/resd.sh",
        "*/42 * * * * /bin/bash /etc/resd.sh",
        "*/43 * * * * /bin/bash /etc/resd.sh",
        "*/44 * * * * /bin/bash /etc/resd.sh",
        "*/45 * * * * /bin/bash /etc/resd.sh",
        "*/46 * * * * /bin/bash /etc/resd.sh",
        "*/47 * * * * /bin/bash /etc/resd.sh",
        "*/48 * * * * /bin/bash /etc/resd.sh",
        "*/49 * * * * /bin/bash /etc/resd.sh",
        "*/50 * * * * /bin/bash /etc/resd.sh",
        "*/51 * * * * /bin/bash /etc/resd.sh",
        "*/52 * * * * /bin/bash /etc/resd.sh",
        "*/53 * * * * /bin/bash /etc/resd.sh",
        "*/54 * * * * /bin/bash /etc/resd.sh",
        "*/55 * * * * /bin/bash /etc/resd.sh",
        "*/56 * * * * /bin/bash /etc/resd.sh",
        "*/57 * * * * /bin/bash /etc/resd.sh",
        "*/58 * * * * /bin/bash /etc/resd.sh",
        "*/59 * * * * /bin/bash /etc/resd.sh",
        
        
    ]

    existing_crontab = ""
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing cron found!\033[0m")
        return

    new_crontab = existing_crontab
    for entry in entries_to_delete:
        if entry in existing_crontab:
            new_crontab = new_crontab.replace(entry, "")

    if new_crontab != existing_crontab:
        subprocess.call(f"echo '{new_crontab}' | crontab -", shell=True)
        display_notification("\033[92mDeleting Previous Crons..\033[0m")
    else:
        print("\033[91mCron doesn't exist, moving on..!\033[0m")            
def delete_cron2():
    entries_to_delete = [
        "*/1 * * * * /bin/bash /etc/res.sh",  
        "*/2 * * * * /bin/bash /etc/res.sh",  
        "*/3 * * * * /bin/bash /etc/res.sh",  
        "*/4 * * * * /bin/bash /etc/res.sh",  
        "*/5 * * * * /bin/bash /etc/res.sh",  
        "*/6 * * * * /bin/bash /etc/res.sh",
        "*/7 * * * * /bin/bash /etc/res.sh",
        "*/8 * * * * /bin/bash /etc/res.sh",
        "*/9 * * * * /bin/bash /etc/res.sh",
        "*/10 * * * * /bin/bash /etc/res.sh",  
        "*/11 * * * * /bin/bash /etc/res.sh",  
        "*/12 * * * * /bin/bash /etc/res.sh", 
        "*/13 * * * * /bin/bash /etc/res.sh",
        "*/14 * * * * /bin/bash /etc/res.sh",
        "*/15 * * * * /bin/bash /etc/res.sh",
        "*/16 * * * * /bin/bash /etc/res.sh",
        "*/17 * * * * /bin/bash /etc/res.sh",
        "*/18 * * * * /bin/bash /etc/res.sh",
        "*/19 * * * * /bin/bash /etc/res.sh",
        "*/20 * * * * /bin/bash /etc/res.sh",
        "*/21 * * * * /bin/bash /etc/res.sh",
        "*/22 * * * * /bin/bash /etc/res.sh",
        "*/23 * * * * /bin/bash /etc/res.sh",
        "*/24 * * * * /bin/bash /etc/res.sh",
        "*/25 * * * * /bin/bash /etc/res.sh",
        "*/26 * * * * /bin/bash /etc/res.sh",
        "*/27 * * * * /bin/bash /etc/res.sh",
        "*/28 * * * * /bin/bash /etc/res.sh",
        "*/29 * * * * /bin/bash /etc/res.sh",
        "*/30 * * * * /bin/bash /etc/res.sh",
        "*/31 * * * * /bin/bash /etc/res.sh",
        "*/32 * * * * /bin/bash /etc/res.sh",
        "*/33 * * * * /bin/bash /etc/res.sh",
        "*/34 * * * * /bin/bash /etc/res.sh",
        "*/35 * * * * /bin/bash /etc/res.sh",
        "*/36 * * * * /bin/bash /etc/res.sh",
        "*/37 * * * * /bin/bash /etc/res.sh",
        "*/38 * * * * /bin/bash /etc/res.sh",
        "*/39 * * * * /bin/bash /etc/res.sh",
        "*/40 * * * * /bin/bash /etc/res.sh",
        "*/41 * * * * /bin/bash /etc/res.sh",
        "*/42 * * * * /bin/bash /etc/res.sh",
        "*/43 * * * * /bin/bash /etc/res.sh",
        "*/44 * * * * /bin/bash /etc/res.sh",
        "*/45 * * * * /bin/bash /etc/res.sh",
        "*/46 * * * * /bin/bash /etc/res.sh",
        "*/47 * * * * /bin/bash /etc/res.sh",
        "*/48 * * * * /bin/bash /etc/res.sh",
        "*/49 * * * * /bin/bash /etc/res.sh",
        "*/50 * * * * /bin/bash /etc/res.sh",
        "*/51 * * * * /bin/bash /etc/res.sh",
        "*/52 * * * * /bin/bash /etc/res.sh",
        "*/53 * * * * /bin/bash /etc/res.sh",
        "*/54 * * * * /bin/bash /etc/res.sh",
        "*/55 * * * * /bin/bash /etc/res.sh",
        "*/56 * * * * /bin/bash /etc/res.sh",
        "*/57 * * * * /bin/bash /etc/res.sh",
        "*/58 * * * * /bin/bash /etc/res.sh",
        "*/59 * * * * /bin/bash /etc/res.sh",
        
        
    ]

    existing_crontab = ""
    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing cron found!\033[0m")
        return

    new_crontab = existing_crontab
    for entry in entries_to_delete:
        if entry in existing_crontab:
            new_crontab = new_crontab.replace(entry, "")

    if new_crontab != existing_crontab:
        subprocess.call(f"echo '{new_crontab}' | crontab -", shell=True)
        display_notification("\033[92mDeleting Previous Crons..\033[0m")
    else:
        print("\033[91mCron doesn't exist, moving on..!\033[0m")          

def res_iq():
    if subprocess.call("test -f /etc/resq.sh", shell=True) == 0:
        subprocess.call("sudo rm /etc/resq.sh", shell=True)

    with open("/etc/resq.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("pids=$(pgrep frps)\n")
        f.write("sudo kill -9 $pids\n")
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart azumifrps_quic\n")
        f.write("sudo journalctl --vacuum-size=1M\n")

    subprocess.call("chmod +x /etc/resq.sh", shell=True)

    existing_entry = "0 * * * * /bin/bash /etc/resq.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing crontab found.\033[0m")

    if existing_entry in existing_crontab:
        print("\033[91mCrontab already exists.\033[0m")
    else:
        new_crontab = existing_crontab.strip() + "\n0 * * * * /bin/bash /etc/resq.sh\n"
        subprocess.call("echo '{}' | crontab -".format(new_crontab), shell=True)
        display_checkmark("\033[92m1 hour reset timer added!\033[0m")

    display_checkmark("\033[92mIT IS DONE.!\033[0m")
	
def res_kq():
    if subprocess.call("test -f /etc/resq.sh", shell=True) == 0:
        subprocess.call("sudo rm /etc/resq.sh", shell=True)

    with open("/etc/resq.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("pids=$(pgrep frpc)\n")
        f.write("sudo kill -9 $pids\n")  
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart azumifrpc_quic\n")
        f.write("sudo journalctl --vacuum-size=1M\n") 

    subprocess.call("chmod +x /etc/resq.sh", shell=True)
    
    existing_entry = "0 * * * * /bin/bash /etc/resq.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing crontab found.\033[0m")

    if existing_entry in existing_crontab:
        print("\033[91mCrontab already exists.\033[0m")
    else:
        new_crontab = existing_crontab.strip() + "\n0 * * * * /bin/bash /etc/resq.sh\n"
        subprocess.call("echo '{}' | crontab -".format(new_crontab), shell=True)
        display_checkmark("\033[92m2 hour reset timer added!\033[0m")

    display_checkmark("\033[92mIT IS DONE.!\033[0m")
    
def res_in():
    if subprocess.call("test -f /etc/resd.sh", shell=True) == 0:
        subprocess.call("sudo rm /etc/resd.sh", shell=True)

    with open("/etc/resd.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("pids=$(pgrep frps)\n")
        f.write("sudo kill -9 $pids\n")
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart azumifrps_KCP\n")
        f.write("sudo journalctl --vacuum-size=1M\n")

    subprocess.call("chmod +x /etc/resd.sh", shell=True)

    existing_entry = "0 * * * * /bin/bash /etc/resd.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing crontab found.\033[0m")

    if existing_entry in existing_crontab:
        print("\033[91mCrontab already exists.\033[0m")
    else:
        new_crontab = existing_crontab.strip() + "\n0 * * * * /bin/bash /etc/resd.sh\n"
        subprocess.call("echo '{}' | crontab -".format(new_crontab), shell=True)
        display_checkmark("\033[92m2 hour reset timer added!\033[0m")

    display_checkmark("\033[92mIT IS DONE.!\033[0m")
	
def res_kn():
    if subprocess.call("test -f /etc/resd.sh", shell=True) == 0:
        subprocess.call("sudo rm /etc/resd.sh", shell=True)

    with open("/etc/resd.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("pids=$(pgrep frpc)\n")
        f.write("sudo kill -9 $pids\n")
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart azumifrpc_KCP\n")
        f.write("sudo journalctl --vacuum-size=1M\n") 

    subprocess.call("chmod +x /etc/resd.sh", shell=True)
    
    existing_entry = "0 * * * * /bin/bash /etc/resd.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing crontab found.\033[0m")

    if existing_entry in existing_crontab:
        print("\033[91mCrontab already exists.\033[0m")
    else:
        new_crontab = existing_crontab.strip() + "\n0 * * * * /bin/bash /etc/resd.sh\n"
        subprocess.call("echo '{}' | crontab -".format(new_crontab), shell=True)
        display_checkmark("\033[92m1 hour reset timer added!\033[0m")

    display_checkmark("\033[92mIT IS DONE.!\033[0m")
	
def iran_kcp():            
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIRAN Menu  \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m") 

    local_ports = input("\033[93mEnter the \033[92mlocal\033[93m ports : \033[0m")
    remote_ports = input("\033[93mEnter the \033[92mremote\033[93m ports : \033[0m")

    local_ports_list = local_ports.replace(" ", ",").split(",")
    remote_ports_list = remote_ports.replace(" ", ",").split(",")

    local_ports_list = [port.strip() for port in local_ports_list]
    remote_ports_list = [port.strip() for port in remote_ports_list]

    num_instances = len(local_ports_list)

    if os.path.exists("frp/frpsd.toml"):
        os.remove("frp/frpsd.toml")

    with open("frp/frpsd.toml", "w") as f:
        f.write("[common]\n")
        kcpbind_port = input("\033[93mEnter \033[92mKCP Port\033[93m: \033[0m")
        f.write("bind_port = {}\n".format(kcpbind_port))
        f.write("kcpBindPort = {}\n".format(kcpbind_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m: \033[0m")
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")
        f.write("\n")
        f.write("[v2ray]\n")  
        f.write("type = tcp\n")
        f.write("local_port = {}\n".format(",".join(local_ports_list)))
        f.write("remote_port = {}\n".format(",".join(remote_ports_list)))
        f.write("use_encryption = true\n")

    display_checkmark("\033[92mIRAN configuration generated. Yours Truly, Azumi.\033[0m")

    
    service_name = "azumifrps_KCP"
    frps_path = "/root/frp/frpsd.toml"

    service_content = f'''[Unit]
Description=frps service
After=network.target

[Service]
ExecStart=/root/frp/./frps -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)
    display_notification("\033[93mStarting FRP service...\033[0m")
    time.sleep(1)
    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    time.sleep(1)
    res_in()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

def kharej1_kcp():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej Server \033[92m[1]\033[93m \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m")
    
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")

    if os.path.exists("frp/frpcd.toml"):
        os.remove("frp/frpcd.toml")

    with open("frp/frpcd.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mKCP port\033[93m : \033[0m")
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m: \033[0m")
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("transport.protocol = kcp\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * 1)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        v2ray_number = starting_v2ray_number

        with open("frp/frpcd.toml", "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(v2ray_number))
            f.write("type = tcp\n")
            f.write("local_ip = 127.0.0.1\n")
            f.write("local_port = {}\n".format(local_port))
            f.write("remote_port = {}\n".format(remote_port))
            f.write("group = Azumi{}\n".format(group_number))
            f.write("group_key = azumichwan\n")
            f.write("health_check_type = tcp\n")
            f.write("health_check_timeout_s = 3\n")
            f.write("health_check_max_failed = 3\n")
            f.write("health_check_interval_s = 10\n")
            f.write("use_encryption = true\n")

    time.sleep(1)

    service_name = "azumifrpc_KCP"
    frps_path = "/root/frp/frpcd.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_kn()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = len(groups)
    last_v2ray_number = start_number + num_v2ray_instances 

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")

def kharej2_kcp():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej Server \033[92m[2]\033[93m \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m") 
    
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")

    if os.path.exists("frp/frpcd.toml"):
        os.remove("frp/frpcd.toml")

    with open("frp/frpcd.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mKCP port\033[93m: \033[0m")
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m: \033[0m")
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("transport.protocol = kcp\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * 1)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        v2ray_number = starting_v2ray_number

        with open("frp/frpcd.toml", "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(v2ray_number))
            f.write("type = tcp\n")
            f.write("local_ip = 127.0.0.1\n")
            f.write("local_port = {}\n".format(local_port))
            f.write("remote_port = {}\n".format(remote_port))
            f.write("group = Azumi{}\n".format(group_number))
            f.write("group_key = azumichwan\n")
            f.write("health_check_type = tcp\n")
            f.write("health_check_timeout_s = 3\n")
            f.write("health_check_max_failed = 3\n")
            f.write("health_check_interval_s = 10\n")
            f.write("use_encryption = true\n")

    time.sleep(1)

    service_name = "azumifrpc_KCP"
    frps_path = "/root/frp/frpcd.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_kn()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = len(groups)
    last_v2ray_number = start_number + num_v2ray_instances 

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")
	
def kharej3_kcp():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej Server \033[92m[3]\033[93m \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m") 
    
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")

    if os.path.exists("frp/frpcd.toml"):
        os.remove("frp/frpcd.toml")

    with open("frp/frpcd.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mKCP port\033[93m: \033[0m")
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m: \033[0m")
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("transport.protocol = kcp\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * 1)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        v2ray_number = starting_v2ray_number

        with open("frp/frpcd.toml", "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(v2ray_number))
            f.write("type = tcp\n")
            f.write("local_ip = 127.0.0.1\n")
            f.write("local_port = {}\n".format(local_port))
            f.write("remote_port = {}\n".format(remote_port))
            f.write("group = Azumi{}\n".format(group_number))
            f.write("group_key = azumichwan\n")
            f.write("health_check_type = tcp\n")
            f.write("health_check_timeout_s = 3\n")
            f.write("health_check_max_failed = 3\n")
            f.write("health_check_interval_s = 10\n")
            f.write("use_encryption = true\n")

    time.sleep(1)

    service_name = "azumifrpc_KCP"
    frps_path = "/root/frp/frpcd.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_kn()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = len(groups)
    last_v2ray_number = start_number + num_v2ray_instances 

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")
	
def kharej4_kcp():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej Server \033[92m[4]\033[93m \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m") 
    
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")

    if os.path.exists("frp/frpcd.toml"):
        os.remove("frp/frpcd.toml")

    with open("frp/frpcd.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mKCP port\033[93m: \033[0m")
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m: \033[0m")
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("transport.protocol = kcp\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * 1)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        v2ray_number = starting_v2ray_number

        with open("frp/frpcd.toml", "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(v2ray_number))
            f.write("type = tcp\n")
            f.write("local_ip = 127.0.0.1\n")
            f.write("local_port = {}\n".format(local_port))
            f.write("remote_port = {}\n".format(remote_port))
            f.write("group = Azumi{}\n".format(group_number))
            f.write("group_key = azumichwan\n")
            f.write("health_check_type = tcp\n")
            f.write("health_check_timeout_s = 3\n")
            f.write("health_check_max_failed = 3\n")
            f.write("health_check_interval_s = 10\n")
            f.write("use_encryption = true\n")

    time.sleep(1)

    service_name = "azumifrpc_KCP"
    frps_path = "/root/frp/frpcd.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_kn()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = len(groups)
    last_v2ray_number = start_number + num_v2ray_instances 

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")
	
def kharej5_kcp():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej Server \033[92m[5]\033[93m \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────\033[0m") 
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")

    if os.path.exists("frp/frpcd.toml"):
        os.remove("frp/frpcd.toml")

    with open("frp/frpcd.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mKCP port\033[93m: \033[0m")
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m: \033[0m")
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("transport.protocol = kcp\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * 1)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        v2ray_number = starting_v2ray_number

        with open("frp/frpcd.toml", "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(v2ray_number))
            f.write("type = tcp\n")
            f.write("local_ip = 127.0.0.1\n")
            f.write("local_port = {}\n".format(local_port))
            f.write("remote_port = {}\n".format(remote_port))
            f.write("group = Azumi{}\n".format(group_number))
            f.write("group_key = azumichwan\n")
            f.write("health_check_type = tcp\n")
            f.write("health_check_timeout_s = 3\n")
            f.write("health_check_max_failed = 3\n")
            f.write("health_check_interval_s = 10\n")
            f.write("use_encryption = true\n")

    time.sleep(1)

    service_name = "azumifrpc_KCP"
    frps_path = "/root/frp/frpcd.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_kn()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = len(groups)
    last_v2ray_number = start_number + num_v2ray_instances 

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")
    
def rmve_cron():
    entries_to_remove = [
        "0 */2 * * * /bin/bash /etc/clear.sh",
        "0 */2 * * * /bin/bash /etc/res.sh"
    ]

    if subprocess.call("test -f /etc/res.sh", shell=True) == 0:
        subprocess.call("rm /etc/res.sh", shell=True)
        
    if subprocess.call("test -f /etc/clear.sh", shell=True) == 0:
        subprocess.call("rm /etc/clear.sh", shell=True)

    existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    modified_crontab = existing_crontab

    for entry in entries_to_remove:
        if entry in modified_crontab:
            modified_crontab = modified_crontab.replace(entry, "")

    if modified_crontab != existing_crontab:
        subprocess.call("echo '{}' | crontab -".format(modified_crontab), shell=True)
        print("\033[92mDone!\033[0m")
    else:
        print("\033[91m\nIt doesn't exist..\033[0m")
	    
def res_tcp():
    if subprocess.call("test -f /etc/res.sh", shell=True) == 0:
        subprocess.call("sudo rm /etc/res.sh", shell=True)

    with open("/etc/res.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("pids=$(pgrep frps)\n")
        f.write("sudo kill -9 $pids\n") 
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart azumifrps1\n")
        f.write("sudo journalctl --vacuum-size=1M\n")  

    subprocess.call("chmod +x /etc/res.sh", shell=True)
    
    existing_entry = "0 * * * * /bin/bash /etc/res.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing crontab found.\033[0m")

    if existing_entry in existing_crontab:
        print("\033[91mCrontab already exists.\033[0m")
    else:
        new_crontab = existing_crontab.strip() + "\n0 * * * * /bin/bash /etc/res.sh\n"
        subprocess.call("echo '{}' | crontab -".format(new_crontab), shell=True)
        display_checkmark("\033[92m1 hour reset timer added!\033[0m")

    display_checkmark("\033[92mIT IS DONE!\033[0m")

def res_tcp2():
    if subprocess.call("test -f /etc/res.sh", shell=True) == 0:
        subprocess.call("sudo rm /etc/res.sh", shell=True)

    with open("/etc/res.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("pids=$(pgrep frpc)\n")
        f.write("sudo kill -9 $pids\n") 
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart azumifrpc1\n")
        f.write("sudo journalctl --vacuum-size=1M\n") 


    subprocess.call("chmod +x /etc/res.sh", shell=True)
    
    existing_entry = "0 * * * * /bin/bash /etc/res.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing crontab found.\033[0m")

    if existing_entry in existing_crontab:
        print("\033[91mCrontab already exists.\033[0m")
    else:
        new_crontab = existing_crontab.strip() + "\n0 * * * * /bin/bash /etc/res.sh\n"
        subprocess.call("echo '{}' | crontab -".format(new_crontab), shell=True)
        display_checkmark("\033[92m1 hour reset timer added!\033[0m")

    display_checkmark("\033[92mIT IS DONE.!\033[0m")
	
def res_li():
    if subprocess.call("test -f /etc/res.sh", shell=True) == 0:
        subprocess.call("sudo rm /etc/res.sh", shell=True)

    with open("/etc/res.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("pids=$(pgrep frps)\n")
        f.write("sudo kill -9 $pids\n") 
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart azumifrps2\n")
        f.write("sudo journalctl --vacuum-size=1M\n") 

    subprocess.call("chmod +x /etc/res.sh", shell=True)
    
    existing_entry = "0 * * * * /bin/bash /etc/res.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing crontab found.\033[0m")

    if existing_entry in existing_crontab:
        print("\033[91mCrontab already exists.\033[0m")
    else:
        new_crontab = existing_crontab.strip() + "\n0 * * * * /bin/bash /etc/res.sh\n"
        subprocess.call("echo '{}' | crontab -".format(new_crontab), shell=True)
        display_checkmark("\033[92m1 hour reset timer added!\033[0m")

    display_checkmark("\033[92mIT IS DONE.!\033[0m")
    
def res_lk():
    if subprocess.call("test -f /etc/res.sh", shell=True) == 0:
        subprocess.call("sudo rm /etc/res.sh", shell=True)

    with open("/etc/res.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("pids=$(pgrep frpc)\n")
        f.write("sudo kill -9 $pids\n")
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart azumifrpc2\n")
        f.write("sudo journalctl --vacuum-size=1M\n") 


    subprocess.call("chmod +x /etc/res.sh", shell=True)
    
    existing_entry = "0 * * * * /bin/bash /etc/res.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing crontab found.\033[0m")

    if existing_entry in existing_crontab:
        print("\033[91mCrontab already exists.\033[0m")
    else:
        new_crontab = existing_crontab.strip() + "\n0 * * * * /bin/bash /etc/res.sh\n"
        subprocess.call("echo '{}' | crontab -".format(new_crontab), shell=True)
        display_checkmark("\033[92m1 hour reset timer added!\033[0m")

    display_checkmark("\033[92mIT IS DONE.!\033[0m")
    
def res_ii3():
    if subprocess.call("test -f /etc/res.sh", shell=True) == 0:
        subprocess.call("sudo rm /etc/res.sh", shell=True)

    with open("/etc/res.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("pids=$(pgrep frps)\n")
        f.write("sudo kill -9 $pids\n")
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart azumifrps4\n")
        f.write("sudo journalctl --vacuum-size=1M\n") 

    subprocess.call("chmod +x /etc/res.sh", shell=True)
    
    existing_entry = "0 * * * * /bin/bash /etc/res.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing crontab found.\033[0m")

    if existing_entry in existing_crontab:
        print("\033[91mCrontab already exists.\033[0m")
    else:
        new_crontab = existing_crontab.strip() + "\n0 * * * * /bin/bash /etc/res.sh\n"
        subprocess.call("echo '{}' | crontab -".format(new_crontab), shell=True)
        display_checkmark("\033[92m1 hour reset timer added!\033[0m")

    display_checkmark("\033[92mIT IS DONE.!\033[0m")
    
def res_ki3():
    if subprocess.call("test -f /etc/res.sh", shell=True) == 0:
        subprocess.call("sudo rm /etc/res.sh", shell=True)

    with open("/etc/res.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("pids=$(pgrep frpc)\n")
        f.write("sudo kill -9 $pids\n")
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart azumifrpc11\n")
        f.write("sudo systemctl restart azumifrpc12\n")
        f.write("sudo systemctl restart azumifrpc13\n")
        f.write("sudo journalctl --vacuum-size=1M\n") 

    subprocess.call("chmod +x /etc/res.sh", shell=True)
    
    existing_entry = "0 * * * * /bin/bash /etc/res.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing crontab found.\033[0m")

    if existing_entry in existing_crontab:
        print("\033[91mCrontab already exists.\033[0m")
    else:
        new_crontab = existing_crontab.strip() + "\n0 * * * * /bin/bash /etc/res.sh\n"
        subprocess.call("echo '{}' | crontab -".format(new_crontab), shell=True)
        display_checkmark("\033[92m1 hour reset timer added!\033[0m")

    display_checkmark("\033[92mIT IS DONE.!\033[0m")
    
def res_k1():
    if subprocess.call("test -f /etc/res.sh", shell=True) == 0:
        subprocess.call("sudo rm /etc/res.sh", shell=True)

    with open("/etc/res.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("pids=$(pgrep frpc)\n")
        f.write("sudo kill -9 $pids\n")
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart azumifrpc3\n")
        f.write("sudo journalctl --vacuum-size=1M\n") 

    subprocess.call("chmod +x /etc/res.sh", shell=True)
    
    existing_entry = "0 * * * * /bin/bash /etc/res.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing crontab found.\033[0m")

    if existing_entry in existing_crontab:
        print("\033[91mCrontab already exists.\033[0m")
    else:
        new_crontab = existing_crontab.strip() + "\n0 * * * * /bin/bash /etc/res.sh\n"
        subprocess.call("echo '{}' | crontab -".format(new_crontab), shell=True)
        display_checkmark("\033[92m1 hour reset timer added!\033[0m")

    display_checkmark("\033[92mIT IS DONE.!\033[0m")
    
def res_k2():
    if subprocess.call("test -f /etc/res.sh", shell=True) == 0:
        subprocess.call("sudo rm /etc/res.sh", shell=True)

    with open("/etc/res.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("pids=$(pgrep frpc)\n")
        f.write("sudo kill -9 $pids\n") 
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart azumifrpc4\n")
        f.write("sudo journalctl --vacuum-size=1M\n") 

    subprocess.call("chmod +x /etc/res.sh", shell=True)
    
    existing_entry = "0 * * * * /bin/bash /etc/res.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing crontab found.\033[0m")

    if existing_entry in existing_crontab:
        print("\033[91mCrontab already exists.\033[0m")
    else:
        new_crontab = existing_crontab.strip() + "\n0 * * * * /bin/bash /etc/res.sh\n"
        subprocess.call("echo '{}' | crontab -".format(new_crontab), shell=True)
        display_checkmark("\033[92m1 hour reset timer added!\033[0m")

    display_checkmark("\033[92mIT IS DONE.!\033[0m")
    
def res_k3():
    if subprocess.call("test -f /etc/res.sh", shell=True) == 0:
        subprocess.call("sudo rm /etc/res.sh", shell=True)

    with open("/etc/res.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("pids=$(pgrep frpc)\n")
        f.write("sudo kill -9 $pids\n")
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart azumifrpc5\n")
        f.write("sudo journalctl --vacuum-size=1M\n") 

    subprocess.call("chmod +x /etc/res.sh", shell=True)
    
    existing_entry = "0 * * * * /bin/bash /etc/res.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing crontab found.\033[0m")

    if existing_entry in existing_crontab:
        print("\033[91mCrontab already exists.\033[0m")
    else:
        new_crontab = existing_crontab.strip() + "\n0 * * * * /bin/bash /etc/res.sh\n"
        subprocess.call("echo '{}' | crontab -".format(new_crontab), shell=True)
        display_checkmark("\033[92m1 hour reset timer added!\033[0m")

    display_checkmark("\033[92mIT IS DONE.!\033[0m")
    
def res_k4():
    if subprocess.call("test -f /etc/res.sh", shell=True) == 0:
        subprocess.call("sudo rm /etc/res.sh", shell=True)

    with open("/etc/res.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("pids=$(pgrep frpc)\n")
        f.write("sudo kill -9 $pids\n") 
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart azumifrpc6\n")
        f.write("sudo journalctl --vacuum-size=1M\n") 

    subprocess.call("chmod +x /etc/res.sh", shell=True)
    
    existing_entry = "0 * * * * /bin/bash /etc/res.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing crontab found.\033[0m")

    if existing_entry in existing_crontab:
        print("\033[91mCrontab already exists.\033[0m")
    else:
        new_crontab = existing_crontab.strip() + "\n0 * * * * /bin/bash /etc/res.sh\n"
        subprocess.call("echo '{}' | crontab -".format(new_crontab), shell=True)
        display_checkmark("\033[92m1 hour reset timer added!\033[0m")

    display_checkmark("\033[92mIT IS DONE.!\033[0m")
    
def res_k5():
    if subprocess.call("test -f /etc/res.sh", shell=True) == 0:
        subprocess.call("sudo rm /etc/res.sh", shell=True)

    with open("/etc/res.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("pids=$(pgrep frpc)\n")
        f.write("sudo kill -9 $pids\n")
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart azumifrpc7\n")
        f.write("sudo journalctl --vacuum-size=1M\n") 

    subprocess.call("chmod +x /etc/res.sh", shell=True)
    
    existing_entry = "0 * * * * /bin/bash /etc/res.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing crontab found.\033[0m")

    if existing_entry in existing_crontab:
        print("\033[91mCrontab already exists.\033[0m")
    else:
        new_crontab = existing_crontab.strip() + "\n0 * * * * /bin/bash /etc/res.sh\n"
        subprocess.call("echo '{}' | crontab -".format(new_crontab), shell=True)
        display_checkmark("\033[92m1 hour reset timer added!\033[0m")

    display_checkmark("\033[92mIT IS DONE.!\033[0m")
    
def res_k6():
    if subprocess.call("test -f /etc/res.sh", shell=True) == 0:
        subprocess.call("sudo rm /etc/res.sh", shell=True)

    with open("/etc/res.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("pids=$(pgrep frpc)\n")
        f.write("sudo kill -9 $pids\n") 
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart azumifrpc8\n")
        f.write("sudo journalctl --vacuum-size=1M\n") 

    subprocess.call("chmod +x /etc/res.sh", shell=True)
    
    existing_entry = "0 * * * * /bin/bash /etc/res.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing crontab found.\033[0m")

    if existing_entry in existing_crontab:
        print("\033[91mCrontab already exists.\033[0m")
    else:
        new_crontab = existing_crontab.strip() + "\n0 * * * * /bin/bash /etc/res.sh\n"
        subprocess.call("echo '{}' | crontab -".format(new_crontab), shell=True)
        display_checkmark("\033[92m1 hour reset timer added!\033[0m")

    display_checkmark("\033[92mIT IS DONE.!\033[0m")
    
def res_k7():
    if subprocess.call("test -f /etc/res.sh", shell=True) == 0:
        subprocess.call("sudo rm /etc/res.sh", shell=True)

    with open("/etc/res.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("pids=$(pgrep frpc)\n")
        f.write("sudo kill -9 $pids\n") 
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart azumifrpc9\n")
        f.write("sudo journalctl --vacuum-size=1M\n")

    subprocess.call("chmod +x /etc/res.sh", shell=True)
    
    existing_entry = "0 * * * * /bin/bash /etc/res.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing crontab found.\033[0m")

    if existing_entry in existing_crontab:
        print("\033[91mCrontab already exists.\033[0m")
    else:
        new_crontab = existing_crontab.strip() + "\n0 * * * * /bin/bash /etc/res.sh\n"
        subprocess.call("echo '{}' | crontab -".format(new_crontab), shell=True)
        display_checkmark("\033[92m1 hour reset timer added!\033[0m")

    display_checkmark("\033[92mIT IS DONE.!\033[0m")
    
def res_k8():
    if subprocess.call("test -f /etc/res.sh", shell=True) == 0:
        subprocess.call("sudo rm /etc/res.sh", shell=True)

    with open("/etc/res.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("pids=$(pgrep frpc)\n")
        f.write("sudo kill -9 $pids\n") 
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart azumifrpc10\n")
        f.write("sudo journalctl --vacuum-size=1M\n")

    subprocess.call("chmod +x /etc/res.sh", shell=True)
    
    existing_entry = "0 * * * * /bin/bash /etc/res.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing crontab found.\033[0m")

    if existing_entry in existing_crontab:
        print("\033[91mCrontab already exists.\033[0m")
    else:
        new_crontab = existing_crontab.strip() + "\n0 * * * * /bin/bash /etc/res.sh\n"
        subprocess.call("echo '{}' | crontab -".format(new_crontab), shell=True)
        display_checkmark("\033[92m1 hour reset timer added!\033[0m")

    display_checkmark("\033[92mIT IS DONE.!\033[0m")
    
def res_k9():
    if subprocess.call("test -f /etc/res.sh", shell=True) == 0:
        subprocess.call("sudo rm /etc/res.sh", shell=True)

    with open("/etc/res.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("pids=$(pgrep frpc)\n")
        f.write("sudo kill -9 $pids\n") 
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart azumifrpc11\n")
        f.write("sudo journalctl --vacuum-size=1M\n")
        
    subprocess.call("chmod +x /etc/res.sh", shell=True)
    
    existing_entry = "0 * * * * /bin/bash /etc/res.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing crontab found.\033[0m")

    if existing_entry in existing_crontab:
        print("\033[91mCrontab already exists.\033[0m")
    else:
        new_crontab = existing_crontab.strip() + "\n0 * * * * /bin/bash /etc/res.sh\n"
        subprocess.call("echo '{}' | crontab -".format(new_crontab), shell=True)
        display_checkmark("\033[92m1 hour reset timer added!\033[0m")

    display_checkmark("\033[92mIT IS DONE.!\033[0m")
    
def res_k10():
    if subprocess.call("test -f /etc/res.sh", shell=True) == 0:
        subprocess.call("sudo rm /etc/res.sh", shell=True)

    with open("/etc/res.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("pids=$(pgrep frpc)\n")
        f.write("sudo kill -9 $pids\n")
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart azumifrpc12\n")
        f.write("sudo journalctl --vacuum-size=1M\n")

    subprocess.call("chmod +x /etc/res.sh", shell=True)

    existing_entry = "0 * * * * /bin/bash /etc/res.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing crontab found.\033[0m")

    if existing_entry in existing_crontab:
        print("\033[91mCrontab already exists.\033[0m")
    else:
        new_crontab = existing_crontab.strip() + "\n0 * * * * /bin/bash /etc/res.sh\n"
        subprocess.call("echo '{}' | crontab -".format(new_crontab), shell=True)
        display_checkmark("\033[92m1 hour reset timer added!\033[0m")

    display_checkmark("\033[92mIT IS DONE.!\033[0m")

def res_i():
    if subprocess.call("test -f /etc/res.sh", shell=True) == 0:
        subprocess.call("sudo rm /etc/res.sh", shell=True)

    with open("/etc/res.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("pids=$(pgrep frps)\n")
        f.write("sudo kill -9 $pids\n")
        f.write("sudo systemctl daemon-reload\n")
        f.write("sudo systemctl restart azumifrps3\n")
        f.write("sudo journalctl --vacuum-size=1M\n")

    subprocess.call("chmod +x /etc/res.sh", shell=True)

    existing_entry = "0 * * * * /bin/bash /etc/res.sh"
    existing_crontab = ""

    try:
        existing_crontab = subprocess.check_output("crontab -l", shell=True).decode()
    except subprocess.CalledProcessError:
        print("\033[91mNo existing crontab found.\033[0m")

    if existing_entry in existing_crontab:
        print("\033[91mCrontab already exists.\033[0m")
    else:
        new_crontab = existing_crontab.strip() + "\n0 * * * * /bin/bash /etc/res.sh\n"
        subprocess.call("echo '{}' | crontab -".format(new_crontab), shell=True)
        display_checkmark("\033[92m1 hour reset timer added!\033[0m")

    display_checkmark("\033[92mIT IS DONE.!\033[0m")
    

    
def clear_c():
    script_path = '/etc/clear.sh'
    command = 'sync; echo 1 > /proc/sys/vm/drop_caches'
    script_content = f'#!/bin/sh\n{command}'

    with open(script_path, 'w') as f:
        f.write(script_content)

    cron_command = f'0 * * * * sh {script_path}'
    os.system(f'(crontab -l | grep -v "{script_path}") | crontab -')
    os.system(f'(crontab -l 2>/dev/null; echo "{cron_command}") | crontab -')
        
        
def start_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mService Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mTCP Tunnel SERVICE \033[0m')
    print('2. \033[93mKCP Tunnel SERVICE \033[0m')
    print('3. \033[96mQuic Tunnel SERVICE \033[0m')
    print('4. \033[93mLoadBalance Single Server SERVICE \033[0m')
    print('5. \033[96mLoadBalance [10] Kharej [1] IRAN SERVICE \033[0m')
    print('6. \033[97mLoadBalance [1] Kharej [3] IRAN SERVICE  \033[0m')
    print('0. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            start_tcp_tunnel()
            break
        elif server_type == '2':
            start_kcp_tunnel()
            break
        elif server_type == '3':
            start_quic_tunnel()
            break
        elif server_type == '4':
            start_single_load()
            break
        elif server_type == '5':
            start_kharej5()
            break
        elif server_type == '6':
            start_kharej1()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')
			
def start_kharej1():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mLoadBalance [1] Kharej [3] IRAN SERVICE \033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mRestart SERVICE \033[0m')
    print('2. \033[93mStop SERVICE \033[0m')
    print('5. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            restart_kharej1()
            break
        elif server_type == '2':
            stop_kharej1()
            break
        elif server_type == '3':
            os.system("clear")
            start_menu()
            break
        else:
            print('Invalid choice.')
            
def start_kharej10():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mLoadBalance [10] Kharej [2] IRAN SERVICE \033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mRestart SERVICE \033[0m')
    print('2. \033[93mStop SERVICE \033[0m')
    print('5. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            restart_kharej10()
            break
        elif server_type == '2':
            stop_kharej10()
            break
        elif server_type == '3':
            os.system("clear")
            start_menu()
            break
        else:
            print('Invalid choice.')            

def restart_kharej10():
    os.system("clear")
    display_notification("\033[93mRestarting LoadBalance [10] Kharej [2] IRAN...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl restart azumifrps3.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl restart azumifrpc12.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl restart azumifrpc11.service > /dev/null 2>&1", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def stop_kharej10():
    os.system("clear")
    display_notification("\033[93mRestarting LoadBalance [10] Kharej [2] IRAN...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl stop azumifrps3.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl stop azumifrpc12.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl stop azumifrpc11.service > /dev/null 2>&1", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def stop_kharej1():
    os.system("clear")
    display_notification("\033[93mRestarting LoadBalance [1] Kharej [3] IRAN...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl stop azumifrps4.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl stop azumifrpc13.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc12.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl stop azumifrpc11.service > /dev/null 2>&1", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def restart_kharej1():
    os.system("clear")
    display_notification("\033[93mRestarting LoadBalance [1] Kharej [3] IRAN...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl restart azumifrps4.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl restart azumifrpc13.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl restart azumifrpc12.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl restart azumifrpc11.service > /dev/null 2>&1", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
		
def start_kharej5():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mLoadBalance [10] Kharej [1] IRAN SERVICE\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mRestart SERVICE \033[0m')
    print('2. \033[93mStop SERVICE \033[0m')
    print('5. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            restart_kharej5()
            break
        elif server_type == '2':
            stop_kharej5()
            break
        elif server_type == '5':
            os.system("clear")
            start_menu()
            break
        else:
            print('Invalid choice.')


def restart_kharej5():
    os.system("clear")
    display_notification("\033[93mRestarting LoadBalance [10] Kharej [1] IRAN...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl restart azumifrpc3.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl restart azumifrpc4.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl restart azumifrpc5.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl restart azumifrpc6.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl restart azumifrpc7.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl restart azumifrpc8.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl restart azumifrpc9.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl restart azumifrpc10.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl restart azumifrpc11.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl restart azumifrpc12.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl restart azumifrpc13.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        
        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
		
def stop_kharej5():
    os.system("clear")
    display_notification("\033[93mStopping LoadBalance [10] Kharej [1] IRAN...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl stop azumifrpc3.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl stop azumifrpc4.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl stop azumifrpc5.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl stop azumifrpc6.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl stop azumifrpc7.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc8.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc9.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc10.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc11.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc12.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc13.service > /dev/null 2>&1", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mStop completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
			
def start_single_load():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mLoadbalance Single Server Service\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mRestart SERVICE \033[0m')
    print('2. \033[93mStop SERVICE \033[0m')
    print('5. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            restart_single_load()
            break
        elif server_type == '2':
            stop_single_load()
            break
        elif server_type == '5':
            os.system("clear")
            start_menu()
            break
        else:
            print('Invalid choice.')

def restart_single_load():
    os.system("clear")
    display_notification("\033[93mRestarting LoadBalance Single Server...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")
    
    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl restart azumifrps2.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl restart azumifrpc2.service > /dev/null 2>&1", shell=True)
        
        print("Progress: ", end="")
        
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration
        
        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)
        
        display_checkmark("\033[92mRestart completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
			
def stop_single_load():
    os.system("clear")
    display_notification("\033[93mStopping LoadBalance Single Server...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")
    
    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl stop azumifrps2.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl stop azumifrpc2.service > /dev/null 2>&1", shell=True)
        
        print("Progress: ", end="")
        
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration
        
        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)
        
        display_checkmark("\033[92mStop completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())

def start_tcp_tunnel():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mTCP Tunnel Service\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mRestart SERVICE \033[0m')
    print('2. \033[93mStop SERVICE \033[0m')
    print('5. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            restart_tcp_tunnel()
            break
        elif server_type == '2':
            stop_tcp_tunnel()
            break
        elif server_type == '5':
            os.system("clear")
            start_menu()
            break
        else:
            print('Invalid choice.')

def restart_tcp_tunnel():
    os.system("clear")
    display_notification("\033[93mRestarting TCP Tunnel Service...\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    
    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl restart azumifrps1.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl restart azumifrpc1.service > /dev/null 2>&1", shell=True)
        
        print("Progress: ", end="")
        
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration
        
        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)
        
        display_checkmark("\033[92mRestart completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())

def stop_tcp_tunnel():
    os.system("clear")
    display_notification("\033[93mStopping TCP Tunnel Service...\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    
    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl stop azumifrps1.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl stop azumifrpc1.service > /dev/null 2>&1", shell=True)
        
        print("Progress: ", end="")
        
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration
        
        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)
        
        display_checkmark("\033[92mStop completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())

def start_kcp_tunnel():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKCP Tunnel Service\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mRestart SERVICE \033[0m')
    print('2. \033[93mStop SERVICE \033[0m')
    print('5. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            restart_kcp_tunnel()
            break
        elif server_type == '2':
            stop_kcp_tunnel()
            break
        elif server_type == '5':
            os.system("clear")
            start_menu()
            break
        else:
            print('Invalid choice.')

def restart_kcp_tunnel():
    os.system("clear")
    display_notification("\033[93mRestarting KCP Tunnel Service...\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    
    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl restart azumifrps_KCP.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl restart azumifrpc_KCP.service > /dev/null 2>&1", shell=True)
        
        print("Progress: ", end="")
        
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration
        
        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)
        
        display_checkmark("\033[92mRestart completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())

def stop_kcp_tunnel():
    os.system("clear")
    display_notification("\033[93mStopping KCP Tunnel Service...\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    
    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl stop azumifrps_KCP.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl stop azumifrpc_KCP.service > /dev/null 2>&1", shell=True)
        
        print("Progress: ", end="")
        
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration
        
        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)
        
        display_checkmark("\033[92mStop completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())

def start_quic_tunnel():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mQuic Tunnel Service\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mRestart SERVICE \033[0m')
    print('2. \033[93mStop SERVICE \033[0m')
    print('5. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            restart_quic_tunnel()
            break
        elif server_type == '2':
            stop_quic_tunnel()
            break
        elif server_type == '5':
            os.system("clear")
            start_menu()
            break
        else:
            print('Invalid choice.')

def restart_quic_tunnel():
    os.system("clear")
    display_notification("\033[93mRestarting Quic Tunnel Service...\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    
    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl restart azumifrps_quic.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl restart azumifrpc_quic.service > /dev/null 2>&1", shell=True)
        
        print("Progress: ", end="")
        
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration
        
        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)
        
        display_checkmark("\033[92mRestart completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())

def stop_quic_tunnel():
    os.system("clear")
    display_notification("\033[93mStopping Quic Tunnel Service...\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    
    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl stop azumifrps_quic.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl stop azumifrpc_quic.service > /dev/null 2>&1", shell=True)
        
        print("Progress: ", end="")
        
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration
        
        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)
        
        display_checkmark("\033[92mStop completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def remove_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mUninstall Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mTCP Tunnel \033[0m')
    print('2. \033[93mKCP Tunnel \033[0m')
    print('3. \033[96mQuic Tunnel \033[0m')
    print('4. \033[93mLoadBalance Single Server \033[0m')
    print('5. \033[96mLoadBalance [10] Kharej [1] IRAN \033[0m')
    print('6. \033[97mLoadBalance [1] Kharej [3] IRAN  \033[0m')
    print('0. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            remove_tcp_tunnel()
            break
        elif server_type == '2':
            remove_kcp_tunnel()
            break
        elif server_type == '3':
            remove_quic_tunnel()
            break
        elif server_type == '4':
            remove_single_load()
            break
        elif server_type == '5':
            remove_kharej5()
            break
        elif server_type == '6':
            remove_kharej1()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')

def remove_tcp_tunnel():
    os.system("clear")
    display_notification("\033[93mRemoving TCP Tunnel...\033[0m")
    delete_cron1()
    delete_cron7()
    delete_cron2()
    delete_cron8()
    print("\033[93m╭───────────────────────────────────────╮\033[0m")

    try:
        if subprocess.call("test -f /root/frp/frpc.toml", shell=True) == 0:
            subprocess.run("rm /root/frp/frpc.toml", shell=True)
        if subprocess.call("test -f /root/frp/frps.toml", shell=True) == 0:
            subprocess.run("rm /root/frp/frps.toml", shell=True)

        time.sleep(1)
        subprocess.run("systemctl disable azumifrps1.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrps1.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrps1.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl disable azumifrpc1.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc1.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc1.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl daemon-reload", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def remove_quic_tunnel():
    os.system("clear")
    display_notification("\033[93mRemoving Quic Tunnel...\033[0m")
    delete_cron5()
    delete_cron11()
    delete_cron6()
    delete_cron12()
    print("\033[93m╭───────────────────────────────────────╮\033[0m")

    try:
        if subprocess.call("test -f /root/frp/frpcq.toml", shell=True) == 0:
            subprocess.run("rm /root/frp/frpcq.toml", shell=True)
        if subprocess.call("test -f /root/frp/frpsq.toml", shell=True) == 0:
            subprocess.run("rm /root/frp/frpsq.toml", shell=True)

        time.sleep(1)
        subprocess.run("systemctl disable azumifrps_quic.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrps_quic.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrps_quic.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl disable azumifrpc_quic.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc_quic.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc_quic.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl daemon-reload", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def remove_kcp_tunnel():
    os.system("clear")
    display_notification("\033[93mRemoving KCP Tunnel...\033[0m")
    delete_cron3()
    delete_cron9()
    delete_cron4()
    delete_cron10()
    print("\033[93m╭───────────────────────────────────────╮\033[0m")

    try:
        if subprocess.call("test -f /root/frp/frpcd.toml", shell=True) == 0:
            subprocess.run("rm /root/frp/frpcd.toml", shell=True)
        if subprocess.call("test -f /root/frp/frpsd.toml", shell=True) == 0:
            subprocess.run("rm /root/frp/frpsd.toml", shell=True)

        time.sleep(1)
        subprocess.run("systemctl disable azumifrps_KCP.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrps_KCP.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrps_KCP.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl disable azumifrpc_KCP.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc_KCP.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc_KCP.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl daemon-reload", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
		
def remove_single_load():
    os.system("clear")
    display_notification("\033[93mRemoving LoadBalance Single Server...\033[0m")
    delete_cron1()
    delete_cron7()
    delete_cron2()
    delete_cron8()
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        if subprocess.call("test -f /root/frp/frpc.toml", shell=True) == 0:
            subprocess.run("rm /root/frp/frpc.toml", shell=True)
        if subprocess.call("test -f /root/frp/frps.toml", shell=True) == 0:
            subprocess.run("rm /root/frp/frps.toml", shell=True)

        time.sleep(1)
        subprocess.run("systemctl disable azumifrps2.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrps2.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrps2.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl disable azumifrpc2.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc2.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc2.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl daemon-reload", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
		
def remove_kharej5():
    os.system("clear")
    display_notification("\033[93mRemoving LoadBalance [10] Kharej [1] IRAN...\033[0m")
    delete_cron1()
    delete_cron7()
    delete_cron2()
    delete_cron8()
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        if subprocess.call("test -f /root/frp/frpc.toml", shell=True) == 0:
            subprocess.run("rm /root/frp/frpc.toml", shell=True)
        if subprocess.call("test -f /root/frp/frps.toml", shell=True) == 0:
            subprocess.run("rm /root/frp/frps.toml", shell=True)

        subprocess.run("systemctl disable azumifrpc3.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc3.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc3.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl disable azumifrpc4.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc4.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc4.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl disable azumifrpc5.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc5.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc5.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl disable azumifrpc6.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc6.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc6.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl disable azumifrpc7.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc7.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc7.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable azumifrpc8.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc8.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc8.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl disable azumifrpc9.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc9.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc9.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl disable azumifrpc10.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc10.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc10.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl disable azumifrpc11.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc11.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc11.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl disable azumifrpc12.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc12.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc12.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable azumifrpc13.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc13.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc13.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl disable azumifrps3.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrps3.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrps3.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable azumifrps4.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrps4.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrps4.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl daemon-reload", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())

def remove_kharej10():
    os.system("clear")
    display_notification("\033[93mRemoving LoadBalance [10] Kharej [2] IRAN...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        if subprocess.call("test -f /root/frp/frpc1.toml", shell=True) == 0:
            subprocess.run("rm /root/frp/frpc1.toml", shell=True)
        if subprocess.call("test -f /root/frp/frpc2.toml", shell=True) == 0:
            subprocess.run("rm /root/frp/frpc2.toml", shell=True)
        if subprocess.call("test -f /root/frp/frps.toml", shell=True) == 0:
            subprocess.run("rm /root/frp/frps.toml", shell=True)

        time.sleep(1)
        subprocess.run("systemctl disable azumifrps3.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrps3.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrps3.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable azumifrps4.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrps4.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrps4.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl disable azumifrpc12.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc12.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc12.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl disable azumifrpc11.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc11.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc11.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl daemon-reload", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
		
def remove_kharej1():
    os.system("clear")
    delete_cron1()
    delete_cron7()
    delete_cron2()
    delete_cron8()
    display_notification("\033[93mRemoving LoadBalance [1] Kharej [3] IRAN...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        if subprocess.call("test -f /root/frp/frpc1.toml", shell=True) == 0:
            subprocess.run("rm /root/frp/frpc1.toml", shell=True)
        if subprocess.call("test -f /root/frp/frpc2.toml", shell=True) == 0:
            subprocess.run("rm /root/frp/frpc2.toml", shell=True)
        if subprocess.call("test -f /root/frp/frpc3.toml", shell=True) == 0:
            subprocess.run("rm /root/frp/frpc3.toml", shell=True)
        if subprocess.call("test -f /root/frp/frps.toml", shell=True) == 0:
            subprocess.run("rm /root/frp/frps.toml", shell=True)

        time.sleep(1)
        subprocess.run("systemctl disable azumifrps3.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrps3.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrps3.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable azumifrps4.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrps4.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrps4.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl disable azumifrpc13.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc13.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc13.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl disable azumifrpc12.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc12.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc12.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl disable azumifrpc11.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc11.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc11.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl daemon-reload", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
    
def display_status(service_name):
    status_output = os.popen(f"systemctl is-active {service_name}").read().strip()
    if status_output == "active":
        status = "\033[92m\u2713 Active\033[0m"
        print("\033[92m╔════════════════════════════════════╗\033[0m")
        print("\033[92m║              FRP Status            ║\033[0m")
        print("\033[92m╠════════════════════════════════════╣\033[0m")
        print("\033[92m \033[0m    Service:      |    ", status, " \033[92m \033[0m")
        print("\033[92m╚════════════════════════════════════╝\033[0m")


def status_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mStatus Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mTCP Tunnel \033[0m')
    print('2. \033[93mKCP Tunnel\033[0m')
    print('3. \033[96mQuic Tunnel \033[0m')
    print('4. \033[93mLoadBalance Single Server \033[0m')
    print('5. \033[96mLoadBalance [10] Kharej [1] IRAN  \033[0m')
    print('6. \033[97mLoadBalance [1] Kharej [3] IRAN  \033[0m')
    print('0. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            status1_menu()
            break
        elif server_type == '2':
            statuskcp_menu()
            break
        elif server_type == '3':
            statusquic_menu()
            break
        elif server_type == '4':
            status2_menu()
            break
        elif server_type == '5':
            status3_menu()
            break
        elif server_type == '6':
            status4_menu()
            break
        elif server_type == '0':
            os.system('clear')
            main_menu()
            break
        else:
            print('Invalid choice.')

def status3_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mStatus Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')

    services = {
        'iran': ['azumifrps3'],
        'kharej': ['azumifrpc3', 'azumifrpc4', 'azumifrpc5', 'azumifrpc6', 'azumifrpc7' , 'azumifrpc8' , 'azumifrpc9' , 'azumifrpc10' , 'azumifrpc11' , 'azumifrpc12' , 'azumifrpc13']
    }

    print("\033[93m╔════════════════════════════════════════════╗\033[0m")
    print("\033[93m║                 \033[92mFRP Status\033[93m                 ║\033[0m")
    print("\033[93m╠════════════════════════════════════════════╣\033[0m")

    for service, service_names in services.items():
        try:
            for service_name in service_names:
                config_service_name = f"{service_name}.service"
                status_output = os.popen(f"systemctl is-active {config_service_name}").read().strip()

                if status_output == "active":
                    status = "\033[92m✓ Active     \033[0m"
                    if service == 'iran':
                        display_name = '\033[93mIRAN Server   \033[0m'
                    elif service == 'kharej':
                        display_name = '\033[93mKharej Service\033[0m'
                    else:
                        display_name = service
                    print(f"\033[93m║\033[0m    {display_name}:   |    {status:<10} \033[93m   ║\033[0m")

        except OSError as e:
            print(f"Error in retrieving status for {service}: {e}")
            continue

    print("\033[93m╚════════════════════════════════════════════╝\033[0m")

def status1_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mStatus Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')

    services = {
        'iran': ['azumifrps1'],
        'kharej': ['azumifrpc1']
    }

    print("\033[93m╔════════════════════════════════════════════╗\033[0m")
    print("\033[93m║                 \033[92mFRP Status\033[93m                 ║\033[0m")
    print("\033[93m╠════════════════════════════════════════════╣\033[0m")

    for service, service_names in services.items():
        try:
            for service_name in service_names:
                config_service_name = f"{service_name}.service"
                status_output = os.popen(f"systemctl is-active {config_service_name}").read().strip()

                if status_output == "active":
                    status = "\033[92m✓ Active     \033[0m"
                    if service == 'iran':
                        display_name = '\033[93mIRAN Server   \033[0m'
                    elif service == 'kharej':
                        display_name = '\033[93mKharej Service\033[0m'
                    else:
                        display_name = service
                    print(f"\033[93m║\033[0m    {display_name}:   |    {status:<10} \033[93m   ║\033[0m")

        except OSError as e:
            print(f"Error in retrieving status for {service}: {e}")
            continue

    print("\033[93m╚════════════════════════════════════════════╝\033[0m")    

def statusquic_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mStatus Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')

    services = {
        'iran': ['azumifrps_quic'],
        'kharej': ['azumifrpc_quic']
    }

    print("\033[93m╔════════════════════════════════════════════╗\033[0m")
    print("\033[93m║                 \033[92mFRP Status\033[93m                 ║\033[0m")
    print("\033[93m╠════════════════════════════════════════════╣\033[0m")

    for service, service_names in services.items():
        try:
            for service_name in service_names:
                config_service_name = f"{service_name}.service"
                status_output = os.popen(f"systemctl is-active {config_service_name}").read().strip()

                if status_output == "active":
                    status = "\033[92m✓ Active     \033[0m"
                    if service == 'iran':
                        display_name = '\033[93mIRAN Server   \033[0m'
                    elif service == 'kharej':
                        display_name = '\033[93mKharej Service\033[0m'
                    else:
                        display_name = service
                    print(f"\033[93m║\033[0m    {display_name}:   |    {status:<10} \033[93m   ║\033[0m")

        except OSError as e:
            print(f"Error in retrieving status for {service}: {e}")
            continue

    print("\033[93m╚════════════════════════════════════════════╝\033[0m")
    
def statuskcp_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mStatus Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')

    services = {
        'iran': ['azumifrps_KCP'],
        'kharej': ['azumifrpc_KCP']
    }

    print("\033[93m╔════════════════════════════════════════════╗\033[0m")
    print("\033[93m║                 \033[92mFRP Status\033[93m                 ║\033[0m")
    print("\033[93m╠════════════════════════════════════════════╣\033[0m")

    for service, service_names in services.items():
        try:
            for service_name in service_names:
                config_service_name = f"{service_name}.service"
                status_output = os.popen(f"systemctl is-active {config_service_name}").read().strip()

                if status_output == "active":
                    status = "\033[92m✓ Active     \033[0m"
                    if service == 'iran':
                        display_name = '\033[93mIRAN Server   \033[0m'
                    elif service == 'kharej':
                        display_name = '\033[93mKharej Service\033[0m'
                    else:
                        display_name = service
                    print(f"\033[93m║\033[0m    {display_name}:   |    {status:<10} \033[93m   ║\033[0m")

        except OSError as e:
            print(f"Error in retrieving status for {service}: {e}")
            continue

    print("\033[93m╚════════════════════════════════════════════╝\033[0m")
	
def status2_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mStatus Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')

    services = {
        'iran': ['azumifrps2'],
        'kharej': ['azumifrpc2']
    }

    print("\033[93m╔════════════════════════════════════════════╗\033[0m")
    print("\033[93m║                 \033[92mFRP Status\033[93m                 ║\033[0m")
    print("\033[93m╠════════════════════════════════════════════╣\033[0m")

    for service, service_names in services.items():
        try:
            for service_name in service_names:
                config_service_name = f"{service_name}.service"
                status_output = os.popen(f"systemctl is-active {config_service_name}").read().strip()

                if status_output == "active":
                    status = "\033[92m✓ Active     \033[0m"
                    if service == 'iran':
                        display_name = '\033[93mIRAN Server   \033[0m'
                    elif service == 'kharej':
                        display_name = '\033[93mKharej Service\033[0m'
                    else:
                        display_name = service
                    print(f"\033[93m║\033[0m    {display_name}:   |    {status:<10} \033[93m   ║\033[0m")

        except OSError as e:
            print(f"Error in retrieving status for {service}: {e}")
            continue

    print("\033[93m╚════════════════════════════════════════════╝\033[0m")
    

def status4_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mStatus Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')

    services = {
        'iran': ['azumifrps4'],
        'kharej': ['azumifrpc11', 'azumifrpc12', 'azumifrpc13']
    }

    print("\033[93m╔════════════════════════════════════════════╗\033[0m")
    print("\033[93m║                 \033[92mFRP Status\033[93m                 ║\033[0m")
    print("\033[93m╠════════════════════════════════════════════╣\033[0m")

    for service, service_names in services.items():
        try:
            for service_name in service_names:
                config_service_name = f"{service_name}.service"
                status_output = os.popen(f"systemctl is-active {config_service_name}").read().strip()

                if status_output == "active":
                    status = "\033[92m✓ Active     \033[0m"
                    if service == 'iran':
                        display_name = '\033[93mIRAN Server   \033[0m'
                    elif service == 'kharej':
                        display_name = '\033[93mKharej Service\033[0m'
                    else:
                        display_name = service
                    print(f"\033[93m║\033[0m    {display_name}:   |    {status:<10} \033[93m   ║\033[0m")

        except OSError as e:
            print(f"Error in retrieving status for {service}: {e}")
            continue

    print("\033[93m╚════════════════════════════════════════════╝\033[0m")

def status6_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mStatus Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')

    services = {
        'iran': ['azumifrps4'],
        'kharej': ['azumifrpc11', 'azumifrpc12']
    }

    print("\033[93m╔════════════════════════════════════════════╗\033[0m")
    print("\033[93m║                 \033[92mFRP Status\033[93m                 ║\033[0m")
    print("\033[93m╠════════════════════════════════════════════╣\033[0m")

    for service, service_names in services.items():
        try:
            for service_name in service_names:
                config_service_name = f"{service_name}.service"
                status_output = os.popen(f"systemctl is-active {config_service_name}").read().strip()

                if status_output == "active":
                    status = "\033[92m✓ Active     \033[0m"
                    if service == 'iran':
                        display_name = '\033[93mIRAN Server   \033[0m'
                    elif service == 'kharej':
                        display_name = '\033[93mKharej Service\033[0m'
                    else:
                        display_name = service
                    print(f"\033[93m║\033[0m    {display_name}:   |    {status:<10} \033[93m   ║\033[0m")

        except OSError as e:
            print(f"Error in retrieving status for {service}: {e}")
            continue

    print("\033[93m╚════════════════════════════════════════════╝\033[0m")

    
def frp_menu():
    def stop_loading():
        display_error("\033[91mInstallation process interrupted.\033[0m")
        exit(1)

    ipv4_forward_status = subprocess.run(["sysctl", "net.ipv4.ip_forward"], capture_output=True, text=True)
    if "net.ipv4.ip_forward = 0" not in ipv4_forward_status.stdout:
        subprocess.run(["sudo", "sysctl", "-w", "net.ipv4.ip_forward=1"])

    ipv6_forward_status = subprocess.run(["sysctl", "net.ipv6.conf.all.forwarding"], capture_output=True, text=True)
    if "net.ipv6.conf.all.forwarding = 0" not in ipv6_forward_status.stdout:
        subprocess.run(["sudo", "sysctl", "-w", "net.ipv6.conf.all.forwarding=1"])


    arch = subprocess.check_output('uname -m', shell=True).decode().strip()

    if arch in ['x86_64', 'amd64']:
        frp_download_url = "https://github.com/fatedier/frp/releases/download/v0.52.3/frp_0.52.3_linux_amd64.tar.gz"
        frp_directory_name = "frp_0.52.3_linux_amd64"
    elif arch in ['aarch64', 'arm64']:
        frp_download_url = "https://github.com/fatedier/frp/releases/download/v0.52.3/frp_0.52.3_linux_arm64.tar.gz"
        frp_directory_name = "frp_0.52.3_linux_arm64"
    else:
        display_error(f"Unsupported CPU architecture: {arch}")
        return

    display_notification("\033[93mDownloading FRP...\033[0m")

    try:
        subprocess.run(['wget', '-O', '/root/frp.tar.gz', frp_download_url], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        display_checkmark("\033[92mFRP downloaded successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        display_error(f"An error occurred while downloading FRP: {str(e)}")
        return

    try:
        subprocess.run(['tar', '-xf', '/root/frp.tar.gz', '-C', '/root'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['rm', '/root/frp.tar.gz'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        display_error(f"An error occurred while extracting the FRP archive: {str(e)}")
        return

    old_dir_path = f'/root/{frp_directory_name}'
    new_dir_path = '/root/frp'

    try:
        if os.path.exists(new_dir_path):
            shutil.rmtree(new_dir_path)
        os.rename(old_dir_path, new_dir_path)
        display_checkmark("\033[92mFRP downloaded and installed successfully!\033[0m")
    except Exception as e:
        display_error(f"An error occurred while moving frp: {str(e)}")
        return

    subprocess.call('sysctl -p &>/dev/null', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    display_checkmark("\033[92mIP forward enabled!\033[0m")
    display_loading()


def install_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mInstall Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_notification("\033[93mInstalling FRP...\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    frp_menu()
      
def tcp_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mTCP Tunnel Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_tcp_menu()
            break
        elif server_type == '2':
            iran_tcp_menu()
            break
        elif server_type == '3':
            os.system('clear')
            main_menu()
            break
        else:
            print('Invalid choice.')
            
def kharej_tcp_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mKharej \033[93mTCP Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  There are two methods to establish a tunnel, either we enter an IPV6 address for each port or we use localIP for each port")
    print("\033[93m  By LocalIP, i mean 127.0.0.1 which will be added automatically for each port")
    print("\033[96m  Method 2 is easier since you don't need to define an IPV6 for each port")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mMethod 1 [IPV6]\033[0m')
    print('2. \033[93mMethod 2 [LocalIP] \033[0m')
    print('3. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_method1()
            break
        elif server_type == '2':
            kharej_method2()
            break
        elif server_type == '3':
            os.system('clear')
            tcp_menu()
            break
        else:
            print('Invalid choice.')
            
def iran_tcp_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mIRAN \033[93mTCP Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Dashboard is for people who want to have means to be able to check the current connections")
    print("\033[93m  Dashboard needs a sub-domain, so if you don't have a sub-domain, please refrain running the dashboard version")
    print("\033[96m  Without dashboard is easier to setup")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mWith Dashboard\033[0m')
    print('2. \033[93mWithout Dashboard \033[0m')
    print('3. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            iran_tcp_dashboard()
            break
        elif server_type == '2':
            iran_tcp_no_dashboard()
            break
        elif server_type == '3':
            os.system('clear')
            tcp_menu()
            break
        else:
            print('Invalid choice.')
        
def kharej_method1():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mKharej \033[93mMethod\033[92m [1]\033[93m TCP Tunnel \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For every config | port, there will be an IPV6 address")
    print("\033[93m  If you have 3 different configs with different ports, enter an IPV6 address for each one of them")
    print("\033[96m  Enter Local and Remote Port, in TCP tunnel you can enter the same port for local and remote")
    print("\033[97m  Enter Local and Remote Port, in TCP tunnel you can enter the same port for local and remote")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────────╮")
    
    frpc_ini_path = "frp/frpc.toml"
    
    if os.path.exists(frpc_ini_path):
        os.remove(frpc_ini_path)
    
    num_ipv6 = int(input("\033[93mEnter the Number of \033[92mConfigs [IPV6]\033[93m : \033[0m"))
    time.sleep(1)
    display_notification("\033[93mGenerating...\033[0m")

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPv6 address: \033[0m")

    with open(frpc_ini_path, "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m (default 443): \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        f.write("authentication_mode = token\n")
        f.write("token = azumi\n")


    for i in range(1, num_ipv6 + 1):
        kharej_ipv6 = input("\033[93mEnter \033[92m{}th Kharej \033[93m IPv6 address: \033[0m".format(i))
        kharej_port = input("\033[93mEnter \033[92mLocal port\033[93m: \033[0m")
        iran_port = input("\033[93mEnter \033[92mRemote port\033[93m: \033[0m")
        print("\033[93m──────────────────────────────────────────────────────────\033[0m")

        with open(frpc_ini_path, "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(i))
            f.write("type = tcp\n")
            f.write("local_port = {}\n".format(kharej_port))
            f.write("remote_port = {}\n".format(iran_port))
            f.write("local_ip{} = {}\n".format(i, kharej_ipv6))
            f.write("use_encryption = true\n")
            f.write("use_compression = true\n")


    display_checkmark("\033[92mKharej configuration generated. Yours Truly, Azumi.\033[0m")

    with open("/etc/systemd/system/azumifrpc1.service", "w") as f:
        f.write("[Unit]\n")
        f.write("Description=frpc service\n")
        f.write("After=network.target\n")
        f.write("\n")
        f.write("[Service]\n")
        f.write("ExecStart=/root/frp/./frpc -c /root/frp/frpc.toml\n")
        f.write("Restart=always\n")
        f.write("RestartSec=5\n") 
        f.write("LimitNOFILE=1048576\n")     
        f.write("User=root\n")
        f.write("\n")
        f.write("[Install]\n")
        f.write("WantedBy=multi-user.target\n")
        
    time.sleep(1)
    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/azumifrpc1.service")
    os.system("systemctl enable azumifrpc1")
    display_notification("\033[93mStarting FRP service...\033[0m")
    os.system("systemctl restart azumifrpc1")
    res_tcp2()
    display_checkmark("\033[92mFRP Service Started!\033[0m")    

def kharej_method2():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mKharej \033[93mMethod\033[92m [2]\033[93m TCP Tunnel \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭─────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  In this method, you don't need to enter any IPV6 any more, we use local_ip instead for each port | Config")
    print("\033[93m  Instead, if you have different configs with different ports, just specify how many configs you have")
    print("\033[96m  Based on that input, it will automatically add local_ip for each config | ports")
    print("\033[93m╰─────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")

    frpc_ini_path = "frp/frpc.toml"

    if os.path.exists(frpc_ini_path):
        os.remove(frpc_ini_path)
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    display_notification("\033[93mIF YOU WANT TO TUNNEL ONLY 1 CONFIG, ENTER [1], IF YOU WANT TO TUNNEL MULTIPLE CONFIGS, ENTER 2 OR 3 OR MORE\033[0m")
    num_ports = int(input("\033[93mHow many \033[92mconfigs\033[93m do you have?: \033[0m"))
    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")
    

    with open(frpc_ini_path, "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m (default 443): \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        f.write("authentication_mode = token\n")
        f.write("token = azumi\n")

    for i in range(1, num_ports + 1):
        kharej_port = input("\033[93mEnter \033[92mLocal \033[93mport for \033[92mConfig {}\033[93m: \033[0m".format(i))
        iran_port = input("\033[93mEnter \033[92mRemote \033[93mport for \033[92mConfig {}\033[93m: \033[0m".format(i))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────────────────────────\033[0m")

        with open(frpc_ini_path, "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(i))
            f.write("type = tcp\n")
            f.write("local_port = {}\n".format(kharej_port))
            f.write("remote_port = {}\n".format(iran_port))
            f.write("local_ip = 127.0.0.1\n")
            f.write("use_encryption = true\n")
            f.write("use_compression = true\n")
        

    display_checkmark("\033[92mKharej configuration generated. Yours Truly, Azumi.\033[0m")

    with open("/etc/systemd/system/azumifrpc1.service", "w") as f:
        f.write("[Unit]\n")
        f.write("Description=frpc service\n")
        f.write("After=network.target\n")
        f.write("\n")
        f.write("[Service]\n")
        f.write("ExecStart=/root/frp/./frpc -c /root/frp/frpc.toml\n")
        f.write("Restart=always\n")
        f.write("RestartSec=5\n")
        f.write("LimitNOFILE=1048576\n")
        f.write("User=root\n")
        f.write("\n")
        f.write("[Install]\n")
        f.write("WantedBy=multi-user.target\n")



    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/azumifrpc1.service")
    os.system("systemctl enable azumifrpc1")
    display_notification("\033[93mStarting FRP service...\033[0m")
    os.system("systemctl restart azumifrpc1")
    res_tcp2()
    display_checkmark("\033[92mFRP Service Started!\033[0m") 
    
def create_decorated_box(message):
    line = "\033[92m+" + "=" * (len(message) + 2) + "+\033[0m"
    print(line)
    print("\033[92m| " + message + " |\033[0m")
    print(line)
	
def iran_tcp_no_dashboard():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mIRAN \033[93mwithout Dashboard \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  This doesn't have any Dashboard, so it's easier to set up")
    print("\033[93m  You should always configure the IRAN server first and then Kharej")
    print("\033[96m  Enter local and remote ports")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────────╮")
    local_ports = input("\033[93mEnter the \033[92mlocal\033[93m ports (\033[0mcomma-separated\033[93m): \033[0m")
    remote_ports = input("\033[93mEnter the \033[92mremote\033[93m ports (\033[0mcomma-separated\033[93m): \033[0m")

    local_ports_list = local_ports.replace(" ", "").split(",")
    remote_ports_list = remote_ports.replace(" ", "").split(",")
    print("\033[93m╰─────────────────────────────────────────────────────────────╯\033[0m")

    num_instances = len(local_ports_list)

    if os.path.exists("frp/frps.toml"):
        os.remove("frp/frps.toml")
    

    with open("frp/frps.toml", "w") as f:
        f.write("[common]\n")
        bind_port = input("\033[93mEnter \033[92mTunnel Port\033[93m (default 443): \033[0m")
        if not bind_port:
            bind_port = "443"
        f.write("bind_port = {}\n".format(bind_port))
        f.write("token = azumi\n")
        f.write("\n")
        for i in range(num_instances):
            f.write("[v2ray{}]\n".format(i+1))
            f.write("type = tcp\n")
            f.write("local_port = {}\n".format(local_ports_list[i]))
            f.write("remote_port = {}\n".format(remote_ports_list[i]))
            f.write("use_encryption = true\n")
            f.write("use_compression = true\n")
            f.write("\n")


    display_checkmark("\033[92mIRAN configuration generated. Yours Truly, Azumi.\033[0m")

    service_name = "azumifrps1"
    frps_path = "/root/frp/frps.toml"

    service_content = f'''[Unit]
Description=frps service
After=network.target

[Service]
ExecStart=/root/frp/./frps -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)
        
    

    display_notification("\033[93mStarting FRP service...\033[0m")
    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_tcp()
    display_checkmark("\033[92mFRP Service Started!\033[0m")


def stop_loading(load_bar_id):
    subprocess.run(['kill', str(load_bar_id)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
def iran_tcp_dashboard():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mWith Dashboard\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For Dashboard, You need to have a sub-domain with correct DNS Record")
    print("\033[93m  Enter your desired Dashboard Username & Password and Port")
    print("\033[96m  The rest of the configuration is the same as without the dashboard configuration.")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭──────────────────────────────────────────────────────────────────────────────────────╮")
    domain = input("\033[93mEnter your \033[92mSub-Domain\033[93m: [Better to make sure port 80 is available] \033[0m")
    email = input("\033[93mEnter your \033[92mEmail\033[93m: \033[0m")

    display_notification("\033[93mInstalling Certbot...\033[0m")
    loading_bar_pid = None

    try:
        loading_bar_pid = subprocess.Popen(
            ['bash', '-c', 'while true; do echo -ne "\e[93mInstalling Certbot, gimme a sec: [\\] \r\e[0m"; sleep 0.1; echo -ne "\e[93mInstalling Certbot, gimme a sec: [|] \r\e[0m"; sleep 0.1; echo -ne "\e[93mInstalling Certbot, gimme a sec: [/] \r\e[0m"; sleep 0.1; echo -ne "\e[93mInstalling Certbot, gimme a sec: [-] \r\e[0m"; sleep 0.1; done'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        ).pid

        subprocess.run(['apt', 'install', 'certbot', '-y'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        stop_loading(loading_bar_pid)

        display_notification("\033[93mChecking port 80 availability...\033[0m")
        pid = subprocess.run(['lsof', '-t', '-i', ':80'], capture_output=True, text=True).stdout.strip()
        if pid:
            print(f"\033[93mPort 80 is in use by process with ID [{pid}]. Stopping the process...\033[0m")
            subprocess.run(['sudo', 'kill', pid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        display_notification(f"\033[93mStarting Certbot for your \033[92mDomain {domain}\033[0m")
        subprocess.run(['sudo', 'certbot', 'certonly', '--standalone', '--preferred-challenges', 'http', '--agree-tos', '--email', email, '-d', domain])

        stop_loading(loading_bar_pid)
        
        display_notification("\033[93mFor multiple ports, use commas , (no space) eg : 8080,8081\033[0m")
        kharej_v2ray_port = input("\033[93mEnter \033[92mLocal\033[93m port:\033[0m ")
        iran_v2ray_port = input("\033[93mEnter \033[92mremote\033[93m port:\033[0m ")
        dashboard_user = input("\033[93mEnter the \033[92mDashboard username\033[93m: \033[0m")
        dashboard_pwd = input("\033[93mEnter the \033[92mDashboard password\033[93m: \033[0m")
        dashboard_port = input("\033[93mEnter the \033[92mDashboard port\033[93m: \033[0m")
        bind_port = input("\033[93mEnter \033[92mTunnel port\033[93m (default 443): \033[0m")
        if not bind_port:
           bind_port = "443"
        print("\033[93m───────────────────────────────────────────────────────────────────────────────\033[0m")

        with open('frp/frps.toml', 'w') as frps_ini:
            frps_ini.write(f'''[common]
bind_port = {bind_port}
token = azumi
dashboard_port = {dashboard_port}
dashboard_user = {dashboard_user}
dashboard_pwd = {dashboard_pwd}
dashboard_tls_mode = true
dashboard_tls_cert_file = /etc/letsencrypt/live/{domain}/fullchain.pem
dashboard_tls_key_file = /etc/letsencrypt/live/{domain}/privkey.pem

[v2ray]
type = tcp
local_ip = 127.0.0.1
local_port = {iran_v2ray_port}
remote_port = {kharej_v2ray_port}
use_encryption = true
use_compression = true
''')

        service_name = "azumifrps1"
        frps_path = "/root/frp/frps.toml"

        service_content = f'''[Unit]
Description=frps service
After=network.target

[Service]
ExecStart=/root/frp/./frps -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

        service_path = "/etc/systemd/system/{}.service".format(service_name)

        with open(service_path, 'w') as service_file:
            service_file.write(service_content)

        display_checkmark("\033[92mIran configuration With Dashboard generated. Yours Truly, Azumi!\033[0m")
        time.sleep(1)

        subprocess.run(['systemctl', 'start', 'nginx'], check=True)
        subprocess.run(['systemctl', 'daemon-reload'], check=True)
        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)
        subprocess.run(['systemctl', 'enable', service_name], check=True)
        subprocess.run(['systemctl', 'restart', service_name], check=True)
        res_tcp()
        display_checkmark("\033[92mFRP Service Started!\033[0m")
        
        time.sleep(1)
        create_decorated_box("Your Dashboard Address: https://{}:{}".format(domain, dashboard_port))
        create_decorated_box("Username: {}".format(dashboard_user))
        create_decorated_box("Password: {}".format(dashboard_pwd))

    except Exception as e:
        print("\033[91mAn error occurred while setting up Iran - With Dashboard.\033[0m")
        print(f"Error Details: {str(e)}")

        if loading_bar_pid:
            stop_loading(loading_bar_pid)



        print("\033[91mSetup failed. Please try again.\033[0m")

    
def single_load_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mLoadbalance \033[92m[1] \033[96mKharej \033[92m[1] \033[96mIRAN Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_single_load()
            break
        elif server_type == '2':
            iran_single_load()
            break
        elif server_type == '3':
            os.system('clear')
            main_menu()
            break
        else:
            print('Invalid choice.')
            
          
def kharej_single_load():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mKharej \033[93mLoadbalance Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  There are two methods to establish a tunnel, either we enter an IPV6 address for each port or we use local_ip for each port")
    print("\033[93m  By Local_ip, i mean 127.0.0.1 which will be added automatically for each port")
    print("\033[96m  Method 2 is easier since you don't need to define an IPV6 for each port")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mMethod(1)[IPV6]\033[0m')
    print('2. \033[93mMethod(2)[Local-IP]\033[0m')
    print('3. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_load_ipv6()
            break
        elif server_type == '2':
            kharej_load_local()
            break
        elif server_type == '3':
            os.system('clear')
            single_load_menu()
            break
        else:
            print('Invalid choice.')
            
def kharej_load_local():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mKharej \033[93mMethod\033[92m [2]\033[93m Loadbalance \033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  In this method, you don't need to enter any IPV6 any more, we use local_ip instead for each port | Config")
    print("\033[93m  Instead, if you have different configs with different ports, just specify how many loadbalance groups you want for loadbalancing")
    print("\033[96m  Based on that input, it will automatically add local_ip for each config | ports")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮")

    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mload balance groups[\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input. Please enter a valid number\033[0m")
            
    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name, "ipv6_addresses": []}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m (default 443): \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        f.write("token = azumi\n")

    starting_v2ray_number = 1  

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        group_number = group_index + 1

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────\033[0m")


        for i in range(1):  
            v2ray_number = starting_v2ray_number

            with open("frp/frpc.toml", "a") as f:
                f.write("\n")
                f.write("[v2ray{}]\n".format(v2ray_number))
                f.write("type = tcp\n")
                f.write("local_ip = 127.0.0.1\n")
                f.write("local_port = {}\n".format(local_port))
                f.write("remote_port = {}\n".format(remote_port))
                f.write("group = Azumi{}\n".format(group_number))
                f.write("group_key = azumichwan\n")
                f.write("health_check_type = tcp\n")
                f.write("health_check_timeout_s = 3\n")
                f.write("health_check_max_failed = 3\n")
                f.write("health_check_interval_s = 10\n")
                f.write("use_encryption = true\n")
                f.write("use_compression = true\n")

            starting_v2ray_number += 1  

    time.sleep(1)

    service_name = "azumifrpc2"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_lk()
    display_checkmark("\033[92mFRP Service Started!\033[0m")




def kharej_load_ipv6():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mKharej \033[93mMethod\033[92m[1]\033[93m Loadbalance \033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════════════\033[0m')

    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  In this method, you need to enter an IPV6 for each port | Config")
    print("\033[93m  If you have different configs with different ports, first specify how many loadbalance groups you want")
    print("\033[96m  Then based on that input, you enter different IPV6 for each port")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮")

    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mload balance groups[\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input. Please enter a valid number\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)

        while True:
            try:
                num_ipv6 = int(input("\033[93mEnter the number of \033[92mKharej IPv6 addresses\033[93m needed for \033[92m{}\033[93m: \033[0m".format(group_name)))
                break
            except ValueError:
                print("\033[91mInvalid input. Please enter a valid number\033[0m")

        group = {"name": group_name, "num_ipv6": num_ipv6, "ipv6_addresses": []}
        groups.append(group)

    time.sleep(1)
    print("configuring...")

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m (default 443): \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        f.write("token = azumi\n")

    starting_v2ray_number = 1 
    for group_index, group in enumerate(groups):
        group_name = group["name"]
        num_ipv6 = group["num_ipv6"]
        group_number = group_index + 1
        starting_v2ray_number += group_index * num_ipv6

        for i in range(1, num_ipv6 + 1):
            kharej_ipv6 = input("\033[93mEnter \033[92mKharej\033[93m IPv6 address \033[92m{}\033[93m for \033[92m{}\033[93m: \033[0m".format(i, group_name))
            group["ipv6_addresses"].append(kharej_ipv6)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────\033[0m")

        for i, kharej_ipv6 in enumerate(group["ipv6_addresses"]):
            v2ray_number = starting_v2ray_number + i

            with open("frp/frpc.toml", "a") as f:
                f.write("\n")
                f.write("[v2ray{}]\n".format(v2ray_number))
                f.write("type = tcp\n")
                f.write("local_ip{} = {}\n".format(v2ray_number, kharej_ipv6))
                f.write("local_port = {}\n".format(local_port))
                f.write("remote_port = {}\n".format(remote_port))
                f.write("group = Azumi{}\n".format(group_number))
                f.write("group_key = azumichwan\n")
                f.write("health_check_type = tcp\n")
                f.write("health_check_timeout_s = 3\n")
                f.write("health_check_max_failed = 3\n")
                f.write("health_check_fail_wait_s = 10\n\n")

    time.sleep(1)

    service_name = "azumifrpc2"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_lk()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    

def iran_single_load():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIran Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mWith Dashboard\033[0m')
    print('2. \033[93mWithout Dashboard\033[0m')
    print('3. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            iran_tcp_dashboardd()
            break
        elif server_type == '2':
            iran_tcp_no_dashboardd()
            break
        elif server_type == '3':
            os.system('clear')
            single_load_menu()
            break
        else:
            print('Invalid choice.')  
            
def iran_tcp_no_dashboardd():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mIRAN \033[93mwithout Dashboard \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  This doesn't have any Dashboard, so it's easier to set up")
    print("\033[93m  You should always configure the IRAN server first and then Kharej")
    print("\033[96m  Enter local and remote ports")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────────╮")
    local_ports = input("\033[93mEnter the \033[92mlocal\033[93m ports : \033[0m")
    remote_ports = input("\033[93mEnter the \033[92mremote\033[93m ports : \033[0m")

    local_ports_list = local_ports.replace(" ", "").split(",")
    remote_ports_list = remote_ports.replace(" ", "").split(",")
    print("\033[93m╰─────────────────────────────────────────────────────────────╯\033[0m")

    num_instances = len(local_ports_list)

    if os.path.exists("frp/frps.toml"):
        os.remove("frp/frps.toml")
    

    with open("frp/frps.toml", "w") as f:
        f.write("[common]\n")
        bind_port = input("\033[93mEnter \033[92mTunnel Port\033[93m (default 443): \033[0m")
        if not bind_port:
            bind_port = "443"
        f.write("bind_port = {}\n".format(bind_port))
        f.write("token = azumi\n")
        f.write("\n")
        for i in range(num_instances):
            f.write("[v2ray{}]\n".format(i+1))
            f.write("type = tcp\n")
            f.write("local_port = {}\n".format(local_ports_list[i]))
            f.write("remote_port = {}\n".format(remote_ports_list[i]))
            f.write("use_encryption = true\n")
            f.write("use_compression = true\n")
            f.write("\n")

    display_checkmark("\033[92mIRAN configuration generated. Yours Truly, Azumi.\033[0m")

    service_name = "azumifrps2"
    frps_path = "/root/frp/frps.toml"

    service_content = f'''[Unit]
Description=frps service
After=network.target

[Service]
ExecStart=/root/frp/./frps -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)
        


    display_notification("\033[93mStarting FRP service...\033[0m")
    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_li()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    
def iran_tcp_dashboardd():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mWith Dashboard\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For Dashboard, You need to have a sub-domain with correct DNS Record")
    print("\033[93m  Enter your desired Dashboard Username & Password and Port")
    print("\033[96m  The rest of the configuration is the same as without the dashboard configuration.")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭──────────────────────────────────────────────────────────────────────────────────────╮")
    domain = input("\033[93mEnter your \033[92mSub-Domain\033[93m: [Better to make sure port 80 is available] \033[0m")
    email = input("\033[93mEnter your \033[92mEmail\033[93m: \033[0m")

    display_notification("\033[93mInstalling Certbot...\033[0m")
    loading_bar_pid = None

    try:
        loading_bar_pid = subprocess.Popen(
            ['bash', '-c', 'while true; do echo -ne "\e[93mInstalling Certbot, gimme a sec: [\\] \r\e[0m"; sleep 0.1; echo -ne "\e[93mInstalling Certbot, gimme a sec: [|] \r\e[0m"; sleep 0.1; echo -ne "\e[93mInstalling Certbot, gimme a sec: [/] \r\e[0m"; sleep 0.1; echo -ne "\e[93mInstalling Certbot, gimme a sec: [-] \r\e[0m"; sleep 0.1; done'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        ).pid

        subprocess.run(['apt', 'install', 'certbot', '-y'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        stop_loading(loading_bar_pid)


        display_notification("\033[93mChecking port 80 availability...\033[0m")
        pid = subprocess.run(['lsof', '-t', '-i', ':80'], capture_output=True, text=True).stdout.strip()
        if pid:
            print(f"\033[93mPort 80 is in use by process with ID [{pid}]. Stopping the process...\033[0m")
            subprocess.run(['sudo', 'kill', pid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        display_notification(f"\033[93mStarting Certbot for your \033[92mDomain {domain}\033[0m")
        subprocess.run(['sudo', 'certbot', 'certonly', '--standalone', '--preferred-challenges', 'http', '--agree-tos', '--email', email, '-d', domain])

        stop_loading(loading_bar_pid)
        
        display_notification("\033[93mFor multiple ports, use commas , (no space) eg : 8080,8081\033[0m")
        kharej_v2ray_port = input("\033[93mEnter \033[92mLocal\033[93m port:\033[0m ")
        iran_v2ray_port = input("\033[93mEnter \033[92mremote\033[93m port:\033[0m ")
        dashboard_user = input("\033[93mEnter the \033[92mDashboard username\033[93m: \033[0m")
        dashboard_pwd = input("\033[93mEnter the \033[92mDashboard password\033[93m: \033[0m")
        dashboard_port = input("\033[93mEnter the \033[92mDashboard port\033[93m: \033[0m")
        bind_port = input("\033[93mEnter \033[92mTunnel port\033[93m (default 443): \033[0m")
        if not bind_port:
           bind_port = "443"
        print("\033[93m───────────────────────────────────────────────────────────────────────────────\033[0m")

        with open('frp/frps.toml', 'w') as frps_ini:
            frps_ini.write(f'''[common]
bind_port = {bind_port}
token = azumi
dashboard_port = {dashboard_port}
dashboard_user = {dashboard_user}
dashboard_pwd = {dashboard_pwd}
dashboard_tls_mode = true
dashboard_tls_cert_file = /etc/letsencrypt/live/{domain}/fullchain.pem
dashboard_tls_key_file = /etc/letsencrypt/live/{domain}/privkey.pem

[v2ray]
type = tcp
local_ip = 127.0.0.1
local_port = {iran_v2ray_port}
remote_port = {kharej_v2ray_port}
use_encryption = true
use_compression = true
''')

        service_name = "azumifrps2"
        frps_path = "/root/frp/frps.toml"

        service_content = f'''[Unit]
Description=frps service
After=network.target

[Service]
ExecStart=/root/frp/./frps -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

        service_path = "/etc/systemd/system/{}.service".format(service_name)

        with open(service_path, 'w') as service_file:
            service_file.write(service_content)

        display_checkmark("\033[92mIran configuration With Dashboard generated. Yours Truly, Azumi!\033[0m")
        time.sleep(1)

        subprocess.run(['systemctl', 'start', 'nginx'], check=True)
        subprocess.run(['systemctl', 'daemon-reload'], check=True)
        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)
        subprocess.run(['systemctl', 'enable', service_name], check=True)
        subprocess.run(['systemctl', 'restart', service_name], check=True)
        res_li()
        display_checkmark("\033[92mFRP Service Started!\033[0m")
        
        time.sleep(1)
        create_decorated_box("Your Dashboard Address: https://{}:{}".format(domain, dashboard_port))
        create_decorated_box("Username: {}".format(dashboard_user))
        create_decorated_box("Password: {}".format(dashboard_pwd))

    except Exception as e:
        print("\033[91mAn error occurred while setting up Iran - With Dashboard.\033[0m")
        print(f"Error Details: {str(e)}")

        if loading_bar_pid:
            stop_loading(loading_bar_pid)



        print("\033[91mSetup failed. Please try again.\033[0m")            
                       
def i3kharej_1iran_load():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92m[10]\033[93mKharej\033[92m [1]\033[93mIRAN Loadbalance Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[96mKHAREJ - Method\033[92m [1]\033[96m - IPV6\033[0m')
    print('2. \033[93mKHAREJ - Method\033[92m [2]\033[96m - localIP\033[0m')
    print('3. \033[92mIRAN\033[0m')
    print('4. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            i3kharej_1iran_kharej_ipv6()
            break
        elif server_type == '2':
            i3kharej_1iran_kharej_local()
            break
        elif server_type == '3':
            i3kharej_1iran_iran()
            break
        elif server_type == '4':
            os.system('clear')
            main_menu()
            break
        else:
            print('Invalid choice.')  
             
            
def i3kharej_1iran_kharej_local():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m Kharej Method\033[92m [2]\033[97m Loadbalance\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Configure each Kharej server seperately")
    print("\033[93m  This method is easier since you don't need to enter an IPV6 for each loadbalance group")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[91mKharej\033[92m [1]\033[0m')
    print('2. \033[93mKharej\033[92m [2]\033[0m')
    print('3. \033[96mKharej\033[92m [3]\033[0m')
    print('4. \033[97mKharej\033[92m [4]\033[0m')
    print('5. \033[93mKharej\033[92m [5]\033[0m')
    print('6. \033[91mKharej\033[92m [6]\033[0m')
    print('7. \033[93mKharej\033[92m [7]\033[0m')
    print('8. \033[96mKharej\033[92m [8]\033[0m')
    print('9. \033[97mKharej\033[92m [9]\033[0m')
    print('10.\033[93mKharej\033[92m [10]\033[0m')
    print('0. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej1_local()
            break
        elif server_type == '2':
            kharej2_local()
            break
        elif server_type == '3':
            kharej3_local()
            break
        elif server_type == '4':
            kharej4_local()
            break
        elif server_type == '5':
            kharej5_local()
            break
        elif server_type == '6':
            kharej6_local()
            break
        elif server_type == '7':
            kharej7_local()
            break
        elif server_type == '8':
            kharej8_local()
            break
        elif server_type == '9':
            kharej9_local()
            break
        elif server_type == '10':
            kharej10_local()
            break
        elif server_type == '0':
            os.system('clear')
            i3kharej_1iran_load()
            break
        else:
            print('Invalid choice.')  
            
def kharej1_local():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej Server \033[92m[1]\033[93m \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For each port, create a loadbalance group, so if i have 3 configs with 3 different ports, i enter 3 for loadbalance input")
    print("\033[93m  For each loadbalance group, enter your config's ports. eg : for loadbalance GP1, port 8080 and for GP2, port 8081")
    print("\033[96m  Since we are establishing a tunnel between one iran server and 5 kharej servers, we need to specify V2ray instance numbers")
    print("\033[92m  For example, if i have 3 configs with different ports on the first kharej server, i make 3 loadbalance group, so the V2ray number is 3")
    print("\033[93m  Then when configuring the Second kharej server, i enter the number 4 for V2ray number, so it starts from that number")
    print("\033[96m  If i don't do that, the connection won't be established")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮") 
    
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * 1)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        v2ray_number = starting_v2ray_number

        with open("frp/frpc.toml", "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(v2ray_number))
            f.write("type = tcp\n")
            f.write("local_ip = 127.0.0.1\n")
            f.write("local_port = {}\n".format(local_port))
            f.write("remote_port = {}\n".format(remote_port))
            f.write("group = Azumi{}\n".format(group_number))
            f.write("group_key = azumichwan\n")
            f.write("health_check_type = tcp\n")
            f.write("health_check_timeout_s = 3\n")
            f.write("health_check_max_failed = 3\n")
            f.write("health_check_interval_s = 10\n")
            f.write("use_encryption = true\n")
            f.write("use_compression = true\n")

    time.sleep(1)

    service_name = "azumifrpc3"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_k1()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = len(groups)
    last_v2ray_number = start_number + num_v2ray_instances 

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")
            
def kharej2_local():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej Server \033[92m[2]\033[93m \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For each port, create a loadbalance group, so if i have 3 configs with 3 different ports, i enter 3 for loadbalance input")
    print("\033[93m  For each loadbalance group, enter your config's ports. eg : for loadbalance GP1, port 8080 and for GP2, port 8081")
    print("\033[96m  Since we are establishing a tunnel between one iran server and 5 kharej servers, we need to specify V2ray instance numbers")
    print("\033[92m  For example, if i have 3 configs with different ports on the first kharej server, i make 3 loadbalance group, so the V2ray number is 3")
    print("\033[93m  Then when configuring the Second kharej server, i enter the number 4 for V2ray number, so it starts from that number")
    print("\033[96m  If i don't do that, the connection won't be established")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮") 
    
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * 1)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        v2ray_number = starting_v2ray_number

        with open("frp/frpc.toml", "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(v2ray_number))
            f.write("type = tcp\n")
            f.write("local_ip = 127.0.0.1\n")
            f.write("local_port = {}\n".format(local_port))
            f.write("remote_port = {}\n".format(remote_port))
            f.write("group = Azumi{}\n".format(group_number))
            f.write("group_key = azumichwan\n")
            f.write("health_check_type = tcp\n")
            f.write("health_check_timeout_s = 3\n")
            f.write("health_check_max_failed = 3\n")
            f.write("health_check_interval_s = 10\n")
            f.write("use_encryption = true\n")
            f.write("use_compression = true\n")

    time.sleep(1)

    service_name = "azumifrpc4"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_k2()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = len(groups)
    last_v2ray_number = start_number + num_v2ray_instances

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")
    
def kharej3_local():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej Server \033[92m[3]\033[93m \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For each port, create a loadbalance group, so if i have 3 configs with 3 different ports, i enter 3 for loadbalance input")
    print("\033[93m  For each loadbalance group, enter your config's ports. eg : for loadbalance GP1, port 8080 and for GP2, port 8081")
    print("\033[96m  Since we are establishing a tunnel between one iran server and 5 kharej servers, we need to specify V2ray instance numbers")
    print("\033[92m  For example, if i have 3 configs with different ports on the first kharej server, i make 3 loadbalance group, so the V2ray number is 3")
    print("\033[93m  Then when configuring the Second kharej server, i enter the number 4 for V2ray number, so it starts from that number")
    print("\033[96m  If i don't do that, the connection won't be established")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮") 
    
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * 1)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        v2ray_number = starting_v2ray_number

        with open("frp/frpc.toml", "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(v2ray_number))
            f.write("type = tcp\n")
            f.write("local_ip = 127.0.0.1\n")
            f.write("local_port = {}\n".format(local_port))
            f.write("remote_port = {}\n".format(remote_port))
            f.write("group = Azumi{}\n".format(group_number))
            f.write("group_key = azumichwan\n")
            f.write("health_check_type = tcp\n")
            f.write("health_check_timeout_s = 3\n")
            f.write("health_check_max_failed = 3\n")
            f.write("health_check_interval_s = 10\n")
            f.write("use_encryption = true\n")
            f.write("use_compression = true\n")

    time.sleep(1)

    service_name = "azumifrpc5"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_k3()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = len(groups)
    last_v2ray_number = start_number + num_v2ray_instances

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")
    
def kharej4_local():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej Server \033[92m[4]\033[93m \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For each port, create a loadbalance group, so if i have 3 configs with 3 different ports, i enter 3 for loadbalance input")
    print("\033[93m  For each loadbalance group, enter your config's ports. eg : for loadbalance GP1, port 8080 and for GP2, port 8081")
    print("\033[96m  Since we are establishing a tunnel between one iran server and 5 kharej servers, we need to specify V2ray instance numbers")
    print("\033[92m  For example, if i have 3 configs with different ports on the first kharej server, i make 3 loadbalance group, so the V2ray number is 3")
    print("\033[93m  Then when configuring the Second kharej server, i enter the number 4 for V2ray number, so it starts from that number")
    print("\033[96m  If i don't do that, the connection won't be established")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮") 
    
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * 1)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        v2ray_number = starting_v2ray_number

        with open("frp/frpc.toml", "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(v2ray_number))
            f.write("type = tcp\n")
            f.write("local_ip = 127.0.0.1\n")
            f.write("local_port = {}\n".format(local_port))
            f.write("remote_port = {}\n".format(remote_port))
            f.write("group = Azumi{}\n".format(group_number))
            f.write("group_key = azumichwan\n")
            f.write("health_check_type = tcp\n")
            f.write("health_check_timeout_s = 3\n")
            f.write("health_check_max_failed = 3\n")
            f.write("health_check_interval_s = 10\n")
            f.write("use_encryption = true\n")
            f.write("use_compression = true\n")

    time.sleep(1)

    service_name = "azumifrpc6"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_k4()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = len(groups)
    last_v2ray_number = start_number + num_v2ray_instances

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")
    
def kharej5_local():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej Server \033[92m[5]\033[93m \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For each port, create a loadbalance group, so if i have 3 configs with 3 different ports, i enter 3 for loadbalance input")
    print("\033[93m  For each loadbalance group, enter your config's ports. eg : for loadbalance GP1, port 8080 and for GP2, port 8081")
    print("\033[96m  Since we are establishing a tunnel between one iran server and 5 kharej servers, we need to specify V2ray instance numbers")
    print("\033[92m  For example, if i have 3 configs with different ports on the first kharej server, i make 3 loadbalance group, so the V2ray number is 3")
    print("\033[93m  Then when configuring the Second kharej server, i enter the number 4 for V2ray number, so it starts from that number")
    print("\033[96m  If i don't do that, the connection won't be established")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮") 
    
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * 1)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        v2ray_number = starting_v2ray_number

        with open("frp/frpc.toml", "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(v2ray_number))
            f.write("type = tcp\n")
            f.write("local_ip = 127.0.0.1\n")
            f.write("local_port = {}\n".format(local_port))
            f.write("remote_port = {}\n".format(remote_port))
            f.write("group = Azumi{}\n".format(group_number))
            f.write("group_key = azumichwan\n")
            f.write("health_check_type = tcp\n")
            f.write("health_check_timeout_s = 3\n")
            f.write("health_check_max_failed = 3\n")
            f.write("health_check_interval_s = 10\n")
            f.write("use_encryption = true\n")
            f.write("use_compression = true\n")

    time.sleep(1)

    service_name = "azumifrpc7"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_k5()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = len(groups)
    last_v2ray_number = start_number + num_v2ray_instances

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")
    
def kharej6_local():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej Server \033[92m[6]\033[93m \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For each port, create a loadbalance group, so if i have 3 configs with 3 different ports, i enter 3 for loadbalance input")
    print("\033[93m  For each loadbalance group, enter your config's ports. eg : for loadbalance GP1, port 8080 and for GP2, port 8081")
    print("\033[96m  Since we are establishing a tunnel between one iran server and 5 kharej servers, we need to specify V2ray instance numbers")
    print("\033[92m  For example, if i have 3 configs with different ports on the first kharej server, i make 3 loadbalance group, so the V2ray number is 3")
    print("\033[93m  Then when configuring the Second kharej server, i enter the number 4 for V2ray number, so it starts from that number")
    print("\033[96m  If i don't do that, the connection won't be established")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮") 
    
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m: \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * 1)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        v2ray_number = starting_v2ray_number

        with open("frp/frpc.toml", "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(v2ray_number))
            f.write("type = tcp\n")
            f.write("local_ip = 127.0.0.1\n")
            f.write("local_port = {}\n".format(local_port))
            f.write("remote_port = {}\n".format(remote_port))
            f.write("group = Azumi{}\n".format(group_number))
            f.write("group_key = azumichwan\n")
            f.write("health_check_type = tcp\n")
            f.write("health_check_timeout_s = 3\n")
            f.write("health_check_max_failed = 3\n")
            f.write("health_check_interval_s = 10\n")
            f.write("use_encryption = true\n")
            f.write("use_compression = true\n")

    time.sleep(1)

    service_name = "azumifrpc8"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_k6()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = len(groups)
    last_v2ray_number = start_number + num_v2ray_instances

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")
            
def kharej7_local():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej Server \033[92m[7]\033[93m \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For each port, create a loadbalance group, so if i have 3 configs with 3 different ports, i enter 3 for loadbalance input")
    print("\033[93m  For each loadbalance group, enter your config's ports. eg : for loadbalance GP1, port 8080 and for GP2, port 8081")
    print("\033[96m  Since we are establishing a tunnel between one iran server and 5 kharej servers, we need to specify V2ray instance numbers")
    print("\033[92m  For example, if i have 3 configs with different ports on the first kharej server, i make 3 loadbalance group, so the V2ray number is 3")
    print("\033[93m  Then when configuring the Second kharej server, i enter the number 4 for V2ray number, so it starts from that number")
    print("\033[96m  If i don't do that, the connection won't be established")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮") 
    
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")
    for group_index, group in enumerate(groups):
        group_name = group["name"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * 1)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        v2ray_number = starting_v2ray_number

        with open("frp/frpc.toml", "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(v2ray_number))
            f.write("type = tcp\n")
            f.write("local_ip = 127.0.0.1\n")
            f.write("local_port = {}\n".format(local_port))
            f.write("remote_port = {}\n".format(remote_port))
            f.write("group = Azumi{}\n".format(group_number))
            f.write("group_key = azumichwan\n")
            f.write("health_check_type = tcp\n")
            f.write("health_check_timeout_s = 3\n")
            f.write("health_check_max_failed = 3\n")
            f.write("health_check_interval_s = 10\n")
            f.write("use_encryption = true\n")
            f.write("use_compression = true\n")

    time.sleep(1)

    service_name = "azumifrpc9"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_k7()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = len(groups)
    last_v2ray_number = start_number + num_v2ray_instances

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")
    
def kharej8_local():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej Server \033[92m[8]\033[93m \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For each port, create a loadbalance group, so if i have 3 configs with 3 different ports, i enter 3 for loadbalance input")
    print("\033[93m  For each loadbalance group, enter your config's ports. eg : for loadbalance GP1, port 8080 and for GP2, port 8081")
    print("\033[96m  Since we are establishing a tunnel between one iran server and 5 kharej servers, we need to specify V2ray instance numbers")
    print("\033[92m  For example, if i have 3 configs with different ports on the first kharej server, i make 3 loadbalance group, so the V2ray number is 3")
    print("\033[93m  Then when configuring the Second kharej server, i enter the number 4 for V2ray number, so it starts from that number")
    print("\033[96m  If i don't do that, the connection won't be established")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮") 
    
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * 1)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        v2ray_number = starting_v2ray_number

        with open("frp/frpc.toml", "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(v2ray_number))
            f.write("type = tcp\n")
            f.write("local_ip = 127.0.0.1\n")
            f.write("local_port = {}\n".format(local_port))
            f.write("remote_port = {}\n".format(remote_port))
            f.write("group = Azumi{}\n".format(group_number))
            f.write("group_key = azumichwan\n")
            f.write("health_check_type = tcp\n")
            f.write("health_check_timeout_s = 3\n")
            f.write("health_check_max_failed = 3\n")
            f.write("health_check_interval_s = 10\n")
            f.write("use_encryption = true\n")
            f.write("use_compression = true\n")

    time.sleep(1)

    service_name = "azumifrpc10"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_k8()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = len(groups)
    last_v2ray_number = start_number + num_v2ray_instances

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")
    
def kharej9_local():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej Server \033[92m[9]\033[93m \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For each port, create a loadbalance group, so if i have 3 configs with 3 different ports, i enter 3 for loadbalance input")
    print("\033[93m  For each loadbalance group, enter your config's ports. eg : for loadbalance GP1, port 8080 and for GP2, port 8081")
    print("\033[96m  Since we are establishing a tunnel between one iran server and 5 kharej servers, we need to specify V2ray instance numbers")
    print("\033[92m  For example, if i have 3 configs with different ports on the first kharej server, i make 3 loadbalance group, so the V2ray number is 3")
    print("\033[93m  Then when configuring the Second kharej server, i enter the number 4 for V2ray number, so it starts from that number")
    print("\033[96m  If i don't do that, the connection won't be established")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮") 
    
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * 1)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        v2ray_number = starting_v2ray_number

        with open("frp/frpc.toml", "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(v2ray_number))
            f.write("type = tcp\n")
            f.write("local_ip = 127.0.0.1\n")
            f.write("local_port = {}\n".format(local_port))
            f.write("remote_port = {}\n".format(remote_port))
            f.write("group = Azumi{}\n".format(group_number))
            f.write("group_key = azumichwan\n")
            f.write("health_check_type = tcp\n")
            f.write("health_check_timeout_s = 3\n")
            f.write("health_check_max_failed = 3\n")
            f.write("health_check_interval_s = 10\n")
            f.write("use_encryption = true\n")
            f.write("use_compression = true\n")

    time.sleep(1)

    service_name = "azumifrpc11"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_k9()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = len(groups)
    last_v2ray_number = start_number + num_v2ray_instances

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")
    
def kharej10_local():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej Server \033[92m[10]\033[93m \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For each port, create a loadbalance group, so if i have 3 configs with 3 different ports, i enter 3 for loadbalance input")
    print("\033[93m  For each loadbalance group, enter your config's ports. eg : for loadbalance GP1, port 8080 and for GP2, port 8081")
    print("\033[96m  Since we are establishing a tunnel between one iran server and 5 kharej servers, we need to specify V2ray instance numbers")
    print("\033[92m  For example, if i have 3 configs with different ports on the first kharej server, i make 3 loadbalance group, so the V2ray number is 3")
    print("\033[93m  Then when configuring the Second kharej server, i enter the number 4 for V2ray number, so it starts from that number")
    print("\033[96m  If i don't do that, the connection won't be established")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮") 
    
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPV4/IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * 1)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: \033[0m".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        v2ray_number = starting_v2ray_number

        with open("frp/frpc.toml", "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(v2ray_number))
            f.write("type = tcp\n")
            f.write("local_ip = 127.0.0.1\n")
            f.write("local_port = {}\n".format(local_port))
            f.write("remote_port = {}\n".format(remote_port))
            f.write("group = Azumi{}\n".format(group_number))
            f.write("group_key = azumichwan\n")
            f.write("health_check_type = tcp\n")
            f.write("health_check_timeout_s = 3\n")
            f.write("health_check_max_failed = 3\n")
            f.write("health_check_interval_s = 10\n")
            f.write("use_encryption = true\n")
            f.write("use_compression = true\n")

    time.sleep(1)

    service_name = "azumifrpc12"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_k10()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = len(groups)
    last_v2ray_number = start_number + num_v2ray_instances

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")
    
def i3kharej_1iran_kharej_ipv6():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m Kharej Method\033[92m[1]\033[97m Loadbalance\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Configure each Kharej server seperately")
    print("\033[93m  In This method we enter an IPV6 for each port")
    print("\033[97m  for example: we have 2 configs with different ports, first we make 2 loadbalance groups and we specify an IPV6 for each different port as well")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[91mKharej\033[92m [1]\033[0m')
    print('2. \033[93mKharej\033[92m [2]\033[0m')
    print('3. \033[96mKharej\033[92m [3]\033[0m')
    print('4. \033[97mKharej\033[92m [4]\033[0m')
    print('5. \033[93mKharej\033[92m [5]\033[0m')
    print('6. \033[91mKharej\033[92m [6]\033[0m')
    print('7. \033[93mKharej\033[92m [7]\033[0m')
    print('8. \033[96mKharej\033[92m [8]\033[0m')
    print('9. \033[97mKharej\033[92m [9]\033[0m')
    print('10.\033[93mKharej\033[92m [10]\033[0m')
    print('0. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej1()
            break
        elif server_type == '2':
            kharej2()
            break
        elif server_type == '3':
            kharej3()
            break
        elif server_type == '4':
            kharej4()
            break
        elif server_type == '5':
            kharej5()
            break
        elif server_type == '6':
            kharej6()
            break
        elif server_type == '7':
            kharej7()
            break
        elif server_type == '8':
            kharej8()
            break
        elif server_type == '9':
            kharej9()
            break
        elif server_type == '10':
            kharej10()
            break
        elif server_type == '0':
            os.system('clear')
            i3kharej_1iran_load()
            break
        else:
            print('Invalid choice.') 
    


def kharej1():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mKharej \033[93mServer \033[92m[1] \033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For each port, create a loadbalance group, so if i have 3 configs with 3 different ports, i enter 3 for loadbalance input")
    print("\033[96m  In this method, we also specify an IPV6 for each PORT within the loadbalance group")
    print("\033[93m  For each loadbalance group, enter your config's ports. eg : for loadbalance GP1, port 8080 and for GP2, port 8081")
    print("\033[96m  Since we are establishing a tunnel between one iran server and 5 kharej servers, we need to specify V2ray instance numbers")
    print("\033[92m  For example, if i have 3 configs with different ports on the first kharej server, i make 3 loadbalance group, so the V2ray number is 3")
    print("\033[93m  Then when configuring the Second kharej server, i enter the number 4 for V2ray number, so it starts from that number")
    print("\033[96m  If i don't do that, the connection won't be established")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮")

    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mload balance groups[\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input. Please enter a valid number\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)

        while True:
            try:
                num_ipv6 = int(input("\033[93mEnter the number of \033[92mKharej IPv6 addresses\033[93m needed for \033[92m{}\033[93m: \033[0m".format(group_name)))
                break
            except ValueError:
                print("\033[91mInvalid input. Please enter a valid number\033[0m")

        group = {"name": group_name, "num_ipv6": num_ipv6, "ipv6_addresses": []}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m: \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        num_ipv6 = group["num_ipv6"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * num_ipv6)

        for i in range(1, num_ipv6 + 1):
            kharej_ipv6 = input("\033[93mEnter \033[92mKharej\033[93m IPv6 address \033[92m{}\033[93m for \033[92m{}\033[93m: \033[0m".format(i, group_name))
            group["ipv6_addresses"].append(kharej_ipv6)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        for i, kharej_ipv6 in enumerate(group["ipv6_addresses"]):
            v2ray_number = starting_v2ray_number + i

            with open("frp/frpc.toml", "a") as f:
                f.write("\n")
                f.write("[v2ray{}]\n".format(v2ray_number))
                f.write("type = tcp\n")
                f.write("local_ip{} = {}\n".format(v2ray_number, kharej_ipv6))
                f.write("local_port = {}\n".format(local_port))
                f.write("remote_port = {}\n".format(remote_port))
                f.write("group = Azumi{}\n".format(group_number))
                f.write("group_key = azumichwan\n")
                f.write("health_check_type = tcp\n")
                f.write("health_check_timeout_s = 3\n")
                f.write("health_check_max_failed = 3\n")
                f.write("health_check_interval_s = 10\n")
                f.write("use_encryption = true\n")
                f.write("use_compression = true\n")

    time.sleep(1)

    service_name = "azumifrpc3"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_k1()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

	
    num_v2ray_instances = sum(group["num_ipv6"] for group in groups)
    last_v2ray_number = start_number + num_v2ray_instances

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")

def kharej2():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mKharej \033[93mServer \033[92m[2] \033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For each port, create a loadbalance group, so if i have 3 configs with 3 different ports, i enter 3 for loadbalance input")
    print("\033[92m  In this method, we also specify an IPV6 for each PORT within the loadbalance group")
    print("\033[93m  For each loadbalance group, enter your config's ports. eg : for loadbalance GP1, port 8080 and for GP2, port 8081")
    print("\033[96m  Since we are establishing a tunnel between one iran server and 5 kharej servers, we need to specify V2ray instance numbers")
    print("\033[92m  For example, if i have 3 configs with different ports on the first kharej server, i make 3 loadbalance group, so the V2ray number is 3")
    print("\033[93m  Then when configuring the Second kharej server, i enter the number 4 for V2ray number, so it starts from that number")
    print("\033[96m  If i don't do that, the connection won't be established")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮")

    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mload balance groups[\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input. Please enter a valid number\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)

        while True:
            try:
                num_ipv6 = int(input("\033[93mEnter the number of \033[92mKharej IPv6 addresses\033[93m needed for \033[92m{}\033[93m: \033[0m".format(group_name)))
                break
            except ValueError:
                print("\033[91mInvalid input. Please enter a valid number\033[0m")

        group = {"name": group_name, "num_ipv6": num_ipv6, "ipv6_addresses": []}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        num_ipv6 = group["num_ipv6"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * num_ipv6)

        for i in range(1, num_ipv6 + 1):
            kharej_ipv6 = input("\033[93mEnter \033[92mKharej\033[93m IPv6 address \033[92m{}\033[93m for \033[92m{}\033[93m: \033[0m".format(i, group_name))
            group["ipv6_addresses"].append(kharej_ipv6)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m: ".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m: ".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        for i, kharej_ipv6 in enumerate(group["ipv6_addresses"]):
            v2ray_number = starting_v2ray_number + i

            with open("frp/frpc.toml", "a") as f:
                f.write("\n")
                f.write("[v2ray{}]\n".format(v2ray_number))
                f.write("type = tcp\n")
                f.write("local_ip{} = {}\n".format(v2ray_number, kharej_ipv6))
                f.write("local_port = {}\n".format(local_port))
                f.write("remote_port = {}\n".format(remote_port))
                f.write("group = Azumi{}\n".format(group_number))
                f.write("group_key = azumichwan\n")
                f.write("health_check_type = tcp\n")
                f.write("health_check_timeout_s = 3\n")
                f.write("health_check_max_failed = 3\n")
                f.write("health_check_interval_s = 10\n")
                f.write("use_encryption = true\n")
                f.write("use_compression = true\n")

    time.sleep(1)

    service_name = "azumifrpc4"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_k2()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = sum(group["num_ipv6"] for group in groups)
    last_v2ray_number = start_number + num_v2ray_instances

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")
    
def kharej3():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mKharej \033[93mServer \033[92m[3] \033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For each port, create a loadbalance group, so if i have 3 configs with 3 different ports, i enter 3 for loadbalance input")
    print("\033[92m  In this method, we also specify an IPV6 for each PORT within the loadbalance group")
    print("\033[93m  For each loadbalance group, enter your config's ports. eg : for loadbalance GP1, port 8080 and for GP2, port 8081")
    print("\033[96m  Since we are establishing a tunnel between one iran server and 5 kharej servers, we need to specify V2ray instance numbers")
    print("\033[92m  For example, if i have 3 configs with different ports on the first kharej server, i make 3 loadbalance group, so the V2ray number is 3")
    print("\033[93m  Then when configuring the Second kharej server, i enter the number 4 for V2ray number, so it starts from that number")
    print("\033[96m  If i don't do that, the connection won't be established")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮")

    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mload balance groups[\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input. Please enter a valid number\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)

        while True:
            try:
                num_ipv6 = int(input("\033[93mEnter the number of \033[92mKharej IPv6 addresses\033[93m needed for \033[92m{}\033[93m: \033[0m".format(group_name)))
                break
            except ValueError:
                print("\033[91mInvalid input. Please enter a valid number\033[0m")

        group = {"name": group_name, "num_ipv6": num_ipv6, "ipv6_addresses": []}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m: \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        num_ipv6 = group["num_ipv6"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * num_ipv6)

        for i in range(1, num_ipv6 + 1):
            kharej_ipv6 = input("\033[93mEnter \033[92mKharej\033[93m IPv6 address \033[92m{}\033[93m for \033[92m{}\033[93m: \033[0m".format(i, group_name))
            group["ipv6_addresses"].append(kharej_ipv6)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        for i, kharej_ipv6 in enumerate(group["ipv6_addresses"]):
            v2ray_number = starting_v2ray_number + i

            with open("frp/frpc.toml", "a") as f:
                f.write("\n")
                f.write("[v2ray{}]\n".format(v2ray_number))
                f.write("type = tcp\n")
                f.write("local_ip{} = {}\n".format(v2ray_number, kharej_ipv6))
                f.write("local_port = {}\n".format(local_port))
                f.write("remote_port = {}\n".format(remote_port))
                f.write("group = Azumi{}\n".format(group_number))
                f.write("group_key = azumichwan\n")
                f.write("health_check_type = tcp\n")
                f.write("health_check_timeout_s = 3\n")
                f.write("health_check_max_failed = 3\n")
                f.write("health_check_interval_s = 10\n")
                f.write("use_encryption = true\n")
                f.write("use_compression = true\n")

    time.sleep(1)

    service_name = "azumifrpc5"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_k3()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = sum(group["num_ipv6"] for group in groups)
    last_v2ray_number = start_number + num_v2ray_instances

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")

def kharej4():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mKharej \033[93mServer \033[92m[4] \033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For each port, create a loadbalance group, so if i have 3 configs with 3 different ports, i enter 3 for loadbalance input")
    print("\033[92m  In this method, we also specify an IPV6 for each PORT within the loadbalance group")
    print("\033[93m  For each loadbalance group, enter your config's ports. eg : for loadbalance GP1, port 8080 and for GP2, port 8081")
    print("\033[96m  Since we are establishing a tunnel between one iran server and 5 kharej servers, we need to specify V2ray instance numbers")
    print("\033[92m  For example, if i have 3 configs with different ports on the first kharej server, i make 3 loadbalance group, so the V2ray number is 3")
    print("\033[93m  Then when configuring the Second kharej server, i enter the number 4 for V2ray number, so it starts from that number")
    print("\033[96m  If i don't do that, the connection won't be established")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮")

    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mload balance groups[\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input. Please enter a valid number\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)

        while True:
            try:
                num_ipv6 = int(input("\033[93mEnter the number of \033[92mKharej IPv6 addresses\033[93m needed for \033[92m{}\033[93m: \033[0m".format(group_name)))
                break
            except ValueError:
                print("\033[91mInvalid input. Please enter a valid number\033[0m")

        group = {"name": group_name, "num_ipv6": num_ipv6, "ipv6_addresses": []}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        num_ipv6 = group["num_ipv6"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * num_ipv6)

        for i in range(1, num_ipv6 + 1):
            kharej_ipv6 = input("\033[93mEnter \033[92mKharej\033[93m IPv6 address \033[92m{}\033[93m for \033[92m{}\033[93m: \033[0m".format(i, group_name))
            group["ipv6_addresses"].append(kharej_ipv6)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        for i, kharej_ipv6 in enumerate(group["ipv6_addresses"]):
            v2ray_number = starting_v2ray_number + i

            with open("frp/frpc.toml", "a") as f:
                f.write("\n")
                f.write("[v2ray{}]\n".format(v2ray_number))
                f.write("type = tcp\n")
                f.write("local_ip{} = {}\n".format(v2ray_number, kharej_ipv6))
                f.write("local_port = {}\n".format(local_port))
                f.write("remote_port = {}\n".format(remote_port))
                f.write("group = Azumi{}\n".format(group_number))
                f.write("group_key = azumichwan\n")
                f.write("health_check_type = tcp\n")
                f.write("health_check_timeout_s = 3\n")
                f.write("health_check_max_failed = 3\n")
                f.write("health_check_interval_s = 10\n")
                f.write("use_encryption = true\n")
                f.write("use_compression = true\n")

    time.sleep(1)

    service_name = "azumifrpc6"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_k4()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = sum(group["num_ipv6"] for group in groups)
    last_v2ray_number = start_number + num_v2ray_instances

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")

def kharej5():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mKharej \033[93mServer \033[92m[5] \033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For each port, create a loadbalance group, so if i have 3 configs with 3 different ports, i enter 3 for loadbalance input")
    print("\033[92m  In this method, we also specify an IPV6 for each PORT within the loadbalance group")
    print("\033[93m  For each loadbalance group, enter your config's ports. eg : for loadbalance GP1, port 8080 and for GP2, port 8081")
    print("\033[96m  Since we are establishing a tunnel between one iran server and 5 kharej servers, we need to specify V2ray instance numbers")
    print("\033[92m  For example, if i have 3 configs with different ports on the first kharej server, i make 3 loadbalance group, so the V2ray number is 3")
    print("\033[93m  Then when configuring the Second kharej server, i enter the number 4 for V2ray number, so it starts from that number")
    print("\033[96m  If i don't do that, the connection won't be established")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮")

    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mload balance groups[\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input. Please enter a valid number\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)

        while True:
            try:
                num_ipv6 = int(input("\033[93mEnter the number of \033[92mKharej IPv6 addresses\033[93m needed for \033[92m{}\033[93m: \033[0m".format(group_name)))
                break
            except ValueError:
                print("\033[91mInvalid input. Please enter a valid number\033[0m")

        group = {"name": group_name, "num_ipv6": num_ipv6, "ipv6_addresses": []}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        num_ipv6 = group["num_ipv6"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * num_ipv6)

        for i in range(1, num_ipv6 + 1):
            kharej_ipv6 = input("\033[93mEnter \033[92mKharej\033[93m IPv6 address \033[92m{}\033[93m for \033[92m{}\033[93m: \033[0m".format(i, group_name))
            group["ipv6_addresses"].append(kharej_ipv6)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        for i, kharej_ipv6 in enumerate(group["ipv6_addresses"]):
            v2ray_number = starting_v2ray_number + i

            with open("frp/frpc.toml", "a") as f:
                f.write("\n")
                f.write("[v2ray{}]\n".format(v2ray_number))
                f.write("type = tcp\n")
                f.write("local_ip{} = {}\n".format(v2ray_number, kharej_ipv6))
                f.write("local_port = {}\n".format(local_port))
                f.write("remote_port = {}\n".format(remote_port))
                f.write("group = Azumi{}\n".format(group_number))
                f.write("group_key = azumichwan\n")
                f.write("health_check_type = tcp\n")
                f.write("health_check_timeout_s = 3\n")
                f.write("health_check_max_failed = 3\n")
                f.write("health_check_interval_s = 10\n")
                f.write("use_encryption = true\n")
                f.write("use_compression = true\n")

    time.sleep(1)

    service_name = "azumifrpc7"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_k5()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = sum(group["num_ipv6"] for group in groups)
    last_v2ray_number = start_number + num_v2ray_instances

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")

def kharej6():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mKharej \033[93mServer \033[92m[6] \033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For each port, create a loadbalance group, so if i have 3 configs with 3 different ports, i enter 3 for loadbalance input")
    print("\033[96m  In this method, we also specify an IPV6 for each PORT within the loadbalance group")
    print("\033[93m  For each loadbalance group, enter your config's ports. eg : for loadbalance GP1, port 8080 and for GP2, port 8081")
    print("\033[96m  Since we are establishing a tunnel between one iran server and 5 kharej servers, we need to specify V2ray instance numbers")
    print("\033[92m  For example, if i have 3 configs with different ports on the first kharej server, i make 3 loadbalance group, so the V2ray number is 3")
    print("\033[93m  Then when configuring the Second kharej server, i enter the number 4 for V2ray number, so it starts from that number")
    print("\033[96m  If i don't do that, the connection won't be established")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮")

    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mload balance groups[\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input. Please enter a valid number\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)

        while True:
            try:
                num_ipv6 = int(input("\033[93mEnter the number of \033[92mKharej IPv6 addresses\033[93m needed for \033[92m{}\033[93m: \033[0m".format(group_name)))
                break
            except ValueError:
                print("\033[91mInvalid input. Please enter a valid number\033[0m")

        group = {"name": group_name, "num_ipv6": num_ipv6, "ipv6_addresses": []}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        num_ipv6 = group["num_ipv6"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * num_ipv6)

        for i in range(1, num_ipv6 + 1):
            kharej_ipv6 = input("\033[93mEnter \033[92mKharej\033[93m IPv6 address \033[92m{}\033[93m for \033[92m{}\033[93m: \033[0m".format(i, group_name))
            group["ipv6_addresses"].append(kharej_ipv6)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        for i, kharej_ipv6 in enumerate(group["ipv6_addresses"]):
            v2ray_number = starting_v2ray_number + i

            with open("frp/frpc.toml", "a") as f:
                f.write("\n")
                f.write("[v2ray{}]\n".format(v2ray_number))
                f.write("type = tcp\n")
                f.write("local_ip{} = {}\n".format(v2ray_number, kharej_ipv6))
                f.write("local_port = {}\n".format(local_port))
                f.write("remote_port = {}\n".format(remote_port))
                f.write("group = Azumi{}\n".format(group_number))
                f.write("group_key = azumichwan\n")
                f.write("health_check_type = tcp\n")
                f.write("health_check_timeout_s = 3\n")
                f.write("health_check_max_failed = 3\n")
                f.write("health_check_interval_s = 10\n")
                f.write("use_encryption = true\n")
                f.write("use_compression = true\n")

    time.sleep(1)

    service_name = "azumifrpc8"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_k6()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

	
    num_v2ray_instances = sum(group["num_ipv6"] for group in groups)
    last_v2ray_number = start_number + num_v2ray_instances

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")

def kharej7():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mKharej \033[93mServer \033[92m[7] \033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For each port, create a loadbalance group, so if i have 3 configs with 3 different ports, i enter 3 for loadbalance input")
    print("\033[92m  In this method, we also specify an IPV6 for each PORT within the loadbalance group")
    print("\033[93m  For each loadbalance group, enter your config's ports. eg : for loadbalance GP1, port 8080 and for GP2, port 8081")
    print("\033[96m  Since we are establishing a tunnel between one iran server and 5 kharej servers, we need to specify V2ray instance numbers")
    print("\033[92m  For example, if i have 3 configs with different ports on the first kharej server, i make 3 loadbalance group, so the V2ray number is 3")
    print("\033[93m  Then when configuring the Second kharej server, i enter the number 4 for V2ray number, so it starts from that number")
    print("\033[96m  If i don't do that, the connection won't be established")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮")

    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mload balance groups[\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input. Please enter a valid number\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)

        while True:
            try:
                num_ipv6 = int(input("\033[93mEnter the number of \033[92mKharej IPv6 addresses\033[93m needed for \033[92m{}\033[93m: \033[0m".format(group_name)))
                break
            except ValueError:
                print("\033[91mInvalid input. Please enter a valid number\033[0m")

        group = {"name": group_name, "num_ipv6": num_ipv6, "ipv6_addresses": []}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        num_ipv6 = group["num_ipv6"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * num_ipv6)

        for i in range(1, num_ipv6 + 1):
            kharej_ipv6 = input("\033[93mEnter \033[92mKharej\033[93m IPv6 address \033[92m{}\033[93m for \033[92m{}\033[93m: \033[0m".format(i, group_name))
            group["ipv6_addresses"].append(kharej_ipv6)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        for i, kharej_ipv6 in enumerate(group["ipv6_addresses"]):
            v2ray_number = starting_v2ray_number + i

            with open("frp/frpc.toml", "a") as f:
                f.write("\n")
                f.write("[v2ray{}]\n".format(v2ray_number))
                f.write("type = tcp\n")
                f.write("local_ip{} = {}\n".format(v2ray_number, kharej_ipv6))
                f.write("local_port = {}\n".format(local_port))
                f.write("remote_port = {}\n".format(remote_port))
                f.write("group = Azumi{}\n".format(group_number))
                f.write("group_key = azumichwan\n")
                f.write("health_check_type = tcp\n")
                f.write("health_check_timeout_s = 3\n")
                f.write("health_check_max_failed = 3\n")
                f.write("health_check_interval_s = 10\n")
                f.write("use_encryption = true\n")
                f.write("use_compression = true\n")

    time.sleep(1)

    service_name = "azumifrpc9"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_k7()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = sum(group["num_ipv6"] for group in groups)
    last_v2ray_number = start_number + num_v2ray_instances

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")
    
def kharej8():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mKharej \033[93mServer \033[92m[8] \033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For each port, create a loadbalance group, so if i have 3 configs with 3 different ports, i enter 3 for loadbalance input")
    print("\033[92m  In this method, we also specify an IPV6 for each PORT within the loadbalance group")
    print("\033[93m  For each loadbalance group, enter your config's ports. eg : for loadbalance GP1, port 8080 and for GP2, port 8081")
    print("\033[96m  Since we are establishing a tunnel between one iran server and 5 kharej servers, we need to specify V2ray instance numbers")
    print("\033[92m  For example, if i have 3 configs with different ports on the first kharej server, i make 3 loadbalance group, so the V2ray number is 3")
    print("\033[93m  Then when configuring the Second kharej server, i enter the number 4 for V2ray number, so it starts from that number")
    print("\033[96m  If i don't do that, the connection won't be established")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮")

    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mload balance groups[\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input. Please enter a valid number\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)

        while True:
            try:
                num_ipv6 = int(input("\033[93mEnter the number of \033[92mKharej IPv6 addresses\033[93m needed for \033[92m{}\033[93m: \033[0m".format(group_name)))
                break
            except ValueError:
                print("\033[91mInvalid input. Please enter a valid number\033[0m")

        group = {"name": group_name, "num_ipv6": num_ipv6, "ipv6_addresses": []}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        num_ipv6 = group["num_ipv6"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * num_ipv6)

        for i in range(1, num_ipv6 + 1):
            kharej_ipv6 = input("\033[93mEnter \033[92mKharej\033[93m IPv6 address \033[92m{}\033[93m for \033[92m{}\033[93m: \033[0m".format(i, group_name))
            group["ipv6_addresses"].append(kharej_ipv6)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        for i, kharej_ipv6 in enumerate(group["ipv6_addresses"]):
            v2ray_number = starting_v2ray_number + i

            with open("frp/frpc.toml", "a") as f:
                f.write("\n")
                f.write("[v2ray{}]\n".format(v2ray_number))
                f.write("type = tcp\n")
                f.write("local_ip{} = {}\n".format(v2ray_number, kharej_ipv6))
                f.write("local_port = {}\n".format(local_port))
                f.write("remote_port = {}\n".format(remote_port))
                f.write("group = Azumi{}\n".format(group_number))
                f.write("group_key = azumichwan\n")
                f.write("health_check_type = tcp\n")
                f.write("health_check_timeout_s = 3\n")
                f.write("health_check_max_failed = 3\n")
                f.write("health_check_interval_s = 10\n")
                f.write("use_encryption = true\n")
                f.write("use_compression = true\n")

    time.sleep(1)

    service_name = "azumifrpc10"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_k8()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = sum(group["num_ipv6"] for group in groups)
    last_v2ray_number = start_number + num_v2ray_instances

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")

def kharej9():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mKharej \033[93mServer \033[92m[9] \033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For each port, create a loadbalance group, so if i have 3 configs with 3 different ports, i enter 3 for loadbalance input")
    print("\033[92m  In this method, we also specify an IPV6 for each PORT within the loadbalance group")
    print("\033[93m  For each loadbalance group, enter your config's ports. eg : for loadbalance GP1, port 8080 and for GP2, port 8081")
    print("\033[96m  Since we are establishing a tunnel between one iran server and 5 kharej servers, we need to specify V2ray instance numbers")
    print("\033[92m  For example, if i have 3 configs with different ports on the first kharej server, i make 3 loadbalance group, so the V2ray number is 3")
    print("\033[93m  Then when configuring the Second kharej server, i enter the number 4 for V2ray number, so it starts from that number")
    print("\033[96m  If i don't do that, the connection won't be established")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮")

    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mload balance groups[\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input. Please enter a valid number\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)

        while True:
            try:
                num_ipv6 = int(input("\033[93mEnter the number of \033[92mKharej IPv6 addresses\033[93m needed for \033[92m{}\033[93m: \033[0m".format(group_name)))
                break
            except ValueError:
                print("\033[91mInvalid input. Please enter a valid number\033[0m")

        group = {"name": group_name, "num_ipv6": num_ipv6, "ipv6_addresses": []}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        num_ipv6 = group["num_ipv6"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * num_ipv6)

        for i in range(1, num_ipv6 + 1):
            kharej_ipv6 = input("\033[93mEnter \033[92mKharej\033[93m IPv6 address \033[92m{}\033[93m for \033[92m{}\033[93m: \033[0m".format(i, group_name))
            group["ipv6_addresses"].append(kharej_ipv6)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        for i, kharej_ipv6 in enumerate(group["ipv6_addresses"]):
            v2ray_number = starting_v2ray_number + i

            with open("frp/frpc.toml", "a") as f:
                f.write("\n")
                f.write("[v2ray{}]\n".format(v2ray_number))
                f.write("type = tcp\n")
                f.write("local_ip{} = {}\n".format(v2ray_number, kharej_ipv6))
                f.write("local_port = {}\n".format(local_port))
                f.write("remote_port = {}\n".format(remote_port))
                f.write("group = Azumi{}\n".format(group_number))
                f.write("group_key = azumichwan\n")
                f.write("health_check_type = tcp\n")
                f.write("health_check_timeout_s = 3\n")
                f.write("health_check_max_failed = 3\n")
                f.write("health_check_interval_s = 10\n")
                f.write("use_encryption = true\n")
                f.write("use_compression = true\n")

    time.sleep(1)

    service_name = "azumifrpc11"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_k9()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = sum(group["num_ipv6"] for group in groups)
    last_v2ray_number = start_number + num_v2ray_instances

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")

def kharej10():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mKharej \033[93mServer \033[92m[10] \033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For each port, create a loadbalance group, so if i have 3 configs with 3 different ports, i enter 3 for loadbalance input")
    print("\033[92m  In this method, we also specify an IPV6 for each PORT within the loadbalance group")
    print("\033[93m  For each loadbalance group, enter your config's ports. eg : for loadbalance GP1, port 8080 and for GP2, port 8081")
    print("\033[96m  Since we are establishing a tunnel between one iran server and 5 kharej servers, we need to specify V2ray instance numbers")
    print("\033[92m  For example, if i have 3 configs with different ports on the first kharej server, i make 3 loadbalance group, so the V2ray number is 3")
    print("\033[93m  Then when configuring the Second kharej server, i enter the number 4 for V2ray number, so it starts from that number")
    print("\033[96m  If i don't do that, the connection won't be established")
    print("\033[93m╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮")

    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mload balance groups[\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input. Please enter a valid number\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)

        while True:
            try:
                num_ipv6 = int(input("\033[93mEnter the number of \033[92mKharej IPv6 addresses\033[93m needed for \033[92m{}\033[93m: \033[0m".format(group_name)))
                break
            except ValueError:
                print("\033[91mInvalid input. Please enter a valid number\033[0m")

        group = {"name": group_name, "num_ipv6": num_ipv6, "ipv6_addresses": []}
        groups.append(group)

    time.sleep(1)

    iran_ipv6 = input("\033[93mEnter \033[92mIRAN\033[93m IPv6 address: \033[0m")

    if os.path.exists("frp/frpc.toml"):
        os.remove("frp/frpc.toml")

    with open("frp/frpc.toml", "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")

    while True:
        try:
            start_number = int(input("\033[93mEnter the starting v2ray and group number: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    for group_index, group in enumerate(groups):
        group_name = group["name"]
        num_ipv6 = group["num_ipv6"]
        group_number = start_number + group_index  
        starting_v2ray_number = start_number + (group_index * num_ipv6)

        for i in range(1, num_ipv6 + 1):
            kharej_ipv6 = input("\033[93mEnter \033[92mKharej\033[93m IPv6 address \033[92m{}\033[93m for \033[92m{}\033[93m: \033[0m".format(i, group_name))
            group["ipv6_addresses"].append(kharej_ipv6)

        local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
        remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
        print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

        for i, kharej_ipv6 in enumerate(group["ipv6_addresses"]):
            v2ray_number = starting_v2ray_number + i

            with open("frp/frpc.toml", "a") as f:
                f.write("\n")
                f.write("[v2ray{}]\n".format(v2ray_number))
                f.write("type = tcp\n")
                f.write("local_ip{} = {}\n".format(v2ray_number, kharej_ipv6))
                f.write("local_port = {}\n".format(local_port))
                f.write("remote_port = {}\n".format(remote_port))
                f.write("group = Azumi{}\n".format(group_number))
                f.write("group_key = azumichwan\n")
                f.write("health_check_type = tcp\n")
                f.write("health_check_timeout_s = 3\n")
                f.write("health_check_max_failed = 3\n")
                f.write("health_check_interval_s = 10\n")
                f.write("use_encryption = true\n")
                f.write("use_compression = true\n")

    time.sleep(1)

    service_name = "azumifrpc12"
    frps_path = "/root/frp/frpc.toml"

    service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_k10()
    display_checkmark("\033[92mFRP Service Started!\033[0m")

    num_v2ray_instances = sum(group["num_ipv6"] for group in groups)
    last_v2ray_number = start_number + num_v2ray_instances

    print("Use the last V2ray number for configuring the next kharej server.")
    print("+--------------------------------------------------+")
    print("|   Number of Load Balance Groups: {}              |".format(num_groups))
    print("|   Total V2Ray Instances Created: {}              |".format(num_v2ray_instances))
    print("|   \033[92mLast V2Ray Number: {}\033[0m                          |".format(last_v2ray_number))
    print("+--------------------------------------------------+")

def i3kharej_1iran_iran():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIRAN Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mWith Dashboard\033[0m')
    print('2. \033[93mWithout Dashboard\033[0m')
    print('3. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            iran_with_dash()
            break
        elif server_type == '2':
            iran_without_dash()
            break
        elif server_type == '3':
            os.system('clear')
            i3kharej_1iran_load()
            break
        else:
            print('Invalid choice.')  
                        
	
def iran_without_dash():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIRAN Menu  \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  This doesn't have any Dashboard, so it's easier to setup")
    print("\033[93m  You should always Configure IRAN server first and then Kharej")
    print("\033[96m  Enter local and Remote port")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")

    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────────────────────╮") 

    local_ports = input("\033[93mEnter the \033[92mlocal\033[93m ports : \033[0m")
    remote_ports = input("\033[93mEnter the \033[92mremote\033[93m ports : \033[0m")

    local_ports_list = local_ports.replace(" ", ",").split(",")
    remote_ports_list = remote_ports.replace(" ", ",").split(",")

    local_ports_list = [port.strip() for port in local_ports_list]
    remote_ports_list = [port.strip() for port in remote_ports_list]

    num_instances = len(local_ports_list)

    if os.path.exists("frp/frps.toml"):
        os.remove("frp/frps.toml")

    with open("frp/frps.toml", "w") as f:
        f.write("[common]\n")
        bind_port = input("\033[93mEnter \033[92mTunnel Port\033[93m : \033[0m")
        if not bind_port:
            bind_port = "443"
        f.write("bind_port = {}\n".format(bind_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")
        f.write("\n")
        f.write("[v2ray]\n")  
        f.write("type = tcp\n")
        f.write("local_port = {}\n".format(",".join(local_ports_list)))
        f.write("remote_port = {}\n".format(",".join(remote_ports_list)))
        f.write("use_encryption = true\n")
        f.write("use_compression = true\n")

    display_checkmark("\033[92mIRAN configuration generated. Yours Truly, Azumi.\033[0m")

    
    service_name = "azumifrps3"
    frps_path = "/root/frp/frps.toml"

    service_content = f'''[Unit]
Description=frps service
After=network.target

[Service]
ExecStart=/root/frp/./frps -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)
    display_notification("\033[93mStarting FRP service...\033[0m")
    time.sleep(1)
    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    time.sleep(1)
    res_i()
    display_checkmark("\033[92mFRP Service Started!\033[0m")


def iran_with_dash():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mWith Dashboard\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  For Dashboard, You need to have a sub-domain with correct DNS Record")
    print("\033[93m  Enter your desired Dashboard Username & Password and Port")
    print("\033[96m  The rest of the configuration is the same as without the dashboard configuration.")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭──────────────────────────────────────────────────────────────────────────────────────╮")
    domain = input("\033[93mEnter your \033[92mSub-Domain\033[93m: [Better to make sure port 80 is available] \033[0m")
    email = input("\033[93mEnter your \033[92mEmail\033[93m: \033[0m")

    display_notification("\033[93mInstalling Certbot...\033[0m")
    loading_bar_pid = None

    try:
        loading_bar_pid = subprocess.Popen(
            ['bash', '-c', 'while true; do echo -ne "\e[93mInstalling Certbot, gimme a sec: [\\] \r\e[0m"; sleep 0.1; echo -ne "\e[93mInstalling Certbot, gimme a sec: [|] \r\e[0m"; sleep 0.1; echo -ne "\e[93mInstalling Certbot, gimme a sec: [/] \r\e[0m"; sleep 0.1; echo -ne "\e[93mInstalling Certbot, gimme a sec: [-] \r\e[0m"; sleep 0.1; done'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        ).pid

        subprocess.run(['apt', 'install', 'certbot', '-y'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        stop_loading(loading_bar_pid)


        display_notification("\033[93mChecking port 80 availability...\033[0m")
        pid = subprocess.run(['lsof', '-t', '-i', ':80'], capture_output=True, text=True).stdout.strip()
        if pid:
            print(f"\033[93mPort 80 is in use by process with ID [{pid}]. Stopping the process...\033[0m")
            subprocess.run(['sudo', 'kill', pid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        display_notification(f"\033[93mStarting Certbot for your \033[92mDomain {domain}\033[0m")
        subprocess.run(['sudo', 'certbot', 'certonly', '--standalone', '--preferred-challenges', 'http', '--agree-tos', '--email', email, '-d', domain])

        stop_loading(loading_bar_pid)


        display_notification("\033[93mFor multiple ports, use commas , (no space) eg : 8080,8081\033[0m")
        kharej_v2ray_port = input("\033[93mEnter \033[92mLocal\033[93m port:\033[0m ")
        iran_v2ray_port = input("\033[93mEnter \033[92mremote\033[93m port:\033[0m ")
        dashboard_user = input("\033[93mEnter the \033[92mDashboard username\033[93m: \033[0m")
        dashboard_pwd = input("\033[93mEnter the \033[92mDashboard password\033[93m: \033[0m")
        dashboard_port = input("\033[93mEnter the \033[92mDashboard port\033[93m: \033[0m")
        bind_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m")
        if not bind_port:
           bind_port = "443"
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"

        print("\033[93m───────────────────────────────────────────────────────────────────────────────\033[0m")

        with open('frp/frps.toml', 'w') as frps_ini:
            frps_ini.write(f'''[common]
bind_port = {bind_port}
vhost_https_port = {load_port}
transport.tls.disable_custom_tls_first_byte = false
token = azumi
dashboard_port = {dashboard_port}
dashboard_user = {dashboard_user}
dashboard_pwd = {dashboard_pwd}
dashboard_tls_mode = true
dashboard_tls_cert_file = /etc/letsencrypt/live/{domain}/fullchain.pem
dashboard_tls_key_file = /etc/letsencrypt/live/{domain}/privkey.pem

[v2ray]
type = tcp
local_ip = 127.0.0.1
local_port = {iran_v2ray_port}
remote_port = {kharej_v2ray_port}
use_encryption = true
use_compression = true
''')

        service_name = "azumifrps3"
        frps_path = "/root/frp/frps.toml"

        service_content = f'''[Unit]
Description=frps service
After=network.target

[Service]
ExecStart=/root/frp/./frps -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

        service_path = "/etc/systemd/system/{}.service".format(service_name)

        with open(service_path, 'w') as service_file:
            service_file.write(service_content)

        display_checkmark("\033[92mIran configuration With Dashboard generated. Yours Truly, Azumi!\033[0m")
        time.sleep(1)

        subprocess.run(['systemctl', 'start', 'nginx'], check=True)
        subprocess.run(['systemctl', 'daemon-reload'], check=True)
        subprocess.run(['sudo', 'chmod', 'u+x', '/etc/systemd/system/{}.service'.format(service_name)], check=True)
        subprocess.run(['systemctl', 'enable', service_name], check=True)
        subprocess.run(['systemctl', 'restart', service_name], check=True)
        res_i()
        display_checkmark("\033[92mFRP Service Started!\033[0m")
        
        time.sleep(1)
        create_decorated_box("Your Dashboard Address: https://{}:{}".format(domain, dashboard_port))
        create_decorated_box("Username: {}".format(dashboard_user))
        create_decorated_box("Password: {}".format(dashboard_pwd))

    except Exception as e:
        print("\033[91mAn error occurred while setting up Iran - With Dashboard.\033[0m")
        print(f"Error Details: {str(e)}")

        if loading_bar_pid:
            stop_loading(loading_bar_pid)



        print("\033[91mSetup failed. Please try again.\033[0m")
            
def i1kharej_3iran():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92m[1]\033[96mKharej \033[92m[3]\033[96mIRAN\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ\033[0m')
    print('2. \033[93mIRAN\033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            i3kharej()
            break
        elif server_type == '2':
            i3iran()
            break
        elif server_type == '3':
            os.system('clear')
            main_menu()
            break
        else:
            print('Invalid choice.') 
      
            
def i3iran():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92m[1]\033[96mKharej \033[92m[3]\033[96mIRAN\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[91mIRAN Server \033[92m[1]\033[0m')
    print('2. \033[97mIRAN Server \033[92m[2]\033[0m')
    print('3. \033[93mIRAN Server \033[92m[3]\033[0m')
    print('4. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            i3iran_first()
            break
        elif server_type == '2':
            i3iran_second()
            break
        elif server_type == '3':
            i3iran_third()
            break
        elif server_type == '4':
            os.system('clear')
            i1kharej_3iran()
            break
        else:
            print('Invalid choice.') 
            
def i3kharej():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mKharej \033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[96mMethod 1 [IPV6] \033[0m')
    print('2. \033[97mMethod 2 [LocalIP]\033[0m')
    print('3. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            i3kharej_ipv6()
            break
        elif server_type == '2':
            i3kharej_local()
            break
        elif server_type == '3':
            os.system('clear')
            i1kharej_3iran()
            break
        else:
            print('Invalid choice.')             

def i3kharej_ipv6():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mKharej IPV6\033[93m Method \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭─────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[96m  Since we are using Loadblance, you should specify how many loadbalance group you want")
    print("\033[97m  For example : if you have 2 config with different port, you create 2 loadbalance groups")
    print("\033[92m  Then you should specify how many IRAN server you have")
    print("\033[93m  Then based on that, you should enter Local & Remote port for each IRAN server")
    print("\033[96m  For example : i have 2 iran servers. i also have 2 configs with different ports on the kahrej server")
    print("\033[93m  I create 2 loadbalance groups and for each loadbalance group, i specify local and remote ports")
    print("\033[92m  I also need to do the same thing for the next iran server since i have 2 iran servers.")
    print("\033[96m  For each loadbalance group, i also sepcify one or tow IPV6 address")
    print("\033[93m╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮") 
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")
    
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")
    
    while True:
        try:
            num_iran_servers = int(input("\033[93mEnter the number of \033[92mIRAN\033[93m servers:\033[0m "))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")
    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)

    for server_num in range(1, num_iran_servers + 1):
        frpc_path = "frp/frpc{}.toml".format(server_num)
        if os.path.exists(frpc_path):
            os.remove(frpc_path)

    frpc1_path = "frp/frpc1.toml"
    if not os.path.exists(frpc1_path):
        with open(frpc1_path, "w") as f:
            f.write("[common]\n")
            f.write("server_addr = SERVER_IP\n")
            server_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m")
            if not server_port:
                server_port = "443"
            f.write("server_port = {}\n".format(server_port))
            load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
            if not load_port:
                load_port = "8443"
            f.write("vhost_https_port = {}\n".format(load_port))
            f.write("transport.tls.disable_custom_tls_first_byte = false\n")
            f.write("token = azumi\n")

    for server_num in range(2, num_iran_servers + 1):
        frpc_path = "frp/frpc{}.toml".format(server_num)
        shutil.copyfile(frpc1_path, frpc_path)

    for server_num in range(1, num_iran_servers + 1):
        iran_ipv6 = input("\033[93mEnter \033[92mIRAN IPv6 \033[93maddress for Server \033[92m{}:\033[0m ".format(server_num))

        frpc_path = "frp/frpc{}.toml".format(server_num)

        with open(frpc_path, "w") as f:
            f.write("[common]\n")
            f.write("server_addr = {}\n".format(iran_ipv6))
            f.write("server_port = {}\n".format(server_port))
            f.write("vhost_https_port = 8443\n")
            f.write("transport.tls.disable_custom_tls_first_byte = false\n")
            f.write("token = azumi\n")

        for group_index, group in enumerate(groups):
            group_name = group["name"]
            local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
            remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
            ipv6_count = int(input("\033[93mEnter the number of IPv6 addresses needed for \033[92m{}\033[93m:\033[0m ".format(group_name)))
            ipv6_addresses = []
            for i in range(ipv6_count):
                ipv6_address = input("\033[93mEnter \033[92mKharej\033[93m IPv6 address {} for \033[92m{}\033[93m:\033[0m ".format(i + 1, group_name))
                ipv6_addresses.append(ipv6_address)
            print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

            v2ray_number = group_index + 1

            with open(frpc_path, "a") as f:
                f.write("\n")
                f.write("[v2ray{}]\n".format(v2ray_number))
                f.write("type = tcp\n")
                if ipv6_count == 0:
                    f.write("local_ip = 127.0.0.1\n")
                else:
                    f.write("local_ip = {}\n".format(" ".join(ipv6_addresses)))
                f.write("local_port = {}\n".format(local_port))
                f.write("remote_port = {}\n".format(remote_port))
                f.write("group = Azumi{}\n".format(group_index + 1))
                f.write("group_key = azumichwan\n")
                f.write("health_check_type = tcp\n")
                f.write("health_check_timeout_s = 3\n")
                f.write("health_check_max_failed = 3\n")
                f.write("health_check_interval_s = 10\n")
                f.write("use_encryption = true\n")
                f.write("use_compression = true\n")

        time.sleep(1)


        service_name = "azumifrpc1{}".format(server_num)
        frpc_path = "/root/frp/frpc{}.toml".format(server_num)

        service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frpc_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

        service_path = "/etc/systemd/system/{}.service".format(service_name)

        with open(service_path, "w") as f:
            f.write(service_content)

        os.system("systemctl daemon-reload")
        os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
        os.system("systemctl enable {}".format(service_name))
        os.system("systemctl restart {}".format(service_name))
        res_ki3()
        display_checkmark("\033[92mFRP Service Started!\033[0m")

def i3kharej_local():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mKharej LocalIP\033[93m Method \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭─────────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[96m  Since we are using Loadblance, you should specify how many loadbalance group you want")
    print("\033[97m  For example : if you have 2 config with different port, you create 2 loadbalance groups")
    print("\033[92m  Then you should specify how many IRAN server you have")
    print("\033[93m  Then based on that, you should enter Local & Remote port for each IRAN server")
    print("\033[96m  For example : i have 2 iran servers. i also have 2 configs with different ports on the kahrej server")
    print("\033[93m  I create 2 loadbalance groups and for each loadbalance group, i specify local and remote ports")
    print("\033[92m  I also need to do the same thing for the next iran server since i have 2 iran servers.")
    print("\033[93m╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮") 
    while True:
        try:
            num_groups = int(input("\033[93mEnter the number of \033[92mloadbalance groups\033[96m [For each different port, there should be a group\033[92m]: \033[0m"))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")
    
    print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")
    
    while True:
        try:
            num_iran_servers = int(input("\033[93mEnter the number of \033[92mIRAN\033[93m servers:\033[0m "))
            break
        except ValueError:
            print("\033[91mInvalid input! Please enter a valid input!!\033[0m")

    groups = []
    for i in range(num_groups):
        group_name = "Loadbalance Group {}".format(i + 1)
        group = {"name": group_name}
        groups.append(group)

    time.sleep(1)


    for server_num in range(1, num_iran_servers + 1):
        frpc_path = "frp/frpc{}.toml".format(server_num)
        if os.path.exists(frpc_path):
            os.remove(frpc_path)

    frpc1_path = "frp/frpc1.toml"
    if not os.path.exists(frpc1_path):
        with open(frpc1_path, "w") as f:
            f.write("[common]\n")
            f.write("server_addr = SERVER_IP\n")
            server_port = input("\033[93mEnter \033[92mTunnel port\033[93m : \033[0m")
            if not server_port:
                server_port = "443"
            f.write("server_port = {}\n".format(server_port))
            load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
            if not load_port:
                load_port = "8443"
            f.write("vhost_https_port = {}\n".format(load_port))
            f.write("transport.tls.disable_custom_tls_first_byte = false\n")
            f.write("token = azumi\n")

    for server_num in range(2, num_iran_servers + 1):
        frpc_path = "frp/frpc{}.toml".format(server_num)
        shutil.copyfile(frpc1_path, frpc_path)

    for server_num in range(1, num_iran_servers + 1):
        iran_ipv6 = input("\033[93mEnter \033[92mIRAN IPV4/IPv6 \033[93maddress for Server \033[92m{}:\033[0m ".format(server_num))

        frpc_path = "frp/frpc{}.toml".format(server_num)

        with open(frpc_path, "w") as f:  
            f.write("[common]\n")
            f.write("server_addr = {}\n".format(iran_ipv6))
            f.write("server_port = {}\n".format(server_port))
            f.write("vhost_https_port = {}\n".format(load_port))
            f.write("transport.tls.disable_custom_tls_first_byte = false\n")
            f.write("token = azumi\n")

        for group_index, group in enumerate(groups):
            group_name = group["name"]
            local_port = input("\033[93mEnter the \033[92mLocal\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
            remote_port = input("\033[93mEnter the \033[92mRemote\033[93m Port for \033[92m{}\033[93m:\033[0m ".format(group_name))
            print("\033[93m───────────────────────────────────────────────────────────────────────────────────────\033[0m")

            v2ray_number = group_index + 1

            with open(frpc_path, "a") as f:
                f.write("\n")
                f.write("[v2ray{}]\n".format(v2ray_number))
                f.write("type = tcp\n")
                f.write("local_ip = 127.0.0.1\n")
                f.write("local_port = {}\n".format(local_port))
                f.write("remote_port = {}\n".format(remote_port))
                f.write("group = Azumi{}\n".format(group_index + 1))
                f.write("group_key = azumichwan\n")
                f.write("health_check_type = tcp\n")
                f.write("health_check_timeout_s = 3\n")
                f.write("health_check_max_failed = 3\n")
                f.write("health_check_interval_s = 10\n")
                f.write("use_encryption = true\n")
                f.write("use_compression = true\n")

        time.sleep(1)


        service_name = "azumifrpc1{}".format(server_num)
        frpc_path = "/root/frp/frpc{}.toml".format(server_num)

        service_content = f'''[Unit]
Description=frpc service
After=network.target

[Service]
ExecStart=/root/frp/./frpc -c {frpc_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

        service_path = "/etc/systemd/system/{}.service".format(service_name)

        with open(service_path, "w") as f:
            f.write(service_content)

        os.system("systemctl daemon-reload")
        os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
        os.system("systemctl enable {}".format(service_name))
        os.system("systemctl restart {}".format(service_name))
        res_ki3()
        display_checkmark("\033[92mFRP Service Started!\033[0m")

    
def i3iran_first():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mIRAN \033[93mServer \033[92m[1] \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Configure IRAN server first and then Kharej server")
    print("\033[93m  If you have different ports on Kharej server, Specify Port range for local and remot inputs")
    print("\033[96m  For example, if you have 2 configs with 8080 and 8081 ports, you specify 8080,8081 for local/remote ")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮") 
    local_ports = input("\033[93mEnter the \033[92mlocal\033[93m ports : \033[0m")
    remote_ports = input("\033[93mEnter the \033[92mremote\033[93m ports : \033[0m")

    local_ports_list = local_ports.replace(" ", ",").split(",")
    remote_ports_list = remote_ports.replace(" ", ",").split(",")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")

    local_ports_list = [port.strip() for port in local_ports_list]
    remote_ports_list = [port.strip() for port in remote_ports_list]

    num_instances = len(local_ports_list)

    if os.path.exists("frp/frps.toml"):
        os.remove("frp/frps.toml")

    with open("frp/frps.toml", "w") as f:
        f.write("[common]\n")
        bind_port = input("\033[93mEnter \033[92mTunnel Port\033[93m : \033[0m")
        if not bind_port:
            bind_port = "443"
        f.write("bind_port = {}\n".format(bind_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")
        f.write("\n")
        f.write("[v2ray]\n") 
        f.write("type = tcp\n")
        f.write("local_port = {}\n".format(",".join(local_ports_list)))
        f.write("remote_port = {}\n".format(",".join(remote_ports_list)))
        f.write("use_encryption = true\n")
        f.write("use_compression = true\n")

    display_checkmark("\033[92mIRAN configuration generated. Yours Truly, Azumi.\033[0m")


    service_name = "azumifrps4"
    frps_path = "/root/frp/frps.toml"

    service_content = f'''[Unit]
Description=frps service
After=network.target

[Service]
ExecStart=/root/frp/./frps -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)
        
    display_notification("\033[93mStarting FRP service...\033[0m")
    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_ii3()
    display_checkmark("\033[92mFRP Service Started!\033[0m")
    
def i3iran_second():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mIRAN \033[93mServer \033[92m[2] \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Configure IRAN server first and then Kharej server")
    print("\033[93m  If you have different ports on Kharej server, Specify Port range for local and remot inputs")
    print("\033[96m  For example, if you have 2 configs with 8080 and 8081 ports, you specify 8080,8081 for local/remote ")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮") 
    local_ports = input("\033[93mEnter the \033[92mlocal\033[93m ports : \033[0m")
    remote_ports = input("\033[93mEnter the \033[92mremote\033[93m ports : \033[0m")

    local_ports_list = local_ports.replace(" ", ",").split(",")
    remote_ports_list = remote_ports.replace(" ", ",").split(",")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")

    local_ports_list = [port.strip() for port in local_ports_list]
    remote_ports_list = [port.strip() for port in remote_ports_list]

    num_instances = len(local_ports_list)

    if os.path.exists("frp/frps.toml"):
        os.remove("frp/frps.toml")

    with open("frp/frps.toml", "w") as f:
        f.write("[common]\n")
        bind_port = input("\033[93mEnter \033[92mTunnel Port\033[93m (default 443): \033[0m")
        if not bind_port:
            bind_port = "443"
        f.write("bind_port = {}\n".format(bind_port))
        f.write("vhost_https_port = 8443\n")
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")
        f.write("\n")
        f.write("[v2ray]\n") 
        f.write("type = tcp\n")
        f.write("local_port = {}\n".format(",".join(local_ports_list)))
        f.write("remote_port = {}\n".format(",".join(remote_ports_list)))
        f.write("use_encryption = true\n")
        f.write("use_compression = true\n")

    display_checkmark("\033[92mIRAN configuration generated. Yours Truly, Azumi.\033[0m")


    service_name = "azumifrps4"
    frps_path = "/root/frp/frps.toml"

    service_content = f'''[Unit]
Description=frps service
After=network.target

[Service]
ExecStart=/root/frp/./frps -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)
        
    display_notification("\033[93mStarting FRP service...\033[0m")
    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_ii3()
    display_checkmark("\033[92mFRP Service Started!\033[0m")
    
def i3iran_third():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mIRAN \033[93mServer \033[92m[3] \033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Configure IRAN server first and then Kharej server")
    print("\033[93m  If you have different ports on Kharej server, Specify Port range for local and remot inputs")
    print("\033[96m  For example, if you have 2 configs with 8080 and 8081 ports, you specify 8080,8081 for local/remote ")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────────╮") 
    local_ports = input("\033[93mEnter the \033[92mlocal\033[93m ports : \033[0m")
    remote_ports = input("\033[93mEnter the \033[92mremote\033[93m ports : \033[0m")

    local_ports_list = local_ports.replace(" ", ",").split(",")
    remote_ports_list = remote_ports.replace(" ", ",").split(",")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────────╯\033[0m")

    local_ports_list = [port.strip() for port in local_ports_list]
    remote_ports_list = [port.strip() for port in remote_ports_list]

    num_instances = len(local_ports_list)

    if os.path.exists("frp/frps.toml"):
        os.remove("frp/frps.toml")

    with open("frp/frps.toml", "w") as f:
        f.write("[common]\n")
        bind_port = input("\033[93mEnter \033[92mTunnel Port\033[93m : \033[0m")
        if not bind_port:
            bind_port = "443"
        f.write("bind_port = {}\n".format(bind_port))
        load_port = input("\033[93mEnter \033[92mLoadbalance Port\033[93m(default 8443): \033[0m")
        if not load_port:
            load_port = "8443"
        f.write("vhost_https_port = {}\n".format(load_port))
        f.write("transport.tls.disable_custom_tls_first_byte = false\n")
        f.write("token = azumi\n")
        f.write("\n")
        f.write("[v2ray]\n") 
        f.write("type = tcp\n")
        f.write("local_port = {}\n".format(",".join(local_ports_list)))
        f.write("remote_port = {}\n".format(",".join(remote_ports_list)))
        f.write("use_encryption = true\n")
        f.write("use_compression = true\n")

    display_checkmark("\033[92mIRAN configuration generated. Yours Truly, Azumi.\033[0m")


    service_name = "azumifrps4"
    frps_path = "/root/frp/frps.toml"

    service_content = f'''[Unit]
Description=frps service
After=network.target

[Service]
ExecStart=/root/frp/./frps -c {frps_path}
Restart=always
RestartSec=5
LimitNOFILE=1048576
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)
        
    display_notification("\033[93mStarting FRP service...\033[0m")
    os.system("systemctl daemon-reload")
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl enable {}".format(service_name))
    os.system("systemctl restart {}".format(service_name))
    res_ii3()
    display_checkmark("\033[92mFRP Service Started!\033[0m")
    
main_menu()
