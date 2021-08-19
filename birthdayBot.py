import discord
import json
import asyncio
from datetime import datetime, date
from discord.ext import commands
from dateutil import relativedelta

TOKEN = "" # Le token du bot
CHANNEL = 0 # L'id du channel ou les annivs seront envoyer


# Load data
try:
    old_data = json.loads(open("birthday.json").read())
except Exception:
    print("No data Yet")
    old_data = {}

def time_between_date(day_a, day_b):
    delta = day_a - day_b
    return delta.days

def get_age(bday):
    now = datetime.now()
    dif = relativedelta.relativedelta(bday, now)
    return abs(dif.years)

def format_json(_date):
    return {
        "age": get_age(_date),
        "birthday": f"{_date.day}/{_date.month}/{_date.year}"
    }

def check_birthday():
    now = date.today()
    bday_of = []
    for p, d in old_data.items():
        day, month, _ = list(map(int, d.get("birthday").split("/")))
        if date(now.year, month, day) == now: bday_of.append(p)
    return bday_of


client = commands.Bot(command_prefix = "+")

@client.event
async def on_ready():
    print("Connected as: ")
    print(f"{client.user.name}#{client.user.discriminator}")
    print(client.user.id)
    print("-----------------")
    await client.change_presence(activity=discord.Game(name='The cake is a lie 🎂'))


@client.command(aliases=['add'])
async def create(ctx, name, _date):

    if name in old_data:
        embed = discord.Embed(
            title=":no_entry: Le nom est déjà pris !",
            description=f":arrow_forward: Testez avec **{name}0** ou autre",
            color=0xdb0000
        )
        await ctx.send(embed=embed)

    else:
        try:
            bday = datetime.strptime(_date, "%d/%m/%Y")
            
            embed = discord.Embed(
                title=":white_check_mark: Bravo !", 
                description=f":birthday: Anniversaire créé pour {name} le {bday.day}/{bday.month}",
                color=0x09ce29
            )

            old_data[name] = format_json(bday)

            with open("birthday.json", 'w') as js:
                json.dump(old_data, js, indent=4)

            await ctx.send(embed=embed)
            
        except ValueError:
            embed = discord.Embed(
                title=":no_entry: Erreur dans la commande !",
                description=":arrow_forward: <nom> <dd/mm/yyyy>",
                color=0xdb0000
            )
            await ctx.send(embed=embed)

@client.command(aliases=['get'])
async def gets(ctx, name):
    target = old_data.get(name)
    if target is not None:
        embed = discord.Embed(title=f"Information de {name}")
        embed.set_thumbnail(url="https://image.flaticon.com/icons/png/512/3076/3076404.png")
        age = target.get("age")
        embed.add_field(name="Age", value=f"{age} an{'s' if age > 1 else ''}", inline=False)
        embed.add_field(name="Date de naissance :date:", value=target.get("birthday"), inline=False)
        
        day, month, _ = list(map(int, target.get('birthday').split('/')))
        now = datetime.now()
        bday = datetime.strptime(f"{day}/{month}/{now.year}", "%d/%m/%Y")
        days_left = time_between_date(bday, now)
        if days_left < 0: days_left = time_between_date(bday + relativedelta.relativedelta(years=1), now)
        if days_left == 0:
            embed.add_field(name="Prochain anniversaire :hourglass:", value="It is today baka :stuck_out_tongue_closed_eyes:", inline=False)
        else:
            embed.add_field(name="Prochain anniversaire :hourglass:", value=f"{days_left} jour{'s' if days_left > 0 else ''}", inline=False)
        await ctx.send(embed=embed)
            
    else:
        embed = discord.Embed(title=":octagonal_sign: Zut ce nom n'est pas enregistré !", color=0xdb0000)
        await ctx.send(embed=embed)

@client.command(aliases=['del', 'remove'])
async def delete(ctx, name):
    global old_data
            
    if name not in old_data:
        embed = discord.Embed(title=":octagonal_sign: Zut ce nom n'est pas enregistré !", color=0xdb0000)
        await ctx.send(embed=embed)
    else:
        del old_data[name]
        embed = discord.Embed(
            title=":white_check_mark: Suppression effectué !",
            description=f":wave: Bye, bye {name}",
            color=0xdf8911
        )
        await ctx.send(embed=embed) 
        
        with open("birthday.json",'w') as js:
            json.dump(old_data, js, indent=4)

@client.command(aliases=['helps'])
async def helpCommand(ctx):
    embed = discord.Embed(title="Help !", description="Comment utiliser les commandes du bot", color=0xca1cc4)
    embed.set_thumbnail(url="https://images4.alphacoders.com/732/732394.png")
    embed.add_field(name="Ajouter un anniversaire :white_check_mark:", value="+add nom dd/mm/yyyy", inline=False)
    embed.add_field(name="Voir les informations d'une personne :bookmark_tabs:", value="+get nom", inline=False)
    embed.add_field(name="Supprimer un anniversaire :x:", value="+del nom ou +remove nom", inline=True)
    embed.set_footer(text="Bot by Wongt8")
    await ctx.send(embed=embed)


async def birthday_loop():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL)
    
    while True:
        new_bday = check_birthday()
        print(new_bday)
        for name in new_bday:
            age = old_data.get(name).get('age') + 1
            embed = discord.Embed(
                title=f":birthday: Joyeux anniversaire à {name} !",
                description=f":partying_face: Et bravo pour tes {age} an{'s' if age > 1 else ''}",
                color=0x28c3c0)
            await channel.send(embed=embed)
            old_data[name]["age"] += 1

        if len(new_bday) > 0:
            with open("birthday.json",'w') as js:
                json.dump(old_data, js, indent=4)

        await asyncio.sleep(86400)


client.loop.create_task(birthday_loop())
client.run(TOKEN)