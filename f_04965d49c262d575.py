import csv
import matplotlib.pyplot as plt


# Uppgift 1: Funktionen för att läsa in csv-filen och skapa en lista
def read_file(filename):
    """
    Funktionen läser innehållet från en CSV-fil och returnerar det som en lista.

    Args:
    filename (str): Namnet på CSV-filen som ska läsas in.

    Returns:
    list: En lista med innehållet från CSV-filen.
    """
    try:
        with open(filename, 'r', encoding='UTF-8') as file: #
            reader = csv.reader(file, delimiter=';')
            data = [row for row in reader]
        return data
    except FileNotFoundError:
        print("Filen kunde inte hittas.")
        return []


# Uppgift 2: Funktionen för att sortera och visa de bästa och sämsta resultaten år 2018
def sort_results_by_column(data, column_index):
    """
    Funktionen sorterar innehållet i en lista utifrån en vald kolumn och visar de tio bästa och sämsta resultaten år 2018.

    Args:
    data: En lista med innehållet från CSV-filen.
    column_index (int): index för den kolumn där vi kommer att söka efter medelvärdet
    Returns:
    pisadata_sorterad: lista över par (land, värde) sorterade i fallande ordning
    """
    country_value_pairs = [(data[i + 2][0], int(data[i + 2][column_index])) for i in range(len(data) - 2)]
    pisadata_sorterad = sorted(country_value_pairs, key=lambda x: x[1], reverse=True)

    # Skriv ut de tio bästa resultaten
    header = "De tio länder som hade bäst resultat år 2018"
    delim = "-"*len(header)
    print(header)
    print(delim)
    print("Land            Resultat")
    print(delim)
    # topp 10 länder
    for country, value in pisadata_sorterad[:10]:
        print(f"{country:<15} {value}")
    print()

    # Skriv ut de tio sämsta resultaten
    header = "De tio länder som hade sämst resultat år 2018"
    delim = "-"*len(header)
    print(header)
    print(delim)
    print("Land            Resultat")
    print(delim)
    # de 10 värsta länderna från lägsta poäng till högsta poäng
    # __reverced__ används för att få en tillfällig inverterad lista
    for country, value in pisadata_sorterad[-10:].__reversed__():
        print(f"{country:<15} {value}")
    return pisadata_sorterad


def kolumnmedel(data, column_index):
    """
    Funktionen beräknar medelvärdet för en kolumn i en lista.

     Args:
     data: Lista över data.
     column_index (int): Index för kolumnen för att beräkna medelvärdet.

     Returnerar:
     float: Medelvärdet för kolumnen.
    """
    total = 0
    count = 0

    for row in data[2:]:
        # försök att konvertera värdet till int-typ, om detta inte är möjligt, hoppa över det
        try:
            # sammanfatta alla kolumnvärden
            value = int(row[column_index])
            total += value
            count += 1
        except ValueError:
            continue

    if count == 0:
        return 0
    else:
        # dividera summan med antalet element
        return round(total / count)


def arsmedel(data):
    """
    Funktionen skapar en lista över beväpnade med medelvärde/studieår för alla länder.

    Args:
    data (lista): Initial lista med data.

    Returnerar:
    lista: Beväpnad lista med medelvärde/studieår.
    """
    armed = []

    # Beräkna medelvärdet av kolumnen för varje år och lägg till det i den beväpnade listan
    for index in range(13, 19):
        mean_value = kolumnmedel(data, index)
        year = data[0][index]
        armed.append((year, mean_value))
    return armed


def get_data(pisadata, medelvAr, data):
    """
    Funktionen samlar data från listorna 'pisadata' och 'medelvAr' och skapar en ny lista med information
    om medelvärdena för varje år och land.

    Args:
    pisadata: PISA-data.
    medelvAr (lista): En lista som innehåller data relaterad till år och deras motsvarande medelvärden.
    data (lista): En lista till vilken den samlade datan kommer att läggas till.

    Returnerar:
    list: En lista som innehåller den samlade datan strukturerad efter år, land och medelvärden.
    """

    mean_indices = [i for i in range(13, 19)]
    for i in range(len(medelvAr)):
        year = medelvAr[i][0]  # Extraherar årtalet från titeln
        # Insamling av data för innevarande år
        row_data = [year]

        for country in nordic_countries:
            # Sök efter index för skandinaviska länder från en given tabelluppsättning
            index = [i for i, row in enumerate(pisadata) if row[0] == country][0]
            scandinavian_average = pisadata[index][mean_indices[i]]
            row_data.append(int(scandinavian_average))

        row_data.append(medelvAr[i][1])
        data.append(row_data)
    return data


# Uppgift 3:
# I denna deluppgift skall ni jämföra hur matematikkunskaperna i de nordiska länderna (Sverige,
# Norge, Danmark, Finland och Island) har utvecklats under åren 2003 – 2018 i jämförelse med
# medelvärdet per undersökningstillfälle för alla länder som finns i den tidigare inlästa listan pisadata.
def nordTabell(pisadata, medelvAr):
    """
    Funktionen skapar en tabell och graf som visar medelvärden för de skandinaviska länderna.

    Args:
    pisadata (lista): PISA-data.
    yearly_average (lista): Årsmedelvärden.
    nordic_countries (lista): Lista över skandinaviska länder.

    Returnerar:
    Ingen
    """
    # Skapa en tabellrubrik
    header = ["År"]
    header.extend(nordic_countries)
    header.append("Medelvärde")
    table_data = [header]

    # hämta de data som krävs i en funktion för återanvändning
    table_data = get_data(pisadata, medelvAr, table_data)

    # vacker bordsutgång
    header = ("{:<5} {:<10} {:<10} {:<10} {:<10} {:<10} {:<7}"
              .format("År", "Sweden", "Norway", "Denmark", "Finland", "Iceland", "Medelvärde"))
    separator = "-" * len(header)
    print("Kunskapsutveckling i matematik enligt PISA-undersökningen 2003 – 2018.")
    print(separator)
    print("{:>35}".format("Länder:"))
    print(separator)

    for row in table_data:
        print("{:<5} {:<10} {:<10} {:<10} {:<10} {:<10} {:<7}".format(*row))

    print(separator)


# Функция для отображения графа
def nordGraf(pisadata, medelvAr):
    """
    Funktionen skapar ett diagram över poängutvecklingen per år för olika länder.

    Args:
    data (lista): De data som ska plottas i listlistformat.

    Returnerar:
    Ingen
    """
    header = ["År"]
    header.extend(nordic_countries)
    header.append("Medelvärde")
    graph_data = [header]
    # erhålla data för visning på en graf
    graph_data = get_data(pisadata, medelvAr, graph_data)

    # uppdelning i rubriker och datalinjer
    header = graph_data[0]
    rows = graph_data[1:]

    # initialisera ordboken och fylla den med data
    # nyckel - land, data - värden per år
    data_dict = {header[i]: [] for i in range(len(header))}
    for row in rows:
        for i in range(len(header)):
            data_dict[header[i]].append(int(row[i]))

    plt.figure(figsize=(10, 6))
    for country in header[1:]:
        # skapa en graf på X-axeln - år, på Y-axeln - värdet av indikatorer för varje land
        plt.plot(data_dict["År"], data_dict[country], marker='o', label=country)

    plt.title('PISA: 2003-2018')
    plt.xlabel('År')
    plt.ylabel('Poäng')
    plt.legend()
    plt.grid(True)
    plt.show()


# Uppgift 4:
# Denna deluppgift går ut på att presentera trender i data och du skall skapa två tabeller.
# Den första tabellen ska presentera de länder som kontinuerligt har förbättrat sina resultat mellan år 2003 till 2018.
def battreSamre(pisadata, improving):
    """
    Funktionen skapar en graf över betygstrender per år för olika länder.

    Args:
    data (lista): Data som ska plottas i listformat.

    Returnerar:
    Ingen
    """
    print()
    if improving:
        header = "Länder som hela tiden har förbättrat sina resultat mellan 2003 – 2018"
    else:
        header = "Länder som konsekvent försämrade sina resultat mellan 2003 - 2018"

    delim = "-"*len(header)
    print(header)
    print(delim)
    print("{:>42}".format("År och resultat:"))
    print("{:<20} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5}".format("Land", "2018", "2015", "2012", "2009", "2006", "2003"))
    print(delim)

    tabel_data = []

    # vi beaktar endast uppgifterna från den tredje raden
    for row in pisadata[2:]:
        country = row[0]
        scores = [int(score) for score in row[-6:]]  # får alla medelvärden, eftersom de är de sista 6 i raden
        # om flaggan förbättra är sann, skapa tabellen för ökande länder, annars för minskande länder
        if improving and all(scores[i] >= scores[i + 1] for i in range(len(scores) - 1)):
            tabel_data.append([country] + scores)
        elif not improving and all(scores[i] <= scores[i + 1] for i in range(len(scores) - 1)):
            tabel_data.append([country] + scores)

    for row in tabel_data:
        print("{:<20} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5}".format(row[0], *row[1:]))


# Uppgift 5:
# Hur har kvinnorna klarat sig i förhållande till männen sett för alla länder, inte bara de nordiska?
def kvinna_man(data):
    """
    Funktionen analyserar data som jämför resultaten för män och kvinnor över olika år och länder,
     och visar en tabell med data där kvinnor presterade bättre än män.

    Args:
    data (lista): Data som ska analyseras i listformat.

    Returnerar:
    Ingen
    """
    # Skapa en lista för att lagra resultat där kvinnor presterade bättre än män
    women_better = []

    # Gå igenom varje land (förutom rubrikerna)
    for row in data[2:]:
        country = row[0]
        for i in range(1, len(row) - 6, 2):  # Steg av två för att jämföra M och F för varje år, ignorera kolumner med medelvärden
            year = int(data[0][i])
            score_m = int(row[i])
            score_f = int(row[i+1])
            if score_f > score_m:  # om kvinnligt konto > manligt konto lägg till i resultatlistan
                women_better.append((year, country, score_m, score_f))

    # organisera uppgifterna efter år med hjälp av ordlistan yearly_data, där: nyckel - år, värde - land, antal män och kvinnor
    yearly_data = {2018: [], 2015: [], 2012: [], 2009: [], 2006: [], 2003: []}
    for year, country, score_f, score_m in women_better:
        yearly_data[year].append((country, score_f, score_m))

    # Skriv ut tabellen
    separator = "-" * 50
    print("    År och länder när kvinnorna presterar bättre än männen")
    print("{:>40}".format("under åren 2003–2018."))
    print("{:<12} {:<15} {:<8} {:<5}".format("År", "Land", "Män", "Kvinnor"))
    print(separator)

    for k in yearly_data.keys():
        # Iterera med årtalsnycklar i ordlistan yearly_data
        for i, (country, score_f, score_m) in enumerate(yearly_data[k]):
            if i == 0:  # Skriv ut årtalet på första raden, annars skrivs raden utan årtal ut
                print(f"\n{k:<5}\t{country:<20} {score_f:<7} {score_m:<7}")
            else:
                print(f"\t{country:<20} {score_f:<7} {score_m:<7}")


# Huvudprogram med Meny
menu = """
Program för att läsa in och analysera data från PISA-undersökningen
1. Läs in csv-filen.
2. Bästa resp. sämsta resultat år 2018.
3. Matematikkunskaper i norden år 2003 – 2018.
4. Kontinuerligt förbättrat resp. försämrat år 2003 – 2018.
5. Kvinnor presterar bättre än män under åren 2003–2018.
6. Avsluta programmet.
"""

print(menu)
nordic_countries = ['Sweden', 'Norway', 'Denmark', 'Finland', 'Iceland']

while True:
    # pisadata = read_file("pisadata.csv")

    choice = input("Välj ett menyalternativ (1 - 6): ")
    if choice == '1':
        filename = input("Ange filnamn eller tryck bara Enter för data.csv: ") or 'pisadata.csv'
        pisadata = read_file(filename)
        print("Fem första raderna i pisadata:")
        for row in pisadata[:5]:
            print(row)
    elif choice == '2':
        if 'pisadata' not in locals():
            print("Du måste välja alternativ 1 först.")
        else:
            pisadata_sorterad = sort_results_by_column(pisadata, 13)
    elif choice == '3':
        if 'pisadata' not in locals():
            print("Du måste välja alternativ 1 först.")
        else:
            medelvAr = arsmedel(pisadata)
            nordTabell(pisadata, medelvAr)
            nordGraf(pisadata, medelvAr)
    elif choice == '4':
        if 'pisadata' not in locals():
            print("Du måste välja alternativ 1 först.")
        else:
            battreSamre(pisadata, True)
            battreSamre(pisadata, False)
    elif choice == '5':
        if 'pisadata' not in locals():
            print("Du måste välja alternativ 1 först.")
        else:
            kvinna_man(pisadata)
            print()
    elif choice == '6':
        print("Programmet är avslutat.")
        break
    else:
        print("Ogiltigt val. Välj igen.")
