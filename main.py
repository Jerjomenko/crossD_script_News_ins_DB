import datetime
import os
import requests
from bs4 import BeautifulSoup as Bs
import psycopg2
from response_text import create_html_response, response, cookies, headers
from news_create_modul import CreateHauptNewsFromFile, CreateNewsFromFile
from postgres_cnf import postgre

create_html_response(response)
print("Файл result.html успешно создан.")
news_link_list = []

""" функция достаёт ссылку на главную новость. """
def link_haupt_news(obj):
  with open(obj, encoding="utf-8") as f:
    obj = f.read()
    soup = Bs(obj, "html.parser")
    block = soup.find("div", class_="teaser teaser--top").find("a")
    href = "https://www.sportschau.de" + block.get("href")
    return ("haupt_news", href)


""" функция парсит второй блок новостей и возвращает ссалки на саму новость. """
def nachrichten_list(obj):
    with open(obj, encoding="utf-8") as f:
        obj = f.read()
        soup = Bs(obj, "html.parser")
        block = soup.find_all("div", class_="teaser teaser--small")
        link_list = []
        for i in range(14):
            name = "news"+str(i)
            a = block[i].find("a")
            href = "https://www.sportschau.de"+ a.get("href")
            news_link_list.append((name, href))
        return link_list

haupt_news = link_haupt_news("result.html")
news_link_list.append(haupt_news)
nachrichten_list("result.html")
print("Создан список ссылок на все новости.")


""" данная функция создаёт все фаилы , для всех новостей. """
def create_all_news_htmls():
    for i in news_link_list:
        if "news" in i[0]:
            response = requests.get(i[1], cookies=cookies, headers=headers)
            with open(f"html_ordner/{i[0]}.html", "w", encoding="utf-8") as file:
                file.write(response.text)
                print(f"File {i[0]} succesfull created...")


create_all_news_htmls()
print("Созданы все файлы html на все новости.")

list_of_news_table = []

def create_obj_for_db():
    for filename in os.listdir("html_ordner/"):
        if "haupt_news" in filename:
            db_obj = CreateHauptNewsFromFile(filename)
            news_status = "1"
        else:
            db_obj = CreateNewsFromFile(filename)
            news_status = "0"
        news_name = filename.replace(".html", "")
        news_title = db_obj.create_h1()
        news_text = db_obj.news_text()
        news_img = db_obj.create_img()
        news_qwelle = db_obj.date_author()
        news_download_day = datetime.datetime.now()
        list_of_news_table.append((news_name, news_status, news_title, news_text, news_img, news_qwelle, news_download_day))


create_obj_for_db()
print("Все страницы спарсены и данные дабавленны в список  list_of_news_table для дальнейшего сохранения в БД.")

""" функция добовляет данные в Базу Данных """
def insert_haupt_news():
    with psycopg2.connect(**postgre) as conn:
        print("Succesfull Connected....")
        for i in range(1, len(list_of_news_table)+1):
            with conn.cursor() as cur:
                # Überprüfen, ob die Daten bereits vorhanden sind
                cur.execute(f"SELECT * FROM news WHERE id = {i}")
                existing_data = cur.fetchone()
                if existing_data is not None:
                    # Vergleichen Sie die vorhandenen Daten mit den neuen Daten
                    if existing_data[3] == list_of_news_table[i-1][2]:
                        print("Daten sind edentisch, keine Aktualisierung erforderlich.")
                        return
                    else:
                        # Aktualisieren Sie die vorhandenen Daten
                        query = f""" UPDATE news SET title = %s, text = %s, photo = %s,qwelle = %s, download_day = %s
                                WHERE id = {i} """
                        cur.execute(query, (list_of_news_table[i-1][2], list_of_news_table[i-1][3], list_of_news_table[i-1][4],
                                        list_of_news_table[i-1][5], list_of_news_table[i-1][6]))
                        print("Daten erfolgreich aktualisiert.")
                else:
                    # Fügen Sie die neuen Daten hinzu
                    query = """ INSERT INTO news (news_name, status, title, text, photo, qwelle, download_day)
                            VALUES (%s, %s, %s, %s, %s, %s, %s) """
                    cur.execute(query, (list_of_news_table[i-1]))
                    print(f"Nachricht nummer {i} ist gespeichert.")
                    print("Daten erfolgreich hinzugefügt.")
        conn.commit()
        print("Verbindung zum PosrgreSQL-Server geschlossen.")

insert_haupt_news()
print("Данные успешно добавлены в Базу Данных.")

if os.path.exists("result.html"):
    os.remove("result.html")
    print("Datei erfolgreich gelöscht.")
else:
    print("Die Datei existiert nicht.")

html_path = "html_ordner"
for filename in os.listdir(html_path):
    if filename.endswith(".html"):
        os.remove(os.path.join(html_path, filename))
print("All HTML files deleted successfully!")

img_path = "img"
for filename in os.listdir(img_path):
    if filename.endswith(".jpg"):
        os.remove(os.path.join(img_path, filename))
print("All images files deleted successfully!")


