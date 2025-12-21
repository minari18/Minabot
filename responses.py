# Archivo que guarda las respuesta del bot ante un mensaje
import random
from gaccha import *


def Randomize(a):
    return random.choice(a)


pets = ["Cat", "Dog", "Fish", "Bunny"]

total_pets = []
dogs = []
fish = []
cats = []
bunnies = []


def get_response(message):
    u_message = message.lower()

    if u_message == "hola":
        return "Hola creador"

    if u_message == "-dado":
        return str(random.randint(1, 6))

    if u_message == "-pet":
        option = str(Randomize(pets))

        if option.lower() == "dog":
            total_pets.append("1")
            dogs.append("1")
            return (
                "Obtuviste un perrito! \nTiene un total de: "
                + str(len(total_pets))
                + " mascotas"
                + "\nY un total de: "
                + str(len(dogs))
                + " perritos."
            )

        elif option.lower() == "cat":
            total_pets.append("1")
            cats.append("1")
            return (
                "Obtuviste un gatito! \nTiene un total de: "
                + str(len(total_pets))
                + " mascotas"
                + "\nY un total de: "
                + str(len(cats))
                + " gatitos."
            )

        elif option.lower() == "fish":
            total_pets.append("1")
            fish.append("1")
            return (
                "Obtuviste un pez! \nTiene un total de: "
                + str(len(total_pets))
                + " mascotas"
                + "\nY un total de: "
                + str(len(fish))
                + " peces."
            )

        elif option.lower() == "bunny":
            total_pets.append("1")
            bunnies.append("1")
            return (
                "Obtuviste un conejito! \nTiene un total de: "
                + str(len(total_pets))
                + " mascotas"
                + "\nY un total de: "
                + str(len(bunnies))
                + " conejitos."
            )
    if u_message == "-gachainfo":
        return (
            "*Genshin Gacha en discord!!*\n"
            + "\nCon las mismas funciones del gacha de genshin, con un poquito más de probabilidad (we mihoyo haters)\n"
            + "-5 estrellas = 1%\n"
            + "-4 estrellas = 5%\n"
            + "-3 estrellas = 94 %\n"
            + "*4 star pity: cada 10 deseos\n"
            + "*5 star pity: cada 70 deseos\n"
            "\nAdemás, no hay sistema de personajes limitados. Si consigues un deseo dorado. te podrá tocar cualquier five star!!\n"
            + "\nAnd... thats pretty much it! Enjoy pulling for characters!!"
        )
