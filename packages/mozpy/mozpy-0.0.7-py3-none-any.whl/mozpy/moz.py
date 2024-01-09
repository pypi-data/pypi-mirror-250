import colorama
def printer(string):
    print(colorama.Fore.YELLOW+string, end='🍌')


def s1():
    while 1:
        a = (input('add ra vared konid'))
        if len(a) == 3:
            a = int(a)
            print(f"{a%10} x1")
            print(f"{a%100-a%10} x10")
            print(f"{a-a%100} x100")
            exit()


s1()