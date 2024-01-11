from dotenv import load_dotenv
from dasscostorageclient import DaSSCoStorageClient
import os

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

client = DaSSCoStorageClient(client_id, client_secret)
