import discord
import main
import os

from typing import Optional


class MyClient(discord.Client):
	async def on_ready(self):
		print(f'Logged on as {self.user}')
		self.id_dict = main.load_pokedict()
		self.dev_mode = os.getenv('DEVMODE', 'false').lower() == 'true'
		print('Ready')

	async def on_message(self, message: discord.Message):
		if message.content.startswith('!'):
			args = message.content.split()
			if args[0] == '!fuse':
				_, p1, p2 = args

				id1 = self.id_dict.get(p1.lower())
				id2 = self.id_dict.get(p2.lower())

				print(f'{id1=} {id2=}')

				url = main.get_fusion_url(id1, id2)
				await self.embed_img(message, url, f'{p1}/{p2}')

	async def embed_img(self, message: discord.Message, url: str, description: Optional[str] = None):
		embed = discord.Embed(description=description)
		embed.set_image(url=url)

		msg = message.author.mention

		if self.dev_mode:
			msg = f'DEVMODE\n{msg}'

		await message.channel.send(msg, embed=embed)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.environ['POKEFUSION_TOKEN'])
