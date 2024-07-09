import asyncio
from telethon import TelegramClient

api_id = 23313724
api_hash = "9a048695d31d76ed4d977920a8b40eec"
phone_number = "+918089708574"

async def main():
    client = TelegramClient('anon', api_id, api_hash)
    assert await client.connect()
    if not client.is_user_authorized():
        await client.send_code_request(phone_number)
        me = await client.sign_in(phone_number, input('Enter code: '))

async def run_main():
    await main()

asyncio.run(run_main())