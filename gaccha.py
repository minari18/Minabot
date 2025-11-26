# Genshin gacha but better
import random
import sys
import borrarlineas
import time

# Repliquemos el sistema de gacha de genshin, con un poquito más de probabilidad

# Probabilidades
# 5 estrellas = 1%
# 4 estrellas = 5%
# 3 estrellas = 94 %


def genshin(mensaje):

    usuario_4s = str(mensaje.author) + "_fourstars" + ".txt"
    four_star_conseguidos = open(usuario_4s, "a+")

    usuario_5s = str(mensaje.author) + "_fivestars" + ".txt"
    five_stars_conseguidos = open(usuario_5s, "a+")

    usuario_pity = str(mensaje.author) + "_pity" + ".txt"
    pity = open(usuario_pity, "a+")
    leer_pity = pity.readlines()

    # Leer el pity
    pity_cantidad = []
    with open(usuario_pity, "r+") as read_pity:
        num_pity = read_pity.readlines()
        # print("Pity read: ", num_pity)
        for elementos in num_pity:
            pity_cantidad.append(elementos.strip())

    #

    print(len(pity_cantidad))
    print(len(leer_pity))
    five_stars = [
        "qiqi",
        "jean",
        "diluc",
        "keqing",
        "mona",
        "xiao",
        "venti",
        "ganyu",
        "albedo",
        "hutao",
        "wanderer",
        "itto",
        "ayaka",
        "raiden shogun",
        "yelan",
        "kokomi",
        "yoimiya",
        "zhongli",
        "yae miko",
        "ayato",
        "kazuha",
        "tighnari",
        "eula",
        "klee",
        "tartaglia",
        "nahida",
        "aloy",
        "nilou",
    ]
    # print(len(five_stars))

    four_stars = [
        "fischl",
        "bennett",
        "rosaria",
        "sucrose",
        "xiangling",
        "kaeya",
        "layla",
        "thoma",
        "xingqiu",
        "noelle",
        "barbara",
        "sayu",
        "yaoyao",
        "kujou sara",
        "collei",
        "faruzan",
        "candace",
        "dori",
        "yunjin",
        "gorou",
        "yanfei",
        "diona",
        "chongyun",
        "beidou",
        "razor",
        "lisa",
        "kuki shinobu",
        "xinyan",
    ]

    # print(len(four_stars))

    # Listas 4 y  5 star
    lista_4star = []
    lista_5star = []

    # Crear una lista para las armas random, para un 94%
    lista_3_stars = []
    for i in range(94):
        lista_3_stars.append("arma random")

    lista_gacha = lista_3_stars.copy()

    # Crear la lista final

    if int(len(lista_gacha)) < 100:
        for i in range(5):
            random_4star = random.choice(four_stars)
            lista_4star.append(random_4star)
        # Lista 5 star (1%)
        random_5star = random.choice(five_stars)
        lista_5star.append(random_5star)

        lista_gacha.extend(lista_4star)
        lista_gacha.extend(lista_5star)
        # print("Cantidad: ", len(lista_gacha))
        # print(lista_5star)
        # print(lista_4star)
    else:
        for i in range(6):
            lista_gacha.pop()
        lista_5star.clear()
        lista_4star.clear()
        for i in range(5):
            random_4star = random.choice(four_stars)
            lista_4star.append(random_4star)
        # Lista 5 star (1%)
        random_5star = random.choice(five_stars)
        lista_5star.append(random_5star)

        lista_gacha.extend(lista_4star)
        lista_gacha.extend(lista_5star)

    print("Cantidad 2: ", len(lista_gacha))
    print(lista_5star)
    print(lista_4star)

    if int(len(pity_cantidad)) % 70 == 0 and int(len(pity_cantidad)) > 0:
        pity.write("1")
        pity_cantidad.clear()
        borrarlineas.delete_lines(usuario_pity)
        cinco_estrella = random.choice(five_stars)
        print("\n" + cinco_estrella + "\nPity: " + str(len(pity_cantidad)))

        if cinco_estrella in five_stars:
            five_stars_conseguidos.write(cinco_estrella + "\n")
            return (
                "Obtuviste.... "
                + str(cinco_estrella)
                + "!!"
                + "\nPity: "
                + str(len(pity_cantidad))
            )
        print(
            "\nFive stars:\n",
            five_stars_conseguidos,
            "\nFour stars: \n",
            four_star_conseguidos,
        )

    else:
        if (int(len(pity_cantidad))) % 10 == 0 and int(len(pity_cantidad)) > 0:
            pity.write("1" + "\n")
            cuatro_estrella = random.choice(four_stars)
            print("\n" + cuatro_estrella + "\nPity: " + str(len(pity_cantidad)))
            if cuatro_estrella in four_stars:
                four_star_conseguidos.write(cuatro_estrella + "\n")
                return (
                    "Obtuviste.... "
                    + str(cuatro_estrella)
                    + "!!"
                    + "\nPity: "
                    + str(len(pity_cantidad))
                )
        else:
            pity.write("1" + "\n")
            deseo = random.choice(lista_gacha)
            print(deseo + "\nPity: " + str(len(pity_cantidad)))

            if deseo in four_stars:
                four_star_conseguidos.write(deseo + "\n")

            if deseo in five_stars:
                five_stars_conseguidos.write(deseo + "\n")
            return (
                "Obtuviste.... "
                + str(deseo)
                + "!!"
                + "\nPity: "
                + str(len(pity_cantidad))
            )
    four_star_conseguidos.close()
    five_stars_conseguidos.close()
    pity.close()
