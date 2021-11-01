import math, json, base64
from pathlib import Path, PurePath
from io import BytesIO
from PIL import Image

def DecodeImage(base64Image):
    return BytesIO(base64.b64decode(base64Image))

def IsColor(r, g, b):
    color_dist = abs(r-g) + abs(g-b) + abs(r-b)
    result = True
    if color_dist <= 70:
        result = False
    return result

def IsWhite(r, g, b):
    min_val = min(r,g,b)
    color_dist = abs(r-g) + abs(g-b) + abs(r-b)
    result = False
    if min_val >= 240 and color_dist <= 6:
        result = True
    return result

def EnhanceColor(normalized):
    if normalized > 0.04045:
        return math.pow( (normalized + 0.055) / (1.0 + 0.055), 2.4)
    else:
        return normalized / 12.92

def RGBtoXY(r, g, b):
    rNorm = r / 255.0
    gNorm = g / 255.0
    bNorm = b / 255.0
    rFinal = EnhanceColor(rNorm)
    gFinal = EnhanceColor(gNorm)
    bFinal = EnhanceColor(bNorm)
    X = rFinal * 0.649926 + gFinal * 0.103455 + bFinal * 0.197109
    Y = rFinal * 0.234327 + gFinal * 0.743075 + bFinal * 0.022598
    Z = rFinal * 0.000000 + gFinal * 0.053077 + bFinal * 1.035763
    if X + Y + Z == 0:
        return (0,0)
    else:
        xFinal = X / (X + Y + Z)
        yFinal = Y / (X + Y + Z)
        return (xFinal, yFinal)

def RGBtoHEX(color):
    return '#%02x%02x%02x' % color

def FillBulbs(colors, bulbs=1):
    bulb_colors = []
    for c in colors:
        r = c[0]
        g = c[1]
        b = c[2]
        if IsColor(r,g,b) or IsWhite(r,g,b):
            bulb_colors.append(RGBtoXY(r,g,b))
    if len(bulb_colors) > 0 and len(bulb_colors) <= bulbs:
        i = 0
        l = len(bulb_colors)
        while len(bulb_colors) < bulbs:
            bulb_colors.append(bulb_colors[i%l])
    return bulb_colors
