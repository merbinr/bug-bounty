import requests
import time


CRT_ON_ERROR_SLEEP_TIME = 30

class CrtShHelper:
    def __init__(self, domain: str) -> None:
        self.domain = domain
        self.crt_url = f"https://crt.sh/?Identity={domain.strip()}&exclude=expired&match=ILIKE&deduplicate=Y&output=json"

    def _process_output(self, data: dict) -> dict:
        """_summary_

        Args:
            data dict: crtsh output

        Returns:
            dict: {"domains" : ["b.a.com"], "wildcards" : ["*.a.com"]}
        """
        domains = []
        wildcards = []

        for each_entry in data:
            name_values: list = each_entry.get("name_value").split("\n")
            for each_name in name_values:
                each_name: str
                if each_name.startswith("*"):
                    wildcards.append(each_name.strip().removeprefix("*."))
                else:
                    domains.append(each_name.strip())
        return {
            "domains" : list(set(domains)),
            "wildcards" : list(set(wildcards))
        }

    def fetch_domains(self) -> dict:
        """ 
        Retruns filtered output from crt.sh

        Returns:
            dict: {"domains" : ["b.a.com"], "wildcards" : ["a.com"]}
        """
        while True:
            res = requests.get(url=self.crt_url)
            status_code = res.status_code
            if status_code == 200:
                output = self._process_output(data=res.json())
                return output
            else:
                print(f"Got {status_code} status code from crtsh, retring in {CRT_ON_ERROR_SLEEP_TIME} sec")
                time.sleep(CRT_ON_ERROR_SLEEP_TIME)


