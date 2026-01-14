import dropbox

def downloadFile(dbx, dropboxPath, localPath):
    try:
        metadata, res = dbx.files_download(path=dropboxPath)
        with open(localPath, 'wb') as f:
            f.write(res.content)
        print(f"Successfully downloaded '{dropboxPath}' to '{localPath}'")
    except dropbox.exceptions.HttpError as e:
        print(f"HTTP error downloading file: {e}")
    except dropbox.exceptions.ApiError as e:
        print(f"API error downloading file: {e.pathLookup}")