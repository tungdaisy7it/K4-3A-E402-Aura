# Token, ngữ cảnh và chi phí

## Đơn vị xử lý của mô hình

Đơn vị cơ bản mà mô hình nhận và sinh ra là token; token có thể là một từ, một phần của từ, dấu câu hoặc một cụm ký tự. Mô hình làm việc trên chuỗi token thay vì trực tiếp trên số tiếng mà người đọc nhìn thấy.

## Vì sao số token khác số tiếng

Tokenizer cắt văn bản theo các cụm ký tự đã học, nên số token không bằng số tiếng và có thể thay đổi khi dùng tokenizer khác. Muốn có con số chính xác, cần chạy đúng tokenizer trên đúng nội dung.

## Token đầu vào và đầu ra

Chi phí của một lần gọi được tính từ token đầu vào và token đầu ra; hai phần cần được đếm riêng theo bảng giá của mô hình. Khi đề bài chỉ hỏi nội dung đầu vào, token của phần trả lời chưa sinh không thuộc kết quả cần đếm.
