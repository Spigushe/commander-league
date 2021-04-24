import collections
import json

from discord.ext import commands
from discord_argparse import *

class MyHelpCommand(commands.DefaultHelpCommand):
	async def send_command_help(self, command):
		self.add_command_formatting(command)
		for name, param in command.clean_params.items():
			if isinstance(param.annotation, ArgumentConverter):
				arguments = param.annotation.arguments
				if not arguments:
					continue
				self.paginator.add_line("Arguments:")
				max_size = max(len(name) for name in arguments)

				for name, argument in arguments.items():
					entry = "{0}{1:<{width}} {2}".format(self.indent * " ", name, argument.doc, width=max_size)
					self.paginator.add_line(self.shorten_text(entry))
		self.paginator.close_page()
		await self.send_pages()

class ArgumentConverter(ArgumentConverter):
	def sort(self):
		self.arguments = collections.OrderedDict(sorted(self.arguments.items()))

	def get_args(self):
		return self.arguments.keys()

	def __add__(self, other):
		args = {}
		for k,v in self.arguments.items():
			args[k] = v
		for k,v in other.arguments.items():
			if k in args.keys():
				pass
			args[k] = v
		return ArgumentConverter(**args)




# Registration parser
registration = ArgumentConverter(
	nickname = RequiredArgument(
		str,
		doc="Nickname on Rooster Rangers' Cockatrice Server"
	),
	hash = RequiredArgument(
		str,
		doc="Hashcode from Cockatrice's deckfile"
	),
	link = RequiredArgument(
		str,
		doc="Moxfield link to the decklist"
	),
	macrotype = OptionalArgument(
		str,
		doc="Macrotype of the deck: Aggro, Tempo, Control, Combo, Midrange",
		default=""
	)
)
