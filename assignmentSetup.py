#testing
import hikari
import lightbulb
from lock import *
import psycopg2

#Setting connection to database in AWS RDS
conn = psycopg2.connect(
    host=host_name,
    database=database_name,
    user=primary_user,
    password=password,
    port= port_key
)

#Initializing cursor object
#Setting auto-commit false (?)
cursor = conn.cursor()
conn.autocommit = True

bot = lightbulb.BotApp(
    token=TOKEN, 
    #default_enabled_guilds=(guildID)
)

@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print('Bot has started')

@bot.listen(hikari.StartedEvent)
async def on_ready(event):
    print('I am online!')

@bot.command
@lightbulb.option('duedate', 'Due date of assignment. Format: MM-DD-YYYY (example: 03-01-2022)')
@lightbulb.option('assignment', 'Assignment name')
@lightbulb.option('section', 'Class assignment is from. Format: @"class" (example: @comp380) ')
@lightbulb.command('addassn', 'Set up a notification for an upcoming assignment.')
@lightbulb.implements(lightbulb.SlashCommand)
async def addassn(ctx):
    duedate = ctx.options.duedate
    assignment = ctx.options.assignment
    section = ctx.options.section
    guildID = ctx.member.guild_id
    userID = ctx.member.id
    username = ctx.member.username

    #store input in database/table
    query = "INSERT INTO student (guild_ID, user_id, username, section, assignment, due_date) VALUES(%s, %s, %s, %s, %s, %s);"
    data = (guildID, userID, username, section, assignment, duedate)
    cursor.execute(query, data)
    #commit changes
    conn.commit()
    await ctx.respond(f'Noted, {assignment} is due on {duedate} for {section}')


bot.run()