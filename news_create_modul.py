import io
import urllib.request
from io import BytesIO

import psycopg2
from PIL import Image
from bs4 import BeautifulSoup as Bs


class CreateHauptNewsFromFile:

    def __init__(self, name):
        self.name = name

    def create_h1(self):
        with open("html_ordner/" + self.name, encoding="utf-8") as f:
            obj = f.read()
            soup = Bs(obj, "html.parser")
            block = soup.find("div", class_="seitenkopf__title")
        if block:
            h1 = block.find("h1").find("span", class_="seitenkopf__headline--text").text
            return h1
        else:
            return " "

    def news_text(self):
        with open("html_ordner/" + self.name, encoding="utf-8") as f:
            obj = f.read()
            soup = Bs(obj, "html.parser")
            block = soup.find("article", class_="container content-wrapper__group")
            if block:
                p_list = block.find_all("p", class_="textabsatz")
                news_text = ""
                for i in p_list:
                    news_text += i.text
                news_text = news_text.replace("\n\n", "\n")
                return news_text
            else:
                return ""

    def create_img(self):
        with open("html_ordner/" + self.name, encoding="utf-8") as f:
            obj = f.read()
            soup = Bs(obj, "html.parser")
            block_img = soup.find("div", class_="ts-picture__wrapper").find("img")
            if block_img:
                img_link = block_img.get("src")
                with urllib.request.urlopen(img_link) as response:
                    image_data = response.read()
                name = self.name.replace(".html", "")
                with open("img/" + name + ".jpg", "wb") as f:
                    f.write(image_data)
                img_io = io.BytesIO(image_data)
                img_obj = Image.open(img_io)
                img_byte_array = io.BytesIO()
                img_obj.save(img_byte_array, format='JPEG')
                img_byte_array = img_byte_array.getvalue()
                return psycopg2.Binary(img_byte_array)
            else:
                print("Es gibt keinen bild zur dieser nachricht.")

    def date_author(self):
        text_date_author = ""
        with open("html_ordner/" + self.name, encoding="utf-8") as f:
            obj = f.read()
            soup = Bs(obj, "html.parser")
            block1 = soup.find("article", class_="container content-wrapper__group").find("p",
                                                                                          class_="metatextline").text
            if block1:
                text_date_author += block1
                block2 = soup.find("div", class_="backlink__author").text
                if block2:
                    text_date_author += "\n" + block2
                return text_date_author
            else:
                return ""


class CreateNewsFromFile:

    def __init__(self, name) -> None:
        self.name = name


    def create_h1(self):
        with open("html_ordner/"+self.name, encoding="utf-8") as f:
            obj = f.read()
            soup = Bs(obj, "html.parser")
            block = soup.find("div" , class_="seitenkopf__title")
            if block:
                h1 = block.find("h1").find("span", class_="seitenkopf__headline--text").text
                return h1
            else:
                return ""


    def news_text(self):
        with open("html_ordner/"+self.name, encoding="utf-8") as f:
            obj = f.read()
            soup = Bs(obj, "html.parser")
            block = soup.find("article", class_="container content-wrapper__group")
            if block:
                p_list = block.find_all("p", class_="textabsatz")
                news_text = ""
                for i in p_list:
                    news_text += i.text
                news_text = news_text.replace("\n", "")
                return news_text
            else:
                return ""

    def create_img(self):
        with open("html_ordner/"+self.name, encoding="utf-8") as f:
            obj = f.read()
            soup = Bs(obj, "html.parser")
            block_img = soup.find("article", class_="container content-wrapper__group").find("div", class_="ts-picture__wrapper").find("img")
            if block_img:
                img_link = block_img.get("src")
                with urllib.request.urlopen(img_link) as response:
                    image_data = response.read()
                img_name = self.name.replace(".html", "")
                with open("img/"+img_name+".jpg", "wb") as f:
                    f.write(image_data)
                img_io = io.BytesIO(image_data)
                img_obj = Image.open(img_io)
                img_byte_array = io.BytesIO()
                img_obj.save(img_byte_array, format='JPEG')
                img_byte_array = img_byte_array.getvalue()
                return psycopg2.Binary(img_byte_array)
            else:
                print("Es gibt keinen bild zur dieser nachricht.")


    def date_author(self):
        text_date_author = ""
        with open("html_ordner/"+self.name, encoding="utf-8") as f:
            obj = f.read()
            soup = Bs(obj, "html.parser")
            block1 = soup.find("article" , class_="container content-wrapper__group").find("p", class_="metatextline").text
            if block1:
                text_date_author += block1
                with open("html_ordner/"+self.name, encoding="utf-8") as f:
                    obj = f.read()
                    soup = Bs(obj, "html.parser")
                    block2 = soup.find("div" , class_="backlink__author").text
                    if block2:
                        text_date_author += "\n" + block2
                        return text_date_author
            else:
                return ""
