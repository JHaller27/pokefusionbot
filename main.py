import requests
import typer
import random
import yaml
from functools import cache


def load_pokedict() -> dict[str, int]:
	with open('data.yml') as fp:
		data = yaml.safe_load(fp)
	pokedict = data['idMap']
	for fix_name in data['nameFixMap']:
		pokedict[fix_name] = pokedict[data['nameFixMap'][fix_name]]

	return pokedict


@cache
def does_image_exist(image_url: str):
	resp = requests.head(image_url)
	return resp.status_code != 404


@cache
def get_fusion_url(head_id: str, body_id: str):
	fusion_id = f'{head_id}.{body_id}'
	fusionUrl = f'https://raw.githubusercontent.com/Aegide/custom-fusion-sprites/main/CustomBattlers/{fusion_id}.png'

	if does_image_exist(fusionUrl):
		# color = green
		return fusionUrl

	# Screenshot of autogen pokemon
	else:
		# color = red
		return f'https://raw.githubusercontent.com/Aegide/autogen-fusion-sprites/master/Battlers/{head_id}/{fusion_id}.png'


def main(head_name: str = typer.Argument(None), body_name: str = typer.Argument(None), invert: bool = typer.Option(False, '-i', '--invert')):
	pokedict = load_pokedict()
	all_names = list(pokedict.keys())

	if head_name is None and body_name is None:
		head_name = random.choice(all_names)
		body_name = random.choice(all_names)

	if body_name is None:
		body_name = random.choice(all_names)
		head_name, body_name = random.choices((head_name, body_name), k=2)

	if invert:
		head_name, body_name = body_name, head_name

	print(head_name, body_name)
	head_id = pokedict.get(head_name.lower())
	body_id = pokedict.get(body_name.lower())

	if head_id is None:
		print(f'No pokemon named {head_name}')
		raise typer.Abort()

	if body_id is None:
		print(f'No pokemon named {body_name}')
		raise typer.Abort()

	print(get_fusion_url(head_id, body_id))


if __name__ == '__main__':
	typer.run(main)
