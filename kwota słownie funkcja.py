def kwota_slownie(kwota):
    jednosci = ["zero", "jeden", "dwa", "trzy", "cztery", "pięć", "sześć", "siedem", "osiem", "dziewięć", "dziesięć",
             "jedenaście", "dwanaście", "trzynaście", "czternaście", "piętnaście", "szesnaście", "siedemnaście", "osiemnaście", "dziewiętnaście"]
    dziesiatki = ["dwadzieścia", "trzydzieści", "czterdzieści", "pięćdziesiąt", "sześćdziesiąt", "siedemndziesiąt", "osiemdziesiąt", "dziewięćdziesiąt"]
    setki = ["sto", "dwieście", "trzysta", "czterysta", "pięćset", "sześćset", "siedemset", "osiemset", "dziewięćset"]
    grupy = [[" "],
             ["tysiąc", "tysiące", "tysięcy"],
            ["milion", "miliony", "milionów"]]

    grupy1 = 0
    lista = []

    while kwota != 0:
        slownie = []
        setki1 = kwota % 1000 // 100
        dziesiatki1 = kwota % 100 // 10
        jednosci1 = kwota % 10
        if setki1 > 0:
            slownie.append(setki[setki1-1])
        if dziesiatki1 > 1:
            slownie.append(dziesiatki[dziesiatki1-2])
        if dziesiatki1 == 1:
            dziesiatki1 *= 10
            nascie = dziesiatki1+jednosci1
            slownie.append(jednosci[nascie])
        elif jednosci1 > 0:
            slownie.append(jednosci[jednosci1])
        if jednosci1 == 1 and setki1 + dziesiatki1 == 0:
            tysiace_plus = 0
        elif 2 <= jednosci1 < 5 and dziesiatki1 < 20:
            tysiace_plus = 1
        else:
            tysiace_plus = 2

        if grupy1 > 0:
            slownie.append(grupy[grupy1][tysiace_plus])
        slownie = ' '.join(slownie)
        lista.insert(0, slownie)
        kwota //= 1000
        grupy1 += 1
    return ' '.join(lista)


print(kwota_slownie(534023))