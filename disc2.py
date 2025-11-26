import discord
import responses
import gaccha
import os
import time
import yt_dlp
from dotenv import load_dotenv


queue = []
load_dotenv()


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        (
            await message.author.send(response)
            if is_private
            else await message.channel.send(response)
        )
    except Exception:
        print(" ")


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
        try:
            voice_channel = message.author.voice.channel
        except AttributeError:
            " "
        if message.author == client.user:
            return

        print(f'{username} said: "{user_message}" ({channel})')

        if user_message == "-gacha":
            whoosh = "*Whooooosh* ✧･ﾟ: *✧･ﾟ:*:✧･ﾟ: *✧･ﾟ:* ..."
            conseguido = str(gaccha.genshin(message))
            print("Deseo: ", conseguido)
            await message.channel.send(whoosh)
            time.sleep(2)
            await message.channel.send(conseguido)
        elif user_message == "-personajes":
            # 4stars
            archivo = open(str(message.author) + "_fourstars" + ".txt", "r+")
            leer = archivo.readlines()
            cuatros = []

            for lines in leer:
                cuatros.append(lines.strip())

            print(cuatros)

            # 5stars
            archivo2 = open(str(message.author) + "_fivestars" + ".txt", "r+")
            leer2 = archivo2.readlines()
            cincos = []

            for lines in leer2:
                cincos.append(lines.strip())

            print(cincos)

            # Enviar el msje con los psjes

            msje_chars = (
                "Hola "
                + str(message.author)
                + "!!"
                + "\nTus personajes cuatro estrellas son: "
                + "\n"
                + str(cuatros)
                + "\nY tus personajes cinco estrellas son: "
                + "\n"
                + str(cincos)
            )
            await message.channel.send(msje_chars)

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
