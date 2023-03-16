def hello():
    print("                                  Приветствую в игре 'Крестики и Нолики'!!!")
    print("     Правила:")
    print(" 1. Для того чтобы поставить крестик или нолик, нужно ввести номер строки и номер столбца через пробел.")
    print(" 2. Первым ходит крестик.")
    print(" 3. Выигрывает тот, кто сумеет занять тремя крестиками или ноликиами строку, столбец или диагональ")
    print(" ")


def fieldsh():
    print(f"  0  1  2")
    for i in range(3):
        print(f"{i} {gamefield[i][0]} {gamefield[i][1]} {gamefield[i][2]}")


def askncheck():
    while True:
        coords = input(" Ваш ход: ").split()
        if len(coords) != 2:
            print("Введите 2 координаты! ")
            continue

        x, y = coords

        if not(x.isdigit()) or not(y.isdigit()):
            print(" Введите числа! ")
            continue

        x, y = int(x), int(y)

        if 0 > x or x > 2 or 0 > y or y > 2:
            print(" Координаты вне диапазона! ")
            continue

        if gamefield[x][y] != " ":
            print(" Клетка занята! ")
            continue

        return x, y


def win():
    win_coord = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))
    for coords in win_coord:
        symbols = []
        for c in coords:
            symbols.append(gamefield[c[0]][c[1]])
        if symbols == ["X", "X", "X"]:
            print("Выиграл крестик !!!")
            return True
        if symbols == ["0", "0", "0"]:
            print("Выиграл нолик !!!")
            return True
    return False


hello()
gamefield = [[" "]*3 for i in range(3)]

hod = 0
while True:
    hod += 1

    fieldsh()

    if hod % 2 == 1:
        print(" Ход крестика: ")
    else:
        print(" Ход нолика: ")

    x, y = askncheck()

    if hod % 2 == 1:
        gamefield[x][y] = "X"
    else:
        gamefield[x][y] = "0"

    if win():
        break

    if hod == 9:
        print("Ничья")
        break
