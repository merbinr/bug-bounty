from helpers.crtsh import CrtShHelper
from helpers.dns_bruteforce import DNSBruteforceHelper
from utils.logger import get_logger
from utils.filehandler import create_dir, write_lines_to_file

domain = "cargurus.com"

logger = get_logger()

def main():
    logger.info("Staring Crtscan...")
    crtsh_helper = CrtShHelper(domain=domain)
    data = crtsh_helper.fetch_domains()

    crt_out_dir_path = f"output/{domain}/crtsh"
    create_dir(crt_out_dir_path)
    subdomains = data.get("domains")

    write_lines_to_file(data=subdomains, path=f"{crt_out_dir_path}/subdomains.txt")
    wild_cards = data.get("wildcards")
    write_lines_to_file(data=wild_cards, path=f"{crt_out_dir_path}/wild_cards.txt")
    logger.info("Completed Crtscan...")

    logger.info("Staring DNS Bruteforce...")
    dns_bruteforce_helper = DNSBruteforceHelper(resolvers_path="data/dns_bruteforce/resolvers.txt", 
                                                domains_path=f"{crt_out_dir_path}/wild_cards.txt", 
                                                wordlist_path="data/dns_bruteforce/wordlist.txt", 
                                                output_parent_dir=f"output/{domain}/dns_bruteforce")
    dns_bruteforce_helper.perform_bruteforce()
    logger.info("Completed DNS Bruteforce...")


    # dns_bruteforce_helper = DNSBruteforceHelper(wildcard)
    # dns_bruteforced_data = dns_bruteforce_helper.perform_bruteforce()

    # with open("dns_brute_data.json", "w") as f:
    #     json.dump(dns_bruteforced_data, f, default=str)

if __name__=="__main__":
    main()
