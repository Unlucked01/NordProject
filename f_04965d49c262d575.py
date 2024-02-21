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


def nordic_graph(pisadata, yearly_average, nordic_countries):
    # Создаем список годов в обратном порядке
    years = [year for year, _ in reversed(yearly_average)]
    mean_indices = [i for i in reversed(range(len(pisadata[1]))) if 'Medelvärde' in pisadata[0][i]]

    # Создаем заголовок для графика
    plt.title("PISA-undersökning 2003 – 2018")
    plt.ylim(350, 550)
    plt.xlim(2003, 2018)

    # Добавляем подписи осей
    plt.xlabel("År")
    plt.ylabel("Kunskapsutveckling")

    # Словарь для хранения данных для каждой страны
    country_data = {country: [] for country in nordic_countries}

    # Извлекаем данные для каждой страны
    for country in nordic_countries:
        index = [i for i, row in enumerate(pisadata) if row[0] == country][0]
        country_mean_indices = [i for i in mean_indices if i < len(pisadata[index])]
        country_data[country] = [float(row[mean_index]) for row, mean_index in
                                 zip(pisadata[index + 1:], country_mean_indices)]

    print(country_data)
    exit(0)
    # Добавляем кривые для каждой страны, если есть данные
    for country, data in country_data.items():
        if data:
            plt.plot(years, data, label=country)

    # Добавляем кривую для годового среднего значения
    average_values = [avg for _, avg in reversed(yearly_average)]
    plt.plot(years, average_values, label="Medelvärde", linestyle='--', color='black')

    # Добавляем легенду
    plt.legend()

    # Отображаем график
    plt.show()


#     №4


def battreSamre(pisadata, improving):
    if improving:
        print("Таблица стран с улучшающимися результатами:")
    else:
        print("Таблица стран с ухудшающимися результатами:")

    header = ["Länder"]
    years = ["2018", "2015", "2012", "2009", "2006", "2003"]
    header.extend(years)

    table_data = [header]

    for row in pisadata[1:]:
        country = row[0]
        scores = row[1:-1]  # Исключаем последний элемент, так как это среднее значение
        print(row[1:-2])
        try:
            improving_or_decreasing = all(
                int(scores[i]) < int(scores[i + 1]) for i in range(len(scores) - 1)) if improving else all(
                int(scores[i]) > int(scores[i + 1]) for i in range(len(scores) - 1))
        except:
            pass
        if improving_or_decreasing:
            table_data.append([country] + scores)

    for row in table_data:
        print("\t".join(row))

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
    battreSamre(pisadata, True)

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
        # nordic_graph(pisadata, mean, nordic_countries)
        pass
    elif choice == '4':
        pass
    elif choice == '6':
        print("Programmet är avslutat.")
        break
    else:
        print("Ogiltigt val. Välj igen.")
