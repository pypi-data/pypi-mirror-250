[![littxlecord](https://littxlecord.readthedocs.io/en/latest/_static/littxlecord.png)](https://github.com/littxle/littxlecord)

[![](https://img.shields.io/discord/1190258614640836659?label=discord&style=for-the-badge&logo=discord&color=5865F2&logoColor=white)](https://discord.gg/8ew7Sw6Tzy)
[![](https://img.shields.io/pypi/v/littxlecord.svg?style=for-the-badge&logo=pypi&color=yellow&logoColor=white)](https://pypi.org/project/littxlecord/)
[![](https://aschey.tech/tokei/github/littxle/littxlecord?style=for-the-badge)](https://github.com/littxle/littxlecord)

An easy-to-use extension for [Discord.py](https://github.com/Rapptz/discord.py)
and [Pycord](https://github.com/Pycord-Development/pycord) with some utility functions.

## Features
### ✏️ Reduce boilerplate code
- Easy cog management
- Embed templates
- Datetime and file utilities
- Wrapper for [aiosqlite](https://github.com/omnilib/aiosqlite)

### ✨ Error handling
- Automatic error handling for slash commands
- Error webhook reports
- Custom logging

### ⚙️ Extensions
- **Help command** - Automatically generate a help command for your bot
- **Status changer** - Change the bot's status in an interval
- **Blacklist** - Block users from using your bot

## Installing
Python 3.9 or higher is required.
```
pip install littxlecord
```
You can also install the latest version from GitHub. Note that this version may be unstable
and requires [git](https://git-scm.com/downloads) to be installed.
```
pip install git+https://github.com/littxle/littxlecord
```
If you need the latest version in your `requirements.txt` file, you can add this line:
```
littxlecord @ git+https://github.com/littxle/littxlecord
```

## Useful Links
- [Documentation](https://littxlecord.readthedocs.io/) | [Getting started](https://littxlecord.readthedocs.io/en/latest/pages/getting_started.html)
- [Pycord](https://docs.pycord.dev/) | [Discord.py](https://discordpy.readthedocs.io/en/stable/)
- [PyPi](https://pypi.org/project/littxlecord/)

## Examples
- For more examples, see the [example repository](https://github.com/littxle/littxlecord_template)
or the [sample code](https://littxlecord.readthedocs.io/en/latest/examples/examples.html).
- **Note:** It's recommended to [load the token](https://guide.pycord.dev/getting-started/creating-your-first-bot#protecting-tokens) from a `.env` file instead of hardcoding it.
littxlecord can automatically load the token if a `TOKEN` variable is present in the `.env` file.

### Pycord
```py
import littxlecord
import discord

bot = littxlecord.Bot(
    intents=discord.Intents.default()
)

if __name__ == "__main__":
    bot.load_cogs("cogs")  # Load all cogs in the "cogs" folder
    bot.run("TOKEN")
```

### Discord.py
```py
import asyncio
import discord
import littxlecord


class Bot(littxlecord.Bot):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())

    async def setup_hook(self):
        await super().setup_hook()
        await self.tree.sync()


async def main():
    async with Bot() as bot:
        bot.add_help_command()
        bot.load_cogs("cogs")  # Load all cogs in the "cogs" folder
        await bot.start("TOKEN")


if __name__ == "__main__":
    asyncio.run(main())
```

## Contributing
I am always happy to receive contributions. Here is how to do it:
1. Fork this repository
2. Make changes
3. Create a pull request

You can also [create an issue](https://github.com/littxle/littxlecord/issues/new) if you find any bugs.
