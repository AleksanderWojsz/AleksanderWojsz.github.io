from bs4 import BeautifulSoup
import requests
from googlesearch import search

html_text = requests.get("https://en.wikipedia.org/wiki/List_of_most_visited_palaces_and_monuments").text
soup = BeautifulSoup(html_text, "lxml")

full_table = soup.find("table", class_="wikitable sortable")
rows = full_table.find_all("tr")

with open("index.md", "w", encoding="utf-8") as file:  # Otwiera plik w trybie zapisu
    file.write(rows[0].text.strip() + "\n\n")
    file.write("| Position |")
    file.write(" | ".join(rows[1].text.strip().replace("\n", ", ").split(", ")[
                          :3]) + " | more |\n")  # Łączy trzy pierwsze elementy odzielając je przecinkami
    file.write("| --- | --- | --- | --- | --- |\n")

    position = 1  # Inicjalizuje zmienną licznikową dla pozycji

    for row in rows[2:5]:  # pomija nagłówek
        cells = row.find_all("td")

        # Dodaje pozycję jako pierwszą komórkę w każdym wierszu
        file.write(f"| {position}")


        for i in range(3):
            file.write(" | ")
            if i == 1:  # czy to kolumna z linkiem do miasta
                city_links = cells[i].find_all("a")  # Wyszukuje wszystkie linki w komórce

                country_flag = city_links[0].find("img")  # Znajduje obraz flagi kraju
                country_flag_url = "https:" + country_flag.get("src")  # Pobiera adres URL flagi
                file.write(f"![Flaga]({country_flag_url}) ")  # Zapisuje obraz flagi

                country_name = city_links[0].get("title")  # Pobiera nazwę kraju
                country_url = "https://en.wikipedia.org" + city_links[0].get("href")  # Pobiera adres URL kraju
                file.write(f"[{country_name}]({country_url}), ")  # Zapisuje nazwę kraju jako link

                city_name = city_links[1].text.strip()  # Pobiera nazwę miasta
                city_url = "https://en.wikipedia.org" + city_links[1].get("href")  # Pobiera adres URL miasta
                file.write(f"[{city_name}]({city_url})")  # Zapisuje nazwę miasta jako link
            else:
                file.write(cells[i].text.strip())

        # Dodaje link "more" prowadzący do podstrony z zawartością "hello"
        subpage_filename = f"subpage{position}.md"
        file.write(f" | [more]({subpage_filename}) |")

        monument_name = cells[0].text.strip()

        # Tworzy i zapisuje do pliku subpage{numer}.md zawartość "hello"
        with open(subpage_filename, "w", encoding="utf-8") as subpage_file:
            subpage_file.write("Additonal info: \n\n")
            for url in search(monument_name + " -site:https://en.wikipedia.org", stop=3):
                subpage_file.write(f"- [{url}]({url})\n")

            subpage_file.write("\n")
            subpage_file.write("Pictures: \n\n")


            headers = { #  https://stackoverflow.com/questions/72805266/python-web-scraping-code-error-http-error-406-not-acceptable
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            }
            html_text2 = requests.get("https://www.shutterstock.com/pl/search/" + monument_name, headers=headers).text
            soup = BeautifulSoup(html_text2, "lxml")
            images = soup.find("div", class_="mui-1nl4cpc-gridContainer-root")
            for image in images.find_all("div", role="img", limit=5):
                image_url = image.find("img").get("src")
                subpage_file.write(f"![Obrazek]({image_url})\n\n")





        file.write("\n")
        position += 1  # Zwiększa licznik pozycji
