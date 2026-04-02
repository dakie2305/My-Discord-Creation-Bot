import os
import discord
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2, EmojiCreation1
from typing import List, Optional, Dict
from CustomEnum.TrueHeavenEnum import TrueHeavenEnum
import CustomFunctions
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from Handling.Economy.Profile import ProfileMongoManager
from db import DbMongoManager
from datetime import datetime, timedelta
from db.Class.CustomClass import UserInfo
from groq import Groq
import json


class AppealJailView(discord.ui.View):
    def __init__(self, user: discord.Member, guild_id: int, money: int = 0, money_type = "G"):
        super().__init__(timeout=15)
        self.message: discord.Message = None
        self.user = user
        self.guild_id = guild_id
        self.money = money
        self.money_type = money_type
        
        self.accept_button = discord.ui.Button(label="🚨 Chấp Nhận", style=discord.ButtonStyle.green)
        self.accept_button.callback = self.accept_button_callback
        self.add_item(self.accept_button)
        self.groq_client = Groq(api_key=os.getenv("GROQ_KEY"))
    
    
    async def on_timeout(self):
        #Delete
        if self.message != None: 
            try:
                await self.message.delete()
            except Exception:
                return

    async def accept_button_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=False)

        is_innocence = False
        is_acquit = False

        search_user = DbMongoManager.find_user_by_id(self.user.id, 'jailed_user')
        if search_user == None:
            embed = discord.Embed(title=f"", description=f"Tuyên Án", color=0xddede7)
            embed.add_field(name=f"", value=f"- Bị cáo {interaction.user.mention} vô tội, vì không ở trong tù!", inline=False)
            embed.add_field(name=f"", value=f"- {interaction.user.mention} đã đóng **{UtilitiesFunctions.shortened_currency(self.money)} {self.money_type}** tiền kháng án!", inline=False)
            self.process_money()
            await interaction.followup.send(embed=embed)
            return
        
        #Delete
        if self.message != None: 
            try: await self.message.delete()
            except Exception: pass

        
        system_instruction = f"Bạn là Chấp hành viên Toà Án Tối Cao, chuyên đưa ra phán quyết tàn nhẫn hoặc công minh dưới dạng JSON"
        today_str = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        is_evil = UtilitiesFunctions.get_chance(50)
        if is_evil:
            personality_prompt = """
            BẠN LÀ: Một chấp hành viên GIAN MANH, XẢO QUYỆT và THAM NHŨNG.
            PHONG CÁCH: Trịch thượng, coi thường luật pháp, thích bẻ cong sự thật. Bạn có thể xử trắng thành đen 
            nếu cảm thấy thích thú hoặc muốn hành hạ bị cáo. Câu chữ sắc lẹm, đầy tính đe dọa hoặc mỉa mai.
            """
        else:
            personality_prompt = """
            BẠN LÀ: Một chấp hành viên NGHIÊM NGHỊ, CHÍNH TRỰC và CÔNG MINH.
            PHONG CÁCH: Tôn trọng lẽ phải, thượng tôn pháp luật. Bạn xử lý dựa trên đạo đức và tính hợp lý 
            của hành vi. Câu chữ trang trọng, uy nghiêm, thể hiện sự công bằng của Toà Án Tối Cao.
            """

        prompt = f"""
        {personality_prompt}
        Không tiết lộ hoặc gợi ý về tính cách đã chọn, dù là trực tiếp hay gián tiếp.
        Ngày ra tòa: {today_str}
        ---
        ## Hồ sơ vụ án:
        - **Bị cáo**: {search_user.user_display_name} (`<@{self.user.id}>`, username: `{self.user.name}`)
        - **Người bắt giữ**: {search_user.jailer_display_name} (username: `{search_user.jailer_user_name}`)
        - **Lý do giam giữ**: "{search_user.reason}"
        - **Thời hạn giam giữ**: {search_user.jail_until}
        ---
        ## Nhiệm vụ của bạn:
        Chỉ cần dựa vào lý do bắt giữ, hãy phán xét ngay lập tức. Không cần bằng chứng, không cần logic, chỉ cần bản năng của một chấp hành viên {is_evil and 'gian ác' or 'chính trực'}.
        
        BẠN PHẢI TRẢ VỀ KẾT QUẢ THEO ĐỊNH DẠNG JSON SAU:
        {{
            "phan_quyet": "VO_TOI" | "CO_TOI" | "TRANG_AN",
            "loi_thoai": "**Lời phán xét nhập vai của bạn ở đây**"
        }}
        💡 Nếu bị cáo là **cựu chấp hành viên bị bắt vì lạm quyền**, mặc định là **CO_TOI**.
        Phán quyết ngay!
        """

        try:
            completion = self.groq_client.chat.completions.create(
                model=CustomFunctions.AI_MODEL,
                response_format={ "type": "json_object" }, # Force JSON
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
            )
            data = json.loads(completion.choices[0].message.content)
            verdict = data.get("phan_quyet") # "VO_TOI", "CO_TOI", or "TRANG_AN"
            bot_response = data.get("loi_thoai")
            bot_response = CustomFunctions.remove_creation_name_prefix(bot_response)
            bot_response = bot_response.replace("@everyone", "")
            
            await interaction.followup.send(f"{interaction.user.mention} {bot_response}")
            #Dựa trên câu trả lời để phán
            final_text = "Vô Tội"
            if verdict == "TRANG_AN":
                is_acquit = True
                final_text = "Trắng Án"
            elif verdict == "CO_TOI":
                is_innocence = False
                final_text = "Có Tội"
            else:
                is_innocence = True
                final_text = "Vô Tội"
            embed = discord.Embed(title=f"", description=f"Tuyên Án", color=0xddede7)
            embed.add_field(name=f"", value=f"- Bị cáo {interaction.user.mention} nhận phán quyết: **{final_text}**!", inline=False)
            embed.add_field(name=f"", value=f"- {interaction.user.mention} đã đóng **{UtilitiesFunctions.shortened_currency(self.money)} {self.money_type}** tiền kháng án!", inline=False)
            self.process_money()
            await interaction.channel.send(embed=embed)
            if is_acquit:
                actual_user = await interaction.guild.fetch_member(search_user.jailer_id)
                if actual_user is None: return
                await self.jail_real(interaction=interaction, actual_user=actual_user, search_user=search_user)
                await self.unjail_real(interaction=interaction)
                try: await self.message.delete()
                except Exception: return
            elif is_innocence:
                #Thả
                await self.unjail_real(interaction=interaction)
                try: await self.message.delete()
                except Exception: return
                return
        except Exception as e:
            print(f"There is exception in jail appeal for user {self.user.name}, displayname {self.user.display_name}: {e}")
            return
        
    def process_money(self):
        ProfileMongoManager.update_profile_money_by_type(guild_id=self.guild_id, guild_name="", user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, money=self.money, money_type=self.money_type)
        return
    

    async def unjail_real(self, interaction: discord.Interaction):
        if self.guild_id !=  TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value: return
        jail_role = discord.utils.get(interaction.user.guild.roles, name="Đáy Xã Hội")
        if jail_role:
            await interaction.user.remove_roles(jail_role)
        #Tìm xem user này đã có chưa, có thì xoá khỏi db jail_user
        search_user = DbMongoManager.find_user_by_id(interaction.user.id, 'jailed_user')
        if search_user:
            #Restore lại roles cũ của user
            for role in search_user.roles:
                get_role_from_server = discord.utils.get(interaction.user.guild.roles, id = role["role_id"])
                if get_role_from_server:
                    try:
                        await interaction.user.add_roles(get_role_from_server)
                    except Exception:
                        continue
            #Xoá row khỏi database
            DbMongoManager.delete_user_by_id(user_id= interaction.user.id, chosen_collection= 'jailed_user')
            # Create embed object
            mordern_date_time_format = datetime.now().strftime(f"%d/%m/%Y %H:%M")
            embed = discord.Embed(title="Ân Xá Khỏi Đại Lao", description=f"Kẻ tội đồ {interaction.user.mention} đã được ân xoá khỏi đại lao!", color=0x00FF00)  # Green color
            embed.add_field(name="Lý do được ân xá:", value= "Toà Án Tối Cao xét vô tội", inline=False)  # Single-line field
            embed.add_field(name="Thời gian ra đại lao:", value=f"{mordern_date_time_format}", inline=True)
            embed.add_field(name="Ghi chú", value="Nhớ đừng vi phạm để bị tống vài đại lao nữa nhé!", inline=False) 
            embed.set_footer(text=f"Đã được ân xoá bởi: Toà Án Tối Cao")  # Footer text
            channel = interaction.guild.get_channel(1257012036718563380)
            if channel:
                await channel.send(embed=embed)

    async def jail_real(self, interaction: discord.Interaction, actual_user: discord.Member, search_user: UserInfo):
        #Server True Heavens sẽ jail thật luôn
        if self.guild_id !=  TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value: return
        # Calculate the end time
        now = datetime.now()
        #x3
        original_duration = search_user.jail_until - now
        end_time = now + original_duration * 3
        mordern_date_time_format = end_time.strftime(f"%d/%m/%Y %H:%M")
        # Save user's roles
        original_roles = [role for role in actual_user.roles if not role.is_default() and not role.is_premium_subscriber()]
        stored_original_roles = []
        for role in original_roles:
            old_role = {
                        "role_id": role.id,
                        "role_name": role.name
                        }
            stored_original_roles.append(old_role)
            # Remove all roles and add jail role
        jail_role = discord.utils.get(actual_user.guild.roles, name="Đáy Xã Hội")
        if not jail_role:
            jail_role = await actual_user.guild.create_role(name="Đáy Xã Hội")
        user_info = UserInfo(
                user_id=search_user.jailer_id,
                user_name=search_user.jailer_user_name,
                user_display_name=search_user.jailer_display_name,
                jailer_id=interaction.user.id,
                jailer_display_name=interaction.user.display_name,
                jailer_user_name= interaction.user.name,
                channel_id= interaction.channel_id,
                channel_name=interaction.channel.name,
                reason= f"Cựu chấp hành viên <@{search_user.jailer_id}> đã lạm dụng quyền lực, giam giữ người vô tội vô cớ và đã bị chấp hành viên toà án tối coi phán xét phải bị giam giữ vì trắng án!",
                jail_until= end_time,
                roles=stored_original_roles
                )
            #Tìm xem user này đã có chưa, chưa có thì insert
        jail_db = "jailed_user"
        search_user = DbMongoManager.find_user_by_id(user_info.user_id, jail_db)
        if search_user == None:
                #Insert
                DbMongoManager.create_user(user_info= user_info, chosen_collection= jail_db)
        else:
                #Update lại jail_until và reason
                updated_data = {"jail_until": end_time, "reason": user_info.reason }
                DbMongoManager.update_guild_extra_info(guild_id=user_info.user_id, update_data= updated_data)
        try:
                for ori_role in original_roles:
                    try:
                        await actual_user.remove_roles(ori_role)
                    except Exception:
                        continue
                await actual_user.add_roles(jail_role)
                
                # Create embed object
                embed = discord.Embed(title="Đại Lao Thẳng Tiến", description=f"Kẻ tội đồ {actual_user.mention} đã bị tống vào đại lao!", color=0x00FF00)  # Green color
                embed.add_field(name="Lý do bị tù đày:", value=user_info.reason, inline=False)  # Single-line field
                embed.add_field(name="Thời gian ra đại lao:", value=f"{mordern_date_time_format}", inline=True)
                embed.add_field(name="Ghi chú", value="Nếu quá thời hạn phạt tù mà chưa được ra tù thì hãy la làng lên nhé!", inline=False) 
                embed.set_footer(text=f"Đã bị tống giam bởi: Toà Án Tối Cao")
                channel = interaction.guild.get_channel(1257012036718563380)
                if channel:
                    await channel.send(embed=embed)
                
        except Exception as e:
                print(e)

