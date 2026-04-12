# nerimity.py

Python API wrapper for Nerimity originating from [Fiiral](https://github.com/F-iiral), maintained by [isanosaurus](https://github.com/isanosaurus)
### **[Nerimity Server](https://nerimity.com/i/493CV)** <br>
For questions, help or anything else feel free to join the **[nerimity.py](https://nerimity.com/i/493CV)** Nerimity server.
# Quick jumps
- **[Current Features](#current-features)** <br>
See the features that the framework currently supports.
- **[Installation](#installation)** <br>
Guide on how to install nerimity.py.
- **[Notice: Prefix Command and Slash Commands](#notice-prefix-commands-and-slash-command)**<br>
Description of what prefix and slash commands are and what differneces there are between them.
- **[Example Bot](#example-commands-bot)** <br>
An example bot you can directly use.
- **[Use-case-examples](#use-case-examples)** <br>
Many various examples on how to use specific functions.

# Current features
#### Command Handling:
- Define and register commands using the @client.command decorator.
- Execute commands with parameters.

### Register event listeners using the @client.listen decorator.
Handle various events such as:
- on_ready
- on_message_create
- on_message_updated
- on_message_deleted
- on_button_clicked
- on_presence_change
- on_reaction_add
- on_member_updated
- on_role_updated
- on_role_deleted
- on_role_created
- on_channel_updated
- on_channel_deleted
- on_channel_created
- on_server_updated
- on_member_join
- on_member_left
- on_server_joined
- on_server_left
- on_friend_request_sent
- on_friend_request_pending
- on_friend_request_accepted
- on_friend_removed
- on_minute_pulse
- on_hour_pulse

#### Message Handling:
- Send messages to channels.
    - add attachments
    - add buttons with custom callback
- Edit and delete messages.
- React and unreact to messages.

#### Attachment Handling:
- Create and upload attachments.
- Deserialize attachments from JSON.

#### Channel Management:
- Update channel information.
- Send messages to channels.
- Get messages from channels.
- Purge messages from channels.
- Deserialize channels from JSON.

#### Context Handling:
- Send messages, remove messages, and react to messages within a command context.

#### Invite Management:
- Create and delete server invites.
- Deserialize invites from JSON.

#### Member Management:
- Follow, unfollow, add friend, remove friend, and send direct messages to members.
- Kick, ban, and unban server members.
- Deserialize members and server members from JSON.

#### Post Management:
- Create, delete, comment on, like, and unlike posts.
- Get comments on posts.
- Deserialize posts from JSON.

#### Role Management:
- Create, update, and delete roles.
- Deserialize roles from JSON.

#### Server Management:
- Get server details and ban list.
- Create, update, and delete channels and roles.
- Create and delete invites.
- Update server members.
- Deserialize servers from JSON.

#### Status Management:
- Change the presence status of the bot.

#### Button Interaction:
- Handle button interactions and send popups.
- Deserialize button interactions from JSON.

#### Permissions:
- Manage user and role permissions.
- Check for specific permissions before executing commands.
- Deserialize permissions from JSON.

# Installation
## Option 1: Install via PyPI (recommended)
```shell
pip install nerimity
```

## Option 2: clone this repository
1. Clone the repository
```shell
git clone https://github.com/isanosaurus/nerimity.py.git
```
2. Copy the `nerimity` folder and insert it into your workspace. It should look like this:
![Image](./readme-assets/directory-view.png)

### Done!

## Notice: Prefix commands and Slash Command
A prefixed command is a command that uses the set prefix in the bot's code. Bots will not react if the message does not start with the prefix.

Slash commands are registered to Nerimity directly and can be shown by typing `/` into the message bar. Registered slash commands will show up there with arguments that need to be provided, if the command needs them.<br>
**Newly** registered slash commands will **only show up after reloading the app**

Except the above stated things there are no differences between prefix and slash command.


## Example commands bot
```py
import nerimity


client = nerimity.Client(
    token="YOUR_BOT_TOKEN",
    prefix='!',
)

# Prefix command -> !ping
@client.command(name="ping")
async def ping(ctx: nerimity.Context):
    await ctx.send("Pong!")

# Slash command -> /test
@client.slash_command(name="test", description="A test slash command")
async def test(ctx: nerimity.Context):
    await ctx.send("Test successful")

@client.listen("on_ready")
async def on_ready(params):
    print(f"Logged in as {client.account.username}")


client.run()
```

## Issues
If you encounter any issues while using the framework feel free to open an [Issue](https://github.com/isanosaurus/nerimity.py).

## Use case examples
### Sending an attachment
```py
@client.command(name="testattachment")
async def testattachment(ctx: nerimity.Context):
    file = await nerimity.Attachment.construct("test.png").upload()
    result = await ctx.send("Test", attachment=file)
```

### Sending buttons with messages
```py
@client.command(name="testbutton")
async def testbutton(ctx: nerimity.Context):
    popup_button = nerimity.Button.construct(label="Popup!", id="popuptestbutton", alert=True)
    async def popup_callback(buttoninteraction: nerimity.ButtonInteraction):
        user = client.get_user(buttoninteraction.userId)
        buttoninteraction.send_popup("Test", f"Hello, {user.username}!")
    await popup_button.set_callback(popup_callback)

    message_button = nerimity.Button.construct(label="Message!", id="messagetestbutton")
    async def message_callback(buttoninteraction: nerimity.ButtonInteraction):
        user = client.get_user(buttoninteraction.userId)
        await ctx.send(f"Hello, {user.username}!")
    await message_button.set_callback(message_callback)
    await ctx.send("Test", buttons=[message_button, popup_button])
```

### Sending an HTML embed
```py
import pathlib
import random
import bs4

wlc_gifs = [
    "https://c.tenor.com/1MfQk9vFF7MAAAAC/tenor.gif",
    "https://c.tenor.com/x8Vc_4yrQuoAAAAC/tenor.gif",
]

@client.command(name="testwelcomeembed")
async def testwelcomeembed(ctx: nerimity.Context):
    # Load the HTML template and modify it using BeautifulSoup
    html_path = pathlib.Path(__file__).parent / "welcome_embed.html"
    soup = bs4.BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")

    # Edit the HTML elements as needed (e.g., set the background image, avatar, and username)
    bg_image = soup.find(class_="bgimage")
    bg_image["src"] = random.choice(wlc_gifs)

    avatar_elem = soup.find(class_="avatar-img")
    avatar_elem["src"] = f"https://cdn.nerimity.com/{ctx.author.avatar}"

    name_elem = soup.find(class_="uname")
    name_elem.string = ctx.author.username

    # Convert the modified HTML to a string and create an embed
    embed = nerimity.Embed.construct(str(soup))
    # Attach the embed to a message and send it
    await ctx.send(f"[@:{ctx.author.id}]", embed=embed)
```

### Creating a post
```py
@client.command(name="createpost")
async def createpost(ctx: nerimity.Context, params):
    content = ""
    for param in params:
        content += param + " "
    await ctx.send("Creating post with text: " + content)
    post = nerimity.Post.create_post(content)
    print(post)
    await ctx.send("Post created.")
```

### Commenting on a post
```py
@client.command(name="comment")
async def comment(ctx: nerimity.Context, params):
    post_id = int(params[0])
    content = ""
    for param in params[1:]:
        content += param + " "
    post = nerimity.Post.get_post(post_id)
    post.create_comment(content)
    await ctx.send("Commented on post.")
```

### Deleting a post
```py
@client.command(name="deletepost")
async def deletepost(ctx: nerimity.Context, params):
    post_id = int(params[0])
    post = nerimity.Post.get_post(post_id)
    post.delete_post()
    await ctx.send("Deleted post.")
```

### Creating a channel
```py
@client.command(name="createchannel")
async def createchannel(ctx: nerimity.Context, params):
    title = params[0]
    permissions = nerimity.Permissions.ChannelPermissions.construct(public=True, send_messages=True, join_voice=True)
    print(permissions)
    everyone_role = ctx.server.get_role(ctx.server.default_role_id)
    new_channel = ctx.server.create_channel(title, type=nerimity.ChannelTypes.SERVER_TEXT)
    await new_channel.set_permissions(permission_integer=permissions, role=everyone_role)
    await ctx.send(f"Channel '{title}' created.")
```

### Creating a role
```py
@client.command(name="createrole")
async def createrole(ctx: nerimity.Context, params):
    name = params[0]
    hide_role = bool(params[1])
    role = ctx.server.create_role()
    role.update_role(name=name, hide_role=hide_role)
    permissions = nerimity.Permissions.RolePermissions.construct(admin=True, manage_roles=True, send_messages=True)
    print(permissions)
    await role.set_permissions(permissions)
    await ctx.send(f"Role '{name}' created.")
```

### Setting for a role in a channel
```py
@client.command(name="setpermissions")
async def setpermissions(ctx: nerimity.Context, params):
    channel_id = int(params[0])
    role_id = int(params[1])
    send_messages = bool(params[2])
    join_voice = bool(params[3])
    
    channel = ctx.server.get_channel(channel_id)
    role = ctx.server.get_role(role_id)
    
    permissions = nerimity.Permissions.ChannelPermissions.construct(send_messages=send_messages, join_voice=join_voice)
    await channel.set_permissions(permission_integer=permissions, role=role)
    
    await ctx.send(f"Permissions set for role '{role.name}' in channel '{channel.name}'.")
```


## Issues
If you encounter any issues while using the framework feel free to open an [Issue](https://github.com/isanosaurus/nerimity.py).