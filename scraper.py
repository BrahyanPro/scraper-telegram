from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os, sys
import configparser
import csv
import json
import time

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

def banner():
    print(f"""
{re}╔╦╗{cy}┌─┐┬  ┌─┐{re}╔═╗  ╔═╗{cy}┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐
{re} ║ {cy}├┤ │  ├┤ {re}║ ╦  ╚═╗{cy}│  ├┬┘├─┤├─┘├┤ ├┬┘
{re} ╩ {cy}└─┘┴─┘└─┘{re}╚═╝  ╚═╝{cy}└─┘┴└─┴ ┴┴  └─┘┴└─

            version : 1.0
    BrahyanPro Scraper for quisqueya jobs
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
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue

print(gr+'[+] Choose a group to scrape members :'+re)
i=0
for g in groups:
    print(gr+'['+cy+str(i)+gr+']'+cy+' - '+ g.title)
    i+=1

print('')
g_index = input(gr+"[+] Enter a Number : "+re)
target_group=groups[int(g_index)]

print(gr+'[+] Fetching Members...')
time.sleep(1)
all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)

print(len(all_participants))
print(all_participants)


for participant in all_participants:
    #Convert to int


    user = client.get_input_entity(participant.id)
    print(user)




#print(gr+'[+] Saving In file...')
#time.sleep(1)
#data = []  # Lista para almacenar los datos de los miembros

#for user in all_participants:
#    user_data = {
#        'username': user.username if user.username else "",
#        'user_id': user.id,
#        'access_hash': user.access_hash,
#        'name': (user.first_name if user.first_name else "") + " " + (user.last_name if user.last_name else "").strip(),
#        'group': target_group.title,
#        'group_id': target_group.id
#    }
#    data.append(user_data)
#with open("members.json", "w", encoding='UTF-8') as f:
#    json.dump(data, f, ensure_ascii=False, indent=4)


#with open("members.csv","w",encoding='UTF-8') as f:
#    writer = csv.writer(f,delimiter=",",lineterminator="\n")
#    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
#    for user in all_participants:
#        if user.username:
#            username= user.username
#        else:
#            username= ""
#        if user.first_name:
#            first_name= user.first_name
#        else:
#            first_name= ""
#        if user.last_name:
#            last_name= user.last_name
#        else:
#            last_name= ""
#        name= (first_name + ' ' + last_name).strip()
#        writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])
#print(gr+'[+] Members scraped successfully.')
