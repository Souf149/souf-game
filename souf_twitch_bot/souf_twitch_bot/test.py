from souf_twitch_bot.bot import Bot
from souf_twitch_bot.config import settings
import twitchio
import asyncio
from twitchio.ext import pubsub


users_channel_id = 12345
client = twitchio.Client(token=settings.access_token)
client.pubsub = pubsub.PubSubPool(client)


@client.event()
async def event_pubsub_bits(event: pubsub.PubSubBitsMessage):
    print(event)


@client.event()
async def event_pubsub_channel_points(event: pubsub.PubSubChannelPointsMessage):
    print(event)


async def main():
    topics = [
        pubsub.channel_points(settings.access_token)[users_channel_id],
        pubsub.bits(settings.access_token)[users_channel_id],
    ]
    await client.pubsub.subscribe_topics(topics)
    await client.start()


client.loop.run_until_complete(main())
