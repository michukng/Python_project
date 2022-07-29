# Rejest pacjentów

import sys, datetime, csv

# Nagłówki do plików z wizytą pacjenta - (visit_date.csv) oraz z kartoteką pacjenta - (description_patient.csv)
fieldnames_visit = ["first_name", "last_name", "pesel", "phone_number", "visit_date", "days_to_visit", "confirmed"]
fieldnames_description = ["first_name", "last_name", "pesel", "phone_number", "birth_date", "patient_card"]

# Listy stworzone do przechowywania wizyt pacjentów - (patient_visit) oraz do opisu pacjentów - (patient_description)
patient_visit = []
patient_description = []

# Nazwy plików
file_name_visit = "visit_date.csv"
file_name_description = "description_patient.csv"


# Funkcja do stworzenia pliku z wizytą pacjenta
def add_to_file_visit():
    with open(file_name_visit, "w", newline="") as file:
        file_writer = csv.DictWriter(file, fieldnames=fieldnames_visit, delimiter="\t")
        file_writer.writeheader()

        file_writer_row = csv.writer(file, delimiter="\t")
        for patients_visit in patient_visit:
            file_writer_row.writerow(patients_visit)

# Funkcja do stworzenia pliku z kartoteką pacjenta
def add_to_file_description():
    with open(file_name_description, "w", newline="") as file_des:
        file_writer_description = csv.DictWriter(file_des, fieldnames=fieldnames_description, delimiter="\t")
        file_writer_description.writeheader()

        file_writer_row_description = csv.writer(file_des, delimiter="\t")
        for patients_des in patient_description:
            file_writer_row_description.writerow(patients_des)

# Utworzenie wyjątku, w wypadku gdyby plików nie było na komputerze
try:
    with open(file_name_visit, "r") as file:
        file_reader = csv.reader(file, delimiter="\t")
        next(file_reader)
        for patients_visit in file_reader:
            patient_visit.append(patients_visit)

    with open(file_name_description, "r") as file_des:
        file_reader_des = csv.reader(file_des, delimiter="\t")
        next(file_reader_des)
        for patients_des in file_reader_des:
            patient_description.append(patients_des)
except FileNotFoundError:
    add_to_file_visit()
    add_to_file_description()

# Funkcja dodwania pacjenta
def add_patient():
    adding_patient = []
    checking_patient = []

    for patient in patient_description:
        checking_patient.append(patient[2])

    first_name = input("\nPodaj imię pacjenta: ")
    first_name = first_name.capitalize()
    last_name = input("Podaj nazwisko pacjenta: ")
    last_name = last_name.capitalize()

    while True:
        pesel = input("Podaj pesel pacjenta: ")
        if pesel.isdigit() == False or len(pesel) != 11:
            print("Błędny numer pesel.")
        else:
            break

    while True:
        try:
            phone_number = int(input("Podaj numer telefonu do pacjenta: "))
            break
        except ValueError:
            print("Błędny numer!")

    while True:
        try:
            visit_date = input("Podaj datę wizyty pacjenta DD/MM/YY oraz godzinę HH:MM: ")
            visit_date = datetime.datetime.strptime(visit_date, "%d/%m/%Y %H:%M")
            visiting_date = visit_date.strftime("%d/%m/%Y %H:%M")
            break
        except ValueError:
            print("Proszę podać poprawną datę/godzinę wizyty pacjenta.")

    today = datetime.datetime.today().replace(second=0, microsecond=0)
    days_to_visit = visit_date - today
    confirmed = "niepotwierdzony"
    adding_patient.extend([first_name, last_name, pesel, phone_number, visiting_date, days_to_visit, confirmed])
    patient_visit.append(adding_patient)
    print("Dodano pacjenta!")

    # Sprawdzenie czy pesel pacjenta jest w kartotece
    if pesel in checking_patient:
        # Jeśli pesel pacjenta znajduję się w kartotece, program prosi o uzupełnienie dolegliwości pacjenta
        print("Kartotekta pacjenta już istnieje.")
        print("Co dolega pacjentowi?")
        patient_card = "\n" + input()

        for patient in patient_description:
            patient[5] = patient[5] + patient_card
    else:
        # Jeśli pesel pacjenta nie występuje w kartotece, program prosi o uzupełnienie potrzebnych danych do kartoteki
        print("Pacjent nie posiada kartoteki, proszę uzupełnić potrzebne dane: ")

        while True:
            try:
                day = int(input("Dzień urodzenia: "))
                month = int(input("Miesiąc urodzenia: "))
                year = int(input("Rok urodzenia: "))
                date_of_birth = datetime.date(year, month, day)
                date_of_birth = datetime.date.strftime(date_of_birth, "%d-%m-%Y")
                break
            except (ValueError, TypeError):
                print("Błędna data!")
        print("Co dolega pacjentowi?")
        patient_card = "\n" + input()
        # Dodawanie pacjenta do kartoteki
        patient_description.append([first_name, last_name, pesel, phone_number, date_of_birth, patient_card])
        add_to_file_description()

# Funkcja potwierdzania wizyt pacjentów, domyślnie przy dodawaniu wizyty pacjenta, program zapisuje wizytę pacjenta jako niepotwierdzoną
# Program przypomina o potwierdzeniu wizyty pacjenta, gdy do wizyty zostaną 3 dni
def confirmation_patients():
    print("\nPacjenci do potwierdzenia:")

    # Wyświetlanie pacjentów, którzy mają wizyty do potwierdzenia
    for position, i in enumerate(patient_visit, 1):
        if i[6] == "niepotwierdzony":
            print(f"{position}. {i[0]} {i[1]} numer telefonu: {i[3]} data i godzina wizyty: {i[4]}")

    while True:
        try:
            which_one = int(input("Proszę podać indeks pacjenta, żeby potwierdzić wizytę: "))
            patient_visit[which_one - 1][6] = "potwierdzony"
            add_to_file_visit()
            print(f"Pacjent został potwierdzony na wizytę dnia {patient_visit[which_one - 1][4]}.")
            break
        except ValueError:
            print("Proszę podać liczbę!")
        except IndexError:
            print("Nie ma takiego indeksu!")

# Funkcja, która wyświetla wizyty pacjentów
def date_of_patients_visit():
    print("\nWizyty pacjentów:")

    for patients in patient_visit:
        print(f"{patients[0]} {patients[1]} data {patients[4]}")

# Funkcja przesunięcia/usunięcia wizyty pacjenta
def delete_postpone_visit():
    print("\nKtórego pacjenta przesunąć/usunąć wizytę?")
    for position, patient in enumerate(patient_visit, 1):
        print(f"{position}. {patient[0]} {patient[1]} data {patient[4]}")

    while True:
        try:
            which_one = int(input("Podaj indeks: "))
            break
        except ValueError:
            print("Proszę podać liczbę!")
        except IndexError:
            print("Nie ma takiego indeksu!")
    delete_or_postpone = input("""W celu przesunięcia wizyty pacjenta proszę wpisać przesuń,
w celu usunięcia wizyty pacjenta proszę wpisać usuń: """)

    if delete_or_postpone == "usuń":
        patient_visit.pop(which_one - 1)
        print("Usunięto pacjenta!")
    elif delete_or_postpone == "przesuń":

        while True:
            try:
                visit_date = input("Podaj nową datę wizyty pacjenta DD/MM/YY oraz godzinę HH:MM: ")
                visit_date = datetime.datetime.strptime(visit_date, "%d/%m/%Y %H:%M")
                visiting_date = visit_date.strftime("%d/%m/%Y %H:%M")
                break
            except (ValueError, TypeError):
                print("Podaj poprawną datę.")

        today = datetime.datetime.today().replace(second=0, microsecond=0)
        days_to_visit = visit_date - today
        patient_visit[which_one - 1][4] = visiting_date
        patient_visit[which_one - 1][5] = days_to_visit
        print("Wizyta pacjenta została przesunięta.\n")

# Funkcja z kartoteką pacjentów
def patient_description_file():
    while True:
        # Program prosi o podanie numeru pesel pacjenta, w celu wyświetlenia jego kartoteki
        pesel = input("Podaj pesel pacjenta: ")
        if pesel.isdigit() == False or len(pesel) != 11:
            print("Błędny numer pesel.")
        else:
            break
    # Wyświetlanie kartoteki pacjenta
    for patient in patient_description:
        if pesel in patient[2]:
            print(f"{patient[0]} {patient[1]} opis pacjenta:"
                  f"{patient[5]}")
    # Program wysyła zapytanie czy chcemy uzuepłnić wizyte pacjenta
    while True:
        fill_in = input("Czy chcesz uzupełnić kartotekę pacjenta? T/N: ")
        fill_in = fill_in.upper()

        if fill_in == "T":
            description = "\n" + input("Uzupełnij kartotekę: ")
            for patient in patient_description:
                patient[5] = patient[5] + description
            print("Uzupełniono kartę pacjenta.")
            add_to_file_description()
            break
        elif fill_in == "N":
            print("Nie dokonano zmian w karcie pacjenta.")
            break
        else:
            print("Zły wybór.")

# Aktualizowanie na bieżąco czasu do wizyty pacjentów
while True:
    for i in patient_visit:
        today = datetime.datetime.today().replace(second=0, microsecond=0)
        days_to_visit = datetime.datetime.strptime(i[4], "%d/%m/%Y %H:%M") - today
        i[5] = days_to_visit
        add_to_file_visit()
        # Jeżeli do wizyty jest mniej niż 3 dni i pacjent jest niepotwierdzony, program wysyła o tym informacje
        if days_to_visit.days < 3:
            if i[6] == "niepotwierdzony":
                print(f"""Potwierdź pacjenta: {i[0]} {i[1]} o numerze telefonu: {i[3]} data i godzina wizyty: {i[4]}""")
        # Jeżeli data wizyty pacjenta minęła, program usuwa jego wizytę z systemu
        if days_to_visit.days < 0:
            patient_visit.remove(i)

    print("""Rejestr pacjentów gabinetu stomatologicznego
1. Dodaj wizytę pacjenta.
2. Potwierdzanie pacjentów.
3. Daty wizyt pacjentów.
4. Przełóż/usuń wizytę pacjenta.
5. Kartoteki pacjentów.
6. Wyjdź z rejestru.""")
    user_choice = int(input("Wybierz numer: "))

    if user_choice == 1:
        add_patient()
        # Sortowanie pacjentów od najbliższej wizyty
        for patients in patient_visit:
            patients[0], patients[5] = patients[5], patients[0]
        patient_visit = sorted(patient_visit)
        for patients in patient_visit:
            patients[0], patients[5] = patients[5], patients[0]
        add_to_file_visit()

    elif user_choice == 2:
        confirmation_patients()

    elif user_choice == 3:
        date_of_patients_visit()

    elif user_choice == 4:
        delete_postpone_visit()
        # Sortowanie pacjentów od najbliższej wizyty
        for patients in patient_visit:
            patients[0], patients[5] = patients[5], patients[0]
        patient_visit = sorted(patient_visit)
        for patients in patient_visit:
            patients[0], patients[5] = patients[5], patients[0]
        add_to_file_visit()

    elif user_choice == 5:
        patient_description_file()

    elif user_choice == 6:
        sys.exit()

    else:
        print("Nie ma takiej opcji.")