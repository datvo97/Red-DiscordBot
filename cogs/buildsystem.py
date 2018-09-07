from copy import deepcopy
from datetime import datetime, timedelta
import imghdr
import os
import os.path
import shutil
import time
import re
import string

import aiohttp
try:
    from dateutil.relativedelta import relativedelta
    dateutil_available = True
except:
    dateutil_available = False
import discord
from discord.ext import commands

from .utils.dataIO import dataIO
from .utils import checks, chat_formatting as cf


default_settings = {
    "submissions": {},
    "next_id": 1
}


class BuildSystem:

    """Allows for submission and review of custom builds."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.data_base = "data/reviewbuild"
        self.submissions_path = "data/reviewbuild/submissions.json"
        self.builds = dataIO.load_json(
            os.path.join("data", "mobilelegends", "builds.json"))
        self.heroes = dataIO.load_json(
            os.path.join("data", "mobilelegends", "heroes.json"))
        self.submissions = dataIO.load_json(self.submissions_path)

    def _round_time(self, dt: datetime, round_to: int=60) -> datetime:
        seconds = (dt - dt.min).seconds
        rounding = (seconds + (round_to / 2)) // round_to * round_to
        return dt + timedelta(0, rounding - seconds, -dt.microsecond)

    def _make_readable_delta(self, sub_time: float) -> str:
        sub_dt = self._round_time(datetime.fromtimestamp(sub_time))
        now_dt = self._round_time(datetime.fromtimestamp(time.time()))

        delta = relativedelta(now_dt, sub_dt)
        attrs = ['years', 'months', 'days', 'hours', 'minutes']
        return ", ".join(['%d %s' % (getattr(delta, attr),
                                     (getattr(delta, attr) != 1 and
                                      attr or attr[:-1]))
                          for attr in attrs if (getattr(delta, attr) or
                                                attr == attrs[-1])])
        + " ago"

    def _get_num_waiting_subs(self, server_id: int) -> int:
        return len([sub for sub in
                    list(self.submissions[server_id]["submissions"].values())
                    if sub["status"] == "waiting"])

    async def _send_update_pm(self, server: discord.Server, subid: str):
        sub = self.submissions[server.id]["submissions"][subid]

        user = server.get_member(sub["submitter"])

        if sub["status"] == "rejected":
            await self.bot.send_message(
                user,
                "Your build submission `{}` in {} has been rejected by {}.\n"
                "Here is the reason they gave:{}"
                "As a reminder, here is what your Hero Power looks like:"
                .format(sub["Hero's Name"], server.name,
                        server.get_member(
                    sub["rejector"]).mention,
                    cf.box(sub["reject_reason"])))
            await self.bot.send_file(user, sub["image"])
            await self.bot.send_message(
                user,
                "You may fix the problems with your build and resubmit it,"
                " or contact the rejector with any questions.")
        elif sub["status"] == "approved":
            await self.bot.send_message(
                user,
                "Your build submission `{}` in {} has been approved by {}."
                .format(sub["Hero's Name"], server.name,
                        server.get_member(sub["approver"]).mention))

    @checks.admin_or_permissions(kick_members=True)
    async def _approve_build(self, ctx: commands.Context, subid: str):
        server = ctx.message.server
        sub = self.submissions[ctx.message.server.id]["submissions"][subid]

        sub["status"] = "approved"
        sub["approver"] = ctx.message.author.id
        sub["approve_time"] = time.time()

        dataIO.save_json(self.submissions_path, self.submissions)

        author = ctx.message.author
        await self.bot.say("Enter the Hero Power ")
        msg = await self.bot.wait_for_message(author=author, timeout=30)
        if msg is None:
            await self.bot.say("No hero power provided!")
            return
        hp = msg.content
        msg = None
        await self.bot.say("Enter the Global Rank ")
        msg = await self.bot.wait_for_message(author=author, timeout=30)
        if msg is None:
            await self.bot.say("No global rank provided!")
            return
        gr = msg.content
        msg = None
        await self.bot.say("Enter the Local Rank ")
        msg = await self.bot.wait_for_message(author=author, timeout=30)
        if msg is None:
            await self.bot.say("No local rank provided!")
            return
        lr = msg.content
        msg = None

        await self.bot.say(cf.box(
                    ".. {}{}Build {}'s {} Build \n"
                    "Hero Power: {}\nGlobal Rank: {}\nLocal Rank: {}\n"
                    "Build: {}\n"
                    .format(sub["Hero's Name"], sub["id"], server.get_member(sub["submitter"]).display_name, sub["Hero's Name"], hp, gr, lr, sub["Build"])))

        await self.bot.say(cf.box(
                    "... {}{}Build\n"
                    .format(sub["Hero's Name"], sub["id"])))

        await self.bot.say(cf.box(
                    "!addbuild {} {} {} \n"
                    .format(sub["Hero's Name"], hp, "[Insert the (bolded) build id number]")))

        await self._send_update_pm(ctx.message.server, subid)

    @checks.admin_or_permissions(kick_members=True)
    async def _reject_build(self, ctx: commands.Context, subid: str,
                            reason: str):

        sub = self.submissions[ctx.message.server.id]["submissions"][subid]
        sub["status"] = "rejected"
        sub["rejector"] = ctx.message.author.id
        sub["reject_time"] = time.time()
        sub["reject_reason"] = reason

        dataIO.save_json(self.submissions_path, self.submissions)

        await self._send_update_pm(ctx.message.server, subid)

    @commands.command(pass_context=True, no_pm=True, name="submitbuild")
    async def _submitbuild(self, ctx: commands.Context):
        """Submits a new build for review.

        Should include an image as a Discord attachment
        """

        await self.bot.type()
        await self.bot.say("Analyzing your screenshot, please wait...")
        attach = ctx.message.attachments
        url = ""
        if attach:
            url = attach[0]["url"]
        else:
            await self.bot.reply(cf.error(
            "You must provide a Discord attachment"))
            await self.bot.say("https://imgur.com/kn6vY6F")
            return

        server = ctx.message.server
        if server.id not in self.submissions:
            self.submissions[server.id] = deepcopy(default_settings)
            dataIO.save_json(self.submissions_path, self.submissions)
        author = ctx.message.author
        await self.bot.say("Enter the name of the hero ")
        msg = await self.bot.wait_for_message(author=author, timeout=30)
        if msg is None:
            await self.bot.say("No name provided!")
            return
        name = msg.content
        msg = None
        heroBuild = ""
        await self.bot.say(name)
        await self.bot.say("Enter the build ")
        msg = await self.bot.wait_for_message(author=author, timeout=60)
        if msg is None:
            await self.bot.say("No build provided!")
            return
        heroBuild = msg.content
        heroBuild = heroBuild.replace("1", "")
        heroBuild = heroBuild.replace("2", "")
        heroBuild = heroBuild.replace("3", "")
        heroBuild = heroBuild.replace("4", "")
        heroBuild = heroBuild.replace("5", "")
        heroBuild = heroBuild.replace("6", "")
        heroBuild = heroBuild.replace("7", "")
        heroBuild = heroBuild.replace("8", "")
        heroBuild = heroBuild.replace("9", "")
        heroBuild = heroBuild.replace("0", "")
        heroBuild = heroBuild.replace("<", "")
        heroBuild = heroBuild.replace(">", "")
        msg = None
        await self.bot.say(heroBuild)

        if server.id not in self.submissions:
            self.submissions[server.id] = deepcopy(default_settings)
            dataIO.ssubave_json(self.submissions_path, self.submissions)

        new_build_id = str(self.submissions[server.id]["next_id"])
        self.submissions[server.id]["next_id"] += 1
        dataIO.save_json(self.submissions_path, self.submissions)

        path = "{}/{}".format(self.data_base, server.id)
        if not os.path.exists(path):
            os.makedirs(path)

        path += "/" + new_build_id
        os.makedirs(path)

        path += "/" + attach[0]["filename"]

        async with aiohttp.get(url) as new_build_file:
            f = open(path, "wb")
            f.write(await new_build_file.read())
            f.close

        if imghdr.what(path) not in ["png", "jpeg", "jpg"]:
            await self.bot.reply(
                cf.error("Only JPG and PNG images are supported."))
            shutil.rmtree(
                "{}/{}/{}".format(self.data_base, server.id, new_build_id))
            return


        self.submissions[server.id]["submissions"][new_build_id] = {
            "id": new_build_id,
            "status": "waiting",
            "submitter": ctx.message.author.id,
            "Hero's Name": name,
            "Build" : heroBuild,
            "image": path,
            "submit_time": time.time(),
            "approver": None,
            "approve_time": None,
            "rejector": None,
            "reject_time": None,
            "reject_reason": None
        }
        dataIO.save_json(self.submissions_path, self.submissions)

        await self.bot.reply(cf.info(
            "Submission successful, ID {}."
            " You can check its status with `{}checkbuild {}`."
            .format(new_build_id, ctx.prefix, new_build_id)))

    @commands.command(pass_context=True)
    async def listbuilds(self, ctx, hName: str):
        """List builds for specified hero"""
        server = ctx.message.server
        hhname = ""
        hhname = hName.lower()
        events = []
        try:
            self.heroes[hhname]
        except KeyError:
            await self.bot.say("Cannot find info for that hero, please check spelling or wait for the hero to be released on NA servers.")
            return
        for hero in self.heroes[hhname]:
            embeddd=discord.Embed(title=hero["Role"], description="Speciality: " + hero["Speciality"], color=0x09dafb)
            embeddd.set_author(name=hero["Name"] + " Builds", url=hero["source_url"], icon_url=hero["icon_url"])
            embeddd.set_thumbnail(url=hero["profile_url"])
            embeddd.add_field(name="To view the build, Type !showbuild [Build ID]", value="Example: !showbuild 69", inline=False)
            for buld in self.builds[hhname]:
                embeddd.add_field(name="Hero Power: " + buld["hero_power"], value="Build ID: " + buld["bid"], inline=True)
            embeddd.set_footer(text=hero["members_credit"])
            await self.bot.say(embed=embeddd)

    @checks.admin_or_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def addbuild(self, ctx, heroName: str, heroPower: str, build_id: str):
        """Adds the specified build"""
        hero_name = ""
        hero_name = heroName.lower()

        try:
            self.builds[hero_name]
        except KeyError:
            await self.bot.say("Cannot find info for that hero, please check spelling or wait for the hero to be released on NA servers.")
            return

        new_build = {
            "hero_power": heroPower,
            "bid": build_id
        }
        self.builds[hero_name].append(new_build)
        dataIO.save_json(os.path.join("data", "mobilelegends", "builds.json"), self.builds)

        await self.bot.say("Hero: " + hero_name + "\nBuild ID: " + build_id + "\nHero Power: " + heroPower + "\nBuild has been added.")

    @checks.admin_or_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def removebuild(self, ctx, heroName: str, build_id: str):
        """Removes the specified build"""
        server = ctx.message.server
        hero_name = ""
        hero_name = heroName.lower()

        try:
            self.builds[hero_name]
        except KeyError:
            await self.bot.say("Cannot find info for that hero, please check spelling or wait for the hero to be released on NA servers.")
            return

        to_remove =\
            [event for event in self.builds[hero_name] if event["bid"] == build_id]
        if len(to_remove) == 0:
            await self.bot.say("No build to remove!")
        else:
            self.builds[hero_name].remove(to_remove[0])
            dataIO.save_json(
                os.path.join("data", "mobilelegends", "builds.json"),
                self.builds)
            await self.bot.say("Removed the specified build.")

    @commands.command(pass_context=True, no_pm=True, name="checkbuild")
    async def _checkbuild(self, ctx: commands.Context,
                          submission_id: str):
        """Check the status of a submitted build."""

        await self.bot.type()

        server = ctx.message.server
        author = ctx.message.author

        if submission_id not in self.submissions[server.id]["submissions"]:
            self.bot.reply(cf.error(
                "Submission with ID {} not found.")).format(submission_id)
            return

        sub = self.submissions[server.id]["submissions"][submission_id]
        status = ""
        extra = ""
        if sub["status"] == "waiting":
            status = "Awaiting review."
        elif sub["status"] == "approved":
            status = "Approved."
            extra = "\nApproved by: {}\nApproved: {}".format(
                server.get_member(sub["approver"]).display_name,
                sub["approve_time"])
        elif sub["status"] == "rejected":
            status = "Rejected."
            extra = "\nRejected by: {}\nRejected: {}\n"
            "Rejection reason: {}".format(
                server.get_member(sub["rejector"]).display_name,
                sub["reject_time"], sub["reject_reason"])

        await self.bot.reply(cf.box(
            "Submission ID: {}\nSubmitted by: {}\nSubmitted: {}\n"
            "Hero's Name: {}\nBuild: {}\nStatus: {}{}".format(
                submission_id, server.get_member(
                    sub["submitter"]).display_name,
                self._make_readable_delta(sub["submit_time"]),
                sub["Hero's Name"], sub["Build"], status, extra)))

    @commands.command(pass_context=True, no_pm=True, name="reviewbuild")
    @checks.admin_or_permissions(kick_members=True)
    async def _reviewbuild(self, ctx: commands.Context):
        """Review build submissions."""

        server = ctx.message.server
        if server.id not in self.submissions:
            self.submissions[server.id] = deepcopy(default_settings)
            dataIO.save_json(self.submissions_path, self.submissions)

        if self._get_num_waiting_subs(server.id) == 0:
            await self.bot.reply("There are no submissions awaiting review.")
            return

        approved = 0
        rejected = 0
        skipped = 0

        for subid, sub in self.submissions[server.id]["submissions"].items():
            if sub["status"] == "waiting":
                await self.bot.say(cf.box(
                    "Submission ID: {}\nSubmitted by: {}\nSubmitted: {}\n"
                    "Hero's Name: {}\nBuild: {}\n"
                    .format(subid,
                            server.get_member(sub["submitter"]).display_name,
                            self._make_readable_delta(sub["submit_time"]),
                            sub["Hero's Name"], sub["Build"])))
                await self.bot.upload(sub["image"])
                await self.bot.reply(cf.question(
                    "What is your decision for this build? You may say"
                    " \"approve\" to add it, \"reject <reason>\" to refuse it,"
                    " or \"skip\" to postpone judgment. You may also say"
                    " \"exit\" to exit the review process."))

                decision = None
                while not decision:
                    r = await self.bot.wait_for_message(
                        timeout=30, channel=ctx.message.channel,
                        author=ctx.message.author)
                    if r is None:
                        await self.bot.say("No response provided!")
                        return
                    resp = r.content.strip().lower().split()
                    if resp[0] not in ("approve", "reject", "skip", "exit"):
                        await self.bot.reply(cf.warning(
                            "Please say either \"approve\","
                            " \"reject <reason>\", or \"skip\"."))
                    elif resp[0] == "reject" and len(resp) == 1:
                        await self.bot.reply(cf.warning(
                            "If you reject a build,"
                            " you must provide a reason."))
                    else:
                        decision = resp

                if decision[0] == "approve":
                    try:
                        await self._approve_build(ctx, subid)
                    except discord.HTTPException as e:
                        await self.bot.reply(
                            cf.error("An error occurred while creating"
                                     " the new build: {}".format(cf.box(e))))
                        continue
                    await self.bot.reply(
                        cf.info("Submission {} approved and added. "
                                .format(subid)))
                    approved += 1
                elif decision[0] == "reject":
                    reason = " ".join(decision[1:])
                    await self._reject_build(ctx, subid, reason)
                    await self.bot.reply(
                        cf.info("Submission {} rejected.").format(subid))
                    rejected += 1
                elif decision[0] == "skip":
                    await self.bot.reply(
                        cf.info("Submission {} skipped.".format(subid)))
                    skipped += 1
                elif decision[0] == "exit" or decision is None:
                    break

        await self.bot.reply(cf.info(
            "Exiting review process.\n"
            "This session: {} approved, {} rejected, {} skipped.\n"
            .format(approved, rejected, skipped))),


def check_folders():
    if not os.path.exists("data/reviewbuild"):
        print("Creating data/reviewbuild directory...")
        os.makedirs("data/reviewbuild")


def check_files():
    f = "data/reviewbuild/submissions.json"
    if not dataIO.is_valid_json(f):
        print("Creating data/reviewbuild/submissions.json...")
        dataIO.save_json(f, {})


def setup(bot: commands.Bot):
    check_folders()
    check_files()

    if dateutil_available:
        bot.add_cog(BuildSystem(bot))
    else:
        raise RuntimeError("You need to install `python-dateutil`: `pip install python-dateutil`.")
