import argparse
from core.scanner import run_scan

def main():
    # Defines an arguments parser that will read the command line flags
    parser = argparse.ArgumentParser(
        prog="dachshund",
        description="Dachshund - sniff out subdomains and paths like a hound!!!"
    )
    
    # Setting the arguments and their requirements
    parser.add_argument("-u", "--url", required=True, help="Target with FUZZ keyword, e.g. FUZZ.example.com")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist")
    parser.add_argument("-t", "--threads", type=int, default=40, help="Threads (default: 40)")
    parser.add_argument("-o", "--output", help="Save results to file")
    parser.add_argument("--timeout", type=float, default=5.0, help="HTTP timeout in seconds (default: 5.0)")
    parser.add_argument("-mc", "--match-codes", default="200", help="Comma-separated status codes to match, e.g. 200,301,403 (default: 200)")

    args = parser.parse_args()

    # Checks to see if there is the word FUZZ in the provided url
    if "FUZZ" not in args.url:
        parser.error("URL must contain FUZZ, e.g. example.com/FUZZ")

    # Turn "200,301,403" into [200, 301, 403]
    match_codes = [int(code.strip()) for code in args.match_codes.split(",")]

    # Runs the main function
    run_scan(url_template=args.url, wordlist_path=args.wordlist, threads=args.threads, output=args.output, timeout=args.timeout, match_codes=match_codes)


if __name__ == "__main__":
    main()