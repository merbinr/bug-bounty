import dns.exception
import dns.resolver
import random
import string
from joblib import Parallel, delayed
import time
from tqdm import tqdm

SLEEP_BETWEEN_REQUESTS = 0.001
NUMBER_OF_THREADS = 100

class DNSBruteforceHelper:
    def __init__(self, wildcards: list[str], 
                 wordlist_path="wordlist_tiny.txt", 
                 resolvers_path="resolvers.txt" ) -> None:
        self.wildcards = wildcards
        self.wordlist_path = wordlist_path
        self.resolvers = self._read_resolvers(path=resolvers_path)

    def _read_resolvers(self, path: str) -> list[str]:
        with open(path) as f:
            return f.read().splitlines()

    def _check_pre_scan(self, target: str):
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['8.8.8.8', '8.8.4.4']
        resolver.timeout = 10
        record_type = 'NS'
        random_string = self._generate_random_string()
        target = f"{random_string}.{target}"

        try:
            answers = resolver.resolve(target, record_type)
            for answer in answers:
                print(f'{record_type} record for {target}: {answer.to_text()}')
        except dns.resolver.NXDOMAIN:
            # Not found
            return True
        except dns.exception.Timeout:
            pass
        except Exception as e:
            print(f'An error occurred: {e}')
        return False

    def _generate_random_string(self, length=8):
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(length))

        
    def _prepare_scan(self, target: str):
        number_of_resolvers = len(self.resolvers)
        index = 0
        for word in self._read_wordlist(filepath=self.wordlist_path):
            word = word.strip()
            if index >= (number_of_resolvers):
                index = 0
            data = {
                "target" : f"{word}.{target}",
                "resolver" : self.resolvers[index]
                }
            index = index + 1
            yield data


    def _read_wordlist(self, filepath: str):
        with open(filepath) as f:
            for each_word in f:
                yield each_word

    def _scan(self, prepared_target: dict):
        # time.sleep(SLEEP_BETWEEN_REQUESTS)
        resolver_address = prepared_target.get("resolver")
        target = prepared_target.get("target")
        resolver = dns.resolver.Resolver()
        resolver.timeout = 10
        resolver.nameservers = [resolver_address]
        record_type = 'NS'
        try:
            answers = resolver.resolve(target, record_type)
            for answer in answers:
                # valid sub
                return target
        except dns.resolver.NoAnswer:
            # valid sub
            return target
        
        except:
            # invalid sub
            return
        

    def perform_bruteforce(self):
        output = []
        for target in self.wildcards:
            target = target.removeprefix("*.").strip()
            pre_check_passed = self._check_pre_scan(target=target)
            if not pre_check_passed:
                output.append({
                    "wildcard_dns_record" : True,
                    "domain" : target,
                    "subdomains" : []
                })
                continue

            prepared_targets = self._prepare_scan(target=target)
            subdomains_unfiltered = Parallel(n_jobs=NUMBER_OF_THREADS, prefer="threads")(
                delayed(self._scan)(target_data) for target_data in tqdm(prepared_targets))
            valid_subdomains = []
            for subdomain in subdomains_unfiltered:
                if subdomain:
                    valid_subdomains.append(subdomain)
            output.append({
                    "wildcard_dns_record" : False,
                    "domain" : target,
                    "subdomains" : valid_subdomains
                })
        return output



