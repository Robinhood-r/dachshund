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

# This is the main scan function
def run_scan(url_template, wordlist_path, threads=40, output=None, timeout=20):

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
        hostname = url_template.replace("FUZZ", word)
        return hostname, dns_lookup(hostname, timeout)

    # Creates a pool of workers and tells the worker to not wait for job to finish on another thread. Assign it to a thread as soon as one is free.
    with ThreadPoolExecutor(max_workers=threads) as executer:
        futures = [executer.submit(worker, w) for w in words]

        print()
        # It gives us each feature as soon at it finishes,whenever they complete and gets the actual return value from the completed worder function.
        for future in as_completed(futures):
            hostname, ip = future.result()
            #
            with print_lock:
                done += 1
                if ip:
                    found.append((hostname, ip))
                    sys.stdout.write("\r" + " " * 60 + "\r")
                    print(f"{GREEN}{hostname:<40}{RESET} [FOUND: {ip}]")
                
                sys.stdout.flush()

    
    # Calculates the the total time taken for the process after all the thread pools are done.
    elapsed = time.time() - start

    print()
      
    print(f"{YELLOW}:: Progress: [{done}/{total}]{RESET}")
    print('-' * 60)
    print(f"{BOLD}:: Done in {elapsed:.2f}s — {len(found)} found{RESET}")

    # Checks to see if the user has provided an output and opens the file in writing mode and writes the results in them
    if output:
        with open(output, "w") as f:
            for hostname, ip in found:
                f.write(f"{hostname} {ip}\n")
        print(f":: Results saved to {output}")

    # Returns the found list
    return found

# Tests the file 
if __name__ == "__main__":
    run_scan("FUZZ.google.com", "/run/media/dan/Dev/Github/dachshund/core/test_wordlist.txt")                