#testing
import hikari
from hikari import *
import lightbulb
from lightbulb import *
from lock import *
import psycopg2
import datetime

#Setting connection to database
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
    #default_enabled_guilds=(deg)
)

@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print('Bot has started')

@bot.listen(hikari.StartedEvent)
async def on_ready(event):
    print('I am online!')


@bot.command
@lightbulb.option('duedate', 'Due date of assignment. Format: MM-DD-YYYY (example: 03-01-2022)', type=datetime.datetime)
@lightbulb.option('assignment', 'Assignment name')
@lightbulb.option('section', 'Class assignment is from. Format: @"class" (example: @comp380) ', type=hikari.Role)
@lightbulb.command('addassn', 'Set up a notification for an upcoming assignment.')
@lightbulb.implements(lightbulb.SlashCommand)
async def addassn(ctx):
    duedate = ctx.options.duedate
    assignment = ctx.options.assignment
    section = ctx.options.section
    guildID = ctx.member.guild_id
    userID = ctx.member.id
    username = ctx.member.username
    ######checks for proper input before sending it to database:###########
    class_id = section.id
    class_name = section.name
    role_ids = ctx.member.role_ids
    #checks if user has assigned role and disallows the user to use @everyone role
    if class_id not in role_ids:
        await ctx.respond('You are not assigned to this class! Check if you are assigned to the class and try the command again.')
    elif class_id == guildID:
        await ctx.respond('This role is not a valid class!')
    else:
        #store user input into database
        query = "INSERT INTO student (guild_id, user_id, username, section, section_id, assignment, due_date) VALUES(%s, %s, %s, %s, %s, %s, %s);"
        data = (guildID, userID, username, class_name, class_id, assignment, duedate)
        #check for invalid dates
        try: 
            cursor.execute(query, data)
        except psycopg2.errors.InvalidDatetimeFormat:
            print("Invalid Date format!")
            await ctx.respond(f'{duedate} is not a valid date! Please try the command again with the date format being: MM-DD-YYYY')
        else:
            #commit user input to database
            conn.commit()
            await ctx.respond(f'Noted, {assignment} is due on {duedate} for {section}')


bot.run()