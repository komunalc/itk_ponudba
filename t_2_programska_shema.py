from bs4 import BeautifulSoup
import requests
import openpyxl

# Ustvari excel workbook
wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'programi in sheme'

ws.append(['Program', 'S', 'M', 'L', 'XL'])

# URL strani
naslov = 'https://www.t-2.net/primerjalnik-programskih-shem'

# Pošlji GET zahtevek na URL
req = requests.get(naslov)

# Ustvari BeautifulSoup objekt
soup = BeautifulSoup(req.text, 'html.parser')

# Poišči <div> z id-jem 'compare__body'
compare_body = soup.find('div', id='compare__body')

# Preveri, če smo našli div
if compare_body:
    # Poišči vse vrstice v tabeli (vsak <tr> element)
    rows = compare_body.find_all('tr')

    # Za vsak program izpiši ime in pakete, v katerih je vključen ali ni vključen
    for row in rows[1:]:  # Preskoči prvo vrstico, ker je to vrstica z glavo (headers)
        cols = row.find_all('td')
        if len(cols) > 0:
            program_name = cols[0].get_text(strip=True)
            included_s = 1 if "included-s" in cols[1].get('class', []) else 0
            included_m = 1 if "included-m" in cols[2].get('class', []) else 0
            included_l = 1 if "included-l" in cols[3].get('class', []) else 0
            included_xl = 1 if "included-xl" in cols[4].get('class', []) else 0

            # Izpis rezultatov - lep print
            """ print(f'Program: {program_name}')
            print(f'  Paket S: {included_s}')
            print(f'  Paket M: {included_m}')
            print(f'  Paket L: {included_l}')
            print(f'  Paket XL: {included_xl}')
            print('-' * 40) """
            
            # Izpis rezultatov v tab delimited obliki
            #print(f'{program_name}\t{included_s}\t{included_m}\t{included_l}\t{included_xl}')

            # Shranjevanje rezultatov v excelovo datoteko
            xlsx_vsebina = [program_name, included_s, included_m, included_l, included_xl]
            ws.append(xlsx_vsebina)

    # Shranjevanje datoteke
    wb.save('t_2.xlsx')

    print("Podatki so shranjeni v excelovo datoteko!")

else:
    print("Element z id-jem 'compare__body' ni bil najden.")
