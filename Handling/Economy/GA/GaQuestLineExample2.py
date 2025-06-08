
from Handling.Economy.GA.GaQuestClass import GuardianQuestLines, NextSteps
#region quest_romance_letter
quest_romance_letter = [
    GuardianQuestLines(
        id="start",
        title="Lá Thư Tình Cũ Kỹ Từ Cố Nhân",
        description="Bạn nhận được một lá thư cũ kỹ, không ghi tên người gửi, nhưng giọng văn thân thuộc lạ lùng. Lá thư nói về một lời hứa bị bỏ quên và một bí mật đang ngủ yên ở Vùng Đất Lãng Quên. {guardian.ga_name} trầm ngâm. 'Có vẻ như một quá khứ đang gọi Ngài, chủ nhân.'",
        choice_a="Điều tra nguồn gốc lá thư.",
        choice_b="Hỏi {guardian.ga_name} về Vùng Đất Lãng Quên.",
        choice_c="Phớt lờ lá thư, có vẻ không an toàn.",
        choice_timeout="{guardian.ga_name} nhìn bạn đầy ẩn ý. 'Thời gian sẽ không chờ đợi những bí mật bị chôn vùi đâu, Ngài.'",
        next_steps=NextSteps(
            choice_a="investigate_letter",
            choice_b="ask_about_forgotten_lands",
            choice_c="ignore_letter_outcome",
            timeout="letter_timeout"
        ),
        gold=10, silver=100, ga_exp=10, dignity_point=5
    ),

    GuardianQuestLines(
        id="investigate_letter",
        title="Dấu Vết Của Ký Ức",
        description="Bạn và {guardian.ga_name} bắt đầu điều tra. Lá thư được viết bằng loại giấy hiếm, chỉ tìm thấy ở Thư Viện Cấm. Tại đó, một thủ thư già lẩm bẩm về 'những trái tim bị chia cắt bởi lời nguyền.' {guardian.ga_name} cảm thấy một sự liên kết kỳ lạ.",
        choice_a="Tìm kiếm thông tin về lời nguyền.",
        choice_b="Hỏi thủ thư về người gửi thư.",
        choice_c="Rời khỏi thư viện, cảm thấy bất an.",
        choice_timeout="{guardian.ga_name} thúc giục. 'Đừng để những lời nói của lão thủ thư làm Ngài phân tâm, Ngài.'",
        next_steps=NextSteps(
            choice_a="search_curse_info",
            choice_b="ask_about_sender",
            choice_c="leave_library_outcome",
            timeout="library_timeout"
        ),
        gold=15, silver=150, ga_exp=15, dignity_point=5
    ),

    GuardianQuestLines(
        id="ask_about_forgotten_lands",
        title="Lời Thì Thầm Của Vùng Đất Lãng Quên",
        description="{guardian.ga_name} kể về Vùng Đất Lãng Quên, một nơi bị thời gian lãng quên, nơi những lời nguyền cổ xưa vẫn còn tồn tại. 'Có những linh hồn bị mắc kẹt ở đó, bị chia cắt khỏi những gì họ yêu thương,' {guardian.ga_name} nói với ánh mắt u buồn. 'Ta tin rằng lá thư này có liên quan đến một trong số họ.'",
        choice_a="Tin tưởng {guardian.ga_name}, lên đường đến Vùng Đất Lãng Quên.",
        choice_b="Tìm thêm thông tin trước khi đi.",
        choice_c="Vẫn còn hoài nghi, từ chối tham gia.",
        choice_timeout="{guardian.ga_name} khẽ thở dài. 'Sự thật không thể tự tìm đến Ngài đâu, chủ nhân.'",
        next_steps=NextSteps(
            choice_a="journey_to_forgotten_lands",
            choice_b="investigate_letter",
            choice_c="refuse_quest_outcome",
            timeout="guardian_sad_timeout"
        ),
        gold=10, silver=100, ga_exp=10, dignity_point=5
    ),

    GuardianQuestLines(
        id="search_curse_info",
        title="Bí Mật Của Lời Nguyền Hắc Ám",
        description="Bạn và {guardian.ga_name} tìm thấy một cuốn sách cũ rích, nói về Lời Nguyền Trái Tim Tan Vỡ, một lời nguyền giam cầm linh hồn những người yêu nhau, chia cắt họ mãi mãi. Để hóa giải, cần 'Huyết Tâm Ngọc' và 'Khóa Ánh Trăng'. {guardian.ga_name} nhìn bạn, ánh mắt đầy quyết tâm.",
        choice_a="Tìm kiếm Huyết Tâm Ngọc.",
        choice_b="Tìm kiếm Khóa Ánh Trăng.",
        choice_c="Thử tìm một cách hóa giải khác.",
        choice_timeout="{guardian.ga_name} nói. 'Chúng ta không có nhiều thời gian để tìm kiếm đâu, Ngài!'",
        next_steps=NextSteps(
            choice_a="seek_blood_heart_gem",
            choice_b="seek_moonlight_key",
            choice_c="search_alternative_solution",
            timeout="search_curse_timeout"
        ),
        gold=20, silver=200, ga_exp=20, dignity_point=10
    ),

    GuardianQuestLines(
        id="ask_about_sender",
        title="Cái Tên Bị Lãng Quên",
        description="Thủ thư già kể rằng người gửi thư là một pháp sư cổ xưa tên là Lyra, người đã yêu một Guardian và bị Lời Nguyền Trái Tim Tan Vỡ chia cắt. Ông ta tin rằng Lyra vẫn còn sống, nhưng linh hồn cô ấy bị mắc kẹt. {guardian.ga_name} chợt tái mặt, một ký ức đau khổ thoáng qua trong mắt Ngài.",
        choice_a="Hỏi {guardian.ga_name} về Lyra.",
        choice_b="Tìm kiếm dấu vết của pháp sư Lyra.",
        choice_c="Không tin thủ thư, bỏ qua câu chuyện.",
        choice_timeout="{guardian.ga_name} nắm chặt tay bạn. 'Có gì đó không ổn, chủ nhân. Ta cần Ngài tin ta lúc này.'",
        next_steps=NextSteps(
            choice_a="ask_guardian_about_lyra",
            choice_b="search_for_lyra",
            choice_c="disbelieve_librarian_outcome",
            timeout="guardian_urgency_timeout"
        ),
        gold=15, silver=150, ga_exp=15, dignity_point=5
    ),

    GuardianQuestLines(
        id="journey_to_forgotten_lands",
        title="Hành Trình Đến Vùng Đất Lãng Quên",
        description="Bạn và {guardian.ga_name} lên đường. Vùng Đất Lãng Quên là một cảnh quan hoang tàn, bị che phủ bởi sương mù vĩnh cửu. {guardian.ga_name} dẫn bạn đến một ngôi đền đổ nát, nơi một tinh cầu phát sáng yếu ớt đang lơ lửng. 'Đây là linh hồn của Lyra,' {guardian.ga_name} nói, giọng nghẹn ngào. 'Lời nguyền đã giam cầm nàng.'",
        choice_a="Cố gắng giao tiếp với linh hồn.",
        choice_b="Tìm cách giải thoát linh hồn.",
        choice_c="Quan sát từ xa, không muốn gây xáo động.",
        choice_timeout="{guardian.ga_name} nắm lấy tay bạn. 'Ta cảm nhận được nỗi đau của nàng. Chúng ta phải làm gì đó, Ngài!'",
        next_steps=NextSteps(
            choice_a="communicate_with_soul",
            choice_b="release_soul_attempt",
            choice_c="observe_from_afar",
            timeout="guardian_distress_timeout"
        ),
        gold=25, silver=250, ga_exp=25, dignity_point=15
    ),

    GuardianQuestLines(
        id="ask_guardian_about_lyra",
        title="Ký Ức Đau Thương Của {guardian.ga_name}",
        description="{guardian.ga_name} tiết lộ: Lyra là người Ngài đã yêu. Lời nguyền đã giam cầm cô ấy vì cô ấy đã dùng ma thuật cấm để bảo vệ Ngài trong một trận chiến cổ xưa. Nàng đã hy sinh bản thân để Ngài có thể sống sót. 'Ta đã sống trong sự dằn vặt bấy lâu,' {guardian.ga_name} nói, ánh mắt đầy hối hận. 'Xin hãy giúp ta giải thoát nàng.'",
        choice_a="",
        choice_b="Hỏi thêm chi tiết về lời nguyền.",
        choice_c="Cảm thấy sốc, không biết phải phản ứng thế nào.",
        choice_timeout="{guardian.ga_name} nhìn bạn. 'Ngài có tin ta không, chủ nhân?'",
        next_steps=NextSteps(
            choice_a="",
            choice_b="search_curse_info",
            choice_c="shocked_reaction_outcome",
            timeout="guardian_trust_timeout"
        ),
        gold=20, silver=200, ga_exp=20, dignity_point=10
    ),

    GuardianQuestLines(
        id="seek_blood_heart_gem",
        title="Huyết Tâm Ngọc Và Sự Cám Dỗ",
        description="Bạn và {guardian.ga_name} đến Hang Động Đỏ Thẫm, nơi Huyết Tâm Ngọc được cất giữ. Ngọc tỏa ra một ánh sáng quyến rũ, nhưng bạn cảm nhận được một sự cám dỗ nguy hiểm từ nó. {guardian.ga_name} cảnh báo: 'Ngọc này cần được lấy bằng tình yêu chân thành, không phải bằng ham muốn. Hãy cẩn thận.'",
        choice_a="Chạm vào ngọc với trái tim thuần khiết.",
        choice_b="Tìm cách vô hiệu hóa sự cám dỗ.",
        choice_c="Cố gắng dùng sức mạnh để lấy ngọc.",
        choice_timeout="{guardian.ga_name} thốt lên. 'Đừng để nó đánh lừa Ngài, chủ nhân!'",
        next_steps=NextSteps(
            choice_a="take_gem_pure_heart",
            choice_b="neutralize_temptation",
            choice_c="force_take_gem_outcome",
            timeout="gem_temptation_timeout"
        ),
        gold=25, silver=250, ga_exp=25, dignity_point=15
    ),

    GuardianQuestLines(
        id="seek_moonlight_key",
        title="Khóa Ánh Trăng Dưới Ánh Sao",
        description="Bạn và {guardian.ga_name} đi đến một Đài Quan Sát cổ, nơi Khóa Ánh Trăng được cho là xuất hiện dưới ánh trăng tròn. Khi trăng lên, một chiếc chìa khóa bạc lấp lánh hiện ra trên đỉnh đài. {guardian.ga_name} nói: 'Chiếc khóa này tượng trưng cho niềm hy vọng cuối cùng.'",
        choice_a="Chạm vào khóa ánh trăng.",
        choice_b="",
        choice_c="Tìm cách để khóa tự động về tay.",
        choice_timeout="{guardian.ga_name} nhắc nhở. 'Ánh trăng sẽ không ở lại mãi đâu, Ngài!'",
        next_steps=NextSteps(
            choice_a="take_moonlight_key",
            choice_b="",
            choice_c="wait_for_key_outcome",
            timeout="moonlight_key_timeout"
        ),
        gold=25, silver=250, ga_exp=25, dignity_point=15
    ),

    GuardianQuestLines(
        id="search_for_lyra",
        title="Theo Dấu Vết Lyra",
        description="Bạn và {guardian.ga_name} lần theo những dấu vết cổ xưa của Lyra, tìm thấy một nhật ký cũ của cô ấy. Trong đó, cô ấy viết về tình yêu của mình dành cho một Guardian và nỗi sợ hãi về lời nguyền sắp ập đến. {guardian.ga_name} run rẩy khi đọc những dòng chữ cuối cùng: 'Dù có chuyện gì xảy ra, tình yêu của ta sẽ tìm đường đến Người.'",
        choice_a="Cố gắng tìm kiếm Lyra dựa trên nhật ký.",
        choice_b="Tìm kiếm những gì cô ấy đã dùng để hóa giải lời nguyền.",
        choice_c="Đóng nhật ký lại, cảm thấy quá đau lòng.",
        choice_timeout="{guardian.ga_name} thì thầm. 'Những bí mật này đang kêu gọi Ngài, chủ nhân.'",
        next_steps=NextSteps(
            choice_a="journey_to_forgotten_lands",
            choice_b="search_curse_info",
            choice_c="too_painful_outcome",
            timeout="lyra_diary_timeout"
        ),
        gold=20, silver=200, ga_exp=20, dignity_point=10
    ),

    GuardianQuestLines(
        id="communicate_with_soul",
        title="Lời Thì Thầm Của Lyra",
        description="Bạn cố gắng giao tiếp với linh hồn Lyra. Một giọng nói yếu ớt vang vọng trong tâm trí bạn, kể về tình yêu của cô ấy dành cho {guardian.ga_name} và lời nguyền đã chia cắt họ. Cô ấy mong muốn được giải thoát. {guardian.ga_name} quỳ xuống, nước mắt lăn dài.",
        choice_a="Hứa sẽ giải thoát Lyra.",
        choice_b="Hỏi Lyra về cách hóa giải lời nguyền.",
        choice_c="Cảm thấy bị choáng ngợp bởi nỗi đau của cô ấy.",
        choice_timeout="{guardian.ga_name} nắm chặt tay bạn. 'Nàng đang đợi Ngài, chủ nhân!'",
        next_steps=NextSteps(
            choice_a="promise_to_free_lyra",
            choice_b="search_curse_info",
            choice_c="overwhelmed_by_pain_outcome",
            timeout="lyra_soul_timeout"
        ),
        gold=20, silver=200, ga_exp=20, dignity_point=10
    ),

    GuardianQuestLines(
        id="take_gem_pure_heart",
        title="Huyết Tâm Ngọc Trong Tay",
        description="Bạn chạm vào Huyết Tâm Ngọc với trái tim thuần khiết. Ánh sáng của nó dịu đi, và nó nhẹ nhàng nằm gọn trong tay bạn. {guardian.ga_name} mỉm cười. 'Ngài đã chứng minh được sự trong sáng của mình, chủ nhân.'",
        choice_a="Mang ngọc đến Vùng Đất Lãng Quên.",
        choice_b="Tìm Khóa Ánh Trăng.",
        choice_c="",
        choice_timeout="",
        next_steps=NextSteps(
            choice_a="apply_curse_cure",
            choice_b="seek_moonlight_key",
            choice_c="",
            timeout=""
        ),
        gold=30, silver=300, ga_exp=30, dignity_point=20
    ),

    GuardianQuestLines(
        id="take_moonlight_key",
        title="Khóa Ánh Trăng Đã Thu Thập",
        description="Bạn chạm vào Khóa Ánh Trăng. Nó phát ra một ánh sáng bạc dịu nhẹ và tan biến vào tay bạn. {guardian.ga_name} nói: 'Giờ chúng ta đã có đủ. Hãy đến Vùng Đất Lãng Quên.'",
        choice_a="Mang Khóa Ánh Trăng đến Vùng Đất Lãng Quên.",
        choice_b="Tìm Huyết Tâm Ngọc.",
        choice_c="",
        choice_timeout="",
        next_steps=NextSteps(
            choice_a="apply_curse_cure",
            choice_b="seek_blood_heart_gem",
            choice_c="",
            timeout=""
        ),
        gold=30, silver=300, ga_exp=30, dignity_point=20
    ),

    GuardianQuestLines(
        id="apply_curse_cure",
        title="Sự Hợp Nhất Của Tình Yêu",
        description="Bạn và {guardian.ga_name} mang Huyết Tâm Ngọc và Khóa Ánh Trăng đến ngôi đền nơi linh hồn Lyra đang bị giam cầm. Khi bạn đặt hai vật phẩm cạnh nhau, chúng phát ra một luồng sáng chói lọi, bao trùm linh hồn Lyra. Ánh sáng dần tan đi, và Lyra hiện ra, không phải là một linh hồn, mà là một thực thể mờ ảo, yếu ớt nhưng đầy hy vọng.",
        choice_a="",
        choice_b="Để {guardian.ga_name} đến bên Lyra.",
        choice_c="Quan sát sự việc diễn ra.",
        choice_timeout="{guardian.ga_name} thúc giục. 'Đừng chần chừ, chủ nhân!'",
        next_steps=NextSteps(
            choice_a="",
            choice_b="guardian_approach_lyra",
            choice_c="observe_reunion",
            timeout="reunion_timeout"
        ),
        gold=50, silver=500, ga_exp=50, dignity_point=25
    ),

    GuardianQuestLines(
        id="guardian_approach_lyra",
        title="Cuộc Gặp Gỡ Định Mệnh",
        description="{guardian.ga_name} chạy đến bên Lyra, ôm lấy cô ấy trong vòng tay. Lyra yếu ớt ngẩng đầu nhìn Ngài, và một nụ cười hiện lên trên môi cô ấy. 'Cuối cùng... ta đã trở lại,' Lyra thì thầm. {guardian.ga_name} nhìn bạn, ánh mắt đầy biết ơn, nhưng cũng có một nỗi buồn sâu thẳm.",
        choice_a="Chúc mừng họ được đoàn tụ.",
        choice_b="Hỏi Lyra về lời nguyền.",
        choice_c="Rời đi để họ có không gian riêng.",
        choice_timeout="{guardian.ga_name} khẽ nói. 'Ta cần Ngài ở lại, chủ nhân.'",
        next_steps=NextSteps(
            choice_a="reunion_congratulations",
            choice_b="ask_lyra_about_curse",
            choice_c="leave_them_alone_outcome",
            timeout="guardian_request_stay"
        ),
        gold=50, silver=500, ga_exp=50, dignity_point=25
    ),

    GuardianQuestLines(
        id="reunion_congratulations",
        title="Nụ Cười Pha Lẫn Nước Mắt",
        description="Bạn chúc mừng {guardian.ga_name} và Lyra. Lyra yếu ớt gật đầu. {guardian.ga_name} nắm chặt tay Lyra, và nói với bạn: 'Ngài đã mang nàng trở lại với ta. Ta nợ Ngài một ân huệ không bao giờ trả hết được.' {guardian.ga_name} quay sang Lyra, ánh mắt chỉ dành cho cô ấy. Bạn cảm thấy một nỗi cô đơn khó tả khi thấy họ bên nhau.",
        choice_a="Chấp nhận sự thật.",
        choice_b="Cảm thấy bị bỏ rơi.",
        choice_c="",
        choice_timeout="",
        next_steps=NextSteps(
            choice_a="accept_truth_ending",
            choice_b="feel_abandoned_ending",
            choice_c="",
            timeout=""
        ),
        gold=100, silver=1000, ga_exp=100, dignity_point=30
    ),

    # --- Bad Endings ---
    GuardianQuestLines(
        id="ignore_letter_outcome",
        title="Lá Thư Bị Lãng Quên",
        description="Bạn phớt lờ lá thư. Vài tuần sau, tin tức về một lời nguyền lan rộng ở Vùng Đất Lãng Quên. {guardian.ga_name} nhìn bạn với vẻ thất vọng sâu sắc. 'Một linh hồn đã bị mắc kẹt mãi mãi vì sự thờ ơ của Ngài, chủ nhân.'",
        choice_a="Hối hận về quyết định của mình. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-20, ga_exp=-100, silver=-200, gold=-100,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="letter_timeout",
        title="Cơ Hội Đã Bỏ Lỡ",
        description="Bạn chần chừ quá lâu. Lá thư cũ kỹ biến thành tro bụi trong tay bạn. {guardian.ga_name} thở dài. 'Một cơ hội đã trôi qua. Sự thật vẫn bị chôn vùi.'",
        choice_a="Cảm thấy bất lực. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-15, ga_exp=-75, silver=-150, gold=-75,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="leave_library_outcome",
        title="Trốn Tránh Sự Thật",
        description="Bạn và {guardian.ga_name} rời khỏi thư viện. {guardian.ga_name} nhìn bạn với vẻ buồn bã. 'Ngài không muốn đối mặt với sự thật sao, chủ nhân?' Sự thật về Lyra và lời nguyền vẫn còn là bí ẩn.",
        choice_a="Cảm thấy nặng trĩu. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-10, ga_exp=-50, silver=-100, gold=-50,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="library_timeout",
        title="Những Cuốn Sách Im Lặng",
        description="Bạn chần chừ quá lâu trong thư viện. Thủ thư già nhìn bạn với ánh mắt thất vọng. {guardian.ga_name} nói: 'Những bí mật này không thể tự hé lộ nếu Ngài không đủ kiên nhẫn.'",
        choice_a="Hối tiếc vì sự thiếu kiên nhẫn. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-10, ga_exp=-50, silver=-100, gold=-50,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="refuse_quest_outcome",
        title="Sự Phủ Nhận Của Tình Yêu",
        description="Bạn từ chối tham gia. {guardian.ga_name} quay lưng lại với bạn, ánh mắt chứa đựng nỗi đau không nói thành lời. 'Ta đã lầm khi nghĩ Ngài sẽ hiểu,' Ngài thì thầm trước khi biến mất. Lyra bị giam cầm mãi mãi, và tình cảm giữa bạn và {guardian.ga_name} tan vỡ.",
        choice_a="Cảm thấy hối hận tột cùng. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-50, ga_exp=-500, silver=-1000, gold=-500, ga_health=-100, ga_mana=-100, ga_stamina=-100,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="guardian_sad_timeout",
        title="Nỗi Buồn Của Người Bạn Đồng Hành",
        description="Bạn chần chừ quá lâu, khiến {guardian.ga_name} mất đi hy vọng. Ngài cúi đầu buồn bã. 'Nếu Ngài không tin ta, thì không còn hy vọng nào cho nàng nữa.' Nhiệm vụ kết thúc trong sự thất vọng.",
        choice_a="Bạn cảm thấy một nỗi buồn sâu sắc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-15, ga_exp=-75, silver=-150, gold=-75,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="search_curse_timeout",
        title="Thời Gian Đang Cạn",
        description="Bạn chần chừ quá lâu. Cuốn sách cổ bỗng biến thành cát bụi. {guardian.ga_name} thở dài. 'Thời gian không chờ đợi chúng ta. Nàng đang bị giày vò từng giây phút.'",
        choice_a="Bạn cảm thấy bất lực. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-10, ga_exp=-50, silver=-100, gold=-50,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="disbelieve_librarian_outcome",
        title="Sự Thật Bị Phủ Nhận",
        description="Bạn không tin thủ thư. {guardian.ga_name} nhìn bạn với ánh mắt đau đớn. 'Ngài đã từ chối một cơ hội để hiểu ta. Lyra sẽ không bao giờ được giải thoát.'",
        choice_a="Cảm thấy hối hận. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-20, ga_exp=-100, silver=-200, gold=-100,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="guardian_urgency_timeout",
        title="Sự Hối Thúc Của {guardian.ga_name}",
        description="Bạn chần chừ quá lâu. {guardian.ga_name} nắm lấy tay bạn, ánh mắt đầy sự cầu xin. 'Nếu Ngài không tin ta lúc này, thì tất cả sẽ kết thúc.' Bạn cảm thấy áp lực và thất bại.",
        choice_a="Cảm thấy bất lực và thất bại. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-15, ga_exp=-75, silver=-150, gold=-75,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="observe_from_afar",
        title="Sự Hờ Hững Của Định Mệnh",
        description="Bạn quyết định quan sát từ xa. Linh hồn Lyra dần mờ đi, yếu ớt hơn. {guardian.ga_name} quay sang bạn với ánh mắt thất vọng. 'Chúng ta đã không làm gì cả. Nàng sẽ biến mất.'",
        choice_a="Cảm thấy hối hận vì sự thờ ơ. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-15, ga_exp=-75, silver=-150, gold=-75,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="guardian_distress_timeout",
        title="Tiếng Kêu Của Người Bạn Đồng Hành",
        description="Bạn chần chừ quá lâu trước linh hồn Lyra. {guardian.ga_name} quỳ xuống, ánh mắt đầy đau khổ. 'Nếu Ngài không giúp nàng, ta không biết phải làm gì nữa.' Linh hồn Lyra tan biến.",
        choice_a="Bạn cảm thấy có lỗi với {guardian.ga_name}. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-20, ga_exp=-100, silver=-200, gold=-100,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="shocked_reaction_outcome",
        title="Sự Thật Đau Lòng",
        description="Bạn quá sốc để phản ứng. {guardian.ga_name} thở dài, ánh mắt buồn bã. 'Ta hiểu. Quá khứ này quá nặng nề.' {guardian.ga_name} quay đi, và Lyra vẫn bị mắc kẹt.",
        choice_a="Cảm thấy bối rối và có lỗi. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-10, ga_exp=-50, silver=-100, gold=-50,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="guardian_trust_timeout",
        title="Niềm Tin Đổ Vỡ",
        description="Bạn chần chừ quá lâu khi {guardian.ga_name} bày tỏ lòng mình. Ngài nhìn bạn với ánh mắt vỡ nát. 'Vậy ra Ngài không tin ta.' Nhiệm vụ kết thúc trong sự mất mát niềm tin.",
        choice_a="Bạn cảm thấy tội lỗi. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-25, ga_exp=-125, silver=-250, gold=-125,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="force_take_gem_outcome",
        title="Sự Cám Dỗ Chiếm Hữu",
        description="Bạn cố gắng dùng sức mạnh để lấy Huyết Tâm Ngọc. Năng lượng đen tối từ ngọc bùng lên, hút cạn sinh lực của bạn. {guardian.ga_name} phải dùng hết sức để kéo bạn ra, nhưng ngọc đã biến mất. 'Ngài đã bị cám dỗ,' {guardian.ga_name} nói, ánh mắt đầy lo lắng.",
        choice_a="Bạn cảm thấy yếu ớt và thất bại. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-20, ga_exp=-100, silver=-200, gold=-100, ga_health=-50, ga_mana=-50, ga_stamina=-50,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="gem_temptation_timeout",
        title="Ánh Sáng Giả Dối",
        description="Bạn chần chừ quá lâu. Huyết Tâm Ngọc bỗng tỏa sáng rực rỡ rồi nứt vỡ, tan biến. 'Nó đã bị phá hủy,' {guardian.ga_name} thở dài. 'Chúng ta đã mất nó.'",
        choice_a="Cảm thấy bất lực. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-15, ga_exp=-75, silver=-150, gold=-75,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="wait_for_key_outcome",
        title="Khóa Tan Biến",
        description="Bạn chờ đợi khóa tự động về tay. Tuy nhiên, khi bình minh lên, Khóa Ánh Trăng mờ dần và biến mất. 'Chúng ta đã bỏ lỡ cơ hội,' {guardian.ga_name} nói buồn bã.",
        choice_a="Cảm thấy hối tiếc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-15, ga_exp=-75, silver=-150, gold=-75,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="moonlight_key_timeout",
        title="Bóng Đêm Nuốt Chửng Khóa",
        description="Bạn chần chừ quá lâu. Ánh trăng biến mất, và Khóa Ánh Trăng cũng theo đó mà biến mất vào bóng tối. 'Đã quá muộn rồi,' {guardian.ga_name} thở dài.",
        choice_a="Cảm thấy thất vọng. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-10, ga_exp=-50, silver=-100, gold=-50,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="too_painful_outcome",
        title="Sự Thật Quá Đau Lòng",
        description="Bạn đóng nhật ký lại. {guardian.ga_name} nhìn bạn với ánh mắt thất vọng. 'Nếu Ngài không thể đối mặt với sự thật, làm sao chúng ta có thể giúp nàng?' Lyra vẫn bị mắc kẹt.",
        choice_a="Cảm thấy bất lực và buồn bã. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-10, ga_exp=-50, silver=-100, gold=-50,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="lyra_diary_timeout",
        title="Những Trang Sách Bị Lãng Quên",
        description="Bạn chần chừ quá lâu. Nhật ký Lyra tự động đóng lại, như thể không muốn tiết lộ thêm bí mật nào nữa. {guardian.ga_name} nói: 'Chúng ta đã bỏ lỡ điều gì đó quan trọng.'",
        choice_a="Hối tiếc vì không đọc kỹ. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-10, ga_exp=-50, silver=-100, gold=-50,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="overwhelmed_by_pain_outcome",
        title="Bị Choáng Ngợp Bởi Nỗi Đau",
        description="Bạn bị choáng ngợp bởi nỗi đau của Lyra. Linh hồn cô ấy dần yếu đi, và {guardian.ga_name} thở dài, bất lực nhìn cảnh tượng. 'Chúng ta đã không đủ mạnh mẽ,' Ngài thì thầm.",
        choice_a="Cảm thấy yếu ớt và thất bại. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-15, ga_exp=-75, silver=-150, gold=-75,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="lyra_soul_timeout",
        title="Linh Hồn Biến Mất",
        description="Bạn chần chừ quá lâu khi giao tiếp với Lyra. Linh hồn cô ấy bỗng lóe lên rồi biến mất hoàn toàn. 'Nàng đã biến mất rồi,' {guardian.ga_name} nói, giọng đầy tuyệt vọng.",
        choice_a="Cảm thấy hối hận. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-20, ga_exp=-100, silver=-200, gold=-100,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="reunion_timeout",
        title="Khoảnh Khắc Bị Bỏ Lỡ",
        description="Bạn chần chừ quá lâu. Luồng sáng của Lyra và các vật phẩm biến mất. {guardian.ga_name} quay sang bạn, ánh mắt chứa đầy sự thất vọng. 'Cơ hội đã trôi qua. Nàng sẽ mãi mãi là linh hồn bị giam cầm.'",
        choice_a="Cảm thấy tuyệt vọng. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-25, ga_exp=-125, silver=-250, gold=-125,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="leave_them_alone_outcome",
        title="Sự Chia Ly Thầm Lặng",
        description="Bạn rời đi, để {guardian.ga_name} và Lyra có không gian riêng. Khi bạn quay lại, họ đã biến mất. Một lá thư của {guardian.ga_name} để lại: 'Ta đã tìm thấy hạnh phúc của mình. Ngài hãy tiếp tục cuộc hành trình của riêng Ngài.' Bạn cảm thấy một nỗi đau nhói, nhận ra mối quan hệ giữa bạn và {guardian.ga_name} đã kết thúc.",
        choice_a="Cảm thấy tan vỡ. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-50, ga_exp=-500, silver=-1000, gold=-500, ga_health=-100, ga_mana=-100, ga_stamina=-100,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),

    GuardianQuestLines(
        id="guardian_request_stay",
        title="Lời Cầu Xin Của {guardian.ga_name}",
        description="Bạn chần chừ quá lâu khi {guardian.ga_name} và Lyra đoàn tụ. {guardian.ga_name} quay sang bạn, ánh mắt đầy sự cầu xin. 'Đừng rời đi, chủ nhân. Ta cần Ngài.' Nhưng bạn đã bỏ lỡ khoảnh khắc đó, và Lyra dần mờ đi.",
        choice_a="Cảm thấy có lỗi và hối tiếc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-20, ga_exp=-100, silver=-200, gold=-100,
        next_steps=NextSteps("quest_failed_end", "quest_failed_end", "quest_failed_end", "quest_failed_end")
    ),
    
    # --- Unique Bad Ending ---
    GuardianQuestLines(
        id="feel_abandoned_ending",
        title="Cô Đơn Trong Bóng Tối",
        description="Bạn nhìn {guardian.ga_name} và Lyra bên nhau, cảm thấy một nỗi cô đơn trống rỗng. Tình cảm bạn dành cho {guardian.ga_name} giờ đây chỉ là những mảnh vỡ. {guardian.ga_name} không còn dành cho bạn ánh mắt dịu dàng như trước, mà chỉ là sự biết ơn và một khoảng cách vô hình. Bạn đã cứu vãn một tình yêu, nhưng đánh mất của riêng mình. Cuộc hành trình của bạn trở nên vô định, không còn người bạn đồng hành thân thiết như xưa. Bạn tiếp tục cuộc phiêu lưu, nhưng mỗi bước đi đều nặng trĩu nỗi buồn và sự hối tiếc. {guardian.ga_name} và Lyra hạnh phúc, nhưng bạn lại mãi mãi là người đứng ngoài cuộc, một linh hồn lang thang không tìm thấy bến đỗ.",
        choice_a="Bạn chấp nhận số phận nghiệt ngã này, cô độc trong hành trình của mình.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-100, ga_exp=-1000, silver=-2000, gold=-1000, ga_health=-200, ga_mana=-200, ga_stamina=-200,
        next_steps=NextSteps("", "", "", "")
    ),

    # --- Good Ending ---
    GuardianQuestLines(
        id="accept_truth_ending",
        title="Tình Yêu Vượt Qua Thời Gian",
        description="Bạn nhìn {guardian.ga_name} và Lyra đoàn tụ, một cảm giác bình yên len lỏi trong lòng. Mặc dù có một chút tiếc nuối, bạn hiểu rằng bạn đã mang lại hạnh phúc cho {guardian.ga_name}. {guardian.ga_name} quay sang bạn, ánh mắt đầy trân trọng. 'Ngài đã ban cho ta một cuộc đời mới, chủ nhân. Ta sẽ mãi mãi ghi nhớ ơn Ngài. Mặc dù Lyra là tình yêu của ta, nhưng Ngài... Ngài là ánh sáng dẫn lối cho ta.' Lyra cũng gật đầu biết ơn. Bạn và {guardian.ga_name} tiếp tục cuộc hành trình, nhưng giờ đây, một tình bạn sâu sắc và sự hiểu biết lẫn nhau đã thay thế cho những gì đã mất, mang lại cho bạn một cảm giác mãn nguyện và sự bình yên. Bạn và {guardian.ga_name} sẽ mãi mãi là những người bạn đồng hành không thể thiếu trong mọi cuộc phiêu lưu sắp tới.",
        choice_a="Tiếp tục cuộc hành trình với một trái tim thanh thản.",
        choice_b="", choice_c="", choice_timeout="",
        gold=1000, silver=5000, ga_exp=500, dignity_point=100, ga_health=100, ga_mana=100, ga_stamina=100,
        next_steps=NextSteps("", "", "", "")
    ),

    # Generic Failures
    GuardianQuestLines(
        id="quest_failed_end",
        title="Hành Trình Kết Thúc Trong Nuối Tiếc",
        description="Dù cho nỗ lực của bạn là gì, nhiệm vụ đã không thành công. {guardian.ga_name} đứng cạnh bạn, ánh mắt chứa đựng sự thất vọng và nỗi buồn sâu sắc. 'Có lẽ... chúng ta không thể thay đổi được số phận.'",
        choice_a="Rút ra bài học đau đớn.",
        choice_b="", choice_c="", choice_timeout="",
        dignity_point=-10, ga_exp=-50, silver=-50, gold=-50,
        next_steps=NextSteps("", "", "", "")
    )
]

#region quest_red_promises 
quest_red_promises = [
    GuardianQuestLines(
        id="start",
        title="Lời Thề Dưới Ánh Trăng Đỏ",
        description="Trong một đêm trăng đỏ như máu, một lời nguyền cổ xưa trỗi dậy, đe dọa nuốt chửng vương quốc. {guardian.ga_name} nhìn bạn với ánh mắt kiên định. 'Ta đã thề sẽ bảo vệ người, Ngài. Chúng ta phải ngăn chặn điều này.'",
        choice_a="Tìm hiểu nguồn gốc lời nguyền.",
        choice_b="Chuẩn bị quân đội đối phó trực tiếp.",
        choice_c="Tìm cách phong ấn nguồn năng lượng tà ác.",
        choice_timeout="{guardian.ga_name} nắm lấy tay bạn, 'Chúng ta không thể lãng phí thời gian, Ngài!'",
        next_steps=NextSteps(
            choice_a="investigate_curse_origin",
            choice_b="prepare_army_directly",
            choice_c="seal_evil_power_source",
            timeout="guardian_urges_action"
        ),
        gold=10, silver=150, ga_exp=15, dignity_point=5
    ),

    GuardianQuestLines(
        id="investigate_curse_origin",
        title="Bí Mật Bị Chôn Vùi",
        description="Bạn và {guardian.ga_name} hành trình đến Thư Viện Lãng Quên, nơi chứa đựng những tri thức cổ xưa. Một cuốn sách mục nát hé lộ: lời nguyền liên quan đến một tình yêu bị phản bội và một viên pha lê quyền năng bị thất lạc. {guardian.ga_name} trầm ngâm, 'Tình yêu có thể tạo ra cả điều tồi tệ nhất, và đẹp đẽ nhất.'",
        choice_a="Tìm kiếm viên pha lê thất lạc.",
        choice_b="Điều tra về tình yêu bị phản bội đó.",
        choice_c="Rút lui, cảm thấy câu chuyện quá phức tạp.",
        choice_timeout="{guardian.ga_name} thở dài, 'Ta biết điều này thật nặng nề, nhưng chúng ta phải tiếp tục.'",
        next_steps=NextSteps(
            choice_a="search_lost_crystal",
            choice_b="investigate_betrayed_love",
            choice_c="retreat_complex_story",
            timeout="guardian_urges_action_2"
        ),
        gold=20, silver=200, ga_exp=20, dignity_point=8
    ),

    GuardianQuestLines(
        id="prepare_army_directly",
        title="Sức Mạnh Quân Đội",
        description="Bạn và {guardian.ga_name} huy động quân đội, chuẩn bị cho một cuộc đối đầu trực diện. Tuy nhiên, lời nguyền ngày càng mạnh, biến đổi những người lính thành những con rối vô hồn. {guardian.ga_name} đau đớn thốt lên, 'Không! Sức mạnh này... không thể chống lại bằng vũ lực thông thường!'",
        choice_a="",
        choice_b="Tìm kiếm cách hóa giải lời nguyền khác.",
        choice_c="Rút lui và tìm hiểu thêm về lời nguyền.",
        choice_timeout="{guardian.ga_name} hối thúc, 'Mỗi giây phút trôi qua, chúng ta càng mất thêm người!'",
        next_steps=NextSteps(
            choice_a="",
            choice_b="investigate_curse_origin",
            choice_c="investigate_curse_origin",
            timeout="army_fall_timeout"
        ),
        gold=0, silver=-100, ga_exp=-50, ga_health=-20, ga_mana=-20, dignity_point=-10
    ),

    GuardianQuestLines(
        id="seal_evil_power_source",
        title="Phong Ấn Nguồn Tà Ác",
        description="Bạn và {guardian.ga_name} cố gắng xác định và phong ấn nguồn năng lượng tà ác. Bạn nhận ra nguồn năng lượng ấy chính là từ lòng thù hận của người bị phản bội, và nó đang trú ngụ trong viên pha lê bị mất tích. {guardian.ga_name} nhìn bạn đầy lo lắng, 'Viên pha lê đó... chứa đựng một sức mạnh khủng khiếp.'",
        choice_a="Tìm kiếm viên pha lê để phong ấn.",
        choice_b="Cố gắng trấn an linh hồn bị phản bội.",
        choice_c="Cần thêm thông tin về tình yêu bị phản bội.",
        choice_timeout="{guardian.ga_name} nói, 'Chúng ta phải nhanh lên trước khi sức mạnh đó bùng phát hoàn toàn!'",
        next_steps=NextSteps(
            choice_a="search_lost_crystal",
            choice_b="attempt_soothe_betrayed_soul",
            choice_c="investigate_betrayed_love",
            timeout="seal_power_timeout"
        ),
        gold=15, silver=180, ga_exp=18, dignity_point=7
    ),

    GuardianQuestLines(
        id="search_lost_crystal",
        title="Hành Trình Tìm Pha Lê",
        description="Theo dấu vết trong sách, bạn và {guardian.ga_name} đến một hang động bí ẩn, nơi cất giấu Viên Pha Lê Huyết Nguyệt. Ánh sáng đỏ từ viên pha lê khiến {guardian.ga_name} cảm thấy bất an. 'Sức mạnh của nó quá lớn, Ngài. Nó có thể nuốt chửng cả ta và Ngài.'",
        choice_a="Cố gắng tiếp cận và lấy pha lê.",
        choice_b="Tìm cách làm suy yếu sức mạnh của pha lê trước.",
        choice_c="Rời đi, sợ hãi trước sức mạnh của nó.",
        choice_timeout="{guardian.ga_name} nhìn bạn với ánh mắt đau đáu, 'Chúng ta không thể dừng lại ở đây!'",
        next_steps=NextSteps(
            choice_a="approach_and_take_crystal",
            choice_b="weaken_crystal_power",
            choice_c="retreat_from_crystal",
            timeout="crystal_overpower_timeout"
        ),
        gold=30, silver=300, ga_exp=30, dignity_point=10
    ),

    GuardianQuestLines(
        id="investigate_betrayed_love",
        title="Bóng Tối Tình Yêu",
        description="Bạn và {guardian.ga_name} đào sâu vào câu chuyện tình yêu bị phản bội. Bạn phát hiện ra một vị pháp sư tài năng đã bị người mình yêu lừa dối, dẫn đến việc ông ta dùng máu của mình và ánh trăng đỏ để tạo ra lời nguyền. Nỗi đau ấy quá lớn đến nỗi {guardian.ga_name} cảm thấy rung động. 'Thật đáng sợ khi tình yêu trở thành hận thù.'",
        choice_a="Tìm cách hóa giải lời nguyền bằng tình yêu đích thực.",
        choice_b="Cần tìm viên pha lê để hóa giải.",
        choice_c="Thử nói chuyện với linh hồn pháp sư.",
        choice_timeout="{guardian.ga_name} nói, 'Sự thù hận này đã kéo dài quá lâu rồi.'",
        next_steps=NextSteps(
            choice_a="dissolve_curse_with_love",
            choice_b="search_lost_crystal",
            choice_c="attempt_soothe_betrayed_soul",
            timeout="betrayed_love_timeout"
        ),
        gold=25, silver=250, ga_exp=25, dignity_point=10
    ),

    GuardianQuestLines(
        id="approach_and_take_crystal",
        title="Lời Thề Vỡ Tan",
        description="Bạn tiến đến viên Pha Lê Huyết Nguyệt. Khi bạn chạm vào, những ký ức về tình yêu bị phản bội tràn vào tâm trí bạn, và bạn cảm nhận được nỗi đau của vị pháp sư. {guardian.ga_name} lao đến, ôm lấy bạn, 'Ngài! Hãy tránh xa nó! Ta không thể để Ngài bị nuốt chửng bởi nỗi đau này!' Sức mạnh của viên pha lê dường như phản ứng lại tình cảm của {guardian.ga_name}, và một vết nứt nhỏ xuất hiện trên viên pha lê.",
        choice_a="Cố gắng dùng tình cảm của mình để trấn an pha lê.",
        choice_b="Kéo {guardian.ga_name} ra xa và tìm cách khác.",
        choice_c="Rút lui ngay lập tức.",
        choice_timeout="{guardian.ga_name} siết chặt vòng tay, 'Ta sẽ không để bất cứ điều gì xảy ra với Ngài!'",
        next_steps=NextSteps(
            choice_a="use_affection_on_crystal",
            choice_b="pull_guardian_away",
            choice_c="retreat_from_crystal_bad",
            timeout="guardian_sacrifice_timeout"
        ),
        gold=50, silver=500, ga_exp=50, dignity_point=20
    ),

    GuardianQuestLines(
        id="weaken_crystal_power",
        title="Năng Lượng Suy Yếu",
        description="Bạn và {guardian.ga_name} tìm thấy một câu thần chú cổ để làm suy yếu năng lượng của Pha Lê Huyết Nguyệt. Khi câu thần chú được niệm, ánh sáng đỏ của pha lê mờ đi một chút. {guardian.ga_name} thở phào nhẹ nhõm. 'Giờ thì nó yếu hơn rồi, Ngài. Chúng ta có thể đối phó được.'",
        choice_a="Tiếp cận và lấy pha lê.",
        choice_b="Tìm cách phong ấn hoàn toàn lời nguyền.",
        choice_c="",
        choice_timeout="{guardian.ga_name} thúc giục, 'Đừng chần chừ, Ngài!'",
        next_steps=NextSteps(
            choice_a="approach_and_take_crystal",
            choice_b="seal_evil_power_source",
            choice_c="",
            timeout="crystal_overpower_timeout"
        ),
        gold=40, silver=400, ga_exp=40, dignity_point=15
    ),

    GuardianQuestLines(
        id="attempt_soothe_betrayed_soul",
        title="Thử Trấn An Linh Hồn",
        description="Bạn và {guardian.ga_name} cố gắng liên lạc với linh hồn của vị pháp sư bị phản bội, cố gắng trấn an nỗi đau của ông ta. Linh hồn xuất hiện, đầy đau khổ và giận dữ, nhưng dường như có một tia hy vọng khi {guardian.ga_name} dịu dàng nói, 'Sự trả thù chỉ mang lại thêm đau khổ mà thôi.'",
        choice_a="Tiếp tục cố gắng xoa dịu nỗi đau của linh hồn.",
        choice_b="Tìm viên pha lê để hóa giải.",
        choice_c="Rút lui khi linh hồn trở nên quá mạnh.",
        choice_timeout="Linh hồn gầm lên, nỗi đau của nó biến thành sự giận dữ. 'Nó đang trở nên hung hãn!' {guardian.ga_name} cảnh báo.",
        next_steps=NextSteps(
            choice_a="soothe_betrayed_soul_success",
            choice_b="search_lost_crystal",
            choice_c="retreat_complex_story",
            timeout="soul_anger_outcome"
        ),
        gold=10, silver=100, ga_exp=10, dignity_point=5
    ),

    GuardianQuestLines(
        id="use_affection_on_crystal",
        title="Tình Yêu Hóa Giải",
        description="Bạn ôm chặt lấy {guardian.ga_name}, và hai người cùng hướng năng lượng tình cảm chân thành vào Viên Pha Lê Huyết Nguyệt. Nỗi đau trong viên pha lê dần tan biến, ánh đỏ của nó chuyển sang màu hồng dịu dàng. {guardian.ga_name} nhìn bạn với ánh mắt tràn đầy yêu thương, 'Ngài... ta cảm nhận được sự bình yên.' Lời nguyền tan biến, nhưng viên pha lê cũng trở thành một viên đá bình thường, tượng trưng cho tình yêu thuần khiết. Thế nhưng, {guardian.ga_name} đột nhiên gục ngã, vết nứt trên pha lê hóa ra đã lấy đi một phần sức mạnh của {guardian.ga_name} để đổi lấy sự bình yên. {guardian.ga_name} mỉm cười yếu ớt, 'Ta... ta yêu Ngài... đừng quên...'",
        choice_a="Ôm lấy {guardian.ga_name}, bạn cảm thấy trái tim mình vỡ vụn.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_guardian_sacrifice", "ending_guardian_sacrifice", "ending_guardian_sacrifice", "ending_guardian_sacrifice"),
        gold=1000, silver=5000, ga_exp=1000, dignity_point=100, ga_health=-1000, ga_mana=-1000, ga_stamina=-1000
    ),

    GuardianQuestLines(
        id="pull_guardian_away",
        title="Phản Ứng Bất Ngờ",
        description="Bạn kéo {guardian.ga_name} ra xa khỏi pha lê. Viên pha lê bỗng bùng lên ánh sáng đỏ rực, một luồng năng lượng tà ác bao trùm bạn và {guardian.ga_name}. {guardian.ga_name} ôm chặt bạn, cố gắng che chắn. 'Nó... nó đang tấn công chúng ta!' Viên pha lê vỡ tan, giải phóng toàn bộ năng lượng tà ác vào không khí. Vương quốc rơi vào bóng tối vĩnh viễn.",
        choice_a="Bạn và {guardian.ga_name} bị nuốt chửng bởi lời nguyền.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_eternal_darkness", "ending_eternal_darkness", "ending_eternal_darkness", "ending_eternal_darkness"),
        gold=0, silver=-1000, ga_exp=-500, dignity_point=-100, ga_health=-500, ga_mana=-500, ga_stamina=-500
    ),

    GuardianQuestLines(
        id="soothe_betrayed_soul_success",
        title="Linh Hồn Tìm Thấy Bình Yên",
        description="Bạn và {guardian.ga_name} đã thành công trấn an nỗi đau của vị pháp sư. Linh hồn ông ta dần trở nên thanh thản và tan biến vào hư không, mang theo lời nguyền. {guardian.ga_name} thở phào, 'Cuối cùng, ông ấy cũng tìm thấy sự bình yên.' Vương quốc thoát khỏi lời nguyền, nhưng một khoảng trống vẫn còn trong trái tim bạn.",
        choice_a="Bạn và {guardian.ga_name} trở về, vương quốc được cứu.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_bittersweet_peace", "ending_bittersweet_peace", "ending_bittersweet_peace", "ending_bittersweet_peace"),
        gold=500, silver=2000, ga_exp=200, dignity_point=50, ga_health=50, ga_mana=50, ga_stamina=50
    ),

    GuardianQuestLines(
        id="dissolve_curse_with_love",
        title="Sức Mạnh Tình Yêu Thật Sự",
        description="Bạn và {guardian.ga_name} cùng nhau tìm cách hòa giải lời nguyền bằng tình yêu và sự tha thứ. {guardian.ga_name} nhìn bạn với ánh mắt tin tưởng tuyệt đối, 'Ta tin rằng tình yêu của chúng ta đủ mạnh để phá tan mọi lời nguyền, Ngài.' Một luồng năng lượng ấm áp tỏa ra từ hai bạn, chạm đến tận cùng của lời nguyền. Lời nguyền dần tan biến, nhưng nó cũng mang theo một phần ký ức của {guardian.ga_name} về nỗi đau và sự mất mát trong quá khứ, khiến {guardian.ga_name} không còn nhớ rõ lý do vì sao bản thân lại là một Guardian của người.",
        choice_a="Lời nguyền được hóa giải, nhưng có một sự mất mát không thể bù đắp.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_love_erases_memories", "ending_love_erases_memories", "ending_love_erases_memories", "ending_love_erases_memories"),
        gold=800, silver=4000, ga_exp=800, dignity_point=80, ga_health=100, ga_mana=100, ga_stamina=100
    ),

    # Bad Endings
    GuardianQuestLines(
        id="guardian_urges_action",
        title="Sự Hối Thúc Vô Vọng",
        description="Bạn chần chừ quá lâu, {guardian.ga_name} nhìn bạn với vẻ thất vọng sâu sắc. 'Ngài... sự thiếu quyết đoán này sẽ hủy diệt tất cả.' Lời nguyền lan rộng, nhấn chìm vương quốc trong bóng tối. {guardian.ga_name} bị cuốn vào một cơn bão năng lượng tà ác và biến mất.",
        choice_a="Vương quốc sụp đổ, bạn mất đi {guardian.ga_name}.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_lost_guardian", "ending_lost_guardian", "ending_lost_guardian", "ending_lost_guardian"),
        gold=-100, silver=-500, ga_exp=-200, dignity_point=-50, ga_health=-100, ga_mana=-100, ga_stamina=-100
    ),

    GuardianQuestLines(
        id="guardian_urges_action_2",
        title="Gánh Nặng Thinh Lặng",
        description="Bạn chần chừ, không muốn đối mặt với sự phức tạp của câu chuyện. {guardian.ga_name} đứng lặng, ánh mắt chứa đầy nỗi buồn. 'Nếu Ngài không muốn tiếp tục, ta sẽ tự mình gánh chịu...'. Nhưng một mình {guardian.ga_name} không thể ngăn cản lời nguyền. Vương quốc dần chìm vào quên lãng.",
        choice_a="Bạn rút lui, {guardian.ga_name} đơn độc chiến đấu và thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_abandoned_kingdom", "ending_abandoned_kingdom", "ending_abandoned_kingdom", "ending_abandoned_kingdom"),
        gold=-50, silver=-200, ga_exp=-100, dignity_point=-20, ga_health=-50, ga_mana=-50, ga_stamina=-50
    ),

    GuardianQuestLines(
        id="retreat_complex_story",
        title="Nỗi Đau Vô Vọng",
        description="Bạn quyết định câu chuyện quá phức tạp và nguy hiểm. {guardian.ga_name} nhìn bạn với ánh mắt cầu xin, nhưng bạn đã quay lưng. Lời nguyền không được ngăn chặn, vương quốc dần bị biến thành một vương quốc của những linh hồn đau khổ. {guardian.ga_name} vẫn ở lại, cố gắng bảo vệ những gì còn sót lại, nhưng cuối cùng cũng chỉ là một bóng ma.",
        choice_a="Bạn rời đi, để lại {guardian.ga_name} và vương quốc chìm trong đau khổ.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_kingdom_of_sorrow", "ending_kingdom_of_sorrow", "ending_kingdom_of_sorrow", "ending_kingdom_of_sorrow"),
        gold=-150, silver=-700, ga_exp=-300, dignity_point=-70, ga_health=-150, ga_mana=-150, ga_stamina=-150
    ),

    GuardianQuestLines(
        id="army_fall_timeout",
        title="Biến Đổi Khủng Khiếp",
        description="Bạn chần chừ trong việc cứu những người lính. Lời nguyền nhanh chóng nuốt chửng toàn bộ quân đội, biến họ thành những sinh vật gớm ghiếc, tấn công bạn và {guardian.ga_name}. {guardian.ga_name} phải dùng toàn bộ sức lực để bảo vệ bạn, nhưng cuối cùng cả hai đều bị áp đảo. 'Ta... ta xin lỗi, Ngài...' {guardian.ga_name} thều thào trước khi gục xuống.",
        choice_a="Bạn và {guardian.ga_name} bị đánh bại bởi quân đội biến đổi.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_overwhelmed_by_curse", "ending_overwhelmed_by_curse", "ending_overwhelmed_by_curse", "ending_overwhelmed_by_curse"),
        gold=-200, silver=-800, ga_exp=-400, dignity_point=-80, ga_health=-200, ga_mana=-200, ga_stamina=-200
    ),

    GuardianQuestLines(
        id="seal_power_timeout",
        title="Sức Mạnh Bùng Phát",
        description="Bạn chần chừ trong việc phong ấn nguồn năng lượng. Viên pha lê bỗng nổ tung, giải phóng toàn bộ nỗi đau và thù hận của vị pháp sư vào không khí. {guardian.ga_name} bị cuốn đi trong luồng năng lượng đen tối, không thể cứu vãn. Vương quốc chìm trong hỗn loạn.",
        choice_a="Nguồn năng lượng bùng phát, {guardian.ga_name} biến mất.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_guardian_consumed", "ending_guardian_consumed", "ending_guardian_consumed", "ending_guardian_consumed"),
        gold=-150, silver=-600, ga_exp=-250, dignity_point=-60, ga_health=-150, ga_mana=-150, ga_stamina=-150
    ),

    GuardianQuestLines(
        id="retreat_from_crystal",
        title="Nỗi Sợ Hãi Chế Ngự",
        description="Bạn quyết định rời đi, quá sợ hãi trước sức mạnh của Viên Pha Lê Huyết Nguyệt. {guardian.ga_name} nhìn bạn với ánh mắt thất vọng. 'Ngài... chúng ta không thể bỏ cuộc lúc này.' Nhưng bạn đã quay lưng. Lời nguyền không được hóa giải, và ánh trăng đỏ vẫn tiếp tục bao trùm vương quốc, biến mọi thứ thành vô vọng.",
        choice_a="Bạn rút lui, để lời nguyền tiếp tục hoành hành.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_hopeless_kingdom", "ending_hopeless_kingdom", "ending_hopeless_kingdom", "ending_hopeless_kingdom"),
        gold=-100, silver=-400, ga_exp=-150, dignity_point=-40, ga_health=-100, ga_mana=-100, ga_stamina=-100
    ),

    GuardianQuestLines(
        id="crystal_overpower_timeout",
        title="Ánh Sáng Nuốt Chửng",
        description="Bạn chần chừ quá lâu trước Viên Pha Lê Huyết Nguyệt. Năng lượng của nó bùng phát mạnh mẽ, nuốt chửng bạn và {guardian.ga_name}. {guardian.ga_name} cố gắng nắm lấy tay bạn, nhưng sức mạnh đó quá lớn. 'Ngài... đừng quên... ta sẽ luôn ở bên Ngài...' Giọng nói của {guardian.ga_name} yếu dần rồi tắt hẳn.",
        choice_a="Bạn và {guardian.ga_name} bị viên pha lê nuốt chửng.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_crystal_consumes_all", "ending_crystal_consumes_all", "ending_crystal_consumes_all", "ending_crystal_consumes_all"),
        gold=-200, silver=-900, ga_exp=-450, dignity_point=-90, ga_health=-200, ga_mana=-200, ga_stamina=-200
    ),

    GuardianQuestLines(
        id="betrayed_love_timeout",
        title="Lòng Hận Thù Trường Tồn",
        description="Bạn chần chừ trong việc tìm kiếm cách hóa giải lời nguyền. Nỗi đau và sự thù hận của vị pháp sư vẫn tiếp tục lan tỏa, khiến vương quốc ngày càng chìm sâu vào bóng tối. {guardian.ga_name} cảm thấy bất lực, 'Ta... ta không thể làm gì nếu không có sự giúp đỡ của Ngài.'",
        choice_a="Lời nguyền trở nên vĩnh viễn, vương quốc mất hết hy vọng.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_eternal_hatred", "ending_eternal_hatred", "ending_eternal_hatred", "ending_eternal_hatred"),
        gold=-100, silver=-300, ga_exp=-100, dignity_point=-30, ga_health=-50, ga_mana=-50, ga_stamina=-50
    ),

    GuardianQuestLines(
        id="guardian_sacrifice_timeout",
        title="Hy Sinh Vô Vọng",
        description="{guardian.ga_name} cố gắng bảo vệ bạn khỏi sức mạnh của viên pha lê, đẩy bạn ra xa. Viên pha lê bùng nổ, và {guardian.ga_name} hứng chịu toàn bộ sức mạnh của nó. Một tiếng thét đau đớn vang lên, rồi tất cả chìm vào im lặng. {guardian.ga_name} biến mất, chỉ còn lại sự trống rỗng trong trái tim bạn.",
        choice_a="{guardian.ga_name} hy sinh để cứu bạn, nhưng lời nguyền vẫn còn đó.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_guardian_sacrifice_failed", "ending_guardian_sacrifice_failed", "ending_guardian_sacrifice_failed", "ending_guardian_sacrifice_failed"),
        gold=-300, silver=-1000, ga_exp=-500, dignity_point=-100, ga_health=-500, ga_mana=-500, ga_stamina=-500
    ),

    GuardianQuestLines(
        id="retreat_from_crystal_bad",
        title="Thoát Ly Trong Hoảng Loạn",
        description="Bạn hoảng sợ và vội vã rút lui khỏi hang động, bỏ lại Viên Pha Lê Huyết Nguyệt. {guardian.ga_name} cố gắng theo bạn, nhưng không thể. Sức mạnh của viên pha lê bắt đầu phá hủy mọi thứ xung quanh. Vương quốc bị nhấn chìm trong biển lửa và hỗn loạn. {guardian.ga_name} bị mắc kẹt, không thể thoát ra.",
        choice_a="Bạn thoát hiểm nhưng để lại {guardian.ga_name} và vương quốc chìm trong hoang tàn.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_kingdom_in_chaos", "ending_kingdom_in_chaos", "ending_kingdom_in_chaos", "ending_kingdom_in_chaos"),
        gold=-200, silver=-800, ga_exp=-400, dignity_point=-80, ga_health=-200, ga_mana=-200, ga_stamina=-200
    ),

    GuardianQuestLines(
        id="soul_anger_outcome",
        title="Cơn Thịnh Nộ Của Linh Hồn",
        description="Bạn chần chừ trong việc xoa dịu linh hồn. Nỗi đau của nó bùng phát thành cơn thịnh nộ dữ dội. Linh hồn tấn công bạn và {guardian.ga_name} bằng một sức mạnh khủng khiếp. {guardian.ga_name} phải dùng toàn bộ năng lượng để tạo ra một lá chắn, nhưng nó không đủ mạnh để ngăn cản sự cuồng nộ. Cả hai bạn bị thương nặng và phải rút lui trong đau đớn. Linh hồn vẫn còn đó, nỗi thù hận vẫn còn đó, và vương quốc vẫn chìm trong lời nguyền.",
        choice_a="Bạn và {guardian.ga_name} bị thương nặng và nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_injured_and_failed", "ending_injured_and_failed", "ending_injured_and_failed", "ending_injured_and_failed"),
        gold=-100, silver=-300, ga_exp=-100, dignity_point=-30, ga_health=-100, ga_mana=-100, ga_stamina=-100
    ),

    # Final Endings
    GuardianQuestLines(
        id="ending_guardian_sacrifice",
        title="Sự Hy Sinh Vô Điều Kiện",
        description="Bạn ôm chặt lấy {guardian.ga_name} khi hơi thở của cô ấy dần yếu đi. Nước mắt bạn rơi lã chã khi nhìn cô ấy tan biến thành những đốm sáng, mang theo tình yêu vĩnh cửu. Vương quốc được cứu, nhưng bạn đã mất đi người bạn đồng hành trung thành nhất, người đã yêu bạn hơn cả sinh mệnh của mình. Bạn biết, dù có thể xây dựng lại vương quốc, nhưng khoảng trống trong trái tim bạn sẽ không bao giờ được lấp đầy. Mỗi khi nhìn thấy ánh trăng đỏ, bạn lại nhớ về lời thề dưới ánh trăng, và sự hy sinh của {guardian.ga_name} - một tình yêu bất diệt. Bạn sống sót, nhưng với nỗi đau vĩnh cửu và sự mất mát không thể bù đắp. Cuộc phiêu lưu tiếp tục, nhưng nó sẽ không bao giờ giống như trước.",
        choice_a="Bạn sống sót, nhưng trái tim tan vỡ.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("", "", "", ""),
        gold=1000, silver=5000, ga_exp=1000, dignity_point=100, ga_health=0, ga_mana=0, ga_stamina=0
    ),

    GuardianQuestLines(
        id="ending_eternal_darkness",
        title="Bóng Tối Vĩnh Hằng",
        description="Khi viên pha lê vỡ tan, một làn sóng năng lượng tà ác quét qua vương quốc. Mọi thứ chìm vào bóng tối vĩnh hằng, và bạn cùng {guardian.ga_name} bị biến thành một phần của lời nguyền, mắc kẹt trong nỗi đau vô tận. Không có lối thoát, không có hy vọng. Bạn và {guardian.ga_name} chỉ còn là những tiếng than vãn vô vọng trong màn đêm bất tận, mãi mãi vĩnh viễn.",
        choice_a="Bạn và {guardian.ga_name} bị biến thành một phần của lời nguyền.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0, ga_health=0, ga_mana=0, ga_stamina=0
    ),

    GuardianQuestLines(
        id="ending_bittersweet_peace",
        title="Bình Yên Cay Đắng",
        description="Vương quốc thoát khỏi lời nguyền, nhưng linh hồn của vị pháp sư đã hoàn toàn tan biến, mang theo một phần lịch sử và nỗi đau. Bạn cảm thấy một sự nhẹ nhõm, nhưng cũng có một nỗi buồn man mác. {guardian.ga_name} đứng bên cạnh bạn, ánh mắt vẫn còn vương vấn nỗi buồn. 'Chúng ta đã cứu vương quốc, Ngài. Nhưng có những vết sẹo sẽ không bao giờ lành.' Bạn đã đạt được hòa bình, nhưng với cái giá là một phần nào đó của quá khứ đã mất, và một sự mất mát nhỏ trong trái tim {guardian.ga_name} khi phải chứng kiến nỗi đau của một linh hồn đã không thể siêu thoát. Cuộc phiêu lưu tiếp tục, nhưng với một chút trầm tư hơn.",
        choice_a="Vương quốc được cứu, nhưng có một chút nuối tiếc.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("", "", "", ""),
        gold=500, silver=2000, ga_exp=200, dignity_point=50, ga_health=50, ga_mana=50, ga_stamina=50
    ),

    GuardianQuestLines(
        id="ending_love_erases_memories",
        title="Tình Yêu Xóa Nhòa Ký Ức",
        description="Lời nguyền được hóa giải, vương quốc bình yên trở lại. Bạn nhìn {guardian.ga_name}, người bạn đồng hành đã cùng bạn trải qua bao sóng gió. Nhưng khi bạn cố gắng nhắc lại những kỷ niệm về hành trình, ánh mắt {guardian.ga_name} đầy bối rối. 'Ta... ta không nhớ rõ lắm, Ngài. Ta chỉ biết rằng ta luôn muốn ở bên Ngài.' Tình yêu của bạn đã quá mạnh mẽ, đến mức nó đã xóa đi những ký ức đau khổ của {guardian.ga_name} về quá khứ, bao gồm cả lý do tại sao {guardian.ga_name} là một Guardian của bạn. {guardian.ga_name} vẫn là người bạn đồng hành của bạn, nhưng một phần hồn của cô ấy đã mất đi vĩnh viễn. Bạn đã cứu vương quốc, nhưng phải chấp nhận sự thật rằng người mình yêu không còn nhớ về những gì đã khiến cô ấy trở thành chính mình.",
        choice_a="Vương quốc được cứu, nhưng {guardian.ga_name} mất đi ký ức.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("", "", "", ""),
        gold=800, silver=4000, ga_exp=800, dignity_point=80, ga_health=100, ga_mana=100, ga_stamina=100
    ),

    GuardianQuestLines(
        id="ending_lost_guardian",
        title="Người Bảo Hộ Biến Mất",
        description="Khi lời nguyền lan rộng, bạn chứng kiến {guardian.ga_name} bị cuốn vào vòng xoáy năng lượng đen tối, biến mất không dấu vết. Bạn sống sót, nhưng vương quốc đã sụp đổ, và bạn đã mất đi người bạn đồng hành thân thiết nhất. Mỗi ngày trôi qua là một nỗi đau khôn nguôi, và bạn mãi mãi bị ám ảnh bởi hình ảnh cuối cùng của {guardian.ga_name} trước khi cô ấy biến mất, một lời thề bị phá vỡ, một tình yêu không thể hoàn thành. Bạn là người sống sót duy nhất, nhưng bạn không còn là chính mình.",
        choice_a="Bạn sống sót, nhưng vương quốc sụp đổ và {guardian.ga_name} biến mất.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0, ga_health=0, ga_mana=0, ga_stamina=0
    ),

    GuardianQuestLines(
        id="ending_abandoned_kingdom",
        title="Vương Quốc Bị Bỏ Rơi",
        description="Bạn đã rút lui, để {guardian.ga_name} đơn độc chiến đấu với lời nguyền. Tuy nhiên, một mình cô ấy không thể ngăn cản sức mạnh tà ác. Vương quốc dần chìm vào bóng tối và quên lãng. Bạn sống với sự hối tiếc và cảm giác tội lỗi khi đã bỏ rơi người bạn đồng hành của mình. Bạn nghe những lời thì thầm về một Guardian dũng cảm đã hy sinh để bảo vệ một vương quốc đã bị lãng quên, và bạn biết rằng đó là {guardian.ga_name}, người đã chiến đấu đến hơi thở cuối cùng. Bạn sống, nhưng bạn đã mất đi tất cả những gì quý giá nhất.",
        choice_a="Bạn sống với sự hối tiếc và cảm giác tội lỗi.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0, ga_health=0, ga_mana=0, ga_stamina=0
    ),

    GuardianQuestLines(
        id="ending_kingdom_of_sorrow",
        title="Vương Quốc Của Nỗi Đau",
        description="Bạn đã quay lưng lại với câu chuyện phức tạp, để vương quốc chìm trong đau khổ. Những linh hồn bị mắc kẹt bởi lời nguyền ngày càng nhiều, và {guardian.ga_name} biến thành một bóng ma vĩnh viễn, bị giam cầm bởi nỗi đau của vương quốc, mãi mãi cố gắng bảo vệ một nơi đã không còn hy vọng. Bạn sống trong thế giới bên ngoài, nhưng linh hồn bạn mãi mãi bị ám ảnh bởi những tiếng than vãn và hình ảnh của {guardian.ga_name} bị xiềng xích bởi lời nguyền. Bạn sống, nhưng không bao giờ có được sự bình yên.",
        choice_a="Bạn sống, nhưng vương quốc và {guardian.ga_name} chìm trong đau khổ.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0, ga_health=0, ga_mana=0, ga_stamina=0
    ),

    GuardianQuestLines(
        id="ending_overwhelmed_by_curse",
        title="Bị Áp Đảo Bởi Lời Nguyền",
        description="Quân đội biến đổi thành những sinh vật gớm ghiếc, nuốt chửng bạn và {guardian.ga_name}. Bạn và {guardian.ga_name} bị biến thành những con rối vô hồn của lời nguyền, mãi mãi lang thang trong vương quốc đã sụp đổ. Không còn ký ức, không còn cảm xúc, chỉ còn là những vỏ bọc rỗng tuếch, mãi mãi bị giam cầm trong bóng tối vĩnh cửu. Mối tình giữa bạn và {guardian.ga_name} đã bị phá hủy bởi lời nguyền, không thể cứu vãn. Đó là một cái kết bi thảm cho tất cả.",
        choice_a="Bạn và {guardian.ga_name} bị biến thành con rối của lời nguyền.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0, ga_health=0, ga_mana=0, ga_stamina=0
    ),

    GuardianQuestLines(
        id="ending_guardian_consumed",
        title="Người Bảo Hộ Bị Nuốt Chửng",
        description="Nguồn năng lượng tà ác bùng phát, nuốt chửng {guardian.ga_name} trong ánh sáng đen tối. Bạn chứng kiến cảnh tượng kinh hoàng đó, không thể làm gì để cứu vãn. Bạn sống sót, nhưng với nỗi đau khôn cùng và cảm giác tội lỗi vì đã không thể bảo vệ người bạn đồng hành của mình. Lời nguyền vẫn còn đó, và bạn phải sống trong một vương quốc bị tàn phá, mãi mãi bị ám ảnh bởi hình ảnh {guardian.ga_name} bị nuốt chửng, và lời thề của cô ấy đã không thể hoàn thành. Bạn là người duy nhất còn lại, nhưng bạn đã mất đi tất cả.",
        choice_a="Bạn sống sót, nhưng {guardian.ga_name} bị nuốt chửng bởi lời nguyền.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0, ga_health=0, ga_mana=0, ga_stamina=0
    ),

    GuardianQuestLines(
        id="ending_hopeless_kingdom",
        title="Vương Quốc Vô Vọng",
        description="Bạn đã rút lui, để lời nguyền tiếp tục hoành hành. Ánh trăng đỏ vẫn tiếp tục bao trùm vương quốc, biến mọi thứ thành vô vọng. Bạn và {guardian.ga_name} sống sót, nhưng không còn hy vọng nào cho vương quốc. {guardian.ga_name} nhìn bạn với ánh mắt trống rỗng, và bạn biết rằng mình đã thất bại. Vương quốc mãi mãi chìm trong bóng tối, và bạn và {guardian.ga_name} phải sống trong sự tuyệt vọng, mãi mãi bị ám ảnh bởi sự bất lực của mình. Mối tình của hai bạn đã bị phai nhạt bởi sự tuyệt vọng.",
        choice_a="Bạn và {guardian.ga_name} sống sót, nhưng vương quốc mất hết hy vọng.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0, ga_health=0, ga_mana=0, ga_stamina=0
    ),

    GuardianQuestLines(
        id="ending_crystal_consumes_all",
        title="Pha Lê Nuốt Chửng Tất Cả",
        description="Năng lượng của Viên Pha Lê Huyết Nguyệt bùng phát, nuốt chửng bạn và {guardian.ga_name}. Bạn và {guardian.ga_name} trở thành một phần của viên pha lê, bị giam cầm trong một giấc mơ vĩnh cửu về nỗi đau và sự phản bội. Không có lối thoát, không có hy vọng. Bạn và {guardian.ga_name} mãi mãi bị mắc kẹt, cùng nhau chia sẻ một số phận bi thảm, tình yêu của hai bạn đã bị nuốt chửng bởi sức mạnh của lời nguyền, chỉ còn lại sự trống rỗng và hối tiếc.",
        choice_a="Bạn và {guardian.ga_name} bị viên pha lê nuốt chửng vĩnh viễn.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0, ga_health=0, ga_mana=0, ga_stamina=0
    ),

    GuardianQuestLines(
        id="ending_eternal_hatred",
        title="Thù Hận Vĩnh Cửu",
        description="Lời nguyền của vị pháp sư trở nên vĩnh viễn, không thể hóa giải. Vương quốc chìm trong bóng tối của lòng thù hận, không bao giờ có thể thoát ra. Bạn và {guardian.ga_name} sống sót, nhưng phải chứng kiến sự hủy diệt của vương quốc, và nỗi đau của những linh hồn bị giam cầm. {guardian.ga_name} nhìn bạn với ánh mắt đau khổ, và bạn biết rằng không có gì có thể thay đổi được số phận này. Tình yêu của hai bạn đã không đủ mạnh để chiến thắng sự thù hận, và bạn phải sống với nỗi ân hận vĩnh cửu.",
        choice_a="Bạn và {guardian.ga_name} sống sót, nhưng vương quốc chìm trong thù hận vĩnh cửu.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0, ga_health=0, ga_mana=0, ga_stamina=0
    ),

    GuardianQuestLines(
        id="ending_guardian_sacrifice_failed",
        title="Sự Hy Sinh Vô Nghĩa",
        description="{guardian.ga_name} đã hy sinh để cứu bạn, nhưng lời nguyền vẫn còn đó, không hề suy yếu. Vương quốc vẫn chìm trong bóng tối, và bạn phải sống với nỗi đau mất mát {guardian.ga_name}, và sự thật rằng sự hy sinh của cô ấy là vô nghĩa. Bạn mang theo nỗi ân hận và trái tim tan vỡ, không thể tìm thấy ý nghĩa trong cuộc sống mà {guardian.ga_name} đã đổi lấy. Mối tình của hai bạn đã kết thúc trong bi kịch, và bạn sẽ mãi mãi bị ám ảnh bởi sự hy sinh vô vọng ấy.",
        choice_a="Bạn sống sót, nhưng {guardian.ga_name} hy sinh vô nghĩa.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0, ga_health=0, ga_mana=0, ga_stamina=0
    ),

    GuardianQuestLines(
        id="ending_kingdom_in_chaos",
        title="Vương Quốc Hoang Tàn",
        description="Khi bạn hoảng loạn rút lui, Viên Pha Lê Huyết Nguyệt bùng nổ, phá hủy mọi thứ xung quanh. Vương quốc bị nhấn chìm trong biển lửa và hỗn loạn. {guardian.ga_name} bị mắc kẹt trong đống đổ nát, không thể thoát ra. Bạn sống sót, nhưng vương quốc của bạn đã bị hủy diệt, và {guardian.ga_name} đã mất tích trong biển lửa đó. Bạn sống với nỗi đau của sự mất mát, và hình ảnh {guardian.ga_name} bị mắc kẹt mãi mãi ám ảnh bạn. Tình yêu của hai bạn đã tan vỡ cùng với vương quốc. Bạn sống sót, nhưng vương quốc và {guardian.ga_name} chìm trong hoang tàn.",
        choice_a="",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0, ga_health=0, ga_mana=0, ga_stamina=0
    ),

    GuardianQuestLines(
        id="ending_injured_and_failed",
        title="Thất Bại Đau Đớn",
        description="Bạn và {guardian.ga_name} bị thương nặng, không thể tiếp tục nhiệm vụ. Linh hồn của vị pháp sư vẫn còn đó, giận dữ và đầy thù hận, và lời nguyền vẫn tiếp tục hoành hành. Bạn và {guardian.ga_name} phải rút lui trong đau đớn, mang theo nỗi thất bại và sự hối tiếc. Vương quốc vẫn chìm trong bóng tối, và bạn biết rằng mình đã không thể cứu vãn nó. Mối tình của hai bạn đã bị tổn thương bởi nỗi đau và sự thất bại, và bạn phải sống với sự thật rằng mình đã không đủ mạnh mẽ.",
        choice_a="",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0, ga_health=0, ga_mana=0, ga_stamina=0
    ),
]
#region quest_forgetten_garden
quest_forgetten_garden = [
    GuardianQuestLines(
        id="start",
        title="Tiếng Hát Từ Khu Vườn Bị Lãng Quên",
        description="Một giai điệu du dương, kỳ lạ vọng lại từ khu vườn cổ xưa, nơi mà ít ai dám bén mảng. {guardian.ga_name} khẽ nghiêng đầu, ánh mắt lấp lánh sự tò mò. 'Ta nghe thấy một giai điệu rất đẹp, Ngài. Nó như đang gọi mời ta vậy.'",
        choice_a="Đi vào khu vườn để tìm hiểu.",
        choice_b="Tìm hiểu về lịch sử khu vườn trước.",
        choice_c="Bỏ qua, có lẽ chỉ là gió thôi.",
        choice_timeout="{guardian.ga_name} nhìn bạn với ánh mắt thúc giục, 'Chúng ta không thể bỏ lỡ một giai điệu tuyệt vời như vậy, Ngài!'",
        next_steps=NextSteps(
            choice_a="enter_forgotten_garden",
            choice_b="research_garden_history",
            choice_c="ignore_garden_music_outcome",
            timeout="guardian_eager_timeout"
        ),
        gold=10, silver=100, ga_exp=10, dignity_point=5
    ),

    GuardianQuestLines(
        id="enter_forgotten_garden",
        title="Bước Chân Vào Vườn Cổ Tích",
        description="Bạn và {guardian.ga_name} bước vào khu vườn. Những bông hoa rực rỡ hiếm thấy đua nhau khoe sắc, và tiếng hát càng trở nên rõ ràng hơn, dẫn lối đến một giàn hoa hồng cổ. {guardian.ga_name} mỉm cười, 'Thật đẹp! Ngài có thấy nó giống như một câu chuyện cổ tích không?'",
        choice_a="Tìm hiểu ai đang hát.",
        choice_b="Ngắm nhìn những bông hoa.",
        choice_c="Kiểm tra xem có nguy hiểm nào không.",
        choice_timeout="{guardian.ga_name} thúc giục, 'Tiếng hát đang chờ chúng ta khám phá, Ngài!'",
        next_steps=NextSteps(
            choice_a="find_singer",
            choice_b="admire_flowers",
            choice_c="check_for_dangers",
            timeout="garden_beauty_timeout"
        )
    ),

    GuardianQuestLines(
        id="research_garden_history",
        title="Cuốn Sách Bụi Bặm",
        description="Bạn và {guardian.ga_name} đến thư viện địa phương. Một cuốn sách cũ kỹ kể về một nàng tiên hoa đã ban phước cho khu vườn này, nhưng sau đó biến mất vì một lời nguyền về sự cô đơn. Tiếng hát được cho là của nàng tiên hoa đang tìm kiếm một linh hồn đồng điệu. {guardian.ga_name} trầm tư, 'Ta mong nàng không quá cô đơn.'",
        choice_a="Tìm cách gặp nàng tiên hoa.",
        choice_b="Quay lại khu vườn để tìm hiểu thêm.",
        choice_c="Nhiệm vụ quá phức tạp, từ bỏ.",
        choice_timeout="{guardian.ga_name} nói, 'Chúng ta không có nhiều thời gian để do dự đâu!'",
        next_steps=NextSteps(
            choice_a="seek_flower_fairy",
            choice_b="enter_forgotten_garden",
            choice_c="abandon_fairy_quest",
            timeout="guardian_eager_timeout"
        )
    ),

    GuardianQuestLines(
        id="find_singer",
        title="Gặp Gỡ Linh Hồn Của Vườn",
        description="Bạn và {guardian.ga_name} đi theo tiếng hát đến một bụi hoa hồng trắng tinh khôi. Từ đó, một hình dáng lung linh, mờ ảo hiện ra. Đó là một cô gái với mái tóc dài như dòng suối và đôi mắt buồn bã, đang khẽ ngân nga. {guardian.ga_name} thì thầm, 'Nàng tiên hoa sao... nàng thật đẹp, nhưng cũng thật cô độc.'",
        choice_a="Chạm vào nàng tiên hoa.",
        choice_b="Cố gắng giao tiếp bằng lời nói.",
        choice_c="Quan sát từ xa để không làm kinh động.",
        choice_timeout="Nàng tiên hoa khẽ run rẩy, dường như nhận ra sự hiện diện của bạn và {guardian.ga_name}. 'Nàng đang lo sợ!' {guardian.ga_name} cảnh báo.",
        next_steps=NextSteps(
            choice_a="touch_flower_fairy",
            choice_b="talk_to_fairy",
            choice_c="observe_fairy_from_afar",
            timeout="fairy_scared_outcome"
        )
    ),

    GuardianQuestLines(
        id="admire_flowers",
        title="Sắc Màu Hạnh Phúc",
        description="Bạn và {guardian.ga_name} dạo quanh khu vườn, chiêm ngưỡng vẻ đẹp của những loài hoa kỳ lạ. {guardian.ga_name} hái một bông hoa đang nở rộ, cài lên tóc bạn. 'Chúng đẹp quá, Ngài. Giống như nụ cười của Ngài vậy.' Tiếng hát dường như hòa quyện vào không khí, làm khu vườn càng thêm sống động.",
        choice_a="Tìm hiểu nguồn gốc của tiếng hát.",
        choice_b="Tiếp tục ngắm hoa, tận hưởng khoảnh khắc.",
        choice_c="Kiểm tra xem có lối thoát nào không.",
        choice_timeout="{guardian.ga_name} khẽ nắm lấy tay bạn, 'Có lẽ chúng ta nên tìm hiểu thêm về giai điệu này, Ngài?'",
        next_steps=NextSteps(
            choice_a="find_singer",
            choice_b="linger_in_garden_outcome",
            choice_c="exit_garden_prematurely",
            timeout="garden_beauty_timeout"
        )
    ),

    GuardianQuestLines(
        id="seek_flower_fairy",
        title="Hành Trình Tìm Nàng Tiên",
        description="Bạn và {guardian.ga_name} trở lại khu vườn, mang theo những kiến thức về lời nguyền. Bạn cảm thấy có một sợi dây liên kết vô hình giữa mình và giai điệu buồn bã đó. {guardian.ga_name} nhìn bạn đầy trìu mến. 'Ngài dường như có một mối liên hệ đặc biệt với nàng tiên hoa này.'",
        choice_a="Đi sâu vào khu vườn tìm nàng tiên.",
        choice_b="Thử gọi nàng tiên bằng tên.",
        choice_c="Tìm cách hóa giải lời nguyền từ bên ngoài.",
        choice_timeout="{guardian.ga_name} thúc giục, 'Nàng tiên đang chờ chúng ta, Ngài!'",
        next_steps=NextSteps(
            choice_a="find_singer",
            choice_b="call_fairy_name",
            choice_c="seek_curse_solution_outside",
            timeout="guardian_eager_timeout"
        )
    ),

    # Choices leading to the ending
    GuardianQuestLines(
        id="touch_flower_fairy",
        title="Dòng Chảy Kết Nối",
        description="Bạn nhẹ nhàng chạm vào nàng tiên hoa. Một luồng sáng ấm áp truyền qua bạn, và bạn cảm nhận được nỗi cô đơn sâu thẳm của nàng, cùng với một tia hy vọng. {guardian.ga_name} nắm lấy tay bạn, năng lượng của cô ấy hòa quyện với bạn, tạo thành một luồng sáng mạnh mẽ hơn. 'Ngài... chúng ta có thể giúp nàng!'",
        choice_a="Cùng {guardian.ga_name} dùng tình cảm để xoa dịu nàng tiên.",
        choice_b="Rút tay lại, cảm thấy quá choáng ngợp.",
        choice_c="",
        choice_timeout="{guardian.ga_name} siết chặt tay bạn, 'Đừng sợ, Ngài! Chúng ta không đơn độc!'",
        next_steps=NextSteps(
            choice_a="soothe_fairy_with_affection",
            choice_b="overwhelmed_retreat_outcome",
            choice_c="",
            timeout="guardian_comfort_timeout"
        )
    ),

    GuardianQuestLines(
        id="talk_to_fairy",
        title="Lời Nói Từ Trái Tim",
        description="Bạn nhẹ nhàng nói chuyện với nàng tiên hoa, bày tỏ sự đồng cảm. Nàng tiên hoa lắng nghe, ánh mắt dịu đi. {guardian.ga_name} tiếp lời, kể về những cuộc phiêu lưu của hai bạn, về tình bạn, tình yêu và sự gắn kết. Nàng tiên hoa khẽ mỉm cười. 'Các người... thật khác biệt.'",
        choice_a="Tiếp tục chia sẻ về tình cảm giữa bạn và {guardian.ga_name}.",
        choice_b="Hỏi nàng tiên về nỗi cô đơn của nàng.",
        choice_c="Thử hát một bài hát cho nàng nghe.",
        choice_timeout="{guardian.ga_name} thì thầm, 'Nàng đang chờ đợi sự chân thành từ chúng ta, Ngài.'",
        next_steps=NextSteps(
            choice_a="share_our_bond",
            choice_b="ask_fairy_about_loneliness",
            choice_c="sing_to_fairy",
            timeout="fairy_waiting_timeout"
        )
    ),

    GuardianQuestLines(
        id="call_fairy_name",
        title="Tiếng Gọi Từ Trái Tim",
        description="Bạn và {guardian.ga_name} cùng gọi tên nàng tiên hoa. Một luồng ánh sáng ấm áp bao trùm khu vườn, và nàng tiên hoa hiện ra rõ ràng hơn, ánh mắt không còn buồn bã nữa. {guardian.ga_name} mỉm cười rạng rỡ, 'Nàng đã nghe thấy chúng ta, Ngài! Nàng đang đến gần hơn rồi!'",
        choice_a="Tiếp cận nàng tiên hoa và bày tỏ sự quan tâm.",
        choice_b="Cố gắng tìm kiếm một cổ vật giúp hóa giải lời nguyền.",
        choice_c="",
        choice_timeout="{guardian.ga_name} nắm lấy tay bạn, 'Chúng ta đã tạo ra một sự kết nối, Ngài!'",
        next_steps=NextSteps(
            choice_a="talk_to_fairy",
            choice_b="search_for_artifact_for_curse",
            choice_c="",
            timeout="fairy_approaches_timeout"
        )
    ),

    GuardianQuestLines(
        id="soothe_fairy_with_affection",
        title="Giai Điệu Của Tình Yêu",
        description="Bạn và {guardian.ga_name} cùng nhau hướng năng lượng yêu thương và sự ấm áp vào nàng tiên hoa. Nàng tiên hoa dần tan biến vào một luồng ánh sáng rực rỡ, nhưng không phải biến mất, mà là trở thành một phần của khu vườn, mang theo sự bình yên và những lời chúc phúc. {guardian.ga_name} ôm chặt bạn, 'Ngài... chúng ta đã giúp nàng tìm thấy sự bình yên, và ta... ta cũng tìm thấy điều đó bên Ngài.' Khu vườn bừng sáng, và tình cảm giữa bạn và {guardian.ga_name} càng thêm sâu sắc.",
        choice_a="Cảm nhận sự bình yên và hạnh phúc.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_garden_of_love", "ending_garden_of_love", "ending_garden_of_love", "ending_garden_of_love"),
        gold=500, silver=2500, ga_exp=250, dignity_point=50, ga_health=50, ga_mana=50, ga_stamina=50
    ),

    GuardianQuestLines(
        id="share_our_bond",
        title="Câu Chuyện Của Chúng Ta",
        description="Bạn và {guardian.ga_name} cùng nhau kể về những kỷ niệm, những thử thách đã vượt qua và tình cảm sâu đậm giữa hai người. Nàng tiên hoa lắng nghe, ánh mắt nàng lấp lánh như những giọt sương. Nàng tiên hoa đột nhiên khẽ cười, một nụ cười rạng rỡ như ánh bình minh, và một luồng sáng bao trùm lấy bạn và {guardian.ga_name}. Nàng tiên hoa đã hóa giải lời nguyền cô đơn, không phải bằng cách tự giải thoát, mà bằng cách nhận ra tình yêu đích thực giữa bạn và {guardian.ga_name} chính là chìa khóa. Nàng trao cho hai bạn một món quà: khả năng cảm nhận và chia sẻ cảm xúc một cách sâu sắc hơn nữa với nhau, nhưng điều đó cũng có nghĩa là bạn và {guardian.ga_name} sẽ mãi mãi gắn kết, không thể rời xa dù chỉ một bước chân. {guardian.ga_name} nhìn bạn, ánh mắt vừa hạnh phúc vừa có chút bối rối. 'Ta... ta sẽ không bao giờ rời xa Ngài, dù chỉ một khoảnh khắc.'",
        choice_a="Bạn và {guardian.ga_name} mãi mãi gắn kết, không thể tách rời.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_eternal_bond", "ending_eternal_bond", "ending_eternal_bond", "ending_eternal_bond"),
        gold=700, silver=3000, ga_exp=300, dignity_point=70, ga_health=0, ga_mana=0, ga_stamina=0
    ),

    GuardianQuestLines(
        id="ask_fairy_about_loneliness",
        title="Chia Sẻ Nỗi Cô Đơn",
        description="Bạn hỏi nàng tiên hoa về nỗi cô đơn của nàng. Nàng tiên hoa chầm chậm kể về một câu chuyện tình yêu dang dở, về một tình yêu đã bị định mệnh chia cắt, khiến nàng phải chịu lời nguyền cô đơn. {guardian.ga_name} nắm lấy tay bạn, 'Ta hiểu cảm giác đó... nỗi đau khi không thể ở bên người mình yêu.' Nàng tiên hoa nhìn {guardian.ga_name} với ánh mắt đầy cảm thông, rồi quay sang bạn. 'Có lẽ... các người có thể hiểu.'",
        choice_a="Cố gắng tìm cách hàn gắn quá khứ của nàng tiên hoa.",
        choice_b="Cùng {guardian.ga_name} an ủi nàng.",
        choice_c="Tìm cách hóa giải lời nguyền.",
        choice_timeout="{guardian.ga_name} nói, 'Nàng đang cần sự đồng cảm của chúng ta, Ngài.'",
        next_steps=NextSteps(
            choice_a="heal_fairy_past",
            choice_b="soothe_fairy_with_affection",
            choice_c="seek_curse_solution_outside",
            timeout="fairy_despair_timeout"
        )
    ),

    GuardianQuestLines(
        id="heal_fairy_past",
        title="Hàn Gắn Vết Thương Xưa",
        description="Bạn và {guardian.ga_name} cùng nhau tìm hiểu về câu chuyện tình yêu dang dở của nàng tiên hoa. Bạn phát hiện ra rằng người nàng yêu đã hóa thân vào một loài hoa hiếm trong khu vườn, chờ đợi ngày nàng trở lại. {guardian.ga_name} nhìn bạn, 'Có lẽ chúng ta có thể giúp họ đoàn tụ, Ngài.' Cùng với {guardian.ga_name}, bạn thực hiện một nghi lễ để hóa giải lời nguyền, giúp nàng tiên hoa và người yêu cô ấy đoàn tụ. Nàng tiên hoa ôm lấy bạn và {guardian.ga_name} trong một luồng ánh sáng rực rỡ, rồi cùng người yêu tan biến vào không trung, mang theo sự bình yên và niềm hạnh phúc. Khu vườn tràn ngập hương thơm và ánh sáng. Tuy nhiên, khi họ biến mất, một phần nhỏ ký ức về tình yêu giữa bạn và {guardian.ga_name} cũng bị cuốn đi, giống như một cái giá để đổi lấy hạnh phúc cho họ. {guardian.ga_name} nhìn bạn với ánh mắt lạ lẫm. 'Ngài... chúng ta đã làm gì thế này?'",
        choice_a="Bạn và {guardian.ga_name} đã giúp họ, nhưng mất đi một phần ký ức về nhau.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_love_sacrifice_memories", "ending_love_sacrifice_memories", "ending_love_sacrifice_memories", "ending_love_sacrifice_memories"),
        gold=600, silver=2800, ga_exp=280, dignity_point=60, ga_health=-50, ga_mana=-50, ga_stamina=-50
    ),

    # Bad Endings
    GuardianQuestLines(
        id="ignore_garden_music_outcome",
        title="Giai Điệu Mờ Dần",
        description="Bạn quyết định bỏ qua tiếng hát. Vài ngày sau, khu vườn trở nên héo úa và tàn tạ, không còn vẻ đẹp như trước. {guardian.ga_name} nhìn bạn với vẻ buồn bã, 'Giai điệu đã tắt rồi, Ngài. Có lẽ chúng ta đã bỏ lỡ một điều gì đó quan trọng.'",
        choice_a="Cảm thấy hối tiếc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_faded_melody", "ending_faded_melody", "ending_faded_melody", "ending_faded_melody"),
        gold=-20, silver=-150, ga_exp=-70, dignity_point=-10
    ),

    GuardianQuestLines(
        id="guardian_eager_timeout",
        title="Ánh Mắt Thất Vọng",
        description="Bạn chần chừ quá lâu, {guardian.ga_name} lắc đầu thất vọng. 'Chúng ta không thể giúp nàng nếu cứ đứng đây!' Nhiệm vụ kết thúc vì sự thiếu quyết đoán của bạn.",
        choice_a="Cảm thấy bất lực. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_missed_opportunity", "ending_missed_opportunity", "ending_missed_opportunity", "ending_missed_opportunity"),
        gold=-30, silver=-200, ga_exp=-100, dignity_point=-15
    ),

    GuardianQuestLines(
        id="garden_beauty_timeout",
        title="Vẻ Đẹp Tan Biến",
        description="Bạn và {guardian.ga_name} chần chừ. Tiếng hát dần tắt, và vẻ đẹp của khu vườn cũng phai nhạt. Những bông hoa héo úa, và không khí trở nên u ám. {guardian.ga_name} thở dài buồn bã. 'Thật đáng tiếc. Vẻ đẹp này đã không thể kéo dài.'",
        choice_a="Cảm thấy nuối tiếc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_fading_beauty", "ending_fading_beauty", "ending_fading_beauty", "ending_fading_beauty"),
        gold=-25, silver=-180, ga_exp=-80, dignity_point=-12
    ),

    GuardianQuestLines(
        id="check_for_dangers",
        title="Cạm Bẫy Vô Hình",
        description="Bạn và {guardian.ga_name} cẩn thận kiểm tra khu vườn. Bạn phát hiện ra một cái bẫy vô hình do thời gian tạo ra. Trong lúc vô hiệu hóa bẫy, bạn vô tình làm tổn thương một vài bông hoa quý hiếm. Tiếng hát ngưng bặt. {guardian.ga_name} nhìn bạn lo lắng. 'Có lẽ chúng ta đã làm kinh động đến nàng.'",
        choice_a="Bạn gây ra hậu quả không mong muốn. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_unintended_consequences", "ending_unintended_consequences", "ending_unintended_consequences", "ending_unintended_consequences"),
        gold=-10, silver=-50, ga_exp=-30, dignity_point=-5
    ),

    GuardianQuestLines(
        id="abandon_fairy_quest",
        title="Từ Bỏ Hy Vọng",
        description="Bạn quyết định rằng nhiệm vụ này quá phức tạp. {guardian.ga_name} nhìn bạn với ánh mắt đầy thất vọng. 'Ta hy vọng nàng tiên hoa có thể tìm thấy sự bình yên theo một cách nào đó.' Khu vườn vẫn ở đó, nhưng tiếng hát đã không còn, và không ai còn nhắc đến nó nữa.",
        choice_a="Từ bỏ nhiệm vụ và cảm thấy một chút hối tiếc.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_abandoned_hope", "ending_abandoned_hope", "ending_abandoned_hope", "ending_abandoned_hope"),
        gold=-50, silver=-300, ga_exp=-150, dignity_point=-25
    ),

    GuardianQuestLines(
        id="fairy_scared_outcome",
        title="Sự Sợ Hãi Chế Ngự",
        description="Bạn chần chừ. Nàng tiên hoa trở nên hoảng sợ và tan biến vào hư không, không còn dấu vết. {guardian.ga_name} thở dài buồn bã. 'Nàng đã quá sợ hãi. Chúng ta không thể cứu vãn.'",
        choice_a="Nàng tiên hoa biến mất. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_frightened_fairy", "ending_frightened_fairy", "ending_frightened_fairy", "ending_frightened_fairy"),
        gold=-30, silver=-150, ga_exp=-50, dignity_point=-10
    ),

    GuardianQuestLines(
        id="linger_in_garden_outcome",
        title="Lạc Lối Trong Vẻ Đẹp",
        description="Bạn và {guardian.ga_name} tiếp tục ngắm hoa, bị cuốn hút bởi vẻ đẹp của khu vườn mà quên đi mục đích ban đầu. Tiếng hát dần tắt, và bạn nhận ra mình đã lãng phí thời gian. {guardian.ga_name} khẽ thở dài, 'Chúng ta đã quá mải mê với vẻ đẹp này, Ngài.'",
        choice_a="Bạn chìm đắm trong vẻ đẹp và bỏ lỡ cơ hội. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_lost_in_beauty", "ending_lost_in_beauty", "ending_lost_in_beauty", "ending_lost_in_beauty"),
        gold=-20, silver=-100, ga_exp=-40, dignity_point=-8
    ),

    GuardianQuestLines(
        id="exit_garden_prematurely",
        title="Rời Đi Sớm",
        description="Bạn quyết định rời khỏi khu vườn mà không khám phá hết. {guardian.ga_name} nhìn bạn với ánh mắt bối rối, 'Ngài... chúng ta đã bỏ lỡ điều gì đó phải không?' Khu vườn dần trở nên héo úa một lần nữa sau khi bạn rời đi.",
        choice_a="Bạn rời đi và nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_premature_exit", "ending_premature_exit", "ending_premature_exit", "ending_premature_exit"),
        gold=-20, silver=-100, ga_exp=-50, dignity_point=-10
    ),

    GuardianQuestLines(
        id="seek_curse_solution_outside",
        title="Tìm Kiếm Vô Vọng",
        description="Bạn và {guardian.ga_name} cố gắng tìm kiếm cách hóa giải lời nguyền từ bên ngoài khu vườn. Tuy nhiên, lời nguyền chỉ có thể được hóa giải bởi chính nàng tiên hoa hoặc qua sự kết nối tâm linh. Bạn và {guardian.ga_name} không thể tìm thấy bất kỳ giải pháp nào. {guardian.ga_name} nói, 'Có lẽ chúng ta đã tìm sai cách, Ngài.'",
        choice_a="Nhiệm vụ thất bại vì không tìm được giải pháp.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_fruitless_search", "ending_fruitless_search", "ending_fruitless_search", "ending_fruitless_search"),
        gold=-30, silver=-150, ga_exp=-80, dignity_point=-12
    ),

    GuardianQuestLines(
        id="overwhelmed_retreat_outcome",
        title="Quá Sức Chịu Đựng",
        description="Bạn rút tay lại, cảm thấy quá choáng ngợp bởi nỗi cô đơn của nàng tiên hoa. Nàng tiên hoa khẽ rùng mình và tan biến. {guardian.ga_name} nhìn bạn với vẻ lo lắng, 'Ngài ổn chứ? Nàng ấy... đã biến mất rồi.'",
        choice_a="Bạn rút lui vì bị choáng ngợp. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_overwhelmed_failure", "ending_overwhelmed_failure", "ending_overwhelmed_failure", "ending_overwhelmed_failure"),
        gold=-25, silver=-120, ga_exp=-60, dignity_point=-10
    ),

    GuardianQuestLines(
        id="guardian_comfort_timeout",
        title="Sự Hỗ Trợ Không Đủ",
        description="{guardian.ga_name} cố gắng an ủi bạn, nhưng bạn đã chần chừ quá lâu. Nàng tiên hoa cảm thấy bị bỏ rơi và tan biến hoàn toàn. {guardian.ga_name} thở dài. 'Đã quá muộn rồi.'",
        choice_a="Nàng tiên hoa biến mất. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_too_late", "ending_too_late", "ending_too_late", "ending_too_late"),
        gold=-30, silver=-180, ga_exp=-70, dignity_point=-15
    ),

    GuardianQuestLines(
        id="fairy_waiting_timeout",
        title="Sự Chờ Đợi Vô Vọng",
        description="Bạn chần chừ trong việc chia sẻ. Nàng tiên hoa cảm thấy mất hy vọng và dần mờ đi. {guardian.ga_name} buồn bã nói, 'Nàng ấy... đã không còn chờ đợi chúng ta nữa.'",
        choice_a="Nàng tiên hoa biến mất. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_lost_hope_fairy", "ending_lost_hope_fairy", "ending_lost_hope_fairy", "ending_lost_hope_fairy"),
        gold=-25, silver=-150, ga_exp=-60, dignity_point=-12
    ),

    GuardianQuestLines(
        id="fairy_approaches_timeout",
        title="Khoảng Cách Không Thể Rút Ngắn",
        description="Bạn chần chừ. Nàng tiên hoa, mặc dù đã đến gần, nhưng không thể vượt qua khoảng cách vô hình giữa bạn và nàng. Nàng thở dài, rồi dần dần mờ đi. {guardian.ga_name} nhìn bạn với ánh mắt tiếc nuối, 'Thật đáng tiếc, Ngài. Chúng ta đã gần lắm rồi.'",
        choice_a="Bạn bỏ lỡ cơ hội. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_missed_connection", "ending_missed_connection", "ending_missed_connection", "ending_missed_connection"),
        gold=-30, silver=-160, ga_exp=-75, dignity_point=-13
    ),

    GuardianQuestLines(
        id="search_for_artifact_for_curse",
        title="Tìm Kiếm Vô Vọng",
        description="Bạn và {guardian.ga_name} cố gắng tìm kiếm một cổ vật để hóa giải lời nguyền của nàng tiên hoa. Tuy nhiên, lời nguyền này không thể được hóa giải bằng vật chất, mà bằng cảm xúc. Bạn và {guardian.ga_name} không thể tìm thấy bất kỳ cổ vật nào có ích. {guardian.ga_name} nói, 'Có lẽ chúng ta đã lầm, Ngài.'",
        choice_a="Nhiệm vụ thất bại vì tìm sai hướng.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_fruitless_search_again", "ending_fruitless_search_again", "ending_fruitless_search_again", "ending_fruitless_search_again"),
        gold=-20, silver=-100, ga_exp=-50, dignity_point=-8
    ),

    GuardianQuestLines(
        id="fairy_despair_timeout",
        title="Nỗi Tuyệt Vọng Sâu Thẳm",
        description="Bạn chần chừ. Nỗi tuyệt vọng của nàng tiên hoa trở nên quá lớn, và nàng hoàn toàn tan biến, mang theo cả linh hồn của khu vườn. Khu vườn giờ đây trở nên hoang tàn, một vùng đất chết. {guardian.ga_name} gục đầu, 'Ta... ta đã không thể làm gì.'",
        choice_a="Nàng tiên hoa biến mất, khu vườn chết. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("ending_garden_of_despair", "ending_garden_of_despair", "ending_garden_of_despair", "ending_garden_of_despair"),
        gold=-50, silver=-250, ga_exp=-120, dignity_point=-20
    ),

    # Final Endings
    GuardianQuestLines(
        id="ending_garden_of_love",
        title="Khu Vườn Của Tình Yêu",
        description="Khu vườn bị lãng quên giờ đây tràn ngập sức sống và ánh sáng. Tiếng hát của nàng tiên hoa không còn buồn bã nữa, mà trở thành một giai điệu vui tươi, hòa quyện với tiếng cười của bạn và {guardian.ga_name}. Nàng tiên hoa đã tìm thấy sự bình yên, trở thành một phần của khu vườn, mãi mãi ban phước cho nơi đây. Mỗi khi bạn và {guardian.ga_name} dạo bước trong khu vườn, bạn cảm nhận được sự kết nối sâu sắc hơn, tình yêu của hai bạn đã nở rộ cùng với những bông hoa. Đây là một kết thúc ngọt ngào, nơi tình yêu và sự thấu hiểu đã chiến thắng nỗi cô đơn, mang lại hạnh phúc cho tất cả. Cuộc phiêu lưu tiếp tục, nhưng giờ đây mỗi bước chân đều nhẹ nhàng và tràn ngập tình yêu.",
        choice_a="Khu vườn tràn ngập tình yêu, bạn và {guardian.ga_name} hạnh phúc.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("generic_ending", "", "", ""),
        gold=500, silver=2500, ga_exp=250, dignity_point=50
    ),

    GuardianQuestLines(
        id="ending_eternal_bond",
        title="Mối Nối Vĩnh Cửu",
        description="Khu vườn bừng sáng, nàng tiên hoa đã ban phước cho bạn và {guardian.ga_name} một món quà: một mối liên kết vĩnh cửu, sâu sắc đến mức hai bạn không thể rời xa nhau. Mỗi cảm xúc, mỗi suy nghĩ của bạn đều được {guardian.ga_name} cảm nhận, và ngược lại. {guardian.ga_name} nhìn bạn với ánh mắt vừa hạnh phúc vừa có chút bối rối. 'Ta... ta sẽ không bao giờ rời xa Ngài, dù chỉ một khoảnh khắc. Điều này... thật tuyệt vời, nhưng cũng thật kỳ lạ.' Bạn và {guardian.ga_name} giờ đây là một thể thống nhất, một tình yêu không thể phá vỡ. Đây là một kết thúc độc đáo, nơi tình yêu của bạn và {guardian.ga_name} đã vượt qua mọi giới hạn, nhưng cũng mang theo một cái giá: sự tự do cá nhân đã mất đi. Cuộc phiêu lưu tiếp tục, nhưng mỗi khoảnh khắc đều có {guardian.ga_name} bên cạnh bạn, mãi mãi.",
        choice_a="Bạn và {guardian.ga_name} mãi mãi gắn kết, không thể tách rời.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("generic_ending", "", "", ""),
        gold=700, silver=3000, ga_exp=300, dignity_point=70
    ),

    GuardianQuestLines(
        id="ending_love_sacrifice_memories",
        title="Tình Yêu Đổi Lấy Ký Ức",
        description="Nàng tiên hoa và người yêu nàng đã đoàn tụ, khu vườn tràn ngập niềm hạnh phúc. Tuy nhiên, khi họ tan biến, một phần nhỏ ký ức về tình yêu giữa bạn và {guardian.ga_name} cũng bị cuốn đi. {guardian.ga_name} nhìn bạn với ánh mắt lạ lẫm, 'Ngài... chúng ta đã làm gì thế này? Tại sao ta lại ở đây cùng Ngài?' Bạn đã cứu vương quốc, nhưng phải chấp nhận một cái giá đau lòng: tình yêu của bạn và {guardian.ga_name} đã phải hy sinh một phần ký ức để đổi lấy hạnh phúc cho người khác. Mối quan hệ của bạn và {guardian.ga_name} giờ đây là một tờ giấy trắng, và bạn phải bắt đầu lại từ đầu, cố gắng xây dựng lại những kỷ niệm và tình cảm đã mất. Đó là một cái kết bi thảm, nơi bạn phải đối mặt với một tình yêu bị lãng quên.",
        choice_a="Bạn và {guardian.ga_name} mất đi ký ức về tình yêu của mình.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("generic_ending", "", "", ""),
        gold=600, silver=2800, ga_exp=280, dignity_point=60
    ),

    # Final Bad Endings
    GuardianQuestLines(
        id="ending_faded_melody",
        title="Giai Điệu Tắt Lịm",
        description="Khi bạn bỏ qua tiếng hát, khu vườn dần héo úa và chết đi. Tiếng hát của nàng tiên hoa đã tắt hẳn, và không còn ai nhớ đến nàng nữa. {guardian.ga_name} đứng bên cạnh bạn, ánh mắt u buồn. 'Chúng ta đã có cơ hội, nhưng chúng ta đã bỏ lỡ.' Nàng tiên hoa biến mất mãi mãi, và khu vườn chỉ còn là một đống đổ nát, tượng trưng cho sự thờ ơ của bạn. Cuộc phiêu lưu tiếp tục, nhưng với một nỗi ân hận sâu sắc.",
        choice_a="Khu vườn héo úa, nàng tiên hoa biến mất.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("generic_ending", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0
    ),

    GuardianQuestLines(
        id="ending_missed_opportunity",
        title="Cơ Hội Bị Bỏ Lỡ",
        description="Sự thiếu quyết đoán của bạn đã khiến cơ hội cứu nàng tiên hoa trôi qua. {guardian.ga_name} nhìn bạn với ánh mắt thất vọng, 'Ta đã tin rằng Ngài sẽ làm điều đúng đắn.' Nàng tiên hoa biến mất, không để lại dấu vết, và khu vườn trở nên hoang tàn, không còn tiếng hát. Bạn sống với sự hối tiếc vì đã không hành động khi có thể, và {guardian.ga_name} phải chịu đựng nỗi buồn vì sự bất lực của bạn. Cuộc phiêu lưu tiếp tục, nhưng nó đã mất đi một phần ý nghĩa.",
        choice_a="Nhiệm vụ thất bại, bạn hối tiếc.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("generic_ending", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0
    ),

    GuardianQuestLines(
        id="ending_fading_beauty",
        title="Vẻ Đẹp Phai Tàn",
        description="Vẻ đẹp của khu vườn và tiếng hát của nàng tiên hoa dần phai nhạt, không còn ai nhớ đến. {guardian.ga_name} nhìn bạn với ánh mắt buồn bã, 'Đáng lẽ chúng ta đã có thể cứu vãn điều này.' Nàng tiên hoa tan biến vào hư không, và khu vườn trở thành một nơi hoang vắng, chỉ còn lại những ký ức về một vẻ đẹp đã mất. Bạn và {guardian.ga_name} phải sống với sự thật rằng bạn đã bỏ lỡ một vẻ đẹp và một linh hồn đang cần được giúp đỡ. Cuộc phiêu lưu tiếp tục, nhưng với một khoảng trống trong lòng.",
        choice_a="Vẻ đẹp phai tàn, nàng tiên hoa biến mất.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("generic_ending", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0
    ),

    GuardianQuestLines(
        id="ending_unintended_consequences",
        title="Hậu Quả Không Mong Muốn",
        description="Hành động của bạn đã vô tình làm tổn thương nàng tiên hoa, khiến tiếng hát của nàng tắt hẳn và nàng biến mất. {guardian.ga_name} nhìn bạn với ánh mắt đau đớn. 'Ngài... ta không nghĩ đây là điều chúng ta mong muốn.' Khu vườn giờ đây chỉ còn là một nơi đầy rẫy những bông hoa bị tàn phá, một lời nhắc nhở về sai lầm của bạn. Bạn sống với nỗi ân hận và cảm giác tội lỗi, và {guardian.ga_name} phải chịu đựng sự đau khổ vì hành động của bạn. Cuộc phiêu lưu tiếp tục, nhưng với một gánh nặng trong tâm trí.",
        choice_a="Bạn gây ra hậu quả không mong muốn, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("generic_ending", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0
    ),

    GuardianQuestLines(
        id="ending_abandoned_hope",
        title="Hy Vọng Bị Bỏ Rơi",
        description="Bạn đã từ bỏ nhiệm vụ, để nàng tiên hoa chìm trong cô đơn và biến mất vĩnh viễn. {guardian.ga_name} nhìn bạn với ánh mắt thất vọng sâu sắc. 'Có lẽ nàng tiên hoa đã không còn hy vọng nào nữa.' Khu vườn trở thành một nơi bị lãng quên, không còn ai nhắc đến câu chuyện về nàng tiên hoa. Bạn sống với sự hối tiếc và cảm giác tội lỗi, và {guardian.ga_name} phải chịu đựng nỗi buồn vì sự thờ ơ của bạn. Cuộc phiêu lưu tiếp tục, nhưng với một vết sẹo không thể lành.",
        choice_a="Bạn từ bỏ nhiệm vụ, nàng tiên hoa biến mất.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("generic_ending", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0
    ),

    GuardianQuestLines(
        id="ending_frightened_fairy",
        title="Nàng Tiên Hoảng Sợ",
        description="Nàng tiên hoa đã quá sợ hãi và tan biến mãi mãi. {guardian.ga_name} thở dài, 'Chúng ta đã không thể xoa dịu nỗi sợ hãi của nàng.' Khu vườn trở nên trống rỗng, không còn sự sống. Bạn sống với nỗi ân hận vì đã không thể làm gì để giúp nàng, và {guardian.ga_name} phải chịu đựng sự buồn bã vì sự mất mát đó. Cuộc phiêu lưu tiếp tục, nhưng với một nỗi tiếc nuối.",
        choice_a="Nàng tiên hoa biến mất vì sợ hãi.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("generic_ending", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0
    ),

    GuardianQuestLines(
        id="ending_lost_in_beauty",
        title="Lạc Lối Trong Vẻ Đẹp",
        description="Bạn và {guardian.ga_name} quá mải mê với vẻ đẹp của khu vườn mà quên đi mục đích ban đầu. Tiếng hát tắt, và nàng tiên hoa biến mất. {guardian.ga_name} nhìn bạn với ánh mắt thất vọng. 'Chúng ta đã bỏ lỡ điều quan trọng nhất.' Khu vườn vẫn đẹp, nhưng giờ đây chỉ là một vỏ bọc rỗng tuếch, không còn linh hồn. Bạn sống với nỗi ân hận vì đã bị vẻ đẹp bên ngoài làm mờ mắt, và {guardian.ga_name} phải chịu đựng nỗi buồn vì sự lãng phí cơ hội. Cuộc phiêu lưu tiếp tục, nhưng với một bài học đau đớn.",
        choice_a="Bạn chìm đắm trong vẻ đẹp và bỏ lỡ cơ hội.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("generic_ending", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0
    ),

    GuardianQuestLines(
        id="ending_premature_exit",
        title="Rời Đi Vô Nghĩa",
        description="Bạn quyết định rời khỏi khu vườn sớm, bỏ lại nàng tiên hoa. {guardian.ga_name} nhìn bạn với ánh mắt buồn bã. 'Có lẽ nàng đã cần chúng ta hơn thế.' Khu vườn héo úa và nàng tiên hoa biến mất. Bạn sống với nỗi ân hận vì đã không hoàn thành nhiệm vụ, và {guardian.ga_name} phải chịu đựng sự buồn bã vì sự từ bỏ của bạn. Cuộc phiêu lưu tiếp tục, nhưng với một sự thất bại.",
        choice_a="Bạn rời đi, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("generic_ending", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0
    ),

    GuardianQuestLines(
        id="ending_fruitless_search",
        title="Tìm Kiếm Vô Vọng",
        description="Bạn và {guardian.ga_name} không thể tìm thấy cách hóa giải lời nguyền từ bên ngoài. Nàng tiên hoa biến mất trong cô đơn, và khu vườn trở nên hoang tàn. {guardian.ga_name} nhìn bạn với ánh mắt mệt mỏi. 'Chúng ta đã cố gắng, nhưng không đủ.' Bạn sống với nỗi ân hận vì đã không tìm được giải pháp, và {guardian.ga_name} phải chịu đựng sự buồn bã vì sự bất lực. Cuộc phiêu lưu tiếp tục, nhưng với một thất bại không thể tránh khỏi.",
        choice_a="Nhiệm vụ thất bại vì không tìm được giải pháp.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("generic_ending", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0
    ),

    GuardianQuestLines(
        id="ending_overwhelmed_failure",
        title="Sự Choáng Ngợp Thất Bại",
        description="Bạn bị nỗi cô đơn của nàng tiên hoa choáng ngợp và rút lui, khiến nàng biến mất. {guardian.ga_name} nhìn bạn với ánh mắt đau khổ. 'Ngài... ta hy vọng Ngài sẽ mạnh mẽ hơn.' Khu vườn trở nên trống rỗng. Bạn sống với nỗi ân hận vì đã không đủ mạnh mẽ để đối mặt với nỗi đau, và {guardian.ga_name} phải chịu đựng sự buồn bã vì sự yếu đuối của bạn. Cuộc phiêu lưu tiếp tục, nhưng với một bài học khắc nghiệt.",
        choice_a="Bạn rút lui vì bị choáng ngợp, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("generic_ending", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0
    ),

    GuardianQuestLines(
        id="ending_too_late",
        title="Quá Muộn Để Cứu Vãn",
        description="Bạn chần chừ quá lâu, khiến nàng tiên hoa tan biến mãi mãi. {guardian.ga_name} nhìn bạn với ánh mắt buồn bã, 'Chúng ta đã quá muộn để cứu vãn nàng.' Khu vườn trở nên hoang tàn. Bạn sống với nỗi ân hận vì đã không hành động kịp thời, và {guardian.ga_name} phải chịu đựng sự buồn bã vì sự chậm trễ của bạn. Cuộc phiêu lưu tiếp tục, nhưng với một sự nuối tiếc vĩnh cửu.",
        choice_a="Nàng tiên hoa biến mất, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("generic_ending", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0
    ),

    GuardianQuestLines(
        id="ending_lost_hope_fairy",
        title="Nàng Tiên Mất Hy Vọng",
        description="Sự chần chừ của bạn đã khiến nàng tiên hoa mất đi hy vọng và biến mất. {guardian.ga_name} nhìn bạn với ánh mắt buồn bã. 'Nàng ấy đã không còn tin vào chúng ta nữa.' Khu vườn trở nên im lặng và u ám. Bạn sống với nỗi ân hận vì đã không thể giữ vững hy vọng của nàng, và {guardian.ga_name} phải chịu đựng sự buồn bã vì sự mất mát đó. Cuộc phiêu lưu tiếp tục, nhưng với một trái tim nặng trĩu.",
        choice_a="Nàng tiên hoa biến mất, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("generic_ending", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0
    ),

    GuardianQuestLines(
        id="ending_missed_connection",
        title="Mối Kết Nối Bỏ Lỡ",
        description="Nàng tiên hoa đã đến gần, nhưng sự chần chừ của bạn đã khiến bạn bỏ lỡ cơ hội tạo ra một kết nối. Nàng biến mất. {guardian.ga_name} nhìn bạn với ánh mắt tiếc nuối. 'Thật đáng tiếc, Ngài. Chúng ta đã gần lắm rồi.' Khu vườn trở lại vẻ hoang tàn. Bạn sống với nỗi ân hận vì đã bỏ lỡ một cơ hội quý giá, và {guardian.ga_name} phải chịu đựng sự buồn bã vì sự tiếc nuối đó. Cuộc phiêu lưu tiếp tục, nhưng với một sự hối tiếc.",
        choice_a="Bạn bỏ lỡ cơ hội, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("generic_ending", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0
    ),

    GuardianQuestLines(
        id="ending_fruitless_search_again",
        title="Tìm Kiếm Vô Vọng Lặp Lại",
        description="Bạn và {guardian.ga_name} tiếp tục tìm kiếm một cổ vật để hóa giải lời nguyền, nhưng vô ích. Nàng tiên hoa biến mất trong cô đơn, và khu vườn trở nên hoang tàn. {guardian.ga_name} nhìn bạn với ánh mắt mệt mỏi. 'Chúng ta đã tìm sai cách từ đầu.' Bạn sống với nỗi ân hận vì đã không nhận ra sai lầm của mình, và {guardian.ga_name} phải chịu đựng sự buồn bã vì sự vô ích đó. Cuộc phiêu lưu tiếp tục, nhưng với một bài học đau đớn.",
        choice_a="Nhiệm vụ thất bại vì tìm sai hướng.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("generic_ending", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0
    ),

    GuardianQuestLines(
        id="ending_garden_of_despair",
        title="Khu Vườn Của Tuyệt Vọng",
        description="Nỗi tuyệt vọng của nàng tiên hoa đã nuốt chửng cả linh hồn của khu vườn. Khu vườn giờ đây là một vùng đất chết, không còn dấu hiệu của sự sống. {guardian.ga_name} gục đầu, 'Ta... ta đã không thể làm gì.' Bạn sống với nỗi ân hận sâu sắc vì đã để mọi thứ đi đến bước đường này, và {guardian.ga_name} phải chịu đựng sự đau khổ tột cùng. Cuộc phiêu lưu tiếp tục, nhưng với một cái kết bi thảm, nơi hy vọng đã chết.",
        choice_a="Nàng tiên hoa biến mất, khu vườn chết.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("generic_ending", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0
    ),
    
    GuardianQuestLines(
        id="generic_ending",
        title="Hành Trình Mới",
        description="Bạn và {guardian.ga_name} rời khỏi vùng đất hoang tàn, mang theo những ký ức về cuộc phiêu lưu vừa qua. Dù thành công hay thất bại, mỗi trải nghiệm đều khắc sâu một bài học.",
        choice_a="",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("", "", "", ""),
        gold=0, silver=0, ga_exp=0, dignity_point=0
    ),
]



all_quests_page_2 = [quest_red_promises, quest_forgetten_garden, quest_romance_letter]