from flask import Flask, jsonify,request
from flask_cors import CORS

import asyncio
from telethon.sync import TelegramClient, events
import os
from tqdm import tqdm
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")


async def downloadfile(file_to_download):
    #title: Chat Name
    title = 'Project Notes'
    
    found_file = None
    global download_folder

    #Default Path for Downloads
    download_folder= os.path.join(os.path.expanduser("~"), "Downloads")
    
    async with TelegramClient('name', api_id, api_hash) as client:
        async for chat in client.iter_dialogs():
            if chat.title == title:
                messages = await client.get_messages(chat, limit=200)

                for message in tqdm(messages):
                    # Check if the message contains the desired file
                    if message.media and hasattr(message.media, 'document') and message.media.document.mime_type == 'application/pdf' and message.media.document.attributes[0].file_name == file_to_download:
                        download_path = os.path.join(download_folder,title,file_to_download)
                        await message.download_media(download_path)
                        found_file = "success"
                        print(f"File '{file_to_download}' found and contents saved")
                        break
                      
                    else:
                        print(f"File '{file_to_download}' not found in '{title}' chat")
                if(found_file=="success"):
                    return "success"
                else:
                    return "fail"
        
async def uploadfile(newfilecontents,newname):
    download_folder= os.path.join(os.path.expanduser("~"), "Downloads")
    file_path = os.path.join(download_folder, newname)
    with open(file_path, "wb") as f:
        f.write(newfilecontents)
    
    print(f"File saved to {file_path}")
    print("Upload Initiated!!!")
    title = 'Project Notes'

    async with TelegramClient('name', api_id, api_hash) as client:
        print("Client Connected!!!")
        async for chat in client.iter_dialogs():
            if chat.title == title:
                print("Chat Found Successfully!!!")
                await client.send_file(chat, file_path)
                print(f"File '{file_path}' uploaded to '{title}' chat")
                os.remove(file_path)
                return "success"
        print(f"Chat with title '{title}' not found")
        return "fail"


app=Flask(__name__)
CORS(app)


message="Hello World"
@app.route('/api/home',methods=['GET'])
def return_home():
    
    return jsonify({
        "message":message
    })


@app.route('/api/download',methods=['POST'])
def download():

    filename = request.get_json()
    newfile = filename.get("name")
    print("File Accepted:",newfile)
    newfile = newfile+".pdf"
    finalresult = asyncio.run(downloadfile(newfile))
    return jsonify({
        "result":finalresult
    })
    
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename=file.filename
    file_contents = file.read()

    print("HI")
    asyncio.run(uploadfile(file_contents,filename))
    return 'File uploaded successfully'

if __name__ == "__main__":
    app.run(debug=True,port=8080)
