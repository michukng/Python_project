# Program wydaje resztę w największych możliwych bankontach/monetach
wartosc_nominalu = [500, 200, 100, 50, 20, 10, 5, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]

ilosc_przechowywana = {}

x = 0

while True:
    try:
        kwota = float(input("Reszta do wydania: "))
        break
    except ValueError:
        print("Podana kwota jest nieprawidłowa")

while kwota > 0:
    ilosc = int(kwota / wartosc_nominalu[x])
    kwota = round(kwota % wartosc_nominalu[x], 2)
    z = wartosc_nominalu[x]
    if ilosc > 0:
        ilosc_przechowywana[z] = ilosc
    x += 1

for x, y in ilosc_przechowywana.items():
    print(f"{x} zł - {y} szt")