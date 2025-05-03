# Elections Scraper – Výsledky voleb 2017

Tento projekt ti stáhne výsledky voleb do Poslanecké sněmovny 2017 pro vybraný okres nebo obvod přímo z webu [volby.cz](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) a uloží je do CSV. Stačí zadat odkaz a název výstupního souboru – zbytek už zařídí skript.

## Autor
Jakub Lada  
email: Jakub.Lada@seznam.cz

---

## Co budeš potřebovat
- Python 3.8 nebo novější
- Knihovny z `requirements.txt` (instalace viz níže)

---

## Jak na to (rychlý start)

1. **Vytvoř si virtuální prostředí (doporučuji, ale není nutné):**
   
   Windows PowerShell:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```

2. **Nainstaluj potřebné knihovny:**
   ```powershell
   pip install -r requirements.txt
   ```

---

## Jak skript spustit

Skript potřebuje dva argumenty:
1. Odkaz na stránku s výsledky obcí (např. okres Prostějov)
2. Název výstupního CSV souboru

**Příklad příkazu:**
```powershell
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" vysledky_prostejov.csv
```

Po spuštění skript projde všechny obce v daném okrese, stáhne jejich výsledky a uloží je do CSV. Výstup najdeš ve stejné složce, odkud jsi skript spustil.

---

## Co přesně skript dělá
- Stáhne stránku s výsledky pro zvolený okres/obvod.
- Najde všechny obce a pro každou obec stáhne detailní stránku.
- Z detailu obce vytáhne:
  - kolik bylo voličů v seznamu
  - kolik bylo vydáno obálek
  - kolik bylo platných hlasů
  - kolik hlasů dostala každá strana
- Všechno to uloží do CSV, kde každý řádek je jedna obec a každý sloupec jedna strana.

---

## Jak vypadá výstupní CSV

![Ukázka CSV](ukazka_csv.jpg)

**Co znamenají sloupce:**
- `kód obce` – číselný kód obce
- `název obce` – jméno obce
- `voliči v seznamu` – kolik lidí mohlo volit
- `vydané obálky` – kolik obálek bylo vydáno
- `platné hlasy` – kolik hlasů bylo platných
- Další sloupce – každá strana, kolik dostala hlasů v dané obci

---

## Tipy a poznámky
- Pokud zadáš špatné argumenty, skript ti napoví, co opravit.
- Výsledky jsou vždy pro všechny obce v daném okrese/obvodu.
- Pro jiný okres stačí změnit odkaz v prvním argumentu (najdeš na volby.cz).
- CSV se uloží tam, odkud skript spouštíš (nebo zadej cestu, kam chceš).
- Pokud by se stránka volby.cz změnila, může být potřeba upravit kód.

---

## Odkud jsou data?
Všechno je z veřejného webu [volby.cz](https://www.volby.cz/).