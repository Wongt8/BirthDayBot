import discord,time,json,asyncio
from datetime import datetime,date
from discord.ext import commands
from dateutil import relativedelta

TOKEN = ""


# Load data
try :
    old_data = json.loads(open("birthday.json").read())
except Exception:
    print("No data Yet")
    old_data = []


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

client = commands.Bot(command_prefix = "+")

@client.event
async def on_ready():
    print("Connected as : ")
    print(f"{client.user.name}#{client.user.discriminator}")
    print(client.user.id)
    print("-----------------")
    await client.change_presence(activity=discord.Game(name='The cake is a lie'))


@client.command(aliases=['add'])
async def create(ctx, name, _date):
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
            embed.add_field(name="Age", value=f'{i["age"]} ans', inline=False)
            embed.add_field(name="Date de naissance :date:", value=f"{i['date_of_birth']}/{i['year_of_birth']}", inline=False)
            
            day_month = i['date_of_birth'].split('/')
            year = int(str(datetime.now())[:4])+1 if int(day_month[1]) < int(str(datetime.now())[5:-19]) else int(str(datetime.now())[:4])
            time_left =time_betewn_date(day_month[0],day_month[1],year)
            jour = "jours" if time_left != 1 else "jour"

            embed.add_field(name="Prochain anniversaire :hourglass:", value=f"{time_left} {jour}", inline=False)
            await ctx.send(embed=embed)
            
    if not find:
        embed = discord.Embed(title=":octagonal_sign: Zut ce nom n'est pas enregistrer !",color=0xdb0000)
        await ctx.send(embed=embed)

"""
current_year = int(datetime.now())[:4]
current_date = str(datetime.now())[5:-16] # format of the date "month-day"
"""

client.run(TOKEN)
