from Handling.MiniGame.DuaNgua.DuaNguaView import DuaNguaView
import discord
from discord.ext import commands
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from Handling.Misc.SelfDestructView import SelfDestructView
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
import CustomEnum.UserEnum as UserEnum
import CustomFunctions
import random
from discord.app_commands import Choice
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager


async def setup(bot: commands.Bot):

    await bot.add_cog(DuaNgua(bot=bot))

    print("Dua Ngua game is ready!")


class DuaNgua(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.emoji_pool = ["🐎", "🏇", "🦄", "🦓", "🎠", "🐴"]
        self.prefixes = [
            "Hắc",
            "Bạch",
            "Xích",
            "Thanh",
            "Kim",
            "Lôi",
            "Phong",
            "Vân",
            "Thần",
            "Quỷ",
            "Độc",
            "Phi",
        ]
        self.suffixes = [
            "Lôi Mã",
            "Chiến Mã",
            "Xạ Mã",
            "Huyết Mã",
            "Long Mã",
            "Vương Mã",
            "Tốc Mã",
            "Ảnh Mã",
            "Sát Mã",
            "Truy Mã",
        ]

    # region Dua Ngua
    @discord.app_commands.checks.cooldown(1, 30)
    @discord.app_commands.command(
        name="dua_ngua",
        description="Làm nhà cái tổ chức thi đua ngựa! Không giàu thì đừng cá cược nhé!",
    )
    @discord.app_commands.describe(so_tien="Chọn số tiền cược để tham gia ván đua này.")
    @discord.app_commands.describe(loai_tien="Chọn loại tiền để tham gia cược.")
    @discord.app_commands.describe(
        mult="Chọn tỷ lệ nhận giải. Mặc định người thắng sẽ nhận x2 số tiền đã cược."
    )
    @discord.app_commands.choices(
        loai_tien=[
            Choice(name="Gold", value="G"),
            Choice(name="Silver", value="S"),
            Choice(name="Copper", value="C"),
        ]
    )
    @discord.app_commands.choices(
        mult=[
            Choice(name="x2", value=2),
            Choice(name="x3", value=3),
            Choice(name="x5", value=5),
        ]
    )
    async def dua_ngua_slash_command(
        self,
        interaction: discord.Interaction,
        so_tien: int = None,
        loai_tien: str = None,
        mult: int = 2,
    ):

        await interaction.response.defer(ephemeral=False)
        # Không cho dùng bot nếu không phải user
        if (
            CustomFunctions.check_if_dev_mode()
            and interaction.user.id != UserEnum.UserId.DARKIE.value
        ):
            view = SelfDestructView(timeout=30)

            embed = discord.Embed(
                title="Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",
                color=discord.Color.blue(),
            )

            mess = await interaction.followup.send(
                embed=embed, view=view, ephemeral=True
            )

            view.message = mess
            return

        is_betting = False
        if so_tien is not None and loai_tien is None:
            loai_tien = "C"
            is_betting = True

        if loai_tien is not None and so_tien is None:
            so_tien = 1
            is_betting = True

        if so_tien and loai_tien:
            is_betting = True

        profile = ProfileMongoManager.find_profile_by_id(
            guild_id=interaction.guild_id, user_id=interaction.user.id
        )
        if is_betting and profile is None:
            await interaction.followup.send(
                f"Để cá cược thì bạn phải thực hiện lệnh {SlashCommand.PROFILE.value} trước đã!"
            )
            return
        elif is_betting and profile is not None:
            if loai_tien == "C" and profile.copper < so_tien:
                await interaction.followup.send(
                    f"Bạn không có đủ {EmojiCreation2.COPPER.value} để cá cược!"
                )
                return
            elif loai_tien == "S" and profile.silver < so_tien:
                await interaction.followup.send(
                    f"Bạn không có đủ {EmojiCreation2.SILVER.value} để cá cược!"
                )
                return
            elif loai_tien == "G" and profile.gold < so_tien:
                await interaction.followup.send(
                    f"Bạn không có đủ {EmojiCreation2.GOLD.value} để cá cược!"
                )
                return
        if so_tien is not None and so_tien <= 0:
            await interaction.followup.send("Số tiền nhập không hợp lệ!")
            return

        timeout = 5
        description = f"{interaction.user.mention} đã tổ chức giải đua ngựa."
        if is_betting:
            description += f"\nTiền cược tham gia: **{so_tien}** {UtilitiesFunctions.get_emoji_from_loai_tien(loai_tien)}.\nNgười thắng sẽ nhận x{mult} số tiền cược."
            timeout = 30
        description += f"\nCuộc đua sẽ bắt đầu sau {timeout} giây\n\n{EmojiCreation2.SHINY_POINT.value} Tối đa **8** người có thể tham gia đặt cược!"

        embed = discord.Embed(
            title="Giải Đua Ngựa Mở Rộng",
            description=description,
            color=0x03F8FC,
        )
        horses_pool = self.generate_random_horses()
        track_length = 60
        obstacles = [20, 45]

        for horse in horses_pool:
            embed.add_field(
                name=f"{horse['id']}. {horse['name']}",
                value=f"{UtilitiesFunctions.get_track_string(horse_emoji=horse['emoji'], position=0, track_length=track_length, obstacles=obstacles)}",
                inline=False,
            )
        embed.set_footer(
            text="Nếu ai chưa biết chơi đua ngựa thì cứ nhắn cú pháp\n`dn help`"
        )

        # View
        view = DuaNguaView(
            user=interaction.user,
            horses_pool=horses_pool,
            user_profile=profile,
            so_tien=so_tien,
            loai_tien=loai_tien,
            is_betting=is_betting,
            mult=mult,
            timeout=timeout,
            track_length=track_length,
            obstacles=obstacles,
        )
        mess = await interaction.followup.send(embed=embed, view=view)
        view.message = mess

    def generate_random_horses(self, count=8):
        """Generates a list of unique horse objects for the race."""
        horses = []
        used_names = set()
        while len(horses) < count:
            prefix_chance = UtilitiesFunctions.get_chance(30)
            if prefix_chance:
                prefix = random.choice(self.prefixes)
            else:
                prefix = ""
            name = f"{prefix} {random.choice(self.suffixes)}"
            if name not in used_names:
                used_names.add(name)
                horses.append(
                    {
                        "id": len(horses) + 1,
                        "name": name,
                        "emoji": random.choice(self.emoji_pool),
                    }
                )
        return horses

    @dua_ngua_slash_command.error
    async def dua_ngua_slash_command_error(
        self, interaction: discord.Interaction, error
    ):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True
            )
