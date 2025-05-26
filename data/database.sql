DROP USER IF EXISTS 'quizuser'@'localhost';
CREATE USER 'quizuser'@'localhost' IDENTIFIED BY 'matkhau123';
GRANT ALL PRIVILEGES ON quiz_game.* TO 'quizuser'@'localhost';
FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS quiz_game;
USE quiz_game;

-- Bảng người chơi
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    score INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng chủ đề
CREATE TABLE IF NOT EXISTS topics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Bảng câu hỏi
CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    topic_id INT,
    question TEXT NOT NULL,
    option_a VARCHAR(255) NOT NULL,
    option_b VARCHAR(255) NOT NULL,
    option_c VARCHAR(255) NOT NULL,
    option_d VARCHAR(255) NOT NULL,
    correct_option ENUM('A', 'B', 'C', 'D') NOT NULL,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
);

-- Thêm các chủ đề
INSERT IGNORE INTO topics (name) VALUES
('Văn'), ('Hóa'), ('Ẩm thực'), ('Vật lý'), ('Toán');

-- Câu hỏi chủ đề Văn
INSERT INTO questions (topic_id, question, option_a, option_b, option_c, option_d, correct_option) VALUES
((SELECT id FROM topics WHERE name = 'Văn'), 'Tác phẩm "Truyện Kiều" là của ai?', 'Nguyễn Du', 'Nguyễn Trãi', 'Hồ Xuân Hương', 'Lê Quý Đôn', 'A'),
((SELECT id FROM topics WHERE name = 'Văn'), 'Từ nào sau đây là từ láy?', 'Trăng', 'Đẹp', 'Lấp lánh', 'Cao', 'C'),
((SELECT id FROM topics WHERE name = 'Văn'), 'Thể thơ lục bát gồm mấy câu?', '2 câu', '3 câu', '4 câu', '5 câu', 'A'),
((SELECT id FROM topics WHERE name = 'Văn'), 'Nhân vật chính trong "Chuyện người con gái Nam Xương" là ai?', 'Vũ Nương', 'Thúy Kiều', 'Thúy Vân', 'Tấm', 'A'),
((SELECT id FROM topics WHERE name = 'Văn'), 'Biện pháp tu từ nào được dùng trong câu: "Con ong làm mật yêu hoa"?', 'Ẩn dụ', 'Nhân hóa', 'Hoán dụ', 'So sánh', 'B'),
((SELECT id FROM topics WHERE name = 'Văn'), 'Câu nào có thành phần trạng ngữ?', 'Tôi đi học.', 'Trời mưa to.', 'Sáng nay, tôi đi học.', 'Tôi là học sinh.', 'C'),
((SELECT id FROM topics WHERE name = 'Văn'), 'Thể thơ nào phổ biến trong ca dao?', 'Ngũ ngôn', 'Lục bát', 'Thất ngôn', 'Tự do', 'B'),
((SELECT id FROM topics WHERE name = 'Văn'), 'Tác phẩm "Lão Hạc" là của ai?', 'Nam Cao', 'Ngô Tất Tố', 'Nguyễn Công Hoan', 'Tô Hoài', 'A'),
((SELECT id FROM topics WHERE name = 'Văn'), 'Từ nào đồng nghĩa với "học hành"?', 'Học tập', 'Hành động', 'Làm việc', 'Chơi', 'A'),
((SELECT id FROM topics WHERE name = 'Văn'), 'Câu nào là câu ghép?', 'Tôi học, em chơi.', 'Tôi đi.', 'Em hát.', 'Họ chạy.', 'A');

-- Câu hỏi chủ đề Hóa
INSERT INTO questions (topic_id, question, option_a, option_b, option_c, option_d, correct_option) VALUES
((SELECT id FROM topics WHERE name = 'Hóa'), 'Nguyên tố nào có ký hiệu là O?', 'Oxi', 'Vàng', 'Bạc', 'Hydro', 'A'),
((SELECT id FROM topics WHERE name = 'Hóa'), 'Chất nào sau đây là hợp chất?', 'Nước', 'Sắt', 'Đồng', 'Vàng', 'A'),
((SELECT id FROM topics WHERE name = 'Hóa'), 'Công thức hóa học của nước là gì?', 'CO2', 'O2', 'H2O', 'NaCl', 'C'),
((SELECT id FROM topics WHERE name = 'Hóa'), 'Axit có pH bao nhiêu?', 'Lớn hơn 7', 'Bằng 7', 'Nhỏ hơn 7', 'Không xác định', 'C'),
((SELECT id FROM topics WHERE name = 'Hóa'), 'Kim loại nào dẫn điện tốt nhất?', 'Sắt', 'Đồng', 'Nhôm', 'Bạc', 'D'),
((SELECT id FROM topics WHERE name = 'Hóa'), 'Chất nào sau đây là bazơ?', 'NaOH', 'HCl', 'CO2', 'H2O', 'A'),
((SELECT id FROM topics WHERE name = 'Hóa'), 'Hợp chất muối phổ biến nhất là?', 'NaCl', 'CO2', 'CH4', 'H2O', 'A'),
((SELECT id FROM topics WHERE name = 'Hóa'), 'Chất nào sau đây không tan trong nước?', 'Đường', 'Muối', 'Dầu ăn', 'Axit', 'C'),
((SELECT id FROM topics WHERE name = 'Hóa'), 'Phản ứng hóa học nào giải phóng khí CO2?', 'Đốt cháy than', 'Điện phân nước', 'Nung vôi', 'Tạo muối', 'A'),
((SELECT id FROM topics WHERE name = 'Hóa'), 'Chất nào dùng để khử chua đất?', 'Vôi sống', 'Muối', 'Cát', 'Nước', 'A');

-- Câu hỏi chủ đề Ẩm thực
INSERT INTO questions (topic_id, question, option_a, option_b, option_c, option_d, correct_option) VALUES
((SELECT id FROM topics WHERE name = 'Ẩm thực'), 'Phở là món ăn truyền thống của nước nào?', 'Trung Quốc', 'Thái Lan', 'Việt Nam', 'Hàn Quốc', 'C'),
((SELECT id FROM topics WHERE name = 'Ẩm thực'), 'Bánh chưng được làm từ nguyên liệu chính nào?', 'Gạo nếp', 'Bột mì', 'Khoai tây', 'Ngô', 'A'),
((SELECT id FROM topics WHERE name = 'Ẩm thực'), 'Món ăn nào sau đây là món ngọt?', 'Canh chua', 'Bánh flan', 'Phở bò', 'Bún mắm', 'B'),
((SELECT id FROM topics WHERE name = 'Ẩm thực'), 'Nước mắm thường được làm từ gì?', 'Đậu nành', 'Thịt', 'Cá', 'Tôm', 'C'),
((SELECT id FROM topics WHERE name = 'Ẩm thực'), 'Gỏi cuốn có nguồn gốc từ vùng nào?', 'Miền Trung', 'Miền Bắc', 'Miền Tây', 'Miền Nam', 'D'),
((SELECT id FROM topics WHERE name = 'Ẩm thực'), 'Món ăn nào là đặc sản Huế?', 'Bún bò Huế', 'Bánh cuốn', 'Phở', 'Bún chả', 'A'),
((SELECT id FROM topics WHERE name = 'Ẩm thực'), 'Gia vị nào không thể thiếu trong nước mắm chấm chả giò?', 'Đường', 'Muối', 'Ớt', 'Hành', 'C'),
((SELECT id FROM topics WHERE name = 'Ẩm thực'), 'Bún riêu thường có thành phần nào sau đây?', 'Cua đồng', 'Cá hồi', 'Mực', 'Tôm hùm', 'A'),
((SELECT id FROM topics WHERE name = 'Ẩm thực'), 'Món nào sau đây được nướng?', 'Bánh mì', 'Cơm tấm', 'Chả giò', 'Gà nướng', 'D'),
((SELECT id FROM topics WHERE name = 'Ẩm thực'), 'Bánh xèo thường ăn kèm với gì?', 'Cơm', 'Cháo', 'Rau sống', 'Bánh mì', 'C');

INSERT INTO questions (topic_id, question, option_a, option_b, option_c, option_d, correct_option) VALUES
((SELECT id FROM topics WHERE name = 'Vật lý'), 'Đơn vị đo lực trong hệ SI là gì?', 'Jun', 'Niu-tơn', 'Oát', 'Mét', 'B'),
((SELECT id FROM topics WHERE name = 'Vật lý'), 'Tốc độ ánh sáng trong chân không là bao nhiêu?', '3x10^8 m/s', '3x10^6 m/s', '3x10^5 m/s', '3x10^3 m/s', 'A'),
((SELECT id FROM topics WHERE name = 'Vật lý'), 'Ai là người phát minh định luật vạn vật hấp dẫn?', 'Newton', 'Einstein', 'Galilei', 'Faraday', 'A'),
((SELECT id FROM topics WHERE name = 'Vật lý'), 'Nhiệt độ nước sôi ở điều kiện tiêu chuẩn là bao nhiêu?', '90°C', '100°C', '110°C', '120°C', 'B'),
((SELECT id FROM topics WHERE name = 'Vật lý'), 'Nguồn điện nào sau đây là nguồn điện một chiều?', 'Ổ cắm điện', 'Máy phát điện', 'Pin', 'Biến áp', 'C'),
((SELECT id FROM topics WHERE name = 'Vật lý'), 'Thiết bị dùng để đo cường độ dòng điện là gì?', 'Vôn kế', 'Ampe kế', 'Nhiệt kế', 'Đồng hồ đo điện trở', 'B'),
((SELECT id FROM topics WHERE name = 'Vật lý'), 'Chất nào sau đây dẫn điện tốt nhất?', 'Thủy tinh', 'Nhôm', 'Đồng', 'Gỗ', 'C'),
((SELECT id FROM topics WHERE name = 'Vật lý'), 'Vật lý học nghiên cứu về điều gì?', 'Sự sống', 'Vật chất và năng lượng', 'Tinh thần con người', 'Ngôn ngữ', 'B'),
((SELECT id FROM topics WHERE name = 'Vật lý'), 'Một vật rơi tự do, lực nào tác động lên nó?', 'Lực ma sát', 'Lực từ', 'Trọng lực', 'Lực đàn hồi', 'C'),
((SELECT id FROM topics WHERE name = 'Vật lý'), 'Vật nào sau đây là chất rắn?', 'Nước', 'Không khí', 'Đá', 'Dầu', 'C');

INSERT INTO questions (topic_id, question, option_a, option_b, option_c, option_d, correct_option) VALUES
((SELECT id FROM topics WHERE name = 'Toán'), 'Kết quả của 5 x 6 là gì?', '30', '35', '25', '36', 'A'),
((SELECT id FROM topics WHERE name = 'Toán'), 'Phân số 1/2 bằng bao nhiêu phần trăm?', '25%', '50%', '75%', '100%', 'B'),
((SELECT id FROM topics WHERE name = 'Toán'), 'Chu vi hình tròn được tính bằng công thức nào?', '2πr', 'πr^2', '4πr', 'πd', 'A'),
((SELECT id FROM topics WHERE name = 'Toán'), 'Số nguyên tố là gì?', 'Chỉ chia hết cho 1 và chính nó', 'Là số chia hết cho 2', 'Là số chẵn', 'Là số lẻ', 'A'),
((SELECT id FROM topics WHERE name = 'Toán'), 'Kết quả của căn bậc hai của 49 là?', '6', '7', '8', '9', 'B'),
((SELECT id FROM topics WHERE name = 'Toán'), 'Giá trị của π (pi) xấp xỉ bằng bao nhiêu?', '2.14', '3.14', '4.13', '5.12', 'B'),
((SELECT id FROM topics WHERE name = 'Toán'), 'Một tam giác có tổng các góc bằng bao nhiêu độ?', '90', '180', '270', '360', 'B'),
((SELECT id FROM topics WHERE name = 'Toán'), 'Số nào là số chẵn?', '3', '5', '6', '9', 'C'),
((SELECT id FROM topics WHERE name = 'Toán'), 'Kết quả của 12 + 8 / 2 là?', '10', '16', '20', '18', 'B'),
((SELECT id FROM topics WHERE name = 'Toán'), 'Số thập phân 0.25 tương đương với phân số nào?', '1/2', '1/4', '1/3', '1/5', 'B');
