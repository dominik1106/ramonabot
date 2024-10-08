import os, discord, dotenv, requests, json

dotenv.load_dotenv()
token = str(os.getenv("BOT_TOKEN"))
API_KEY = str(os.getenv("API_KEY"))
API_URL = "http://homelab:3000"

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="kontostand")
async def kontostand(ctx: discord.ApplicationContext, user: discord.User):
    user_id = str(user.id)
    url = "{api_url}/pub/account/{id}".format(api_url=API_URL, id=user_id)

    print(str(user.id))
    print(url)

    res = requests.get(url=url)

    if(res.status_code != 200):
        await ctx.respond("Error" + str(res.json()))

    account = json.loads(res.text)

    await ctx.respond("{user}: {balance} Ramonas".format(
        user=user.name,
        balance=account["balance"]
    ))

@bot.slash_command(name="uberweisung")
async def uberweisung(ctx: discord.ApplicationContext, receiver: discord.User, amount: int, note: str):
    url = "{api_url}/prv/transfer".format(api_url=API_URL)

    body = {
        "sender": str(ctx.author.id),
        "receiver": str(receiver.id),
        "amount": amount,
        "note": note
    }

    headers = {
        "X-API-KEY": API_KEY
    }

    res = requests.post(url=url, data=body, headers=headers)
    
    if(res.status_code != 200):
        await ctx.respond("Error" + str(res.json()))

    transaktion = res.json()

    await ctx.respond("Überweisung von {sender} an {receiver}\nMenge: {amount} Ramonas\nNotiz: ({note})\nTransaktions-ID: {id}".format(
        sender=ctx.author.mention,
        receiver=receiver.mention,
        amount=amount,
        note=note,
        id=transaktion["id"]
    ))

@bot.slash_command(name="transaktion")
async def transaktionen(ctx: discord.ApplicationContext, id: int):
    url = "{api_url}/pub/transaction/{id}".format(api_url=API_URL, id=str(id))

    res = requests.get(url=url)

    if(res.status_code != 200):
        await ctx.respond("Error" + str(res.json()))

    transaktion = res.json()

    print(int(transaktion["sender_id"]))
    sender = await bot.fetch_user(int(transaktion["sender_id"]))
    receiver = await bot.fetch_user(int(transaktion["receiver_id"]))
    amount = transaktion["amount"]
    note = transaktion["note"]
    trs_id = transaktion["id"]



    await ctx.respond("Überweisung von {sender} an {receiver}\nMenge: {amount} Ramonas\nNotiz: ({note})\nTransaktions-ID: {id}".format(
        sender=sender.name,
        receiver=receiver.name,
        amount=amount,
        note=note,
        id=trs_id
    ))

# @bot.slash_command(name="transaktionen")
# async def transaktionen(ctx: discord.ApplicationContext, offset: int, limit: int = 10):
#     await ctx.respond("")

# @bot.slash_command(name="mint")
# async def id(ctx: discord.ApplicationContext):
#     await ctx.respond("Minting new ramonas")

bot.run(os.getenv('BOT_TOKEN'))