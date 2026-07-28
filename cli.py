import argparse
from core.scanner import run_scan

def main():
    # Defines an arguments parser that will read the command line flags
    parser = argparse.ArgumentParser(
        prog="dachshund",
        description="Dachshund - a fast subdomain enumeration tool"
    )
    # Setting the arguments and their requirements
    parser.add_argument("-u", "--url", required=True, help="Target with FUZZ keyword, e.g. FUZZ.example.com")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist")
    parser.add_argument("-t", "--threads", type=int, default=40, help="Threads (default: 40)")
    parser.add_argument("-o", "--output", help="Save results to file")
    parser.add_argument("--timeout", type=float, default=2.0, help="DNS timeout in seconds")
    args = parser.parse_args()

    # Checks to see if there is the word FUZZ in the provided url
    if "FUZZ" not in args.url:
        parser.error("URL must contain FUZZ, e.g. FUZZ.example.com")

    # Runs the main function
    run_scan(args.url, args.wordlist, args.threads, args.output, args.timeout)

if __name__ == "__main__":
    main()