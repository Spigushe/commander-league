def PhraseReponse(arg): #Dictionnaire de réponse du bot
	if arg == "Quel Event ?":
		msg = "Je n'arrive pas à determiner dans quel event tu as fait ta commande. Peut-tu m'aider en votant ci dessous ?"
		msg = msg + "\n:one: pour MainEvent ou :two: pour SideEvent ou :three: pour FunEvent"
		return msg
	if arg == "Erreur Check":
		return "❌ Tu n'as pas les droits pour utiliser cette commande"
	if arg == "Erreur Vote":
		return "❌ Contact un administrateur car je n'ai pas compris ton vote"

	if arg[0] == "Affichage":
		if arg[1] == "Argument Invalide":
			return "❌ Les paramètres que tu as entré sont invalides, tu as mis des valeurs trop grandes, trop petites ou une lettre qui ne correspond pas à une poule"

	if arg[0] == "Ouverture/Fermeture":
		if arg[1] == "Inscriptions ouvertes":
			return f"🟢 Les inscriptions pour le {arg[2]} sont ouvertes"
		if arg[1] == "Inscriptions fermees":
			return f"🔴 Les inscriptions pour le {arg[2]} sont fermees"
		if arg[1] == "Commande inactive":
			return "❌ La commande est inactive pour le moment"
		if arg[1] == "Argument Manquant":
			return "❌ Il faut préciser quel evenement est ouvert aux inscriptions ? Main, Side ou Fun ?"
		if arg[1] == "Argument Invalide":
			return "❌ Je n'ai pas compris quel evenement est ouvert aux inscriptions ? Main, Side ou Fun ?"

	if arg[0] == "Inscription":
		if arg[1] == "Validé":
			return "✅ Ton inscription a bien été validé !"
		if arg[1] == "Tournoi Plein":
			return "\nLe tournoi est plein, tu es dans une liste d'attente"
		if arg[1] == "Quel Macro ?":
			msg = "**Macrotype inconnu**"
			msg = msg + "\nTu n'as pas rajouter de macrotype lors de ton inscription ou bien ce dernier est invalide."
			msg = msg + "\nNous nous basons sur le classement **C** disponible sur le Barrin's Codex."
			msg = msg + "\nhttps://barrins-codex.org/fr/articles/classifier-un-deck/les-macrotypes.html#5_macrotypes"
			msg = msg + "\nTu peux voter ici pour rajouter ton macrotype"
			return msg + "\n:one: pour Aggro ou :two: pour Combo ou :three: pour Control ou :four: pour Midrange ou :five: pour Tempo"
		if arg[1] == "Ajout macro":
			return "✅ Merci d'avoir rajouter ton macrotype, tu as voté : "
		if arg[1] == "Deja inscrit":
			return "❌ Tu es déjà inscrit ! On ne s'inscrit qu'une seule fois !!"
		if arg[1] == "Commande inactive":
			return "❌ Les inscriptions sont fermées pour le moment"
		if arg[1] == "Argument Manquant":
			return "❌ Il faut que je connaisse, votre pseudo Cockatrice, le hastag de votre deck, un lien internet vers votre decklist ainsi que votre eventuel macrotype, ni plus, ni moins."
		if arg[1] == "Argument Invalide":
			return "❌ Je n'ai pas compris les parametres de votre inscriptions, veuillez contacter un administrateur"

	if arg[0] == "Resultat":
		if arg[1] == "Eliminé":
			return "🔴 Tu n'as plus de match à faire dans le tournoi, merci d'avoir participé"
		if arg[1] == "Attente":
			return "🟠 On attend que ton prochain adversaire soit décidé, tu recevra un message lorsqu'on le connaitra"
		if arg[1] == "Next Match vs : ":
			return f"🟢 Ton prochain match est prêt, tu va devoir affronter : **{arg[2]}**"
		if arg[1] == "Joueur introuvable":
			return f"❌ **{arg[2]}** est introuvable dans le tournoi(pas inscrit) ou dans le serveur(absent)."
		if arg[1] == "Auteur invalide":
			return "❌ Tu ne fais pas parti des joueurs du match... tu n'as pas le droit de rentrer le score"
		if arg[1] == "Score Impossible":
			return "❌ Ce résultat me semble étrange, pourrais-tu vérifier stp ?"
		if arg[1] == "Match Introuvable":
			return "❌ Le match est introuvable, est-tu sur que ces deux joueurs se rencontrent ?"
		if arg[1] == "Score Existant":
			return "❌ Le score est déjà écrit, si il y a contestation il faut aller voire un administrateur."
		if arg[1] == "Score validé":
			return "✅ Le score a été enregistré :\n"
		if arg[1] == "Argument Manquant":
			return "❌ Il me manque l'un des joueurs ou le Score, as-tu bien repescté les espaces : Joueur1 0-0 Joueur2"
		if arg[1] == "Argument Invalide":
			return "❌ Les paramètres que tu as entré sont invalides il faut écrire sous la forme : Joueur1 0-0 Joueur2"

	if arg[0] == "Statistique":
		if arg[1] == "Joueur introuvable":
			return f"Je ne trouve pas le joueur **{arg[2]}** parmis les participants de cette saison"

	if arg[0] == "Invitationnal":
		msg = "Voici les joueurs actuellement invitées et la listes des matchs prévus pour le prochain TOP8 Invitationnal : \n"
		msg = msg + f"-🎲 1e : {arg[1][0]} VS 8e : {arg[1][7]}\n-🎲 4e : {arg[1][3]} VS 5e : {arg[1][4]}\n-🎲 2e : {arg[1][1]} VS 7e : {arg[1][6]}\n-🎲 3e : {arg[1][2]} VS 6e : {arg[1][5]}\n"
		msg = msg + "**La personne écrite à gauche décidera de commencer ou non la première manche**\n"
		return msg + "Attention, si les saisons en cours ne sont pas terminés ce classement peut encore changer."

	if arg[0] == "PLS":
		return f"❌ La fonction {arg[1].command.name} a planté, les administrateurs ont normalement été mis au courant. Nous cherchons à résoudre ce problème."

	if arg[0] == "Bot":
		return f"Message envoyé depuis <#{arg[1].channel.id}> par **{arg[1].author.name}**:\n*Contenu du message* `{arg[1].message.content}`"
	if arg[0] == "MPBot":
		return f"✉️\nLe BOT a envoyé le message suivant dans les MP de **{arg[1]}**:```{arg[2]}```"
	if arg[0] == "PLSBOT":
		return f"⚠️⚠️⚠️⚠️⚠️\nLa fonction {arg[1].command.name} a planté, voici le contexte : \nMessage envoyé depuis <#{arg[1].channel.id}> par **{arg[1].author.name}**:\n*Contenu du message* `{arg[1].message.content}`"

	# Cas par défaut
	return "⚠️ Je ne sais pas ce que je dois dire"


dicMessage = {
	# Member voting phrases
	'vote-macrotype': """🤖 **Bip, Boup**
⚠️ I was not able to handle the macrotype you've given me
✉️ Can you react to the right one, please ?
1️⃣ Aggro     2️⃣ Tempo     3️⃣ Control   4️⃣ Combo     5️⃣ Midrange""",
	'vote-error': "❌ The reaction you just used has raised an error. Please reach out to a staff member to get some help",
	'vote-success': "Thank you for your input, I have taken appropriate measures",

	# Registration phrases
	'registration-complete': "✅ You have been successfully registered !",
	'registration-registered': "❌ You are already registered, please use this command only once",
	'registration-full': "🤖 **Bip, Boup**\nThe event is full, I'll check if I can add you to the waiting list",
	'registration-ok': "📝 **New Registration**\nMaster Table has been updated\nMessage content: ",
	'registration-missing': "❌ There are some required information that you did not give us. Please refer to `!help register` for the full command and details about the arguments",
	'registration-disabled': "❌ Registration are closed for all of our event for now",
	'registration-bad-argument': "❌ The arguments used do not fit with what I've been programmed for. Please reach out to a staff member to get som help",
}
