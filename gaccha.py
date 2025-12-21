import sqlite3
import random

DB_PATH = "gacha.db"


def genshin(user):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Obtener el id de discord del usuario
    user_id = user.id

    # Crear usuario si no existe
    c.execute(
        """
        INSERT OR IGNORE INTO users (user_id, username, pity_4star, pity_5star)
        VALUES (?, ?, 0, 0)
    """,
        (user_id, user.name),
    )

    # Leer pity
    c.execute("SELECT pity_4star, pity_5star FROM users WHERE user_id = ?", (user_id,))
    pity_4star, pity_5star = c.fetchone()

    # Obtener personajes de la db
    c.execute("SELECT char_id, name FROM characters WHERE rarity = 5")
    five_stars = c.fetchall()

    c.execute("SELECT char_id, name FROM characters WHERE rarity = 4")
    four_stars = c.fetchall()

    lista_3stars = ["arma random"] * 94

    # Lógica del gacha
    rarity = 3
    obtained_id = None
    obtained_name = None

    # Pity para 5 stars
    if pity_5star >= 69:
        obtained_id, obtained_name = random.choice(five_stars)
        rarity = 5
        pity_5star = -1
        pity_4star = -1

    # Pity para 4 stars
    elif pity_4star >= 9:
        obtained_id, obtained_name = random.choice(four_stars)
        rarity = 4
        pity_4star = -1

    # Obtenidos fuera del pity
    else:
        r = random.randint(1, 100)
        if r <= 1:
            obtained_id, obtained_name = random.choice(five_stars)
            rarity = 5
            pity_5star = -1
            pity_4star = -1

        elif r <= 6:
            obtained_id, obtained_name = random.choice(four_stars)
            rarity = 4
            pity_5star = -1
            pity_4star = -1

        else:
            obtained_name = random.choice(lista_3stars)
            obtained_id = None

    # Guardar en la db el personaje
    if obtained_id is not None:
        c.execute(
            """
            INSERT INTO user_inventory (user_id, char_id, constellation)
            VALUES (?, ?, 1)
            ON CONFLICT(user_id, char_id)
            DO UPDATE SET constellation = constellation + 1
        """,
            (user_id, obtained_id),
        )

    # Actualizar pity
    pity_4star += 1
    pity_5star += 1

    c.execute(
        """
        UPDATE users
        SET pity_4star = ?, pity_5star = ?
        WHERE user_id = ?
    """,
        (pity_4star, pity_5star, user_id),
    )

    conn.commit()
    conn.close()

    return obtained_name, rarity, pity_5star
