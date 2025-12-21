import asyncio
import discord
import responses
import gaccha
import gpt
import os
import sqlite3
import time
import yt_dlp
from dotenv import load_dotenv


queue = []
load_dotenv()
DB_PATH = "gacha.db"


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        (
            await message.author.send(response)
            if is_private
            else await message.channel.send(response)
        )
    except Exception as e:
        return


def Run_DiscordBot():
    TOKEN = os.getenv("TOKEN")
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_message(message):
        username = message.author
        user_message = message.content
        channel = message.channel

        # Meterse al canal de voz
        try:
            voice_channel = message.author.voice.channel
        except AttributeError:
            " "

        # Menciones al bot
        if client.user in message.mentions:
            prompt = message.content.replace(f"<@{client.user.id}>", "").strip()
            # Validar si no hay mensaje aparte de lam ención
            if not prompt:
                await message.channel.send(
                    "Hola!! Soy Testbot0418 ૮ ˶ᵔ ᵕ ᵔ˶ ა. ¿En qué puedo ayudarte?"
                )
                return
            response = gpt.ask_gpt(prompt)
            await message.channel.send(response)

        # Mensajes de usuarios del servidor
        print(f'{username} said: "{user_message}" ({channel})')

        if user_message == "-gacha":
            whoosh = "*Whooooosh* ✧･ﾟ: *✧･ﾟ:*:✧･ﾟ: *✧･ﾟ:* ..."
            obtained, rarity, pity = gaccha.genshin(message.author)
            print("Deseo: ", obtained)
            await message.channel.send(whoosh)
            time.sleep(2)
            if rarity == 4:
                gif = await message.channel.send(file=discord.File("wish/4star.gif"))
                await asyncio.sleep(8)
                await gif.delete()
                await message.channel.send(
                    file=discord.File(f"gchars/{obtained.lower()}.png")
                )
                char_msg = f"Obtuviste... {obtained}!!\nPity: {pity}"
                await message.channel.send(char_msg)
            elif rarity == 5:
                gif = await message.channel.send(file=discord.File("wish/5star.gif"))
                await asyncio.sleep(8)
                await gif.delete()
                await message.channel.send(
                    file=discord.File(f"gchars/{obtained.lower()}.png")
                )
                char_msg = f"Obtuviste... {obtained}!!\nPity: {pity}"
                await message.channel.send(char_msg)
            else:
                await message.channel.send(f"Obtuviste... {obtained}!!\nPity: {pity}")

        elif user_message == "-personajes":
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()

            # Usamos discrim/username como user_id
            user_id = int(message.author.id)

            c.execute(
                """
                SELECT c.name, c.rarity, ui.constellation, ui.obt_date
                FROM user_inventory AS ui
                JOIN characters AS c ON ui.char_id = c.char_id
                WHERE ui.user_id = ?
                ORDER BY c.rarity DESC, c.name
                """,
                (user_id,),
            )

            rows = c.fetchall()
            conn.close()

            if not rows:
                await message.channel.send("Aún no tienes personajes. Usa -gacha :D")
                return

            # Separar por rareza
            five = [
                (r[0], r[2], r[3]) for r in rows if r[1] == 5
            ]  # (name, quantity, date)
            four = [(r[0], r[2], r[3]) for r in rows if r[1] == 4]

            # Construcción del mensaje
            msg = f"Hola {message.author.name}!!\n\n"

            msg += "Acá están tus personajes cinco estrellas:\n"
            if five:
                for name, qty, date in five:
                    msg += f"{name} (C{qty-1}) | Obtenido el {date}\n"
            else:
                msg += "Ninguno\n"

            msg += "\nY acá están tus personajes cuatro estrellas:\n"
            if four:
                for name, qty, date in four:
                    msg += f"{name} (C{qty-1}) | Obtenido el {date}\n"
            else:
                msg += "Ninguno\n"

            total_personajes = len(rows)

            msg += f"\nTienes un total de **{total_personajes} personajes!!**"

            await message.channel.send(msg)

        elif user_message == "-comandos":
            comandos = "play; pause; stop; gachainfo; gacha; personajes; dado; pet"
            await message.channel.send(comandos)

        if message.content.startswith("-play"):
            query = message.content[6:]
            voice_client = discord.utils.get(client.voice_clients, guild=message.guild)

            if not voice_client:
                if message.author.voice:
                    voice_channel = message.author.voice.channel
                    voice_client = await voice_channel.connect()
                else:
                    await message.channel.send(
                        "You need to be in a voice channel to use this command."
                    )
                    return

            # Borrar cookies si se está usando el bot de manera local y no en AWS EC2
            ydl_opts = {"format": "bestaudio/best", "quiet": True}

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][
                    0
                ]
                url = info["url"]
                source = await discord.FFmpegOpusAudio.from_probe(
                    url, executable="ffmpeg/bin/ffmpeg.exe", method="fallback"
                )

            if voice_client.is_playing():
                voice_client.stop()

            voice_client.play(
                source, after=lambda e: print("Player error: %s" % e) if e else None
            )
            await message.channel.send(f'Playing: {info["title"]}')

        if message.content == "-stop":
            voice_client = discord.utils.get(client.voice_clients, guild=message.guild)
            if voice_client.is_playing():
                voice_client.stop()
            await voice_client.disconnect()
            await message.channel.send("Stopped.")

        if message.content == "-pause":
            voice_client = discord.utils.get(client.voice_clients, guild=message.guild)
            if voice_client.is_playing():
                voice_client.pause()
            await message.channel.send("Paused.")

        if message.content == "-resume":
            voice_client = discord.utils.get(client.voice_clients, guild=message.guild)
            if voice_client.is_paused():
                voice_client.resume()
            await message.channel.send("Resumed.")

        if message.content == "-skip":
            voice_client = discord.utils.get(client.voice_clients, guild=message.guild)
            if voice_client.is_playing():
                voice_client.stop()
        else:
            await send_message(message, user_message, is_private=False)

    # Correr el bot
    client.run(TOKEN)
