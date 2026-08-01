# Dachshund

enumerate subdomains like a hound!!!

## What it does

**Dachshund** works by using the ```FUZZ``` keyword which can be placed anywhere in  a URL, subdomain position or a path position.
It checks HTTP responses and supports custom code matching(```-mc```).

It's multi threaded for faster enumeration speed and can save the results of each scan into a file.


## Installation 
 1. Clone the repository:
    ```
    git clone https://github.com/Robinhood-r/dachshund
    ```
 2. Navigate to the project folder:
    ```
    cd dachshund
    ```
 3. Install the program using pip:
    ```
    pip install --break-system-packages .
    ```
 4. Start using the Tool!

 Example command: ```dashi -u "https://example.com/FUZZ" -w path/to/wordlist.txt```

 ## Flags

 ```
-u   URL to fuzz. Must contain FUZZ, e.g. https://example.com/FUZZ
-w   Path to wordlist
-t   Threads (default: 40)
-o   Save results to a file
--timeout   HTTP timeout in seconds (default: 5.0)
-mc  Comma-separated HTTP status codes to match, e.g. 200,301,403
```

## Example output




## Author
Danial R — Cybersecurity enthusiast and aspiring bug bounty hunter

