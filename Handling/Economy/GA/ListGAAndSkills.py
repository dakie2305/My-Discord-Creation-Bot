from typing import List, Optional
from datetime import datetime
from Handling.Economy.GA.GuardianAngelClass import GuardianAngel, GuardianAngelSkill
from CustomEnum.EmojiEnum import EmojiCreation2
import random

list_ga_shop = [
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
]


list_ga_skills = [
    GuardianAngelSkill(
        skill_id = "skill_blizzard",
        skill_name= "Bão Tuyết",
        skill_desc="",
        skill_type= "attack",
        emoji= EmojiCreation2.BLIZZARD.value,
        attack_power= 15,
        item_worth_amount= 100,
        item_worth_type= "G",
        percent_min_mana_req= 30,
        mana_loss= 15,
        buff_defense_percent=0,
        buff_attack_percent=5,
        min_level_required=1,
    ),
]


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
          "https://i.pinimg.com/736x/a0/f8/9b/a0f89b3d9917fd279e93a3aac69b8e7f.jpg",
          "https://i.pinimg.com/736x/a3/58/13/a3581374991998a569b9739e465c58a1.jpg",
          "https://i.pinimg.com/736x/33/a1/b5/33a1b557b76d02cda2f1a65f64974547.jpg",
      ]
    elif ga_id == "shinra":
        background_urls = [
          "https://i.pinimg.com/originals/f0/e3/41/f0e341329cb46cd97c341384961f3f1e.gif",
          "https://i.pinimg.com/originals/cb/87/c2/cb87c206fb0e30728129fcb474f2ce52.gif",
          "https://i.pinimg.com/originals/0d/28/4a/0d284ad1925736d14f087072a778232f.gif",
          "https://i.pinimg.com/originals/b2/3f/a0/b23fa027f9faca52267ff7d37e393c01.gif",
          "https://i.pinimg.com/originals/2f/f7/94/2ff794c670ac411307a0f08953936612.gif",
      ]
    
    return background_urls

def get_random_ga_enemy_generic(level: int = 1):
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
        ("Nhất Viên Sư", "🧙"),
        ("Tiên Quỷ", "🧚‍♂️"),
        ("Big Foot", "👣"),
        ("Xác Sống", "🧟‍♂️"),
        ("Báo Đời Đom Đóm", "🐆"),
    ]
    
    #dựa trên level để tăng giảm stats của kẻ địch
    random_level_bonus = random.randint(-3, 7)
    if level < 10:
        random_level_bonus = random.randint(-3, 5)
    elif level > 10 and level < 20:
        random_level_bonus = random.randint(4, 10)
    elif level > 20 and level < 30:
        random_level_bonus = random.randint(6, 10)
    elif level > 30 and level < 40:
        random_level_bonus = random.randint(3, 15)
    elif level > 40 and level < 50:
        random_level_bonus = random.randint(5, 15)
    else:
        random_level_bonus = random.randint(6, 15)
    
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
    
    percent_boost = 5
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
    
    return data