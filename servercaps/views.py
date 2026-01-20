import discord
from discord.ui import Select, View


class CapsSelect(Select):
    def __init__(self, cog, ctx):
        self.cog = cog
        self.ctx = ctx

        options = [
            discord.SelectOption(label="Overview", emoji="📊", value="overview"),
            discord.SelectOption(label="Server Overview", emoji="🧩", value="server"),
            discord.SelectOption(label="Channels", emoji="📺", value="channels"),
            discord.SelectOption(
                label="Channel Categories", emoji="📁", value="categories"
            ),
            discord.SelectOption(label="Threads", emoji="🧵", value="threads"),
            discord.SelectOption(label="Stage Channels", emoji="🎙", value="stages"),
            discord.SelectOption(label="Audio & Streaming", emoji="🎧", value="audio"),
        ]

        super().__init__(
            placeholder="Select a section",
            options=options,
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(
                "❌ You can't use this menu.", ephemeral=True
            )

        value = self.values[0]

        mapping = {
            "overview": self.cog.build_overview_embed,
            "server": self.cog.build_server_overview_embed,
            "channels": self.cog.build_channel_embed,
            "categories": self.cog.build_category_embed,
            "threads": self.cog.build_thread_embed,
            "stages": self.cog.build_stage_embed,
            "audio": self.cog.build_audio_embed,
        }

        embed = mapping[value](self.ctx)
        await interaction.response.edit_message(embed=embed, view=self.view)


class CapsView(View):
    def __init__(self, cog, ctx):
        super().__init__(timeout=120)
        self.add_item(CapsSelect(cog, ctx))

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if self.message:
            try:
                await self.message.edit(view=self)
            except discord.HTTPException:
                pass
