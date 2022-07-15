## NobetciEczaneRobot

🇹🇷 Türkiye'deki Nöbetçi Eczaneleri Listeleyen Bot

🇬🇧 A Bot That Listing Pharmacies on Duty in Turkey

Demo in telegram: [@NobetciEczaneRobot](https://t.me/NobetciEczaneRobot)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/HuzunluArtemis/NobetciEczaneRobot)

## Features

- Task Quee
- Auth users or public
- 8 Farklı API
- Force Subscribe
- Server stats & Dyno usage for heroku. Use: /stats
- Logger, Pinger, Shell executer

## Bot Commands (Set in [@BotFather](https://t.me/BotFather))

```
start - bot help
ping - check bot online status
stats - bot statistics
shell - execute shell command ❗ admin only
log - send bot logs ❗ admin only
```

## Environment Variables

- `BOT_TOKEN`: Telegram Bot Token. Example: `3asd2a2sd32:As56das65d2as:ASd2a6s3d26as`
- `APP_ID`: Telegram App ID. Example: `32523453`
- `API_HASH`: Telegram Api Hash. Example: `asdasdas6d265asd26asd6as1das`
- `AUTH_IDS`: Auth only some groups or users. If you want public, leave it empty or give `0`. Example: `-100656 56191 -10056561`
- `OWNER_ID`: Bot's owner id. Send `/id` to `t.me/MissRose_bot` in private to get your id.
- `USING_API`: Give one of them:
    - `CollectApi`: Requires `API_KEY` variable. You can get from [here](https://collectapi.com/tr/). Fast.
    - `NosyApi`: Requires `API_KEY` variable. You can get from [here](https://www.nosyapi.com/api/nobetci-eczane). Fast.
    - `EczaneleriOrg`: Free alternative. Fast.
    - `EczanelerGenTr`: Free alternative. Fast.
    - `HastanemyanimdaCom`: Free alternative. Fast.
    - `EczaneleriNet`: Free alternative. Fast.
    - `TrNobetcieczaneCom`: Free alternative. Fast.
    - `EczaIo`: Free alternative. Slow because using selenium. If you on local, install google-chrome and setup chromedriver first.
- `CHROMEDRIVER_PATH`: For sselenium apis. Not required for others. Simply dont fill.
- `GOOGLE_CHROME_BIN`: For sselenium apis. Not required for others. Simply dont fill.
- `HEROKU_API_KEY`: For dyno usage in /stats - Optional.
- `HEROKU_APP_NAME`: For dyno usage in /stats - Optional.
- `CHANNEL_OR_CONTACT`: your users contact link. give your username. example: HuzunluArtemis
- `FORCE_SUBSCRIBE_CHANNEL`: forcesub channel. optional. give channel id like `-1006616516165` or channel username like `HuzunluArtemis`
- Dont use heroku-20 or heroku-18. Use container. Use button.
- `JOIN_CHANNEL_STR`: Join channel warning string. See `config.py`.
- `YOU_ARE_BANNED_STR`: Banned user string. See `config.py`.
- `JOIN_BUTTON_STR`: Join button string. See `config.py`.

## Lisans

![](https://www.gnu.org/graphics/gplv3-127x51.png)

You can use, study share and improve it at your will. Specifically you can redistribute and/or modify it under the terms of the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.html) as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
