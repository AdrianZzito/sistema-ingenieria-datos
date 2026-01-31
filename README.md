# EXECUTE PROJECT
1. Pre execution
Install requirements.txt ```pip install requirements.txt```

2. Once requirements.txt was installed, create .env file, use .env.example as a guide to fill all data and rename as .env
NOTE: To generate value 'DROPBOX_REFRESH_TOKEN' you need to run the file 'dropboxRefreshTokenRequest.py' and follow the requested steps, when it finishes, you will be prompted with a text like 'REFRESH TOKEN:' followed by your refresh token, copy it and paste it on the .env file

3. Then, execute the project with 'python3 main.py' (Database connection should be working to get project running successfully)