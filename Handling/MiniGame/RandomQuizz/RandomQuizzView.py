import discord
from discord.ui import Button, View
from Handling.Economy.Profile import ProfileMongoManager
from CustomEnum.EmojiEnum import EmojiCreation2
import random
from Handling.Economy.Inventory_Shop.ItemClass import Item, list_gift_items
from typing import List
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from Handling.Misc.SelfDestructView import SelfDestructView


class Quizz:
    def __init__(self, question: str, options: list, correct_answer: str):
        self.question = question
        self.options = options
        self.correct_answer = correct_answer

class RandomQuizzView(discord.ui.View):
    def __init__(self, quizz: Quizz):
        super().__init__(timeout=60)
        self.old_message: discord.Message = None
        self.opened = False
        self.quizz = quizz
        # Đổi vị trí lựa chọn, và gắn vào đáp án A, B, C
        self.shuffled_answers = random.sample(quizz.options, len(quizz.options))
        self.option_mapping = {
            "A": self.shuffled_answers[0],
            "B": self.shuffled_answers[1],
            "C": self.shuffled_answers[2]
        }
        self.user_answered = []
        
        for key, value in self.option_mapping.items():
            self.add_item(QuizButton(label=key, custom_id=value, correct_answer=self.quizz.correct_answer, view=self))

    async def on_timeout(self):
        if self.opened == False:
            await self.old_message.delete()
    
class QuizButton(Button):
    def __init__(self, label:str, custom_id: str, correct_answer: str, view: "RandomQuizzView"):
        super().__init__(label=label, style=discord.ButtonStyle.primary, custom_id=custom_id)
        self.correct_answer = correct_answer
        self.parent_view = view

    async def callback(self, interaction: discord.Interaction):
        if self.parent_view.opened == True: return
        await interaction.response.defer(ephemeral=True)
        if interaction.user.id in self.parent_view.user_answered:
            await interaction.followup.send(f'{interaction.user.mention} Mỗi người chỉ có một lượt chọn duy nhất thôi bạn ơi', ephemeral=True)
            return
        self.parent_view.user_answered.append(interaction.user.id)
        chosen_answer = self.custom_id
        if chosen_answer == self.correct_answer:
            try:
                self.parent_view.opened = True
                await self.parent_view.old_message.delete()
                await interaction.followup.send(f"🎉 Chúc mừng bạn đã trả lời chính xác!", ephemeral=True)
                channel = interaction.channel
                #random phần thưởng và thông báo kết quả
                #2% - trừ nhân phẩm. Còn lại gold 10%, silver 35%, exp 30%, dignity 35%, còn lại sẽ drop copper
                amount = random.randint(3500, 35000)
                emoji = EmojiCreation2.COPPER.value
                flag = False
                                
                gold_chance = UtilitiesFunctions.get_chance(10)
                if gold_chance and flag == False: 
                    emoji = EmojiCreation2.GOLD.value
                    amount = random.randint(10, 80)
                    ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_display_name=interaction.user.display_name, user_name=interaction.user.name, gold=amount)
                    flag = True
                    
                silver_chance = UtilitiesFunctions.get_chance(35)
                if silver_chance and flag == False: 
                    emoji = EmojiCreation2.SILVER.value
                    amount = random.randint(40, 200)
                    ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_display_name=interaction.user.display_name, user_name=interaction.user.name, silver=amount)
                    flag = True
                
                giftitem_chance = UtilitiesFunctions.get_chance(35)
                if giftitem_chance and flag == False:
                    amount = 1
                    random_item = random.choice(list_gift_items)
                    emoji = f"[{random_item.emoji} - **{random_item.item_name}**]"
                    flag = True
                    ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_display_name=interaction.user.display_name, user_name=interaction.user.name, item=random_item, amount=amount)
                
                exp_chance = UtilitiesFunctions.get_chance(35)
                if exp_chance and flag == False: 
                    emoji = "Điểm Kinh Nghiệm"
                    amount = random.randint(20, 60)
                    flag = True
                    ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=interaction.user.id, bonus_exp=amount)
                    
                    
                dignity_chance = UtilitiesFunctions.get_chance(35)
                if dignity_chance and flag == False: 
                    emoji = "Nhân Phẩm"
                    amount = random.randint(5, 50)
                    flag = True
                    ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_display_name=interaction.user.display_name, user_name=interaction.user.name, dignity_point=amount)
                
                if flag == False:
                    #Cộng copper
                    ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_display_name=interaction.user.display_name, user_name=interaction.user.name, copper=amount)
                
                embed = discord.Embed(title=f"", description=f"{EmojiCreation2.QUESTION_MARK.value} **Hỏi Nhanh Có Thưởng** {EmojiCreation2.QUESTION_MARK.value}", color=0x0ce7f2)
                embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
                embed.add_field(name=f"", value=f"**Câu hỏi**: {self.parent_view.quizz.question}", inline=False)
                for key, value in self.parent_view.option_mapping.items():
                    embed.add_field(name=f"", value=f"**{key}**. {value}", inline=False)
                embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
                embed.add_field(name=f"", value=f"Đáp án đúng chính là **{self.label}**! Chúc mừng {interaction.user.mention} đã trả lời đúng và nhận được:", inline=False)
                embed.add_field(name=f"", value=f"> {EmojiCreation2.GOLDEN_GIFT_BOX.value}: **{amount}** {emoji}", inline=False)
                embed.set_footer(text=f"Hỏi Nhanh Có Thưởng sẽ xuất hiện ngẫu nhiên, và khi thấy thì nhớ trả lời đúng nhé!", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
                view = SelfDestructView()
                m = await channel.send(embed=embed, view=view)
                view.message = m
            except Exception:
                return
        else:
            await interaction.followup.send(f'{interaction.user.mention} Thôi thua rồi bạn ơi, bạn trả lời sai và quay vào ô mất lượt rồi.', ephemeral=True)
            return

random_quizzes = [
            Quizz(
                question="Thủ đô của Canada tên là gì?",
                options=["Ottawa", "Algonquin", "Vancouver"],
                correct_answer="Ottawa"
            ),
            Quizz(
                question="Thủ đô của Thái Lan tên là gì?",
                options=["Bangkok", "Bangdik", "Bangpussy"],
                correct_answer="Bangkok"
            ),
            Quizz(
                question="Thủ đô của Thái Lan viết trong tiếng Thái là gì?",
                options=["กรุงเทพมหานคร", "ประเทศไทยศูนย์กลาง", "ศูนย์กลางศูนย์กลาง"],
                correct_answer="กรุงเทพมหานคร"
            ),
            Quizz(
                question="Diện tích trái đất xấp xỉ bao nhiêu km2?",
                options=["510.000.000 km2", "513.000.000 km2", "519.000.000 km2"],
                correct_answer="510.000.000 km2"
            ),
            Quizz(
                question="Hình nón (N) có đường sinh gấp hai lần bán kính đáy. Góc ở đỉnh của hình nón là bao nhiêu độ?",
                options=["120", "60", "45"],
                correct_answer="60"
            ),
            Quizz(
                question="Kim tự tháp Kê-ốp ở Ai Cập được xây dựng vào khoảng 2500 năm trước công nguyên, là một hình chóp tứ giác đều có chiều cao là 147m, cạnh đáy dài 230m. Tính thể tích?",
                options=["7776300 m3", "2592100 m3", "1470000 m3"],
                correct_answer="2592100 m3"
            ),
            Quizz(
                question="2 con vịt đi trước 2 con vịt, 2 con vịt đi sau 2 con vịt, 2 con vịt đi giữa 2 con vịt. Hỏi có mấy con vịt?",
                options=["4", "6", "8"],
                correct_answer="4"
            ),
            Quizz(
                question="Con sông dài nhất trên thế giới là gì?",
                options=["Sông Mêkông", "Sông Nile", "Sông Amazon"],
                correct_answer="Sông Nile"
            ),
            Quizz(
                question="Là ai đã vẽ bức tranh nổi tiếng nàng Mona Lisa?",
                options=["Leonardo da Vinci", "Lenardo da Vinci", "Leonardo da Vini"],
                correct_answer="Leonardo da Vinci"
            ),
            Quizz(
                question="Búp bê Barbie tên đầy đủ là gì?",
                options=["Barbara Millicent Roberts", "Barbara Milicent Roberts", "Barbara Millicent Robert"],
                correct_answer="Barbara Millicent Roberts"
            ),
            Quizz(
                question="Búp bê Barbie tên đầy đủ là gì?",
                options=["Barbara Millicent Roberts", "Barbara Milicent Roberts", "Barbara Millicent Robert"],
                correct_answer="Barbara Millicent Roberts"
            ),
            Quizz(
                question="Con vật nào dưới đây không thể bơi?",
                options=["Cá", "Vịt", "Búp bê"],
                correct_answer="Búp bê"
            ),
            Quizz(
                question="Ai đã thả một chiếc búa và một chiếc lông vũ xuống Mặt trăng để chứng minh rằng khi không có không khí, chúng sẽ rơi với tốc độ như nhau?",
                options=["David Scott", "Apollo Scott", "David Apollo"],
                correct_answer="David Scott"
            ),
            Quizz(
                question="Nếu ta có thể xử lý một tỷ nguyên tử mỗi giây, sẽ mất bao lâu để dịch chuyển tức thời một con người?",
                options=["200 tỷ năm", "200 triệu năm", "20 tỷ năm"],
                correct_answer="200 tỷ năm"
            ),
            Quizz(
                question="Đấu trường La Mã nằm ở thành phố nào?",
                options=["La Mã", "Rome", "Ý"],
                correct_answer="Rome"
            ),
            Quizz(
                question="Đấu trường La Mã nằm ở đất nước nào?",
                options=["La Mã", "Rome", "Ý"],
                correct_answer="Ý"
            ),
            Quizz(
                question="Stonehenge là một công trình tượng đài cự thạch ở đâu?",
                options=["Pháp", "Anh", "Ý"],
                correct_answer="Anh"
            ),
            Quizz(
                question="Loại nước giải khát nào chứa sắt và canxi?",
                options=["Cafe", "Nước cam", "Nước dừa"],
                correct_answer="Cafe"
            ),
            Quizz(
                question="1 năm có bao nhiêu tháng có ngày 28?",
                options=["1", "6", "12"],
                correct_answer="12"
            ),
            Quizz(
                question="Loại rượu nào đặc trưng của một số dân tộc mà khi uống phải dùng cần tre hoặc trúc uốn cong để hút rượu?",
                options=["Rượu đế", "Rượu cần", "Rượu bàu đá"],
                correct_answer="Rượu cần"
            ),
            Quizz(
                question="Maria Sharapova là vận động viên nổi tiếng ở môn thể thao nào?",
                options=["Điền kinh", "Quần vợt", "Bơi lội"],
                correct_answer="Quần vợt"
            ),
            Quizz(
                question="Maria Sharapova là vận động viên nổi tiếng ở môn thể thao nào?",
                options=["Điền kinh", "Quần vợt", "Bơi lội"],
                correct_answer="Quần vợt"
            ),
            Quizz(
                question="Một trong những quốc gia có vai trò quan trọng trong quá trình hình thành Liên hợp quốc là?",
                options=["Liên Xô", "Anh", "Pháp"],
                correct_answer="Liên Xô"
            ),
            Quizz(
                question="Trong giai đoạn cuối của Chiến tranh thế giới thứ hai, một trong những vấn đề cấp bách đặt ra là?",
                options=["Thành lập một tổ chức quốc tế nhằm duy trì hòa bình và trật tự thế giới mới", "Thành lập một liên minh giữa Liên Xô và Mĩ để thiết lập trật tự thế giới mới sau chiến tranh", "Thành lập một ủy ban giúp đỡ các nước phát xít"],
                correct_answer="Thành lập một tổ chức quốc tế nhằm duy trì hòa bình và trật tự thế giới mới"
            ),
            Quizz(
                question="Vị vua nào có nhiều vợ nhất nhưng lại không có người con nào?",
                options=["Hàm Nghi", "Lê Thần Tông", "Tự Đức"],
                correct_answer="Tự Đức"
            ),
            Quizz(
                question="Ai là vị trạng nguyên trẻ tuổi nhất nước Nam?",
                options=["Mạc Đĩnh Chi", "Nguyễn Bỉnh Khiêm", "Nguyễn Hiền"],
                correct_answer="Nguyễn Hiền"
            ),
            Quizz(
                question="Văn miếu Quốc Tử Giám, trường đại học đầu tiên của Việt Nam được xây dựng dưới triều đại nào?",
                options=["Lý", "Trần", "Lê"],
                correct_answer="Lý"
            ),
            Quizz(
                question="Lệ Chi Viên là khu vườn trồng loại cây gì?",
                options=["Táo", "Vải", "Cam"],
                correct_answer="Vải"
            ),
            Quizz(
                question="Hoàng đế Bảo Đại tên thật là gì?",
                options=["Nguyễn Phúc Vĩnh Thụy", "Nguyễn Phúc Bảo Long", "Nguyễn Phúc Vĩnh Thụy"],
                correct_answer="Nguyễn Phúc Vĩnh Thụy"
            ),
        ]