import discord
from runner import Runner
from lxml import objectify

client = discord.Client()
runner = Runner()
channels = []
token = ''
config_path = '/home/meet/Documents/Programming/python/messagepile/config.xml'
last_message = ''

@client.event
async def on_ready():
    print("Logged on as {0}!".format(client.user))
    for server in client.guilds:
        print(server)
        for channel in server.channels:
            channels.append(channel)

@client.event
async def on_message(message):
    global last_message

    if message.author == client.user:
        return

    print("Message from {0.author}: {0.content}".format(message))

    if message.content.startswith('!code'):
        split = message.content.split()
        language = split[1]
        await message.channel.send('Running your {0} code. One moment.'.format(language))
        code = last_message[last_message.find('\n') + 1:last_message.rfind('\n')]
        out, err = runner.run_code(language, code, args=split[2:])
        await message.channel.send('stdout:\n```\n' + (out if len(out) > 0 else 'error') + '\n``` '+ (('\nstderr:\n```\n' + err + '\n```') if len(err) > 0 else '') + '\nDone.')
        
    last_message = message.content

if __name__ == '__main__':
    with open(config_path, 'r') as conf_xml:
        data = ''.join(conf_xml.readlines())
        root = objectify.fromstring(data)
        token = root.token.text
    client.run(token)