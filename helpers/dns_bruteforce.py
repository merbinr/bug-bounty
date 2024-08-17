import subprocess


class DNSBruteforceHelper:
    def __init__(self, resolvers_path: str,
                 domains_path: str, wordlist_path: str,
                 output_parent_dir: str,
                 threads: int = 100) -> None:
        self.resolver_path = resolvers_path
        self.domains_path = domains_path
        self.wordlist_path = wordlist_path
        self.threads = threads
        self.output_dir = output_parent_dir
    
    def _check_the_bruteforce_binary(self):
        check_puredns = subprocess.run("which puredns", capture_output=True, shell=True)
        check_massdns = subprocess.run("which massdns", capture_output=True, shell=True)
        if check_puredns.returncode != 0 or check_massdns.returncode !=0:
            FileNotFoundError("puredns or massdns not found!, existing..")
            exit(1)

    def perform_bruteforce(self):
        self._check_the_bruteforce_binary()
        cmd = f"""puredns bruteforce {self.wordlist_path} \
                -d {self.domains_path} \
                --resolvers {self.resolver_path} \
                --rate-limit {self.threads} \
                --write {self.output_dir}/subdomains.txt \
                --write-wildcards {self.output_dir}/wildcards.txt 
                """
        cmd_output = subprocess.run(cmd, capture_output=True, shell=True)
        if cmd_output.returncode != 0:
            print(f"DNS bruteforce completed with non zero exit code: {cmd_output.returncode}\n\
                  stderr: {cmd_output.stderr}")
    


