import math

def haversineDist(a, b):
    #lon1, lat1, lon2, lat2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    lon1, lat1, lon2, lat2 = map(math.radians, a + b)
    res = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return math.asin(math.sqrt(res)) * 2 * 6371  # Radius of earth in kilometers


# NOT USED
def round_sig(x, sig=2): return float("{:.{p}g}".format(x, p=sig))


# NOT USED
def prettify(dist):
    """dist is in km"""
    if dist >= 1: return str(round_sig(dist)) + "km"
    return str(int(round_sig(dist * 1000))) + "m"

def load():
    return eval("".join(open("save.txt", "r").readlines()))


def titleToSpace(s):
    output = [""]
    for letter in s:
        if letter.isupper():
            output.append(letter)
        else:
            output[-1] += letter
    return " ".join([i.capitalize() for i in output]).strip()
