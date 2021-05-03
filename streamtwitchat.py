#!/usr/bin/env -S python3 -u
# -*- coding: utf-8 -*-
"""streamtwichat

streams twitch chat to stdout
expects following environment variables:
- TWITCH_SERVER   twitch chat irc url
- TWITCH_PORT     twitch chat irc port
- TWITCH_NICKNAME lowercase twitch username associated with twitch token
- TWITCH_TOKEN    twitch token associated with twitch username
- TWITCH_CHANNEL  lowercase twitch channel to join
"""
import hashlib
import os
import socket
import sys
import textwrap

from emoji import demojize


def dirty_md5(text: str) -> str:
    """dirty_md5.

    :param text:
    :type text: str
    :rtype: str
    """
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def send(sock: socket.socket, cmd: str, arg: str):
    """send.

    :param sock:
    :type sock: socket.socket
    :param cmd:
    :type cmd: str
    :param arg:
    :type arg: str
    """
    sock.send(f"{cmd} {arg}\n".encode("utf-8"))


def recv(sock: socket.socket):
    """recv.

    :param sock:
    :type sock: socket.socket
    """
    return sock.recv(2048).decode("utf-8")


def main():
    """main."""
    server, port, nickname, token, channel = map(
        os.getenv,
        map(
            lambda s: "TWITCH_" + s, ["SERVER", "PORT", "NICKNAME", "TOKEN", "CHANNEL"]
        ),
    )

    sock = socket.socket()
    sock.connect((server, int(port)))

    send(sock, "PASS", f"{token}")
    send(sock, "NICK", f"{nickname}")
    send(sock, "JOIN", f"#{channel}")

    while ":End of /NAMES list" not in (resp := recv(sock)):
        continue

    try:
        while resp := recv(sock):

            if resp.startswith("PING"):
                send(sock, "PONG", "tmi.twitch.tv")

            elif len(resp) > 0:
                [_, head, msg] = resp.split(":", 2)
                [user, _] = head.split("!", 1)

                max_w = 40
                msg = "\n".join(
                    textwrap.wrap(
                        demojize("> " + msg.replace("\r", "").replace("\n", "")),
                        width=max_w,
                    )
                )
                fulltext = f"< {user} >\n{demojize(msg)}\n"
                print(fulltext)

    except KeyboardInterrupt:
        sock.close()
        sys.exit()


if __name__ == "__main__":
    main()
