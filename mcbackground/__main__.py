from .servernet import setup
from dotenv import load_dotenv

# Load environment variables
load_dotenv(verbose=True)

setup()

from .tasks import setup_tasks
setup_tasks()