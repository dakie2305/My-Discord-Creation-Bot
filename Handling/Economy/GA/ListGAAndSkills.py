from typing import List, Optional
from datetime import datetime
from Handling.Economy.GA.GuardianAngelClass import GuardianAngel, GuardianAngelSkill
from CustomEnum.EmojiEnum import EmojiCreation2
import random
import copy
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions

list_ga_shop_private = [
    GuardianAngel(
      ga_id = "rikka",
      ga_name= "Rikka Tà Vương Nhãn",
      ga_emoji= EmojiCreation2.RIKKA.value,
      stamina = 100,
      max_stamina= 100,
      health= 80,
      max_health= 80,
      mana= 120,
      max_mana= 120,
      attack_power= 20,
      buff_attack_percent = 1,
      worth_amount = 50, 
      worth_type = "D",
    ),
    
    GuardianAngel(
      ga_id = "tatsumaki",
      ga_name= "Tatsumaki Bão Tố",
      ga_emoji= EmojiCreation2.TATSUMAKI.value,
      stamina = 100,
      max_stamina= 100,
      health= 80,
      max_health= 80,
      mana= 120,
      max_mana= 120,
      attack_power= 20,
      buff_attack_percent = 1,
      worth_amount = 50, 
      worth_type = "D",
    ),
    
    GuardianAngel(
      ga_id = "fubuki",
      ga_name= "Fubuki Bão Tuyết",
      ga_emoji= EmojiCreation2.FUBUKI.value,
      stamina = 80,
      max_stamina= 80,
      health= 120,
      max_health= 120,
      mana= 90,
      max_mana= 90,
      buff_attack_percent = 0,
      attack_power= 15,
      worth_amount = 50, 
      worth_type = "D",
    ),
    GuardianAngel(
      ga_id = "makima",
      ga_name= "Makima Thánh Nữ",
      ga_emoji= EmojiCreation2.MAKIMA.value,
      stamina = 120,
      max_stamina= 120,
      health= 100,
      max_health= 100,
      mana= 80,
      max_mana= 80,
      buff_attack_percent = 0,
      attack_power= 15,
      worth_amount = 50, 
      worth_type = "D",
    ),
    
    GuardianAngel(
      ga_id = "reze",
      ga_name= "Reze Quỷ Bom",
      ga_emoji= EmojiCreation2.REZE.value,
      stamina = 110,
      max_stamina= 110,
      health= 100,
      max_health= 100,
      mana= 80,
      max_mana= 80,
      buff_attack_percent = 0,
      attack_power= 15,
      worth_amount = 50, 
      worth_type = "D",
    ),
    
    GuardianAngel(
      ga_id = "asuna",
      ga_name= "Asuna",
      ga_emoji= EmojiCreation2.ASUNA.value,
      stamina = 110,
      max_stamina= 110,
      health= 100,
      max_health= 100,
      mana= 80,
      max_mana= 80,
      buff_attack_percent = 0,
      attack_power= 15,
      worth_amount = 50, 
      worth_type = "D",
    ),
    GuardianAngel(
      ga_id = "megumin",
      ga_name= "Megumin Bộc Liệt Pháp",
      ga_emoji= EmojiCreation2.MEGUMIN.value,
      stamina = 50,
      max_stamina= 50,
      health= 100,
      max_health= 100,
      mana= 130,
      max_mana= 130,
      buff_attack_percent = 1,
      attack_power= 20,
      worth_amount = 50, 
      worth_type = "D",
    ),
    
    GuardianAngel(
      ga_id = "ly_hoa_phuong",
      ga_name= "Lý Hoả Vượng",
      ga_emoji= EmojiCreation2.LY_HOA_PHUONG.value,
      stamina = 100,
      max_stamina= 100,
      health= 100,
      max_health= 100,
      mana= 80,
      max_mana= 80,
      buff_attack_percent = 0,
      attack_power= 15,
      worth_amount = 50, 
      worth_type = "D",
    ),
    
    GuardianAngel(
      ga_id = "shinra",
      ga_name= "Shinra Lính Hoả",
      ga_emoji= EmojiCreation2.SHINRA.value,
      stamina = 100,
      max_stamina= 100,
      health= 100,
      max_health= 100,
      mana= 80,
      max_mana= 80,
      buff_attack_percent = 0,
      attack_power= 15,
      worth_amount = 50, 
      worth_type = "D",
    ),
    
    GuardianAngel(
      ga_id = "hatori_chise",
      ga_name= "Hatori Chise",
      ga_emoji= EmojiCreation2.Hatori_Chise.value,
      stamina = 110,
      max_stamina= 110,
      health= 100,
      max_health= 100,
      mana= 80,
      max_mana= 80,
      buff_attack_percent = 0,
      attack_power= 15,
      worth_amount = 50, 
      worth_type = "D",
    ),
    GuardianAngel(
      ga_id = "raiden_shogun",
      ga_name= "Lôi Thần Raiden Ei",
      ga_emoji= EmojiCreation2.RAIDEN_SHOGUN.value,
      stamina = 80,
      max_stamina= 80,
      health= 100,
      max_health= 100,
      mana= 100,
      max_mana= 100,
      buff_attack_percent = 0,
      attack_power= 15,
      worth_amount = 50, 
      worth_type = "D",
    ),
    GuardianAngel(
      ga_id = "arya",
      ga_name= "Arya",
      ga_emoji= EmojiCreation2.ARYA.value,
      stamina = 100,
      max_stamina= 100,
      health= 100,
      max_health= 100,
      mana= 80,
      max_mana= 80,
      buff_attack_percent = 0,
      attack_power= 15,
      worth_amount = 50, 
      worth_type = "D",
    ),
    GuardianAngel(
      ga_id = "sinon",
      ga_name= "Sinon",
      ga_emoji= EmojiCreation2.SINON.value,
      stamina = 80,
      max_stamina= 80,
      health= 100,
      max_health= 100,
      mana= 100,
      max_mana= 100,
      buff_attack_percent = 0,
      attack_power= 15,
      worth_amount = 50, 
      worth_type = "D",
    ),
    GuardianAngel(
      ga_id = "kurumi",
      ga_name= "Tokisaki Kurumi (Nightmare)",
      ga_emoji= EmojiCreation2.KURUMI.value,
      stamina = 80,
      max_stamina= 80,
      health= 90,
      max_health= 90,
      mana= 120,
      max_mana= 120,
      buff_attack_percent = 0,
      attack_power= 15,
      worth_amount = 50, 
      worth_type = "D",
    ),
    GuardianAngel(
      ga_id = "bocchi",
      ga_name= "Bocchi",
      ga_emoji= EmojiCreation2.BOCCHI.value,
      stamina = 80,
      max_stamina= 80,
      health= 90,
      max_health= 90,
      mana= 120,
      max_mana= 120,
      buff_attack_percent = 0,
      attack_power= 15,
      worth_amount = 50, 
      worth_type = "D",
    ),
    GuardianAngel(
      ga_id = "acheron",
      ga_name= "Raiden Bosenmori Mei",
      ga_emoji= EmojiCreation2.HSR.value,
      stamina = 80,
      max_stamina= 80,
      health= 90,
      max_health= 90,
      mana= 120,
      max_mana= 120,
      buff_attack_percent = 0,
      attack_power= 15,
      worth_amount = 50, 
      worth_type = "D",
    ),
]
list_ga_shop = copy.deepcopy(list_ga_shop_private)

list_ga_skills_private = [
    GuardianAngelSkill(
        skill_id = "skill_blizzard",
        skill_name= "Bão Tuyết",
        skill_desc="Triệu hồi bão tuyết cực mạnh để tấn công kẻ địch! Tăng 5% sức mạnh tấn công và sẽ làm giảm mana của địch!",
        skill_type= ["attack"],
        emoji= EmojiCreation2.BLIZZARD.value,
        attack_power= 30,
        item_worth_amount= 20000,
        item_worth_type= "G",
        percent_min_mana_req= 15,
        mana_loss= 15,
        buff_defense_percent=0,
        buff_attack_percent=5,
        min_level_required=1,
    ),
    GuardianAngelSkill(
        skill_id = "skill_black_fire",
        skill_name= "Hắc Hoả Diệm",
        skill_desc="Triệu hồi Hắc Hoả cực mạnh để tấn công kẻ địch! Sức mạnh sẽ tăng theo tỉ lệ sức mạnh tấn công, và mất 45% mana mỗi khi dùng!",
        skill_type= ["attack"],
        emoji= EmojiCreation2.BLACK_FIRE.value,
        attack_power= 15,
        item_worth_amount= 40000,
        item_worth_type= "G",
        percent_min_mana_req= 40,
        mana_loss= 45,
        buff_defense_percent=0,
        buff_attack_percent=10,
        min_level_required=1,
    ),
    GuardianAngelSkill(
        skill_id = "skill_stun",
        skill_name= "Triệu Lôi",
        skill_desc="Sẽ đánh sốc đối thủ và không cho đối thủ tấn công trong lượt đó, kỹ năng này sẽ mất nhiều mana mỗi khi dùng!",
        skill_type= ["attack"],
        emoji= EmojiCreation2.STUN_SKILL.value,
        attack_power= 20,
        item_worth_amount= 40000,
        item_worth_type= "G",
        percent_min_mana_req= 40,
        mana_loss= 35,
        buff_defense_percent=0,
        buff_attack_percent=5,
        min_level_required=1,
    ),
    GuardianAngelSkill(
        skill_id = "skill_mass_stun",
        skill_name= "Mộc Khắc",
        skill_desc="Triệu hồi sức mạnh đánh sốc cả tổ đội của đối thủ và không cho tổ đội đối thủ tấn công trong lượt đó, kỹ năng này sẽ mất nhiều mana mỗi khi dùng!",
        skill_type= ["attack"],
        emoji= EmojiCreation2.MASS_STUN_SKILL.value,
        attack_power= 1,
        item_worth_amount= 60000,
        item_worth_type= "G",
        percent_min_mana_req= 50,
        mana_loss= 40,
        buff_defense_percent=0,
        buff_attack_percent=5,
        min_level_required=1,
    ),
    GuardianAngelSkill(
        skill_id = "skill_explosion_spell",
        skill_name= "Bộc Liệt Ma Pháp",
        skill_desc="Kỹ năng quen thuộc của Megumin, hy sinh tất cả mana và thể lực để dồn vào một chiêu Bộc Phá duy nhất với sức mạnh khủng khiếp!",
        skill_type= ["attack"],
        emoji= EmojiCreation2.EXPLOSION_SPELL_SKILL.value,
        attack_power= 100,
        item_worth_amount= 60000,
        item_worth_type= "G",
        percent_min_mana_req= 50,
        mana_loss= 35,
        buff_defense_percent=0,
        buff_attack_percent=5,
        min_level_required=1,
    ),
    GuardianAngelSkill(
        skill_id = "skill_potion_destroyer",
        skill_name= "Phá Dược Tiễn",
        skill_desc="Kỹ năng này sẽ phá hủy một số lượng ngẫu nhiên các bình hồi phục của kẻ địch để ngăn kẻ địch lạm dụng chúng!",
        skill_type= ["attack"],
        emoji= EmojiCreation2.POTION_DESTROYER_SKILL.value,
        attack_power= 25,
        item_worth_amount= 60000,
        item_worth_type= "G",
        percent_min_mana_req= 45,
        mana_loss= 35,
        buff_defense_percent=0,
        buff_attack_percent=5,
        min_level_required=1,
    ),
    GuardianAngelSkill(
        skill_id = "skill_trade_stats",
        skill_name= "Tiễn Chỉ Số",
        skill_desc="Kỹ năng này sẽ dùng Thể Lực hoặc Mana của bản thân để phá Thể Lực hoặc Mana của kẻ địch để khắc chế!",
        skill_type= ["attack"],
        emoji= EmojiCreation2.TRADE_STATS_SKILL.value,
        attack_power= 25,
        item_worth_amount= 60000,
        item_worth_type= "G",
        percent_min_mana_req= 50,
        mana_loss= 35,
        buff_defense_percent=0,
        buff_attack_percent=5,
        min_level_required=1,
    ),
    GuardianAngelSkill(
        skill_id = "skill_mass_damage",
        skill_name= "Hỏa Trụ",
        skill_desc="Triệu hồi cột lửa thiêu đốt cả tổ đội của đối thủ, kỹ năng này sẽ mất nhiều mana mỗi khi dùng!",
        skill_type= ["attack"],
        emoji= EmojiCreation2.FIRE_COLL.value,
        attack_power= 1,
        item_worth_amount= 60000,
        item_worth_type= "G",
        percent_min_mana_req= 50,
        mana_loss= 50,
        buff_defense_percent=0,
        buff_attack_percent=5,
        min_level_required=1,
    ),
]
list_ga_skills = copy.deepcopy(list_ga_skills_private)

list_ga_passive_skills_private = [
  GuardianAngelSkill(
        skill_id = "skill_run_away",
        skill_name= "Tẩu Vi Thượng Sách",
        skill_desc="Trong ba mươi sáu kế, bỏ chạy là thượng sách! Khi máu dưới 15% thì Hộ Vệ Thần sẽ chạy trốn để bảo toàn tính, sẽ mất hết mana và thể lực!",
        skill_type= ["passive"],
        emoji= EmojiCreation2.RUN_AWAY.value,
        attack_power= 1,
        item_worth_amount= 40000,
        item_worth_type= "G",
        percent_min_mana_req= 10,
        mana_loss= 45,
        buff_defense_percent=0,
        buff_attack_percent=1,
        min_level_required=1,
    ),
    GuardianAngelSkill(
        skill_id = "skill_critical_strike",
        skill_name= "Ngưỡng Máu Tử",
        skill_desc="Khi Hộ Vệ Thần còn máu dưới 30% thì các đòn tấn công tiếp theo sẽ tăng sát thương, chỉ kích hoạt một lần!",
        skill_type= ["passive"],
        emoji= EmojiCreation2.CRITICAL_DAMAGE.value,
        attack_power= 15,
        item_worth_amount= 40000,
        item_worth_type= "G",
        percent_min_mana_req= 10,
        mana_loss= 45,
        buff_defense_percent=0,
        buff_attack_percent=1,
        min_level_required=1,
    ),
    GuardianAngelSkill(
        skill_id = "summoning_skill",
        skill_name= "Triệu Linh",
        skill_desc="Khi tổ đội dưới ba người thì sẽ có thể dùng 50% mana để triệu hồi một cấp dưới có cấp bằng một nửa người triệu hồi! Có 5% tỉ lệ triệu hồi NPC mạnh hơn gấp hai lần!",
        skill_type= ["passive"],
        emoji= EmojiCreation2.SUMMONING_SKILL.value,
        attack_power= 1,
        item_worth_amount= 75000,
        item_worth_type= "G",
        percent_min_mana_req= 45,
        mana_loss= 50,
        buff_defense_percent=0,
        buff_attack_percent=1,
        min_level_required=1,
    ),
    GuardianAngelSkill(
        skill_id = "mass_heal_skill",
        skill_name= "Phục Sức Pháp",
        skill_desc="Khi tổ đội còn thấp máu sẽ hồi phục 15% máu cho cả tổ đội khi cả tổ đội yếu máu! Kỹ năng này tốn rất nhiều mana!",
        skill_type= ["passive"],
        emoji= EmojiCreation2.MASS_HEAL_SKILL.value,
        attack_power= 1,
        item_worth_amount= 55000,
        item_worth_type= "G",
        percent_min_mana_req= 35,
        mana_loss= 35,
        buff_defense_percent=0,
        buff_attack_percent=1,
        min_level_required=1,
    ),
    GuardianAngelSkill(
        skill_id = "mass_restored_mana_skill",
        skill_name= "Hồi Pháp",
        skill_desc="Khi tổ đội còn thấp mana sẽ hồi phục 20% mana cho cả tổ đội! Kỹ năng này chỉ kích hoạt hai lần trong một trận!",
        skill_type= ["passive"],
        emoji= EmojiCreation2.MASS_MANA_SKILL.value,
        attack_power= 1,
        item_worth_amount= 55000,
        item_worth_type= "G",
        percent_min_mana_req= 35,
        mana_loss= 35,
        buff_defense_percent=0,
        buff_attack_percent=1,
        min_level_required=1,
    ),
    GuardianAngelSkill(
        skill_id = "brain_wash_skill",
        skill_name= "Tẩy Não",
        skill_desc="Nếu tổ đội mình dưới ba người thì sẽ tẩy não một kẻ địch qua phe mình trong một vài lượt chơi! Kỹ năng này sẽ tốn rất nhiều mana!",
        skill_type= ["passive"],
        emoji= EmojiCreation2.BRAINWASH_SKILL.value,
        attack_power= 1,
        item_worth_amount= 45000,
        item_worth_type= "G",
        percent_min_mana_req= 35,
        mana_loss= 35,
        buff_defense_percent=0,
        buff_attack_percent=1,
        min_level_required=1,
    ),
]
list_ga_passive_skills = copy.deepcopy(list_ga_passive_skills_private)

list_ga_passive_skills_private_2 = [
  GuardianAngelSkill(
        skill_id = "skill_resurrection",
        skill_name= "Trỗi Dậy",
        skill_desc="Hồi sinh tất cả đồng đội đã gục ngã trong tổ đội và hồi 30% chỉ số, phe địch sẽ được hồi 50% máu! Chỉ dùng được một lần trong trận chiến!",
        skill_type= ["passive"],
        emoji= EmojiCreation2.RESURRECTION_SKILL.value,
        attack_power= 1,
        item_worth_amount= 50000,
        item_worth_type= "G",
        percent_min_mana_req= 10,
        mana_loss= 45,
        buff_defense_percent=0,
        buff_attack_percent=1,
        min_level_required=1,
    ),
  GuardianAngelSkill(
        skill_id = "skill_spike_arnour",
        skill_name= "Thống Khổ Giáp",
        skill_desc="Sẽ phản lại 35% sát thương đã nhận từ đòn tấn công bình thường, và 10% khả năng gây choáng kẻ địch. Kỹ năng này sẽ mất mana mỗi khi trúng đòn!",
        skill_type= ["passive"],
        emoji= EmojiCreation2.SPIKE_AMOUR.value,
        attack_power= 15,
        item_worth_amount= 50000,
        item_worth_type= "G",
        percent_min_mana_req= 20,
        mana_loss= 20,
        buff_defense_percent=0,
        buff_attack_percent=1,
        min_level_required=1,
    ),
  GuardianAngelSkill(
        skill_id = "skill_self_explosion",
        skill_name= "Tự Kích",
        skill_desc="Khi máu dưới 10% sẽ tự động kích nổ bản thân, gây sát thương lên tất cả mọi người trong cuộc chiến, và làm giảm 40% phần thưởng nhận được!",
        skill_type= ["passive"],
        emoji= EmojiCreation2.SELF_EXPLOSION_SKILL.value,
        attack_power= 100,
        item_worth_amount= 50000,
        item_worth_type= "G",
        percent_min_mana_req= 20,
        mana_loss= 20,
        buff_defense_percent=0,
        buff_attack_percent=1,
        min_level_required=1,
    ),
]
list_ga_passive_skills_2 = copy.deepcopy(list_ga_passive_skills_private_2)


all_skill_lists = [list_ga_skills, list_ga_passive_skills, list_ga_passive_skills_2]

def get_list_back_ground_on_ga_id(ga_id: str):
    background_urls = None
    if ga_id == "fubuki":
        background_urls = [
          "https://i.pinimg.com/originals/f4/1d/7d/f41d7d000c0b8251eaa684ee1d3af768.gif",
          "https://i.pinimg.com/736x/c8/2c/66/c82c66730d12a0c2e8894cee859697e8.jpg",
          "https://i.pinimg.com/originals/c2/7a/53/c27a53e45fa5cdda4121ed1db72d0d6c.gif",
          "https://i.pinimg.com/originals/e6/2e/f0/e62ef010bb2bca2fd5acaaaf64b5e7e0.gif",
          "https://i.pinimg.com/originals/20/b9/47/20b9477b3d421428cb4d343fe969111b.gif",
          "https://i.pinimg.com/originals/94/fd/67/94fd67776353c7901400d3ed9e88b838.gif",
      ]
    elif ga_id == "tatsumaki":
        background_urls = [
          "https://i.pinimg.com/originals/53/5b/10/535b109c17160c380788aae3a0547d9a.gif",
          "https://i.pinimg.com/originals/8e/70/ab/8e70abc971f4d690fc021e1bba9c7ac8.gif",
          "https://i.pinimg.com/originals/bd/4c/4e/bd4c4e1cedbe6c2d1d186aec4eee62bc.gif",
          "https://i.pinimg.com/originals/d1/ad/f5/d1adf5f6ad9c318066a1c5e250e86e85.gif",
          "https://i.pinimg.com/736x/17/8f/eb/178febfb63859f94cbdee980ebbb8eae.jpg",
          "https://i.pinimg.com/originals/bd/2c/6f/bd2c6f155472ade0bdeb28769b14ca21.gif",
          "https://i.pinimg.com/originals/c4/e1/86/c4e186c336d1b7f0b16196d6432e1d99.gif",
      ]
    elif ga_id == "ly_hoa_phuong":
        background_urls = [
          "https://i.pinimg.com/736x/6d/c0/4d/6dc04df23e7f80cc1702aaf3340da762.jpg",
          "https://i.pinimg.com/736x/a3/58/13/a3581374991998a569b9739e465c58a1.jpg",
          "https://i.pinimg.com/736x/33/a1/b5/33a1b557b76d02cda2f1a65f64974547.jpg",
          "https://i.pinimg.com/736x/09/9a/8e/099a8ecb9ede5a8abe6e1722712d6959.jpg",
          "https://i.pinimg.com/736x/f6/8e/40/f68e40474ca2fc8137991c50b44c09b5.jpg",
      ]
    elif ga_id == "shinra":
        background_urls = [
          "https://i.pinimg.com/originals/f0/e3/41/f0e341329cb46cd97c341384961f3f1e.gif",
          "https://i.pinimg.com/originals/cb/87/c2/cb87c206fb0e30728129fcb474f2ce52.gif",
          "https://i.pinimg.com/originals/0d/28/4a/0d284ad1925736d14f087072a778232f.gif",
          "https://i.pinimg.com/originals/b2/3f/a0/b23fa027f9faca52267ff7d37e393c01.gif",
          "https://i.pinimg.com/originals/2f/f7/94/2ff794c670ac411307a0f08953936612.gif",
      ]
    elif ga_id == "hatori_chise":
        background_urls = [
          "https://i.pinimg.com/originals/66/4f/d3/664fd36dfdf564cb7921596f05996fdd.gif",
          "https://i.pinimg.com/originals/32/70/14/327014699a9f31e46f8c41234b7aa273.gif",
          "https://i.pinimg.com/originals/1f/36/9c/1f369c2b68948d693df4b7936a3a3cf9.gif",
          "https://i.pinimg.com/originals/19/40/96/194096b4f2d9aac21842e56dc1816187.gif",
      ]
        
    elif ga_id == "makima":
        background_urls = [
          "https://i.pinimg.com/originals/03/cf/8d/03cf8d2a1d1b5df4dadda7242a913c86.gif",
          "https://i.pinimg.com/originals/a3/5f/7c/a35f7cceadbeddbfad284e7ce52adca1.gif",
          "https://i.pinimg.com/originals/7b/2a/fa/7b2afa88054b838298878346ab755eb7.gif",
          "https://i.pinimg.com/originals/d0/d0/f4/d0d0f497e74132aac08104ea8619e264.gif",
          "https://i.pinimg.com/originals/75/c8/48/75c8489a77f759c252b479a491a83fe1.gif",
          "https://i.pinimg.com/originals/eb/f3/05/ebf3058849bd022783acf7619631726a.gif",
          "https://i.pinimg.com/originals/82/1e/50/821e50a729b8abd7317404090ecf4d34.gif",
          "https://i.pinimg.com/originals/ab/8e/46/ab8e46bfddf37c093c3f27c06c3c325f.gif",
      ]
        
    elif ga_id == "reze":
        background_urls = [
          "https://i.pinimg.com/originals/06/f9/7b/06f97b762d33c085a2c2555c8d876fb3.gif",
          "https://i.pinimg.com/originals/c4/95/90/c495906bdc63b24dfd9e44099616a5f4.gif",
          "https://i.pinimg.com/originals/8f/af/9b/8faf9bce78098e045fa8ec1be704ded4.gif",
          "https://i.pinimg.com/736x/bc/00/0d/bc000d718edad04d7649ae93538b00a7.jpg",
          "https://i.pinimg.com/736x/e0/2f/6f/e02f6fca529f94d4a694dd6544994150.jpg",
          "https://i.pinimg.com/736x/c3/1a/07/c31a073d99379f64e66dd2aa88599623.jpg",
      ]
    elif ga_id == "rikka":
        background_urls = [
          "https://i.pinimg.com/originals/b7/29/f6/b729f606499c57d3f36d7cd3ec7641c7.gif",
          "https://i.pinimg.com/originals/5e/f2/53/5ef2537d03e46c1cd5d392aea7b9f2fc.gif",
          "https://i.pinimg.com/originals/4f/cc/7e/4fcc7e493d0e45a3a8c91b9a862e2418.gif",
          "https://i.pinimg.com/originals/9f/e2/47/9fe247b1a5a4ba33c4f84fd47efecc0d.gif",
          "https://i.pinimg.com/originals/a5/1e/d5/a51ed53343d5a126b542fe2481d617b0.gif",
          "https://i.pinimg.com/originals/ce/9a/22/ce9a226c5950181cc6e3b4cab4c0d4b8.gif",
          "https://i.pinimg.com/originals/80/6c/f4/806cf4a613ad2467eb4f442cbd3c0cdf.gif",
          "https://i.pinimg.com/originals/f2/64/2c/f2642c3783a6485716ef39d437f31fc9.gif",
          "https://i.pinimg.com/originals/dd/3e/4f/dd3e4f6d242ecad5738731da333a592c.gif",
          "https://i.pinimg.com/originals/18/53/cc/1853cc9948053434410ccbdcd52d535c.gif",
          "https://i.pinimg.com/originals/41/d2/ec/41d2ec3fe5361a91360ae35a842e4bd7.gif",
          "https://i.pinimg.com/originals/51/91/da/5191dafcca04f3b198f14987a1541ac6.gif",
          "https://i.pinimg.com/originals/fd/72/6e/fd726e7a345a047d163a15a5d8c1794b.gif",
          "https://i.pinimg.com/originals/80/6c/f4/806cf4a613ad2467eb4f442cbd3c0cdf.gif",
          "https://i.pinimg.com/originals/86/09/2c/86092cbc580fedcd766a80ace9d2bcc3.gif",
      ]
    elif ga_id == "asuna":
        background_urls = [
          "https://i.imgur.com/BNhnFUa.gif",
          "https://i.imgur.com/vxAfOTD.gif",
          "https://i.imgur.com/Sf1nSL2.gif",
          "https://i.imgur.com/beX7Rdv.gif",
          "https://i.imgur.com/Wl3XhD9.gif",
      ]
    elif ga_id == "arya":
        background_urls = [
          "https://i.imgur.com/k0PYV3m.gif",
          "https://i.imgur.com/NM3cLrO.gif",
          "https://i.pinimg.com/originals/c4/85/31/c48531f47f49424a03f8e318a183b054.gif",
          "https://i.pinimg.com/originals/53/0f/1c/530f1c7b35e8928c5ff55f60378dcf10.gif",
          "https://i.pinimg.com/originals/0d/b6/b7/0db6b741356175283bb6196d897a7c83.gif",
          "https://i.pinimg.com/originals/e8/bf/be/e8bfbebed33f24afe110314867ffae84.gif",
          "https://i.pinimg.com/originals/91/1f/f6/911ff6a5913ed95b4af78ab454184e88.gif",
      ]
    elif ga_id == "megumin":
        background_urls = [
          "https://i.imgur.com/mV9rL6d.png",
          "https://i.imgur.com/264hrSD.gif",
          "https://i.imgur.com/MDuDDqU.gif",
          "https://i.imgur.com/otds392.gif",
          "https://i.imgur.com/YHxQRW3.gif",
      ]
    elif ga_id == "sinon":
        background_urls = [
          "https://i.imgur.com/mfK6VO9.gif",
          "https://i.imgur.com/HrEfEin.gif",
          "https://i.imgur.com/5E8PS2P.gif",
          "https://i.imgur.com/MNPXmwO.gif",
          "https://i.imgur.com/PvugtRT.gif",
      ]
    elif ga_id == "kurumi":
        background_urls = [
          "https://i.imgur.com/VipwvbX.gif",
          "https://i.imgur.com/2EC7Rna.gif",
          "https://i.imgur.com/Y6SnZyz.gif",
          "https://i.imgur.com/qvg07tV.gif",
          "https://i.imgur.com/PNWfSnU.gif",
          "https://i.imgur.com/h3M7iMJ.gif",
          "https://i.imgur.com/ZhE1NhQ.gif",
      ]
    elif ga_id == "bocchi":
        background_urls = [
          "https://i.imgur.com/UbgIkur.gif",
          "https://i.imgur.com/3coxE09.gif",
          "https://i.imgur.com/AUucKgg.gif",
          "https://i.imgur.com/Righ4eG.gif",
          "https://i.imgur.com/VdBw3zn.gif",
          "https://i.imgur.com/b8QtGJL.gif",
      ]
        
    elif ga_id == "acheron":
        background_urls = [
          "https://i.pinimg.com/originals/ab/c3/83/abc3834108d988cb0e798c4962f2317c.gif",
          "https://i.pinimg.com/originals/2e/71/f5/2e71f5dc05797aefc00ab7ebfe42d253.gif",
          "https://steamuserimages-a.akamaihd.net/ugc/2476494829524673254/486E1BF9CD53948FB4135D7726C44EE044E6CF3F/?imw=637&imh=358&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true",
          "https://i.pinimg.com/originals/23/98/c4/2398c4cea3a7f072ecf614f127422b91.gif",
          "https://c4.wallpaperflare.com/wallpaper/980/181/137/honkai-star-rail-robin-honkai-star-rail-red-lipstick-anime-girls-paper-umbrellas-hd-wallpaper-preview.jpg",
      ]
    elif ga_id == "raiden_shogun":
        background_urls = [
            "https://i.imgur.com/aIB624X.gif",
            "https://i.imgur.com/oIjq031.gif",
            "https://i.imgur.com/mwhZYDP.gif",
            "https://i.imgur.com/2iZOjxd.gif",
      ]
    elif ga_id == "":
        background_urls = [
            "https://i.imgur.com/aIB624X.gif",
      ]
    return background_urls

def get_random_skill(skill_id: str = None, blacklist_ids: List[str]= None):
  if blacklist_ids is None:
    blacklist_ids = []

  #Nếu có skill name thì ưu tiên tìm xem có skill name không
  if skill_id != None:
    for skill_list in all_skill_lists:
      for skill in skill_list:
        if skill.skill_id == skill_id and skill.skill_id not in blacklist_ids:
          return skill
  else:
    #Nếu không thì random bình thường
    random_skill_list = random.choice(all_skill_lists)
    random_skill = random.choice(random_skill_list)
    if random_skill.skill_id not in blacklist_ids: return random_skill
  return None


def get_random_ga_enemy_generic(level: int = 1, guardian_chance: int = 0, override_name: str = None, override_emoji: str = None):
    data = GuardianAngel(
        ga_id = "enemy_generic",
        ga_name= "",
        ga_emoji= "",
        stamina = 80,
        max_stamina= 80,
        health= 120,
        max_health= 120,
        mana= 90,
        max_mana= 90,
        buff_attack_percent = 0,
        attack_power= 15,
        worth_amount = 50, 
        worth_type = "D",
    )
    
    list_name_emojis = [
        ("Lính Gác", "👮"),
        ("Binh Lính", "💂"),
        ("Vệ Binh", "🕵️‍♂️"),
        ("Ninja", "🥷"),
        ("Cướp", "🦹‍♂️"),
        ("Tướng Cướp", "🦹‍♂️"),
        ("Zombie", "🧟‍♂️"),
        ("Quái Zombie", "🧟‍♀️"),
        ("Ma Nữ Zombie", "🧟"),
        ("Sĩ Binh", "👩‍🏭"),
        ("Địch Nhân", "🥷"),
        ("Ma Cà Rồng", "🧛‍♂️"),
        ("Triệu Hồi Cà Rồng", "🧛‍♂️"),
        ("Quái Vật", "👾"),
        ("Quái Thú", "👾"),
        ("Tà Quỷ", "👿"),
        ("Dâm Quỷ", "👿"),
        ("Quỷ Dữ", "👹"),
        ("Đại Quỷ", "👺"),
        ("Chúa Tể Vampire", "🧛‍♂️"),
        ("Băng Đảng Astraliệt", "👩‍🦼"),
        ("Orge", "🧌"),
        ("Orc", "🧌"),
        ("Quái Nhân", "🧌"),
        ("Pháp Sư", "🧙‍♂️"),
        ("Đại Pháp Sư", "🧙‍♂️"),
        ("Nhất Viên Pháp Sư", "🧙"),
        ("Đại Thần Pháp Sư", "🧙"),
        ("Tiên Quỷ", "🧚‍♂️"),
        ("Pháp Sư Tiên", "🧚‍♂️"),
        ("Big Foot", "👣"),
        ("Xác Sống", "🧟‍♂️"),
        ("Báo Đời Đom Đóm", "🐆"),
        ("Triệu Hồi Sư", "🧙‍♂️"),
        ("Quỷ Triệu Hồi", "👺"),
    ]
    
    #dựa trên level để tăng giảm stats của kẻ địch
    random_level_bonus = random.randint(-3, 7)
    if level < 10:
        random_level_bonus = random.randint(-1, 2)
    elif level >= 10 and level < 20:
        random_level_bonus = random.randint(2, 5)
    elif level >= 20 and level < 30:
        random_level_bonus = random.randint(1, 6)
    elif level >= 30 and level < 40:
        random_level_bonus = random.randint(2, 7)
    elif level >= 40 and level < 50:
        random_level_bonus = random.randint(3, 7)
    elif level >= 50 and level < 75:
        random_level_bonus = random.randint(4, 6)
    elif level >= 75 and level < 85:
        random_level_bonus = random.randint(3, 7)
    else:
        random_level_bonus = random.randint(3, 12)
    
    data.level = level + random_level_bonus
    if data.level <= 0: data.level = 1
    percent_boost = 5
    base = 20
    bonus_base = 30
    data.attack_power = base + bonus_base*int(percent_boost * data.level / 100) #tăng 5% mỗi level
    
    percent_boost = 6
    base = 100
    bonus_base = 100
    data.max_stamina = base + bonus_base*int(percent_boost * data.level / 100)
    data.stamina = data.max_stamina
    
    percent_boost = 5
    base = 100
    bonus_base = 110
    data.max_health = base + bonus_base*int(percent_boost * data.level / 100)
    data.health = data.max_health
    
    percent_boost = 8
    base = 50
    bonus_base = 105
    data.max_mana = base + bonus_base*int(percent_boost * data.level / 100)
    data.mana = data.max_mana
    
    data.buff_attack_percent = random.randint(0, 5)
    data.bonus_dignity_point = random.randint(0, 10)
    data.bonus_exp = random.randint(10, 50)
    data.bonus_exp = data.bonus_exp + data.bonus_exp*int(data.level/10)
    if data.bonus_exp > 100: data.bonus_exp = 100
    
    name, emoji = random.choice(list_name_emojis)
    data.ga_name = name
    data.ga_emoji = emoji
    
    if override_name != None:
      data.ga_name = override_name
    if override_emoji != None:
      data.ga_emoji = override_emoji
    
    #Nếu level của bản thân đã trên 50 thì mọi kẻ địch đều sẽ sở hữu ít nhất một skill
    if level > 50:
        skill = get_random_skill(blacklist_ids=["summoning_skill"])
        if skill != None: data.list_skills.append(skill)
        #random xem có ra guardian không
        if guardian_chance <= 0: guardian_chance = 15
        dice = UtilitiesFunctions.get_chance(guardian_chance)
        if dice:
            random_guardian = copy.deepcopy(random.choice(list_ga_shop))
            data.ga_name = random_guardian.ga_name
            data.ga_emoji = random_guardian.ga_emoji
            skill = get_random_skill()
            if skill != None: data.list_skills.append(skill)

    if data.level > 80:
        #Quái trên 80 thì đương nhiên hưởng thêm skill nữa
        skill = get_random_skill(blacklist_ids=["summoning_skill"])
        if skill != None: data.list_skills.append(skill)
    if data.level > 100:
        #Quái trên 100 thì đương nhiên hưởng thêm skill nữa
        skill = get_random_skill(blacklist_ids=["summoning_skill"])
        if skill != None: data.list_skills.append(skill)
    
    if "Triệu Hồi" in data.ga_name:
        skill = get_random_skill("summoning_skill")
        data.list_skills.append(skill)
        
    if "Megumin" in data.ga_name:
      skill = get_random_skill("skill_explosion_spell")
      if skill: data.list_skills.append(skill)
      
    if "Pháp Sư" in data.ga_name and level >= 25:
        #Tăng mana
        data.max_mana += base + base*int(percent_boost * data.level / 100)
        data.mana = data.max_mana
        #Cộng skill
        skill = get_random_skill(blacklist_ids=["summoning_skill"])
        if skill != None: data.list_skills.append(skill)
    return data