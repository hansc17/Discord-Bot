#Theresa Lee
#Comp 380
#Comp Sci Role

import hikari
import miru


class MyView(miru.View):

    @miru.button(label="CS", emoji="🕵️", style=hikari.ButtonStyle.PRIMARY)
    async def role1_button(self, button: miru.Button, ctx: miru.Context) -> None:
        roleid = 951187316720930868
        roles = ctx.member.role_ids
        if roleid in roles:
            await ctx.member.remove_role(role = roleid)
        else:
            await ctx.member.add_role(role = roleid)

    @miru.button(label="Bio", emoji="🐸", style=hikari.ButtonStyle.PRIMARY)
    async def role2_button(self, button: miru.Button, ctx: miru.Context) -> None:
        roleid = 970876509583708200
        roles = ctx.member.role_ids
        if roleid in roles:
            await ctx.member.remove_role(role = roleid)
        else:
            await ctx.member.add_role(role = roleid)

    @miru.button(label="Eng", emoji="📎", style=hikari.ButtonStyle.PRIMARY)
    async def role3_button(self, button: miru.Button, ctx: miru.Context) -> None:
        roleid = 970876692283424849
        roles = ctx.member.role_ids
        if roleid in roles:
            await ctx.member.remove_role(role = roleid)
        else:
            await ctx.member.add_role(role = roleid)


bot = hikari.GatewayBot(token="OTQ4NzY1ODU2NjM5MzczMzMz.YiAlDw.qswCjw1M1dxbZWh93rVDqdncCps")
miru.load(bot)


@bot.listen()
async def buttons(event: hikari.GuildMessageCreateEvent) -> None:

    if event.is_bot or not event.content:
        return

    if event.content.startswith("/roles"):
        view = MyView(timeout=0)  # Create a new view
        message = await event.message.respond("Choose Roles for notifications!", components=view.build())
        view.start(message)  # Start listening for interactions
        await view.wait() # Wait until the view times out or gets stopped

bot.run()
