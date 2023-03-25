import asyncio
from .player_sync import store_players_in_database
from .stats_sync import store_stats_in_database

def setup_tasks():
	loop = asyncio.get_event_loop()
	loop.create_task(store_players_in_database())
	loop.create_task(store_stats_in_database())
	loop.run_forever()