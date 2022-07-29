""""Kwota słownie."""

def kwota_dowypisania(kwota):
    nominal = ["złotych", "złote"]
    cyfry = ["zero", "jeden", "dwa", "trzy", "cztery", "pięć", "sześć", "siedem", "osiem", "dziewięć", "dziesięć",
             "jedenaście", "dwanaście", "trzynaście", "czternaście", "piętnaście", "szesnaście", "siedemnaście", "osiemnaście", "dziewiętnaście"]
    dziesiat = ["dwadzieścia", "trzydzieści", "czterdzieści", "pięćdziesiąt", "sześćdziesiąt", "siedemndziesiąt", "osiemdziesiąt", "dziewięćdziesiąt"]
    setki = ["sto", "dwieście", "trzysta", "czterysta", "pięćset", "sześćset", "siedemset", "osiemset", "dziewięćset"]
    tysiace = ["tysiąc", "tysiące", "tysięcy"]
    milion = ["milion", "milony", "milionów"]
    slownie = []

    if kwota == 0:
        slownie.append(f"{cyfry[0]} {nominal[0]}")

        if kwota < 20:
            slownie.append(cyfry[kwota])
            if 1 < kwota < 5:
                slownie.append(nominal[1])
            else:
                slownie.append(nominal[0])
            kwota -= kwota
        elif 100 > kwota >= 20:
            kwota1 = kwota // 10
            slownie.append(dziesiat[int(kwota1-2)])
            if kwota % 10 == 0:
                slownie.append(nominal[0])
            kwota1 *= 10
            kwota1 = kwota - kwota1
        elif 1000 > kwota >= 100:
            kwota1 = kwota // 100
            slownie.append(setki[int(kwota1-1)])
            if kwota % 100 == 0:
                slownie.append(nominal[0])
            kwota1 *= 100
            kwota1 = kwota - kwota1
    return slownie

liczba = 300

while liczba > 0:
    kwota_dowypisania(liczba)
    break

print(kwota_dowypisania(liczba))
