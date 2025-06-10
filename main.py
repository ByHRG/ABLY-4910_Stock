import json
import time

import httpx

class ABLY:
    def cookie_setting(self):
        header = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://4910.kr',
            'priority': 'u=1, i',
            'referer': 'https://4910.kr/',
            'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
        }
        req = httpx.get("https://4910.kr/", headers=header)
        token = str(req.headers).split("ably-anonymous-token=")[-1].split(";")[0]
        header["X-Anonymous-Token"] = f"{token}"
        return header

    def url_setting(self, url):
        return url.split("/")[-1].split("?")[0]

    def run(self, url):
        url = self.url_setting(url)
        header = self.cookie_setting()
        header["x-app-type"] = "AGLO"
        header["x-app-version"] = "0.1.0"
        header["x-device-type"] = "PCWeb"
        header["Cookie"] = '__cf_bm=RMYx.0ChZAcr0F8.pX49A3FLw_F1JLD0pnaUopduO6c-1749537441-1.0.1.1-dFHMDTzG0Lxe0bMOWBuLVVtFc5.jvaficIr7FAkZhcpo7WvzX8xqyySjn7rwPTOzfmfg7q_oqTJYle7R83ujaCBrYhWpGqJsGgZWDRPBx2I'
        output = {
            "Url": "https://m.a-bly.com/goods/" + str(url),
            "Stock": {},
        }
        one_depth = {}
        req = httpx.get(f"https://api.a-bly.com/aglo/api/goods/{url}/options/?depth=1", headers=header)
        for i in req.json()["option_components"]:
            one_depth.update({i["name"]:i["goods_option_sno"]})
        for key, value in one_depth.items():
            while True:
                try:
                    req = httpx.get(f"https://api.a-bly.com/aglo/api/goods/{url}/options/?depth=2&selected_option_sno={value}", headers=header)
                    output["Stock"].update({key:req.json()["option_components"][0]["goods_option"]["stock"]})
                    break
                except Exception as e:
                    time.sleep(0.5)
        return output


url = "https://4910.kr/goods/10628422"
print(json.dumps(ABLY().run(url), ensure_ascii=False, indent=4))
