import discord
import time

def get_text_from_file(filename):
    return open(filename,'r').read()

def get_object_in_array_from_name(name,arr):
    for obj in arr:
        if obj.name == name:
            return obj
    return None

class MrAcminClient(discord.Client):
    def __init__(self):
        super().__init__()
        self.__prefix = '#'
    async def on_ready(self):
        print('Logged in as {0}!'.format(self.user))
    async def on_message(self,message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.author == self.user or not message.content.startswith(self.__prefix):
            return
        args = message.content[len(self.__prefix):].split()
        argc = len(args)
        try:
            if args[0] == 'help':
                if argc != 1:
                    raise InvalidArgs("Invalid num of arguments.")
                help_message = get_text_from_file('help.txt')
                await message.channel.send(help_message)
            elif args[0] == 'getAttendance':
                if argc <= 1:
                    raise InvalidArgs("Invalid num of arguments.")
                selected_channel_name = ' '.join(args[1:])
                selected_channel = get_object_in_array_from_name(selected_channel_name, message.guild.voice_channels)
                if selected_channel == None:
                    await message.channel.send("Channel not found.")    
                    return
                user_names = []
                for current_user_id in selected_channel.voice_states.keys():
                    current_user_name = await self.fetch_user(user_id=current_user_id)
                    user_names.append(current_user_name)
                await message.channel.send("__**Attendance at [{0}]**__\n **{1}**:\n {2}".format(time.ctime(),selected_channel.name,'\n'.join(map((lambda user: user.name),user_names)) if len(user_names) else "(No one)."))
            elif args[0] == 'about':
                if argc != 1:
                    raise InvalidArgs("Invalid num of arguments.")
                about_message = get_text_from_file('about.txt')
                await message.channel.send(about_message)
        except BaseException as error:
            print(error)

def main():
    client = MrAcminClient()
    token = get_text_from_file('token.txt')
    client.run(token)

if __name__ == '__main__':
    main()
