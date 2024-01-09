
from src.youtube_channel_details_api_client_apiharbor.api_client import YouTubeChannelDetailsApiClient
import asyncio

api = YouTubeChannelDetailsApiClient('__YOUR_RAPIDAPI_KEY__')

async def test_get_channel_details():
    r = await api.get_channel_details('@MrBeast')
    assert r.status == 200
    assert r.data.channel_id == 'UCX6OQ3DkcsbYNE6H8uQQuVA' 

async def main():
  await test_get_channel_details()
  return None

asyncio.run(main())