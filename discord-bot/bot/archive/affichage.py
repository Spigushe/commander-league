@bot.command(
	name="affichage",
	help="Affiche le résultat des matchs d'une poule ou d'une table particulière à partir du numéro de table ou de la lettre de la poule si il n'y a pas d'arguments, la fonction affiche tous les matchs du tournoi",
	brief="Affiche la table X ou les match de la poule X ou tous les matchs",
	usage="!Affichage 1 ou !Affichage A ou !Affichage",
	aliases=["Afficher", "Affiche"]
)
async def Affichage(ctx, *args):
	await EffacerMessage(ctx.message)
	Event = await CheckEvent(ctx)
	await sendMessage(getChannel(Event["CanalBot"]),"🔔\n"+PhraseReponse(("Bot",ctx)))

	tableau = getTableau(Event["ListeMatch"])
	#Si pas d'arguments, on affiche tous les Matchs
	if len(args) == 0 :
		i=1
		Message = ""
		for ligne in tableau:
			Message = Message + AfficherMatch(tableau,i) + "\n"
			i=i+1
		return await sendMessage(ctx,Message)
	#Si l'argument est un nombre, on affiche la table qui correspond
	if args[0].isnumeric() :
		if (args[0] == "0"): raise IndexError
		return await sendMessage(ctx,AfficherMatch(tableau,int(args[0])))
	#Si l'argument est une lettre, on affiche la poule qui correspond
	return await sendMessage(ctx,AfficherPoule(Event,tableau,str(args[0]).upper()))

@Affichage.error
async def Affichage_error(ctx, error):
	await EffacerMessage(ctx.message)
	if isinstance(error, IndexError):
		await sendMessage(getChannel(BotRetourGeneral),"🔔❌\n"+PhraseReponse(("Bot",ctx)))
		return await sendMessage(ctx.author,PhraseReponse(("Affichage","Argument Invalide")))
	if isinstance(error, ValueError):
		await sendMessage(getChannel(BotRetourGeneral),"🔔❌\n"+PhraseReponse(("Bot",ctx)))
		return await sendMessage(ctx.author,PhraseReponse(("Affichage","Argument Invalide")))
	await sendMessage(ctx.author,PhraseReponse(("PLS",ctx)))
	await sendMessage(getChannel(BotRetourGeneral),PhraseReponse(("PLSBOT",ctx)))
