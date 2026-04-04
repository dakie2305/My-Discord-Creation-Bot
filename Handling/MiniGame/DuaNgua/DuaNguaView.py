from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
import discord
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from typing import List, Dict
import random
import asyncio


class PlayerBetInfo:
    def __init__(
        self,
        user: discord.Member,
        user_profile: Profile,
        horse_id: int,
        so_tien,
        loai_tien,
    ):
        self.user = user
        self.user_profile = user_profile
        self.horse_id = horse_id
        self.so_tien = so_tien
        self.loai_tien = loai_tien


class DuaNguaView(discord.ui.View):
    def __init__(
        self,
        user: discord.Member,
        horses_pool: List[Dict],
        user_profile: Profile = None,
        so_tien: int = None,
        loai_tien=None,
        is_betting=False,
        mult: int = 2,
        timeout: int = 30,
        track_length: int = 60,
        obstacles: List[int] = None,
    ):
        super().__init__(timeout=timeout)
        self.message: discord.Message = None
        self.user = user
        self.horses_pool = horses_pool
        self.user_profile = user_profile
        self.so_tien = so_tien
        self.loai_tien = loai_tien
        self.is_running = False
        self.is_betting = is_betting
        self.mult = mult
        self.player_list: List[PlayerBetInfo] = []
        self.horse_positions: Dict[int, int] = {h["id"]: 0 for h in horses_pool}
        self.comments = ["Đang chờ người tham gia..."]
        self.track_length = track_length
        self.obstacles = obstacles
        if self.is_betting:
            betting_button = discord.ui.Button(
                label="Tham Gia Đặt Cược 🐎", style=discord.ButtonStyle.primary
            )
            betting_button.callback = self.bet_button
            self.add_item(betting_button)

    async def bet_button(self, interaction: discord.Interaction):
        # Player limit
        if len(self.player_list) >= 8:
            await interaction.response.send_message(
                content="Ván đua đã đủ 8 người tham gia! Vui lòng đợi ván sau.",
                ephemeral=True,
            )
            return

        # Check if already joined
        for player in self.player_list:
            if interaction.user.id == player.user.id:
                await interaction.response.send_message(
                    content="Bạn đã đặt cược rồi! Vui lòng đợi kết quả.", ephemeral=True
                )
                return

        await interaction.response.defer(ephemeral=True)

        # Check profile and money
        player_profile = ProfileMongoManager.find_profile_by_id(
            guild_id=interaction.guild_id, user_id=interaction.user.id
        )
        if player_profile is None:
            await interaction.followup.send(
                content=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!",
                ephemeral=True,
            )
            return

        can_afford = False
        if self.loai_tien == "C" and player_profile.copper >= self.so_tien:
            can_afford = True
        elif self.loai_tien == "S" and player_profile.silver >= self.so_tien:
            can_afford = True
        elif self.loai_tien == "G" and player_profile.gold >= self.so_tien:
            can_afford = True

        if not can_afford:
            currency_name = ""
            if self.loai_tien == "C":
                currency_name = EmojiCreation2.COPPER.value
            elif self.loai_tien == "S":
                currency_name = EmojiCreation2.SILVER.value
            elif self.loai_tien == "G":
                currency_name = EmojiCreation2.GOLD.value
            await interaction.followup.send(
                content=f"Bạn không có đủ {currency_name} để tham gia!",
                ephemeral=True,
            )
            return

        # Show horse selection
        view = HorseSelectView(self, player_profile)
        await interaction.followup.send(
            content=f"Hãy chọn con ngựa bạn muốn đặt cược (**{self.so_tien}**)",
            view=view,
            ephemeral=True,
        )

    async def on_timeout(self):
        if self.message:
            self.clear_items()
            await self.message.edit(view=None)
            await self.start_race()

    async def start_race(self):
        self.is_running = True
        commentary_pool = [
            "Cuộc đua đang diễn ra hết sức căng thẳng!",
            "Con ngựa {name} đang bứt phá ngoạn mục!",
            "Có vẻ như {name} vừa vấp phải một chướng ngại vật!",
            "{name} đang lao nhanh như một cơn gió!",
            "Khán giả đang hò reo cổ vũ hết mình!",
            "Khoảng cách giữa các con ngựa đang dần được rút ngắn!",
            "Liệu ai sẽ là người chạm đích đầu tiên đây?",
            "{name} bỗng bùng tốc rất đáng nể!",
            "Một cú tăng tốc bất ngờ từ {name}!",
            "Mọi ánh mắt đang đổ dồn vào {name}!",
            "{name} đang dẫn đầu cuộc đua!",
            "{name} đang bứt phá ngoạn mục!",
        ]

        for turn in range(8):
            await asyncio.sleep(2)

            # Move horses
            for horse in self.horses_pool:
                h_id = horse["id"]
                # Normal move
                move = random.randint(4, 9)
                # Check obstacles
                current_pos = self.horse_positions[h_id]
                for obs in self.obstacles:
                    if current_pos <= obs < current_pos + move:
                        # Obstacle hit!
                        effect = random.choice(["boost", "fail", "none"])
                        if effect == "boost":
                            move += random.randint(2, 4)
                        elif effect == "fail":
                            move -= random.randint(2, 3)

                self.horse_positions[h_id] += move

            # Tie breaker on final turn
            if turn == 7:
                for h_id in self.horse_positions:
                    self.horse_positions[h_id] += h_id * 0.01

            # Find leader
            leader_id = max(self.horse_positions, key=self.horse_positions.get)
            leader_horse = next(h for h in self.horses_pool if h["id"] == leader_id)
            leader_name = f"{leader_horse['name']} số {leader_horse['id']}"

            # Generate commentary
            new_comment = random.choice(commentary_pool).format(name=leader_name)
            self.comments.append(new_comment)
            if len(self.comments) > 3:
                self.comments.pop(0)

            description = ""
            comment_text = "\n".join(self.comments)
            if self.is_betting:
                description = f"Tiền cược tham gia: **{self.so_tien}** {UtilitiesFunctions.get_emoji_from_loai_tien(self.loai_tien)}.\nNgười thắng sẽ nhận x{self.mult} số tiền cược."
            # Update Embed
            embed = discord.Embed(
                title="Giải Đua Ngựa Mở Rộng - Đang Diễn Ra",
                description=description,
                color=0x03F8FC,
            )
            for horse in self.horses_pool:
                h_id = horse["id"]
                pos = int(self.horse_positions[h_id])
                track_str = UtilitiesFunctions.get_track_string(
                    horse_emoji=horse["emoji"],
                    position=pos,
                    track_length=self.track_length,
                    obstacles=self.obstacles,
                )
                embed.add_field(
                    name=f"{h_id}. {horse['name']}",
                    value=track_str,
                    inline=False,
                )

            await self.message.edit(content=comment_text, embed=embed)

        await self.process_results()

    async def process_results(self):
        # Determine winner
        winner_id = max(self.horse_positions, key=self.horse_positions.get)
        winner_horse = next(h for h in self.horses_pool if h["id"] == winner_id)

        winners_list = []
        losers_list = []
        total_house_payout = 0

        # Rank horses by final positions
        ranked_horse_ids = sorted(
            self.horse_positions, key=self.horse_positions.get, reverse=True
        )

        # 1. Update the ORIGINAL message with final horse standings
        standings_embed = discord.Embed(
            title="Kết Quả Cuộc Đua - Đã Kết Thúc",
            description=f"Chúc mừng ngựa **{winner_horse['name']} {winner_horse['emoji']}** đã dành chiến thắng!",
            color=0x03F8FC,
        )
        for horse in self.horses_pool:
            h_id = horse["id"]
            pos = int(self.horse_positions[h_id])
            track_str = UtilitiesFunctions.get_track_string(
                horse_emoji=horse["emoji"],
                position=pos,
                track_length=self.track_length,
                obstacles=self.obstacles,
            )
            status = f"{EmojiCreation2.FIRST_CUP.value}" if h_id == winner_id else "❌"
            standings_embed.add_field(
                name=f"{status} {h_id}. {horse['name']}", value=track_str, inline=False
            )
        await self.message.edit(
            content="Cuộc đua đã kết thúc!", embed=standings_embed, view=None
        )
        if not self.is_betting:
            return

        # Construct the BETTING SUMMARY in a REPLY
        amount_won = 0
        total_house_payout = 0
        total_house_win = 0
        for player in self.player_list:
            if player.horse_id == winner_id:
                amount_won = player.so_tien * self.mult
                total_house_payout += amount_won
                # Give reward to winners
                # THE HOUSE (host) PAYS THE PRIZE
                emoji = ""
                if player.loai_tien == "C":
                    emoji = EmojiCreation2.COPPER.value
                    ProfileMongoManager.update_profile_money(
                        guild_id=self.message.guild.id,
                        guild_name="",
                        user_id=player.user.id,
                        user_name=player.user.name,
                        user_display_name=player.user.display_name,
                        copper=amount_won,
                    )
                    ProfileMongoManager.update_profile_money(
                        guild_id=self.message.guild.id,
                        guild_name="",
                        user_id=self.user.id,
                        user_name=self.user.name,
                        user_display_name=self.user.display_name,
                        copper=-amount_won,
                    )
                elif player.loai_tien == "S":
                    emoji = EmojiCreation2.SILVER.value
                    ProfileMongoManager.update_profile_money(
                        guild_id=self.message.guild.id,
                        guild_name="",
                        user_id=player.user.id,
                        user_name=player.user.name,
                        user_display_name=player.user.display_name,
                        silver=amount_won,
                    )
                    ProfileMongoManager.update_profile_money(
                        guild_id=self.message.guild.id,
                        guild_name="",
                        user_id=self.user.id,
                        user_name=self.user.name,
                        user_display_name=self.user.display_name,
                        silver=-amount_won,
                    )
                elif player.loai_tien == "G":
                    emoji = EmojiCreation2.GOLD.value
                    ProfileMongoManager.update_profile_money(
                        guild_id=self.message.guild.id,
                        guild_name="",
                        user_id=player.user.id,
                        user_name=player.user.name,
                        user_display_name=player.user.display_name,
                        gold=amount_won,
                    )
                    ProfileMongoManager.update_profile_money(
                        guild_id=self.message.guild.id,
                        guild_name="",
                        user_id=self.user.id,
                        user_name=self.user.name,
                        user_display_name=self.user.display_name,
                        gold=-amount_won,
                    )

                winners_list.append(
                    f"{player.user.mention} (Đã nhận **{amount_won}** {emoji})"
                )
            else:
                total_house_win += self.so_tien
                losers_list.append(player.user.mention)

        # Trừ % số tiền từ game nếu có bet
        text_tax = ""
        if self.is_betting:
            tax_money = int(total_house_win * 10 / 100)
            if tax_money <= 0:
                tax_money = 1
            if self.loai_tien == "C":
                ProfileMongoManager.update_profile_money(
                    guild_id=self.user.guild.id,
                    guild_name="",
                    user_id=self.user.id,
                    user_name=self.user.name,
                    user_display_name=self.user.display_name,
                    copper=-tax_money,
                )
            if self.loai_tien == "S":
                ProfileMongoManager.update_profile_money(
                    guild_id=self.user.guild.id,
                    guild_name="",
                    user_id=self.user.id,
                    user_name=self.user.name,
                    user_display_name=self.user.display_name,
                    silver=-tax_money,
                )
            if self.loai_tien == "G":
                ProfileMongoManager.update_profile_money(
                    guild_id=self.user.guild.id,
                    guild_name="",
                    user_id=self.user.id,
                    user_name=self.user.name,
                    user_display_name=self.user.display_name,
                    gold=-tax_money,
                )
            text_tax = f"\nNhà cái đã tốn thêm **{tax_money}** {UtilitiesFunctions.get_emoji_from_loai_tien(self.loai_tien)} để đóng phí bảo kê ván đua!"

        # Economy summary
        net_house_profit = total_house_win - total_house_payout

        profit_emoji = "📈" if net_house_profit >= 0 else "📉"
        profit_color = 0x00FF00 if net_house_profit >= 0 else 0xFF0000

        currency_emoji = UtilitiesFunctions.get_emoji_from_loai_tien(self.loai_tien)

        summary_embed = discord.Embed(
            title="Bảng Vàng Đua Ngựa",
            description="### [ TỔNG KẾT ĐẶT CƯỢC ]",
            color=profit_color,
        )

        summary_embed.add_field(
            name=f"{EmojiCreation2.SHINY_POINT.value} Nhà cái ({self.user.display_name})",
            value=f"{profit_emoji} {'Lãi được' if net_house_profit >= 0 else 'Lỗ vốn'}: **{abs(net_house_profit)}** {currency_emoji}",
            inline=False,
        )

        summary_embed.add_field(
            name=f"{EmojiCreation2.SHINY_POINT.value} Danh sách thắng",
            value="\n".join(winners_list) if winners_list else "Không ai thắng cả.",
            inline=False,
        )

        summary_embed.add_field(
            name=f"{EmojiCreation2.SHINY_POINT.value} Danh sách thua",
            value=", ".join(losers_list) if losers_list else "Không có ai thua.",
            inline=False,
        )

        summary_embed.add_field(
            name=f"{EmojiCreation2.SHINY_POINT.value} Tiền phí bảo kê:",
            value=text_tax,
            inline=False,
        )
        summary_embed.set_footer(text="Cảm ơn mọi người đã tham gia giải đua!")
        await self.message.reply(embed=summary_embed)


class HorseSelectView(discord.ui.View):
    def __init__(self, main_view: DuaNguaView, player_profile: Profile):
        super().__init__(timeout=30)
        self.main_view = main_view
        self.player_profile = player_profile
        self.add_item(HorseSelect(main_view, player_profile))


class HorseSelect(discord.ui.Select):
    def __init__(self, main_view: DuaNguaView, player_profile: Profile):
        self.main_view = main_view
        self.player_profile = player_profile
        options = []
        for horse in main_view.horses_pool:
            options.append(
                discord.SelectOption(
                    label=f"{horse['id']}. {horse['name']}",
                    value=str(horse["id"]),
                    emoji=horse["emoji"],
                )
            )
        super().__init__(
            placeholder="Chọn ngựa của bạn...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        horse_id = int(self.values[0])

        # Double check if user joined while selecting
        for player in self.main_view.player_list:
            if interaction.user.id == player.user.id:
                await interaction.response.edit_message(
                    content="Bạn đã đặt cược rồi!", view=None
                )
                return

        # Deduct money immediately and credit the host
        if self.main_view.loai_tien == "C":
            # Deduct from player
            ProfileMongoManager.update_profile_money(
                guild_id=interaction.guild_id,
                guild_name=interaction.guild.name,
                user_id=interaction.user.id,
                user_name=interaction.user.name,
                user_display_name=interaction.user.display_name,
                copper=-self.main_view.so_tien,
            )
            # Credit the host
            ProfileMongoManager.update_profile_money(
                guild_id=interaction.guild_id,
                guild_name=interaction.guild.name,
                user_id=self.main_view.user.id,
                user_name=self.main_view.user.name,
                user_display_name=self.main_view.user.display_name,
                copper=self.main_view.so_tien,
            )
        elif self.main_view.loai_tien == "S":
            # Deduct from player
            ProfileMongoManager.update_profile_money(
                guild_id=interaction.guild_id,
                guild_name=interaction.guild.name,
                user_id=interaction.user.id,
                user_name=interaction.user.name,
                user_display_name=interaction.user.display_name,
                silver=-self.main_view.so_tien,
            )
            # Credit the host
            ProfileMongoManager.update_profile_money(
                guild_id=interaction.guild_id,
                guild_name=interaction.guild.name,
                user_id=self.main_view.user.id,
                user_name=self.main_view.user.name,
                user_display_name=self.main_view.user.display_name,
                silver=self.main_view.so_tien,
            )
        elif self.main_view.loai_tien == "G":
            # Deduct from player
            ProfileMongoManager.update_profile_money(
                guild_id=interaction.guild_id,
                guild_name=interaction.guild.name,
                user_id=interaction.user.id,
                user_name=interaction.user.name,
                user_display_name=interaction.user.display_name,
                gold=-self.main_view.so_tien,
            )
            # Credit the host
            ProfileMongoManager.update_profile_money(
                guild_id=interaction.guild_id,
                guild_name=interaction.guild.name,
                user_id=self.main_view.user.id,
                user_name=self.main_view.user.name,
                user_display_name=self.main_view.user.display_name,
                gold=self.main_view.so_tien,
            )

        new_player = PlayerBetInfo(
            user=interaction.user,
            user_profile=self.player_profile,
            horse_id=horse_id,
            so_tien=self.main_view.so_tien,
            loai_tien=self.main_view.loai_tien,
        )
        self.main_view.player_list.append(new_player)

        horse_name = next(
            h["name"] for h in self.main_view.horses_pool if h["id"] == horse_id
        )
        await interaction.response.edit_message(
            content=f"Bạn đã đặt cược thành công cho ngựa **{horse_name}**!", view=None
        )
