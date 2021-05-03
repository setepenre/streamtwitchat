# streamtwitchat

Streams twitch chat

## prerequesites

- python 3

## setup

```bash
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## run

streamtwitchat expects the following environment variables:
- `TWITCH_SERVER`   twitch chat irc url
- `TWITCH_PORT`     twitch chat irc port
- `TWITCH_NICKNAME` lowercase twitch username associated with twitch token
- `TWITCH_TOKEN`    twitch token associated with twitch username, https://dev.twitch.tv/docs/irc/guide
- `TWITCH_CHANNEL`  lowercase twitch channel to join

```bash
$ ./streamtwitchat
< username >
> message
...
```
