# pyLuci Library

Core library of [The Luci](jonesroothttps://github.com/jonesroot/py-luci), a python based telegram userbot.

[![PyPI - Version](https://img.shields.io/pypi/v/pyLuci?style=round)](https://pypi.org/project/pyLuci)    
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pyLuci?label=DOWNLOADS&style=round)](https://pypi.org/project/pyLuci)    
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github,com/jonesroot/Lucifer-UserBot/graphs/commit-activity)
[![Open Source Love svg2](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github,com/jonesroot/Lucifer-UserBot)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)

# Installation
```bash
pip3 install -U pyLuci
```

# Documentation 
[![Documentation](https://img.shields.io/badge/Documentation-Ayra-blue)](http://ayra.tech/)

# Usage
- Create folders named `plugins`, `addons`, `assistant` and `resources`.   
- Add your plugins in the `plugins` folder and others accordingly.   
- Create a `.env` file with following mandatory Environment Variables
   ```
   API_ID
   API_HASH
   SESSION
   MONGO_URI
   ```
- Check
[`.env.sample`](https://github.com/jonesroot/pyLuci/blob/main/.env.sample) for more details.   
- Run `python3 -m Ayra` to start the bot.   

## Creating plugins
 - ### To work everywhere

```python
@ayra_cmd(
    pattern="start"
)   
async def _(e):   
    await e.eor("Ayra Started!")   
```

- ### To work only in groups

```python
@ayra_cmd(
    pattern="start",
    groups_only=True,
)   
async def _(e):   
    await eor(e, "Ayra Started.")   
```

- ### Assistant Plugins 👇

```python
@asst_cmd("start")   
async def _(e):   
    await e.reply("Ayra Started.")   
```

See more working plugins on [the offical repository](https://github.com/jonesroot/pyLuci)!

> Made with 💕 by [Kynan](https://t.me/kenapanan).    


# License
[![License](https://www.gnu.org/graphics/agplv3-155x51.png)](LICENSE)   
Naya-Userbot is licensed under [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html) v3 or later.

# Credits
* [![Kynan-Devs](https://img.shields.io/static/v1?label=Kynan&message=devs&color=critical)](https://t.me/kenapanan)
* [Lonami](https://github.com/Lonami) for [Telethon](https://github.com/LonamiWebs/Telethon)
