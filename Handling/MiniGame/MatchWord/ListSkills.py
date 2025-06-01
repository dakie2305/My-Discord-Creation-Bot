
from CustomEnum.SlashEnum import SlashCommand
from Handling.MiniGame.MatchWord.MwClass import SpecialItem


list_special_items_cap_thap = [
    SpecialItem(
        item_id="ct_minus",
        item_name="Trừ Điểm Của Đối Phương",
        item_description=f"Kỹ năng này sẽ trừ đi 2 điểm của đối thủ trong trò chơi nối chữ, lưu ý là đối phương đã từng chơi trò này. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point =2,
        level="Cấp Thấp",
        required_target=True
    ),
    SpecialItem(
        item_id="ct_add",
        item_name="Cộng Điểm Bản Thân",
        item_description=f"Kỹ năng này sẽ cộng cho bản thân 2 điểm trong trò chơi nối chữ. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point =2,
        level="Cấp Thấp",
        required_target=False
    ),
    SpecialItem(
        item_id="ct_hint",
        item_name="Gợi Ý Nửa Từ",
        item_description=f"Kỹ năng này sẽ gợi ý một nửa từ cần thiết để hoàn thành lượt chơi nối chữ hiện tại. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point =0,
        level="Cấp Thấp",
        required_target=False
    ),
    SpecialItem(
        item_id="ct_minus_first",
        item_name="Trừ Điểm Top 1",
        item_description=f"Kỹ năng này sẽ trừ 10 điểm của player top 1 trong bảng xếp hạng. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=10,
        level="Cấp Thấp",
        required_target=False
    ),
    SpecialItem(
        item_id="ct_minus_second",
        item_name="Trừ Điểm Top 2",
        item_description=f"Kỹ năng này sẽ trừ 8 điểm của player top 2 trong bảng xếp hạng. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=8,
        level="Cấp Thấp",
        required_target=False
    ),
    SpecialItem(
        item_id="ct_add_user",
        item_name="Cộng Điểm Đối Phương",
        item_description=f"Kỹ năng này sẽ cộng 2 điểm cho đối phương bất kỳ ngoại trừ bản thân, lưu ý là đối phương đã từng chơi trò này. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=2,
        level="Cấp Thấp",
        required_target=True
    ),
    SpecialItem(
        item_id="ct_allow",
        item_name="Cho Phép Tiếp Tục Chơi",
        item_description=f"Kỹ năng này sẽ cho phép tiếp tục nối từ dù vừa mới nối từ xong. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=0,
        level="Cấp Thấp",
        required_target=False
    ),
    SpecialItem(
        item_id="ct_curr_player",
        item_name="Vui Lòng Né Qua Chỗ Khác",
        item_description=f"Kỹ năng này sẽ biến đối phương thành người đã nối từ hiện tại (dù cho người nối từ hiện tại có là ai khác). Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=0,
        level="Cấp Thấp",
        required_target=True
    ),
    SpecialItem(
        item_id="ct_random_skill_cc",
        item_name="Đổi Điểm",
        item_description=f"Kỹ năng này sẽ đổi 1 điểm của bạn để đổi lấy một kỹ năng rank Cấp Cao ngẫu nhiên. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=1,
        level="Cấp Thấp",
        required_target=False
    ),
    SpecialItem(
        item_id="ct_steal_point",
        item_name="Ăn Cắp Điểm",
        item_description=f"Kỹ năng này sẽ có 50/50 phần trăm ăn cắp 3 điểm của đối phương. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=3,
        level="Cấp Thấp",
        required_target=True
    ),
    SpecialItem(
        item_id="ct_protect",
        item_name="Bảo Hộ",
        item_description=f"Kỹ năng này sẽ bảo vệ người chơi và vô hiệu hoá kỹ năng của player khác. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=1,
        level="Cấp Thấp",
        required_target=False
    ),
    SpecialItem(
        item_id="ct_protect_user",
        item_name="Bảo Hộ Đối Phương",
        item_description=f"Kỹ năng này sẽ bảo vệ đối phương và vô hiệu hoá kỹ năng của player khác. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=1,
        level="Cấp Thấp",
        required_target=True
    ),
    SpecialItem(
        item_id="ct_ban",
        item_name="Câm Lặng",
        item_description=f"Kỹ năng này sẽ khoá miệng đối phương, ban đối phương khỏi trò chơi nối từ trong 2 vòng nhất định. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=2,
        level="Cấp Thấp",
        required_target=True
    ),
]

list_special_items_cap_cao = [
    SpecialItem(
        item_id="cc_minus",
        item_name="Trừ Điểm Đối Phương",
        item_description=f"Kỹ năng này sẽ trừ đi 5 điểm của đối thủ trong trò chơi nối chữ, lưu ý là đối phương đã từng chơi trò này. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=5,
        level="Cấp Cao",
        required_target=True
    ),
    SpecialItem(
        item_id="cc_minus_all",
        item_name="Trừ Điểm Tất Cả Player",
        item_description=f"Kỹ năng này sẽ trừ 3 điểm cho tất cả player. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:{SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=3,
        level="Cấp Cao",
        required_target=False
    ),
    SpecialItem(
        item_id="cc_add",
        item_name="Cộng Điểm Bản Thân",
        item_description=f"Kỹ năng này sẽ cộng cho bản thân 5 điểm trong trò chơi nối chữ. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=5,
        level="Cấp Cao",
        required_target=False
    ),
    SpecialItem(
        item_id="cc_hint",
        item_name="Gợi Ý",
        item_description=f"Kỹ năng này sẽ gợi ý từ cần thiết để hoàn thành lượt chơi nối chữ hiện tại. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=0,
        level="Cấp Cao",
        required_target=False
    ),
    SpecialItem(
        item_id="cc_minus_first",
        item_name="Trừ Điểm Top 1",
        item_description=f"Kỹ năng này sẽ trừ 20 điểm của player top 1 trong bảng xếp hạng. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=20,
        level="Cấp Cao",
        required_target=False
    ),
    SpecialItem(
        item_id="cc_minus_second",
        item_name="Trừ Điểm Top 2",
        item_description=f"Kỹ năng này sẽ trừ 16 điểm của player top 2 trong bảng xếp hạng. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=16,
        level="Cấp Cao",
        required_target=False
    ),
    SpecialItem(
        item_id="cc_add_user",
        item_name="Cộng Điểm Đối Phương",
        item_description=f"Kỹ năng này sẽ cộng 5 điểm cho đối phương bất kỳ ngoại trừ bản thân, lưu ý là đối phương đã từng chơi trò này. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=5,
        level="Cấp Cao",
        required_target=True
    ),
    SpecialItem(
        item_id="cc_random_skill_dc",
        item_name="Đổi Điểm",
        item_description=f"Kỹ năng này sẽ đổi 2 điểm của bạn để đổi lấy một kỹ năng rank Đẳng Cấp ngẫu nhiên. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=2,
        level="Cấp Cao",
        required_target=False
    ),
    SpecialItem(
        item_id="cc_steal_point",
        item_name="Ăn Cắp Điểm",
        item_description=f"Kỹ năng này sẽ ăn cắp 6 điểm của đối phương. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n  {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=6,
        level="Cấp Cao",
        required_target=True
    ),
    SpecialItem(
        item_id="cc_protect",
        item_name="Bảo Hộ Giáp Gai",
        item_description=f"Kỹ năng này sẽ bảo hộ người chơi và phản lại kỹ năng của player khác. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=1,
        level="Cấp Cao",
        required_target=False
    ),
    SpecialItem(
        item_id="cc_ban",
        item_name="Câm Lặng",
        item_description=f"Kỹ năng này sẽ khoá miệng đối phương, ban đối phương khỏi trò chơi nối từ trong 4 vòng nhất định. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=4,
        level="Cấp Cao",
        required_target=True
    ),
]
list_special_items_dang_cap = [
    SpecialItem(
        item_id="dc_minus",
        item_name="Trừ Điểm Đối Phương",
        item_description=f"Kỹ năng này sẽ trừ đi 10 điểm của đối thủ trong trò chơi nối chữ, lưu ý là đối phương đã từng chơi trò này. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=10,
        level="Đẳng Cấp",
        required_target=True
    ),
    SpecialItem(
        item_id="dc_minus_all",
        item_name="Trừ Điểm Tất Cả Player",
        item_description=f"Kỹ năng này sẽ trừ 8 điểm cho tất cả player. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=8,
        level="Đẳng Cấp",
        required_target=False
    ),
    SpecialItem(
        item_id="dc_add",
        item_name="Cộng Điểm Bản Thân",
        item_description=f"Kỹ năng này sẽ cộng cho bản thân 10 điểm trong trò chơi nối chữ. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=10,
        level="Đẳng Cấp",
        required_target=False
    ),
    SpecialItem(
        item_id="dc_minus_first",
        item_name="Trừ Điểm Top 1",
        item_description=f"Kỹ năng này sẽ trừ 25 điểm của player top 1 trong bảng xếp hạng. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=25,
        level="Đẳng Cấp",
        required_target=False
    ),
    SpecialItem(
        item_id="dc_minus_second",
        item_name="Trừ Điểm Top 2",
        item_description=f"Kỹ năng này sẽ trừ 20 điểm của player top 2 trong bảng xếp hạng. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=16,
        level="Đẳng Cấp",
        required_target=False
    ),
    SpecialItem(
        item_id="dc_add_user",
        item_name="Cộng Điểm Cho Đối Phương",
        item_description=f"Kỹ năng này sẽ cộng 10 điểm cho đối phương bất kỳ ngoại trừ bản thân, lưu ý là đối phương đã từng chơi trò này. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=10,
        level="Đẳng Cấp",
        required_target=True
    ),
    SpecialItem(
        item_id="dc_del_skill",
        item_name="Huỷ Kỹ Năng Đối Thủ",
        item_description=f"Kỹ năng này sẽ xoá đi một kỹ năng ngẫu nhiên của đối phương. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=0,
        level="Đẳng Cấp",
        required_target=True
    ),
    SpecialItem(
        item_id="dc_steal_skill",
        item_name="Ăn Cắp Kỹ Năng Đối Thủ",
        item_description=f"Kỹ năng này sẽ ăn cắp một kỹ năng ngẫu nhiên của đối phương cho bản thân. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=0,
        level="Đẳng Cấp",
        required_target=True
    ),
    SpecialItem(
        item_id="dc_steal_point",
        item_name="Ăn Cắp Điểm",
        item_description=f"Kỹ năng này sẽ ăn cắp 9 điểm của đối phương. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n  {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=9,
        level="Đẳng Cấp",
        required_target=True
    ),
    SpecialItem(
        item_id="dc_protect",
        item_name="Bảo Hộ Hoàn Giáp",
        item_description=f"Kỹ năng này sẽ bảo hộ người chơi, phản lại kỹ năng của player khác và cướp luôn kỹ năng của đối thủ. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=1,
        level="Đẳng Cấp",
        required_target=False
    ),
]
list_special_items_toi_thuong = [
    SpecialItem(
        item_id="tt_minus_all",
        item_name="Trừ Điểm Tối Thượng",
        item_description=f"Kỹ năng này sẽ trừ đi 25 điểm của toàn bộ đối thủ trong trò chơi nối chữ. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=25,
        level="Tối Thượng",
        required_target=False
    ),
    SpecialItem(
        item_id="tt_swap_3",
        item_name="Thay Thế Top 3",
        item_description=f"Kỹ năng này sẽ lập tức cộng đủ điểm để đẩy người chơi lên top 3. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=5,
        level="Tối Thượng",
        required_target=False
    ),
    SpecialItem(
        item_id="tt_swap_2",
        item_name="Thay Thế Top 2",
        item_description=f"Kỹ năng này sẽ lập tức cộng đủ điểm để đẩy người chơi lên top 2. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này: {SlashCommand.SKILL_USE.value}",
        quantity = 1,
        point=5,
        level="Tối Thượng",
        required_target=False
    ),
]