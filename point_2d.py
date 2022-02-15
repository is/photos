__version__ = '0.0.1'

def extract_xy(*args):
    if len(args) == 1 and (type(args[0]) == int or type(args[0]) == float):
        return (args[0], args[0])

    if len(args) == 2:
        return (args[0], args[1])

    arg = args[0]
    if type(arg) == list or type(arg) == tuple:
        return arg[:2]

    if type(arg) == Point2D:
        return arg
    return args[:2]


class Point2D(tuple):
    def __new__(self, *args):
        x, y = extract_xy(*args)
        return tuple.__new__(Point2D, (x, y))

    def __mul__(self, p):
        x, y = extract_xy(p)
        return Point2D(self[0] * x, self[1] * y)
    
    def __add__(self, p):
        x, y = extract_xy(p)
        return Point2D(self[0] + x, self[1] + y)
    
    def __truediv__(self, p):
        x, y = extract_xy(p)
        return Point2D(self[0] / x, self[1] / y)
    
    def __sub__(self, p):
        x, y = extract_xy(p)
        return Point2D(self[0] - x, self[1] - y)

    def center_extend(self, *p):
        r = Rect(self, self)
        return r.center_extend(*p)

    def extend(self, *p):
        r = Rect(self, self)
        return r.extend(*p)


class Rect(tuple):
    def __new__(self, P0, P1):
        return tuple.__new__(Rect, (P0, P1))

    def move(self, P):
        self.P0 += P
        self.P1.add(P)
        return self

    def extend(self, *p):
        P = Point2D(*p)
        return Rect(self[0], self[1] + P)
    ex = extend

    def center_extend(self, *p):
        P =Point2D(*p) / 2
        return Rect(self[0] - P, self[1] + P)
    exc = center_extend

# 
P2 = Point2D
R = Rect

if __name__ == '__main__':
    P0 = Point2D(10, 20)
    print(P0)
    P1 = P0 * 2
    print(P1)
    P2 = P1 - 5
    print(P2)
    # print(P0.add(5))
    # P0.sub(30, 30)
    # print(P0)
    # r = P0.center_extend(10, 10)
    # print(r)
    # P1 = Point2D(P0)
    # print(P1)
    # P3 = P1 + P0
    # print(len(P3))
    # x, y = P3
    # print(x, y)
