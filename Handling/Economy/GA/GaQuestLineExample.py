
from Handling.Economy.GA.GaQuestClass import GuardianQuestLines, NextSteps

#region quest ghost of the forrest
quest_ghost_of_forrest = [
    GuardianQuestLines(
        id="start",
        title="Linh Hồn Lang Thang Của Khu Rừng Cổ",
        description="Một cảm giác lạnh lẽo bao trùm khu rừng cổ, nơi những linh hồn bị mắc kẹt. {guardian.ga_name} cau mày. 'Tôi cảm nhận được sự đau khổ sâu sắc. Có lẽ chúng ta nên điều tra.'",
        choice_a="Đi sâu vào khu rừng cổ.",
        choice_b="Tìm hiểu về lịch sử khu rừng trước.",
        choice_c="Bỏ qua, linh hồn không phải mối bận tâm của mình.",
        choice_timeout="{guardian.ga_name} nhìn bạn đầy lo lắng. 'Những linh hồn đó cần được giải thoát, chủ nhân!'",
        next_steps=NextSteps(
            choice_a="enter_ancient_forest",
            choice_b="research_forest_history",
            choice_c="ignore_spirits_outcome",
            timeout="ga_worried_timeout_3"
        ),
        gold=10, silver=100, ga_exp=10, dignity_point=5
    ),

    GuardianQuestLines(
        id="enter_ancient_forest",
        title="Bước Chân Vào Vùng Đất Của Linh Hồn",
        description="Bạn và {guardian.ga_name} tiến vào khu rừng cổ. Cây cối già nua vặn vẹo, và những tiếng thì thầm khe khẽ vang vọng. {guardian.ga_name} chỉ về phía một ánh sáng mờ ảo. 'Có vẻ một linh hồn đang mắc kẹt ở đó.'",
        choice_a="Tiếp cận linh hồn để giao tiếp.",
        choice_b="Quan sát từ xa để đánh giá.",
        choice_c="Tìm đường vòng, tránh xa linh hồn đó.",
        choice_timeout="{guardian.ga_name} thúc giục. 'Chúng ta cần hành động nhanh trước khi linh hồn tan biến!'",
        next_steps=NextSteps(
            choice_a="approach_spirit",
            choice_b="observe_spirit_from_afar",
            choice_c="avoid_spirit_outcome",
            timeout="spirit_fades_timeout"
        )
    ),

    GuardianQuestLines(
        id="research_forest_history",
        title="Tìm Hiểu Lịch Sử Rừng",
        description="Bạn và {guardian.ga_name} đến thư viện cổ gần nhất. Bạn tìm thấy một cuốn sách nói về một lời nguyền cổ đại đã giam cầm những linh hồn trong khu rừng. Cách hóa giải lời nguyền là tìm 'Cổ Vật Thanh Tẩy'.",
        choice_a="Tìm kiếm Cổ Vật Thanh Tẩy.",
        choice_b="Trở lại khu rừng, thử cách khác.",
        choice_c="Từ bỏ nhiệm vụ vì quá phức tạp.",
        choice_timeout="{guardian.ga_name} nói. 'Chúng ta không có nhiều thời gian để tìm kiếm đâu!'",
        next_steps=NextSteps(
            choice_a="seek_purifying_artifact",
            choice_b="enter_ancient_forest",
            choice_c="abandon_quest_ancient_forest",
            timeout="ga_worried_timeout_3"
        )
    ),

    GuardianQuestLines(
        id="approach_spirit",
        title="Tiếp Cận Linh Hồn",
        description="Bạn và {guardian.ga_name} tiến đến gần linh hồn. Nó hiện ra như một bóng ma mờ ảo, run rẩy trong đau khổ. {guardian.ga_name} dịu dàng nói: 'Đừng sợ, chúng tôi đến để giúp đỡ.'",
        choice_a="Cố gắng trấn an linh hồn.",
        choice_b="Thử thanh tẩy linh hồn bằng phép thuật.",
        choice_c="Hỏi linh hồn về nguyên nhân mắc kẹt.",
        choice_timeout="Linh hồn gầm gừ, có vẻ như nó không tin tưởng bạn. 'Nó đang trở nên bất ổn!' {guardian.ga_name} cảnh báo.",
        next_steps=NextSteps(
            choice_a="soothe_spirit",
            choice_b="purify_spirit_attempt",
            choice_c="ask_spirit_cause",
            timeout="spirit_anger_outcome"
        )
    ),

    GuardianQuestLines(
        id="observe_spirit_from_afar",
        title="Quan Sát Từ Xa",
        description="Bạn và {guardian.ga_name} ẩn mình quan sát linh hồn. Nó phát ra những tiếng than vãn và dường như đang tìm kiếm thứ gì đó. {guardian.ga_name} nhận ra: 'Nó đang tìm kiếm sự bình yên.'",
        choice_a="Tiếp cận và cố gắng giúp nó tìm sự bình yên.",
        choice_b="Tìm cách để linh hồn tự giải thoát.",
        choice_c="Rút lui khỏi khu rừng.",
        choice_timeout="{guardian.ga_name} thúc giục. 'Chúng ta không thể cứ đứng nhìn mãi được!'",
        next_steps=NextSteps(
            choice_a="approach_spirit",
            choice_b="let_spirit_be_outcome",
            choice_c="retreat_from_forest",
            timeout="spirit_fades_timeout"
        )
    ),

    GuardianQuestLines(
        id="seek_purifying_artifact",
        title="Tìm Kiếm Cổ Vật Thanh Tẩy",
        description="Bạn và {guardian.ga_name} đi theo chỉ dẫn trong sách, đến một ngôi đền cổ bị lãng quên. Cổ Vật Thanh Tẩy nằm trên bệ đá giữa ngôi đền, được bảo vệ bởi những tàn dư của lời nguyền.",
        choice_a="Tiến lên lấy cổ vật.",
        choice_b="Tìm cách vô hiệu hóa lời nguyền trước.",
        choice_c="Kiểm tra xem có cạm bẫy nào không.",
        choice_timeout="{guardian.ga_name} nói. 'Cổ vật ở ngay trước mắt chúng ta, chủ nhân!'",
        next_steps=NextSteps(
            choice_a="take_artifact",
            choice_b="deactivate_curse_first",
            choice_c="check_for_traps",
            timeout="artifact_disappears_timeout"
        )
    ),

    # Final Stage Outcomes
    GuardianQuestLines(
        id="soothe_spirit",
        title="Linh Hồn Được An Ủi",
        description="Bạn và {guardian.ga_name} trấn an linh hồn bằng những lời nói chân thành và năng lượng chữa lành. Linh hồn dần dần bình tĩnh lại, ánh sáng của nó trở nên dịu nhẹ hơn, rồi từ từ tan biến, mang theo sự bình yên trở lại khu rừng.",
        choice_a="Nhiệm vụ hoàn thành! Khu rừng trở nên yên bình.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_success_end_3", "quest_success_end_3", "quest_success_end_3", "quest_success_end_3")
    ),

    GuardianQuestLines(
        id="purify_spirit_attempt",
        title="Thanh Tẩy Không Thành Công",
        description="Bạn cố gắng thanh tẩy linh hồn bằng phép thuật, nhưng nó quá mạnh và kháng cự. Linh hồn gầm lên giận dữ, đẩy bạn và {guardian.ga_name} lùi lại. 'Nó không thể bị thanh tẩy dễ dàng!' {guardian.ga_name} nói.",
        choice_a="Bạn bị thương nhẹ. Nhiệm vụ thất bại.",
        ga_exp= 50, silver = -50, gold=-50, ga_health=-50, ga_mana=-50, ga_stamina=-50,
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3")
    ),

    GuardianQuestLines(
        id="ask_spirit_cause",
        title="Nguyên Nhân Mắc Kẹt",
        description="Bạn hỏi linh hồn về nguyên nhân bị mắc kẹt. Linh hồn truyền đạt một hình ảnh: một phù thủy độc ác đã tạo ra lời nguyền. 'Chúng ta cần tìm cách hóa giải lời nguyền!' {guardian.ga_name} nói.",
        choice_a="Tìm kiếm cách hóa giải lời nguyền.",
        choice_b="Vẫn cố gắng thanh tẩy linh hồn.",
        choice_c="",
        choice_timeout="{guardian.ga_name} thúc giục. 'Thời gian không cho phép chúng ta chần chừ!'",
        next_steps=NextSteps(
            choice_a="seek_purifying_artifact", # Dẫn đến tìm cổ vật
            choice_b="purify_spirit_attempt",
            choice_c="",
            timeout="spirit_anger_outcome"
        )
    ),

    GuardianQuestLines(
        id="take_artifact",
        title="Lấy Cổ Vật Thành Công",
        description="Bạn chạm vào Cổ Vật Thanh Tẩy. Một luồng ánh sáng ấm áp tỏa ra, xua tan những tàn dư của lời nguyền. {guardian.ga_name} reo lên: 'Chúng ta đã có nó! Giờ hãy mang nó về khu rừng!'",
        choice_a="Mang cổ vật trở lại khu rừng.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("return_to_forest_with_artifact", "", "", "")
    ),

    GuardianQuestLines(
        id="deactivate_curse_first",
        title="Vô Hiệu Hóa Lời Nguyền",
        description="Bạn và {guardian.ga_name} tìm cách vô hiệu hóa lời nguyền bao quanh cổ vật. Sau một hồi nỗ lực, luồng năng lượng đen tối bao quanh cổ vật yếu đi đáng kể. 'Giờ thì an toàn hơn rồi,' {guardian.ga_name} nói.",
        choice_a="Lấy cổ vật.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("take_artifact", "", "", "")
    ),

    GuardianQuestLines(
        id="check_for_traps",
        title="Kiểm Tra Cạm Bẫy",
        description="Bạn cẩn thận kiểm tra xung quanh bệ đá. Bạn phát hiện một sợi dây bẫy ẩn giấu. {guardian.ga_name} giúp bạn vô hiệu hóa nó. 'May mà chúng ta cẩn thận,' {guardian.ga_name} thở phào.",
        choice_a="Lấy cổ vật.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("take_artifact", "", "", "")
    ),

    GuardianQuestLines(
        id="return_to_forest_with_artifact",
        title="Sức Mạnh Thanh Tẩy",
        description="Bạn và {guardian.ga_name} mang Cổ Vật Thanh Tẩy trở lại khu rừng. Khi bạn đặt cổ vật lên bệ đá gần linh hồn, một luồng sáng mạnh mẽ bùng lên, thanh tẩy linh hồn và hóa giải lời nguyền khỏi khu rừng.",
        choice_a="Nhiệm vụ hoàn thành! Khu rừng được giải thoát.",
        choice_b="", choice_c="", choice_timeout="",
        ga_exp= 300, silver = 1000, gold=500, ga_health=50, ga_mana=50, ga_stamina=50, dignity_point=10,
        next_steps=NextSteps("quest_success_end_3", "quest_success_end_3", "quest_success_end_3", "quest_success_end_3")
    ),

    # Failures
    GuardianQuestLines(
        id="ignore_spirits_outcome",
        title="Phớt Lờ Tiếng Kêu Cứu",
        description="Bạn quyết định bỏ qua. Vài ngày sau, khu rừng trở nên u ám hơn, và những câu chuyện về linh hồn quấy phá lan rộng. {guardian.ga_name} nhìn bạn với vẻ thất vọng.",
        choice_a="Cảm thấy hối tiếc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point= -5, ga_exp= -50, silver = -50, gold=-50,
        next_steps=NextSteps("quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3")
    ),

    GuardianQuestLines(
        id="ga_worried_timeout_3",
        title="Ánh Mắt Lo Lắng",
        description="Bạn chần chừ quá lâu. {guardian.ga_name} lắc đầu thất vọng. 'Chúng ta không thể cứu họ nếu cứ đứng đây!' Nhiệm vụ kết thúc vì sự thiếu quyết đoán.",
        choice_a="Cảm thấy bất lực. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3"),
        dignity_point= -10, ga_exp= -50, silver = -100, gold=-50,
    ),

    GuardianQuestLines(
        id="spirit_fades_timeout",
        title="Linh Hồn Tan Biến",
        description="Bạn và {guardian.ga_name} chần chừ. Linh hồn yếu ớt dần dần tan biến vào hư vô, không thể được cứu vớt. {guardian.ga_name} thở dài buồn bã. 'Đã quá muộn rồi.'",
        choice_a="Cảm thấy nuối tiếc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point= -5, ga_exp= -50, silver = -100, gold=-50,
        next_steps=NextSteps("quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3")
    ),

    GuardianQuestLines(
        id="avoid_spirit_outcome",
        title="Tránh Xa Linh Hồn",
        description="Bạn và {guardian.ga_name} cố gắng tìm đường vòng, nhưng khu rừng dường như không cho phép. Bạn lạc lối và không thể tìm thấy lối thoát. 'Chúng ta đã đi sai đường rồi, chủ nhân,' {guardian.ga_name} nói.",
        choice_a="Bạn bị lạc và nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point= -5, ga_exp= -50, silver = -100, gold=-50,
        next_steps=NextSteps("quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3")
    ),

    GuardianQuestLines(
        id="abandon_quest_ancient_forest",
        title="Từ Bỏ Nhiệm Vụ",
        description="Bạn quyết định rằng nhiệm vụ này quá phức tạp và nguy hiểm. Bạn và {guardian.ga_name} quay lưng lại với số phận của khu rừng. 'Tôi hy vọng có ai đó khác có thể giúp đỡ,' {guardian.ga_name} nói với giọng buồn bã.",
        choice_a="Cảm thấy nhẹ nhõm, nhưng cũng có chút hối tiếc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point= -10, ga_exp= -150, silver = -500, gold=-50,
        next_steps=NextSteps("quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3")
    ),

    GuardianQuestLines(
        id="spirit_anger_outcome",
        title="Linh Hồn Nổi Giận",
        description="Bạn chần chừ trong việc quyết định cách tiếp cận. Linh hồn gầm lên giận dữ, nó trở nên mạnh hơn và tấn công bạn. {guardian.ga_name} phải tạo lá chắn để bảo vệ bạn.",
        choice_a="Bạn bị tấn công và phải rút lui. Nhiệm vụ thất bại.",
        dignity_point= -5, ga_exp= -50, silver = -50, gold=-50,
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3")
    ),

    GuardianQuestLines(
        id="let_spirit_be_outcome",
        title="Mặc Kệ Linh Hồn",
        description="Bạn quyết định để linh hồn tự giải thoát. Tuy nhiên, linh hồn không thể tự mình vượt qua lời nguyền và cuối cùng tan biến hoàn toàn. 'Chúng ta đã không thể giúp nó,' {guardian.ga_name} nói buồn bã.",
        choice_a="Bạn cảm thấy bất lực. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point= -5, ga_exp= -50, silver = -50, gold=-50,
        next_steps=NextSteps("quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3")
    ),

    GuardianQuestLines(
        id="retreat_from_forest",
        title="Rút Lui Khỏi Rừng",
        description="Bạn và {guardian.ga_name} quyết định rút lui khỏi khu rừng cổ. Bạn cảm thấy một nỗi buồn man mác khi rời đi, biết rằng linh hồn vẫn đang mắc kẹt ở đó. 'Chúng ta không thể làm gì lúc này,' {guardian.ga_name} thở dài.",
        choice_a="Rút lui và nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point= -10, ga_exp= -50, silver = -50, gold=-50,
        next_steps=NextSteps("quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3")
    ),

    GuardianQuestLines(
        id="artifact_disappears_timeout",
        title="Cổ Vật Biến Mất",
        description="Bạn chần chừ quá lâu trước cổ vật. Năng lượng của lời nguyền bùng phát mạnh mẽ, khiến cổ vật biến mất vào hư vô. 'Không! Đã quá muộn rồi!' {guardian.ga_name} thốt lên.",
        choice_a="Cổ vật biến mất, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point= -10, ga_exp= -50, silver = -50, gold=-50,
        next_steps=NextSteps("quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3")
    ),

    # Generic Endings
    GuardianQuestLines(
        id="quest_success_end_3",
        title="Hòa Bình Cho Khu Rừng",
        description="Khu rừng cổ đã tìm thấy sự bình yên. Những linh hồn được giải thoát, và không khí trở nên trong lành. {guardian.ga_name} mỉm cười. 'Chúng ta đã mang lại sự bình yên cho nơi đây, chủ nhân.'",
        ga_exp= 200, silver = 1000, gold=500, ga_health=50, ga_mana=50, ga_stamina=50, dignity_point=10,
        choice_a="Bạn cảm thấy tự hào về bản thân và {guardian.ga_name}.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("continue_adventure_3", "continue_adventure_3", "continue_adventure_3", "continue_adventure_3")
    ),

    GuardianQuestLines(
        id="quest_failed_end_3",
        title="Bóng Tối Tiếp Diễn",
        description="Khu rừng cổ vẫn chìm trong sự đau khổ của những linh hồn mắc kẹt. {guardian.ga_name} cúi đầu, vẻ mặt buồn bã. 'Chúng ta... đã không thể thay đổi số phận của họ.'",
        choice_a="Rút ra bài học đau đớn.",
        dignity_point= -10, ga_exp= -50, silver = -50, gold=-50,
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("continue_adventure_3", "continue_adventure_3", "continue_adventure_3", "continue_adventure_3")
    ),

    GuardianQuestLines(
        id="continue_adventure_3",
        title="Hành Trình Tiếp Nối",
        description="Bạn và {guardian.ga_name} rời khỏi khu rừng cổ, mang theo những ký ức về hành trình vừa qua. Những cuộc phiêu lưu mới đang chờ đợi...",
        choice_a="",
        choice_b="", choice_c="", choice_timeout="",
        ga_exp= 50, silver = 1000, gold=10,
        next_steps=NextSteps("", "", "", "")
    )
]

#region quest_night_market 
quest_night_market = [
    GuardianQuestLines(
        id="start",
        title="Lễ Hội Vĩnh Hằng Của Thung Lũng Ảo Ảnh",
        description="Một tấm thiệp mời bí ẩn dẫn bạn và {guardian.ga_name} đến một thung lũng hẻo lánh, nơi một lễ hội lộng lẫy đang diễn ra. Âm nhạc vang vọng, người dân tươi cười, nhưng {guardian.ga_name} khẽ cau mày. 'Ta cảm thấy một sự giả dối ẩn sâu dưới vẻ rạng rỡ này, Ngài.'",
        choice_a="Hòa mình vào lễ hội, tìm hiểu dân làng.",
        choice_b="Tìm kiếm những điều bất thường trong lễ hội.",
        choice_c="Rời đi ngay lập tức, cảm giác không lành.",
        choice_timeout="{guardian.ga_name} thúc giục. 'Nếu ta bỏ qua, liệu có điều gì tồi tệ hơn sẽ xảy ra không, Ngài?'",
        next_steps=NextSteps(
            choice_a="join_festival",
            choice_b="investigate_oddities",
            choice_c="leave_festival_early",
            timeout="ga_uneasy_timeout"
        ),
        gold=20, silver=100, ga_exp=15, dignity_point=5
    ),

    GuardianQuestLines(
        id="join_festival",
        title="Bữa Tiệc Bất Tận",
        description="Bạn và {guardian.ga_name} tham gia vào lễ hội. Mọi người mời bạn nhảy múa, ca hát và ăn uống. Thức ăn ngọt ngào, âm nhạc mê hoặc. {guardian.ga_name} thì thầm: 'Thật kỳ lạ, không ai dường như mệt mỏi cả.'",
        choice_a="Tham gia một điệu nhảy truyền thống.",
        choice_b="Cố gắng nói chuyện riêng với một người dân.",
        choice_c="Tìm một nơi yên tĩnh để quan sát.",
        choice_timeout="{guardian.ga_name} nói khẽ. 'Chúng ta không thể mãi bị cuốn theo điệu nhạc này, Ngài.'",
        next_steps=NextSteps(
            choice_a="participate_dance",
            choice_b="talk_to_villager",
            choice_c="observe_quietly",
            timeout="dance_hypnosis_timeout"
        )
    ),

    GuardianQuestLines(
        id="investigate_oddities",
        title="Dấu Vết Kỳ Lạ",
        description="Bạn và {guardian.ga_name} bắt đầu điều tra. Bạn nhận thấy rằng tất cả các cánh cửa nhà đều bị khóa từ bên ngoài, và có những ký hiệu lạ được khắc trên các cây cổ thụ xung quanh thung lũng. {guardian.ga_name} chạm vào một ký hiệu. 'Đây là ma thuật cầm tù, Ngài.'",
        choice_a="Thử giải mã các ký hiệu.",
        choice_b="Tìm một con đường bí mật ra khỏi thung lũng.",
        choice_c="Đối mặt với trưởng làng để hỏi rõ.",
        choice_timeout="{guardian.ga_name} thúc giục. 'Chúng ta phải tìm ra ý nghĩa của chúng trước khi quá muộn!'",
        next_steps=NextSteps(
            choice_a="decipher_symbols",
            choice_b="seek_secret_path",
            choice_c="confront_elder_early",
            timeout="symbols_activate_timeout"
        )
    ),

    GuardianQuestLines(
        id="participate_dance",
        title="Điệu Nhảy Không Ngừng",
        description="Bạn tham gia điệu nhảy. Nhạc ngày càng nhanh, ánh sáng càng rực rỡ. {guardian.ga_name} cố gắng kéo bạn lại. 'Chủ nhân, dừng lại! Ngài đang mất kiểm soát!' Nhưng cơ thể bạn không tuân lệnh. Một nụ cười vô hồn nở trên môi dân làng.",
        choice_a="Cố gắng kháng cự lại sự thôi miên của điệu nhạc.",
        choice_b="Để cơ thể cuốn theo điệu nhảy, xem điều gì sẽ xảy ra.",
        choice_c="",
        choice_timeout="Điệu nhảy trở nên cuồng loạn. 'Ngài đang bị hấp dẫn!' {guardian.ga_name} gầm lên.",
        next_steps=NextSteps(
            choice_a="resist_hypnosis",
            choice_b="yield_to_dance",
            choice_c="",
            timeout="yield_to_dance" # Force this outcome if timeout
        )
    ),

    GuardianQuestLines(
        id="talk_to_villager",
        title="Lời Thì Thầm Trong Bóng Tối",
        description="Bạn kéo một người dân làng ra khỏi đám đông. Anh ta nhìn bạn với đôi mắt trống rỗng. 'Lễ hội... không bao giờ kết thúc... đó là... lời nguyền.' Anh ta thì thầm trước khi bị một lực vô hình kéo trở lại. {guardian.ga_name} nắm chặt tay. 'Ta biết mà! Có điều gì đó đang điều khiển họ!'",
        choice_a="Tìm kiếm nguồn gốc của lời nguyền.",
        choice_b="Cố gắng cảnh báo những người khác.",
        choice_c="",
        choice_timeout="{guardian.ga_name} nói khẽ. 'Chúng ta không còn nhiều thời gian để lãng phí nữa, Ngài.'",
        next_steps=NextSteps(
            choice_a="seek_curse_source",
            choice_b="warn_others_outcome",
            choice_c="",
            timeout="curse_absorbs_timeout"
        )
    ),

    GuardianQuestLines(
        id="seek_curse_source",
        title="Bệ Thờ Cổ",
        description="Bạn và {guardian.ga_name} tìm đến một bệ thờ cổ nằm sâu trong rừng, nơi những linh hồn bị mắc kẹt dường như đang cung cấp năng lượng cho lễ hội. Một thực thể vô hình, với hàng trăm con mắt, lơ lửng phía trên bệ thờ. {guardian.ga_name} chuẩn bị chiến đấu. 'Đây là thứ đang giam cầm họ, Ngài!'",
        choice_a="Cố gắng phá hủy bệ thờ.",
        choice_b="Tìm cách nói chuyện với thực thể.",
        choice_c="Rút lui và tìm kế hoạch khác.",
        choice_timeout="Thực thể bắt đầu tập trung năng lượng. 'Nó đang tấn công!' {guardian.ga_name} hét lên.",
        next_steps=NextSteps(
            choice_a="destroy_altar_attempt",
            choice_b="commune_with_entity",
            choice_c="retreat_from_altar",
            timeout="entity_attacks_outcome"
        )
    ),

    GuardianQuestLines(
        id="yield_to_dance",
        title="Hòa Mình Vào Hư Vô",
        description="Bạn buông bỏ mọi kháng cự, để cơ thể mình cuốn theo điệu nhảy cuồng loạn. Mọi ký ức, mọi suy nghĩ dần tan biến. {guardian.ga_name} gọi tên bạn trong vô vọng, nhưng bạn chỉ thấy một nụ cười vô hồn nở trên môi mình. Bạn trở thành một phần của lễ hội, mãi mãi nhảy múa, mãi mãi mỉm cười trong sự trống rỗng. {guardian.ga_name} lao vào đám đông, cố gắng kéo bạn ra, nhưng bị những bàn tay vô hình đẩy lùi. Hắn nhìn bạn, nước mắt tuôn rơi khi bạn biến thành một bức tượng sống, mãi mãi là một hình ảnh rạng rỡ của sự hủy diệt, còn hắn thì phải mang theo nỗi đau mất mát không thể chịu đựng.",
        choice_a="Bạn trở thành một phần vĩnh cửu của lễ hội.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_festival_trap", "quest_failed_end_festival_trap", "quest_failed_end_festival_trap", "quest_failed_end_festival_trap"),
        gold=-500, silver=-500, ga_exp=-200, dignity_point=-50, ga_health=-999, ga_mana=-999, ga_stamina=-999, force_dead=True,
    ),

    GuardianQuestLines(
        id="commune_with_entity",
        title="Thỏa Thuận Với Thực Thể",
        description="Bạn cố gắng giao tiếp với thực thể. Nó mở ra hàng trăm con mắt, hiển thị những hình ảnh về nỗi sợ hãi và khao khát sâu thẳm nhất của bạn. 'Ngươi muốn gì?' một giọng nói đồng loạt vang lên. {guardian.ga_name} cảnh báo. 'Cẩn thận, Ngài! Nó đang cố gắng thao túng Ngài!'",
        choice_a="Cố gắng thương lượng để giải thoát dân làng.",
        choice_b="Cầu xin nó dừng lại.",
        choice_c="Chấp nhận sức mạnh mà nó có thể ban tặng.",
        choice_timeout="Thực thể cười khúc khích. 'Ngươi đã chọn.'",
        next_steps=NextSteps(
            choice_a="negotiate_entity",
            choice_b="beg_entity_outcome",
            choice_c="accept_entity_power_outcome",
            timeout="accept_entity_power_outcome" # Force this outcome if timeout
        )
    ),

    GuardianQuestLines(
        id="accept_entity_power_outcome",
        title="Sức Mạnh Đổi Lấy Linh Hồn",
        description="Bạn đồng ý nhận sức mạnh từ thực thể. Một luồng năng lượng đen tối bao trùm lấy bạn, đốt cháy linh hồn. Bạn cảm thấy sức mạnh dâng trào, nhưng cùng lúc đó, ý chí của bạn bị tước đoạt. Bạn trở thành một người hầu vô tri của thực thể, một phần của lễ hội vĩnh hằng. {guardian.ga_name} gầm lên, lao vào tấn công thực thể, nhưng vô ích. Hắn bị hất văng, nhìn bạn biến thành một con rối không hồn. Từ đó, {guardian.ga_name} lang thang, mang theo sự ám ảnh về đôi mắt trống rỗng của bạn, và hắn biết, bạn đã hoàn toàn mất đi.",
        choice_a="Bạn trở thành con rối của thực thể, {guardian.ga_name} bị tổn thương sâu sắc.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_enslaved", "quest_failed_end_enslaved", "quest_failed_end_enslaved", "quest_failed_end_enslaved"),
        gold=-700, silver=-700, ga_exp=-300, dignity_point=-70, ga_health=-999, ga_mana=-999, ga_stamina=-999, force_dead=True
    ),

    # Failures and generic endings
    GuardianQuestLines(
        id="leave_festival_early",
        title="Rời Bỏ Bóng Tối",
        description="Bạn và {guardian.ga_name} quyết định rời khỏi thung lũng. Cảm giác nhẹ nhõm xen lẫn một nỗi lo lắng không tên. Vài ngày sau, tin đồn về thung lũng biến mất khỏi bản đồ lan truyền. 'Có lẽ đó là một quyết định đúng đắn, Ngài,' {guardian.ga_name} thở phào.",
        choice_a="Rời khỏi và nhiệm vụ kết thúc.",
        choice_b="", choice_c="", choice_timeout="",
        gold=50, silver=100, ga_exp=20, dignity_point=0,
        next_steps=NextSteps("quest_failed_end_4", "quest_failed_end_4", "quest_failed_end_4", "quest_failed_end_4")
    ),

    GuardianQuestLines(
        id="ga_uneasy_timeout",
        title="Cảm Giác Bất An",
        description="Bạn chần chừ quá lâu. {guardian.ga_name} thở dài. 'Có vẻ như sự chần chừ của Ngài đã tước đi cơ hội can thiệp. Ta cảm thấy một sự sợ hãi đang bao trùm thung lũng.' Nhiệm vụ kết thúc trong sự không chắc chắn.",
        choice_a="Bạn cảm thấy bất lực. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        gold=-20, silver=-50, ga_exp=-20, dignity_point=-5,
        next_steps=NextSteps("quest_failed_end_4", "quest_failed_end_4", "quest_failed_end_4", "quest_failed_end_4")
    ),

    GuardianQuestLines(
        id="dance_hypnosis_timeout",
        title="Điệu Nhảy Chiếm Hữu",
        description="Bạn chần chừ trong điệu nhảy. Âm nhạc và chuyển động ngày càng mạnh mẽ, áp đảo ý chí của bạn. {guardian.ga_name} cố gắng kéo bạn ra, nhưng vô ích. Bạn bị cuốn vào điệu nhảy, ý thức dần mờ đi. 'Ngài đang mất chính mình!' {guardian.ga_name} gào lên.",
        choice_a="Bạn bị cuốn vào điệu nhảy vĩnh cửu.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-50, silver=-100, ga_exp=-50, dignity_point=-10, ga_health=-25, ga_mana=-25, ga_stamina=-25,
        next_steps=NextSteps("quest_failed_end_festival_trap", "quest_failed_end_festival_trap", "quest_failed_end_festival_trap", "quest_failed_end_festival_trap")
    ),

    GuardianQuestLines(
        id="symbols_activate_timeout",
        title="Ký Hiệu Tức Giận",
        description="Bạn chần chừ quá lâu trước các ký hiệu. Chúng bắt đầu phát sáng rực rỡ, một làn sóng năng lượng giam cầm bao trùm thung lũng, khiến không khí trở nên nặng nề hơn. 'Chúng ta đã lãng phí thời gian, Ngài!' {guardian.ga_name} nói, vẻ mặt nghiêm trọng.",
        choice_a="Bạn cảm thấy bị mắc kẹt. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        gold=-30, silver=-80, ga_exp=-30, dignity_point=-5,
        next_steps=NextSteps("quest_failed_end_4", "quest_failed_end_4", "quest_failed_end_4", "quest_failed_end_4")
    ),

    GuardianQuestLines(
        id="observe_quietly",
        title="Quan Sát Đáng Sợ",
        description="Bạn và {guardian.ga_name} quan sát từ xa. Bạn thấy những người dân làng, khi ở một mình, lại có ánh mắt vô hồn và thốt ra những lời thì thầm vô nghĩa. {guardian.ga_name} nói. 'Họ đã không còn là chính mình nữa, Ngài.'",
        choice_a="Tìm kiếm nguồn gốc của sự biến đổi này.",
        choice_b="Cố gắng tìm lối thoát bí mật.",
        choice_c="",
        choice_timeout="{guardian.ga_name} thúc giục. 'Nguy hiểm đang đến gần!'",
        next_steps=NextSteps(
            choice_a="seek_curse_source",
            choice_b="seek_secret_path",
            choice_c="",
            timeout="curse_absorbs_timeout"
        )
    ),

    GuardianQuestLines(
        id="decipher_symbols",
        title="Lời Nguyền Cổ Xưa",
        description="Bạn và {guardian.ga_name} giải mã các ký hiệu. Chúng là một lời nguyền cổ xưa, trói buộc linh hồn dân làng vào một vòng lặp vĩnh cửu để cung cấp năng lượng cho một thực thể bị giam cầm. {guardian.ga_name} nắm chặt tay. 'Chúng ta phải giải phóng họ!'",
        choice_a="Tìm kiếm nơi thực thể bị giam cầm.",
        choice_b="Cố gắng phá hủy các ký hiệu.",
        choice_c="",
        choice_timeout="{guardian.ga_name} nghiêm nghị. 'Chúng ta không có nhiều thời gian, Ngài!'",
        next_steps=NextSteps(
            choice_a="seek_curse_source",
            choice_b="destroy_symbols_attempt",
            choice_c="",
            timeout="symbols_activate_timeout"
        )
    ),

    GuardianQuestLines(
        id="destroy_symbols_attempt",
        title="Phá Hủy Bất Thành",
        description="Bạn cố gắng phá hủy các ký hiệu, nhưng chúng quá mạnh. Một luồng năng lượng phản kháng bắn ngược lại, khiến bạn choáng váng. {guardian.ga_name} đỡ bạn. 'Chúng ta cần một cách khác, Ngài. Chúng được bảo vệ bởi một thứ gì đó rất mạnh.'",
        choice_a="Bạn bị choáng váng, nhiệm vụ gặp trở ngại.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-30, silver=-50, ga_exp=-30, ga_health=-10, ga_mana=-10, ga_stamina=-10,
        next_steps=NextSteps("investigate_oddities", "investigate_oddities", "investigate_oddities", "investigate_oddities")
    ),

    GuardianQuestLines(
        id="seek_secret_path",
        title="Con Đường Cụt",
        description="Bạn và {guardian.ga_name} tìm kiếm một con đường bí mật. Bạn tìm thấy một hang động ẩn giấu, nhưng nó dẫn đến một vách đá thẳng đứng. Không có lối thoát. 'Có vẻ như chúng ta đã bị mắc kẹt, Ngài,' {guardian.ga_name} nói với vẻ thất vọng.",
        choice_a="Bạn bị mắc kẹt, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-40, silver=-100, ga_exp=-40, dignity_point=-10,
        next_steps=NextSteps("quest_failed_end_4", "quest_failed_end_4", "quest_failed_end_4", "quest_failed_end_4")
    ),

    GuardianQuestLines(
        id="confront_elder_early",
        title="Trưởng Làng Lạnh Lùng",
        description="Bạn và {guardian.ga_name} đối mặt với trưởng làng. Ông ta mỉm cười lạnh lẽo. 'Ngài không thể thay đổi những gì đã định sẵn.' Một lớp sương mù dày đặc bao trùm lấy bạn và {guardian.ga_name}, mọi thứ mờ dần. 'Chúng ta đã mắc bẫy!' {guardian.ga_name} gầm lên.",
        choice_a="Bạn bị mắc kẹt trong sương mù. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-50, silver=-150, ga_exp=-50, dignity_point=-15, ga_health=-25, ga_mana=-25, ga_stamina=-25,
        next_steps=NextSteps("quest_failed_end_fog_trap", "quest_failed_end_fog_trap", "quest_failed_end_fog_trap", "quest_failed_end_fog_trap")
    ),

    GuardianQuestLines(
        id="resist_hypnosis",
        title="Ý Chí Kiên Cường",
        description="Bạn tập trung ý chí, chống lại sự thôi miên của điệu nhạc. {guardian.ga_name} hỗ trợ bạn bằng năng lượng của hắn. Dần dần, bạn cảm thấy mình thoát khỏi ảnh hưởng, nhưng dân làng nhìn bạn với đôi mắt trống rỗng và thù địch. 'Họ đã nhận ra chúng ta là kẻ ngoại lai,' {guardian.ga_name} nói. 'Chúng ta phải tìm ra cách giải thoát họ.'",
        choice_a="Tìm kiếm nguồn gốc của sự mê hoặc.",
        choice_b="Cố gắng thoát khỏi vòng vây của dân làng.",
        choice_c="",
        choice_timeout="{guardian.ga_name} thúc giục. 'Họ đang tiến đến gần!'",
        next_steps=NextSteps(
            choice_a="seek_curse_source",
            choice_b="escape_villagers_attempt",
            choice_c="",
            timeout="yield_to_dance"
        )
    ),

    GuardianQuestLines(
        id="warn_others_outcome",
        title="Cảnh Báo Vô Vọng",
        description="Bạn cố gắng cảnh báo những người dân làng khác, nhưng họ chỉ mỉm cười trống rỗng và quay lưng đi, tiếp tục nhảy múa. 'Họ không thể nghe thấy chúng ta, Ngài,' {guardian.ga_name} nói với giọng buồn bã. 'Họ đã bị trói buộc quá chặt rồi.'",
        choice_a="Cảnh báo không thành, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-20, silver=-40, ga_exp=-20, dignity_point=-5,
        next_steps=NextSteps("quest_failed_end_4", "quest_failed_end_4", "quest_failed_end_4", "quest_failed_end_4")
    ),

    GuardianQuestLines(
        id="curse_absorbs_timeout",
        title="Lời Nguyền Cạn Kiệt",
        description="Bạn chần chừ quá lâu. Năng lượng của lời nguyền bao trùm thung lũng trở nên mạnh mẽ hơn. Bạn cảm thấy mình bị hút cạn sức lực, và ý thức dần mờ đi. 'Ngài đang bị hấp thụ!' {guardian.ga_name} thét lên, nhưng đã quá muộn.",
        choice_a="Bạn bị hấp thụ vào lời nguyền.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-70, silver=-150, ga_exp=-70, dignity_point=-15, ga_health=-50, ga_mana=-50, ga_stamina=-50,
        next_steps=NextSteps("quest_failed_end_festival_trap", "quest_failed_end_festival_trap", "quest_failed_end_festival_trap", "quest_failed_end_festival_trap")
    ),

    GuardianQuestLines(
        id="entity_attacks_outcome",
        title="Cuộc Tấn Công Hủy Diệt",
        description="Bạn chần chừ. Thực thể bị giam cầm bùng nổ trong cơn thịnh nộ, bắn ra hàng ngàn xúc tu vô hình. Bạn và {guardian.ga_name} bị đâm xuyên, cơ thể tan rã trong ánh sáng xanh quỷ dị. Linh hồn của cả hai bị thực thể hấp thụ hoàn toàn, trở thành một phần vĩnh viễn của sự giam cầm. {guardian.ga_name} cố gắng chiến đấu đến hơi thở cuối cùng, nhưng không thể cứu vãn được số phận của cả hai.",
        choice_a="Bạn và {guardian.ga_name} bị hủy diệt hoàn toàn.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-900, silver=-900, ga_exp=-400, dignity_point=-90, ga_health=-999, ga_mana=-999, ga_stamina=-999, force_dead=True,
        next_steps=NextSteps("quest_failed_end_total_annihilation_2", "quest_failed_end_total_annihilation_2", "quest_failed_end_total_annihilation_2", "quest_failed_end_total_annihilation_2")
    ),

    GuardianQuestLines(
        id="destroy_altar_attempt",
        title="Sức Mạnh Áp Đảo",
        description="Bạn và {guardian.ga_name} tấn công bệ thờ. Thực thể gầm lên, phản công dữ dội. Mặc dù bạn và {guardian.ga_name} chiến đấu dũng cảm, năng lượng của thực thể quá lớn. Bạn bị đẩy lùi, cảm thấy sức mạnh kiệt quệ, và bệ thờ vẫn đứng vững. {guardian.ga_name} thở hổn hển. 'Nó quá mạnh, Ngài!'",
        choice_a="Bạn và {guardian.ga_name} bị kiệt sức. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-50, silver=-100, ga_exp=-50, dignity_point=-10, ga_health=-30, ga_mana=-30, ga_stamina=-30,
        next_steps=NextSteps("quest_failed_end_4", "quest_failed_end_4", "quest_failed_end_4", "quest_failed_end_4")
    ),

    GuardianQuestLines(
        id="retreat_from_altar",
        title="Rút Lui Khỏi Nguy Hiểm",
        description="Bạn và {guardian.ga_name} quyết định rút lui khỏi bệ thờ. Cảm giác bất lực bao trùm khi bạn quay lưng lại với những linh hồn đang bị giam cầm. 'Chúng ta không thể đối phó với thứ đó ngay bây giờ,' {guardian.ga_name} nói với giọng buồn bã.",
        choice_a="Rút lui và nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-30, silver=-70, ga_exp=-30, dignity_point=-5,
        next_steps=NextSteps("quest_failed_end_4", "quest_failed_end_4", "quest_failed_end_4", "quest_failed_end_4")
    ),

    GuardianQuestLines(
        id="negotiate_entity",
        title="Lời Hứa Phản Bội",
        description="Bạn cố gắng thương lượng để giải thoát dân làng. Thực thể im lặng một lúc, rồi giọng nói của nó vang lên: 'Ta sẽ giải thoát chúng... nếu ngươi thay thế.' {guardian.ga_name} hét lên. 'Đừng tin nó, Ngài!'",
        choice_a="Chấp nhận trở thành vật hiến tế.",
        choice_b="Từ chối lời đề nghị.",
        choice_c="",
        choice_timeout="Thực thể cười khúc khích. 'Ngươi không có lựa chọn nào khác.'",
        next_steps=NextSteps(
            choice_a="become_sacrifice",
            choice_b="entity_attacks_outcome", # Re-direct to attack if refused after negotiation
            choice_c="",
            timeout="become_sacrifice"
        )
    ),

    GuardianQuestLines(
        id="become_sacrifice",
        title="Hy Sinh Vô Nghĩa",
        description="Bạn chấp nhận trở thành vật hiến tế. Thực thể lao vào bạn, hấp thụ linh hồn bạn một cách tàn bạo. Trong giây phút cuối cùng, bạn nhìn thấy dân làng vẫn tiếp tục nhảy múa, mắt họ trống rỗng, không hề được giải thoát. Thực thể đã lừa dối bạn. {guardian.ga_name} gào thét tên bạn, nhưng bạn đã biến mất, chỉ còn lại một tiếng vang đau đớn trong không gian. {guardian.ga_name} đứng đó, nhìn những người dân làng không hồn, hiểu rằng sự hy sinh của bạn là vô ích, và bạn đã vĩnh viễn là một phần của lễ hội mục nát này.",
        choice_a="Bạn bị hy sinh, linh hồn bạn bị hấp thụ, dân làng không được giải thoát.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_enslaved", "quest_failed_end_enslaved", "quest_failed_end_enslaved", "quest_failed_end_enslaved"),
        gold=-800, silver=-800, ga_exp=-350, dignity_point=-80, ga_health=-999, ga_mana=-999, ga_stamina=-999, force_dead=True,
    ),

    GuardianQuestLines(
        id="beg_entity_outcome",
        title="Lời Cầu Xin Vô Vọng",
        description="Bạn cầu xin thực thể dừng lại. Nó chỉ cười khẩy, giọng nói vang vọng khắp căn phòng. 'Sự yếu đuối của ngươi không có giá trị ở đây.' Thực thể trừng phạt bạn bằng một luồng năng lượng. {guardian.ga_name} nhanh chóng tạo lá chắn để bảo vệ bạn, nhưng cả hai đều bị đẩy lùi và bị thương. 'Nó không thể được thuyết phục, Ngài!' {guardian.ga_name} nói, vẻ mặt đau đớn.",
        choice_a="Bạn và {guardian.ga_name} bị thương. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-50, silver=-100, ga_exp=-50, dignity_point=-10, ga_health=-20, ga_mana=-20, ga_stamina=-20,
        next_steps=NextSteps("quest_failed_end_4", "quest_failed_end_4", "quest_failed_end_4", "quest_failed_end_4")
    ),

    GuardianQuestLines(
        id="escape_villagers_attempt",
        title="Không Lối Thoát",
        description="Bạn và {guardian.ga_name} cố gắng thoát khỏi vòng vây của dân làng, nhưng họ đông hơn và di chuyển với một tốc độ kỳ lạ. Họ không ngừng mỉm cười khi họ đẩy bạn sâu hơn vào trung tâm lễ hội. 'Chúng ta bị mắc kẹt rồi, Ngài!' {guardian.ga_name} hét lên.",
        choice_a="Bạn bị dồn vào đường cùng. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-60, silver=-120, ga_exp=-60, dignity_point=-15, ga_health=-30, ga_mana=-30, ga_stamina=-30,
        next_steps=NextSteps("quest_failed_end_festival_trap", "quest_failed_end_festival_trap", "quest_failed_end_festival_trap", "quest_failed_end_festival_trap")
    ),

    # Final Bad Endings
    GuardianQuestLines(
        id="quest_failed_end_festival_trap",
        title="Cái Bẫy Vĩnh Cửu",
        description="Bạn trở thành một phần của lễ hội vĩnh hằng, linh hồn bị mắc kẹt trong điệu nhảy không ngừng. Bạn mỉm cười mãi mãi, nhưng bên trong là sự trống rỗng và nỗi kinh hoàng. {guardian.ga_name} bị ám ảnh bởi hình ảnh bạn, không thể quên được đôi mắt vô hồn đó. Hắn lang thang khắp thế giới, là một cái bóng của chính mình, mang theo nỗi đau và sự bất lực, biết rằng bạn đã mãi mãi mất đi dưới ánh sáng lộng lẫy nhưng tàn độc của lễ hội. Sự sống của hắn trở thành một sự trừng phạt cho sự thất bại của hắn khi không thể cứu lấy bạn, người bạn đồng hành thân thiết nhất.",
        choice_a="Bạn bị giam cầm, {guardian.ga_name} đau khổ.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-500, silver=-500, ga_exp=-200, dignity_point=-50, ga_health=-999, ga_mana=-999, ga_stamina=-999, force_dead=True,
        next_steps=NextSteps("continue_adventure_4", "continue_adventure_4", "continue_adventure_4", "continue_adventure_4")
    ),

    GuardianQuestLines(
        id="quest_failed_end_enslaved",
        title="Linh Hồn Nô Lệ",
        description="Bạn bị thực thể chiếm hữu hoàn toàn, trở thành một con rối vô tri, phục vụ cho những mục đích hắc ám của nó. Mọi ý chí tự do của bạn đều biến mất, chỉ còn lại một cái xác biết cử động theo mệnh lệnh. {guardian.ga_name} đau đớn chứng kiến cảnh tượng này, nỗi tuyệt vọng nhấn chìm hắn. Hắn thề sẽ trả thù cho bạn, nhưng sâu thẳm trong lòng, hắn biết rằng bạn đã không còn nữa, chỉ còn một hình hài trống rỗng. Cuộc sống của hắn giờ đây chỉ còn là một hành trình trả thù vô vọng, không có mục đích hay hy vọng nào nữa.",
        choice_a="Bạn trở thành nô lệ, {guardian.ga_name} sống trong đau khổ và báo thù.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-700, silver=-700, ga_exp=-300, dignity_point=-70, ga_health=-999, ga_mana=-999, ga_stamina=-999, force_dead=True,
        next_steps=NextSteps("continue_adventure_4", "continue_adventure_4", "continue_adventure_4", "continue_adventure_4")
    ),

    GuardianQuestLines(
        id="quest_failed_end_total_annihilation_2",
        title="Sự Hủy Diệt Vĩnh Hằng",
        description="Bạn và {guardian.ga_name} bị thực thể nghiền nát và hấp thụ hoàn toàn. Không còn dấu vết nào của sự tồn tại của cả hai. Tên của bạn và {guardian.ga_name} bị xóa sổ khỏi lịch sử, trở thành những linh hồn vô danh trong cơn đói khát bất tận của thực thể. Thung lũng tiếp tục tồn tại với lễ hội vĩnh hằng, và không ai còn nhớ đến sự tồn tại của hai người đã từng cố gắng giải thoát nó. Cả hai bạn mãi mãi là một phần của cơn thịnh nộ không ngừng của thực thể, không bao giờ được giải thoát hay tìm thấy sự bình yên.",
        choice_a="Bạn và {guardian.ga_name} bị xóa sổ khỏi sự tồn tại.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-900, silver=-900, ga_exp=-400, dignity_point=-90, ga_health=-999, ga_mana=-999, ga_stamina=-999, force_dead=True,
        next_steps=NextSteps("continue_adventure_4", "continue_adventure_4", "continue_adventure_4", "continue_adventure_4")
    ),

    GuardianQuestLines(
        id="quest_failed_end_fog_trap",
        title="Mắc Kẹt Trong Sương Mù",
        description="Bạn và {guardian.ga_name} bị mắc kẹt trong một làn sương mù dày đặc, không thể tìm thấy lối thoát. Từng ngày trôi qua, sương mù càng đặc quánh, và cả hai dần mất đi ý thức, chìm vào giấc ngủ vĩnh cửu không bao giờ tỉnh lại. 'Đây là kết thúc của chúng ta,' {guardian.ga_name} thì thầm trước khi bóng tối nuốt chửng cả hai. Hai linh hồn bị giam cầm trong màn sương mù, mãi mãi là một phần của thung lũng bị nguyền rủa, không bao giờ được giải thoát.",
        choice_a="Bạn và {guardian.ga_name} bị mắc kẹt và chìm vào giấc ngủ vĩnh cửu.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-50, silver=-150, ga_exp=-50, dignity_point=-15, ga_health=-25, ga_mana=-25, ga_stamina=-25,
        next_steps=NextSteps("continue_adventure_4", "continue_adventure_4", "continue_adventure_4", "continue_adventure_4")
    ),

    GuardianQuestLines(
        id="quest_failed_end_4",
        title="Thất Bại Đắng Cay",
        description="Nhiệm vụ thất bại. Thung lũng vẫn chìm trong lời nguyền của lễ hội, và những người dân làng vẫn tiếp tục nhảy múa trong vô vọng. {guardian.ga_name} nhìn bạn với ánh mắt thất vọng. 'Ta hy vọng Ngài sẽ rút ra được bài học từ thất bại này.'",
        choice_a="Rút ra bài học đau đớn.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-30, silver=-70, ga_exp=-30, dignity_point=-5,
        next_steps=NextSteps("continue_adventure_4", "continue_adventure_4", "continue_adventure_4", "continue_adventure_4")
    ),

    GuardianQuestLines(
        id="continue_adventure_4",
        title="Hành Trình Tiếp Nối",
        description="Bạn và {guardian.ga_name} rời khỏi thung lũng, mang theo những ký ức ám ảnh về hành trình vừa qua. Những cuộc phiêu lưu mới đang chờ đợi...",
        choice_a="",
        choice_b="", choice_c="", choice_timeout="",
        gold=10, silver=50, ga_exp=10,
        next_steps=NextSteps("", "", "", "")
    )
]


quest_the_ruin_call = [
    GuardianQuestLines(
        id="start",
        title="Tiếng Gọi Từ Phế Tích Lãng Quên",
        description="Một luồng gió lạnh buốt mang theo tiếng vọng ai oán từ phế tích cổ xưa. {guardian.ga_name} khẽ rùng mình. 'Ta cảm nhận được sự tuyệt vọng sâu sắc. Có lẽ chúng ta nên tìm hiểu.'",
        choice_a="Đi thẳng đến phế tích để điều tra.",
        choice_b="Tìm thông tin về lịch sử của phế tích trước.",
        choice_c="Bỏ qua, phế tích này có vẻ nguy hiểm.",
        choice_timeout="{guardian.ga_name} nhìn bạn đầy lo lắng. 'Những tiếng kêu đó không thể phớt lờ!'",
        next_steps=NextSteps(
            choice_a="enter_ruins",
            choice_b="research_ruins_history",
            choice_c="ignore_ruins_outcome",
            timeout="ga_worried_timeout_2"
        ),
        gold=10, silver=100, ga_exp=10, dignity_point=5
    ),

    GuardianQuestLines(
        id="enter_ruins",
        title="Vào Vùng Đất Đổ Nát",
        description="Bạn và {guardian.ga_name} tiến vào phế tích. Những bức tường đổ nát và tượng đá hoang phế hiện ra. {guardian.ga_name} chỉ vào một cánh cửa bị phong ấn. 'Có vẻ có thứ gì đó bị giam giữ bên trong.'",
        choice_a="Cố gắng phá vỡ phong ấn.",
        choice_b="Tìm kiếm lối đi khác.",
        choice_c="Rút lui khỏi phế tích.",
        choice_timeout="{guardian.ga_name} thúc giục. 'Phong ấn đó có thể là chìa khóa để giải mã bí ẩn!'",
        next_steps=NextSteps(
            choice_a="break_seal",
            choice_b="find_another_way",
            choice_c="retreat_from_ruins",
            timeout="ruins_collapse_timeout"
        )
    ),

    GuardianQuestLines(
        id="research_ruins_history",
        title="Giải Mã Lịch Sử Phế Tích",
        description="Bạn và {guardian.ga_name} đến thư viện cổ. Bạn tìm thấy một cuộn da ghi chép về một lời nguyền cổ đại đã phong ấn một linh hồn vĩ đại trong phế tích. Cách hóa giải là sử dụng 'Pha Lê Hồi Sinh'.",
        choice_a="Tìm kiếm Pha Lê Hồi Sinh.",
        choice_b="Trở lại phế tích, thử cách khác.",
        choice_c="Từ bỏ nhiệm vụ vì quá phức tạp.",
        choice_timeout="{guardian.ga_name} nói. 'Chúng ta không có nhiều thời gian để tìm kiếm đâu!'",
        next_steps=NextSteps(
            choice_a="seek_revival_crystal",
            choice_b="enter_ruins",
            choice_c="abandon_quest_ruins",
            timeout="ga_worried_timeout_2"
        )
    ),

    GuardianQuestLines(
        id="break_seal",
        title="Phá Vỡ Phong Ấn",
        description="Bạn và {guardian.ga_name} cùng cố gắng phá vỡ phong ấn. Một luồng năng lượng đen tối bùng ra. {guardian.ga_name} nhanh chóng tạo ra một lá chắn. 'Linh hồn bị giam cầm đang phản kháng!'",
        choice_a="Tiếp tục phá vỡ phong ấn.",
        choice_b="Tìm kiếm cách khác để mở phong ấn.",
        choice_c="Rút lui ngay lập tức.",
        choice_timeout="Năng lượng phong ấn trở nên dữ dội. 'Nó sẽ nuốt chửng chúng ta!' {guardian.ga_name} cảnh báo.",
        next_steps=NextSteps(
            choice_a="continue_break_seal",
            choice_b="seek_revival_crystal",
            choice_c="retreat_from_ruins",
            timeout="seal_overwhelm_outcome"
        )
    ),

    GuardianQuestLines(
        id="find_another_way",
        title="Tìm Lối Đi Khác",
        description="Bạn và {guardian.ga_name} tìm kiếm xung quanh phế tích. Sau một hồi, bạn phát hiện một khe nứt ẩn. {guardian.ga_name} gật đầu. 'Có vẻ đây là lối vào bí mật.'",
        choice_a="Tiến vào khe nứt.",
        choice_b="Vẫn cố gắng phá vỡ phong ấn chính.",
        choice_c="Từ bỏ, quá nguy hiểm.",
        choice_timeout="{guardian.ga_name} thúc giục. 'Chúng ta không có nhiều thời gian khám phá đâu!'",
        next_steps=NextSteps(
            choice_a="enter_hidden_passage",
            choice_b="break_seal",
            choice_c="retreat_from_ruins",
            timeout="ruins_collapse_timeout"
        )
    ),

    GuardianQuestLines(
        id="seek_revival_crystal",
        title="Tìm Kiếm Pha Lê Hồi Sinh",
        description="Bạn và {guardian.ga_name} theo chỉ dẫn trong cuộn da, đến một hang động sâu thẳm. Pha Lê Hồi Sinh tỏa sáng giữa một hồ nước ngầm, được bảo vệ bởi một chướng khí độc hại.",
        choice_a="Tiến lên lấy pha lê.",
        choice_b="Tìm cách vô hiệu hóa chướng khí.",
        choice_c="Kiểm tra xung quanh xem có nguy hiểm nào không.",
        choice_timeout="{guardian.ga_name} nói. 'Pha lê ở ngay trước mắt chúng ta!'",
        next_steps=NextSteps(
            choice_a="take_crystal",
            choice_b="deactivate_poison_gas",
            choice_c="check_for_dangers",
            timeout="crystal_vanishes_timeout"
        )
    ),

    # Final Stage Outcomes (Leading to Bad Endings)
    GuardianQuestLines(
        id="continue_break_seal",
        title="Phong Ấn Vỡ Tan",
        description="Bạn và {guardian.ga_name} cuối cùng đã phá vỡ phong ấn. Một linh hồn rồng khổng lồ xuất hiện, nhưng nó đã kiệt sức. {guardian.ga_name} nói: 'Nó cần được chữa lành để giải thoát hoàn toàn!'",
        choice_a="Sử dụng phép thuật chữa lành.",
        choice_b="Rút lui ngay, linh hồn rồng quá đáng sợ.",
        choice_c="",
        choice_timeout="{guardian.ga_name} nói. 'Chúng ta không thể để nó lại trong tình trạng này!'",
        next_steps=NextSteps(
            choice_a="heal_dragon_spirit_fail", # Changed to lead to a bad ending
            choice_b="retreat_from_ruins",
            choice_c="",
            timeout="dragon_anger_outcome"
        )
    ),

    GuardianQuestLines(
        id="enter_hidden_passage",
        title="Lối Đi Bí Mật",
        description="Bạn và {guardian.ga_name} tiến vào khe nứt. Bạn thấy mình ở một căn phòng bí mật chứa một viên đá cổ. {guardian.ga_name} nhận ra. 'Đây là Viên Đá Giải Thoát! Nó có thể phá vỡ lời nguyền!'",
        choice_a="Sử dụng Viên Đá Giải Thoát.",
        choice_b="Tìm kiếm thêm thông tin.",
        choice_c="",
        choice_timeout="{guardian.ga_name} thúc giục. 'Chúng ta phải sử dụng nó ngay!'",
        next_steps=NextSteps(
            choice_a="use_release_stone_fail", # Changed to lead to a bad ending
            choice_b="research_ruins_history",
            choice_c="",
            timeout="stone_breaks_timeout"
        )
    ),

    GuardianQuestLines(
        id="take_crystal",
        title="Lấy Pha Lê Thành Công",
        description="Bạn chạm vào Pha Lê Hồi Sinh. Một luồng năng lượng thuần khiết lan tỏa, xua tan chướng khí. {guardian.ga_name} reo lên: 'Tuyệt vời! Giờ hãy mang nó về phế tích!'",
        choice_a="Mang pha lê trở lại phế tích.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("return_to_ruins_with_crystal_fail", "", "", "") # Changed to lead to a bad ending
    ),

    GuardianQuestLines(
        id="deactivate_poison_gas",
        title="Vô Hiệu Hóa Chướng Khí",
        description="Bạn và {guardian.ga_name} tìm cách vô hiệu hóa chướng khí. Sau một hồi nỗ lực, luồng khí độc dần tan biến. 'Giờ thì an toàn hơn rồi,' {guardian.ga_name} nói.",
        choice_a="Lấy pha lê.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("take_crystal", "", "", "")
    ),

    GuardianQuestLines(
        id="check_for_dangers",
        title="Kiểm Tra Nguy Hiểm",
        description="Bạn cẩn thận kiểm tra xung quanh hồ nước. Bạn phát hiện một khe nứt ẩn giấu chất độc. {guardian.ga_name} giúp bạn phong tỏa nó. 'May mà chúng ta cẩn thận,' {guardian.ga_name} thở phào.",
        choice_a="Lấy pha lê.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("take_crystal", "", "", "")
    ),

    # Specific Bad Endings from choices
    GuardianQuestLines(
        id="heal_dragon_spirit_fail",
        title="Linh Hồn Rồng Nổi Giận",
        description="Bạn và {guardian.ga_name} cố gắng chữa lành linh hồn rồng, nhưng do thiếu kinh nghiệm, phép thuật của bạn vô tình khiến nó thêm đau đớn. Linh hồn rồng gầm lên, sức mạnh hỗn loạn nuốt chửng cả phế tích.",
        choice_a="Phế tích bị hủy diệt, nhiệm vụ thất bại hoàn toàn.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-20, ga_exp=-100, silver=-200, gold=-100, ga_health=-100, ga_mana=-100, ga_stamina=-100,
        next_steps=NextSteps("quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique")
    ),

    GuardianQuestLines(
        id="use_release_stone_fail",
        title="Viên Đá Phản Phệ",
        description="Bạn sử dụng Viên Đá Giải Thoát. Tuy nhiên, năng lượng từ lời nguyền quá mạnh, khiến viên đá phản phệ. Một làn sóng năng lượng đen tối bao trùm bạn và {guardian.ga_name}, biến phế tích thành một vùng đất hoang tàn vĩnh viễn.",
        choice_a="Bạn và {guardian.ga_name} bị mắc kẹt vĩnh viễn trong lời nguyền. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-20, ga_exp=-100, silver=-200, gold=-100, ga_health=-100, ga_mana=-100, ga_stamina=-100,
        next_steps=NextSteps("quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique")
    ),

    GuardianQuestLines(
        id="return_to_ruins_with_crystal_fail",
        title="Pha Lê Không Hoàn Hảo",
        description="Bạn và {guardian.ga_name} mang Pha Lê Hồi Sinh trở lại phế tích. Khi bạn đặt pha lê lên bệ đá, thay vì giải phóng, nó chỉ tạm thời trấn áp lời nguyền. Linh hồn rồng vẫn còn đó, nhưng giờ nó bị ràng buộc bởi pha lê, trở thành một nô lệ vĩnh viễn.",
        choice_a="Linh hồn bị biến thành nô lệ, nhiệm vụ thất bại bi thảm.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-20, ga_exp=-100, silver=-200, gold=-100, ga_health=-100, ga_mana=-100, ga_stamina=-100,
        next_steps=NextSteps("quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique")
    ),

    # Failures (from timeouts/bad choices)
    GuardianQuestLines(
        id="ignore_ruins_outcome",
        title="Phớt Lờ Tiếng Kêu Cứu",
        description="Bạn quyết định bỏ qua. Vài ngày sau, phế tích trở nên u ám hơn, và những câu chuyện về các linh hồn quấy phá lan rộng. {guardian.ga_name} nhìn bạn với vẻ thất vọng.",
        choice_a="Cảm thấy hối tiếc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-5, ga_exp=-50, silver=-50, gold=-50,
        next_steps=NextSteps("quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique")
    ),

    GuardianQuestLines(
        id="ga_worried_timeout_2",
        title="Ánh Mắt Lo Lắng",
        description="Bạn chần chừ quá lâu. {guardian.ga_name} lắc đầu thất vọng. 'Chúng ta không thể cứu họ nếu cứ đứng đây!' Nhiệm vụ kết thúc vì sự thiếu quyết đoán.",
        choice_a="Cảm thấy bất lực. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-10, ga_exp=-50, silver=-100, gold=-50,
        next_steps=NextSteps("quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique")
    ),

    GuardianQuestLines(
        id="ruins_collapse_timeout",
        title="Phế Tích Sụp Đổ",
        description="Bạn và {guardian.ga_name} chần chừ. Một phần phế tích sụp đổ, chặn mất lối vào và vật thể quý giá. {guardian.ga_name} thở dài buồn bã. 'Đã quá muộn rồi.'",
        choice_a="Cảm thấy nuối tiếc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-5, ga_exp=-50, silver=-100, gold=-50,
        next_steps=NextSteps("quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique")
    ),

    GuardianQuestLines(
        id="retreat_from_ruins",
        title="Rút Lui Khỏi Phế Tích",
        description="Bạn và {guardian.ga_name} quyết định rút lui khỏi phế tích. Bạn cảm thấy một nỗi buồn man mác khi rời đi, biết rằng linh hồn vẫn đang bị giam cầm. 'Chúng ta không thể làm gì lúc này,' {guardian.ga_name} thở dài.",
        choice_a="Rút lui và nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-10, ga_exp=-50, silver=-50, gold=-50,
        next_steps=NextSteps("quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique")
    ),

    GuardianQuestLines(
        id="abandon_quest_ruins",
        title="Từ Bỏ Nhiệm Vụ",
        description="Bạn quyết định rằng nhiệm vụ này quá phức tạp và nguy hiểm. Bạn và {guardian.ga_name} quay lưng lại với số phận của phế tích. 'Ta hy vọng có ai đó khác có thể giúp đỡ,' {guardian.ga_name} nói với giọng buồn bã.",
        choice_a="Cảm thấy nhẹ nhõm, nhưng cũng có chút hối tiếc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-10, ga_exp=-150, silver=-500, gold=-50,
        next_steps=NextSteps("quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique")
    ),

    GuardianQuestLines(
        id="seal_overwhelm_outcome",
        title="Phong Ấn Quá Mạnh",
        description="Bạn chần chừ trong việc quyết định cách tiếp cận. Năng lượng phong ấn bùng phát mạnh mẽ, tấn công bạn và {guardian.ga_name}. {guardian.ga_name} phải tạo lá chắn để bảo vệ bạn, nhưng bị thương nặng.",
        choice_a="Bạn bị tấn công và phải rút lui. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-5, ga_exp=-50, silver=-50, gold=-50, ga_health=-50,
        next_steps=NextSteps("quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique")
    ),

    GuardianQuestLines(
        id="dragon_anger_outcome",
        title="Linh Hồn Rồng Phẫn Nộ",
        description="Bạn chần chừ trong việc quyết định cách tiếp cận linh hồn rồng. Nó gầm lên giận dữ, trở nên mạnh hơn và tấn công bạn. {guardian.ga_name} phải tạo lá chắn để bảo vệ bạn, nhưng đã kiệt sức.",
        choice_a="Bạn bị tấn công và phải rút lui. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-5, ga_exp=-50, silver=-50, gold=-50, ga_stamina=-50,
        next_steps=NextSteps("quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique")
    ),

    GuardianQuestLines(
        id="stone_breaks_timeout",
        title="Viên Đá Tan Vỡ",
        description="Bạn chần chừ quá lâu trước Viên Đá Giải Thoát. Năng lượng của lời nguyền bùng phát mạnh mẽ, khiến viên đá nứt vỡ và tan biến. 'Không! Đã quá muộn rồi!' {guardian.ga_name} thốt lên.",
        choice_a="Viên đá biến mất, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-10, ga_exp=-50, silver=-50, gold=-50,
        next_steps=NextSteps("quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique")
    ),

    GuardianQuestLines(
        id="crystal_vanishes_timeout",
        title="Pha Lê Biến Mất",
        description="Bạn chần chừ quá lâu trước pha lê. Chướng khí bùng phát mạnh mẽ, khiến pha lê tan biến vào hư vô. 'Không! Đã quá muộn rồi!' {guardian.ga_name} thốt lên.",
        choice_a="Pha lê biến mất, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-10, ga_exp=-50, silver=-50, gold=-50,
        next_steps=NextSteps("quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique", "quest_failed_end_unique")
    ),

    # Unique Bad Ending
    GuardianQuestLines(
        id="quest_failed_end_unique",
        title="Lời Nguyền Vĩnh Cửu",
        description="Phế tích cổ xưa không chỉ không được giải thoát mà còn trở nên nguy hiểm hơn. Năng lượng đen tối lan rộng khắp vùng đất, biến mọi thứ thành hoang tàn. {guardian.ga_name} nhìn bạn với ánh mắt đau buồn sâu sắc, 'Có lẽ... chúng ta không bao giờ nên chạm vào bí ẩn này.'",
        choice_a="Bạn cảm thấy gánh nặng của sự thất bại đè nặng lên vai.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-25, ga_exp=-200, silver=-1000, gold=-500, ga_health=-100, ga_mana=-100, ga_stamina=-100,
        next_steps=NextSteps("continue_adventure_4", "continue_adventure_4", "continue_adventure_4", "continue_adventure_4")
    ),

    GuardianQuestLines(
        id="continue_adventure_4",
        title="Hành Trình Tiếp Nối Trong Bóng Tối",
        description="Bạn và {guardian.ga_name} rời khỏi phế tích, mang theo nỗi ám ảnh về thất bại. Vùng đất từng tươi đẹp giờ đây chìm trong bóng tối vĩnh cửu, như một lời nhắc nhở về những gì đã mất...",
        choice_a="",
        choice_b="", choice_c="", choice_timeout="",
        gold=10, silver=100, ga_exp=50,
        next_steps=NextSteps("", "", "", "")
    )
]

#region quest broken oath
quest_broken_oath = [
    GuardianQuestLines(
        id="start",
        title="Lời Thề Tan Vỡ Của Vùng Đất Cằn Cỗi",
        description="Một lời cầu cứu khẩn thiết vang vọng từ Vùng Đất Cằn Cỗi, nơi mà cây cối héo úa và nước biến mất. {guardian.ga_name} nhìn bạn với ánh mắt kiên định. 'Có vẻ như một lời thề cổ xưa đã bị phá vỡ. Ta cảm thấy sự mất cân bằng sâu sắc.'",
        choice_a="Đi đến Vùng Đất Cằn Cỗi để điều tra.",
        choice_b="Tìm hiểu về lịch sử của lời thề cổ xưa.",
        choice_c="Bỏ qua lời cầu cứu, cho rằng đó là chuyện của người địa phương.",
        choice_timeout="{guardian.ga_name} nói với vẻ lo lắng. 'Những lời thề bị phá vỡ có thể dẫn đến thảm họa lớn hơn, Ngài!'",
        next_steps=NextSteps(
            choice_a="enter_barren_lands",
            choice_b="research_ancient_oath",
            choice_c="ignore_plea_outcome",
            timeout="ga_urgent_timeout_1"
        ),
        gold=50, silver=250, ga_exp=40, dignity_point=20
    ),

    GuardianQuestLines(
        id="enter_barren_lands",
        title="Bước Vào Vùng Đất Héo Khô",
        description="Bạn và {guardian.ga_name} đặt chân đến Vùng Đất Cằn Cỗi. Cây cối khô héo thành bụi, sông ngòi cạn kiệt, và không khí nặng nề. {guardian.ga_name} chỉ vào một tượng đài đổ nát. 'Nơi này từng là một khu vườn tươi tốt. Có lẽ bí mật nằm ở đây.'",
        choice_a="Kiểm tra tượng đài đổ nát.",
        choice_b="Tìm kiếm nguồn nước bị biến mất.",
        choice_c="Quay lại, vùng đất này quá nguy hiểm.",
        choice_timeout="{guardian.ga_name} thúc giục. 'Chúng ta cần tìm hiểu nguyên nhân gây ra sự tàn phá này!'",
        next_steps=NextSteps(
            choice_a="examine_ruined_monument",
            choice_b="search_for_missing_water",
            choice_c="retreat_from_barren_lands",
            timeout="monument_cracks_timeout"
        )
    ),

    GuardianQuestLines(
        id="research_ancient_oath",
        title="Giải Mã Lời Thề Cổ Xưa",
        description="Bạn và {guardian.ga_name} đến một thư viện xa xôi, tìm thấy một cuốn sách cổ ghi chép về 'Lời Thề Giao Ước'. Lời thề này bảo vệ vùng đất, nhưng đòi hỏi sự cống hiến từ một dòng họ. Nếu lời thề bị phá vỡ, vùng đất sẽ chết dần.",
        choice_a="Tìm kiếm hậu duệ của dòng họ đã lập lời thề.",
        choice_b="Trở lại Vùng Đất Cằn Cỗi, tìm hiểu tại chỗ.",
        choice_c="Rời bỏ nhiệm vụ, cho rằng nó quá phức tạp.",
        choice_timeout="{guardian.ga_name} nói. 'Ta tin rằng manh mối nằm ở hậu duệ của dòng họ này, Ngài.'",
        next_steps=NextSteps(
            choice_a="find_descendant",
            choice_b="enter_barren_lands",
            choice_c="abandon_quest_broken_oath",
            timeout="ga_urgent_timeout_1"
        ),
        gold=75, silver=300, ga_exp=60, dignity_point=30
    ),

    GuardianQuestLines(
        id="examine_ruined_monument",
        title="Bí Mật Trong Tượng Đài",
        description="Bạn và {guardian.ga_name} kiểm tra tượng đài. Một dòng chữ cổ xuất hiện: 'Khi tình yêu cạn, lời thề tan.' {guardian.ga_name} cau mày. 'Ta cảm thấy một bi kịch đã xảy ra ở đây.'",
        choice_a="Tìm kiếm dấu vết của bi kịch.",
        choice_b="Thử khôi phục tượng đài bằng phép thuật.",
        choice_c="Bỏ qua, tìm kiếm nơi khác.",
        choice_timeout="Tượng đài bắt đầu nứt rạn. 'Chúng ta không còn nhiều thời gian!' {guardian.ga_name} cảnh báo.",
        next_steps=NextSteps(
            choice_a="seek_tragedy_clues",
            choice_b="restore_monument_attempt",
            choice_c="abandon_monument",
            timeout="monument_cracks_timeout"
        )
    ),

    GuardianQuestLines(
        id="find_descendant",
        title="Truy Tìm Hậu Duệ",
        description="Dựa trên thông tin, bạn và {guardian.ga_name} tìm đến một ngôi làng hẻo lánh. Bạn gặp một người phụ nữ già, vẻ mặt u sầu, tên là Elara, hậu duệ cuối cùng của dòng họ. 'Tôi đã phá vỡ lời thề... vì tình yêu,' bà nói.",
        choice_a="Tìm hiểu về câu chuyện của Elara.",
        choice_b="Thuyết phục Elara lập lại lời thề.",
        choice_c="Buộc Elara phải sửa chữa lỗi lầm.",
        choice_timeout="{guardian.ga_name} nói nhỏ. 'Hãy cẩn thận, Ngài. Bà ấy đang đau khổ.'",
        next_steps=NextSteps(
            choice_a="learn_elaras_story",
            choice_b="persuade_elara",
            choice_c="force_elara_outcome",
            timeout="elara_despair_timeout"
        )
    ),

    # New branching path: Seek Tragedy Clues
    GuardianQuestLines(
        id="seek_tragedy_clues",
        title="Dấu Vết Bi Kịch",
        description="Bạn và {guardian.ga_name} tìm kiếm xung quanh tượng đài và phát hiện một ngôi mộ cổ không tên, được bao phủ bởi những bông hoa héo úa. {guardian.ga_name} cảm nhận được một nỗi buồn sâu sắc. 'Có lẽ đây là nơi tình yêu đã chấm dứt.'",
        choice_a="Kiểm tra ngôi mộ.",
        choice_b="Tìm kiếm những ghi chép cổ gần đó.",
        choice_c="Cố gắng cảm nhận năng lượng còn sót lại.",
        choice_timeout="{guardian.ga_name} cau mày. 'Nỗi buồn ở đây quá mạnh mẽ, Ngài.'",
        next_steps=NextSteps(
            choice_a="examine_tomb",
            choice_b="search_nearby_records",
            choice_c="sense_residual_energy",
            timeout="tomb_collapses_timeout"
        )
    ),

    GuardianQuestLines(
        id="examine_tomb",
        title="Nghiên Cứu Ngôi Mộ",
        description="Bên trong ngôi mộ, bạn tìm thấy một chiếc vòng cổ được khắc tên 'Lysander' và một dòng chữ 'Tình yêu vĩnh cửu, bị chia cắt bởi thù hận.' {guardian.ga_name} thì thầm. 'Lysander... tên của người đàn ông mà Elara yêu.'",
        choice_a="Mang chiếc vòng cổ đến cho Elara.",
        choice_b="Tìm cách kết nối với linh hồn Lysander.",
        choice_c="Chôn cất chiếc vòng cổ trở lại.",
        choice_timeout="Ngôi mộ bắt đầu rung chuyển. 'Có lẽ chúng ta đã làm phiền sự yên nghỉ,' {guardian.ga_name} nói.",
        next_steps=NextSteps(
            choice_a="bring_locket_to_elara",
            choice_b="connect_with_lysander_spirit",
            choice_c="rebury_locket",
            timeout="tomb_collapses_timeout"
        ),
        gold=50, silver=150, ga_exp=30, dignity_point=10
    ),

    GuardianQuestLines(
        id="bring_locket_to_elara",
        title="Chiếc Vòng Cổ Của Ký Ức",
        description="Bạn trao chiếc vòng cổ cho Elara. Bà ấy ôm chặt nó, nước mắt chảy dài. 'Lysander... anh ấy vẫn ở đây.' Nỗi đau trong bà vơi đi một chút, thay vào đó là sự chấp nhận. 'Có lẽ... có lẽ tôi có thể thử lại lời thề, vì anh ấy.'",
        choice_a="Giúp Elara lập lại lời thề.",
        choice_b="Khuyên Elara từ bỏ quá khứ.",
        choice_c="",
        choice_timeout="{guardian.ga_name} nói khẽ. 'Hy vọng đang le lói, Ngài.'",
        next_steps=NextSteps(
            choice_a="help_elara_renew_oath",
            choice_b="advise_elara_move_on",
            choice_c="",
            timeout="elara_despair_timeout"
        ),
        dignity_point=20, ga_exp=50
    ),

    GuardianQuestLines(
        id="help_elara_renew_oath",
        title="Hồi Sinh Lời Thề",
        description="Bạn và {guardian.ga_name} hướng dẫn Elara thực hiện nghi lễ tái lập lời thề. Khi lời thề được cất lên, một luồng năng lượng xanh biếc lan tỏa khắp Vùng Đất Cằn Cỗi. Cây cối bắt đầu đâm chồi nảy lộc, sông ngòi chảy lại, và không khí trở nên trong lành. Elara mỉm cười. 'Tôi cảm thấy anh ấy đang ở đây.' {guardian.ga_name} gật đầu. 'Sự cân bằng đã trở lại, Ngài. Nhờ lòng dũng cảm và sự đồng cảm của Ngài.'",
        choice_a="Lời thề được tái lập, vùng đất hồi sinh.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_success_broken_oath", "quest_success_broken_oath", "quest_success_broken_oath", "quest_success_broken_oath"),
        gold=1000, silver=5000, ga_exp=500, dignity_point=250
    ),

    # Continue existing story lines
    GuardianQuestLines(
        id="learn_elaras_story",
        title="Bi Kịch Tình Yêu",
        description="Elara kể về tình yêu cấm đoán của bà với một người đàn ông từ bộ tộc đối địch, người đã chết trong một cuộc xung đột. Vì quá đau khổ, bà đã bỏ rơi lời thề, tin rằng tình yêu của bà đã phản bội tất cả. 'Vùng đất này đã chịu hậu quả của sự yếu đuối của tôi,' bà nói, nước mắt lưng tròng. {guardian.ga_name} nhìn bạn với ánh mắt nặng trĩu. 'Bi kịch này quá sâu sắc để một lời thề có thể hàn gắn, Ngài.'",
        choice_a="Cố gắng an ủi Elara, nhưng nhận ra rằng không có cách nào sửa chữa được sự đổ vỡ này.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("broken_oath_bad_ending", "broken_oath_bad_ending", "broken_oath_bad_ending", "broken_oath_bad_ending"),
        dignity_point=-25, ga_exp=-100, silver=-300, gold=-150,
    ),

    # Failures and generic endings
    GuardianQuestLines(
        id="ignore_plea_outcome",
        title="Thờ Ơ Với Số Phận",
        description="Bạn và {guardian.ga_name} quyết định phớt lờ lời cầu cứu. Vài tuần sau, tin tức về Vùng Đất Cằn Cỗi hoàn toàn chết khô lan truyền, kéo theo nạn đói và sự hỗn loạn. {guardian.ga_name} nhìn bạn đầy thất vọng. 'Ta hy vọng Ngài sẽ không phải hối tiếc về quyết định này.'",
        choice_a="Cảm thấy một nỗi hối tiếc lạnh lẽo. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-50, ga_exp=-200, silver=-500, gold=-250,
        next_steps=NextSteps("quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1")
    ),

    GuardianQuestLines(
        id="ga_urgent_timeout_1",
        title="Sự Chần Chừ Tai Hại",
        description="Bạn chần chừ quá lâu. {guardian.ga_name} thở dài. 'Thời gian đã không còn cho chúng ta. Vùng đất này sẽ không thể chờ đợi.' Nhiệm vụ kết thúc trong sự thất bại đau đớn.",
        choice_a="Bạn cảm thấy bất lực. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1"),
        dignity_point=-30, ga_exp=-150, silver=-250, gold=-125,
    ),

    GuardianQuestLines(
        id="monument_cracks_timeout",
        title="Tượng Đài Sụp Đổ",
        description="Bạn chần chừ quá lâu trong việc kiểm tra tượng đài. Những vết nứt lan rộng, và nó sụp đổ hoàn toàn, chôn vùi mọi manh mối bên dưới. 'Đã quá muộn rồi,' {guardian.ga_name} nói với giọng buồn bã.",
        choice_a="Bạn cảm thấy một sự mất mát. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-20, ga_exp=-125, silver=-200, gold=-100,
        next_steps=NextSteps("quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1")
    ),

    GuardianQuestLines(
        id="retreat_from_barren_lands",
        title="Rút Lui Khỏi Sự Tuyệt Vọng",
        description="Bạn và {guardian.ga_name} quyết định rút lui. Bạn quay lưng lại với Vùng Đất Cằn Cỗi, bỏ mặc số phận của nó. 'Thật đáng tiếc khi chúng ta không thể giúp được gì,' {guardian.ga_name} nói, giọng đầy tiếc nuối.",
        choice_a="Bạn cảm thấy thất bại. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-30, ga_exp=-150, silver=-150, gold=-150,
        next_steps=NextSteps("quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1")
    ),

    GuardianQuestLines(
        id="search_for_missing_water",
        title="Nguồn Nước Biến Mất",
        description="Bạn và {guardian.ga_name} tìm kiếm nguồn nước. Bạn tìm thấy dấu vết của một con sông ngầm đã bị chuyển hướng một cách bí ẩn. {guardian.ga_name} nói: 'Có ai đó đã cố tình làm điều này.'",
        choice_a="Điều tra kẻ gây ra vụ chuyển hướng nước.",
        choice_b="Thử dùng phép thuật để phục hồi dòng chảy.",
        choice_c="Từ bỏ việc tìm kiếm nước.",
        choice_timeout="{guardian.ga_name} hối thúc. 'Nguồn sống của vùng đất này đang bị đe dọa!'",
        next_steps=NextSteps(
            choice_a="investigate_sabotage",
            choice_b="restore_water_flow_attempt",
            choice_c="abandon_water_search",
            timeout="water_source_collapses_timeout"
        )
    ),

    GuardianQuestLines(
        id="investigate_sabotage",
        title="Dấu Vết Kẻ Phá Hoại",
        description="Bạn và {guardian.ga_name} tìm thấy dấu vết của một nhóm pháp sư hắc ám đã chuyển hướng con sông ngầm để tạo ra một đầm lầy độc hại cho nghi lễ của họ. {guardian.ga_name} chuẩn bị vũ khí. 'Chúng ta phải ngăn chặn chúng!'",
        choice_a="Đối đầu với pháp sư hắc ám.",
        choice_b="Tìm cách đảo ngược phép thuật mà không đối đầu.",
        choice_c="Báo động cho chính quyền địa phương.",
        choice_timeout="{guardian.ga_name} cảnh báo. 'Chúng ta không thể chần chừ, Ngài! Chúng sẽ hoàn thành nghi lễ!'",
        next_steps=NextSteps(
            choice_a="confront_dark_mages_outcome",
            choice_b="reverse_spell_attempt",
            choice_c="report_authorities_outcome",
            timeout="dark_mages_succeed_timeout"
        )
    ),

    GuardianQuestLines(
        id="confront_dark_mages_outcome",
        title="Đối Đầu Với Pháp Sư Hắc Ám",
        description="Bạn và {guardian.ga_name} đối mặt với nhóm pháp sư hắc ám. Họ mạnh hơn bạn nghĩ và cuộc chiến diễn ra khốc liệt. Mặc dù bạn và {guardian.ga_name} chiến đấu dũng cảm, số lượng và phép thuật của họ áp đảo. Cuối cùng, bạn và {guardian.ga_name} bị đánh bại và buộc phải rút lui trong đau đớn. 'Ta đã không thể bảo vệ Ngài khỏi hiểm nguy này,' {guardian.ga_name} thều thào, cơ thể đầy thương tích.",
        choice_a="Bạn bị thương nặng và nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-50, ga_exp=-250, silver=-750, gold=-375, ga_health=-250, ga_mana=-250, ga_stamina=-250,
        next_steps=NextSteps("broken_oath_bad_ending", "broken_oath_bad_ending", "broken_oath_bad_ending", "broken_oath_bad_ending")
    ),

    GuardianQuestLines(
        id="restore_monument_attempt",
        title="Khôi Phục Thất Bại",
        description="Bạn cố gắng khôi phục tượng đài bằng phép thuật, nhưng năng lượng của nó đã cạn kiệt. Tượng đài tiếp tục nứt rạn và cuối cùng sụp đổ, chôn vùi mọi thứ. 'Phép thuật không thể sửa chữa những gì đã tan vỡ,' {guardian.ga_name} nói buồn bã.",
        choice_a="Tượng đài sụp đổ, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-20, ga_exp=-125, silver=-150, gold=-75,
        next_steps=NextSteps("quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1")
    ),

    GuardianQuestLines(
        id="abandon_monument",
        title="Bỏ Qua Tượng Đài",
        description="Bạn và {guardian.ga_name} quyết định bỏ qua tượng đài, hy vọng tìm thấy manh mối ở nơi khác. Tuy nhiên, mọi con đường đều dẫn đến ngõ cụt. 'Có lẽ chúng ta đã bỏ lỡ điều quan trọng nhất,' {guardian.ga_name} nói với vẻ hối tiếc.",
        choice_a="Bạn cảm thấy bế tắc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-20, ga_exp=-125, silver=-150, gold=-75,
        next_steps=NextSteps("quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1")
    ),

    GuardianQuestLines(
        id="elara_despair_timeout",
        title="Nỗi Tuyệt Vọng Của Elara",
        description="Bạn chần chừ quá lâu trong việc nói chuyện với Elara. Bà ấy gục xuống, nỗi tuyệt vọng nhấn chìm bà. 'Quá muộn rồi... không còn hy vọng nào nữa,' bà thì thầm. {guardian.ga_name} nhìn bạn với ánh mắt đầy trách móc. 'Chúng ta đã không thể mang lại hy vọng cho bà ấy.'",
        choice_a="Elara chìm trong tuyệt vọng, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-30, ga_exp=-150, silver=-250, gold=-125,
        next_steps=NextSteps("quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1")
    ),

    GuardianQuestLines(
        id="force_elara_outcome",
        title="Cưỡng Ép Elara",
        description="Bạn cố gắng buộc Elara phải lập lại lời thề, nhưng bà ấy phản kháng dữ dội. Nỗi đau và sự phẫn uất trong bà bùng phát, tạo ra một làn sóng năng lượng tiêu cực lan khắp vùng đất, khiến mọi thứ càng trở nên tồi tệ hơn. 'Ngài đã đẩy bà ấy vào vực thẳm,' {guardian.ga_name} nói, ánh mắt đầy thất vọng.",
        choice_a="Vùng đất trở nên tồi tệ hơn. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-75, ga_exp=-250, silver=-500, gold=-250, ga_health=-125, ga_mana=-125, ga_stamina=-125,
        next_steps=NextSteps("broken_oath_bad_ending", "broken_oath_bad_ending", "broken_oath_bad_ending", "broken_oath_bad_ending")
    ),

    GuardianQuestLines(
        id="persuade_elara",
        title="Thuyết Phục Không Thành",
        description="Bạn cố gắng thuyết phục Elara lập lại lời thề, nhưng bà ấy vẫn không thể vượt qua nỗi đau mất mát. 'Tôi không thể... không còn lý do gì nữa,' bà nói, nước mắt chảy dài. Vùng đất tiếp tục héo úa. {guardian.ga_name} nói: 'Ta e là bà ấy đã mất đi tất cả niềm tin.'",
        choice_a="Elara không thể vượt qua, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-20, ga_exp=-125, silver=-150, gold=-75,
        next_steps=NextSteps("broken_oath_bad_ending", "broken_oath_bad_ending", "broken_oath_bad_ending", "broken_oath_bad_ending")
    ),

    # New branching path: search_nearby_records
    GuardianQuestLines(
        id="search_nearby_records",
        title="Ghi Chép Cổ Xưa",
        description="Bạn tìm thấy một bộ sưu tập những cuộn giấy da cổ gần ngôi mộ. Chúng ghi lại câu chuyện tình yêu bi thảm giữa Elara và Lysander, một người từ bộ tộc đối địch, và việc cái chết của Lysander đã khiến Elara từ bỏ lời thề. {guardian.ga_name} nói. 'Kiến thức này sẽ giúp chúng ta hiểu rõ hơn về tình hình.'",
        choice_a="Tìm Elara để chia sẻ những gì đã tìm thấy.",
        choice_b="Tìm kiếm một cách để hóa giải nỗi đau của Elara.",
        choice_c="Giữ lại thông tin và tiếp tục điều tra.",
        choice_timeout="{guardian.ga_name} thúc giục. 'Thời gian đang chống lại chúng ta, Ngài.'",
        next_steps=NextSteps(
            choice_a="share_records_with_elara",
            choice_b="seek_elaras_healing",
            choice_c="keep_info_investigate",
            timeout="elara_despair_timeout"
        ),
        gold=75, silver=200, ga_exp=50, dignity_point=15
    ),

    GuardianQuestLines(
        id="share_records_with_elara",
        title="Tiết Lộ Sự Thật",
        description="Bạn chia sẻ những ghi chép cổ với Elara. Ban đầu, bà ấy đau khổ hơn, nhưng sau đó, một sự bình yên lạ lùng đến với bà. 'Anh ấy không bao giờ muốn điều này,' bà nói, nước mắt đã khô. 'Tôi đã hiểu lầm anh ấy.' Bà ấy nhìn bạn. 'Tôi đã sẵn sàng tái lập lời thề, nếu có cách.'",
        choice_a="Tìm hiểu cách tái lập lời thề.",
        choice_b="Củng cố tinh thần Elara trước khi tái lập lời thề.",
        choice_c="",
        choice_timeout="{guardian.ga_name} nói. 'Bà ấy đang cần sự dẫn dắt của Ngài.'",
        next_steps=NextSteps(
            choice_a="learn_oath_renewal_method",
            choice_b="strengthen_elara_resolve",
            choice_c="",
            timeout="elara_despair_timeout"
        ),
        dignity_point=30, ga_exp=75
    ),

    GuardianQuestLines(
        id="learn_oath_renewal_method",
        title="Phương Pháp Tái Lập Lời Thề",
        description="Bạn và {guardian.ga_name} tìm thấy một ghi chép khác, mô tả nghi lễ tái lập lời thề. Nó yêu cầu một vật phẩm biểu tượng cho tình yêu đích thực và sự tha thứ. {guardian.ga_name} nói: 'Chiếc vòng cổ của Lysander có thể là vật phẩm đó.'",
        choice_a="Thực hiện nghi lễ tái lập lời thề với Elara.",
        choice_b="Tìm kiếm một vật phẩm khác.",
        choice_c="",
        choice_timeout="{guardian.ga_name} thúc giục. 'Không còn thời gian để tìm kiếm nữa.'",
        next_steps=NextSteps(
            choice_a="perform_oath_renewal",
            choice_b="search_for_alternative_item",
            choice_c="",
            timeout="elara_despair_timeout"
        ),
        gold=100, silver=250, ga_exp=60, dignity_point=20
    ),

    GuardianQuestLines(
        id="perform_oath_renewal",
        title="Lời Thề Được Tái Lập",
        description="Bạn và {guardian.ga_name} cùng Elara thực hiện nghi lễ. Với chiếc vòng cổ của Lysander và lòng tha thứ của Elara, lời thề được tái lập. Vùng Đất Cằn Cỗi dần xanh tươi trở lại, hoa nở rộ, và tiếng nước chảy róc rách. Elara cảm ơn bạn với một nụ cười rạng rỡ. 'Tôi đã tìm thấy bình yên.' {guardian.ga_name} nói: 'Ngài đã mang lại sự sống cho vùng đất này, Ngài.'",
        choice_a="Vùng đất hồi sinh, nhiệm vụ thành công rực rỡ.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_success_broken_oath", "quest_success_broken_oath", "quest_success_broken_oath", "quest_success_broken_oath"),
        gold=1250, silver=6000, ga_exp=600, dignity_point=300
    ),

    # New branching path: sense_residual_energy
    GuardianQuestLines(
        id="sense_residual_energy",
        title="Năng Lượng Bi Ai",
        description="Bạn cố gắng cảm nhận năng lượng còn sót lại từ tượng đài. Một dòng chảy năng lượng lạnh lẽo, đầy bi ai lướt qua bạn, mang theo hình ảnh của một tình yêu tan vỡ và sự tuyệt vọng. {guardian.ga_name} lùi lại. 'Năng lượng này... nó có thể làm suy yếu ý chí của Ngài.'",
        choice_a="Cố gắng thâm nhập sâu hơn vào năng lượng.",
        choice_b="Rút lui và tìm cách khác.",
        choice_c="Tìm kiếm nguồn gốc của năng lượng này.",
        choice_timeout="{guardian.ga_name} cảnh báo. 'Ngài đang gặp nguy hiểm, Ngài!'",
        next_steps=NextSteps(
            choice_a="deep_dive_into_energy",
            choice_b="retreat_from_energy",
            choice_c="find_energy_source",
            timeout="overwhelmed_by_sorrow"
        ),
        gold=-20, silver=-50, ga_exp=-10, ga_mana=-10, ga_stamina=-10
    ),

    GuardianQuestLines(
        id="deep_dive_into_energy",
        title="Hố Sâu Tuyệt Vọng",
        description="Bạn thâm nhập sâu hơn vào dòng năng lượng. Những ký ức đau khổ của Elara và Lysander ập đến, nhấn chìm bạn trong nỗi buồn và sự mất mát. Bạn cảm thấy sức lực cạn kiệt, ý chí suy yếu. {guardian.ga_name} cố gắng kéo bạn ra, nhưng bạn đã quá chìm sâu. 'Ngài phải chống lại nó!' hắn gầm lên.",
        choice_a="Bạn bị nhấn chìm trong nỗi tuyệt vọng, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("broken_oath_bad_ending", "broken_oath_bad_ending", "broken_oath_bad_ending", "broken_oath_bad_ending"),
        dignity_point=-40, ga_exp=-150, silver=-400, gold=-200, ga_health=-100, ga_mana=-100, ga_stamina=-100,
    ),

    # Failures and generic endings continued
    GuardianQuestLines(
        id="tomb_collapses_timeout",
        title="Ngôi Mộ Sụp Đổ",
        description="Bạn chần chừ quá lâu, và ngôi mộ cuối cùng cũng sụp đổ, chôn vùi mọi bí mật. 'Chúng ta đã bỏ lỡ cơ hội cuối cùng,' {guardian.ga_name} nói với vẻ thất thần.",
        choice_a="Ngôi mộ sụp đổ, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-15, ga_exp=-75, silver=-150, gold=-75,
        next_steps=NextSteps("quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1")
    ),

    GuardianQuestLines(
        id="rebury_locket",
        title="Chôn Vùi Ký Ức",
        description="Bạn quyết định chôn cất chiếc vòng cổ trở lại, tin rằng nó nên được yên nghỉ. 'Có lẽ đó là cách tốt nhất,' {guardian.ga_name} nói, dù giọng hắn vẫn còn chút băn khoăn. Bạn đã bỏ lỡ cơ hội để giải quyết vấn đề.",
        choice_a="Bạn chôn vùi chiếc vòng cổ, nhiệm vụ không được giải quyết triệt để.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-10, ga_exp=-50, silver=-100, gold=-50,
        next_steps=NextSteps("broken_oath_bad_ending", "broken_oath_bad_ending", "broken_oath_bad_ending", "broken_oath_bad_ending")
    ),

    GuardianQuestLines(
        id="advise_elara_move_on",
        title="Khuyên Elara Buông Bỏ",
        description="Bạn khuyên Elara nên từ bỏ quá khứ. Bà ấy gật đầu buồn bã, nhưng nỗi đau vẫn còn đó. 'Có lẽ Ngài đúng, nhưng trái tim tôi không thể quên.' Vùng đất chỉ phục hồi một phần, không hoàn toàn. {guardian.ga_name} thở dài. 'Đôi khi, nỗi đau quá lớn để buông bỏ hoàn toàn.'",
        choice_a="Vùng đất phục hồi một phần, nhưng Elara vẫn đau khổ.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=10, ga_exp=25, silver=100, gold=50,
        next_steps=NextSteps("partial_success_haunted_by_past", "partial_success_haunted_by_past", "partial_success_haunted_by_past", "partial_success_haunted_by_past")
    ),

    GuardianQuestLines(
        id="partial_success_haunted_by_past",
        title="Chiến Thắng Mong Manh",
        description="Vùng Đất Cằn Cỗi đã hồi sinh một phần, nhưng nỗi ám ảnh về lời thề tan vỡ và bi kịch tình yêu vẫn còn đó. Elara sống những ngày còn lại trong sự bình yên mong manh, nhưng không bao giờ thực sự thoát khỏi quá khứ. {guardian.ga_name} nói: 'Chúng ta đã làm những gì có thể, Ngài, nhưng một số vết thương không bao giờ lành hoàn toàn.'",
        choice_a="Nhiệm vụ thành công một phần, nhưng vẫn còn nỗi buồn.",
        choice_b="", choice_c="", choice_timeout="",
        gold=500, silver=2000, ga_exp=250, dignity_point=100,
        next_steps=NextSteps("continue_adventure_1", "continue_adventure_1", "continue_adventure_1", "continue_adventure_1")
    ),

    GuardianQuestLines(
        id="seek_elaras_healing",
        title="Tìm Kiếm Liệu Pháp Chữa Lành",
        description="Bạn tìm kiếm các phương pháp chữa lành tâm hồn cho Elara, từ các pháp sư chữa bệnh đến những phương thuốc thảo dược cổ xưa. Cuối cùng, bạn tìm thấy một bài hát ru cổ có khả năng xoa dịu nỗi đau. {guardian.ga_name} nói: 'Một phương pháp nhẹ nhàng hơn, nhưng có lẽ hiệu quả.'",
        choice_a="Hát bài hát ru cho Elara.",
        choice_b="Tìm kiếm một phương pháp mạnh mẽ hơn.",
        choice_c="",
        choice_timeout="{guardian.ga_name} thúc giục. 'Bà ấy đang cần sự giúp đỡ của Ngài!'",
        next_steps=NextSteps(
            choice_a="sing_lullaby_to_elara",
            choice_b="seek_stronger_healing",
            choice_c="",
            timeout="elara_despair_timeout"
        ),
        gold=75, silver=200, ga_exp=40, dignity_point=15
    ),

    GuardianQuestLines(
        id="sing_lullaby_to_elara",
        title="Giai Điệu Bình Yên",
        description="Bạn hát bài hát ru cổ cho Elara. Giai điệu nhẹ nhàng thấm vào tâm hồn bà, xoa dịu nỗi đau và mang lại sự bình yên. Elara ngủ thiếp đi, lần đầu tiên sau nhiều năm, một nụ cười nhẹ nhàng nở trên môi. Khi tỉnh dậy, bà ấy nói: 'Tôi... tôi đã sẵn sàng tái lập lời thề. Vì tương lai, không chỉ vì quá khứ.'",
        choice_a="Giúp Elara tái lập lời thề.",
        choice_b="Để Elara nghỉ ngơi thêm.",
        choice_c="",
        choice_timeout="{guardian.ga_name} nói. 'Hy vọng đã trở lại, Ngài.'",
        next_steps=NextSteps(
            choice_a="help_elara_renew_oath",
            choice_b="let_elara_rest",
            choice_c="",
            timeout="elara_despair_timeout"
        ),
        dignity_point=40, ga_exp=100
    ),

    GuardianQuestLines(
        id="let_elara_rest",
        title="Bình Yên Tạm Thời",
        description="Bạn để Elara nghỉ ngơi thêm. Bà ấy có được một giấc ngủ sâu, nhưng sự chần chừ của bạn đã khiến bạn mất đi động lực. 'Chúng ta cần hành động nhanh chóng, Ngài,' {guardian.ga_name} nói. 'Vùng đất đang chờ đợi.'",
        choice_a="Trở lại để giúp Elara tái lập lời thề.",
        choice_b="Tìm kiếm các giải pháp khác.",
        choice_c="",
        choice_timeout="{guardian.ga_name} nói. 'Sự bình yên này sẽ không kéo dài mãi.'",
        next_steps=NextSteps(
            choice_a="help_elara_renew_oath",
            choice_b="seek_alternative_solutions",
            choice_c="",
            timeout="elara_despair_timeout"
        ),
        gold=-20, silver=-50, ga_exp=-10, dignity_point=-5
    ),

    # New branching path: connect_with_lysander_spirit
    GuardianQuestLines(
        id="connect_with_lysander_spirit",
        title="Thần Giao Cách Cảm Với Linh Hồn",
        description="Bạn cố gắng kết nối với linh hồn của Lysander. Một linh hồn mờ ảo hiện ra, đầy đau khổ và tiếc nuối. Lysander muốn Elara tìm thấy hạnh phúc và giải thoát khỏi lời nguyền. 'Hãy nói với cô ấy... hãy tha thứ,' linh hồn thì thầm rồi tan biến. {guardian.ga_name} nói. 'Một linh hồn cao thượng.'",
        choice_a="Đến nói chuyện với Elara.",
        choice_b="Tìm cách giúp Lysander siêu thoát hoàn toàn.",
        choice_c="",
        choice_timeout="{guardian.ga_name} thúc giục. 'Lysander đã nói, Ngài.'",
        next_steps=NextSteps(
            choice_a="talk_to_elara_about_lysander",
            choice_b="help_lysander_pass_on",
            choice_c="",
            timeout="tomb_collapses_timeout"
        ),
        gold=100, silver=300, ga_exp=75, dignity_point=25
    ),

    GuardianQuestLines(
        id="talk_to_elara_about_lysander",
        title="Lời Nhắn Từ Quá Khứ",
        description="Bạn kể cho Elara nghe về cuộc gặp gỡ với linh hồn Lysander và lời nhắn của anh ấy. Elara bật khóc, nhưng đó là những giọt nước mắt của sự giải thoát. 'Anh ấy muốn tôi tha thứ... cho chính mình.' Bà ấy đứng dậy, một quyết tâm mới trong mắt. 'Tôi sẽ tái lập lời thề. Vì anh ấy, và vì vùng đất này.'",
        choice_a="Giúp Elara tái lập lời thề.",
        choice_b="Tìm một vật phẩm kỷ niệm của Lysander.",
        choice_c="",
        choice_timeout="{guardian.ga_name} nói. 'Hy vọng đã đến, Ngài.'",
        next_steps=NextSteps(
            choice_a="help_elara_renew_oath",
            choice_b="find_lysander_memento",
            choice_c="",
            timeout="elara_despair_timeout"
        ),
        dignity_point=50, ga_exp=125
    ),

    # New branching path: reverse_spell_attempt
    GuardianQuestLines(
        id="reverse_spell_attempt",
        title="Đảo Ngược Phép Thuật",
        description="Bạn và {guardian.ga_name} tìm thấy cuộn kinh cổ về cách đảo ngược phép thuật chuyển hướng dòng chảy. Quá trình này phức tạp và nguy hiểm, đòi hỏi sự tập trung tuyệt đối. {guardian.ga_name} căng thẳng. 'Chúng ta phải cẩn thận, Ngài.'",
        choice_a="Cố gắng đảo ngược phép thuật.",
        choice_b="Tìm kiếm sự giúp đỡ từ một pháp sư.",
        choice_c="Rút lui và tìm cách khác.",
        choice_timeout="Phép thuật bắt đầu phản ứng dữ dội. 'Nó đang trở nên mất kiểm soát!' {guardian.ga_name} hét lên.",
        next_steps=NextSteps(
            choice_a="attempt_reverse_spell",
            choice_b="seek_mage_assistance",
            choice_c="retreat_from_spell",
            timeout="spell_backlash_timeout"
        ),
        gold=75, silver=200, ga_exp=50, dignity_point=15
    ),

    GuardianQuestLines(
        id="attempt_reverse_spell",
        title="Nỗ Lực Thất Bại",
        description="Bạn cố gắng đảo ngược phép thuật, nhưng sự phức tạp của nó vượt quá khả năng của bạn. Năng lượng ma thuật bùng phát, gây ra một vụ nổ nhỏ và làm bạn và {guardian.ga_name} bị thương nhẹ. 'Quá khó,' {guardian.ga_name} nói, phủi bụi.",
        choice_a="Bạn và {guardian.ga_name} bị thương nhẹ, nhiệm vụ gặp trở ngại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-10, ga_exp=-30, silver=-75, gold=-40, ga_health=-10, ga_mana=-10, ga_stamina=-10,
        next_steps=NextSteps("investigate_sabotage", "investigate_sabotage", "investigate_sabotage", "investigate_sabotage")
    ),

    # New branching path: report_authorities_outcome
    GuardianQuestLines(
        id="report_authorities_outcome",
        title="Báo Động Chính Quyền",
        description="Bạn và {guardian.ga_name} báo động cho chính quyền địa phương về nhóm pháp sư hắc ám. Họ cử binh lính đến điều tra, nhưng quá trình này chậm chạp. Vài ngày sau, bạn nhận được tin rằng pháp sư hắc ám đã hoàn thành nghi lễ của họ, và đầm lầy độc hại đã lan rộng. 'Đã quá muộn rồi,' {guardian.ga_name} nói với vẻ mặt u ám.",
        choice_a="Chính quyền quá chậm trễ, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-20, ga_exp=-100, silver=-250, gold=-125,
        next_steps=NextSteps("broken_oath_bad_ending", "broken_oath_bad_ending", "broken_oath_bad_ending", "broken_oath_bad_ending")
    ),

    # New branching path: quest_success_broken_oath - Add new intermediate steps here!
    GuardianQuestLines(
        id="quest_success_broken_oath",
        title="Bình Minh Trở Lại",
        description="Vùng Đất Cằn Cỗi đã hoàn toàn hồi sinh, vượt xa kỳ vọng. Cây cối xanh tươi rậm rạp, sông hồ đầy ắp nước trong lành, và muông thú trở về. Người dân địa phương tổ chức lễ hội lớn để tôn vinh bạn và {guardian.ga_name}. Elara, giờ đã bình yên, trở thành người gìn giữ lời thề mới. {guardian.ga_name} mỉm cười. 'Ngài đã mang lại sự sống và hy vọng cho một vùng đất tưởng chừng đã chết. Một kỳ công vĩ đại!'",
        choice_a="Nhiệm vụ hoàn thành xuất sắc, vùng đất thịnh vượng.",
        choice_b="", choice_c="", choice_timeout="",
        gold=2500, silver=12000, ga_exp=1000, dignity_point=500,
        next_steps=NextSteps("continue_adventure_1", "continue_adventure_1", "continue_adventure_1", "continue_adventure_1")
    ),

    # Final Bad Endings
    GuardianQuestLines(
        id="broken_oath_bad_ending",
        title="Vùng Đất Vĩnh Viễn Chết",
        description="Bi kịch tình yêu đã phá hủy lời thề, và không có gì có thể hàn gắn được sự đổ vỡ này. Vùng Đất Cằn Cỗi chìm trong sự hoang tàn vĩnh viễn, trở thành một minh chứng cho tình yêu bị phản bội và lời thề bị phá vỡ. {guardian.ga_name} đứng bên bạn, ánh mắt buồn bã nhìn về phía chân trời. 'Thật đáng buồn khi ta không thể thay đổi được số phận này, Ngài.'",
        choice_a="Bạn và {guardian.ga_name} rời đi, mang theo nỗi đau thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-75, ga_exp=-500, silver=-1250, gold=-625, ga_health=-250, ga_mana=-250, ga_stamina=-250,
        next_steps=NextSteps("continue_adventure_1", "continue_adventure_1", "continue_adventure_1", "continue_adventure_1")
    ),

    GuardianQuestLines(
        id="quest_failed_end_1",
        title="Thất Bại Đau Đớn",
        description="Nhiệm vụ thất bại. Vùng Đất Cằn Cỗi vẫn chìm trong cảnh hoang tàn, và lời thề bị phá vỡ vẫn còn đó. {guardian.ga_name} nhìn bạn với ánh mắt thất vọng. 'Ta hy vọng Ngài sẽ rút ra được bài học từ thất bại này.'",
        choice_a="Rút ra bài học đau đớn.",
        dignity_point=-30, ga_exp=-150, silver=-150, gold=-150,
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("continue_adventure_1", "continue_adventure_1", "continue_adventure_1", "continue_adventure_1")
    ),

    GuardianQuestLines(
        id="continue_adventure_1",
        title="Hành Trình Tiếp Nối",
        description="Bạn và {guardian.ga_name} rời khỏi Vùng Đất Cằn Cỗi, mang theo những ký ức về hành trình vừa qua. Những cuộc phiêu lưu mới đang chờ đợi...",
        choice_a="",
        choice_b="", choice_c="", choice_timeout="",
        ga_exp=750, silver=25000, gold=1250,
        next_steps=NextSteps("", "", "", "")
    )
]

#region quest_unamed_village
quest_ruin_whisper = [
    GuardianQuestLines(
        id="start",
        title="Bí Mật Của Tàn Tích Thì Thầm",
        description="Bạn và {guardian.ga_name} phát hiện một bản đồ cổ xưa dẫn đến 'Tàn Tích Thì Thầm' - một nơi được đồn đại chứa đựng tri thức vô tận hoặc một lời nguyền kinh hoàng. {guardian.ga_name} khẽ nghiêng đầu. 'Nơi này mang một năng lượng rất... cổ xưa, Ngài.'",
        choice_a="Lập tức lên đường đến tàn tích.",
        choice_b="Tìm hiểu thêm thông tin về 'Tàn Tích Thì Thầm'.",
        choice_c="Bỏ qua, tin đồn thường chỉ là mê tín.",
        choice_timeout="{guardian.ga_name} cau mày. 'Sự im lặng của nơi này khiến ta lo lắng, Ngài.'",
        next_steps=NextSteps(
            choice_a="journey_to_ruins",
            choice_b="research_ruins",
            choice_c="ignore_ruins",
            timeout="guardian_urges_investigation"
        ),
        gold=100, silver=500, ga_exp=75, dignity_point=25
    ),

    GuardianQuestLines(
        id="journey_to_ruins",
        title="Hành Trình Qua Lãng Quên",
        description="Bạn và {guardian.ga_name} vượt qua những khu rừng rậm rạp và đầm lầy âm u để đến được Tàn Tích Thì Thầm. Những công trình đá đổ nát, phủ đầy rêu phong, đứng sừng sững như những bóng ma. Một luồng gió lạnh buốt mang theo những tiếng thì thầm không rõ nguồn gốc. {guardian.ga_name} nắm chặt vũ khí. 'Những tiếng nói này... chúng không đến từ thế giới của chúng ta, Ngài.'",
        choice_a="Đi sâu vào tàn tích, khám phá lối vào chính.",
        choice_b="Tìm kiếm những dấu vết hoặc hiện vật xung quanh tàn tích.",
        choice_c="Cẩn thận dựng trại ở ngoại vi, quan sát qua đêm.",
        choice_timeout="{guardian.ga_name} nhìn quanh cảnh vật. 'Ta không nghĩ chúng ta nên ở lại đây quá lâu, Ngài.'",
        next_steps=NextSteps(
            choice_a="enter_ruins",
            choice_b="search_artifacts",
            choice_c="camp_outside_ruins",
            timeout="ruins_influence_timeout"
        )
    ),

    GuardianQuestLines(
        id="research_ruins",
        title="Những Cuốn Sách Bụi Bặm",
        description="Bạn và {guardian.ga_name} dành thời gian tìm hiểu về Tàn Tích Thì Thầm trong các thư viện cổ. Bạn phát hiện ra rằng nó từng là một học viện cổ đại bị hủy hoại bởi một nghi lễ thất bại, giải phóng một thực thể tâm linh gọi là 'Kẻ Thì Thầm'. {guardian.ga_name} nghiêm nghị. 'Đây không phải là một nơi để tìm kiếm kho báu, Ngài, mà là một lăng mộ.'",
        choice_a="Chuẩn bị kỹ lưỡng và tiến vào tàn tích.",
        choice_b="Tìm kiếm các nghi lễ hoặc cách để phong ấn Kẻ Thì Thầm.",
        choice_c="Cân nhắc từ bỏ nhiệm vụ vì quá nguy hiểm.",
        choice_timeout="{guardian.ga_name} thở dài. 'Sự im lặng này có thể nuốt chửng chúng ta, Ngài.'",
        next_steps=NextSteps(
            choice_a="journey_to_ruins",
            choice_b="seek_sealing_rituals",
            choice_c="abandon_ruins_quest",
            timeout="guardian_urges_investigation"
        ),
        gold=50, silver=200, ga_exp=30, dignity_point=15
    ),

    GuardianQuestLines(
        id="enter_ruins",
        title="Hành Lang Vô Tận",
        description="Bạn và {guardian.ga_name} tiến vào tàn tích qua một cổng đá khổng lồ. Bên trong là một mê cung của những hành lang tối tăm và những căn phòng đổ nát. Tiếng thì thầm càng rõ ràng hơn, như hàng ngàn giọng nói cùng gọi tên bạn. {guardian.ga_name} nhíu mày. 'Những tiếng thì thầm này đang cố gắng xâm nhập tâm trí Ngài!'",
        choice_a="Tiến sâu hơn, cố gắng tìm nguồn gốc tiếng thì thầm.",
        choice_b="Tìm kiếm các thư viện hoặc phòng nghiên cứu cổ.",
        choice_c="Cố gắng tìm lối thoát an toàn.",
        choice_timeout="Tiếng thì thầm trở nên chói tai. 'Ta không thể chịu đựng thêm nữa!' {guardian.ga_name} hét lên.",
        next_steps=NextSteps(
            choice_a="pursue_whispers",
            choice_b="find_research_rooms",
            choice_c="seek_safe_exit_ruins",
            timeout="whispers_overwhelm"
        )
    ),

    GuardianQuestLines(
        id="search_artifacts",
        title="Vật Phẩm Bị Lãng Quên",
        description="Bạn và {guardian.ga_name} tìm thấy một chiếc bùa hộ mệnh cũ kỹ bị chôn vùi trong đất. Nó phát ra một luồng sáng yếu ớt khi tiếng thì thầm vọng đến gần. {guardian.ga_name} cầm lấy nó. 'Thứ này có thể giúp chúng ta chống lại Kẻ Thì Thầm.'",
        choice_a="Sử dụng bùa hộ mệnh để khuếch tán tiếng thì thầm.",
        choice_b="Giữ lại bùa hộ mệnh, tiếp tục khám phá.",
        choice_c="Phá hủy bùa hộ mệnh vì sợ nó có thể là bẫy.",
        choice_timeout="Bùa hộ mệnh phát sáng mạnh hơn. 'Nó đang phản ứng với Ngài!' {guardian.ga_name} nói.",
        next_steps=NextSteps(
            choice_a="use_amulet_deflect",
            choice_b="keep_amulet_explore",
            choice_c="destroy_amulet_outcome",
            timeout="use_amulet_deflect"
        ),
        gold=75, silver=250, ga_exp=40, dignity_point=15
    ),

    GuardianQuestLines(
        id="pursue_whispers",
        title="Căn Phòng Dội Âm",
        description="Tiếng thì thầm dẫn bạn và {guardian.ga_name} đến một căn phòng lớn, nơi không khí đặc quánh năng lượng. Những tiếng nói vọng ra từ mọi phía, thì thầm những bí mật đen tối và những lời hứa hẹn cám dỗ. {guardian.ga_name} bịt tai. 'Ngài phải chống lại chúng, Ngài! Chúng là ảo ảnh!'",
        choice_a="Lắng nghe những lời thì thầm để tìm ra sự thật.",
        choice_b="Cố gắng phá hủy nguồn phát ra tiếng thì thầm.",
        choice_c="Tìm cách phong tỏa căn phòng này.",
        choice_timeout="{guardian.ga_name} hét lên. 'Chúng đang cố gắng phá vỡ ý chí Ngài!'",
        next_steps=NextSteps(
            choice_a="listen_to_whispers",
            choice_b="destroy_whisper_source",
            choice_c="seal_whisper_room",
            timeout="whispers_overwhelm"
        )
    ),

    GuardianQuestLines(
        id="find_research_rooms",
        title="Thư Viện Tan Hoang",
        description="Bạn và {guardian.ga_name} tìm thấy thư viện. Sách vở nằm rải rác, nhưng một số cuộn giấy da vẫn còn nguyên vẹn. Bạn đọc được về những nỗ lực phong ấn Kẻ Thì Thầm của các học giả cổ đại. {guardian.ga_name} chỉ vào một bản vẽ. 'Đây là một nghi lễ... nhưng nó cần một sự hy sinh.'",
        choice_a="Tìm hiểu thêm về nghi lễ phong ấn.",
        choice_b="Tìm kiếm thông tin về điểm yếu của Kẻ Thì Thầm.",
        choice_c="Mang theo những cuộn giấy quan trọng và rời đi.",
        choice_timeout="{guardian.ga_name} hối thúc. 'Thời gian không chờ đợi chúng ta, Ngài!'",
        next_steps=NextSteps(
            choice_a="learn_sealing_ritual",
            choice_b="find_whisper_weakness",
            choice_c="leave_with_scrolls",
            timeout="whispers_overwhelm"
        ),
        gold=100, silver=300, ga_exp=60, dignity_point=20
    ),

    GuardianQuestLines(
        id="listen_to_whispers",
        title="Lời Hứa Giả Dối",
        description="Bạn cố gắng lắng nghe những lời thì thầm. Chúng hứa hẹn cho bạn sức mạnh, tri thức, và quyền năng không giới hạn, đổi lại linh hồn bạn. {guardian.ga_name} cố gắng kéo bạn lại. 'Chủ nhân, đừng nghe chúng! Đó là lời nguyền rủa!' Nhưng những lời hứa ngọt ngào dần cuốn lấy bạn. {guardian.ga_name} nhìn bạn với ánh mắt đau đớn, hắn hiểu rằng bạn đã rơi vào cạm bẫy của Kẻ Thì Thầm. Bạn cười một nụ cười trống rỗng, và Kẻ Thì Thầm thì thầm trong tâm trí bạn: 'Ngươi đã thuộc về ta, mãi mãi...'",
        choice_a="Linh hồn bạn bị Kẻ Thì Thầm chiếm đoạt hoàn toàn.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_possessed_whispers", "quest_failed_end_possessed_whispers", "quest_failed_end_possessed_whispers", "quest_failed_end_possessed_whispers"),
        gold=-2000, silver=-2000, ga_exp=-750, dignity_point=-150, ga_health=-999, ga_mana=-999, ga_stamina=-999, force_dead=True
    ),

    GuardianQuestLines(
        id="learn_sealing_ritual",
        title="Nghi Lễ Tối Thượng",
        description="Bạn và {guardian.ga_name} nghiên cứu sâu hơn. Nghi lễ phong ấn yêu cầu một linh hồn tinh khiết và một sức mạnh ý chí phi thường để trói buộc Kẻ Thì Thầm vĩnh viễn. {guardian.ga_name} nhìn bạn. 'Ta sẽ giúp Ngài thực hiện nghi lễ, Ngài.'",
        choice_a="Thực hiện nghi lễ phong ấn.",
        choice_b="Tìm kiếm một cách khác, không cần hy sinh.",
        choice_c="",
        choice_timeout="{guardian.ga_name} nói khẽ. 'Chúng ta không còn nhiều thời gian để do dự, Ngài.'",
        next_steps=NextSteps(
            choice_a="perform_sealing_ritual",
            choice_b="seek_alternative_method",
            choice_c="",
            timeout="whispers_overwhelm"
        )
    ),

    GuardianQuestLines(
        id="perform_sealing_ritual",
        title="Sự Hy Sinh Cuối Cùng",
        description="Bạn và {guardian.ga_name} bắt đầu nghi lễ. Kẻ Thì Thầm gào thét, tấn công dữ dội. {guardian.ga_name} dồn toàn bộ sức mạnh, tạo ra một lá chắn bảo vệ bạn. Khi nghi lễ gần hoàn tất, một linh hồn tinh khiết cần được dâng hiến. {guardian.ga_name} mỉm cười với bạn, 'Ta... sẽ luôn bên Ngài, Chủ nhân.' Hắn lao vào trung tâm nghi lễ, linh hồn hắn tan biến để trói buộc Kẻ Thì Thầm vĩnh viễn. Tàn tích rung chuyển, và khi mọi thứ lắng xuống, chỉ còn lại sự im lặng. Kẻ Thì Thầm đã bị phong ấn, nhưng {guardian.ga_name} đã không còn nữa. Bạn gục xuống, tiếng thì thầm cuối cùng trong tâm trí bạn là giọng nói của hắn. Bạn đã cứu thế giới, nhưng đổi lại một cái giá quá đắt, một nỗi đau không thể xóa nhòa, mãi mãi là một cái bóng của người bạn đồng hành trung thành đã hy sinh vì bạn.",
        choice_a="Kẻ Thì Thầm bị phong ấn, nhưng {guardian.ga_name} đã hy sinh.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_guardian_sacrifice", "quest_failed_end_guardian_sacrifice", "quest_failed_end_guardian_sacrifice", "quest_failed_end_guardian_sacrifice"),
        gold=0, silver=0, ga_exp=-999, dignity_point=-999, ga_health=-999, ga_mana=-999, ga_stamina=-999
    ),

    # Failures and generic endings
    GuardianQuestLines(
        id="ignore_ruins",
        title="Phớt Lờ Lời Nguyền",
        description="Bạn quyết định bỏ qua Tàn Tích Thì Thầm. Theo thời gian, những câu chuyện về những người mất trí, những giọng nói trong đầu họ bắt đầu lan truyền. {guardian.ga_name} nhìn bạn với ánh mắt nặng trĩu. 'Đôi khi, nguy hiểm lớn nhất không phải là thứ chúng ta đối mặt, mà là thứ chúng ta phớt lờ.'",
        choice_a="Cảm thấy hối tiếc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        gold=-75, silver=-250, ga_exp=-75, dignity_point=-25,
        next_steps=NextSteps("quest_failed_end_5", "quest_failed_end_5", "quest_failed_end_5", "quest_failed_end_5")
    ),

    GuardianQuestLines(
        id="guardian_urges_investigation",
        title="Lời Thúc Giục Bị Bỏ Qua",
        description="Bạn chần chừ quá lâu. {guardian.ga_name} thở dài. 'Sự do dự của Ngài đã tước đi cơ hội can thiệp. Ta cảm thấy tiếng thì thầm đang lan rộng.' Nhiệm vụ kết thúc trong sự không chắc chắn.",
        choice_a="Bạn cảm thấy bất lực. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        gold=-50, silver=-150, ga_exp=-50, dignity_point=-10,
        next_steps=NextSteps("quest_failed_end_5", "quest_failed_end_5", "quest_failed_end_5", "quest_failed_end_5")
    ),

    GuardianQuestLines(
        id="ruins_influence_timeout",
        title="Ảnh Hưởng Của Tàn Tích",
        description="Bạn chần chừ quá lâu. Tiếng thì thầm từ tàn tích trở nên mạnh mẽ hơn, xâm nhập vào tâm trí bạn, gây ra ảo ảnh và sự hoang mang. {guardian.ga_name} cố gắng bảo vệ bạn, nhưng cả hai đều bị ảnh hưởng. 'Chúng ta phải thoát ra!' {guardian.ga_name} gầm lên.",
        choice_a="Bạn và {guardian.ga_name} bị ảnh hưởng bởi tàn tích.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-125, silver=-250, ga_exp=-125, dignity_point=-25, ga_health=-50, ga_mana=-50, ga_stamina=-50,
        next_steps=NextSteps("quest_failed_end_haunted", "quest_failed_end_haunted", "quest_failed_end_haunted", "quest_failed_end_haunted")
    ),

    GuardianQuestLines(
        id="camp_outside_ruins",
        title="Đêm Kinh Hoàng",
        description="Bạn và {guardian.ga_name} cắm trại bên ngoài tàn tích. Suốt đêm, tiếng thì thầm dày vò tâm trí bạn, mang đến những cơn ác mộng sống động. {guardian.ga_name} cũng tỏ ra bồn chồn. 'Nơi này không cho phép ai yên ổn, Ngài.'",
        choice_a="Cảm thấy kiệt sức, nhiệm vụ gặp trở ngại.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-25, silver=-50, ga_exp=-25, ga_health=-10, ga_stamina=-10,
        next_steps=NextSteps("journey_to_ruins", "journey_to_ruins", "journey_to_ruins", "journey_to_ruins")
    ),

    GuardianQuestLines(
        id="destroy_amulet_outcome",
        title="Phá Hủy Lầm Lỗi",
        description="Bạn quyết định phá hủy bùa hộ mệnh. Ngay lập tức, tiếng thì thầm trở nên to hơn, và một cảm giác lạnh lẽo bao trùm lấy bạn. {guardian.ga_name} cau mày. 'Ta không nghĩ đây là một quyết định khôn ngoan, Ngài. Chúng ta đã mất đi một công cụ hữu ích.'",
        choice_a="Bạn mất đi một vật phẩm quan trọng, nhiệm vụ trở nên khó khăn hơn.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-25, silver=-75, ga_exp=-25, dignity_point=-10,
        next_steps=NextSteps("search_artifacts", "search_artifacts", "search_artifacts", "search_artifacts")
    ),

    GuardianQuestLines(
        id="whispers_overwhelm",
        title="Tiếng Thì Thầm Áp Đảo",
        description="Bạn chần chừ quá lâu trong tàn tích. Tiếng thì thầm trở nên chói tai, xâm nhập sâu vào tâm trí bạn, gây ra sự hoang tưởng và ảo giác. {guardian.ga_name} cố gắng kéo bạn ra, nhưng cả hai đều bị mắc kẹt trong cơn hỗn loạn. 'Ý chí Ngài đang bị bào mòn!' {guardian.ga_name} gầm lên.",
        choice_a="Bạn và {guardian.ga_name} bị áp đảo bởi tiếng thì thầm.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-175, silver=-375, ga_exp=-175, dignity_point=-35, ga_health=-125, ga_mana=-125, ga_stamina=-125,
        next_steps=NextSteps("quest_failed_end_haunted", "quest_failed_end_haunted", "quest_failed_end_haunted", "quest_failed_end_haunted")
    ),

    GuardianQuestLines(
        id="seek_safe_exit_ruins",
        title="Lối Thoát Bế Tắc",
        description="Bạn và {guardian.ga_name} cố gắng tìm lối thoát. Nhưng mọi con đường dường như dẫn trở lại trung tâm của tàn tích. Những bức tường như đang di chuyển, đóng sập lại sau lưng bạn. 'Chúng ta đã bị mắc kẹt, Ngài!' {guardian.ga_name} nói với vẻ tuyệt vọng.",
        choice_a="Bạn bị mắc kẹt trong tàn tích. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-150, silver=-300, ga_exp=-150, dignity_point=-30, ga_health=-75, ga_mana=-75, ga_stamina=-75,
        next_steps=NextSteps("quest_failed_end_haunted", "quest_failed_end_haunted", "quest_failed_end_haunted", "quest_failed_end_haunted")
    ),

    GuardianQuestLines(
        id="destroy_whisper_source",
        title="Phá Hủy Nguồn Gốc",
        description="Bạn và {guardian.ga_name} tấn công nguồn phát ra tiếng thì thầm. Một luồng năng lượng đen tối bùng nổ, đẩy bạn lùi lại và gây ra thiệt hại đáng kể. Nguồn gốc chỉ rung chuyển, không bị phá hủy hoàn toàn. {guardian.ga_name} thở hổn hển. 'Nó quá mạnh, Ngài! Chúng ta cần một kế hoạch khác.'",
        choice_a="Bạn và {guardian.ga_name} bị thương, nhiệm vụ gặp trở ngại.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-100, silver=-200, ga_exp=-100, dignity_point=-25, ga_health=-40, ga_mana=-40, ga_stamina=-40,
        next_steps=NextSteps("pursue_whispers", "pursue_whispers", "pursue_whispers", "pursue_whispers")
    ),

    GuardianQuestLines(
        id="seal_whisper_room",
        title="Nghi Lễ Phong Tỏa Khẩn Cấp",
        description="Bạn và {guardian.ga_name} cố gắng phong tỏa căn phòng dội âm. {guardian.ga_name} dùng sức mạnh của hắn để tạo ra một kết giới tạm thời, nhưng tiếng thì thầm vẫn lọt qua, yếu ớt hơn. 'Không đủ để ngăn chặn nó hoàn toàn, Ngài,' {guardian.ga_name} nói, vẻ mặt mệt mỏi.",
        choice_a="Bạn và {guardian.ga_name} bị kiệt sức, chỉ có thể phong tỏa tạm thời.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-50, silver=-125, ga_exp=-50, ga_mana=-30, ga_stamina=-30,
        next_steps=NextSteps("enter_ruins", "enter_ruins", "enter_ruins", "enter_ruins")
    ),

    GuardianQuestLines(
        id="find_whisper_weakness",
        title="Điểm Yếu Bị Lãng Quên",
        description="Bạn và {guardian.ga_name} tìm thấy một cuộn giấy ghi lại điểm yếu của Kẻ Thì Thầm: ánh sáng tinh khiết và sự thật không lay chuyển. {guardian.ga_name} nhìn bạn. 'Chúng ta có thể sử dụng điều này, Ngài!'",
        choice_a="Tìm cách tạo ra ánh sáng tinh khiết mạnh mẽ.",
        choice_b="Cố gắng đối mặt Kẻ Thì Thầm bằng sự thật.",
        choice_c="",
        choice_timeout="{guardian.ga_name} thúc giục. 'Thời gian không còn nhiều!'",
        next_steps=NextSteps(
            choice_a="create_pure_light",
            choice_b="confront_whisper_truth",
            choice_c="",
            timeout="whispers_overwhelm"
        )
    ),

    GuardianQuestLines(
        id="create_pure_light",
        title="Ánh Sáng Yếu Ớt",
        description="Bạn và {guardian.ga_name} cố gắng tạo ra ánh sáng tinh khiết. {guardian.ga_name} dồn năng lượng của mình, nhưng nó không đủ để xuyên qua bóng tối của Kẻ Thì Thầm. 'Ta cần thêm sức mạnh, Ngài,' {guardian.ga_name} thở hổn hển.",
        choice_a="Bạn và {guardian.ga_name} kiệt sức, ánh sáng không đủ mạnh.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-75, silver=-150, ga_exp=-75, ga_mana=-40, ga_stamina=-40,
        next_steps=NextSteps("find_research_rooms", "find_research_rooms", "find_research_rooms", "find_research_rooms")
    ),

    GuardianQuestLines(
        id="confront_whisper_truth",
        title="Sự Thật Đắng Cay",
        description="Bạn đối mặt với Kẻ Thì Thầm bằng sự thật về bản chất của nó và sự hủy diệt nó đã gây ra. Nó gào lên trong đau đớn, nhưng không bị tiêu diệt. 'Lời nói không thể làm hại ta, Ngài! Chỉ có sức mạnh thực sự mới có thể!' {guardian.ga_name} nói, vẻ mặt nghiêm nghị. 'Nó đang mạnh lên, Ngài!'",
        choice_a="Bạn làm Kẻ Thì Thầm suy yếu nhưng không tiêu diệt được.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-50, silver=-100, ga_exp=-50, dignity_point=0,
        next_steps=NextSteps("pursue_whispers", "pursue_whispers", "pursue_whispers", "pursue_whispers")
    ),

    GuardianQuestLines(
        id="leave_with_scrolls",
        title="Rút Lui Với Tri Thức",
        description="Bạn và {guardian.ga_name} mang theo những cuộn giấy cổ và rời khỏi tàn tích. Tiếng thì thầm vẫn văng vẳng trong tai bạn một thời gian, nhưng dần lắng xuống. 'Chúng ta đã có được tri thức, Ngài, nhưng cái giá phải trả là sự bình yên của chính chúng ta,' {guardian.ga_name} nói.",
        choice_a="Bạn và {guardian.ga_name} thoát ra với tri thức, nhưng bị ám ảnh.",
        choice_b="", choice_c="", choice_timeout="",
        gold=200, silver=750, ga_exp=150, dignity_point=50, ga_mana=-20, ga_stamina=-20,
        next_steps=NextSteps("quest_success_haunted_by_knowledge", "quest_success_haunted_by_knowledge", "quest_success_haunted_by_knowledge", "quest_success_haunted_by_knowledge")
    ),

    GuardianQuestLines(
        id="seek_alternative_method",
        title="Tìm Kiếm Phương Pháp Khác",
        description="Bạn và {guardian.ga_name} cố gắng tìm một phương pháp phong ấn không cần hy sinh, nhưng mọi nỗ lực đều vô vọng. Kẻ Thì Thầm ngày càng mạnh hơn khi thời gian trôi qua. 'Ta e rằng không có con đường nào khác, Ngài,' {guardian.ga_name} thở dài.",
        choice_a="Không tìm thấy cách thay thế, nhiệm vụ bế tắc.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-100, silver=-200, ga_exp=-100, dignity_point=-25, ga_mana=-40, ga_stamina=-40,
        next_steps=NextSteps("learn_sealing_ritual", "learn_sealing_ritual", "learn_sealing_ritual", "learn_sealing_ritual")
    ),

    GuardianQuestLines(
        id="use_amulet_deflect",
        title="Lá Chắn Linh Hồn",
        description="Bạn sử dụng bùa hộ mệnh. Nó phát ra một luồng sáng ấm áp, đẩy lùi tiếng thì thầm và khiến bạn cảm thấy an toàn hơn. {guardian.ga_name} gật đầu. 'Thứ này rất hữu ích, Ngài. Nó làm suy yếu ảnh hưởng của Kẻ Thì Thầm.'",
        choice_a="Bùa hộ mệnh giúp bạn chống lại tiếng thì thầm.",
        choice_b="", choice_c="", choice_timeout="",
        gold=50, silver=100, ga_exp=30, dignity_point=10, ga_mana=10, ga_stamina=10,
        next_steps=NextSteps("enter_ruins", "enter_ruins", "enter_ruins", "enter_ruins")
    ),

    GuardianQuestLines(
        id="keep_amulet_explore",
        title="Giữ Lại Hy Vọng",
        description="Bạn giữ lại bùa hộ mệnh và tiếp tục khám phá. Nó thỉnh thoảng phát sáng yếu ớt, như một lời nhắc nhở về sự hiện diện của Kẻ Thì Thầm. {guardian.ga_name} nói. 'Đó là một tia hy vọng nhỏ, Ngài.'",
        choice_a="Bạn vẫn giữ bùa hộ mệnh và tiếp tục hành trình.",
        choice_b="", choice_c="", choice_timeout="",
        gold=25, silver=75, ga_exp=15,
        next_steps=NextSteps("enter_ruins", "enter_ruins", "enter_ruins", "enter_ruins")
    ),

    GuardianQuestLines(
        id="abandon_ruins_quest",
        title="Thoát Ly Khỏi Nỗi Ám Ảnh",
        description="Bạn quyết định từ bỏ nhiệm vụ, cho rằng rủi ro quá lớn. {guardian.ga_name} không nói gì, nhưng bạn cảm nhận được sự thất vọng từ hắn. Vài năm sau, những tin đồn về Tàn Tích Thì Thầm ngày càng đáng sợ, về những linh hồn bị mắc kẹt và tiếng thì thầm điên loạn vang vọng khắp vùng đất. 'Ta hy vọng Ngài không bao giờ phải đối mặt với những gì chúng ta đã phớt lờ,' {guardian.ga_name} cuối cùng cũng lên tiếng.",
        choice_a="Bạn từ bỏ nhiệm vụ, nhưng nỗi sợ hãi vẫn còn đó.",
        choice_b="", choice_c="", choice_timeout="",
        gold=0, silver=0, ga_exp=-175, dignity_point=-50,
        next_steps=NextSteps("quest_failed_end_5", "quest_failed_end_5", "quest_failed_end_5", "quest_failed_end_5")
    ),

    # Final Bad Endings
    GuardianQuestLines(
        id="quest_failed_end_possessed_whispers",
        title="Linh Hồn Bị Chiếm Đoạt",
        description="Linh hồn bạn bị Kẻ Thì Thầm hoàn toàn chiếm đoạt. Bạn trở thành một vật chứa rỗng tuếch, chỉ biết thì thầm những bí mật và lời nguyền rủa của nó, mãi mãi là một công cụ để nó lan rộng ảnh hưởng. {guardian.ga_name} gào thét trong tuyệt vọng khi nhìn thấy bạn biến thành thứ đó, hắn cố gắng chiến đấu, nhưng bị hàng ngàn giọng nói vô hình áp đảo. Cuối cùng, {guardian.ga_name} cũng gục ngã, linh hồn hắn bị xé toạc bởi Kẻ Thì Thầm, cả hai trở thành một phần của nỗi kinh hoàng vĩnh cửu trong Tàn Tích Thì Thầm. Tiếng thì thầm của Kẻ Thì Thầm vang vọng khắp thế giới, mang theo tiếng cười điên dại của bạn và nỗi đau khổ của {guardian.ga_name}, mãi mãi... ",
        choice_a="Bạn và {guardian.ga_name} bị chiếm đoạt và hủy diệt hoàn toàn.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-2000, silver=-2000, ga_exp=-750, dignity_point=-150, ga_health=-999, ga_mana=-999, ga_stamina=-999, force_dead=True,
        next_steps=NextSteps("continue_adventure_5", "continue_adventure_5", "continue_adventure_5", "continue_adventure_5")
    ),

    GuardianQuestLines(
        id="quest_failed_end_guardian_sacrifice",
        title="Hy Sinh Cô Độc",
        description="{guardian.ga_name} đã hy sinh chính mình để phong ấn Kẻ Thì Thầm, cứu bạn và thế giới. Tàn tích chìm vào im lặng, nhưng bạn vẫn nghe thấy giọng nói cuối cùng của hắn vang vọng trong tâm trí. Nỗi đau mất mát quá lớn, khiến bạn suy sụp. Bạn đã chiến thắng, nhưng chiến thắng này quá đắt giá, vì nó phải đánh đổi bằng sự tồn tại của người bạn đồng hành trung thành nhất. Bạn tiếp tục hành trình, nhưng mỗi bước đi đều nặng trĩu nỗi đau, và thế giới dường như mất đi màu sắc tươi sáng khi không có {guardian.ga_name} bên cạnh. Bạn sẽ mãi mãi sống trong nỗi ân hận và tiếc nuối, mang theo gánh nặng của sự hy sinh đó, không bao giờ thực sự được giải thoát khỏi bóng ma của quá khứ.",
        choice_a="Kẻ Thì Thầm bị phong ấn, nhưng {guardian.ga_name} đã hy sinh.",
        choice_b="", choice_c="", choice_timeout="",
        gold=500, silver=1500, ga_exp=200, dignity_point=300, ga_health=-100, ga_mana=-100, ga_stamina=-100,
        next_steps=NextSteps("continue_adventure_5", "continue_adventure_5", "continue_adventure_5", "continue_adventure_5")
    ),

    GuardianQuestLines(
        id="quest_failed_end_haunted",
        title="Ám Ảnh Vĩnh Viễn",
        description="Bạn và {guardian.ga_name} đã thoát khỏi Tàn Tích Thì Thầm, nhưng tiếng thì thầm của Kẻ Thì Thầm đã ám ảnh cả hai mãi mãi. Những giọng nói vang vọng trong tâm trí bạn mỗi đêm, phá hoại giấc ngủ và sự tỉnh táo. {guardian.ga_name} cũng bị ảnh hưởng, hắn trở nên cáu kỉnh và khó chịu, luôn trong trạng thái cảnh giác, không bao giờ tìm thấy sự bình yên. Mặc dù sống sót, cả hai bạn đều mang theo một gánh nặng vô hình, một phần linh hồn bị tổn thương không bao giờ có thể chữa lành. Bạn và {guardian.ga_name} sống phần đời còn lại trong sự dày vò của những tiếng thì thầm, không bao giờ thực sự thoát khỏi Tàn Tích.",
        choice_a="Bạn và {guardian.ga_name} sống sót nhưng bị ám ảnh vĩnh viễn.",
        choice_b="", choice_c="", choice_timeout="",
        gold=125, silver=300, ga_exp=-250, dignity_point=-75, ga_health=-125, ga_mana=-125, ga_stamina=-125,
        next_steps=NextSteps("continue_adventure_5", "continue_adventure_5", "continue_adventure_5", "continue_adventure_5")
    ),

    GuardianQuestLines(
        id="quest_failed_end_5",
        title="Thất Bại Đắng Cay",
        description="Nhiệm vụ thất bại. Tàn Tích Thì Thầm vẫn là một mối đe dọa, và Kẻ Thì Thầm vẫn tiếp tục lan truyền ảnh hưởng của nó. {guardian.ga_name} nhìn bạn với ánh mắt thất vọng. 'Ta hy vọng Ngài sẽ rút ra được bài học từ thất bại này.'",
        choice_a="Rút ra bài học đau đớn.",
        choice_b="", choice_c="", choice_timeout="",
        gold=-75, silver=-175, ga_exp=-75, dignity_point=-10,
        next_steps=NextSteps("continue_adventure_5", "continue_adventure_5", "continue_adventure_5", "continue_adventure_5")
    ),

    GuardianQuestLines(
        id="quest_success_haunted_by_knowledge",
        title="Chiến Thắng Nặng Nề",
        description="Bạn và {guardian.ga_name} đã thoát khỏi Tàn Tích Thì Thầm với những cuộn giấy cổ chứa đựng kiến thức quý giá về Kẻ Thì Thầm và các nghi lễ cổ đại. Tiếng thì thầm vẫn đôi khi vang vọng trong tâm trí bạn, một lời nhắc nhở về những gì bạn đã trải qua. {guardian.ga_name} vẫn cảnh giác, nhưng hắn tự hào về bạn. 'Tri thức này sẽ giúp chúng ta đối phó với những mối đe dọa tương tự trong tương lai, Ngài,' hắn nói. Bạn đã đạt được một chiến thắng quan trọng, nhưng cái giá là sự ám ảnh không ngừng và một phần ký ức vĩnh viễn bị giằng xé bởi những tiếng thì thầm của quá khứ. Tuy nhiên, với tri thức này, bạn và {guardian.ga_name} đã trở nên mạnh mẽ hơn, sẵn sàng đối mặt với bất kỳ hiểm nguy nào sắp tới, dù cho nỗi ám ảnh vẫn luôn tồn tại.",
        choice_a="Bạn và {guardian.ga_name} thoát ra với tri thức quan trọng.",
        choice_b="", choice_c="", choice_timeout="",
        gold=375, silver=900, ga_exp=225, dignity_point=75, ga_mana=25, ga_stamina=25,
        next_steps=NextSteps("continue_adventure_5", "continue_adventure_5", "continue_adventure_5", "continue_adventure_5")
    ),

    GuardianQuestLines(
        id="continue_adventure_5",
        title="Hành Trình Tiếp Nối",
        description="Bạn và {guardian.ga_name} rời khỏi Tàn Tích Thì Thầm, mang theo những bài học và nỗi ám ảnh. Những cuộc phiêu lưu mới đang chờ đợi...",
        choice_a="",
        choice_b="", choice_c="", choice_timeout="",
        gold=50, silver=200, ga_exp=40,
        next_steps=NextSteps("", "", "", "")
    )
]

#region quest_dying_whisper
quest_dying_whisper = [
        GuardianQuestLines(
        id="start",
        title="Lời Nguyền Của Hòn Đảo Quên Lãng",
        description="Một lời nguyền cổ xưa bao trùm Hòn Đảo Quên Lãng, khiến mọi ký ức về nó dần phai nhạt khỏi tâm trí mọi người. {guardian.ga_name} nhìn bạn với vẻ lo lắng. 'Ta cảm nhận được sự lãng quên đang bao trùm. Một sự bất công đang xảy ra.'",
        choice_a="Du hành đến Hòn Đảo Quên Lãng.",
        choice_b="Tìm kiếm những ghi chép cổ về lời nguyền.",
        choice_c="Bỏ qua, cho rằng đó chỉ là một truyền thuyết.",
        choice_timeout="{guardian.ga_name} nói với giọng khẩn thiết. 'Nếu chúng ta không hành động, Hòn Đảo sẽ biến mất mãi mãi, Ngài!'",
        next_steps=NextSteps(
            choice_a="journey_to_forgotten_isle",
            choice_b="research_ancient_curse",
            choice_c="ignore_curse_outcome",
            timeout="ga_urgent_timeout_curse_1"
        ),
        gold=60, silver=280, ga_exp=45, dignity_point=25
    ),

    GuardianQuestLines(
        id="journey_to_forgotten_isle",
        title="Bước Chân Lên Hòn Đảo Lãng Quên",
        description="Bạn và {guardian.ga_name} đặt chân lên Hòn Đảo Quên Lãng. Không khí tĩnh lặng đến rợn người, cây cối mục nát và những công trình đổ nát gợi lên một quá khứ huy hoàng bị lãng quên. {guardian.ga_name} chỉ vào một tượng đài hình chiếc chìa khóa khổng lồ. 'Đây là cổng dẫn đến ký ức, nhưng nó đã bị khóa chặt bởi lời nguyền.'",
        choice_a="Kiểm tra tượng đài chìa khóa.",
        choice_b="Tìm kiếm những người còn sót lại trên đảo.",
        choice_c="Tìm kiếm một lối thoát khỏi hòn đảo.",
        choice_timeout="{guardian.ga_name} thúc giục. 'Chúng ta phải tìm hiểu điều gì đã xảy ra ở đây!'",
        next_steps=NextSteps(
            choice_a="examine_key_monument",
            choice_b="search_for_survivors",
            choice_c="seek_escape_from_isle",
            timeout="monument_fades_timeout"
        )
    ),

    GuardianQuestLines(
        id="research_ancient_curse",
        title="Giải Mã Lời Nguyền Quên Lãng",
        description="Bạn và {guardian.ga_name} đến một kho lưu trữ kiến thức cổ xưa. Một cuộn giấy da cũ kỹ hé lộ về lời nguyền được tạo ra bởi một pháp sư hùng mạnh nhằm bảo vệ một bí mật. Bất cứ ai cố gắng khám phá bí mật sẽ bị lời nguyền cuốn đi, và hòn đảo sẽ dần bị lãng quên.",
        choice_a="Tìm kiếm hậu duệ của pháp sư tạo ra lời nguyền.",
        choice_b="Trở lại Hòn Đảo Quên Lãng, tìm hiểu tại chỗ.",
        choice_c="Rời bỏ nhiệm vụ, cho rằng lời nguyền quá nguy hiểm.",
        choice_timeout="{guardian.ga_name} nói. 'Chúng ta cần tìm hiểu ý định thực sự của pháp sư này, Ngài.'",
        next_steps=NextSteps(
            choice_a="find_curse_creator_descendant",
            choice_b="journey_to_forgotten_isle",
            choice_c="abandon_curse_quest",
            timeout="ga_urgent_timeout_curse_1"
        ),
        gold=85, silver=320, ga_exp=65, dignity_point=35
    ),

    GuardianQuestLines(
        id="examine_key_monument",
        title="Bí Ẩn Đằng Sau Chiếc Chìa Khóa",
        description="Bạn và {guardian.ga_name} kiểm tra tượng đài chìa khóa. Một dòng chữ ẩn hiện: 'Ký ức là chìa khóa, quên lãng là xiềng xích.' {guardian.ga_name} cau mày. 'Lời nguyền này không chỉ xóa đi ký ức, mà còn giam giữ chúng.'",
        choice_a="Tìm kiếm những mảnh ký ức bị lãng quên.",
        choice_b="Thử giải mã dòng chữ bằng phép thuật.",
        choice_c="Bỏ qua, tìm kiếm nơi khác trên đảo.",
        choice_timeout="Tượng đài bắt đầu mờ dần. 'Chúng ta không còn nhiều thời gian trước khi nó biến mất hoàn toàn!' {guardian.ga_name} cảnh báo.",
        next_steps=NextSteps(
            choice_a="seek_forgotten_memories",
            choice_b="attempt_magic_decipher",
            choice_c="abandon_monument_isle",
            timeout="monument_fades_timeout"
        )
    ),

    GuardianQuestLines(
        id="find_curse_creator_descendant",
        title="Truy Tìm Hậu Duệ Pháp Sư",
        description="Dựa trên thông tin, bạn và {guardian.ga_name} tìm đến một thung lũng ẩn. Bạn gặp một học giả ẩn dật tên là Lyra, hậu duệ của pháp sư tạo ra lời nguyền. Bà ấy sống trong sự cô lập, bị ám ảnh bởi lỗi lầm của tổ tiên. 'Cha tôi đã tạo ra lời nguyền để bảo vệ một bí mật, nhưng ông ấy đã đi quá xa,' Lyra nói, giọng run run.",
        choice_a="Tìm hiểu về bí mật mà lời nguyền bảo vệ.",
        choice_b="Thuyết phục Lyra giúp phá giải lời nguyền.",
        choice_c="Buộc Lyra phải tiết lộ bí mật.",
        choice_timeout="{guardian.ga_name} nói nhỏ. 'Hãy cẩn thận, Ngài. Bà ấy đang mang gánh nặng của quá khứ.'",
        next_steps=NextSteps(
            choice_a="learn_secret_curse_protects",
            choice_b="persuade_lyra_to_help",
            choice_c="force_lyra_reveal_secret",
            timeout="lyra_despair_timeout"
        ),
        gold=90, silver=350, ga_exp=70, dignity_point=40
    ),

    GuardianQuestLines(
        id="seek_forgotten_memories",
        title="Mảnh Ghép Ký Ức",
        description="Bạn và {guardian.ga_name} tìm kiếm khắp hòn đảo, thu thập những mảnh ký ức mờ nhạt từ những vật phẩm còn sót lại: một bức thư tình ố vàng, một món đồ chơi trẻ con bị bỏ quên, một cuốn nhật ký cháy dở. {guardian.ga_name} cảm nhận được sự đau khổ. 'Những ký ức này... chúng đang đấu tranh để tồn tại.'",
        choice_a="Ghép nối các mảnh ký ức.",
        choice_b="Sử dụng phép thuật để phục hồi ký ức.",
        choice_c="Bỏ qua, cho rằng những ký ức này không quan trọng.",
        choice_timeout="{guardian.ga_name} cau mày. 'Chúng ta cần nhanh chóng, Ngài. Ký ức đang biến mất!'",
        next_steps=NextSteps(
            choice_a="piece_together_memories",
            choice_b="magic_restore_memories",
            choice_c="ignore_memories",
            timeout="memories_fade_completely_timeout"
        )
    ),

    GuardianQuestLines(
        id="piece_together_memories",
        title="Bức Tranh Quá Khứ",
        description="Bạn và {guardian.ga_name} đã ghép nối các mảnh ký ức. Chúng vẽ nên một bức tranh về một nền văn minh thịnh vượng, được bảo vệ bởi một tinh thể quyền năng. Nhưng sự đố kỵ và tham lam đã khiến tinh thể bị lạm dụng, dẫn đến một cuộc chiến tranh tàn khốc và lời nguyền quên lãng được tạo ra để chôn vùi sự thật. {guardian.ga_name} nói: 'Thảm kịch này cần được phơi bày.'",
        choice_a="Tìm cách giải phóng tinh thể.",
        choice_b="Tìm Lyra để chia sẻ câu chuyện.",
        choice_c="Thử tìm kiếm dấu vết của tinh thể.",
        choice_timeout="Bức tranh ký ức bắt đầu tan biến. 'Thời gian không chờ đợi, Ngài!' {guardian.ga_name} thúc giục.",
        next_steps=NextSteps(
            choice_a="free_crystal",
            choice_b="share_story_with_lyra",
            choice_c="seek_crystal_traces",
            timeout="memories_fade_completely_timeout"
        ),
        gold=150, silver=700, ga_exp=120, dignity_point=70
    ),

    GuardianQuestLines(
        id="learn_secret_curse_protects",
        title="Bí Mật Bị Chôn Vùi",
        description="Lyra miễn cưỡng kể về bí mật: Lời nguyền bảo vệ một Tinh Thể Ký Ức, nơi chứa đựng lịch sử và kiến thức của toàn bộ nền văn minh trên Hòn Đảo Quên Lãng. Cha của Lyra, pháp sư, đã tạo ra lời nguyền để ngăn chặn việc lạm dụng tinh thể sau khi một cuộc chiến tranh tàn khốc gần như hủy diệt hòn đảo. 'Ông ấy sợ rằng con người sẽ lặp lại sai lầm,' Lyra nói, giọng đầy chua xót. {guardian.ga_name} nói: 'Vậy ra lời nguyền là một sự bảo vệ... nhưng nó đã trở thành một xiềng xích.'",
        choice_a="Tìm cách giải phóng tinh thể một cách an toàn.",
        choice_b="Thuyết phục Lyra cùng phá giải lời nguyền.",
        choice_c="Để Lyra tự mình giải quyết.",
        choice_timeout="{guardian.ga_name} thúc giục. 'Chúng ta cần tìm một cách để giải phóng tinh thể, Ngài.'",
        next_steps=NextSteps(
            choice_a="release_crystal_safely",
            choice_b="convince_lyra_to_join",
            choice_c="leave_lyra_to_her_fate",
            timeout="lyra_despair_timeout"
        ),
        gold=100, silver=400, ga_exp=80, dignity_point=45
    ),

    GuardianQuestLines(
        id="release_crystal_safely",
        title="Giải Phóng Tinh Thể Hồi Ức",
        description="Bạn và {guardian.ga_name} cùng Lyra đến vị trí của Tinh Thể Ký Ức, nằm sâu dưới lòng đất. Với sự hướng dẫn của Lyra và sức mạnh của {guardian.ga_name}, bạn thực hiện nghi lễ giải phóng tinh thể. Một luồng ánh sáng rực rỡ bùng lên, lan tỏa khắp Hòn Đảo Quên Lãng. Ký ức ùa về như thác lũ, những công trình đổ nát dần được phục hồi, và những con người từng bị lãng quên giờ đây hồi sinh trong tâm trí mọi người. Lyra mỉm cười, nước mắt chảy dài. 'Cuối cùng... hòn đảo đã được nhớ lại.' {guardian.ga_name} đặt tay lên vai bạn. 'Ngài đã mang lại sự thật và sự sống cho một nơi tưởng chừng đã mất, Ngài.'",
        choice_a="Hòn đảo hồi sinh, ký ức trở lại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_success_forgotten_isle", "quest_success_forgotten_isle", "quest_success_forgotten_isle", "quest_success_forgotten_isle"),
        gold=1500, silver=7500, ga_exp=750, dignity_point=350
    ),

    GuardianQuestLines(
        id="quest_success_forgotten_isle",
        title="Khúc Ca Ký Ức Vang Mãi",
        description="Hòn Đảo Quên Lãng giờ đây được biết đến là Hòn Đảo Ký Ức, một ngọn hải đăng của sự thật và sự tha thứ. Tinh Thể Ký Ức tỏa sáng rực rỡ, kể lại câu chuyện về quá khứ để không ai phải lặp lại sai lầm. Lyra trở thành người bảo vệ tinh thể, chia sẻ kiến thức của nó với thế giới. {guardian.ga_name} nhìn bạn với ánh mắt tự hào. 'Hành trình của chúng ta đã thay đổi số phận của cả một vùng đất. Ngài đã cho thấy rằng ngay cả những điều bị lãng quên nhất cũng có thể tìm thấy con đường trở về.' Hòn đảo nay trở thành một điểm đến cho những ai tìm kiếm sự thật và nguồn cảm hứng, và câu chuyện về hành trình của bạn cùng {guardian.ga_name} được lưu truyền qua nhiều thế hệ.",
        choice_a="Câu chuyện về Hòn Đảo Ký Ức sẽ được ghi nhớ mãi mãi.",
        choice_b="", choice_c="", choice_timeout="",
        gold=2000, silver=10000, ga_exp=1000, dignity_point=500
    ),

    GuardianQuestLines(
        id="ignore_curse_outcome",
        title="Thờ Ơ Với Lãng Quên",
        description="Bạn và {guardian.ga_name} quyết định phớt lờ lời nguyền. Dần dần, những ký ức cuối cùng về Hòn Đảo Quên Lãng biến mất khỏi tâm trí mọi người, như thể nó chưa từng tồn tại. {guardian.ga_name} nhìn bạn đầy thất vọng. 'Ngài đã cho phép một phần lịch sử bị xóa sổ.'",
        choice_a="Bạn cảm thấy một sự hối tiếc lạnh lẽo. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-60, ga_exp=-250, silver=-600, gold=-300,
        next_steps=NextSteps("quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2")
    ),

    GuardianQuestLines(
        id="ga_urgent_timeout_curse_1",
        title="Sự Mờ Nhạt Của Thời Gian",
        description="Bạn chần chừ quá lâu. {guardian.ga_name} thở dài. 'Thời gian không chờ đợi. Hòn đảo đã chìm sâu hơn vào quên lãng.' Nhiệm vụ kết thúc trong sự thất bại đau đớn.",
        choice_a="Bạn cảm thấy bất lực. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2"),
        dignity_point=-40, ga_exp=-180, silver=-300, gold=-150,
    ),

    GuardianQuestLines(
        id="monument_fades_timeout",
        title="Tượng Đài Tan Biến",
        description="Bạn chần chừ quá lâu trong việc kiểm tra tượng đài. Những nét khắc mờ dần, và nó biến mất hoàn toàn, mang theo mọi manh mối. 'Đã quá muộn rồi,' {guardian.ga_name} nói với giọng buồn bã.",
        choice_a="Bạn cảm thấy một sự mất mát. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-25, ga_exp=-140, silver=-220, gold=-110,
        next_steps=NextSteps("quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2")
    ),

    GuardianQuestLines(
        id="seek_escape_from_isle",
        title="Lối Thoát Tuyệt Vọng",
        description="Bạn và {guardian.ga_name} quyết định tìm một lối thoát khỏi Hòn Đảo Quên Lãng. Nhưng càng đi, bạn càng cảm thấy mọi thứ xung quanh mình trở nên mơ hồ, như thể hòn đảo đang cố gắng xóa đi sự hiện diện của bạn. 'Lời nguyền quá mạnh,' {guardian.ga_name} nói, giọng yếu ớt.",
        choice_a="Bạn bị mắc kẹt trên đảo, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-35, ga_exp=-160, silver=-180, gold=-120,
        next_steps=NextSteps("quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2")
    ),

    GuardianQuestLines(
        id="lyra_despair_timeout",
        title="Nỗi Ám Ảnh Của Lyra",
        description="Bạn chần chừ quá lâu trong việc nói chuyện với Lyra. Bà ấy chìm sâu hơn vào nỗi ám ảnh về lỗi lầm của tổ tiên. 'Tôi không thể... gánh nặng này quá lớn,' bà thì thào. {guardian.ga_name} nhìn bạn với ánh mắt đầy trách móc. 'Chúng ta đã không thể mang lại hy vọng cho bà ấy.'",
        choice_a="Lyra chìm trong tuyệt vọng, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-35, ga_exp=-160, silver=-280, gold=-140,
        next_steps=NextSteps("quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2")
    ),

    GuardianQuestLines(
        id="force_lyra_reveal_secret",
        title="Cưỡng Ép Sự Thật",
        description="Bạn cố gắng buộc Lyra phải tiết lộ bí mật. Bà ấy phản kháng dữ dội, nỗi sợ hãi và tức giận bùng phát, tạo ra một làn sóng năng lượng tiêu cực khiến lời nguyền trên hòn đảo càng mạnh hơn. 'Ngài đã đẩy bà ấy vào nguy hiểm,' {guardian.ga_name} nói, ánh mắt đầy thất vọng.",
        choice_a="Lời nguyền trở nên mạnh hơn. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-80, ga_exp=-280, silver=-550, gold=-270, ga_health=-130, ga_mana=-130, ga_stamina=-130,
        next_steps=NextSteps("quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2")
    ),

    GuardianQuestLines(
        id="memories_fade_completely_timeout",
        title="Ký Ức Tan Biến Hoàn Toàn",
        description="Bạn chần chừ quá lâu, và những mảnh ký ức cuối cùng cũng tan biến, không còn sót lại bất kỳ dấu vết nào. 'Mọi thứ đã bị lãng quên mãi mãi,' {guardian.ga_name} nói với vẻ thất thần.",
        choice_a="Ký ức tan biến, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-20, ga_exp=-80, silver=-160, gold=-80,
        next_steps=NextSteps("quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2")
    ),

    GuardianQuestLines(
        id="search_for_survivors",
        title="Tìm Kiếm Bóng Người",
        description="Bạn và {guardian.ga_name} tìm kiếm những người còn sót lại trên Hòn Đảo Quên Lãng. Bạn chỉ tìm thấy những hình bóng mờ ảo, lang thang vô định, không có ký ức về bản thân hay hòn đảo. {guardian.ga_name} nói: 'Họ đã bị lời nguyền chiếm đoạt hoàn toàn.'",
        choice_a="Cố gắng giao tiếp với những linh hồn này.",
        choice_b="Tìm kiếm một nơi trú ẩn cho họ.",
        choice_c="Rút lui, cho rằng họ đã mất.",
        choice_timeout="{guardian.ga_name} hối thúc. 'Chúng ta cần tìm cách giúp họ thoát khỏi lời nguyền!'",
        next_steps=NextSteps(
            choice_a="communicate_with_spirits",
            choice_b="seek_shelter_for_them",
            choice_c="abandon_lost_souls",
            timeout="spirits_fade_timeout"
        )
    ),

    GuardianQuestLines(
        id="communicate_with_spirits",
        title="Lời Thì Thầm Của Linh Hồn",
        description="Bạn cố gắng giao tiếp với những linh hồn mờ ảo. Họ thì thầm những câu chuyện rời rạc về một quá khứ xa xăm, về một tinh thể lấp lánh và sự đổ vỡ. {guardian.ga_name} lắng nghe chăm chú. 'Những ký ức bị giam cầm... Chúng ta cần giải thoát chúng.'",
        choice_a="Cố gắng giúp các linh hồn tìm lại ký ức.",
        choice_b="Tìm cách kết nối các mảnh ký ức của họ.",
        choice_c="Rút lui khi cảm thấy quá sức.",
        choice_timeout="{guardian.ga_name} cảnh báo. 'Họ đang mờ dần, Ngài!'",
        next_steps=NextSteps(
            choice_a="help_spirits_regain_memories",
            choice_b="connect_spirit_memory_fragments",
            choice_c="retreat_from_spirits",
            timeout="spirits_fade_timeout"
        ),
        gold=70, silver=250, ga_exp=50, dignity_point=20
    ),

    GuardianQuestLines(
        id="help_spirits_regain_memories",
        title="Hồi Sinh Linh Hồn",
        description="Bạn và {guardian.ga_name} đã cùng nhau giúp các linh hồn tìm lại ký ức bằng cách chiếu sáng những mảnh ký ức bạn đã thu thập được. Dần dần, những hình bóng mờ ảo trở nên rõ ràng hơn, và họ bắt đầu nhớ lại mình là ai. Họ không thể rời khỏi hòn đảo, nhưng họ đã được giải thoát khỏi sự quên lãng. 'Cảm ơn Ngài,' một linh hồn thì thầm. {guardian.ga_name} nói: 'Họ đã tìm thấy bình yên, Ngài.'",
        choice_a="Các linh hồn được giải thoát, nhiệm vụ thành công một phần.",
        choice_b="", choice_c="", choice_timeout="",
        gold=550, silver=2200, ga_exp=280, dignity_point=120,
        next_steps=NextSteps("partial_success_spirits_at_peace", "partial_success_spirits_at_peace", "partial_success_spirits_at_peace", "partial_success_spirits_at_peace")
    ),

    GuardianQuestLines(
        id="partial_success_spirits_at_peace",
        title="Bình Yên Cho Linh Hồn",
        description="Hòn Đảo Quên Lãng vẫn bị bao trùm bởi lời nguyền, nhưng những linh hồn bị mắc kẹt giờ đây đã tìm thấy sự bình yên. Họ trở thành những người bảo vệ hòn đảo, giữ gìn những ký ức mà họ đã lấy lại được. {guardian.ga_name} nói: 'Ngài đã mang lại sự an ủi cho những linh hồn lạc lối. Đó là một chiến thắng đáng trân trọng, dù không hoàn toàn.'",
        choice_a="Nhiệm vụ thành công một phần, linh hồn được an ủi.",
        choice_b="", choice_c="", choice_timeout="",
        gold=700, silver=3000, ga_exp=350, dignity_point=150,
        next_steps=NextSteps("continue_adventure_2", "continue_adventure_2", "continue_adventure_2", "continue_adventure_2")
    ),

    GuardianQuestLines(
        id="attempt_magic_decipher",
        title="Giải Mã Thất Bại",
        description="Bạn cố gắng giải mã dòng chữ bằng phép thuật, nhưng nó quá phức tạp và cổ xưa. Năng lượng ma thuật phản tác dụng, khiến bạn choáng váng và tượng đài mờ đi nhanh hơn. 'Phép thuật không phải là câu trả lời cho mọi thứ,' {guardian.ga_name} nói, đỡ bạn dậy.",
        choice_a="Phép thuật thất bại, nhiệm vụ gặp trở ngại.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-15, ga_exp=-80, silver=-100, gold=-50, ga_mana=-50,
        next_steps=NextSteps("monument_fades_timeout", "monument_fades_timeout", "monument_fades_timeout", "monument_fades_timeout")
    ),

    GuardianQuestLines(
        id="abandon_monument_isle",
        title="Bỏ Qua Tượng Đài",
        description="Bạn và {guardian.ga_name} quyết định bỏ qua tượng đài, hy vọng tìm thấy manh mối ở nơi khác trên đảo. Tuy nhiên, mọi con đường đều dẫn đến sự trống rỗng và im lặng. 'Có lẽ chúng ta đã bỏ lỡ điều quan trọng nhất,' {guardian.ga_name} nói với vẻ hối tiếc.",
        choice_a="Bạn cảm thấy bế tắc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-25, ga_exp=-140, silver=-160, gold=-80,
        next_steps=NextSteps("quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2")
    ),

    GuardianQuestLines(
        id="persuade_lyra_to_help",
        title="Niềm Tin Được Thắp Sáng",
        description="Bạn cố gắng thuyết phục Lyra giúp phá giải lời nguyền. Ban đầu, bà ấy do dự, nhưng sau khi nghe bạn nói về sự đau khổ của hòn đảo, một tia hy vọng lóe lên trong mắt bà. 'Tôi sẽ giúp... vì tổ tiên tôi đã sai lầm.' {guardian.ga_name} nói: 'Ngài đã chạm đến trái tim bà ấy, Ngài.'",
        choice_a="Lyra đồng ý giúp đỡ.",
        choice_b="Tìm kiếm những công cụ cần thiết cho nghi lễ.",
        choice_c="",
        choice_timeout="{guardian.ga_name} thúc giục. 'Thời gian đang chống lại chúng ta, Ngài.'",
        next_steps=NextSteps(
            choice_a="lyra_joins_cause",
            choice_b="seek_ritual_tools",
            choice_c="",
            timeout="lyra_despair_timeout"
        ),
        dignity_point=50, ga_exp=100
    ),

    GuardianQuestLines(
        id="lyra_joins_cause",
        title="Liên Minh Vì Hòn Đảo",
        description="Lyra, với kiến thức sâu rộng về lời nguyền và lịch sử của tinh thể, đã trở thành một đồng minh vô giá. Cùng với Lyra và {guardian.ga_name}, bạn có một cơ hội thực sự để giải thoát Hòn Đảo Quên Lãng. 'Chúng ta hãy bắt đầu nghi lễ,' Lyra nói với quyết tâm.",
        choice_a="Thực hiện nghi lễ giải phóng tinh thể.",
        choice_b="Tìm hiểu thêm về tác dụng phụ của việc giải phóng tinh thể.",
        choice_c="",
        choice_timeout="{guardian.ga_name} nói. 'Đã đến lúc hành động, Ngài!'",
        next_steps=NextSteps(
            choice_a="release_crystal_safely",
            choice_b="learn_crystal_side_effects",
            choice_c="",
            timeout="lyra_despair_timeout"
        ),
        gold=120, silver=500, ga_exp=90, dignity_point=55
    ),

    GuardianQuestLines(
        id="ignore_memories",
        title="Bỏ Qua Ký Ức",
        description="Bạn và {guardian.ga_name} quyết định bỏ qua những mảnh ký ức, tin rằng chúng không phải là chìa khóa. Nhưng càng đi sâu vào hòn đảo, cảm giác trống rỗng càng lớn. 'Chúng ta đã bỏ lỡ điều gì đó quan trọng,' {guardian.ga_name} nói, giọng đầy tiếc nuối.",
        choice_a="Bạn cảm thấy hối tiếc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-10, ga_exp=-60, silver=-120, gold=-60,
        next_steps=NextSteps("memories_fade_completely_timeout", "memories_fade_completely_timeout", "memories_fade_completely_timeout", "memories_fade_completely_timeout")
    ),

    GuardianQuestLines(
        id="learn_crystal_side_effects",
        title="Mặt Trái Của Sự Hồi Sinh",
        description="Lyra cảnh báo rằng việc giải phóng tinh thể có thể mang lại những ký ức đau khổ và sự hỗn loạn ban đầu khi quá khứ ùa về. 'Sự thật có thể tàn khốc, nhưng nó cần được chấp nhận,' bà nói. {guardian.ga_name} nói: 'Chúng ta phải sẵn sàng đối mặt với mọi điều, Ngài.'",
        choice_a="Tiếp tục nghi lễ, chấp nhận rủi ro.",
        choice_b="Tìm cách giảm thiểu tác động tiêu cực.",
        choice_c="",
        choice_timeout="{guardian.ga_name} thúc giục. 'Không còn đường lui, Ngài!'",
        next_steps=NextSteps(
            choice_a="release_crystal_safely",
            choice_b="mitigate_negative_effects",
            choice_c="",
            timeout="lyra_despair_timeout"
        ),
        gold=50, silver=150, ga_exp=30, dignity_point=10
    ),

    GuardianQuestLines(
        id="mitigate_negative_effects",
        title="Lá Chắn Cảm Xúc",
        description="Bạn, {guardian.ga_name} và Lyra đã tạo ra một lá chắn cảm xúc để giảm thiểu tác động tiêu cực của dòng ký ức ùa về. Khi tinh thể được giải phóng, dù vẫn có sự hỗn loạn, nhưng nỗi đau không quá sức chịu đựng. 'Chúng ta đã làm giảm nhẹ gánh nặng,' {guardian.ga_name} nói, thở phào.",
        choice_a="Tiếp tục nghi lễ giải phóng tinh thể.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("release_crystal_safely", "release_crystal_safely", "release_crystal_safely", "release_crystal_safely"),
        gold=70, silver=200, ga_exp=40, dignity_point=15
    )
]

all_quests = [quest_ghost_of_forrest, quest_night_market, quest_the_ruin_call, quest_broken_oath, quest_ruin_whisper, quest_dying_whisper]