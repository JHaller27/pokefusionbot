import discord
import main
import os


class MyClient(discord.Client):
	async def on_ready(self):
		print(f'Logged on as {self.user}')
		self.id_dict = main.load_pokedict()
		self.dev_mode = os.getenv('DEVMODE').lower() == 'true'

	async def on_message(self, message: discord.Message):
		if message.content.startswith('!'):
			args = message.content.split()
			if args[0] == '!fuse':
				_, p1, p2 = args

				id1 = self.id_dict.get(p1)
				id2 = self.id_dict.get(p2)

				url = main.get_fusion_url(id1, id2)
				await self.respond_to(message, url)

	async def respond_to(self, message: discord.Message, reply: str):
		if self.dev_mode:
			await message.channel.send(f'DEVMODE\n{reply}')
			return

		await message.channel.send(reply)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.environ['POKEFUSION_TOKEN'])
