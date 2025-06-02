
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
        )
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
        next_steps=NextSteps("quest_success_end_3", "quest_success_end_3", "quest_success_end_3", "quest_success_end_3")
    ),

    # Failures
    GuardianQuestLines(
        id="ignore_spirits_outcome",
        title="Phớt Lờ Tiếng Kêu Cứu",
        description="Bạn quyết định bỏ qua. Vài ngày sau, khu rừng trở nên u ám hơn, và những câu chuyện về linh hồn quấy phá lan rộng. {guardian.ga_name} nhìn bạn với vẻ thất vọng.",
        choice_a="Cảm thấy hối tiếc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3")
    ),

    GuardianQuestLines(
        id="ga_worried_timeout_3",
        title="Ánh Mắt Lo Lắng",
        description="Bạn chần chừ quá lâu. {guardian.ga_name} lắc đầu thất vọng. 'Chúng ta không thể cứu họ nếu cứ đứng đây!' Nhiệm vụ kết thúc vì sự thiếu quyết đoán.",
        choice_a="Cảm thấy bất lực. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3")
    ),

    GuardianQuestLines(
        id="spirit_fades_timeout",
        title="Linh Hồn Tan Biến",
        description="Bạn và {guardian.ga_name} chần chừ. Linh hồn yếu ớt dần dần tan biến vào hư vô, không thể được cứu vớt. {guardian.ga_name} thở dài buồn bã. 'Đã quá muộn rồi.'",
        choice_a="Cảm thấy nuối tiếc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3")
    ),

    GuardianQuestLines(
        id="avoid_spirit_outcome",
        title="Tránh Xa Linh Hồn",
        description="Bạn và {guardian.ga_name} cố gắng tìm đường vòng, nhưng khu rừng dường như không cho phép. Bạn lạc lối và không thể tìm thấy lối thoát. 'Chúng ta đã đi sai đường rồi, chủ nhân,' {guardian.ga_name} nói.",
        choice_a="Bạn bị lạc và nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3")
    ),

    GuardianQuestLines(
        id="abandon_quest_ancient_forest",
        title="Từ Bỏ Nhiệm Vụ",
        description="Bạn quyết định rằng nhiệm vụ này quá phức tạp và nguy hiểm. Bạn và {guardian.ga_name} quay lưng lại với số phận của khu rừng. 'Tôi hy vọng có ai đó khác có thể giúp đỡ,' {guardian.ga_name} nói với giọng buồn bã.",
        choice_a="Cảm thấy nhẹ nhõm, nhưng cũng có chút hối tiếc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3")
    ),

    GuardianQuestLines(
        id="spirit_anger_outcome",
        title="Linh Hồn Nổi Giận",
        description="Bạn chần chừ trong việc quyết định cách tiếp cận. Linh hồn gầm lên giận dữ, nó trở nên mạnh hơn và tấn công bạn. {guardian.ga_name} phải tạo lá chắn để bảo vệ bạn.",
        choice_a="Bạn bị tấn công và phải rút lui. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3")
    ),

    GuardianQuestLines(
        id="let_spirit_be_outcome",
        title="Mặc Kệ Linh Hồn",
        description="Bạn quyết định để linh hồn tự giải thoát. Tuy nhiên, linh hồn không thể tự mình vượt qua lời nguyền và cuối cùng tan biến hoàn toàn. 'Chúng ta đã không thể giúp nó,' {guardian.ga_name} nói buồn bã.",
        choice_a="Bạn cảm thấy bất lực. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3")
    ),

    GuardianQuestLines(
        id="retreat_from_forest",
        title="Rút Lui Khỏi Rừng",
        description="Bạn và {guardian.ga_name} quyết định rút lui khỏi khu rừng cổ. Bạn cảm thấy một nỗi buồn man mác khi rời đi, biết rằng linh hồn vẫn đang mắc kẹt ở đó. 'Chúng ta không thể làm gì lúc này,' {guardian.ga_name} thở dài.",
        choice_a="Rút lui và nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3")
    ),

    GuardianQuestLines(
        id="artifact_disappears_timeout",
        title="Cổ Vật Biến Mất",
        description="Bạn chần chừ quá lâu trước cổ vật. Năng lượng của lời nguyền bùng phát mạnh mẽ, khiến cổ vật biến mất vào hư vô. 'Không! Đã quá muộn rồi!' {guardian.ga_name} thốt lên.",
        choice_a="Cổ vật biến mất, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3", "quest_failed_end_3")
    ),

    # Generic Endings
    GuardianQuestLines(
        id="quest_success_end_3",
        title="Hòa Bình Cho Khu Rừng",
        description="Khu rừng cổ đã tìm thấy sự bình yên. Những linh hồn được giải thoát, và không khí trở nên trong lành. {guardian.ga_name} mỉm cười. 'Chúng ta đã mang lại sự bình yên cho nơi đây, chủ nhân.'",
        choice_a="Bạn cảm thấy tự hào về bản thân và {guardian.ga_name}.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("continue_adventure_3", "continue_adventure_3", "continue_adventure_3", "continue_adventure_3")
    ),

    GuardianQuestLines(
        id="quest_failed_end_3",
        title="Bóng Tối Tiếp Diễn",
        description="Khu rừng cổ vẫn chìm trong sự đau khổ của những linh hồn mắc kẹt. {guardian.ga_name} cúi đầu, vẻ mặt buồn bã. 'Chúng ta... đã không thể thay đổi số phận của họ.'",
        choice_a="Rút ra bài học đau đớn.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("continue_adventure_3", "continue_adventure_3", "continue_adventure_3", "continue_adventure_3")
    ),

    GuardianQuestLines(
        id="continue_adventure_3",
        title="Hành Trình Tiếp Nối",
        description="Bạn và {guardian.ga_name} rời khỏi khu rừng cổ, mang theo những ký ức về hành trình vừa qua. Những cuộc phiêu lưu mới đang chờ đợi...",
        choice_a="",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("", "", "", "")
    )
]

#region quest lake mystery
quest_lake_mystery = [
    GuardianQuestLines(
        id="start",
        title="Bí Ẩn Của Hồ Nước Ngừng Đọng",
        description="Một sự tĩnh lặng bất thường bao trùm hồ nước. {guardian.ga_name} nhìn chằm chằm vào mặt nước. 'Tôi cảm thấy một năng lượng kỳ lạ, như thể thời gian ở đây đã ngừng lại.'",
        choice_a="Tiến đến gần hồ để điều tra.",
        choice_b="Tìm kiếm thông tin về lịch sử hồ.",
        choice_c="Bỏ qua, hồ nước có vẻ nguy hiểm.",
        choice_timeout="{guardian.ga_name} cau mày. 'Chúng ta không thể phớt lờ điều này!'",
        next_steps=NextSteps(
            choice_a="approach_lake",
            choice_b="research_lake_history",
            choice_c="ignore_lake_outcome",
            timeout="ga_insist_timeout_1"
        )
    ),

    GuardianQuestLines(
        id="approach_lake",
        title="Bước Chân Đến Bờ Hồ",
        description="Bạn và {guardian.ga_name} đến gần hồ. Mặt nước phẳng lặng như gương, nhưng không có sự sống nào xung quanh. {guardian.ga_name} chỉ vào một vật thể lấp lánh dưới đáy hồ. 'Có vẻ như có thứ gì đó ở đó.'",
        choice_a="Thử lặn xuống để lấy vật thể.",
        choice_b="Sử dụng phép thuật để đưa vật thể lên.",
        choice_c="Quan sát thêm, không hành động vội vàng.",
        choice_timeout="{guardian.ga_name} thúc giục. 'Vật thể đó đang gọi chúng ta!'",
        next_steps=NextSteps(
            choice_a="dive_for_object",
            choice_b="use_magic_to_retrieve",
            choice_c="observe_more",
            timeout="object_disappears_timeout"
        )
    ),

    GuardianQuestLines(
        id="research_lake_history",
        title="Khám Phá Lịch Sử Hồ",
        description="Bạn và {guardian.ga_name} đến thư viện cổ. Bạn tìm thấy một truyền thuyết kể về một viên đá thời gian bị mất tích trong hồ, có khả năng làm ngừng đọng thời gian. 'Chúng ta phải tìm viên đá đó!' {guardian.ga_name} nói.",
        choice_a="Tìm kiếm viên đá thời gian trong hồ.",
        choice_b="Trở lại hồ, thử cách khác.",
        choice_c="Từ bỏ nhiệm vụ, quá rủi ro.",
        choice_timeout="{guardian.ga_name} nói. 'Chúng ta không có nhiều thời gian đâu!'",
        next_steps=NextSteps(
            choice_a="approach_lake", # Dẫn đến tìm vật thể dưới hồ
            choice_b="approach_lake",
            choice_c="abandon_quest_lake",
            timeout="ga_insist_timeout_1"
        )
    ),

    GuardianQuestLines(
        id="dive_for_object",
        title="Lặn Xuống Hồ Sâu",
        description="Bạn lặn xuống làn nước lạnh giá. {guardian.ga_name} tạo một lớp bảo vệ xung quanh bạn. Dưới đáy hồ, bạn thấy một viên đá phát sáng kỳ lạ. Khi bạn chạm vào, thời gian xung quanh dường như chậm lại.",
        choice_a="Cố gắng đưa viên đá lên mặt nước.",
        choice_b="Nghiên cứu viên đá dưới nước.",
        choice_c="Quay lại ngay, có điều gì đó không ổn.",
        choice_timeout="{guardian.ga_name} lo lắng. 'Hãy nhanh lên, năng lượng đang thay đổi!'",
        next_steps=NextSteps(
            choice_a="retrieve_stone",
            choice_b="examine_stone_underwater",
            choice_c="retreat_from_lake",
            timeout="time_distortion_outcome"
        )
    ),

    GuardianQuestLines(
        id="use_magic_to_retrieve",
        title="Sử Dụng Phép Thuật",
        description="Bạn và {guardian.ga_name} tập trung năng lượng. Một luồng ánh sáng từ tay bạn kéo vật thể lên. Đó là một viên đá lấp lánh, phát ra năng lượng kỳ lạ. {guardian.ga_name} nói: 'Đây chính là viên đá thời gian trong truyền thuyết!'",
        choice_a="Kiểm tra viên đá thời gian.",
        choice_b="Mang viên đá đến một nơi an toàn.",
        choice_c="Vứt bỏ viên đá, nó quá nguy hiểm.",
        choice_timeout="{guardian.ga_name} thúc giục. 'Chúng ta phải hành động nhanh với nó!'",
        next_steps=NextSteps(
            choice_a="examine_time_stone",
            choice_b="secure_time_stone",
            choice_c="discard_stone_outcome",
            timeout="time_distortion_outcome"
        )
    ),

    # Final Stages (Success/Failure)
    GuardianQuestLines(
        id="retrieve_stone",
        title="Viên Đá Được Đưa Lên",
        description="Bạn thành công đưa viên đá lên bờ. Ngay lập tức, dòng chảy thời gian của hồ trở lại bình thường, những bông hoa nở rộ và chim hót líu lo. {guardian.ga_name} mỉm cười rạng rỡ. 'Chúng ta đã giải thoát hồ khỏi sự ngừng đọng!'",
        choice_a="Nhiệm vụ hoàn thành! Hồ nước trở lại sự sống.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_success_end_1", "quest_success_end_1", "quest_success_end_1", "quest_success_end_1")
    ),

    GuardianQuestLines(
        id="examine_stone_underwater",
        title="Nghiên Cứu Dưới Nước",
        description="Bạn cố gắng nghiên cứu viên đá dưới nước, nhưng năng lượng của nó quá mạnh. Thời gian xung quanh bạn bị bóp méo, khiến bạn cảm thấy chóng mặt. {guardian.ga_name} kéo bạn lên kịp thời. 'Nguy hiểm quá!'",
        choice_a="Bạn bị choáng váng nhẹ. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1")
    ),

    GuardianQuestLines(
        id="examine_time_stone",
        title="Kiểm Tra Viên Đá Thời Gian",
        description="Bạn và {guardian.ga_name} kiểm tra viên đá thời gian. Nó phát ra một luồng sáng ấm áp, có khả năng điều chỉnh dòng chảy thời gian. {guardian.ga_name} nói: 'Chúng ta có thể dùng nó để giúp đỡ người khác!'",
        choice_a="Đưa viên đá trở lại hồ để khôi phục thời gian.",
        choice_b="Giữ viên đá để sử dụng trong tương lai.",
        choice_c="",
        choice_timeout="{guardian.ga_name} nói. 'Đừng chần chừ, năng lượng của nó đang dần ổn định!'",
        next_steps=NextSteps(
            choice_a="retrieve_stone", # Dẫn đến việc trả lại hồ
            choice_b="keep_time_stone_outcome",
            choice_c="",
            timeout="time_distortion_outcome"
        )
    ),

    GuardianQuestLines(
        id="secure_time_stone",
        title="Bảo Vệ Viên Đá",
        description="Bạn và {guardian.ga_name} đưa viên đá thời gian đến một nơi an toàn, cất giữ cẩn thận để không ai có thể lạm dụng sức mạnh của nó. {guardian.ga_name} gật đầu. 'Một quyết định khôn ngoan, chủ nhân.'",
        choice_a="Nhiệm vụ hoàn thành! Viên đá được bảo vệ.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_success_end_1", "quest_success_end_1", "quest_success_end_1", "quest_success_end_1")
    ),

    # Failures
    GuardianQuestLines(
        id="ignore_lake_outcome",
        title="Phớt Lờ Hồ Nước",
        description="Bạn quyết định bỏ qua hồ. Vài ngày sau, tin đồn về việc thời gian bị bóp méo quanh hồ lan rộng, gây ra sự hỗn loạn. {guardian.ga_name} thở dài. 'Chúng ta đã bỏ lỡ cơ hội giúp đỡ.'",
        choice_a="Cảm thấy hối tiếc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1")
    ),

    GuardianQuestLines(
        id="ga_insist_timeout_1",
        title="Lời Thúc Giục Của Guardian",
        description="Bạn chần chừ quá lâu. {guardian.ga_name} nắm tay bạn. 'Chúng ta phải hành động, chủ nhân! Mọi thứ đang trở nên tệ hơn.' Nhiệm vụ kết thúc vì sự thiếu quyết đoán.",
        choice_a="Cảm thấy bất lực. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1")
    ),

    GuardianQuestLines(
        id="object_disappears_timeout",
        title="Vật Thể Biến Mất",
        description="Bạn và {guardian.ga_name} chần chừ quá lâu. Ánh sáng từ vật thể dưới hồ dần mờ đi và biến mất hoàn toàn. {guardian.ga_name} thở dài. 'Đã quá muộn rồi.'",
        choice_a="Cảm thấy nuối tiếc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1")
    ),

    GuardianQuestLines(
        id="observe_more",
        title="Quan Sát Không Hành Động",
        description="Bạn và {guardian.ga_name} tiếp tục quan sát hồ, nhưng không có gì thay đổi. Vật thể dưới đáy hồ vẫn ở đó, nhưng bạn không tìm ra cách tiếp cận an toàn. 'Chúng ta cần một kế hoạch tốt hơn,' {guardian.ga_name} nói.",
        choice_a="Không tìm được cách. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1")
    ),

    GuardianQuestLines(
        id="abandon_quest_lake",
        title="Từ Bỏ Hồ Nước",
        description="Bạn quyết định rằng bí ẩn của hồ nước quá phức tạp. Bạn và {guardian.ga_name} rời đi, bỏ mặc hồ chìm trong sự tĩnh lặng bất thường. 'Tôi hy vọng hồ sẽ tìm được sự bình yên,' {guardian.ga_name} nói với giọng buồn bã.",
        choice_a="Cảm thấy nhẹ nhõm, nhưng cũng có chút hối tiếc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1")
    ),

    GuardianQuestLines(
        id="time_distortion_outcome",
        title="Thời Gian Biến Dạng",
        description="Bạn chần chừ trong việc quyết định cách tiếp cận. Năng lượng từ viên đá bùng phát mạnh mẽ, làm thời gian xung quanh bạn bị biến dạng. {guardian.ga_name} phải dùng hết sức để bảo vệ bạn khỏi tác động.",
        choice_a="Bạn bị ảnh hưởng bởi sự biến dạng thời gian. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1")
    ),

    GuardianQuestLines(
        id="retreat_from_lake",
        title="Rút Lui Khỏi Hồ",
        description="Bạn và {guardian.ga_name} quyết định rút lui khỏi hồ nước. Bạn cảm thấy một nỗi lo lắng khi rời đi, biết rằng bí ẩn của hồ vẫn chưa được giải đáp. 'Chúng ta không thể mạo hiểm hơn nữa,' {guardian.ga_name} thở dài.",
        choice_a="Rút lui và nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1")
    ),

    GuardianQuestLines(
        id="discard_stone_outcome",
        title="Vứt Bỏ Viên Đá",
        description="Bạn quyết định vứt bỏ viên đá thời gian. Tuy nhiên, năng lượng của nó quá mạnh, và nó gây ra một vụ nổ nhỏ khi bạn ném đi. {guardian.ga_name} phải nhanh chóng kéo bạn ra xa.",
        choice_a="Bạn bị choáng váng nhẹ. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1", "quest_failed_end_1")
    ),

    GuardianQuestLines(
        id="keep_time_stone_outcome",
        title="Giữ Lại Viên Đá Thời Gian",
        description="Bạn và {guardian.ga_name} quyết định giữ lại viên đá thời gian. Sức mạnh của nó rất lớn và có thể được sử dụng trong tương lai. {guardian.ga_name} nói: 'Hãy cẩn thận khi sử dụng nó, chủ nhân.'",
        choice_a="Bạn có được một vật phẩm mạnh mẽ. Nhiệm vụ thành công.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_success_end_1", "quest_success_end_1", "quest_success_end_1", "quest_success_end_1")
    ),

    # Generic Endings
    GuardianQuestLines(
        id="quest_success_end_1",
        title="Sự An Bình Trở Lại",
        description="Hồ nước đã trở lại bình thường, sự sống và thời gian chảy trôi như vốn có. {guardian.ga_name} mỉm cười. 'Chúng ta đã hoàn thành nhiệm vụ một cách xuất sắc, chủ nhân!'",
        choice_a="Bạn cảm thấy hài lòng về thành quả của mình.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("continue_adventure_1", "continue_adventure_1", "continue_adventure_1", "continue_adventure_1")
    ),

    GuardianQuestLines(
        id="quest_failed_end_1",
        title="Hồ Nước Ngừng Đọng Vĩnh Viễn",
        description="Hồ nước vẫn chìm trong sự tĩnh lặng kỳ lạ, thời gian ngừng trôi. {guardian.ga_name} cúi đầu, vẻ mặt buồn bã. 'Tôi ước chúng ta có thể làm được nhiều hơn.'",
        choice_a="Bạn cảm thấy thất vọng. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("continue_adventure_1", "continue_adventure_1", "continue_adventure_1", "continue_adventure_1")
    ),

    GuardianQuestLines(
        id="continue_adventure_1",
        title="Hành Trình Tiếp Nối",
        description="Bạn và {guardian.ga_name} rời khỏi hồ nước, mang theo những ký ức về cuộc phiêu lưu. Những thử thách mới đang chờ đợi...",
        choice_a="",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("", "", "", "")
    )
]

quest_the_ruin_call = [
    GuardianQuestLines(
        id="start",
        title="Tiếng Gọi Từ Phế Tích Lãng Quên",
        description="Một luồng gió lạnh buốt mang theo tiếng vọng ai oán từ phế tích cổ xưa. {guardian.ga_name} khẽ rùng mình. 'Ta cảm nhận được sự tuyệt vọng sâu sắc, bạn. Có lẽ chúng ta nên tìm hiểu.'",
        choice_a="Đi thẳng đến phế tích để điều tra.",
        choice_b="Tìm thông tin về lịch sử của phế tích trước.",
        choice_c="Bỏ qua, phế tích này có vẻ nguy hiểm.",
        choice_timeout="{guardian.ga_name} nhìn bạn đầy lo lắng. 'Những tiếng kêu đó không thể phớt lờ, bạn!'",
        next_steps=NextSteps(
            choice_a="enter_ruins",
            choice_b="research_ruins_history",
            choice_c="ignore_ruins_outcome",
            timeout="ga_worried_timeout_2"
        )
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
        choice_timeout="{guardian.ga_name} nói. 'Chúng ta không có nhiều thời gian để tìm kiếm đâu, bạn!'",
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
        choice_timeout="Năng lượng phong ấn trở nên dữ dội. 'Nó sẽ nuốt chửng chúng ta, bạn!' {guardian.ga_name} cảnh báo.",
        next_steps=NextSteps(
            choice_a="continue_break_seal",
            choice_b="seek_revival_crystal", # Dẫn đến tìm pha lê
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
        choice_timeout="{guardian.ga_name} nói. 'Pha lê ở ngay trước mắt chúng ta, bạn!'",
        next_steps=NextSteps(
            choice_a="take_crystal",
            choice_b="deactivate_poison_gas",
            choice_c="check_for_dangers",
            timeout="crystal_vanishes_timeout"
        )
    ),

    # Final Stage Outcomes
    GuardianQuestLines(
        id="continue_break_seal",
        title="Phong Ấn Vỡ Tan",
        description="Bạn và {guardian.ga_name} cuối cùng đã phá vỡ phong ấn. Một linh hồn rồng khổng lồ xuất hiện, nhưng nó đã kiệt sức. {guardian.ga_name} nói: 'Nó cần được chữa lành để giải thoát hoàn toàn!'",
        choice_a="Sử dụng phép thuật chữa lành.",
        choice_b="Rút lui ngay, linh hồn rồng quá đáng sợ.",
        choice_c="",
        choice_timeout="{guardian.ga_name} nói. 'Chúng ta không thể để nó lại trong tình trạng này, bạn!'",
        next_steps=NextSteps(
            choice_a="heal_dragon_spirit",
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
        choice_timeout="{guardian.ga_name} thúc giục. 'Chúng ta phải sử dụng nó ngay, bạn!'",
        next_steps=NextSteps(
            choice_a="use_release_stone",
            choice_b="research_ruins_history",
            choice_c="",
            timeout="stone_breaks_timeout"
        )
    ),

    GuardianQuestLines(
        id="take_crystal",
        title="Lấy Pha Lê Thành Công",
        description="Bạn chạm vào Pha Lê Hồi Sinh. Một luồng năng lượng thuần khiết lan tỏa, xua tan chướng khí. {guardian.ga_name} reo lên: 'Chúng ta đã có nó, bạn! Hãy mang nó về phế tích!'",
        choice_a="Mang pha lê trở lại phế tích.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("return_to_ruins_with_crystal", "", "", "")
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

    GuardianQuestLines(
        id="return_to_ruins_with_crystal",
        title="Sức Mạnh Hồi Sinh",
        description="Bạn và {guardian.ga_name} mang Pha Lê Hồi Sinh trở lại phế tích. Khi bạn đặt pha lê lên bệ đá gần linh hồn rồng, một luồng sáng mạnh mẽ bùng lên, hồi sinh linh hồn và hóa giải lời nguyền khỏi phế tích.",
        choice_a="Nhiệm vụ hoàn thành! Linh hồn được giải thoát.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_success_end_2", "quest_success_end_2", "quest_success_end_2", "quest_success_end_2")
    ),

    GuardianQuestLines(
        id="heal_dragon_spirit",
        title="Linh Hồn Rồng Được Chữa Lành",
        description="Bạn và {guardian.ga_name} sử dụng phép thuật chữa lành. Linh hồn rồng dần bình phục, ánh sáng của nó trở nên mạnh mẽ hơn, rồi cất cánh bay lên trời, mang theo sự bình yên trở lại phế tích.",
        choice_a="Nhiệm vụ hoàn thành! Phế tích trở nên yên bình.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_success_end_2", "quest_success_end_2", "quest_success_end_2", "quest_success_end_2")
    ),

    GuardianQuestLines(
        id="use_release_stone",
        title="Sử Dụng Viên Đá Giải Thoát",
        description="Bạn sử dụng Viên Đá Giải Thoát. Một luồng ánh sáng mạnh mẽ từ viên đá phá vỡ hoàn toàn lời nguyền, giải thoát linh hồn rồng. Linh hồn rồng bay lên trời, để lại phế tích trong sự bình yên.",
        choice_a="Nhiệm vụ hoàn thành! Phế tích được giải thoát.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_success_end_2", "quest_success_end_2", "quest_success_end_2", "quest_success_end_2")
    ),

    # Failures
    GuardianQuestLines(
        id="ignore_ruins_outcome",
        title="Phớt Lờ Tiếng Kêu Cứu",
        description="Bạn quyết định bỏ qua. Vài ngày sau, phế tích trở nên u ám hơn, và những câu chuyện về các linh hồn quấy phá lan rộng. {guardian.ga_name} nhìn bạn với vẻ thất vọng.",
        choice_a="Cảm thấy hối tiếc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2")
    ),

    GuardianQuestLines(
        id="ga_worried_timeout_2",
        title="Ánh Mắt Lo Lắng",
        description="Bạn chần chừ quá lâu. {guardian.ga_name} lắc đầu thất vọng. 'Chúng ta không thể cứu họ nếu cứ đứng đây, bạn!' Nhiệm vụ kết thúc vì sự thiếu quyết đoán.",
        choice_a="Cảm thấy bất lực. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2")
    ),

    GuardianQuestLines(
        id="ruins_collapse_timeout",
        title="Phế Tích Sụp Đổ",
        description="Bạn và {guardian.ga_name} chần chừ. Một phần phế tích sụp đổ, chặn mất lối vào và vật thể quý giá. {guardian.ga_name} thở dài buồn bã. 'Đã quá muộn rồi.'",
        choice_a="Cảm thấy nuối tiếc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2")
    ),

    GuardianQuestLines(
        id="retreat_from_ruins",
        title="Rút Lui Khỏi Phế Tích",
        description="Bạn và {guardian.ga_name} quyết định rút lui khỏi phế tích. Bạn cảm thấy một nỗi buồn man mác khi rời đi, biết rằng linh hồn vẫn đang bị giam cầm. 'Chúng ta không thể làm gì lúc này, bạn,' {guardian.ga_name} thở dài.",
        choice_a="Rút lui và nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2")
    ),

    GuardianQuestLines(
        id="abandon_quest_ruins",
        title="Từ Bỏ Nhiệm Vụ",
        description="Bạn quyết định rằng nhiệm vụ này quá phức tạp và nguy hiểm. Bạn và {guardian.ga_name} quay lưng lại với số phận của phế tích. 'Ta hy vọng có ai đó khác có thể giúp đỡ,' {guardian.ga_name} nói với giọng buồn bã.",
        choice_a="Cảm thấy nhẹ nhõm, nhưng cũng có chút hối tiếc. (Nhiệm vụ thất bại)",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2")
    ),

    GuardianQuestLines(
        id="seal_overwhelm_outcome",
        title="Phong Ấn Quá Mạnh",
        description="Bạn chần chừ trong việc quyết định cách tiếp cận. Năng lượng phong ấn bùng phát mạnh mẽ, tấn công bạn và {guardian.ga_name}. {guardian.ga_name} phải tạo lá chắn để bảo vệ bạn.",
        choice_a="Bạn bị tấn công và phải rút lui. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2")
    ),

    GuardianQuestLines(
        id="dragon_anger_outcome",
        title="Linh Hồn Rồng Phẫn Nộ",
        description="Bạn chần chừ trong việc quyết định cách tiếp cận linh hồn rồng. Nó gầm lên giận dữ, trở nên mạnh hơn và tấn công bạn. {guardian.ga_name} phải tạo lá chắn để bảo vệ bạn.",
        choice_a="Bạn bị tấn công và phải rút lui. Nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2")
    ),

    GuardianQuestLines(
        id="stone_breaks_timeout",
        title="Viên Đá Tan Vỡ",
        description="Bạn chần chừ quá lâu trước Viên Đá Giải Thoát. Năng lượng của lời nguyền bùng phát mạnh mẽ, khiến viên đá nứt vỡ và tan biến. 'Không! Đã quá muộn rồi!' {guardian.ga_name} thốt lên.",
        choice_a="Viên đá biến mất, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2")
    ),

    GuardianQuestLines(
        id="crystal_vanishes_timeout",
        title="Pha Lê Biến Mất",
        description="Bạn chần chừ quá lâu trước pha lê. Chướng khí bùng phát mạnh mẽ, khiến pha lê tan biến vào hư vô. 'Không! Đã quá muộn rồi!' {guardian.ga_name} thốt lên.",
        choice_a="Pha lê biến mất, nhiệm vụ thất bại.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2", "quest_failed_end_2")
    ),

    # Generic Endings
    GuardianQuestLines(
        id="quest_success_end_2",
        title="Bình Yên Cho Phế Tích",
        description="Phế tích cổ xưa đã tìm thấy sự bình yên. Linh hồn rồng được giải thoát, và không khí trở nên trong lành. {guardian.ga_name} mỉm cười. 'Chúng ta đã mang lại sự bình yên cho nơi đây, bạn.'",
        choice_a="Bạn cảm thấy tự hào về bản thân và {guardian.ga_name}.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("continue_adventure_2", "continue_adventure_2", "continue_adventure_2", "continue_adventure_2")
    ),

    GuardianQuestLines(
        id="quest_failed_end_2",
        title="Bóng Tối Tiếp Diễn",
        description="Phế tích cổ xưa vẫn chìm trong sự giam cầm của lời nguyền. {guardian.ga_name} cúi đầu, vẻ mặt buồn bã. 'Chúng ta... đã không thể thay đổi số phận của họ.'",
        choice_a="Rút ra bài học đau đớn.",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("continue_adventure_2", "continue_adventure_2", "continue_adventure_2", "continue_adventure_2")
    ),

    GuardianQuestLines(
        id="continue_adventure_2",
        title="Hành Trình Tiếp Nối",
        description="Bạn và {guardian.ga_name} rời khỏi phế tích, mang theo những ký ức về hành trình vừa qua. Những cuộc phiêu lưu mới đang chờ đợi...",
        choice_a="",
        choice_b="", choice_c="", choice_timeout="",
        next_steps=NextSteps("", "", "", "")
    )
]

all_quests = [quest_ghost_of_forrest, quest_lake_mystery, quest_the_ruin_call]