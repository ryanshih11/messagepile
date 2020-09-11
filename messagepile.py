import discord
from runner import Runner
from lxml import objectify

client = discord.Client()
runner = Runner()
channels = []
token = ''
config_path = '/home/meet/Documents/Programming/python/messagepile/config.xml'

@client.event
async def on_ready():
    print("Logged on as {0}!".format(client.user))
    for server in client.guilds:
        print(server)
        for channel in server.channels:
            channels.append(channel)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print("Message from {0.author}: {0.content}".format(message))

    if message.content.startswith('!code'):
        await message.channel.send('Received code command.')

if __name__ == '__main__':
    with open(config_path, 'r') as conf_xml:
        data = ''.join(conf_xml.readlines())
        root = objectify.fromstring(data)
        token = root.token.text
    client.run(token)
    #runner.run_code('python', 'print("test")')
