#Theresa Lee
#Comp 380
#Comp Sci Role

import hikari as h
import os
from typing import Optional, Union
from hikari import Embed, GatewayBot, Intents, events

class CompSci(GatewayBot):
    def __init__(self, token: str):
        super().__init__(token, intents=Intents.GUILDS | Intents.GUILD_MESSAGE_REACTIONS | Intents.GUILD_MESSAGES)
        self.event_manager.subscribe(events.GuildMessageCreateEvent, self.send_reaction_embed)
        self.event_manager.subscribe(events.GuildReactionAddEvent, self.reaction_role)
        self.event_manager.subscribe(events.GuildReactionDeleteEvent, self.reaction_role)
        self.embed_id: Optional[int] = None

    async def send_reaction_embed(self, event: events.GuildMessageCreateEvent):
        if event.content and event.content.startswith('/csrole'):
            message = await event.message.respond(embed=Embed(title='React on this for CompSci notifications!'))
            await message.add_reaction("🌸")
            self.embed_id = message.id

    async def reaction_role(self, event: Union[events.GuildReactionAddEvent, events.GuildReactionDeleteEvent]):

        if self.embed_id and event.message_id == self.embed_id:
            guild = self.cache.get_available_guild(event.guild_id)
            assert guild

            role = next(filter(lambda k: k[1].name == 'compsci', guild.get_roles().items()), None)

            if role is None:
                print(f'CompSci role not found for guild {guild.name}')
                return

            if isinstance(event, events.GuildReactionAddEvent):
                await event.member.add_role(role[0])
                print('Reaction added')
            else:
                user = guild.get_member(event.user_id)
                assert user
                await user.remove_role(role[0])
                print('Reaction removed')

bot = CompSci(token =
    'INSERT TOKEN HERE')
bot.run()

@bot.listen(h.StartedEvent)
async def on_started(event):
    print('Bot as started!')
