from httpx import Client
from base64 import b64encode

def get_image_data(image_path):
	with open(image_path, "rb") as img_file:
		return b64encode(img_file.read()).decode('utf-8')

def change_pfp(token, s, fingerprint, super_properties, __dcfduid, __sdcfduid, pfp_name):
	headers = {
		'Host': 'discord.com',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
		'Accept': '*/*',
		'Accept-Language': 'it',
		'Accept-Encoding': 'gzip, deflate, br',
		'Content-Type': 'application/json',
		'Authorization': token,
		'X-Super-Properties': super_properties,
		'X-Fingerprint': fingerprint,
		'X-Debug-Options': 'bugReporterEnabled',
		'Origin': 'https://discord.com',
		'Connection': 'keep-alive',
		'Referer': 'https://discord.com/channels/@me',
		'Cookie': '__dcfduid={}; __sdcfduid={}'.format(__dcfduid, __sdcfduid),
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-origin',
		'Pragma': 'no-cache',
		'Cache-Control': 'no-cache',
		'TE': 'trailers'
	}

	payload = {"avatar":f"data:image/png;base64,{get_image_data('data/pfps/'+pfp_name)}"}

	return s.patch('https://discord.com/api/v9/users/@me', headers=headers, json=payload)
	


