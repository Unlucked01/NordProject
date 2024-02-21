import csv
import matplotlib.pyplot as plt
import pandas as pd


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
    # Sortera listan baserat på den valda kolumnen
    sorted_data = sorted(data[2:], key=lambda x: x[column_index], reverse=True)

    # Skriv ut de tio bästa resultaten
    print("De tio länder som hade bäst resultat år 2018")
    print("--------------------------------------------")
    print("Land      Resultat")
    print("--------------------------------------------")
    for row in sorted_data[:10]:
        print(f"{row[0]:<10} {row[column_index]}")

    print()

    # Skriv ut de tio sämsta resultaten
    print("De tio länder som hade sämst resultat år 2018")
    print("--------------------------------------------")
    print("Land      Resultat")
    print("--------------------------------------------")
    for row in sorted_data[-10:]:
        print(f"{row[0]:<10} {row[column_index]}")


"Task 3"


def column_mean(data, column_index):
    """
    Функция вычисляет среднее значение столбца в списке.

    Args:
    data (list): Список данных.
    column_index (int): Индекс столбца для вычисления среднего значения.

    Returns:
    float: Среднее значение столбца.
    """
    total = 0
    count = 0

    for row in data:
        try:
            value = float(row[column_index])
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
    Функция создает список armed со средним значением/годом исследования для всех стран.

    Args:
    data (list): Исходный список данных.

    Returns:
    list: Список armed со средним значением/годом исследования.
    """
    armed = []

    # Получить индексы столбцов с меткой "Среднее" для каждого года
    mean_indices = [i for i, column in enumerate(data[1]) if 'medel' in column]

    # Для каждого года вычислить среднее значение столбца и добавить его в список armed
    for index in mean_indices:
        mean_value = column_mean(data, index)
        year = data[0][index].split(' ')[-1]  # Извлечь год из метки столбца
        armed.append((year, mean_value))
    return armed


def print_table(data):
    header = ("{:<5} {:<10} {:<10} {:<10} {:<10} {:<10} {:<7}"
              .format("År", "Sweden", "Norway", "Denmark", "Finland", "Iceland", "Medelvärde"))
    separator = "-" * len(header)
    print("Kunskapsutveckling i matematik enligt PISA-undersökningen 2003 – 2018.")
    print(separator)
    print("{:>35}".format("Länder:"))


    for row in data:
        print("{:<5} {:<10} {:<10} {:<10} {:<10} {:<10} {:<7}".format(*row))


    headers_data = data[0]
    print(headers_data)
    headers = {}
    for k in headers_data:
        headers[k] = []
    for row in data[::-1]:
        for index, col in enumerate(row):
            arr_to_add = []
            if str(col).isdigit():
                arr_to_add.append(int(col))
                headers[headers_data[index]].append(int(col))
    # Переводим годы в числа для корректного отображения на графике

    print(headers)

    # Создание графика
    plt.figure(figsize=(10, 6))

    # Для каждой страны и среднего значения
    for country in headers.keys():
        if country != 'År':
            plt.plot(headers['År'], headers[country], marker='o', label=country)

    # Настройка графика
    plt.title('Score Trends Over Years by Country')
    plt.xlabel('Year')
    plt.ylabel('Score')
    plt.legend()
    plt.grid(True)
    plt.gca()  # Инвертирование оси X для корректного отображения годов
    plt.show()


def nordic_table(pisadata, yearly_average, nordic_countries):
    # Создаем заголовок таблицы
    header = ["År"]
    header.extend(nordic_countries)
    header.append("Medelvärde")
    table_data = [header]

    mean_indices = [i for i, column in enumerate(pisadata[1]) if 'medel' in column]

    # Для каждого года
    for i in range(len(yearly_average)):
        year = yearly_average[i][0]  # Извлекаем год из заголовка
        # Собираем данные для текущего года
        row_data = [year]

        for country in nordic_countries:
            index = [i for i, row in enumerate(pisadata) if row[0] == country][0]
            scandinavian_average = pisadata[index][mean_indices[i]]
            row_data.append(scandinavian_average)

        row_data.append(yearly_average[i][1])
        table_data.append(row_data)
    print_table(table_data)
    nordic_graph(table_data)



def nordic_graph(data):
    # Создание DataFrame из данных
    df = pd.DataFrame(data[1:], columns=data[0])

    # Убедимся, что все данные, кроме 'År', числовые
    df[df.columns[1:]] = df[df.columns[1:]].apply(pd.to_numeric)

    # Создание графика
    plt.figure(figsize=(10, 6))
    for country in df.columns:
        if country != 'År':
            plt.plot(df['År'], df[country], marker='o', label=country)

    # Настройка графика
    plt.title('Score Trends Over Years by Country')
    plt.xlabel('Year')
    plt.ylabel('Score')
    plt.legend()
    plt.grid(True)
    plt.show()

#     №4


def battreSamre(pisadata, improving):
    print("Table of countries with" + (" improving " if improving else " worsening ") + "results:")

    header = ["Countries"] + [year for year in [2003, 2006, 2009, 2012, 2015, 2018]]
    table_data = [header]
    for row in pisadata[2::]:
        last_six_values = row[-6:]
        country = row[0]

        scores = [int(score) for score in last_six_values if score.isdigit()]  # Convert scores to integers, ignoring non-digit values
        scores = scores[::-1]
        print(scores)

        if improving and all(scores[i] <= scores[i + 1] for i in range(len(scores) - 1)):
            table_data.append([country] + scores)
        elif not improving and all(scores[i] >= scores[i + 1] for i in range(len(scores) - 1)):
            table_data.append([country] + scores)


    for row in table_data:
        print("\t".join(map(str, row)))


def Woman_man(data):
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
                    women_better.append((country, year, score_m, score_f))

    # Skriv ut tabellen
    print("Länder och år där kvinnor presterade bättre än män:")
    print("Land\t\tÅr\tMän\tKvinnor")
    for item in women_better:
        print(f"{item[0]:<15}{item[1]:<5}{item[2]:<5}{item[3]:<5}")

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
    pisadata = read_file("f_56965d49c2646eaf.csv")
    mean = armed(pisadata)

    # nordic_table(pisadata, mean, nordic_countries)
    # nordic_graph(pisadata, mean, nordic_countries)

    choice = input("Välj ett menyalternativ (1 - 6): ")
    if choice == '1':
        pass
        # filename = input("Ange filnamn eller tryck bara Enter för data.csv: ") or 'data.csv'
        # pisadata = read_file(filename)
        # print("Fem första raderna i pisadata:")
        # for row in pisadata[:5]:
        #     print(row)
    elif choice == '2':
        sort_results_by_column(pisadata, 12)
    elif choice == '3':
        mean = armed(pisadata)
        nordic_table(pisadata, mean, nordic_countries)
        pass
    elif choice == '4':
        print("Analyzing data for continuous improvement over the years...")
        battreSamre(pisadata, True)
        print("\nAnalyzing data for continuous decline over the years...")
        battreSamre(pisadata, False)
    elif choice == '5':
        Woman_man(pisadata)
    elif choice == '6':
        print("Programmet är avslutat.")
        break
    else:
        print("Ogiltigt val. Välj igen.")
