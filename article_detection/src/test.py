import six
from src.detection import Detection

detection = Detection()
try:
    while True:
        q = six.moves.input('>> ')
        result = detection.is_political([q])
        print('input: {}'.format(q))
        if result:
            print('***     Dit is een nieuwsartikel!')
        else:
            print('         Dit is geen politiek artikel')

except EOFError:
    pass
