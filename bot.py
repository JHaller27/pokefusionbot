import discord
import main
import os


class MyClient(discord.Client):
	async def on_ready(self):
		print(f'Logged on as {self.user}')
		self.id_dict = main.load_pokedict()

	async def on_message(self, message: discord.Message):
		if message.content.startswith('!'):
			args = message.content.split()
			match args:
				case ['!fuse', p1, p2]:
					id1 = self.id_dict.get(p1)
					id2 = self.id_dict.get(p2)

					url = main.get_fusion_url(id1, id2)
					await message.channel.send(url)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.environ['POKEFUSION_TOKEN'])
