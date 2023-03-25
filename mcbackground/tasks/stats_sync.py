import asyncio
import uuid 
from zipfile import ZipFile
from os import listdir, path
from json import loads, dumps
from datetime import datetime

from ..db import conn
from ..servernet import get_server_file

async def store_stats_in_database():
	cursor = conn.cursor()
	# Periodically call the same method by looping indefinitely
	while True:
		print("Preparing to update player stats...")
		backups_folder = get_server_file()

		all_zips = [f for f in listdir(backups_folder) if f.endswith('.zip')]
		all_zips = sorted(all_zips)
		
		# Store the final data to be stored in DB
		data_by_date: dict = {}
		for fname in all_zips:
			# Grab fnames that have actual backup data
			print(f"Processing {fname} for stats")
			# The date to associate this particular data point with
			# The file is of the format Backup--world--DATE
			# So just ignore irrelevant strings including zip extension
			raw_date = fname[:-4]
			parsed_date = datetime.strptime(raw_date, "%Y-%m-%d-%H-%M-%S")

			with ZipFile(path.join(backups_folder, fname), 'r') as zf:
				user_datas = []
				# Could potentially break if some other stats folder comes into play.
				stats_fnames = [f for f in zf.namelist() if f.startswith(f"world{path.sep}stats{path.sep}") and f.endswith(".json")]

				for stat_fname in stats_fnames:
					# Get the UUID of the user by parsing file name
					# Separate by folder delimitter and then remove json extension
					uniq_id = stat_fname.split(path.sep)[-1][:-5]

					f = zf.read(stat_fname)
					user_data = clean_stats_json(loads(f))

					# Process the loaded data
					parsed_data = (str(uuid.uuid4()), parsed_date, uniq_id, dumps(user_data['DataVersion']), dumps(clean_stats_json(loads(f))))
					user_datas.append(parsed_data)

				cursor.executemany("INSERT OR IGNORE INTO PlayerStats (id, date, userId, dataVersion, stats) VALUES (?, ?, ?, ?, ?)", user_datas)

		conn.commit()
		print("Done updating player stats")
									
		# Run this in 30 minutes time
		await asyncio.sleep(1800)

def clean_stats_json(loaded_json: dict) -> dict:
	"""JSON loads makes each element in the stats file
	into its own key, and doesn't recursively create
	a dict. Fix that by doing exactly that."""
	cleaned_json = {}

	for key, value in loaded_json.items():
		# We need the last element too because some stats
		# hold accumulations of all its children.
		path_list = key.split(".")

		drill = cleaned_json
		for stat_key in path_list:
			drill = drill.setdefault(stat_key, {})

		# To remove ambiguity and type checking, store the
		# actual stat value in a unique key.
		drill["_stat"] = value	

	return cleaned_json