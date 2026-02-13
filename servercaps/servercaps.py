import discord
from redbot.core import commands

from .views import CapsView


class ServerCaps(commands.Cog):
    """Server limits viewer with dropdown UI"""

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(name="servercaps", aliases=["caps", "serverlimits"])
    async def server_caps(self, ctx: commands.Context):
        """Show server limits with interactive dropdown"""
        view = CapsView(self, ctx)
        embed = self.build_overview_embed(ctx)
        message = await ctx.send(embed=embed, view=view)
        view.message = message

    def build_overview_embed(self, ctx: commands.Context) -> discord.Embed:
        guild = ctx.guild
        tier = guild.premium_tier
        boosts = guild.premium_subscription_count or 0

        emoji_limits = {0: 50, 1: 100, 2: 150, 3: 250}
        sticker_limits = {0: 5, 1: 15, 2: 30, 3: 60}
        soundboard_slots = {0: 8, 1: 24, 2: 36, 3: 48}
        upload = {
            0: "10 MB",
            1: "10 MB",
            2: "50 MB",
            3: "100 MB",
        }

        static_emojis = len([e for e in guild.emojis if not e.animated])
        animated_emojis = len([e for e in guild.emojis if e.animated])

        embed = discord.Embed(
            title="📊 Server Overview",
            description="General server usage & limits",
            color=discord.Color.blurple(),
        )
        embed.add_field(
            name="🚀 Boost Status",
            value=(f"Tier: **{tier}**\nBoosts: **{boosts}**"),
            inline=True,
        )

        embed.add_field(name="🎭 Roles", value=f"{len(guild.roles)} / 250", inline=True)

        embed.add_field(
            name="📺 Channels",
            value=(
                f"**{len(guild.channels)} / 500**\n"
                f"📁 Categories: **{len(guild.categories)}**\n"
                f"💬 Text: **{len(guild.text_channels)}**\n"
                f"🗂 Forums: **{len(guild.forums)}**\n"
                f"🔊 Voice: **{len(guild.voice_channels)}**\n"
                f"🎙 Stage: **{len(guild.stage_channels)}**"
            ),
            inline=True,
        )

        embed.add_field(
            name="🎚 Soundboard Slots",
            value=(
                f"Used: **{len(guild.soundboard_sounds)}**\n"
                f"Total: **{str(soundboard_slots[tier])}**\n"
            ),
            inline=True,
        )

        embed.add_field(
            name="🧵 Threads", value=f"{len(guild.threads)} / 1000", inline=True
        )
        embed.add_field(name="📤 Upload Limit", value=upload[tier], inline=True)

        embed.add_field(
            name="🖼 Stickers",
            value=(
                f"Used: **{len(guild.stickers)}**\n"
                f"Total: **{sticker_limits[tier]}**\n"
                f"Left: **{sticker_limits[tier] - len(guild.stickers)}**"
            ),
            inline=True,
        )
        embed.add_field(
            name="😄 Static Emojis",
            value=(
                f"Used: **{static_emojis}**\n"
                f"Limit: **{emoji_limits[tier]}**\n"
                f"Left: **{emoji_limits[tier] - static_emojis}**"
            ),
            inline=True,
        )

        embed.add_field(
            name="✨ Animated Emojis",
            value=(
                f"Used: **{animated_emojis}**\n"
                f"Limit: **{emoji_limits[tier]}**\n"
                f"Left: **{emoji_limits[tier] - animated_emojis}**"
            ),
            inline=True,
        )

        embed.set_footer(text="Use the dropdown below to view more details")
        return embed

    def build_channel_embed(self, ctx: commands.Context) -> discord.Embed:
        guild = ctx.guild

        embed = discord.Embed(
            title="📺 Channel Breakdown",
            description="Detailed channel counts",
            color=discord.Color.green(),
        )

        embed.add_field(
            name="📁 Categories", value=str(len(guild.categories)), inline=True
        )

        embed.add_field(
            name="💬 Text Channels", value=str(len(guild.text_channels)), inline=True
        )

        embed.add_field(
            name="🔊 Voice Channels", value=str(len(guild.voice_channels)), inline=True
        )

        embed.add_field(
            name="🎤 Stage Channels", value=str(len(guild.stage_channels)), inline=True
        )

        embed.add_field(
            name="📦 Total Channels", value=str(len(guild.channels)), inline=False
        )

        embed.set_footer(text="Maximum channels per server: 500")
        return embed

    def build_stage_embed(self, ctx):
        tier = ctx.guild.premium_tier

        video_seats = {
            0: "50",
            1: "50",
            2: "150",
            3: "300 (+30 per boost past 14)",
        }

        embed = discord.Embed(
            title="🎙 Stage Channel Limits",
            description="Stage-specific caps",
            color=discord.Color.purple(),
        )

        embed.add_field(name="👥 Users (No Stream/Video)", value="10,000", inline=True)
        embed.add_field(name="🎮 Activities on Stages", value="None", inline=True)
        embed.add_field(
            name="📹 Video Stage Seats", value=video_seats[tier], inline=True
        )
        embed.add_field(name="📺 Stage Channels", value="No limit", inline=True)
        embed.add_field(name="✋ Hands Raised", value="No limit", inline=True)
        embed.add_field(name="🖥 Shared Screens", value="1", inline=True)
        embed.add_field(
            name="💬 Messages per min/hour",
            value="No limit (unless slow mode)",
            inline=False,
        )

        return embed

    def build_server_and_audio_embed(self, ctx: commands.Context) -> discord.Embed:
        guild = ctx.guild
        tier = guild.premium_tier

        upload = {
            0: "10 MB",
            1: "10 MB",
            2: "50 MB",
            3: "100 MB",
        }

        soundboard_slots = {0: 8, 1: 24, 2: 36, 3: 48}
        stream_quality = {
            0: "720p @ 30fps",
            1: "720p @ 60fps",
            2: "1080p @ 60fps",
            3: "1080p @ 60fps",
        }
        audio_quality = {0: "96 kbps", 1: "128 kbps", 2: "256 kbps", 3: "384 kbps"}
        go_live_quality = {
            0: "720p @ 60fps",
            1: "720p @ 60fps",
            2: "1080p @ 60fps",
            3: "1080p @ 60fps",
        }

        embed = discord.Embed(
            title="🧩 Server Overview",
            description=f"Boost Tier **{tier}** — server features and voice limits",
            color=discord.Color.teal(),
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        embed.add_field(name="📤 Upload Limit", value=upload[tier], inline=True)
        embed.add_field(
            name="🔗 Vanity URL",
            value="Yes (25 characters)" if tier == 3 else "No",
            inline=True,
        )
        embed.add_field(
            name="🖼 Animated Server Icon",
            value="Yes" if tier >= 1 else "No",
            inline=True,
        )

        banner = ["No", "No", "Static", "Animated"][tier]
        embed.add_field(name="🎨 Server Banner", value=banner, inline=True)
        embed.add_field(
            name="🎭 Custom Role Icons", value="Yes" if tier >= 2 else "No", inline=True
        )

        embed.add_field(name="\u200b", value="\u200b", inline=False)

        embed.add_field(name="🔊 Audio Quality", value=audio_quality[tier], inline=True)
        embed.add_field(
            name="🎚 Soundboard Slots",
            value=(
                f"Used: **{len(guild.soundboard_sounds)}**\n"
                f"Total: **{str(soundboard_slots[tier])}**\n"
            ),
            inline=True,
        )
        embed.add_field(
            name="📡 Stream Quality", value=stream_quality[tier], inline=True
        )
        embed.add_field(
            name="📺 Go Live Stream Quality", value=go_live_quality[tier], inline=True
        )

        if tier == 0:
            embed.add_field(name="👥 Go Live Audience", value="50 members", inline=True)
            embed.add_field(
                name="🖥 Screenshare (No Camera)", value="50 members", inline=True
            )
            embed.add_field(
                name="📹 Voice Channel Video", value="25 members", inline=True
            )

        embed.set_footer(
            text="Audio limits are tier-based • Some limits are fixed by Discord"
        )

        return embed

    def build_thread_embed(self, ctx):
        embed = discord.Embed(title="🧵 Thread Limits", color=discord.Color.gold())

        embed.add_field(
            name="🧵 Threads", value=str(len(ctx.guild.threads)), inline=True
        )
        embed.add_field(name="👥 Members per Thread", value="1000", inline=True)
        embed.add_field(name="🎭 Roles Mentioned (Private)", value="10", inline=True)

        return embed

    def build_category_embed(self, ctx):
        embed = discord.Embed(
            title="📁 Channel & Category Limits", color=discord.Color.blue()
        )

        embed.add_field(name="📺 Total Channels (All Types)", value="500", inline=True)
        embed.add_field(name="📁 Channels per Category", value="50", inline=True)

        return embed

    def build_icon_embed(self, ctx: commands.Context) -> discord.Embed:
        guild = ctx.guild
        embed = discord.Embed(
            title=f"🖼 {guild.name}'s Icon",
            color=discord.Color.blurple(),
        )

        if guild.icon:
            embed.set_image(url=guild.icon.url)
        else:
            embed.description = "No server icon set."

        return embed

    def build_banner_embed(self, ctx: commands.Context) -> discord.Embed:
        guild = ctx.guild
        embed = discord.Embed(
            title=f"🎨 {guild.name}'s Banner",
            color=discord.Color.blurple(),
        )

        if guild.banner:
            embed.set_image(url=guild.banner.url)
        else:
            embed.description = "No server banner set."

        return embed
