import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock


# Doing a check for errors epending on which way the user tries to use the program
try:
    from core.dns_lookup import dns_lookup
except ImportError:
    from dns_lookup import dns_lookup


# Settting ANSI values to color names
GREEN, YELLOW, CYAN, BOLD, RESET = "\033[92m", "\033[93m", "\033[96m", "\033[1m", "\033[0m"

# Creating a lock object so each thread can hold one at a time
print_lock = Lock()

# Defining a function to read a file(wordlist) and returning a clean Pythini list of words by stripping the whitespace in each line
def load_wordlist(path):
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]


# Printing the banner when the program is called
def print_info(url, wordlist_path, threads, total):

      print(f"""{CYAN}{BOLD}
        dachshund - subdomain enumeration
 {RESET}{BOLD}
        :: URL       : {url}
        :: Wordlist  : {wordlist_path} ({total} entries)
        :: Threads   : {threads}
 {RESET}{'-' * 60}
    """)

    