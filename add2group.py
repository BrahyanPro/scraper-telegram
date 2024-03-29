#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import configparser
import os, sys
import csv
import traceback
import time
import random
import json

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

def banner():
    print(f"""
{re}╔╦╗{cy}┌─┐┬  ┌─┐{re}╔═╗  ╔═╗{cy}┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐
{re} ║ {cy}├┤ │  ├┤ {re}║ ╦  ╚═╗{cy}│  ├┬┘├─┤├─┘├┤ ├┬┘
{re} ╩ {cy}└─┘┴─┘└─┘{re}╚═╝  ╚═╝{cy}└─┘┴└─┴ ┴┴  └─┘┴└─
BrahyanKing
            version : 1.0
        """)

cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    banner()
    print(re+"[!] run python3 setup.py first !!\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('clear')
    banner()
    client.sign_in(phone, input(gr+'[+] Enter the code: '+re))

os.system('clear')
banner()
input_file = "members.json"
users = []
with open(input_file, "r", encoding='UTF-8') as f:
    users_data = json.load(f)
    seen = set()
    for user in users_data:
        if user['username'] not in seen:
            seen.add(user['username'])
            users.append(user)

chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    print(chat)
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue

i=0
for group in groups:
    print(gr+'['+cy+str(i)+gr+']'+cy+' - '+group.title)
    i+=1

print(gr+'[+] Choose a group to add members')
g_index = input(gr+"[+] Enter a Number : "+re)
target_group=groups[int(g_index)]

print(gr+"[+] Fetching Members...")
target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)

n = 0

print(gr+"[+] Adding Members to Group BrahyanPro was here...")

for user in users:
    n += 1
    if n % 50 == 0:
      time.sleep(20)
    try:
        print ("Adding {}".format(user['user_id']))
        user_to_add = InputPeerUser(user['user_id'], user['access_hash'])
        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        print(gr+"[+] Espera entre 5-10 segundos...")
        time.sleep(random.randrange(5, 10))
    except PeerFloodError:
        print(re+"[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
    except UserPrivacyRestrictedError:
        print(re+"[!] The user's privacy settings do not allow you to do this. Skipping.")
    except:
        traceback.print_exc()
        print(re+"[!] Unexpected Error")
        continue


#[cred]
#id = 20661591
#hash = 001c28398baa6c5ed27ca22e09a13451
#phone = 18092795529
