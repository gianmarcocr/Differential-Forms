import numpy as np


def phasor(t, x, y, r, T, phase):
    if isinstance(r, (int, float)):
        r1 = r * np.ones_like(t)
    else:
        r1 = r
        # r1 = r(t)/tmax
    pointx = x + r1 * np.cos((2 * np.pi / T) * t + phase)
    pointy = y + r1 * np.sin((2 * np.pi / T) * t + phase)

    return np.vstack((pointx, pointy)).T


def upper_intersection(x0, y0, r0, x1, y1, r1):
    """
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1
    """
    d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    # non intersecting
    if d > r0 + r1:
        return np.nan, np.nan
    # One circle within other
    if d < abs(r0 - r1):
        return np.nan, np.nan
    # coincident circles
    if d == 0 and r0 == r1:
        return np.nan, np.nan
    else:
        a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
        h = np.sqrt(r0 ** 2 - a ** 2)
        x2 = x0 + a * (x1 - x0) / d
        y2 = y0 + a * (y1 - y0) / d
        x3 = x2 + h * (y1 - y0) / d
        y3 = y2 - h * (x1 - x0) / d

        x4 = x2 - h * (y1 - y0) / d
        y4 = y2 + h * (x1 - x0) / d

        if y3 >= y4:  # selezione soluzione
            [x, y] = [x3, y3]
        else:
            [x, y] = [x4, y4]

        return x, y
        # return ([x3, y3], [x4, y4])


def intersection(x0, y0, r0, x1, y1, r1, choice):
    """
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1
    """

    d = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    # non intersecting
    if d > r0 + r1:
        return np.nan, np.nan
    # One circle within other
    if d < abs(r0 - r1):
        return np.nan, np.nan
    # coincident circles
    if d == 0 and r0 == r1:
        return np.nan, np.nan
    else:
        a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
        h = np.sqrt(r0 ** 2 - a ** 2)
        x2 = x0 + a * (x1 - x0) / d
        y2 = y0 + a * (y1 - y0) / d
        x3 = x2 + h * (y1 - y0) / d
        y3 = y2 - h * (x1 - x0) / d

        x4 = x2 - h * (y1 - y0) / d
        y4 = y2 + h * (x1 - x0) / d

        if choice == "up":
            if y3 >= y4:  # selezione soluzione
                [x, y] = [x3, y3]
            else:
                [x, y] = [x4, y4]
        elif choice == "down":
            if y3 <= y4:  # selezione soluzione
                [x, y] = [x3, y3]
            else:
                [x, y] = [x4, y4]

        return x, y


def line_from_points(P, Q):
    a = Q[1] - P[1]
    b = Q[0] - P[0]

    m = a / b
    q = (Q[0] * P[1] - P[0] * Q[1]) / b
    return m, q


def solution(Px, Py, l1, Qx, Qy, l2, u=0, choice="up"):
    sol = []
    for i in range(len(Px)):
        """p1, p2 = upper_intersection(Px[i],Py[i], l1 ,Qx[i], Qy[i], l2)

        m, q = lineFromPoints([Px[i],Py[i]],[Qx[i],Qy[i]])
        if p1[1] >= m * p1[0] + q:
            alpha = np.arctan(m)
            if alpha > 0:
                sol.append([p1[0] + np.cos(alpha), p1[1] + np.sin(alpha)])
            else:
                sol.append([p1[0] - np.cos(alpha), p1[1] - np.sin(alpha)])
        else:
            sol.append(p2)"""

        # x,y = upper_intersection(Px[i],Py[i], l1 ,Qx[i], Qy[i], l2)
        x, y = intersection(Px[i], Py[i], l1, Qx[i], Qy[i], l2, choice)
        sol.append([x, y])
        if u > 0:
            m, q = line_from_points([Px[i], Py[i]], sol[i])
            alpha = np.arctan(m)
            if alpha > 0:
                sol[i][0] = sol[i][0] + u * np.cos(alpha)
                sol[i][1] = sol[i][1] + u * np.sin(alpha)
            else:
                sol[i][0] = sol[i][0] - u * np.cos(alpha)
                sol[i][1] = sol[i][1] - u * np.sin(alpha)
    return np.asarray(sol)


def linecircle(x, y, r, m, q, choice):
    a = -2 * x
    b = -2 * y
    c = a ** 2 / 4 + b ** 2 / 4 - r ** 2
    a1 = 1 + m ** 2
    b1 = 2 * m * q + a + b * m
    c1 = q ** 2 + b * q + c
    delta = b1 ** 2 - 4 * a1 * c1
    if delta > 0:
        if choice == "1":
            x1 = (-b1 + np.sqrt(delta)) / (2 * a1)
        elif choice == "2":
            x1 = (-b1 - np.sqrt(delta)) / (2 * a1)

    if delta <= 0:
        print("non va dio can")
    return x1, m * x1 + q


def prolunga(Sx, Sy, Cx, Cy, r, choice="2"):
    sol = []
    for i in range(len(Sx)):
        m, q = line_from_points([Sx[i], Sy[i]], [Cx[i], Cy[i]])
        sol.append(linecircle(Cx[i], Cy[i], r, m, q, choice))
    return np.asarray(sol)


class Phasor:
    def __int__(self):