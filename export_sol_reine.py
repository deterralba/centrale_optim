for l in open('copy'):
    import re
    m = re.match(r'x#(\d+)#(\d+)\s', l)
    pos = '{:0>2}'.format(m.groups()[1])
    print(pos, end='')