import discord
from discord.ui import View, Button


class CapsButton(Button):
    def __init__(self, *, label, emoji, style, value, cog, ctx):
        super().__init__(label=label, emoji=emoji, style=style)
        self.value = value
        self.cog = cog
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(
                "❌ You can't use these buttons.", ephemeral=True
            )

        mapping = {
            "overview": self.cog.build_overview_embed,
            "server": self.cog.build_server_overview_embed,
            "channels": self.cog.build_channel_embed,
            "categories": self.cog.build_category_embed,
            "threads": self.cog.build_thread_embed,
            "stages": self.cog.build_stage_embed,
            "audio": self.cog.build_audio_embed,
        }

        embed = mapping[self.value](self.ctx)
        await interaction.response.edit_message(embed=embed, view=self.view)


class CapsView(View):
    def __init__(self, cog, ctx):
        super().__init__(timeout=120)

        buttons = [
            ("Overview", "📊", discord.ButtonStyle.primary, "overview"),
            ("Server", "🧩", discord.ButtonStyle.secondary, "server"),
            ("Channels", "📺", discord.ButtonStyle.secondary, "channels"),
            ("Categories", "📁", discord.ButtonStyle.secondary, "categories"),
            ("Threads", "🧵", discord.ButtonStyle.secondary, "threads"),
            ("Stages", "🎙", discord.ButtonStyle.secondary, "stages"),
            ("Audio", "🎧", discord.ButtonStyle.secondary, "audio"),
        ]

        for label, emoji, style, value in buttons:
            self.add_item(
                CapsButton(
                    label=label,
                    emoji=emoji,
                    style=style,
                    value=value,
                    cog=cog,
                    ctx=ctx,
                )
            )

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

        if self.message:
            try:
                await self.message.edit(view=self)
            except discord.HTTPException:
                pass
