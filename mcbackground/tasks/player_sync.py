import asyncio
from ..servernet import get_server_file
from ..db import conn
from json import loads

async def store_players_in_database():
	cursor = conn.cursor()
	try:
		# Periodically call the same method by looping indefinitely
		while True:
			print("Preparing to update users...")

			fpath = get_server_file("usercache.json")

			with open(fpath) as f:
				users = loads(f.read())
				
				cleaned_users = [(user["uuid"], user["name"]) for user in users]

				cursor.executemany("INSERT OR REPLACE INTO Players(uuid, name) VALUES (?, ?)", cleaned_users)
				conn.commit()

				print(f"Updated {len(cleaned_users)} users")

			# Run this in 10 minutes time
			await asyncio.sleep(10)
	except Exception as e:
		print(e)
