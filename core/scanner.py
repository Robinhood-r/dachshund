import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock


# Doing a check for errors epending on which way the user tries to use the program
try:
    from core.http_analyzer import http_probe
except ImportError:
    from http_analyzer import http_probe

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
 ██████╗  █████╗  ██████╗██╗  ██╗███████╗██╗  ██╗██╗   ██╗███╗   ██╗██████╗ 
 ██╔══██╗██╔══██╗██╔════╝██║  ██║██╔════╝██║  ██║██║   ██║████╗  ██║██╔══██╗
 ██║  ██║███████║██║     ███████║███████╗███████║██║   ██║██╔██╗ ██║██║  ██║
 ██║  ██║██╔══██║██║     ██╔══██║╚════██║██╔══██║██║   ██║██║╚██╗██║██║  ██║
 ██████╔╝██║  ██║╚██████╗██║  ██║███████║██║  ██║╚██████╔╝██║ ╚████║██████╔╝
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝ 
{RESET}
{YELLOW}Enumerate subdomains like a hound!!!{RESET}
{RESET}{BOLD}
        :: URL       : {url}
        :: Wordlist  : {wordlist_path} ({total} entries)
        :: Threads   : {threads}
 {RESET}{'-' * 60}
    """)

# This is the main scan function
def run_scan(url_template, wordlist_path, threads=40, output=None, timeout=5.0, match_codes=None):

    # Checks to see if there is a match code provided 
    if match_codes is None:
        match_codes = [200]

    # Checks to see if the word FUZZ is in the url
    if "FUZZ" not in url_template:
        raise ValueError("url_template must contain FUZZ, e.g. FUZZ.example.com")

    # Calls the function to load the wordlist and counts how many words are in the list(total)_
    words = load_wordlist(wordlist_path)
    total = len(words)
    # Calls the print_info function so the user can see whats about to run
    print_info(url_template, wordlist_path, threads, total)

    found = []
    done=0
    start = time.time()

    def worker(word):
        # Swaps the word FUZZ with the word(s) in the wordlist and returns both values at once(hostname and timeout)
        url = url_template.replace("FUZZ", word)
        return url, http_probe(url, timeout)

    # Creates a pool of workers and tells the worker to not wait for job to finish on another thread. Assign it to a thread as soon as one is free.
    with ThreadPoolExecutor(max_workers=threads) as executer:
        futures = [executer.submit(worker, w) for w in words]

        print()
        # It gives us each feature as soon at it finishes,whenever they complete and gets the actual return value from the completed worder function.
        for future in as_completed(futures):
            url, status_code = future.result()
            
            with print_lock:
                done += 1
                if status_code in  match_codes:
                  found.append((url, status_code))
                  sys.stdout.write("\r" + " " * 60 + "\r")
                  print(f"{GREEN}{url:<50}{RESET} [{status_code}]")
                sys.stdout.write(f"\r{YELLOW}:: Progress: [{done}/{total}]{RESET}")
                sys.stdout.flush()       
                

    
    # Calculates the the total time taken for the process after all the thread pools are done.
    elapsed = time.time() - start
    print()      
    print(f"\n{'-' * 60}")
    print(f"{BOLD}:: Done in {elapsed:.2f}s — {len(found)} found{RESET}")

    # Checks to see if the user has provided an output and opens the file in writing mode and writes the results in them
    if output:
        with open(output, "w") as f:
            for url, status_code in found:
                f.write(f"{url} {status_code}\n")
        print(f":: Results saved to {output}")

    # Returns the found list
    return found

# Tests the file 
if __name__ == "__main__":
    run_scan("https://www.google.com/FUZZ", "/run/media/dan/Dev/SecLists-master/Discovery/Web-Content/raft-medium-words-lowercase.txt")                