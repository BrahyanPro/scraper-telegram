#!/bin/env python3

from enum import Enum
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
from telethon.tl.functions.users import GetFullUserRequest
import asyncio
import configparser
import os, sys
import csv
import json
import random
import time

re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"
SLEEP_TIME = 30
UPDATE_TIME = 10


class ExitCode(Enum):
    SUCCESS = 0
    NO_SETUP_ERROR = 1
    INVALID_MODE_ERROR = 2
    FLOOD_ERROR = 3


class main():

    def banner():
        print(f"""
    {re}╔╦╗{cy}┌─┐┬  ┌─┐{re}╔═╗  ╔═╗{cy}┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐
    {re} ║ {cy}├┤ │  ├┤ {re}║ ╦  ╚═╗{cy}│  ├┬┘├─┤├─┘├┤ ├┬┘
    {re} ╩ {cy}└─┘┴─┘└─┘{re}╚═╝  ╚═╝{cy}└─┘┴└─┴ ┴┴  └─┘┴└─
                version : 2.0
        Brahyan Pro Hacker, estamos enviando mensajes
    """)

    async def send_sms():
        try:
            cpass = configparser.RawConfigParser()
            cpass.read('config.data')
            api_id = cpass['cred']['id']
            api_hash = cpass['cred']['hash']
            phone = cpass['cred']['phone']
        except KeyError:
            os.system('clear')
            main.banner()
            print(re + "[!] run python3 setup.py first !!\n")
            sys.exit(1)

        client = TelegramClient(phone, api_id, api_hash)

        await client.connect()
        if not await client.is_user_authorized():
            client.send_code_request(phone)
            os.system('clear')
            main.banner()
            client.sign_in(phone, input(gr + '[+] Enter the code: ' + re))


        os.system('clear')
        main.banner()
        input_file = "members.json"
        users = []
        with open(input_file, "r", encoding='UTF-8') as f:
            users_data = json.load(f)
            seen = set()
            for user in users_data:
                if user['user_id'] not in seen:
                    seen.add(user['user_id'])
                    users.append(user)


        print(gr + "[+] Enviandole propaganda a personas de la lista...")
        website_url = "https://www.quisqueyajobs.com/"
        instagram_url = "https://www.instagram.com/quisqueyajobs"
        twitter_url = "https://twitter.com/quisqueyajobs"
        message = f"""🌟**Aprovecha esta escasa oportunidad, y unete al futuro del empleo en RD.** Ese futuro empieza con QuisqueyaJobs.

💡 "Si buscas empleo o personal, QuisqueyaJobs es tu oportunidad." Una oportunidad de conectar, de crecer, de alcanzar esos objetivos que parecían distantes.

 🚀 **Únete a nuestra lista de espera** y obten beneficios para el lanzamiento, más alcance en tus postulaciones, ver a tus rivales en las vacantes, Inteligencia artificial para mejorar tu perfil, ven y aprovecha que la lista de espera esta abierta.

 📲 **También conecta con nosotros** en Instagram y Twitter. Consejos y la comunidad laboral mas mejor de RD.

 🔗 **Lista de espera en {website_url}**. El lugar donde tu próximo gran paso te espera. Instagram: {instagram_url} | Twitter: {twitter_url}
"""

        count = 0
        for user in users:
            count += 1
            if count == 15:
                print(gr + "[+] Esperando 40 segundos para enviar más mensajes")
                asyncio.sleep(40)
                count = 0
            try:
              user_id = user['user_id']
              username = user['username']
              receiver = InputPeerUser(user_id, user['access_hash'])
              print(gr+"[+] Sending Message to:", user['name'])
              await client.send_message(receiver, message.format(user['name']))
              # Sleeps to avoid being rate limited.
              print(gr+"[+] Waiting {} seconds".format(SLEEP_TIME))
              await asyncio.sleep(SLEEP_TIME)
            except PeerFloodError:
                print(
                    re + "[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
                client.disconnect()
                sys.exit()
            except Exception as e:
                if username != "":
                  try :
                    print("Fallo data del grupo, buscando por username...")
                    receiver = await client.get_input_entity(user['username'])
                    await client.send_message(receiver, message.format(user['name']))
                    print("Encontrado por username y mensaje enviado...")
                    print(gr+"[+] Waiting {} seconds".format(SLEEP_TIME))
                    await asyncio.sleep(SLEEP_TIME)
                    continue
                  except Exception as e:
                    print(user_id, 'Buscando por id y fallo por username')
                    try:
                      receiver = await client(GetFullUserRequest(user_id))
                      print(user_id, 'Usuario encontrado Enviemos el que mensaje')
                      await client.send_message(receiver, message.format(user['name']))
                      print("Encontrado por id y mensaje enviado, siguiente...")
                      continue
                    except Exception as e:
                      print(re + "[!] Error:", e)
                      print(re + "[!] Trying to continue...")
                      continue
                print(re + "[!] Error:", e)
                print(re + "[!] Trying to continue...")
                continue
        await client.disconnect()
        print("Done. Message sent to all users.")

asyncio.run(main.send_sms())
sys.exit(ExitCode.SUCCESS)
# {
#     "username": "",
#     "user_id": 806385098,
#     "access_hash": -7025699338209073182,
#     "name": "Tu Empleo RD ",
#     "group": "Tu Empleo RD",
#     "group_id": 1139496450
# },
