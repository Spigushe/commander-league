import os
import collections

import discord
from discord.ext import commands
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
creds = None
if os.path.exists('token.pickle'):
	with open('token.pickle', 'rb') as token:
		creds = pickle.load(token)
if not creds or not creds.valid:
	if creds and creds.expired and creds.refresh_token:
		creds.refresh(Request())
	else:
		flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
		creds = flow.run_local_server(port=0)
	with open('token.pickle', 'wb') as token:
		pickle.dump(creds, token)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()


from dotenv import load_dotenv
load_dotenv()

from . import logging
logger = logging.logger

import discord_argparse
from . import parser
bot.help_command = parser.MyHelpCommand()

from .message_handler import PhraseReponse
from .event_data import *


#: response emoji when multiple options
SELECTION_EMOJIS = collections.OrderedDict(
	[
		("1️⃣", 1),
		("2️⃣", 2),
		("3️⃣", 3),
		("4️⃣", 4),
		("5️⃣", 5),
		("6️⃣", 6),
		("7️⃣", 7),
		("8️⃣", 8),
		("9️⃣", 9),
		("🔟", 10),
	]
)

dicMessage = {
	# General phrases
	'check-error': "❌ You do not have the required Privileges",
	'cmd-disabled': "❌ The command is not active currently",

	# Member voting phrases
	'vote-macrotype': """🤖 **Bip, Boup**
⚠️ I was not able to handle the macrotype you've given me
✉️ Can you react to the right one, please ?
1️⃣ Aggro     2️⃣ Tempo     3️⃣ Control   4️⃣ Combo     5️⃣ Midrange""",
	'vote-error': "❌ The reaction you just used has raised an error. Please reach out to a staff member to get some help",
	'vote-success': "✅ Thank you for your input",

	# Registration phrases
	'registration-complete': "✅ You have been successfully registered !",
	'registration-registered': "❌ You are already registered, please use this command only once",
	'registration-full': "🤖 **Bip, Boup**\nThe event is full, I'll check if I can add you to the waiting list",
	'registration-ok': "📝 **New Registration**\nMaster Table has been updated\nMessage content: ",
	'registration-missing': "❌ There are some required information that you did not give us. Please refer to `!help register` for the full command and details about the arguments",
	'registration-disabled': "❌ Registration are closed for all of our events for now",
	'registration-bad-argument': "❌ The arguments used do not fit with what I've been programmed for. Please reach out to a staff member to get som help",

	# Registration management phrases
	'open-success': "🟢 Registrations for the following event are activated: ",
	'open-pb-argument': "❌ The argument used do not fit main, side or fun event",
	'close-event': "🟢 Registrations for the following event are disabled: ",
}


def getLeague():
	"""Get the Guild object"""
	return bot.get_guild(int(LIGUEID))

def getChannel(id):
	"""Getting the Channel object"""
	for channel in getLeague().channels:
		if channel.id == id:
			return channel

def getMember(ctx):
	"""Get member if message.author is a guild.member"""
	for member in getLeague().members:
		if member.id == ctx.author.id:
			return member

def getTable(range):
	"""GSuite procedure to manage Spreadsheets"""
	return sheet.values().get(spreadsheetId=SHEETID,range=range).execute().get('values')

def getEvent(key: str):
	table = {
		'Main Event': MAINEVENT,
		'Side Event': SIDEEVENT,
		'Fun Event' : FUNEVENT,
	}
	return table[key]


def is_admin(ctx):
	for role in getMember(ctx).roles:
		if role.permissions.administrator:
			return True
	return False



async def memberVote(member, message: str, options: int):
	"""Method to ask more information from user using reactions"""
	message = await sendMessage(member, message)
	try:
		# try loop in case adding reaction is Discord.Forbidden
		for reaction in list(SELECTION_EMOJIS.keys())[: options]:
			await message.add_reaction(reaction)
	except discord.Forbidden:
		logger.warning("Missing reaction permission")

	def check(reaction, user):
		return user == member and str(reaction.emoji) in SELECTION_EMOJIS
	reaction, user = await bot.wait_for('reaction_add', check=check)

	#Recuperation du message envoyé et de la réaction en double associé
	message = await member.fetch_message(message.id)
	for reaction in message.reactions:
		if reaction.count == 2:
			await sendMessage(member, dicMessage['vote-success'])
			return SELECTION_EMOJIS[str(reaction.emoji)]

	# If a reaction is misinterpreted
	await sendMessage(member,dicMessage['vote-error'])


async def sendMessage(ctx,str):
	"""Method to send message"""
	if str == "":
		return
	while len(str) > 2000 :
		prov = str[:2000]
		i=0
		for x in prov :
			i=i+1
			if x == "\n" :
				if "\n" not in prov[i:] :
					await ctx.send(prov[:i])
					str = str[i:]
	else:
		return await ctx.send(str)

async def deleteMessage(message):
	"""Method to delete a message"""
	try:
		await message.delete()
	except:
		return

def setTable(range,values): #Procedure G.sheet pour editer le tableau
	body = {'values': values}
	send = sheet.values().update(
			spreadsheetId=SHEETID,
			range=range,
			valueInputOption='USER_ENTERED',
			body=body
		).execute()

def registrering (event, list, member, nickname, hash, link, macrotype: str = "0"):
	"""Preparing new version of the table"""
	table = getTable(event[list])
	for line in table:
		if line[0] == str(member.id):
			return { 'status': 'error', 'msg': 'registration-registered' }
		if line[0] == "":
			line[0] = str(member.id)
			line[1] = nickname
			line[2] = hash
			line[3] = link
			line[4] = macrotype
			setTable(event[list], table)
			return { 'status': 'success', 'msg': 'registration-complete' }
	return { 'status': 'error', 'msg': 'registration-full' }



@bot.listen()
async def on_ready():
	"""Login success informative log"""
	logger.info("Logged in as {}", bot.user)
	await bot.change_presence(activity=discord.Game(name="Duel Commander"))


@bot.command(
	name="open",
	help="Open registration for said event (either main, side or fun)",
	hidden=True,
)
@commands.check(is_admin)
async def openRegistration(ctx, arg:str):
	logger.info("Received command: {m}".format(m=ctx.message.content))
	events = { 'mai': 'Main Event', 'sid': 'Side Event', 'fun': 'Fun Event' }
	if arg.lower()[:3] in events.keys():
		await deleteMessage(ctx.message)
		await sendMessage(
			getChannel(BOTRETOURGENERAL),
			dicMessage['open-success']+"**"+events[arg.lower()[:3]]+"**"
		)
		registration.update(enabled=True)
		closeRegistration.update(enabled=True)
		return openRegistration.update(enabled=False,aliases=[events[arg.lower()[:3]]])
	raise discord.ext.commands.errors.BadArgument

@openRegistration.error
async def openRegistration_error(ctx, error):
	await deleteMessage(ctx.message)
	if isinstance(error, discord.ext.commands.errors.BadArgument):
		return await sendMessage(getChannel(BOTRETOURGENERAL),dicMessage['open-pb-argument'])
	if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
		return await sendMessage(getChannel(BOTRETOURGENERAL),dicMessage['open-pb-argument'])
	if isinstance(error, discord.ext.commands.DisabledCommand):
		return await sendMessage(ctx.author,dicMessage['cmd-disabled'])
	if isinstance(error, discord.ext.commands.CheckFailure):
		return await sendMessage(ctx.author,dicMessage['check-error'])
	return await sendMessage(
		getChannel(BOTRETOURGENERAL),
		(
			f"❌ Error during command handling for **{ctx.message.author}**\nMessage content:"
			+ f"```{ctx.message.content}```"
		)
	)


@bot.command(
	name="close",
	help="Close registration for said event (either main, side or fun)",
	hidden=True,
	enabled=False,
)
@commands.check(is_admin)
async def closeRegistration(ctx):
	logger.info("Received command: {m}".format(m=ctx.message.content))
	await deleteMessage(ctx.message)
	event = openRegistration.aliases[0]

	openRegistration.update(aliases=[],enabled=True)
	closeRegistration.update(enabled=False)
	registration.update(enabled=False)

	return await sendMessage(
		getChannel(BOTRETOURGENERAL),
		dicMessage['close-event']+"**"+event+"**"
	)

@closeRegistration.error
async def closeRegistration_error(ctx, error):
	await deleteMessage(ctx.message)
	if isinstance(error, discord.ext.commands.DisabledCommand):
		return await sendMessage(ctx.author,dicMessage['cmd-disabled'])
	if isinstance(error, discord.ext.commands.CheckFailure):
		return await sendMessage(ctx.author,dicMessage['check-error'])
	return await sendMessage(
		getChannel(BOTRETOURGENERAL),
		(
			f"❌ Error during command handling for **{ctx.message.author}**\nMessage content:"
			+ f"```{ctx.message.content}```"
		)
	)

@bot.command(
	name="register",
	aliases=["inscription"],
	brief="Register a player to an event",
	help="Register a player into an open-for-registration tournament with a Cockatrice nickname, the deck's hash from Cockatrice and a Moxfield link to the decklist",
	usage="nickname=player_nickname hash=deck_hash link=deck_link",
	enabled=False,
)
async def registration(ctx, *, args: parser.registration=parser.registration.defaults()):
	logger.info("Received command: {m}".format(m=ctx.message.content))
	await deleteMessage(ctx.message)

	event = getEvent(openRegistration.aliases[0])
	member = getMember(ctx)

	"""
	Registering without macrotype
	Checking this information after registration as it is not a RequiredArgument
	"""
	reg = registrering(
		event, 'ListeInscrit',
		member, args["nickname"], args["hash"], args["link"], ""
	)
	await sendMessage(member, dicMessage[reg['msg']])
	# automatically registered if a seat is available

	wl = {'status':'','msg':''}
	if reg['msg'] == 'registration-full':
		wl = registrering(
			event, 'ListedAttente',
			member, args["nickname"], args["hash"], args["link"], ""
		)
		await sendMessage(member, dicMessage[wl['msg']])
	if reg['msg'] == 'registration-complete' or wl['msg'] == 'registration-complete':
		for role in getLeague().roles:
			if role.name == event["NomRole"]:
				await member.add_roles(role)
	if reg['msg'] == 'registration-registered' or wl['msg'] == 'registration-registered':
		return

	"""
	Checking and updating macrotype
	"""
	macrotypes = ["aggro", "tempo", "control", "combo", "midrange", "agro", "controle", "midrang"]
	if args["macrotype"] != "" and args["macrotype"].lower() not in macrotypes:
		macrotype = await memberVote(member, dicMessage['vote-macrotype'], 5)
		args["macrotype"] = macrotypes[macrotype-1]
	if reg['msg'] == 'registration-complete':
		list = 'ListeInscrit'
	elif wl['msg'] == 'registration-complete':
		list = 'ListedAttente'
	table = getTable(event[list])
	for line in table:
		if line[0] == str(member.id):
			line[4] = args["macrotype"]
			setTable(event[list], table)
			break

	"""
	Sending Log messages
	"""
	await sendMessage(
		getChannel(event["bot-channel"]),
		dicMessage['registration-ok']+"`"+ctx.message.content+"`\nUser: **"+args['nickname']+"**"
	)

@registration.error
async def registration_error(ctx, error):
	await deleteMessage(ctx.message)
	if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
		await sendMessage(ctx.author,dicMessage['registration-missing'])
	if isinstance(error, discord.ext.commands.DisabledCommand):
		return await sendMessage(ctx.author,dicMessage['registration-disabled'])
	if isinstance(error, discord.ext.commands.errors.BadArgument):
		await sendMessage(ctx.author,dicMessage['registration-bad-argument'])
	return await sendMessage(
		getChannel(BOTRETOURGENERAL),
		(
			f"❌ Error during registration for **{ctx.message.author}**\nMessage content:"
			+ f"```{ctx.message.content}```"
		)
	)

def main():
	"""Entrypoint for the Discord Bot"""
	logger.setLevel(logging.INFO)
	bot.run(os.getenv("DISCORD_TOKEN"))
	# reset log level so as to not mess up tests
	logger.setLevel(logging.NOTSET)
