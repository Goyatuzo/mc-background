from os import path, environ, system, listdir
from sys import platform
from pathlib import Path

# The usrename and passwords should be in the environment variables
__username = environ['SMB_USERNAME']
__pwd = environ['SMB_PASSWORD']
__ip = environ['MC_SERVER_IP']
__backup_path = environ['BACKUP_PATH']

# Mount on the home directory
__home_dir = str(Path.home())
mounting_dir = path.join(__home_dir, 'MC_Discord_Bot')

def setup() -> None:
	"""Create the folder to mount the server files if it doesn't exist.
	Then mount the SevTech files onto the computer."""
	print("Mounting...")
	# The command to mount the server files into the file system.
	if platform == "darwin":
		cmd = f"mount -t smbfs //{__username}:{__pwd}@{__ip}/{__backup_path} {mounting_dir}"
	else:
		cmd = f"sudo mount -t cifs //{__ip}/{__backup_path} {mounting_dir} -o username={__username},password={__pwd},uid=$(id -u),gid=$(id -g),nobrl"
	
	mounting_path = Path(mounting_dir)
	# Recursively create the folder if it does not already exist
	if not mounting_path.exists():
		mounting_path.mkdir(parents=True)

	# Run the mounting command
	if len(listdir(mounting_path)) == 0:
            system(cmd)

def get_server_file(*args: str) -> str:
	"""Grab path to file on the server corresponding to input args."""
	return path.join(mounting_dir, *args)
