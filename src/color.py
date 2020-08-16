class Fore:
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37


class Back:
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47


def CSI(n):
    return f'\x1b[{n}m'


def test():
    text = ''
    for n in range(108):
        if n != 0 and n % 10 == 0:
            text += '\n'
        #  text += CSI(n) + f'CSI{n}' + CSI(0)
        text += CSI(n) + 'test' + CSI(0) + '  '
    print(text)


if __name__ == '__main__':
    test()
