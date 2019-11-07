import random


def count(number, secret):
    c1 = list(str(number))
    c2 = list(str(secret))
    biki, korovi = 0, 0
    for i in range(min(len(c1), len(c2))):
        if c1[i] == c2[i]:
            biki += 1
        elif c1[i] in c2:
            korovi += 1
    return biki, korovi


def generate_num():
    global was, number
    i = 0
    if not number:
        return random.randint(1000, 10000)
    while 1:
        i += 1
        num = random.randint(1000, 10000)
        if all(count(n, num) == was[n] for n in was):
            break
        elif i > 2000000:
            break
    return num


def play():
    global was, secret
    print()
    print("Ваш ход.")
    cin = int(input())
    while len(str(cin)) != 4 or len(set(str(cin))) == 1:
        print("Некорректное число")
        cin = int(input())
    return cin


def main():
    global was, number, secret
    print("Игра началась!")
    was = {}
    number = 0
    secret = generate_num()
    while 1:
        number = play()
        if number == secret:
            print("BINGO!!!")
            print("You win!")
            break
        count_vick = count(number, secret)
        if number not in was:
            was[number] = count_vick[0], count_vick[1]
        if count_vick[0] == 3:
            secret = generate_num()
        print("Быков:", count_vick[0], " --- ", "Коров:", count_vick[1])
        print('Сейчас загаданное число =', secret)


if __name__ == '__main__':
    main()