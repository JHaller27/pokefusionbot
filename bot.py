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
			if args[0] == '!fuse' and len(args) == 3:
				_, p1, p2 = args

				id1 = self.id_dict.get(p1.lower())
				if id1 is None:
					await self.send_reply(message, f"**I'm sorry, I don't recognize {p1}.** :cry:")
					return

				id2 = self.id_dict.get(p2.lower())
				if id2 is None:
					await self.send_reply(message, f"**I'm sorry, I don't recognize {p2}.** :cry:")
					return

				url = main.get_fusion_url(id1, id2)
				await self.send_embed(message, url, f'{p1}/{p2}')

	def get_reply(self, message: discord.Message, text: str = '') -> str:
		reply = f'{message.author.mention}\n{text}'

		if self.dev_mode:
			reply = f'DEVMODE\n{reply}'

		return reply

	async def send_reply(self, message: discord.Message, text: str) -> None:
		await message.channel.send(self.get_reply(message, text))

	async def send_embed(self, message: discord.Message, url: str, description: Optional[str] = None):
		embed = discord.Embed(description=description)
		embed.set_image(url=url)

		msg = self.get_reply(message)

		await message.channel.send(msg, embed=embed)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.environ['POKEFUSION_TOKEN'])
