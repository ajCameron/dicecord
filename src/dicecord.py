#!/usr/bin/python3
# vim: ts=4 expandtab

from __future__ import annotations
from typing import List

import random

import discord


class DiscordBot(discord.Client):
    async def on_ready(self) -> None:
        print(f"{self.user} has connected to Discord!")

    async def on_message(self, message: discord.Message) -> None:
        # Don't respond to ourselves.
        if message.author == self.user:
            return

        if message.content.startswith("!roll "):
            await self.roll(message)
            return

    async def roll(self, message: discord.Message) -> None:
        if not isinstance(message.channel, discord.TextChannel):
            print("Attempting to start game in non-text channel")
            return

        [_, *payload] = message.content.split(" ")

        dice = [
            (int(count), int(sides)) for count, sides in [p.split("d") for p in payload]
        ]

        rolls: List[int] = []
        blocks: List[str] = []
        total = 0

        for (count, sides) in dice:
            subtotal = 0

            for _ in range(0, count):
                value = random.randint(1, sides)
                subtotal += value
                rolls.append(value)

            blocks.append(f"{count}d{sides}: {subtotal}")
            total += subtotal

        print(rolls)
        await message.channel.send("Rolling...got " + str(total) + " " + str(blocks))


if __name__ == "__main__":
    with open("discord.token", "r") as token_handle:
        TOKEN = token_handle.read().strip()

    BOT = DiscordBot(max_messages=4096)
    BOT.run(TOKEN)
