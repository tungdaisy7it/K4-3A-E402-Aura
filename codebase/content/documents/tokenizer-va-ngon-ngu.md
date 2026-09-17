# Tokenizer và ngôn ngữ

## Tokenizer học các cụm ký tự

Tokenizer biểu diễn văn bản bằng các đơn vị là cụm ký tự xuất hiện thường xuyên, thay vì mặc định coi mỗi từ hay mỗi ký tự là một token. Cách chia này được xác định bởi bộ mã hóa của từng họ mô hình.

## Khác biệt giữa các ngôn ngữ

Một cụm quen thuộc trong dữ liệu có thể nằm trong một token, còn từ ít gặp hoặc từ có dấu có thể bị tách thành nhiều token. Vì vậy không nên dùng một tỉ lệ cố định giữa số từ và số token cho mọi ngôn ngữ hoặc mọi tokenizer.
