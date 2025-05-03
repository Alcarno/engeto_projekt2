"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Jakub Lada
email: Jakub.Lada@seznam.cz
"""

import sys
import re
import requests
from bs4 import BeautifulSoup
import csv


def check_arguments():
    if len(sys.argv) != 3:
        print("Chyba:Musíš zadat dva argumenty – odkaz a název výstupního souboru.")
        print("Použití: python main.py <odkaz> <vystup.csv>")
        sys.exit(1)
    url = sys.argv[1]
    output_file = sys.argv[2]
    # Kontrola, že odkaz vypadá jako správný odkaz na obec
    if not re.match(r"^https://www\.volby\.cz/pls/ps2017nss/ps32\?", url):
        print("Chyba: První argument musí být odkaz na stránku s výsledky obcí (musí obsahovat 'ps32?'). Zkus to znovu.")
        sys.exit(1)
    if not output_file.endswith('.csv'):
        print("Chyba: Druhý argument musí být název CSV souboru (např. vysledky.csv).")
        sys.exit(1)
    return url, output_file


def get_obec_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Chyba: Něco se pokazilo při stahování stránky: {e}")
        sys.exit(1)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="table")
    if not table:
        print("Chyba: Na stránce jsem nenašel tabulku s obcemi. Zkontroluj odkaz.")
        sys.exit(1)
    obce = []
    for row in table.find_all("tr")[2:]:  # Přeskočí hlavičku
        cells = row.find_all("td")
        if len(cells) < 2:
            continue
        kod_obce = cells[0].text.strip()
        nazev_obce = cells[1].text.strip()
        link_tag = cells[0].find("a")
        if link_tag and link_tag.get("href"):
            detail_url = "https://www.volby.cz/pls/ps2017nss/" + link_tag.get("href")
            obce.append({
                "kod": kod_obce,
                "nazev": nazev_obce,
                "url": detail_url
            })
    return obce


def get_obec_data(obec_url):
    try:
        response = requests.get(obec_url)
        response.raise_for_status()
    except Exception as e:
        print(f"Chyba: Nepodařilo se stáhnout detail obce: {e}")
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    # První tabulka nahoře – tady jsou souhrnné údaje o obci
    try:
        table = soup.find("table", class_="table")
        rows = table.find_all("tr")
        data_cells = rows[2].find_all("td")  # Tohle je první řádek s čísly
        volici = data_cells[3].text.strip().replace('\xa0', '').replace(' ', '')  # Počet voličů v seznamu
        obalky = data_cells[4].text.strip().replace('\xa0', '').replace(' ', '')  # Kolik bylo vydáno obálek
        platne = data_cells[7].text.strip().replace('\xa0', '').replace(' ', '')  # Platné hlasy
    except Exception:
        print("Chyba: Nepodařilo se získat základní údaje o obci. Možná se změnila struktura stránky.")
        return None
    # Teď jdeme na strany a jejich hlasy – jsou v tabulkách níž na stránce
    strany = []
    hlasy = []
    for div in soup.find_all("div", class_="t2_470"):
        table = div.find("table", class_="table")
        if not table:
            continue  # Kdyby tam náhodou nebyla tabulka, přeskočíme
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) >= 3:
                nazev_strany = cells[1].text.strip()  # Název strany
                pocet_hlasu = cells[2].text.strip().replace('\xa0', '').replace(' ', '')  # Hlasy pro stranu
                strany.append(nazev_strany)
                hlasy.append(pocet_hlasu)
    return volici, obalky, platne, strany, hlasy


def save_to_csv(obce, output_file):
    if not obce:
        print("Chyba: Nemám žádná data k uložení. Pravděpodobně se něco pokazilo při stahování nebo zpracování.")
        return
    # Zjistíme všechny názvy stran podle první obce
    for obec in obce:
        if obec.get("strany"):
            strany = obec["strany"]
            break
    else:
        print("Chyba: Nepodařilo se zjistit názvy stran. Zkontroluj, jestli máš správný odkaz nebo jestli se nezměnila stránka.")
        return
    header = ["kód obce", "název obce", "voliči v seznamu", "vydané obálky", "platné hlasy"] + strany
    with open(output_file, mode="w", newline="", encoding="cp1250") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(header)
        for obec in obce:
            row = [obec["kod"], obec["nazev"], obec["volici"], obec["obalky"], obec["platne"]] + obec["hlasy"]
            writer.writerow(row)
    print(f"Hotovo! Data jsou uložená v souboru {output_file}")


def main():
    url, output_file = check_arguments()
    print(f"Odkaz: {url}")
    print(f"Výstupní soubor: {output_file}")
    obce = get_obec_links(url)
    print(f"Nalezeno obcí: {len(obce)}")
    vysledky = []
    for idx, obec in enumerate(obce, 1):
        print(f"Zpracovávám {idx}/{len(obce)}: {obec['nazev']}")
        data = get_obec_data(obec["url"])
        if data:
            volici, obalky, platne, strany, hlasy = data
            vysledky.append({
                "kod": obec["kod"],
                "nazev": obec["nazev"],
                "volici": volici,
                "obalky": obalky,
                "platne": platne,
                "strany": strany,
                "hlasy": hlasy
            })
    save_to_csv(vysledky, output_file)


if __name__ == "__main__":
    main()
