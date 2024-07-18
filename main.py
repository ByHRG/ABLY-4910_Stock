import requests
import json
import httpx

class ABLY:
    def cookie_setting(self):
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Priority': 'u=0, i',
            'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
        req = httpx.get("https://m.a-bly.com/", headers=header)
        token = str(req.cookies).split("ably-anonymous-token=")[-1].split(" for")[0]
        header["X-Anonymous-Token"] = token
        return header

    def url_setting(self, url):
        return url.split("/")[-1].split("?")[0]

    def run(self, url):
        url = self.url_setting(url)
        header = self.cookie_setting()
        req = requests.get(f"https://api.a-bly.com/api/v2/goods/{url}/?channel=0", headers=header)
        output = {
            "Name": req.json()["goods"]["name"],
            "Model": req.json()["goods"]["sku_code"],
            "Image": f'https:{req.json()["goods"]["image"]}',
            "Price": req.json()["goods"]["price"],
            "Url": "https://m.a-bly.com/goods/" + str(url),
            "Stock": {},
        }
        one_depth = {}
        req = requests.get(f"https://api.a-bly.com/api/v2/goods/{url}/options/?depth=1", headers=header)
        for i in req.json()["option_components"]:
            one_depth.update({i["name"]:i["goods_option_sno"]})

        for key, value in one_depth.items():
            requests.options(f"https://api.a-bly.com/aglo/api/goods/{url}/options/?depth=2&selected_option_sno={value}", headers=header)
            req = requests.get(f"https://api.a-bly.com/aglo/api/goods/{url}/options/?depth=2&selected_option_sno={value}", headers=header)
            output["Stock"].update({key:req.json()["option_components"][0]["goods_option"]["stock"]})
        return output


url = "https://4910.kr/goods/10628422"
print(json.dumps(ABLY().run(url), ensure_ascii=False, indent=4))

