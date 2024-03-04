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
        with open(filename, 'r', encoding='UTF-8') as file:
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
    data (list): Listan som ska sorteras.
    column_index (int): Index för den kolumn som bestämmer sorteringsordningen.

    Returns:
    None
    """
    country_value_pairs = [(data[i + 2][0], int(data[i + 2][column_index])) for i in range(len(data) - 2)]
    sorted_pairs = sorted(country_value_pairs, key=lambda x: x[1], reverse=True)

    # Skriv ut de tio bästa resultaten
    header = "De tio länder som hade bäst resultat år 2018"
    delim = "-"*len(header)
    print(header)
    print(delim)
    print("Land            Resultat")
    print(delim)
    for country, value in sorted_pairs[:10]:
        print(f"{country:<15} {value}")
    print()

    # Skriv ut de tio sämsta resultaten
    header = "De tio länder som hade sämst resultat år 2018"
    delim = "-"*len(header)
    print(header)
    print(delim)
    print("Land            Resultat")
    print(delim)
    for country, value in sorted_pairs[-10:]:
        print(f"{country:<15} {value}")


# Uppgift 3:
# I denna deluppgift skall ni jämföra hur matematikkunskaperna i de nordiska länderna (Sverige,
# Norge, Danmark, Finland och Island) har utvecklats under åren 2003 – 2018 i jämförelse med
# medelvärdet per undersökningstillfälle för alla länder som finns i den tidigare inlästa listan pisadata.
def kolumnmedel(data, column_index):
    """
    Funktionen beräknar medelvärdet för en kolumn i en lista.

     Args:
     data (lista): Lista över data.
     column_index (int): Index för kolumnen för att beräkna medelvärdet.

     Returnerar:
     float: Medelvärdet för kolumnen.
    """
    total = 0
    count = 0

    for row in data[1:]:
        try:
            value = int(row[column_index])
            total += value
            count += 1
        except ValueError:
            continue

    if count == 0:
        return 0
    else:
        return round(total / count)


def armed(data):
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


def get_data(pisadata, mean, data):
    mean_indices = [i for i in range(13, 19)]
    for i in range(len(mean)):
        year = mean[i][0]  # Extraherar årtalet från titeln
        # Insamling av data för innevarande år
        row_data = [year]

        for country in nordic_countries:
            index = [i for i, row in enumerate(pisadata) if row[0] == country][0]
            scandinavian_average = pisadata[index][mean_indices[i]]
            row_data.append(int(scandinavian_average))

        row_data.append(mean[i][1])
        data.append(row_data)
    return data


def nordTabell(pisadata, mean, nordic_countries):
    """
    Funktionen skapar en tabell och graf som visar medelvärden för de skandinaviska länderna.

    Args:
    pisadata (lista): PISA-data.
    yearly_average (lista): Årsmedelvärden.
    nordiska_länder (lista): Lista över skandinaviska länder.

    Returnerar:
    Ingen
    """
    # Skapa en tabellrubrik
    header = ["År"]
    header.extend(nordic_countries)
    header.append("Medelvärde")
    table_data = [header]

    table_data = get_data(pisadata, mean, table_data)

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


def nordGraf(pisadata, mean, nordic_countries):
    """
    Funktionen skapar ett diagram över poängutvecklingen per år för olika länder.

    Args:
    data (lista): De data som ska plottas i listlistformat.

    Returnerar:
    Ingen
    """
    # nordic_countries.append("Medelvärde")
    header = ["År"]
    header.extend(nordic_countries)
    header.append("Medelvärde")
    graph_data = [header]
    graph_data = get_data(pisadata, mean, graph_data)

    header = graph_data[0]
    rows = graph_data[1:]

    data_dict = {header[i]: [] for i in range(len(header))}
    for row in rows:
        for i in range(len(header)):
            data_dict[header[i]].append(int(row[i]))

    plt.figure(figsize=(10, 6))
    for country in header[1:]:
        plt.plot(data_dict["År"], data_dict[country], marker='o', label=country)

    plt.title('PISA: 2003-2018')
    plt.xlabel('År')
    plt.ylabel('Poäng')
    plt.legend()
    plt.grid(True)
    plt.show()


# Uppgift 4:
# Denna deluppgift går ut på att presentera trender i data och du skall skapa två tabeller.
# Den första tabellen ska presentera de länder som kontinuerligt har förbättrat sina resultat mellan år
# 2003 till 2018. Använd kolumnerna märkta ”medel” i listan pisadata. Tabellen ska ha följande
# utseende (observera att värdena i tabellen är exempelvärden och inte korrekta värden):
def battreSamre(pisadata, improving):
    """
    Funktionen skapar en graf över betygstrender per år för olika länder.

    Args:
    data (lista): Data som ska plottas i listformat.

    Returnerar:
    Ingen
    """
    header = "Länder som hela tiden har förbättrat sina resultat mellan 2003 – 2018"
    delim = "-"*len(header)
    print(header)
    print(delim)
    print("{:>42}".format("År och resultat:"))
    print("{:<20} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5}".format("Land", "2018", "2015", "2012", "2009", "2006", "2003"))
    print(delim)

    header = ["Land"] + [year for year in [2003, 2006, 2009, 2012, 2015, 2018]]
    table_data = [header]
    for row in pisadata[2::]:
        last_six_values = row[-6:]
        country = row[0]

        scores = [int(score) for score in last_six_values if score.isdigit()]
        scores = scores[::-1]

        if improving and all(scores[i] <= scores[i + 1] for i in range(len(scores) - 1)):
            table_data.append([country] + scores)
        elif not improving and all(scores[i] >= scores[i + 1] for i in range(len(scores) - 1)):
            table_data.append([country] + scores)

    for row in table_data[1:]:
        country = row[0]
        scores = row[1:]
        print("{:<20} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5}".format(country, *scores))


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
        for i in range(1, len(row) - 1, 2):  # Steg om två för att jämföra M och F för varje år
            year = data[0][i].split(' ')[0]  # Hämta året från första raden
            if row[i].isdigit() and row[i+1].isdigit():  # Kontrollera att båda värdena är siffror
                score_m = int(row[i])
                score_f = int(row[i+1])
                if score_f > score_m:
                    women_better.append((year, country, score_f, score_m))

    yearly_data = {}
    for year, country, score_f, score_m in women_better:
        if year not in yearly_data:
            yearly_data[year] = []
        yearly_data[year].append((country, score_f, score_m))

    # Skriv ut tabellen
    separator = "-" * 50
    print("    År och länder när kvinnorna presterar bättre än männen")
    print("{:>40}".format("under åren 2003–2018."))
    print("{:<12} {:<15} {:<8} {:<5}".format("År", "Land", "Kvinnor", "Män"))
    print(separator)

    for k in yearly_data.keys():
        for i, (country, score_f, score_m) in enumerate(yearly_data[k]):
            if i == 0:
                print(f"{k:<5}\t{country:<20} {score_f:<7} {score_m:<7}")
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

# Main program loop
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
            sort_results_by_column(pisadata, 13)
    elif choice == '3':
        if 'pisadata' not in locals():
            print("Du måste välja alternativ 1 först.")
        else:
            mean = armed(pisadata)
            nordTabell(pisadata, mean, nordic_countries)
            nordGraf(pisadata, mean, nordic_countries)
    elif choice == '4':
        if 'pisadata' not in locals():
            print("Du måste välja alternativ 1 först.")
        else:
            battreSamre(pisadata, True)
            print()
            battreSamre(pisadata, False)
            print()
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
