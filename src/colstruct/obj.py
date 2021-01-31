import math


def design_load(LL: int, DL: int) -> float:

    result = (1.6 * LL) + (1.2 * DL)

    return result


# Tied vs spiral is not yet implemented


class Column(object):
    def __init__(self, type_, gross_area, height, Fy, fc, radius_gyration, Pmax):

        self.type_ = type_
        self.height = height
        self.gross_area = gross_area
        self.R = 1.07 - 0.008 * ((height * 12) / radius_gyration)
        self.Fy = Fy
        self.fc = fc
        self.Pmax = Pmax

        _reduced_area = self.R * 0.65 * 0.8 * gross_area
        _x = Pmax - (_reduced_area * (0.85 * fc))
        _y = (_reduced_area * Fy) + (_reduced_area) * (0.85 * fc) * -1

        self.Pg = _x / _y

    @classmethod
    def square(cls, type_, height, DL, LL, Fy, fc):

        Pmax = design_load(DL, LL)

        Ag = Pmax / (1 * 0.65 * 0.8 * (0.85 * fc * (1 - 0.03) + (Fy * 0.03)))

        d = math.sqrt(Ag)
        Ag = math.pow(d, 2)

        radius_gyration = 0.3 * d

        return cls(type_, Ag, height, Fy, fc, radius_gyration, Pmax)

    @classmethod
    def circle(cls, type_, diameter, height, DL, LL, Fy, fc):

        Pmax = design_load(DL, LL)

        Ag = math.pi * math.pow((diameter / 2), 2)

        radius_gyration = 0.25 * diameter

        return cls(type_, Ag, height, Fy, fc, radius_gyration, Pmax)


a = Column.circle("tied", 14, 12, 150, 60, 60, 5)


print(a.R)