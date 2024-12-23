from typing import List, Optional
from datetime import datetime
from Handling.Economy.GA.GuardianAngelClass import GuardianAngel, GuardianAngelSkill
from CustomEnum.EmojiEnum import EmojiCreation2


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
    
    return background_urls
    