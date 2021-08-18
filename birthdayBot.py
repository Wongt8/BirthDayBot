import discord,time,json,asyncio
from datetime import datetime,date
from discord.ext import commands
from dateutil import relativedelta

TOKEN = ""
CHANNEL = 


# Load data
try :
    old_data = json.loads(open("birthday.json").read())
except Exception:
    print("No data Yet")
    old_data = []

def checkJson(name, json_data):
    for i in json_data:
        if i["name"] == name:
            return True
    return False

def time_betewn_date(anniv_day,anniv_month,anniv_year):
    now = str(datetime.now())[:9].split("-")
    day_now = date(int(now[0]),int(now[1]),int(now[2]))
    day_anniv = date(int(anniv_year),int(anniv_month),int(anniv_day))
    delta = day_anniv - day_now
    return delta.days - 17 # Va savoir pk il me add 17 jours en plus

def get_age(_date):
    birthday = datetime.strptime(_date, "%d/%m/%Y")
    now = datetime.now()
    dif = relativedelta.relativedelta(birthday, now)
    return abs(dif.years)

def format_json(name,day,month,_date,year):
    format_dic = {"name":name,"age":get_age(_date),"date_of_birth":day+"/"+month,"year_of_birth":year}
    return format_dic

def check_anniv():
    day,month = str(datetime.now())[8:10],str(datetime.now())[5:7]
    annivOf = []
    for i in old_data:
        if i["date_of_birth"] == day+"/"+month:
            annivOf.append((i["name"],i["age"]))
    return (annivOf,len(annivOf) > 0)


client = commands.Bot(command_prefix = "+")

@client.event
async def on_ready():
    print("Connected as : ")
    print(f"{client.user.name}#{client.user.discriminator}")
    print(client.user.id)
    print("-----------------")
    await client.change_presence(activity=discord.Game(name='The cake is a lie'))
    await birthday_loop()


@client.command(aliases=['add'])
async def create(ctx, name, _date):

    if checkJson(name,old_data):
        embed = discord.Embed(title=":no_entry: Le nom est déjà pris !",
        description=f":arrow_forward: Tester avec **{name}0** ou autre ",color=0xdb0000)
        await ctx.send(embed=embed)

    else :

        try:
            date = datetime.strptime(_date, "%d/%m/%Y")
            date = str(_date).split("/")
            
            embed = discord.Embed(title=":white_check_mark: Bravo !", 
            description=f":birthday: Anniversaire crée pour {name} le {date[0]}/{date[1]}",color=0x09ce29)

            old_data.append(format_json(name,date[0],date[1],_date,date[2]))

            with open("birthday.json",'w') as js:
                json.dump(old_data,js,indent=4)

            await ctx.send(embed=embed)
            
        except ValueError :
            embed = discord.Embed(title=":no_entry: Erreur dans la commande !",
            description=":arrow_forward: <nom> <dd/m/y>",color=0xdb0000)
            await ctx.send(embed=embed)

@client.command(aliases=['get'])
async def gets(ctx, name):
    find = False
    for i in old_data:
        if i["name"] == name :
            find = True
            embed=discord.Embed(title=f"Information de {name}")
            embed.set_thumbnail(url="https://image.flaticon.com/icons/png/512/3076/3076404.png")
            an = "ans" if int(i["age"]) > 1 else "an"
            embed.add_field(name="Age", value=f'{i["age"]} {an}', inline=False)
            embed.add_field(name="Date de naissance :date:", value=f"{i['date_of_birth']}/{i['year_of_birth']}", inline=False)
            
            day_month = i['date_of_birth'].split('/')
            year = int(str(datetime.now())[:4])+1 if int(day_month[1]) < int(str(datetime.now())[5:-19]) else int(str(datetime.now())[:4])
            time_left =time_betewn_date(day_month[0],day_month[1],year)
            jour = "jours" if time_left != 1 else "jour"
            if time_left == 0:
                embed.add_field(name="Prochain anniversaire :hourglass:", value="It is today baka :stuck_out_tongue_closed_eyes:", inline=False)
                await ctx.send(embed=embed)
            else :
                embed.add_field(name="Prochain anniversaire :hourglass:", value=f"{time_left} {jour}", inline=False)
                await ctx.send(embed=embed)
            
    if not find:
        embed = discord.Embed(title=":octagonal_sign: Zut ce nom n'est pas enregistrer !",color=0xdb0000)
        await ctx.send(embed=embed)

@client.command(aliases=['delete'])
async def edits(ctx,name):
    global old_data
    new_data = []
    for i in old_data:
        if i["name"] != name :
            new_data.append(i)
            
    if len(new_data) == len(old_data):
        embed = discord.Embed(title=":octagonal_sign: Zut ce nom n'est pas enregistrer !",color=0xdb0000)
        await ctx.send(embed=embed)
    else :
        embed = discord.Embed(title=":white_check_mark: Suppression effectué !",
        description=f":wave: Bye,bye {name}",color=0xdf8911)
        await ctx.send(embed=embed) 
        old_data = new_data
        with open("birthday.json",'w') as js:
            json.dump(new_data,js,indent=4)

@client.command(aliases=['helps'])
async def helpCommand(ctx):
    embed=discord.Embed(title="Help !", description="Comment utiliser les commandes du bot", color=0xca1cc4)
    embed.set_thumbnail(url="https://images4.alphacoders.com/732/732394.png")
    embed.add_field(name="Ajouter un anniversaire :white_check_mark:", value="+add nom dd/m/y", inline=False)
    embed.add_field(name="Voir les informations d'une personne :bookmark_tabs:", value="+get nom", inline=False)
    embed.add_field(name="Supprimer un anniversaire :x:", value="+delete nom", inline=True)
    embed.set_footer(text="Bot by Wongt8")
    await ctx.send(embed=embed)


async def birthday_loop():
    channel = client.get_channel(CHANNEL)
    while True:

        nameAnniv,match = check_anniv()
        for i in nameAnniv:
            an = "ans" if int(i[1])+1 > 1 else "an"
            embed = discord.Embed(title=f":birthday: Joyeux anniversaire a {i[0]} !",
            description=f":partying_face: Et bravo pour tes {i[1]+1} {an}",color=0x28c3c0)
            await channel.send(embed=embed)
        for i in old_data:
            for j in nameAnniv:
                if i["name"] == j[0]:
                    i["age"] = i["age"]+1

        if match:
            with open("birthday.json",'w') as js:
                json.dump(old_data,js,indent=4)

        await asyncio.sleep(86400)

client.run(TOKEN)
