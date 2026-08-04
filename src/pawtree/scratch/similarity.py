import math

def cosine_similarity(a: list[float], b: list[float]) -> float:
    xy_sum = 0.0
    xx_sum = 0.0
    yy_sum = 0.0
    for x, y in zip(a,b):
        xy_sum += x * y
        xx_sum += x * x
        yy_sum += y * y
    return xy_sum / (math.sqrt(xx_sum) * math.sqrt(yy_sum))

    # steg 1: skalärprodukt — multiplicera parvis, summera
    # steg 2: längden av a
    # steg 3: längden av b
    # steg 4: return steg1 / (steg2 * steg3)
    ...

if __name__ == "__main__":
    print(cosine_similarity([1.0, 0.0], [1.0, 0.0]))   # ska bli 1.0
    print(cosine_similarity([1.0, 0.0], [0.0, 1.0]))   # ska bli 0.0
    print(cosine_similarity([0.9, 0.1], [0.85, 0.15])) # hund vs valp — gissa!