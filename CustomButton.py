import discord
from discord.ext import commands
from discord import app_commands
import CustomFunctions
from typing import List, Optional
from db.DbMongoManager import SnipeMessage, SnipeChannelInfo, PreDeleteAttachmentsInfo
import asyncio


class CustomReportButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Tiếp Nhận Báo Cáo", style=discord.ButtonStyle.primary, custom_id="resolve_report_button")
    async def button_callback(self,interaction: discord.Interaction, button: discord.ui.Button):
        # Xoá button khỏi embed cũ
        self.clear_items()
        await interaction.response.edit_message(view=self)
        # Send a new message
        await interaction.followup.send(f"{interaction.user.mention} đã nhận report và giải quyết! Nếu có gì quá phức tạp, vui lòng liên hệ cấp cao hơn, hoặc Server Master nếu cần thiết.")

class CustomTruthDareComboButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Sự thật", style=discord.ButtonStyle.primary, custom_id="truth_button")
    async def buttonTruth_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        content = CustomFunctions.get_random_response("OnTruthChallenge.txt")
        channel = interaction.channel
        # Create embed object
        embed = discord.Embed(title=f"", description=f"Lượt chơi của: {interaction.user.mention}", color=0x03F8FC)
        embed.add_field(name=f"", value="*Loại trò chơi: Sự Thật*", inline=False)
        embed.add_field(name=f"", value="___________________", inline=False)
        embed.add_field(name=f"{content}", value=f"", inline=False)
        view = CustomTruthDareComboButtons()
        await interaction.followup.send(f"Bạn đã chọn Sự Thật.", ephemeral=True)
        await channel.send(embed=embed, view= view)
        
    @discord.ui.button(label="Thách thức", style=discord.ButtonStyle.secondary, custom_id="dare_button")
    async def buttonDare_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        content = CustomFunctions.get_random_response("OnDareChallenge.txt")
        channel = interaction.channel
        # Create embed object
        embed = discord.Embed(title=f"", description=f"Lượt chơi của: {interaction.user.mention}", color=0x03F8FC)
        embed.add_field(name=f"", value="*Loại trò chơi: Thách Thức*", inline=False)
        embed.add_field(name=f"", value="___________________", inline=False)
        embed.add_field(name=f"{content}", value=f"", inline=False)
        view = CustomTruthDareComboButtons()
        await interaction.followup.send(f"Bạn đã chọn Thách Thức.", ephemeral=True)
        await channel.send(embed=embed, view= view)


class PaginationView(discord.ui.View):
    def __init__(self, bot, interaction: discord.Interaction, items: List[SnipeMessage], per_page = 1, timeout: float = 60):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.interaction = interaction
        self.items = items
        self.per_page = per_page
        self.current_page = 1
        self.max_pages = len(items) // per_page + (len(items) % per_page > 0)
        self.embed = discord.Embed(title="Snipe Messages", description=f"", color=0x03F8FC)
        self.seconds_left = timeout
        self.list_attachtment =[]
        self.discord_message: discord.Message = None
        message = self.items[0]
        if message:
            modern_time = message.deleted_date.strftime(f"%d/%m/%Y %H:%M")
            user = interaction.guild.get_member(message.author_id)
            self.embed.set_thumbnail(url=user.avatar.url)
            self.embed.add_field(name=f"", value=f"**Channel {interaction.channel.mention}. Tin nhắn của user: {user.mention}, username: {user.name}**", inline=False)
            if message.user_message_content != "" and message.user_message_content != None:
                self.embed.add_field(name=f"", value=f"{message.user_message_content}", inline=False)
            if message.user_attachments != None and len(message.user_attachments)>0:
                self.embed.add_field(name=f"", value=f"*________________*", inline=False)
                self.embed.add_field(name=f"Tin nhắn chứa {len(message.user_attachments)} Attachments.", value="", inline=False)
                for index, attachments in enumerate(message.user_attachments):
                    self.embed.add_field(name="", value=f"{index+1}. {attachments.url}", inline=False)
            self.embed.add_field(name=f"", value=f"*________________*", inline=False)
            self.embed.add_field(name=f"", value=f"Thời gian xoá: {modern_time}", inline=True)
            self.embed.add_field(name=f"", value=f"User Invoke: {interaction.user.id}", inline=True)
        self.embed.set_footer(text=f"Trang thứ {self.current_page}/{self.max_pages}")
        
    async def update_embed(self, interaction: discord.Interaction):
        actual_index = self.current_page - 1
        message = self.items[actual_index]
        if message:
            modern_time = message.deleted_date.strftime(f"%d/%m/%Y %H:%M")
            user = interaction.guild.get_member(message.author_id)
            new_embed = discord.Embed(title="Snipe Messages", description=f"", color=0x03F8FC)
            new_embed.set_thumbnail(url=user.avatar.url)
            new_embed.add_field(name=f"", value=f"**Channel {interaction.channel.mention}. Tin nhắn của user: {user.mention}, username: {user.name}**", inline=False)
            file = None
            temp_files = []
            if message.user_message_content != "" and message.user_message_content != None:
                new_embed.add_field(name=f"", value=f"{message.user_message_content}", inline=False)
            if message.user_attachments!= None and len(message.user_attachments)>0:
                new_embed.add_field(name=f"", value=f"*________________*", inline=False)
                new_embed.add_field(name=f"Tin nhắn chứa {len(message.user_attachments)} Attachments.", value="", inline=False)
                for index, attachments in enumerate(message.user_attachments):
                    new_embed.add_field(name="", value=f"{index+1}. {attachments.url}", inline=False)
                    file = await CustomFunctions.get_attachment_file_from_url(url= attachments.url, content_type= attachments.content_type)
                    if file != None:
                        temp_files.append(file)
            new_embed.add_field(name=f"", value=f"*________________*", inline=False)
            new_embed.add_field(name=f"", value=f"Thời gian xoá: {modern_time}", inline=True)
            new_embed.add_field(name=f"", value=f"User Invoke: {interaction.user.id}", inline=True)
            new_embed.set_footer(text=f"Trang thứ {self.current_page}/{self.max_pages}")
            self.embed = new_embed
            self.list_attachtment = temp_files
        await interaction.response.edit_message(embed=self.embed, view=self, attachments=temp_files)

    async def countdown(self):
        while self.seconds_left > 0:
            self.seconds_left -= 1
            self.embed.description = f"Thời gian còn lại: {self.seconds_left} giây"
            await self.discord_message.edit(embed=self.embed, view=self, attachments = self.list_attachtment)
            await asyncio.sleep(1)
        await self.disable_buttons()

    async def disable_buttons(self):
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True 
        self.embed.description = "Đã hết hạn snipe. Vui lòng /snipe lại nếu cần."
        await self.discord_message.edit(embed=self.embed, view=self, attachments = self.list_attachtment)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        if self.discord_message:
            await self.discord_message.edit(embed=self.embed, view=self, attachments = self.list_attachtment)

    
    @discord.ui.button(label="Trước", style=discord.ButtonStyle.secondary, disabled=True, custom_id="prev")
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 1:
            self.current_page -= 1
            self.children[0].disabled = self.current_page == 1
            self.children[1].disabled = False
            await self.update_embed(interaction)

    @discord.ui.button(label="Sau", style=discord.ButtonStyle.primary, custom_id="next")
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.max_pages:
            self.current_page += 1
            self.children[0].disabled = False
            self.children[1].disabled = self.current_page == self.max_pages or self.max_pages == 1
            await self.update_embed(interaction)

