import os
from dotenv import load_dotenv
from dropbox.oauth import DropboxOAuth2FlowNoRedirect

load_dotenv()

APP_KEY = os.getenv("DROPBOX_APP_KEY")
APP_SECRET = os.getenv("DROPBOX_APP_SECRET")

flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET, token_access_type="offline")

url = flow.start()
print("Abre y autoriza:", url)
code = input("Pega el código aquí: ").strip()

result = flow.finish(code)
print("REFRESH TOKEN:", result.refresh_token)