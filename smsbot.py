#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
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


class main():

    def banner():

        print(f"""
    {re}╔╦╗{cy}┌─┐┬  ┌─┐{re}╔═╗  ╔═╗{cy}┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐
    {re} ║ {cy}├┤ │  ├┤ {re}║ ╦  ╚═╗{cy}│  ├┬┘├─┤├─┘├┤ ├┬┘
    {re} ╩ {cy}└─┘┴─┘└─┘{re}╚═╝  ╚═╝{cy}└─┘┴└─┴ ┴┴  └─┘┴└─

                version : 1.0
        Brahyan Pro Hacker, estamos enviando mensajes
            """)

    def send_sms():
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

        client.connect()
        if not client.is_user_authorized():
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
                if user['username'] not in seen:
                    seen.add(user['username'])
                    users.append(user)
        print(gr + "[+] Enviandole propaganda a personas de la lista...")

        website_url = "https://www.quisqueyajobs.com/"
        instagram_url = "https://www.instagram.com/quisqueyajobs"
        twitter_url = "https://twitter.com/quisqueyajobs"

        message = f"""🌟**Imagina un futuro donde cada paso en tu carrera o la búsqueda de tu equipo ideal está alineado con tus sueños.** Ese futuro empieza con QuisqueyaJobs. 

💡 "Si buscas empleo o personal, QuisqueyaJobs es tu oportunidad." Una oportunidad de conectar, de crecer, de alcanzar esos objetivos que parecían distantes. 

 🚀 **Únete a nuestra lista de espera** y sé parte de los pioneros que transformarán el panorama laboral de República Dominicana. Aquí, el futuro no es algo que esperas, es algo que creas.

 📲 **Conéctate con nosotros** en Instagram y Twitter. Inspírate con historias de éxito, consejos y una comunidad que ve más allá del horizonte.

 🔗 **Descubre más en {website_url}**. El lugar donde tu próximo gran paso te espera. Instagram: {instagram_url} | Twitter: {twitter_url}

 **QuisqueyaJobs:** No solo es una plataforma; es un movimiento. ¿Listo para moverte con nosotros hacia un futuro lleno de posibilidades?"""
        for user in users:
            print(user)
            if user['username'] != "":
                receiver = client.get_input_entity(user['username'])
            else:
                receiver = InputPeerUser(user['user_id'], user['access_hash'])

            try:
                print(gr + "[+] Sending Message to:", user['name'])
                client.send_message(receiver, message.format(user['name']))
                print(gr + "[+] Waiting {} seconds".format(SLEEP_TIME))
                time.sleep(SLEEP_TIME)
            except PeerFloodError:
                print(
                    re + "[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
                client.disconnect()
                sys.exit()
            except Exception as e:
                print(re + "[!] Error:", e)
                print(re + "[!] Trying to continue...")
                continue
        client.disconnect()
        print("Done. Message sent to all users.")


main.send_sms()

# {
#     "username": "",
#     "user_id": 806385098,
#     "access_hash": -7025699338209073182,
#     "name": "Tu Empleo RD ",
#     "group": "Tu Empleo RD",
#     "group_id": 1139496450
# },
