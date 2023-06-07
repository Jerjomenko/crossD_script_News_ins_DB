import os
import requests


cookies = {
    'atuserid': '%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%22a39202f2-dc03-44d3-8f27-24d2b9ba19df%22%2C%22options%22%3A%7B%22end%22%3A%222024-05-28T07%3A52%3A11.545Z%22%2C%22path%22%3A%22%2F%22%7D%7D',
}

headers = {
    'authority': 'www.sportschau.de',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6',
    'cache-control': 'max-age=0',
    # 'cookie': 'atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%22a39202f2-dc03-44d3-8f27-24d2b9ba19df%22%2C%22options%22%3A%7B%22end%22%3A%222024-05-28T07%3A52%3A11.545Z%22%2C%22path%22%3A%22%2F%22%7D%7D',
    'referer': 'https://www.google.com/',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}

response = requests.get('https://www.sportschau.de/thema/snooker', cookies=cookies, headers=headers)


def create_html_response(obj):

    if os.path.exists("result.html"):
        print("File already Exist...")
        pass
    else:
        with open("result.html", "w", encoding="utf-8") as file:
            file.write(obj.text)
            print("File result.html succesfull created...")


