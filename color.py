
def CSI(n): 
    return f'\x1b[{n}m'

Black = '30'
Red = '31'
Green = '32'
Yellow = '33'
Blue = '34'
Purple = '35'
Cyanine = '36'
White = '37'





class Color:
    black = '30'
    red = '31'
    green = '32'
    yellow = '33'
    blue = '34'
    purple = '35'
    cyanine = '36'
    white = '37'
    # b_blue = '44'
    # black = '90'
    # red = '91'
    # green = '92'
    # yellow = '93'
    # blue = '94'
    # purple = '95'
    # cyanine = '96'
    # white = '97'

    @classmethod
    def colortext(cls, color, text):
        return '\033[1;{}m{}\033[0m'.format(color, text)

    @classmethod
    def embed_colortext(cls, color, origincolor, text):
        return '\033[0m\033[1;{}m{}\033[0m\033[1;{}m'.format(
            color, text, origincolor)

    @classmethod
    def test(cls):
        origin = cls.colortext(cls.black, 'I {} you')
        embed = cls.embed_colortext(cls.cyanine, cls.black, 'fuck')
        ultimate = origin.format(embed)
        print(ultimate)

    @classmethod
    def test_allcolor(cls, text):
        print('\033[1;{}m{}\033[0m'.format(cls.black, text))
        print('\033[1;{}m{}\033[0m'.format(cls.red, text))
        print('\033[1;{}m{}\033[0m'.format(cls.green, text))
        print('\033[1;{}m{}\033[0m'.format(cls.yellow, text))
        print('\033[1;{}m{}\033[0m'.format(cls.blue, text))
        print('\033[1;{}m{}\033[0m'.format(cls.purple, text))
        print('\033[1;{}m{}\033[0m'.format(cls.cyanine, text))


        print('\033[1;{}m{}\033[0m'.format(cls.white, text))

def test():
    text = ''
    for n in range(108):
        if n != 0 and n%10 == 0:
            text += '\n'
        #  text += CSI(n) + f'CSI{n}' + CSI(0)
        text += CSI(n) +  'test' + CSI(0) + '  '
    print(text)

def colored(text, color):
    #  return text
    return text



if __name__ == '__main__':
    test()
