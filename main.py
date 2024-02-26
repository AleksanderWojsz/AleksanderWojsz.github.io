from bs4 import BeautifulSoup
import requests
from googlesearch import search
import time

def prepare_descriptions():
    title = wiki_soup.find("h1", id="firstHeading").text
    description = wiki_soup.find("div", class_="mw-content-ltr mw-parser-output").find_all("p")[1].text
    table_headers = " | ".join(rows[1].text.strip().replace("\n", "| ").split("| ")[:3])  # lączy trzy pierwsze elementy oddzielając je |

    file.write("## " + title + "\n\n" + description + "\n\n **" + rows[0].text.strip() + "** \n\n")
    file.write("| Position |" + table_headers + " | pictures & links |\n")
    file.write("| --- | --- | --- | --- | --- |\n")


def create_subpage(country_name, city_name):
    subpage_filename = f"subpage{position}.md"
    file.write(f" | [browse]({subpage_filename}) |")

    monument_name = cells[0].text.strip()

    with open(subpage_filename, "w", encoding="utf-8") as subpage_file:
        subpage_file.write("### Additional info: \n\n")
        for url in search(monument_name + " -site:https://en.wikipedia.org", stop=3):
            subpage_file.write(f"- [{url}]({url})\n")
        subpage_file.write("\n\n --- \n\n **Pictures**: \n\n")

        headers = {
            # https://stackoverflow.com/questions/72805266/python-web-scraping-code-error-http-error-406-not-acceptable
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        }
        shutter_html_text = requests.get("https://www.shutterstock.com/pl/search/" + monument_name + " " + country_name + " " + city_name, headers=headers).text
        shutter_soup = BeautifulSoup(shutter_html_text, "lxml")
        images = shutter_soup.find("div", class_="mui-1nl4cpc-gridContainer-root")
        for image in images.find_all("div", role="img", limit=20):
            image_url = image.find("img").get("src")
            subpage_file.write(f"![Obrazek]({image_url})\n\n")


def create_table_row(position):
    file.write(f"| {position}")
    for i in range(3):
        file.write(" | ")
        if i == 1:  # czy kolumna z linkiem do miasta
            city_links = cells[i].find_all("a")

            country_flag_url = "https:" + city_links[0].find("img").get("src")
            file.write(f"![Flaga]({country_flag_url}) ")

            country_name = city_links[0].get("title")
            country_url = "https://en.wikipedia.org" + city_links[0].get("href")
            file.write(f"[{country_name}]({country_url}), ")

            city_name = city_links[1].text.strip()
            city_url = "https://en.wikipedia.org" + city_links[1].get("href")
            file.write(f"[{city_name}]({city_url})")
        else:
            file.write(cells[i].text.strip())
    return country_name, city_name

wiki_html_text = requests.get("https://en.wikipedia.org/wiki/List_of_most_visited_palaces_and_monuments").text
wiki_soup = BeautifulSoup(wiki_html_text, "lxml")

full_table = wiki_soup.find("table", class_="wikitable sortable")
rows = full_table.find_all("tr")

with open("index.md", "w", encoding="utf-8") as file:
    prepare_descriptions()
    position = 1

    for row in rows[2:]:  # pomija nagłówek
        cells = row.find_all("td")

        country_name, city_name = create_table_row(position)
        create_subpage(country_name, city_name)

        position += 1
        file.write("\n")