# Creations Bot Discord


**Creations Bot (Creation 1, Creation 2)** là bot discord được xây dựng nhằm mục đích quản lý, kiểm soát server cá nhân và thực hiện rất nhiều mục đích, phục vụ nhiều nhu cầu cá nhân khác nhau trên nền tảng discord. Hiện tại, đây là GitHub repository về bot Creation 1 và Creation 2, và showcase các ứng dụng của nó trên nền tảng discord, server cá nhân.

- Ngôn ngữ sử dụng: **Python**
- Database: **MongoDB**
- AI Model: **Gemini 1.5 Flash**
- Nền tảng hoạt động: **Discord**
- Host Server: **Raspberry Pi**

![messenger](https://i.imgur.com/i6tG9cW.png)


# Tính năng nổi bật
### Tích hợp A.I. với tính cách độc nhất

Creation 1 và Creation 2 là hai bot được tạo ra song song và tận dụng API lẫn model Gemini có sẵn để build lên một tính cách khác biệt và thiên hướng giống con người. (*Phần quan trọng là do API Gemini free á*)

![ai_sample](https://i.imgur.com/6WfHFr6.gif)

Nhờ A.I. với tính cách đặc biệt, Creation 1 và Creation 2 có thể đóng vai là một member bất khả dĩ, có thể tương tác cùng, và có thể tấu hài trong server.

### Quản lý server cá nhân

Cả hai bot Creation 1 và Creation 2 đều có chức năng và nhiệm vụ khác nhau nhằm duy trì trật và đảm bảo server cá nhân hoạt động đúng luật để tạo một sân chơi lành mạnh.

- Lệnh xoá tin nhắn thông qua message ID.
- Lệnh cô lập user vào một channel cố định.
- Lệnh báo cáo nội dung tin nhắn đến quản trị viên.
- Log lại tin nhắn, log lại hình ảnh đã xoá và gửi đến một channel cố định.

![report-command](https://media.discordapp.net/attachments/1257003289485119499/1263962176020807800/chrome_ImDGLSrqyn.gif?ex=66efdb42&is=66ee89c2&hm=f0283ec465a37069a8f53d53db3b96e3d2b3e0a63126c584f4cf344393851da9&=)

![snipe-command](https://i.imgur.com/mlGfBuU.gif)


### Tích hợp mini-game
Bot Creation có sẵn một số mini-game nổi bật và độc lạ, khác biệt với những mini-game thường thấy và luôn cập nhật và chỉnh sửa thêm theo thời gian và theo kiến nghị từ user:
- Nối từ tiếng Anh
- Nối từ tiếng Việt
- Đoán từ tiếng Việt
- Đoán từ tiếng Anh
- Sự Thật Hay Thách Thức
- Tung đồng xu
- Câu cá
- Bài cào, tài xỉu, tung xúc xắc, nổ hũ,...
- Chiến đấu theo lượt
- Ngoài ra còn nhiều mini game khác, có thể dùng bot để biết thêm

![noi-tu-english](https://i.imgur.com/WXoia3n.gif)

## Sử dụng Source Code

### Clone the Repository (Phương án khuyên dùng)
Nếu đã cài đặt Github desktop thì đây là phương án tôi khuyên dùng, vì như thế bạn sẽ có thể nhanh chóng cập nhật cùng phiên bản mới nhất. Và đây cũng là cách phù hợp nhất nếu bạn có ý định đóng góp thêm vào dự án này. 

Hãy dùng các lệnh sau để clone rep về:

    $ mkdir Creation-Bot
    $ cd Creation-Bot
    $ git clone https://github.com/dakie2305/My-Discord-Creation-Bot


### Luôn cập nhật bản mới nhất
Tôi không quan tâm bạn chọn tải source code về bằng kiểu gì, nhưng việc cập nhật phiên bản mới nhất là rất quan trọng, vì trong đó sẽ chứa các tính năng (thậm chí là bugs mới). Nhớ hãy gắn **Sao(*)** cho project này để được thông báo khi tôi update bản mới nhé. 

## Build

Trước khi chúng ta nhảy vào build và chạy bot, hãy đảm bảo kỹ lưỡng những yếu tố sau.

 - Python >= 3.10.6
 - pip install -r requirements.txt
 - Một file `.env` đã chuẩn bị như sau.
 - Hai Gemini API key.


`.env` cần phải nhập đủ key như sau:

    $ BOT_TOKENN = TOKEN_CREATION_1
    $ OPEN_AI_KEY = API_KEY
    $ GOOGLE_CLOUD_KEY = GOOGLE_CLOUD_KEY
    $ BOT_TOKEN_NO2 = TOKEN_CREATION_2
    $ GOOGLE_CLOUD_KEY_2 = GOOGLE_CLOUD_KEY_2


 1. Start MyCreation1.py
 2. Start MyCreation2.py

Hai Creation 1 và Creation 2 được thiết kế nhằm phục vụ và quản lý server cá nhân, một số chức năng đặc biệt sẽ không hỗ trợ server ngoài.

| Thông tin thêm  | Đường dẫn |
| ------------- |:-------------:|
| Discord      | [Link Server](https://discord.gg/kKzyJAuccr)     |
| Creation 1      | [Top.gg Page](https://top.gg/bot/1257305865124581416)     |
| Creation 2      | [Top.gg Page](https://top.gg/bot/1257713292445618239)     |

---
<p align="center">
<strong>Copyright © Darkie 2025</strong>
</p>