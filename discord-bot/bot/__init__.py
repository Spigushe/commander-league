import os

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

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
LIGUEID = 817430786629173258
SHEETID = "1lJTFm6xMdUYA22tadIdAMZO5pYOH3Sc1OEVZsfeB_h4"
STAT = "Split_2!A4:S53"
BOTSPAM = 833778930858852413
BotRetourGeneral = 834892751363375155
MAINEVENT1 = {
	"ListeMatch": "S3_ME!V4:Z170",
	"ListeScore": "S3_ME!W4:X170",
	"ListeInscrit": "S3_ME!P4:U51",
	"ListedAttente": "S3_ME!P52:U170",
	"CanalBot": 833664664012718090,
	"Categorie": 823186086960037899,
	"NomRole": "MainEvent"
}
SIDEEVENT1 = {
	"ListeMatch": "S3_SE!V4:Z110",
	"ListeScore": "S3_SE!W4:X110",
	"ListeInscrit": "S3_SE!P4:U27",
	"ListedAttente": "S3_SE!P28:U110",
	"CanalBot": 823191678826971196,
	"Categorie": 823186192836722718,
	"NomRole": "SideEvent"
}
FUNEVENT1 = {
	"ListeMatch": "S3_FE!V4:Z66",
	"ListeScore": "S3_FE!W4:X66",
	"ListeInscrit": "S3_FE!P4:U23",
	"ListedAttente": "S3_FE!P24:U66",
	"CanalBot": 823191704827723826,
	"Categorie": 823186631385153576,
	"NomRole": "FunEvent"
}
MAINEVENT2 = {
	"ListeMatch": "S4_ME!V4:Z170",
	"ListeScore": "S4_ME!W4:X170",
	"ListeInscrit": "S4_ME!P4:U51",
	"ListedAttente": "S4_ME!P52:U170",
	"CanalBot": 833664664012718090,
	"Categorie": 823186086960037899,
	"NomRole": "MainEvent"
}
SIDEEVENT2 = {
	"ListeMatch": "S4_SE!V4:Z110",
	"ListeScore": "S4_SE!W4:X110",
	"ListeInscrit": "S4_SE!P4:U27",
	"ListedAttente": "S4_SE!P28:U110",
	"CanalBot": 823191678826971196,
	"Categorie": 823186192836722718,
	"NomRole": "SideEvent"
}
FUNEVENT2 = {
	"ListeMatch": "S4_FE!V4:Z66",
	"ListeScore": "S4_FE!W4:X66",
	"ListeInscrit": "S4_FE!P4:U23",
	"ListedAttente": "S4_FE!P24:U66",
	"CanalBot": 823191704827723826,
	"Categorie": 823186631385153576,
	"NomRole": "FunEvent"
}
MAINEVENT = MAINEVENT1
SIDEEVENT = SIDEEVENT1
FUNEVENT = FUNEVENT1

@bot.listen()
async def on_ready():
	"""Login success informative log"""
	logger.info("Logged in as {}", bot.user)




def to_lower(str):
	return str.lower()

def getTableau(Portee): #Procedure G.sheet pour recuperer le tableau
	return sheet.values().get(spreadsheetId=SHEETID,range=Portee).execute().get('values')

def setTableau(Portee,Valeurs): #Procedure G.sheet pour editer le tableau
	body = {'values': Valeurs}
	send = sheet.values().update(spreadsheetId=SHEETID,range=Portee,valueInputOption='USER_ENTERED',body=body).execute()

async def EffacerMessage(message): #Efface le message d'appel de la commande, si possible
	try:
		await message.delete()
	except:
		return

def getLigue(): #Procedure pour discord afin de recuperer le serveur Ligue.
	return bot.get_guild(int(LIGUEID))

def getAuthor(ctx): #Recherche l'auteur de la commande dans les membres du serveur (utile si commande en MP)
	Ligue = getLigue()
	for member in Ligue.members:
		if member.id == ctx.author.id: return member

def CheckRole(Membre,NomRole): #Renvoir True si le Membre possede le Role
	for role in Membre.roles:
		if role.name == NomRole: return True
	return False

async def CheckEvent(ctx): #Renvoie l'evenement qui correspond au contexte d'appel.
	#Recupère la catégorie d'ou vient le message si il y en a
	Ligue = getLigue()
	CategorieCtx = 0
	for categorie in Ligue.categories:
		for channel in categorie.channels:
			if ctx.channel == channel: CategorieCtx = categorie.id
	#Check si la commande vient d'un channel de tournoi
	if CategorieCtx == MAINEVENT["Categorie"]: return MAINEVENT
	if CategorieCtx == SIDEEVENT["Categorie"]: return SIDEEVENT
	if CategorieCtx == FUNEVENT["Categorie"]: return FUNEVENT
	#Check si l'auteur de la commande n'a qu'un tournoi en cours
	Joueur = getAuthor(ctx)
	RoleMain = CheckRole(Joueur,MAINEVENT["NomRole"])
	RoleSide = CheckRole(Joueur,SIDEEVENT["NomRole"])
	RoleFun = CheckRole(Joueur,FUNEVENT["NomRole"])
	if RoleMain and not (RoleSide or RoleFun): return MAINEVENT
	if RoleSide and not (RoleMain or RoleFun): return SIDEEVENT
	if RoleFun and not (RoleMain or RoleSide): return FUNEVENT
	#Envoie de Mp + Procedure de vote pour l'event
	Vote = await DMVote(Joueur, PhraseReponse("Quel Event ?"), 3)
	if Vote == "1_" : return MAINEVENT
	if Vote == "2_" : return SIDEEVENT
	if Vote == "3_" : return FUNEVENT

async def sendMessage(ctx,str): #Pour envoyer un message de -2000car
	if str == "" : return #Discord n'aime pas envoyer des messages vide
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

def AfficherMatch(tableau,table):
	return f"{tableau[table-1][0]} {tableau[table-1][1]}-{tableau[table-1][2]} {tableau[table-1][3]}"

def AfficherPoule(Event,tableau,Poule):
	i=0
	Message = ""
	if Event == MAINEVENT :
		for x in ["A","B","C","D","E","F","G","H"]:
			if x == Poule:
				for x in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]:
					Message = Message + AfficherMatch(tableau,i+x) + "\n"
				return Message
			i=i+15
	if Event == SIDEEVENT :
		for x in ["A","B","C","D"]:
			if x == Poule:
				for x in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]:
					Message = Message + AfficherMatch(tableau,i+x) + "\n"
				return Message
			i=i+15
	if Event == FUNEVENT :
		for x in ["A","B","C","D"]:
			if x == Poule:
				for x in [1,2,3,4,5,6,7,8,9,10]:
					Message = Message + AfficherMatch(tableau,i+x) + "\n"
				return Message
			i=i+10
	raise IndexError











def is_admin(ctx):
	for role in getAuthor(ctx).roles:
		if role.permissions.administrator: return True
	return False

@bot.command(
	name="Ouverture",
	help="Ouvre les inscriptions pour le tournoi mis en argument (main, side ou fun)",
	hidden=True,
)
@commands.check(is_admin)
async def Ouverture (ctx,arg:str):
	await EffacerMessage(ctx.message)
	await sendMessage(getChannel(BotRetourGeneral),"🔔\n"+PhraseReponse(("Bot",ctx)))
	Inscription.update(name="Inscription",help="Inscrit l'auteur de la commande dans le tournoi en cours, il faut pour cela préciser son Nom sur Cockatrice, son Hash : la suite de caractère qui définit le deck sur le logiciel, un lien url vers la liste et enfin un macrotype(non necessaire), si vous ne connaissez pas le macrotype du deck, allez sur Barrin's Codex",brief="Inscrit l'auteur au tournoi en cours",usage="!Inscription NomCocka hash Lien (Macro)",aliases=["Register"],enabled=True)
	Fermeture.update(name="Fermeture",help="Ferme les inscriptions pour le tournoi dont les inscriptions sont actuellement ouvertes",hidden=True,enabled=True)

	if arg.lower() == "mainevent" or arg.lower() == "main" or arg.lower() == "main event" :
		await sendMessage(getChannel(BotRetourGeneral),PhraseReponse(("Ouverture/Fermeture","Inscriptions ouvertes","Main Event")))
		return Ouverture.update(name="Ouverture",help="Ouvre les inscriptions pour le tournoi mis en argument (main, side ou fun)",hidden=True,enabled=False,aliases = ["Main Event"])
	if arg.lower() == "sideevent" or arg.lower() == "side" or arg.lower() == "side event" :
		await sendMessage(getChannel(BotRetourGeneral),PhraseReponse(("Ouverture/Fermeture","Inscriptions ouvertes","Side Event")))
		return Ouverture.update(name="Ouverture",help="Ouvre les inscriptions pour le tournoi mis en argument (main, side ou fun)",hidden=True,enabled=False,aliases = ["Side Event"])
	if arg.lower() == "funevent" or arg.lower() == "fun" or arg.lower() == "fun event" :
		await sendMessage(getChannel(BotRetourGeneral),PhraseReponse(("Ouverture/Fermeture","Inscriptions ouvertes","Fun Event")))
		return Ouverture.update(name="Ouverture",help="Ouvre les inscriptions pour le tournoi mis en argument (main, side ou fun)",hidden=True,enabled=False,aliases = ["Fun Event"])
	raise discord.ext.commands.errors.BadArgument

@Ouverture.error
async def Ouverture_error(ctx, error):
	if isinstance(error, discord.ext.commands.errors.BadArgument):
		Inscription.update(name="Inscription",help="Inscrit l'auteur de la commande dans le tournoi en cours, il faut pour cela préciser son Nom sur Cockatrice, son Hash : la suite de caractère qui définit le deck sur le logiciel, un lien url vers la liste et enfin un macrotype(non necessaire), si vous ne connaissez pas le macrotype du deck, allez sur Barrin's Codex",brief="Inscrit l'auteur au tournoi en cours",usage="!Inscription NomCocka hash Lien (Macro)",aliases=["Register"],enabled=False)
		Ouverture.update(name="Ouverture",help="Ouvre les inscriptions pour le tournoi mis en argument (main, side ou fun)",hidden=True,enabled=True)
		Fermeture.update(name="Fermeture",help="Ferme les inscriptions pour le tournoi dont les inscriptions sont actuellement ouvertes",hidden=True,enabled=False)
		return await sendMessage(getChannel(BotRetourGeneral),PhraseReponse(("Ouverture/Fermeture","Argument Invalide")))
	if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
		await EffacerMessage(ctx.message)
		return await sendMessage(getChannel(BotRetourGeneral),PhraseReponse(("Ouverture/Fermeture","Argument Manquant")))
	if isinstance(error, discord.ext.commands.DisabledCommand):
		await EffacerMessage(ctx.message)
		return await sendMessage(ctx.author,PhraseReponse(("Ouverture/Fermeture","Commande inactive")))
	if isinstance(error, discord.ext.commands.CheckFailure):
		await EffacerMessage(ctx.message)
		return await sendMessage(ctx.author,PhraseReponse("Erreur Check"))
	await sendMessage(ctx.author,PhraseReponse(("PLS",ctx)))
	await sendMessage(getChannel(BotRetourGeneral),PhraseReponse(("PLSBOT",ctx)))

@bot.command(
	name="Fermeture",
	help="Ferme les inscriptions pour le tournoi dont les inscriptions sont actuellement ouvertes",
	hidden=True,
	enabled=False
)
@commands.check(is_admin)
async def Fermeture (ctx):
	await EffacerMessage(ctx.message)
	await sendMessage(getChannel(BotRetourGeneral),"🔔\n"+PhraseReponse(("Bot",ctx)))
	Inscription.update(name="Inscription",help="Inscrit l'auteur de la commande dans le tournoi en cours, il faut pour cela préciser son Nom sur Cockatrice, son Hash : la suite de caractère qui définit le deck sur le logiciel, un lien url vers la liste et enfin un macrotype(non necessaire), si vous ne connaissez pas le macrotype du deck, allez sur Barrin's Codex",brief="Inscrit l'auteur au tournoi en cours",usage="!Inscription NomCocka hash Lien (Macro)",aliases=["Register"],enabled=False)
	Fermeture.update(name="Fermeture",help="Ferme les inscriptions pour le tournoi dont les inscriptions sont actuellement ouvertes",hidden=True,enabled=False)

	if Ouverture.aliases[0] == "Main Event" :
		await sendMessage(getChannel(BotRetourGeneral),PhraseReponse(("Ouverture/Fermeture","Inscriptions fermees","Main Event")))
		return Ouverture.update(name="Ouverture",help="Ouvre les inscriptions pour le tournoi mis en argument (main, side ou fun)",hidden=True,enabled=True)
	if Ouverture.aliases[0] == "Side Event" :
		await sendMessage(getChannel(BotRetourGeneral),PhraseReponse(("Ouverture/Fermeture","Inscriptions fermees","Side Event")))
		return Ouverture.update(name="Ouverture",help="Ouvre les inscriptions pour le tournoi mis en argument (main, side ou fun)",hidden=True,enabled=True)
	if Ouverture.aliases[0] == "Fun Event" :
		await sendMessage(getChannel(BotRetourGeneral),PhraseReponse(("Ouverture/Fermeture","Inscriptions fermees","Fun Event")))
		return Ouverture.update(name="Ouverture",help="Ouvre les inscriptions pour le tournoi mis en argument (main, side ou fun)",hidden=True,enabled=True)

@Fermeture.error
async def Fermeture_error(ctx, error):
	await EffacerMessage(ctx.message)
	if isinstance(error, discord.ext.commands.DisabledCommand):
		return await sendMessage(ctx.author,PhraseReponse(("Ouverture/Fermeture","Commande inactive")))
	if isinstance(error, discord.ext.commands.CheckFailure):
		return await sendMessage(ctx.author,PhraseReponse("Erreur Check"))
	await sendMessage(ctx.author,PhraseReponse(("PLS",ctx)))
	await sendMessage(getChannel(BotRetourGeneral),PhraseReponse(("PLSBOT",ctx)))









def Inscriptiondanstableau (tableau,Joueur,NomCocka,Hash,Lien,Macro): #Procedure d'inscription du joueur dans le tableau
	Retour = {
		"Reussite": "❌",
		"ReponseBot": "",
		"Tableau": tableau
	}
	for ligne in tableau:
		#Check si déjà inscrit
		if ligne[0] == str(Joueur.id):
			Retour["Reussite"]="❌❌"
			Retour["ReponseBot"] = Retour["ReponseBot"] + PhraseReponse(("Inscription","Deja inscrit"))
			return Retour
		if ligne[0] == "":
			Retour["Reussite"] = "✅"
			Retour["ReponseBot"] = Retour["ReponseBot"] + PhraseReponse(("Inscription","Validé"))
			ligne[0] = str(Joueur.id)
			ligne[1] = NomCocka
			ligne[2] = Hash
			ligne[3] = Lien
			ligne[4] = Macro
			return Retour
	return Retour

def getChannel(ID): #Procedure pour discord (sert essentiellement au message du bot)
	Ligue = getLigue()
	for channel in Ligue.channels:
		if channel.id == ID: return channel

async def DMVote(Membre, str, VoteMax):
	Ligue = getLigue()
	msg = await sendMessage(Membre, str)
	i = 1
	#Rajoute les emojis pour chaque vote afin que l'utilisateur n'ai plus qu'à appuyer dessus
	for x in ["1_","2_","3_","4_","5_"]:
		if i < VoteMax+1:
			for emoji in Ligue.emojis:
				if emoji.name == x: await msg.add_reaction(emoji)
		i=i+1
	#Passage mysterieux ou l'on attend la réaction du 'Membre' sur le msg envoyé plus haut
	def check(reaction, user):
		return user == Membre and reaction.message.id == msg.id
	reaction, user = await bot.wait_for('reaction_add', check=check)
	#Recuperation du message envoyé et de la réaction en double associé
	msg = await Membre.fetch_message(msg.id)
	for react in msg.reactions:
		if react.count == 2: return react.emoji.name
	#Envoie d'un MP si vote incompris
	await sendMessage(Membre,PhraseReponse("Erreur Vote"))

@bot.command(
	name="register",
	#aliases=["inscription"],
	brief="Register a player to an event",
	help="Register a player into an open-for-registration tournament with a Cockatrice nickname, the deck's hash from Cockatrice and a Moxfield link to the decklist",
	usage="player_nickname deck_hash deck_link",
	#enabled=False
)
async def inscription(ctx, *, args: parser.registration=parser.registration.defaults()):
	await EffacerMessage(ctx.message)

	if Ouverture.aliases[0] == "Main Event" : Event = MAINEVENT
	if Ouverture.aliases[0] == "Side Event" : Event = SIDEEVENT
	if Ouverture.aliases[0] == "Fun Event" : Event = FUNEVENT

	await sendMessage(getChannel(Event["CanalBot"]),"📝\n"+PhraseReponse(("Bot",ctx)))

	if len(args) > 1: raise discord.ext.commands.errors.MissingRequiredArgument

	#On rentre le macro si il est correct, sinon macro vide
	Macro = ""
	if len(args) == 1:
		for macro in {"agro", "aggro", "tempo", "control", "controle", "combo", "midrange", "midrang"}:
			if macro == str(args[0]).lower(): Macro = macro

	#On tente d'inscrire dans le tableau d'inscription
	Auteur = getAuthor(ctx)
	tableauInscrit = getTableau(Event["ListeInscrit"])
	retour = Inscriptiondanstableau(tableauInscrit,Auteur,NomCocka,Hash,Lien,Macro)
	setTableau(Event["ListeInscrit"],retour["Tableau"])
	#Si tableau plein, on retente avec la WaitingList
	if retour["Reussite"] == "❌":
		tableauWL = getTableau(Event["ListedAttente"])
		retour = Inscriptiondanstableau(tableauWL,Auteur,NomCocka,Hash,Lien,Macro)
		retour["ReponseBot"] = retour["ReponseBot"] + PhraseReponse(("Inscription","Tournoi Plein"))
		setTableau(Event["ListedAttente"],retour["Tableau"])

	await sendMessage(ctx.author,retour["ReponseBot"])
	await sendMessage(getChannel(Event["CanalBot"]),PhraseReponse(("MPBot",Auteur.name,retour["ReponseBot"])))

	#On s'arrete la si l'inscription a échoué
	if retour["Reussite"] == "❌❌": return

	#On envoie donne le role
	Ligue = getLigue()
	for role in Ligue.roles:
		if role.name == Event["NomRole"]: await Auteur.add_roles(role)

	#On envoie un message de Vote par MP pour le Macrotype si c'était vide ou incorrect
	if Macro == "":
		Macro = await DMVote(Auteur,PhraseReponse(("Inscription","Quel Macro ?")), 5)
		if Macro == "1_" : Macro = "aggro"
		if Macro == "2_" : Macro = "combo"
		if Macro == "3_" : Macro = "control"
		if Macro == "4_" : Macro = "midrange"
		if Macro == "5_" : Macro = "tempo"

		#On met a jour le Macrotype dans le google sheet
		tableauInscrit = getTableau(Event["ListeInscrit"]) #Sécurité au cas ou il y a trop de modification entre le moment de l'inscription et le moment du vote
		for ligne in tableauInscrit:
			if ligne[0] == str(Auteur.id):
				ligne[4] = Macro
				setTableau(Event["ListeInscrit"],tableauInscrit)
				break
		tableauWL = getTableau(Event["ListedAttente"])
		for ligne in tableauWL:
			if ligne[0] == str(Auteur.id):
				ligne[4] = Macro
				setTableau(Event["ListedAttente"],tableauWL)
				break

		#On envoie un petit message dans le CanalBot avec la confirmation du vote
		await sendMessage(ctx.author,PhraseReponse(("Inscription","Ajout macro")) + Macro)
		await sendMessage(getChannel(Event["CanalBot"]),"🗳️ **"+Auteur.name +f"** a fini par voté son macrotype _{Macro}_")

@inscription.error
async def Inscription_error(ctx, error):
	await EffacerMessage(ctx.message)
	if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
		await sendMessage(getChannel(BotRetourGeneral),"📝❌\n"+PhraseReponse(("Bot",ctx)))
		return await sendMessage(ctx.author,PhraseReponse(("Inscription","Argument Manquant")))
	if isinstance(error, discord.ext.commands.DisabledCommand):
		return await sendMessage(ctx.author,PhraseReponse(("Inscription","Commande inactive")))
	if isinstance(error, discord.ext.commands.errors.BadArgument):
		await sendMessage(getChannel(BotRetourGeneral),"📝❌\n"+PhraseReponse(("Bot",ctx)))
		return await sendMessage(ctx.author,PhraseReponse(("Inscription","Argument Invalide")))
	await sendMessage(ctx.author,PhraseReponse(("PLS",ctx)))
	await sendMessage(getChannel(BotRetourGeneral),PhraseReponse(("PLSBOT",ctx)))










def getJoueurInscrit(tableauInscrit,NomJoueur): #Renvoi le membre de la ligue avec le nom inscrit dans le tableau
	Ligue = getLigue()
	for ligne in tableauInscrit:
		if ligne[1].lower() == NomJoueur:
			for member in Ligue.members:
				if str(member.id) == ligne[0]: return member

def NumeroMatch(Event,Tableau,J1,J2): #Recupere le numero de la table ou le match a lieu
	if Event == MAINEVENT: i = 166
	if Event == SIDEEVENT: i = 82
	if Event == FUNEVENT: i = 62
	while i != -1 :
		if (Tableau[i][0].lower() == J1 and Tableau[i][3].lower() == J2): return i+1
		i = i-1
	return -1

def getMatchEliminatoire(Event,tableau,NomJoueur):
	i=0
	if Event == MAINEVENT:
		for ligne in tableau:
			#Check il y a un match dans la Zone des futures match éliminatoire, avec le joueur concerné et dont le score serait 0-0
			if (i> 135) and (ligne[0].lower() == NomJoueur or ligne[3].lower() == NomJoueur) and (max(int(ligne[1]),int(ligne[2])) == 0):
				return [ligne[0],ligne[3]]
			i=i+1
	if Event == SIDEEVENT:
		for ligne in tableau:
			if i> 67 and (ligne[0].lower() == NomJoueur or ligne[3].lower() == NomJoueur) and (max(int(ligne[1]),int(ligne[2])) == 0):
				return [ligne[0],ligne[3]]
			i=i+1
	if Event == FUNEVENT:
		for ligne in tableau:
			if i> 47 and (ligne[0].lower() == NomJoueur or ligne[3].lower() == NomJoueur) and (max(int(ligne[1]),int(ligne[2])) == 0):
				return [ligne[0],ligne[3]]
			i=i+1
	return ["",""]

async def EnvoyerNextMatch(Event,tableauInscrit,tableau,J1,Membre1,msg):
	match = getMatchEliminatoire(Event,tableau,J1)
	if match == ["",""]:
		Ligue = getLigue()
		for role in Ligue.roles:
			if role.name == Event["NomRole"]:
				await Membre1.remove_roles(role,reason="Joueur éliminé")
		await sendMessage(Membre1,msg + "\n" + PhraseReponse(("Resultat","Eliminé")))
		return await sendMessage(getChannel(Event["CanalBot"]),PhraseReponse(("MPBot",Membre1.name,msg+ "\n" + PhraseReponse(("Resultat","Eliminé")))))
	if match[0] == "" or match[1] == "" or (match[0][:13] == "(Looser table"):
		await sendMessage(Membre1,msg+"\n" + PhraseReponse(("Resultat","Attente")))
		return await sendMessage(getChannel(Event["CanalBot"]),PhraseReponse(("MPBot",Membre1.name,msg+"\n" + PhraseReponse(("Resultat","Attente")))))
	if match[0].lower() == J1:
		await sendMessage(Membre1,msg + "\n" + PhraseReponse(("Resultat","Next Match vs : ",match[1])))
		await sendMessage(getJoueurInscrit(tableauInscrit,match[1].lower()),PhraseReponse(("Resultat","Next Match vs : ",match[0])))
		return await sendMessage(getChannel(Event["CanalBot"]),PhraseReponse(("MPBot",Membre1.name,msg + "\n" + PhraseReponse(("Resultat","Next Match vs : ",match[1]))))+PhraseReponse(("MPBot",getJoueurInscrit(tableauInscrit,match[1].lower()).name,PhraseReponse(("Resultat","Next Match vs : ",match[0])))))
	if match[1].lower() == J1:
		await sendMessage(Membre1,msg + "\n" + PhraseReponse(("Resultat","Next Match vs : ",match[0])))
		await sendMessage(getJoueurInscrit(tableauInscrit,match[0].lower()),PhraseReponse(("Resultat","Next Match vs : ",match[1])))
		return await sendMessage(getChannel(Event["CanalBot"]),PhraseReponse(("MPBot",Membre1.name,msg + "\n" + PhraseReponse(("Resultat","Next Match vs : ",match[0]))))+PhraseReponse(("MPBot",getJoueurInscrit(tableauInscrit,match[0].lower()).name,PhraseReponse(("Resultat","Next Match vs : ",match[1])))))

@bot.command(
	name="Resultat",
	help="Rentre le score d'un match pour le tournoi, ce score sera actualisé sur le google doc, il faut le nom des deux joueurs et le score du match",
	brief="Rentre le score d'un match dans le tableau de la ligue",
	usage="!Résultat Joueur1 1-2 Joueur2",
	aliases=["Resultats","Résultat","Résultats","Result","Results"]
)
async def Resultat (ctx,J1: to_lower, Score:str, J2:to_lower):
	await EffacerMessage(ctx.message)
	Event = await CheckEvent(ctx)
	await sendMessage(getChannel(Event["CanalBot"]),"🎮 **Nouveau résultat**\n"+PhraseReponse(("Bot",ctx)))

	#On check si les deux joueurs annoncé existent au sein de la Ligue et si l'auteur de la commande est bien l'un des deux joueurs !
	Auteur = getAuthor(ctx)
	tableauInscrit = getTableau(Event["ListeInscrit"])
	Membre1 = getJoueurInscrit(tableauInscrit,J1)
	Membre2 = getJoueurInscrit(tableauInscrit,J2)
	if Membre1 == None:
		await sendMessage(Auteur,PhraseReponse(("Resultat","Joueur introuvable",J1)))
		return await sendMessage(getChannel(Event["CanalBot"]),PhraseReponse(("MPBot",Auteur,PhraseReponse(("Resultat","Joueur introuvable",J1)))))
	if Membre2 == None:
		await sendMessage(Auteur,PhraseReponse(("Resultat","Joueur introuvable",J2)))
		return await sendMessage(getChannel(Event["CanalBot"]),PhraseReponse(("MPBot",Auteur,PhraseReponse(("Resultat","Joueur introuvable",J)))))
	if (Auteur.id != Membre1.id and Auteur.id != Membre2.id) and not is_admin(ctx):
		await sendMessage(Auteur,PhraseReponse(("Resultat","Auteur invalide")))
		return await sendMessage(getChannel(Event["CanalBot"]),PhraseReponse(("MPBot",Auteur,PhraseReponse(("Resultat","Auteur invalide")))))

	#Si le Score est Impossible
	S1 = int(Score[0]);S2 = int(Score[2])
	if (S1+S2 > 3) or (S1 == S2) or (S1+S2<2) or (S1*S2<0):
		await sendMessage(Auteur,PhraseReponse(("Resultat","Score Impossible")))
		return await sendMessage(getChannel(Event["CanalBot"]),PhraseReponse(("MPBot",Auteur,PhraseReponse(("Resultat","Score Impossible")))))
	tableau = getTableau(Event["ListeMatch"])
	Ntable = max(NumeroMatch(Event,tableau,J1,J2),NumeroMatch(Event,tableau,J2,J1))
	#Si le match n'existe pas
	if Ntable == -1:
		await sendMessage(Auteur,PhraseReponse(("Resultat","Match Introuvable")))
		return await sendMessage(getChannel(Event["CanalBot"]),PhraseReponse(("MPBot",Auteur,PhraseReponse(("Resultat","Match Introuvable")))))

	#On retourne le score si il est a l'envers
	if Ntable == NumeroMatch(Event,tableau,J2,J1):
		X = S1;S1 = S2;S2 = X
	tableauScore = getTableau(Event["ListeScore"])

	#Si il y a deja un score différent de 0-0
	if max(int(tableauScore[Ntable-1][0]),int(tableauScore[Ntable-1][1])) != 0 and not is_admin(ctx):
		await sendMessage(Auteur,PhraseReponse(("Resultat","Score Existant")))
		return await sendMessage(getChannel(Event["CanalBot"]),PhraseReponse(("MPBot",Auteur,PhraseReponse(("Resultat","Score Existant")))))

	#On ajoute le match dans le tableau
	tableauScore[Ntable-1][0] = S1
	tableauScore[Ntable-1][1] = S2
	setTableau(Event["ListeScore"],tableauScore)
	msg = PhraseReponse(("Resultat","Score validé")) + f"{tableau[Ntable-1][0]} {tableauScore[Ntable-1][0]}-{tableauScore[Ntable-1][1]} {tableau[Ntable-1][3]}"

	#On arrete tout si le match rentré n'est pas éliminatoire.
	if (Ntable < 121 and Event == MAINEVENT) or (Ntable < 61 and Event == SIDEEVENT) or (Ntable < 41 and Event == FUNEVENT):
		await sendMessage(Membre1,msg)
		await sendMessage(Membre2,msg)
		return await sendMessage(getChannel(Event["CanalBot"]),PhraseReponse(("MPBot",Membre1.name,msg))+"\n"+PhraseReponse(("MPBot",Membre2.name,msg)))

	#On reprend le tableau à jour et on verifie si il y a un match éliminatoire en attente
	time.sleep(10)
	tableau2 = getTableau(Event["ListeMatch"])
	while tableau == tableau2:
		time.sleep(10)
		tableau2 = getTableau(Event["ListeMatch"])

	#---------------------------------------------------------------------------------------------------------------------------------------Possibilité d'envoyer 1 seul message plutot que 2... a réfléchir
	#---------------------------------------------------------------------------------------------------------------------------------------recuperer [[joueur1,message1],[joueur2,message2],...] et faire un for x in ...
	await EnvoyerNextMatch(Event,tableauInscrit,tableau2,J1,Membre1,msg)
	await EnvoyerNextMatch(Event,tableauInscrit,tableau2,J2,Membre2,msg)

@Resultat.error
async def Resultat_error(ctx, error):
	await EffacerMessage(ctx.message)
	if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
		await sendMessage(getChannel(BotRetourGeneral),"🎮❌\n"+PhraseReponse(("Bot",ctx)))
		return await sendMessage(ctx.author,PhraseReponse(("Resultat","Argument Manquant")))
	if isinstance(error, discord.ext.commands.errors.BadArgument):
		await sendMessage(getChannel(BotRetourGeneral),"🎮❌\n"+PhraseReponse(("Bot",ctx)))
		return await sendMessage(ctx.author,PhraseReponse(("Resultat","Argument Invalide")))
	await sendMessage(ctx.author,PhraseReponse(("PLS",ctx)))
	await sendMessage(getChannel(BotRetourGeneral),PhraseReponse(("PLSBOT",ctx)))









@bot.command(
	name="Statistique",
	help="Renvoie l'ensembles des points Ligue et Winrate du joueur qui appelle la commande",
	brief="Renvoie les Winrate et Point Ligue de l'auteur",
	usage="!Statistique ou !Statistique @Membre1 @Membre2...",
	aliases=["Stat","Stats","Statistiques"]
)
async def Statistique (ctx):
	await sendMessage(getChannel(BotRetourGeneral),"🔔\n"+PhraseReponse(("Bot",ctx)))

	canal = ctx.author
	if ctx.channel.id == BOTSPAM:
		canal = ctx.channel

	ListeMembre = ctx.message.mentions
	if ListeMembre == []:
		ListeMembre = [getAuthor(ctx)]

	tableauStat = getTableau(STAT)
	for Joueur in ListeMembre:
		Reussite = False
		for ligne in tableauStat:
			if int(ligne[0]) == Joueur.id:
				present=[];absent=["1er Main Event","1er Side Event","2nd Main Event","2nd Side Event"]

				if ligne[2] != "": present.append("1er Main Event");absent.remove("1er Main Event")
				if ligne[5] != "": present.append("1er Side Event");absent.remove("1er Side Event")
				if ligne[8] != "": present.append("2nd Main Event");absent.remove("2nd Main Event")
				if ligne[11] != "": present.append("2nd Side Event");absent.remove("2nd Side Event")

				msg = f"Voici les statistiques de **{Joueur.name}**"
				if present != []:
					msg = msg + f"\n**{Joueur.name}** a participé"
					for event in present: msg = msg + " au " + event
				if absent != []:
					msg = msg + f"\n**{Joueur.name}** n'a pas participé"
					for event in absent: msg = msg + " au " + event

				msg = msg + f"\n**{Joueur.name}** a {ligne[14]} points de ligue et un winrate de {ligne[15]}.\n"

				if ligne[16] == "*": msg = msg + f"**{Joueur.name}** __est invité au prochain invitational__ 🏆"
				else : msg = msg + f"**{Joueur.name}** est actuellement classé {ligne[17]}e."

				await sendMessage(canal,msg)
				Reussite = True
		if Reussite == False:
			await sendMessage(canal,PhraseReponse(("Statistique","Joueur introuvable",Joueur.name)))

@Statistique.error
async def Statistique_error(ctx, error):
	await EffacerMessage(ctx.message)
	await sendMessage(ctx.author,PhraseReponse(("PLS",ctx)))
	await sendMessage(getChannel(BotRetourGeneral),PhraseReponse(("PLSBOT",ctx)))









def RecupereFinaliste(tableau,Ntable):
	if tableau[Ntable][0]+tableau[Ntable][3] != "":
		if tableau[Ntable][1] == 2 :
			return [tableau[Ntable][0].lower(),tableau[Ntable][3].lower()]
		if tableau[Ntable][2] == 2 :
			return [tableau[Ntable][3].lower(),tableau[Ntable][0].lower()]
		return []
	if tableau[Ntable-1][1] == 2 :
		return [tableau[Ntable-1][0].lower(),tableau[Ntable-1][3].lower()]
	if tableau[Ntable-1][2] == 2 :
		return [tableau[Ntable-1][3].lower(),tableau[Ntable-1][0].lower()]
	return []

def Tri(ListeInvite):
	for Joueur1 in ListeInvite:
		Temp = ListeInvite.copy()
		Temp.remove(Joueur1)
		for Joueur2 in Temp:
			if Joueur1 == Joueur2:
				ListeInvite.remove(Joueur2)
	return ListeInvite

@bot.command(
	name="Invitationnal",
	help="Renvoie les 8 joueurs invités pour l'invitationnal avec leur classement",
	brief="Renvoie les 8 joueurs invités",
	usage="!Invitationnal",
	aliases=["Invitational","Top8"]
)
async def Invitationnal (ctx):
	await EffacerMessage(ctx.message)
	await sendMessage(getChannel(BotRetourGeneral),"🔔\n"+PhraseReponse(("Bot",ctx)))

	canal = ctx.author
	if ctx.channel.id == BOTSPAM:
		canal = ctx.channel

	tableauM1 = getTableau(MAINEVENT1["ListeMatch"])
	tableauS1 = getTableau(SIDEEVENT1["ListeMatch"])
	tableauM2 = getTableau(MAINEVENT2["ListeMatch"])
	tableauS2 = getTableau(SIDEEVENT2["ListeMatch"])
	M1W = [];M1L = [];M2W = [];M2L = [];S1W = [];S2W = []
	M1 = RecupereFinaliste(tableauM1,166)
	if M1 != []:
		M1W = [M1[0]]
		M1L = [M1[1]]
	M2 = RecupereFinaliste(tableauM2,166)
	if M2 != []:
		M2W = [M2[0]]
		M2L = [M2[1]]
	S1 = RecupereFinaliste(tableauS1,82)
	if S1 != []:
		S1W = [S1[0]]
	S2 = RecupereFinaliste(tableauS2,82)
	if S2 != []:
		S2W = [S2[0]]
	ListeInvite = Tri(M1W+M2W+S1W+S2W+M1L+M2L)
	tableauStat = getTableau(STAT)
	i=1
	JoueurRajout = 8-len(ListeInvite)
	while JoueurRajout > 0:
		for ligne in tableauStat:
			if int(ligne[17]) == i:
				ListeInvite.append(ligne[1])
				JoueurRajout = JoueurRajout-1
		i=i+1
	await sendMessage(canal,PhraseReponse(("Invitationnal",ListeInvite)))

@Invitationnal.error
async def Invitationnal_error(ctx, error):
	await EffacerMessage(ctx.message)
	await sendMessage(ctx.author,PhraseReponse(("PLS",ctx)))
	await sendMessage(getChannel(BotRetourGeneral),PhraseReponse(("PLSBOT",ctx)))









@bot.command(
	name="CLEAN",
	aliases=["CLEAR"],
	hidden=True
)
async def Clean (ctx):
	async for message in ctx.history():
		await EffacerMessage(message)


@bot.command(
	name="Test",
	hidden=True
)
async def Test (ctx):
	await EffacerMessage(ctx.message)
	await sendMessage(ctx.author,PhraseReponse(("PLS",ctx)))
	await sendMessage(getChannel(BotRetourGeneral),PhraseReponse(("PLSBOT",ctx)))


def main():
	"""Entrypoint for the Discord Bot"""
	logger.setLevel(logging.INFO)
	bot.run(os.getenv("DISCORD_TOKEN"))
	# reset log level so as to not mess up tests
	logger.setLevel(logging.NOTSET)
