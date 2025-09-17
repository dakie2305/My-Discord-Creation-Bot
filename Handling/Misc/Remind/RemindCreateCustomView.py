from datetime import datetime, timedelta
import discord
from CustomEnum.SlashEnum import SlashCommand
from typing import List, Optional, Dict

from Handling.Misc.Remind import RemindMongoManager
from Handling.Misc.SelfDestructView import SelfDestructView

class RemindCreateCustom(discord.ui.View):
    def __init__(self, user: discord.Member, content: str):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.user: discord.Member = user
        self.content: str = content


    @discord.ui.button(label="Tạo Mới", style=discord.ButtonStyle.green)
    async def create_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id:  
            await interaction.response.send_message("❌ Bạn không có quyền sử dụng nút này.", ephemeral=True)
            return
        await interaction.response.send_modal(TextInputModal(user=self.user, content=self.content, old_message=self.message))
        return

    async def on_timeout(self):
        # Disable all buttons khi hết hạn
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True
        if self.message:
            try:
                await self.message.edit(view=self)
            except Exception:
                pass

# Create a custom modal for text input
class TextInputModal(discord.ui.Modal):
    def __init__(self, user: discord.Member, content: str, old_message: discord.Message):
        super().__init__(title="Chọn ngày giờ tạo lời nhắc.")
        self.user: discord.Member = user
        self.content = content
        self.old_message: discord.Message = old_message
        self.input_date_field = discord.ui.TextInput(
            label="Nhập ngày đúng định dạng dd/MM/yyyy",
            placeholder="Ví dụ: 31/07/2025",
            required=True,
        )
        self.input_time_field = discord.ui.TextInput(
            label="Nhập giờ đúng định dạng HH:mm",
            placeholder="VD: 14:00",
            required=True,
        )
        self.add_item(self.input_date_field)
        self.add_item(self.input_time_field)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        # Parse datetime
        try:
            date_str = self.input_date_field.value.strip()
            time_str = self.input_time_field.value.strip()
            remind_datetime = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")

            if remind_datetime < datetime.now():
                view = SelfDestructView(timeout=30)
                embed = discord.Embed(title=f"Thời gian không hợp lệ!", description=f"Thời gian đã nhập nằm trong quá khứ!", color=discord.Color.red())
                mess = await interaction.followup.send(embed=embed, view=view)
                view.message = mess
                return
            limit_date = datetime.now() + timedelta(weeks=38)
            if remind_datetime > limit_date:
                view = SelfDestructView(timeout=30)
                unix_time = int(limit_date.timestamp())
                embed = discord.Embed(title=f"Thời gian không hợp lệ!", description=f"Lời nhắc không được phép vượt quá ngày <t:{unix_time}:d>!", color=discord.Color.red())
                mess = await interaction.followup.send(embed=embed, view=view)
                view.message = mess
                return
            # Success response
            remind = RemindMongoManager.create_or_update_remind(remind_id=None, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, guild_id=interaction.guild.id, guild_name=interaction.guild.name, channel_id=interaction.channel.id, channel_name=interaction.channel.name, message_content=self.content, date_remind=remind_datetime)
            unix_time = int(remind_datetime.timestamp())
            embed = discord.Embed(title=f"Tạo lời nhắc thành công!", description=f"", color=0xddede7)
            embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
            embed.add_field(name=f"", value=f"Vào lúc <t:{unix_time}:f> Creation bot sẽ nhắc bạn với nội dung sau:", inline=False)
            embed.add_field(name=f"", value=f"- **{self.content}**", inline=False)
            embed.add_field(name=f"", value=f"Tại Server {interaction.guild.name} tại kênh <#{interaction.channel.id}>", inline=False)
            await interaction.followup.send(content= f"{interaction.user.mention}",embed=embed, ephemeral=False)
            try: await self.old_message.delete()
            except Exception: pass
        except ValueError:
            await interaction.followup.send(content= f"⚠️ Sai định dạng! Vui lòng nhập ngày giờ theo định dạng `dd/MM/yyyy` và `HH:mm`.", ephemeral=False)
        