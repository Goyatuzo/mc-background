import asyncio
from ..servernet import get_server_file
from ..db import cursor, conn
from json import loads

async def store_players_in_database():
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

		# Run this in 30 minutes time
		await asyncio.sleep(10)