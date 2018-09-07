import os
import time
import sqlite3
import csv
import string
import discord
from discord.ext import commands
import aiohttp
import asyncio
import urllib

numbs = {
    "next": "➡",
    "back": "⬅",
    "exit": "❌"
}

class MobileLegends:

	def __init__(self, bot):
		self.bot = bot
	
	async def heroID_from_lineNumber(self, heroName):
		with open(os.path.join("cogs", "heroes.txt"), 'r') as readingFile:
			for (lineNum, line) in enumerate(readingFile):
				if heroName in line.lower().strip():
					return lineNum + 1
			return -1
	
	async def hero_menu(self, ctx, skill_list: list, message: discord.Message=None, page=0, timeout: int=60):
		emb = skill_list[page]
		if not message:
			message =\
				await self.bot.send_message(ctx.message.channel, embed=emb)
			await self.bot.add_reaction(message, "⬅")
			await self.bot.add_reaction(message, "❌")
			await self.bot.add_reaction(message, "➡")
		else:
			message = await self.bot.edit_message(message, embed=emb)
		react = await self.bot.wait_for_reaction(
			message=message, user=ctx.message.author, timeout=timeout,
			emoji=["➡", "⬅", "❌"]
		)
		if react is None:
			await self.bot.remove_reaction(message, "⬅", self.bot.user)
			await self.bot.remove_reaction(message, "❌", self.bot.user)
			await self.bot.remove_reaction(message, "➡", self.bot.user)
			return None
		reacts = {v: k for k, v in numbs.items()}
		react = reacts[react.reaction.emoji]
		await self.bot.clear_reactions(message)
		await self.bot.add_reaction(message, "⬅")
		await self.bot.add_reaction(message, "❌")
		await self.bot.add_reaction(message, "➡")
		if react == "next":
			next_page = 0
			if page == len(skill_list) - 1:
				next_page = 0	# Loop around to the first item
			else:
				next_page = page + 1
			return await self.hero_menu(ctx, skill_list, message=message, page=next_page, timeout=timeout)
		elif react == "back":
			next_page = 0
			if page == 0:
				next_page = len(skill_list) - 1
			else:
				next_page = page - 1
			return await self.hero_menu(ctx, skill_list, message=message, page=next_page, timeout=timeout)
		else:
			return await\
				self.bot.delete_message(message)
				
	@commands.command(pass_context=True)
	async def builds(self, ctx, text:str):
		"""Gets builds from global ranked players. Example: ~builds Miya"""
		heroPID = 0
		heroP = text.lower().strip()
		heroPID = await self.heroID_from_lineNumber(heroP)
		if (heroPID <= 0):
			await self.bot.say("Hero not found. Please check your spelling or mention @Kobe for help")
			return
		theway = os.path.join("cogs", "heroData.db")
		con = sqlite3.connect(theway)
		cur = con.cursor()
		cur.execute("SELECT * FROM authorData WHERE hero=?",(heroP,))
		rows = cur.fetchall()
		embeds = []
		builds = ["i","i","i","i","i"]
		server = self.bot.get_server('239466087958183936')
		for i in range(5):
			thebuild = os.path.join("data", "ml2", "hero"+str(heroPID), "build"+str(i)+".png")
			with open(thebuild,'rb') as img:
				buildmessage = await self.bot.send_file(server.get_channel('400702294892740608'), img)
				builds[i] = str(buildmessage.attachments[0]['url'])
			authorName = str(rows[i][0]).strip()
			worldRank = "World " + str(rows[i][1]).strip()
			winRate = str(rows[i][2]).strip()
			#matchesPlayed = str(rows[i][3]).strip()
			embed = discord.Embed(title=authorName, colour=discord.Colour(0x05EDFF), url="https://m.mobilelegends.com/hero/hero/" + str(heroPID) + "/gear", description=worldRank)
			embed.set_image(url=builds[i])
			embed.set_author(name=heroP.capitalize() + " Builds", url="https://m.mobilelegends.com/hero/hero/" + str(heroPID) + "/gear")
			#embed.add_field(name="Matches Played", value=matchesPlayed, inline=True)
			embed.add_field(name="Win Rate", value=winRate, inline=True)
			embed.set_footer(text="Made possible by Mods of Mobile Legends Fun House ♥", icon_url="https://i.imgur.com/exX6eXU.png")
			embeds.append(embed)
		await self.hero_menu(ctx, embeds, message=None, page=0, timeout=30)

def setup(bot):
	bot.add_cog(MobileLegends(bot))