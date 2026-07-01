# 📊 US Traffic Accident Dashboard (Streamlit)

Ứng dụng Dashboard tương tác trực quan hóa dữ liệu tai nạn giao thông nghiêm trọng tại Mỹ (Severity 4). Được xây dựng bằng **Streamlit**, **Plotly**, và **Scikit-learn** mang lại trải nghiệm phân tích mượt mà và trực quan như Power BI.

---

## ✨ Tính Năng Nổi Bật

1. **Bản đồ US Choropleth (Tổng quan)**:
   * Thể hiện số lượng tai nạn theo từng bang.
   * Tích hợp tính năng **Click-to-Filter**: Click trực tiếp vào một bang bất kỳ trên bản đồ để tự động chuyển sang chế độ phân tích chi tiết của bang đó.

2. **Bản đồ Chi Tiết Bang (Accident Locations)**:
   * Sử dụng Scatter Mapbox định vị chính xác tọa độ các vụ tai nạn (`Start_Lat`, `Start_Lng`).
   * Sử dụng thuật toán clustering **DBSCAN** để tự động nhóm các cụm tai nạn gần nhau và khoanh **vòng tròn đỏ (Hotspot Zones)** kèm tổng số lượng tai nạn của khu vực đó.

3. **Phân tích Khoảng Cách Ảnh Hưởng (Distance)**:
   * Biểu đồ tròn phân tích tỉ lệ khoảng cách đường bị ảnh hưởng do tai nạn (`Distance(mi)`) theo ngưỡng **> 2.5 miles** và **≤ 2.5 miles**.

4. **Phân tích Thời Gian & Thời Tiết**:
   * Biểu đồ phân tích số vụ tai nạn theo **Năm**, **Tháng** (từ 1 - 12), **Giờ trong ngày** (đầy đủ 24 giờ).
   * Nhãn x-axis được thiết kế thẳng đứng nằm ngang rõ ràng, dễ đọc.
   * Biểu đồ thời tiết hiển thị các điều kiện phổ biến nhất xảy ra tai nạn.

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy App (Local)

1. Mở Terminal và di chuyển vào thư mục này:
   ```bash
   cd APP_Visualization
   ```

2. Cài đặt các thư viện phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```

3. Khởi chạy ứng dụng:
   ```bash
   streamlit run app.py
   ```
   Ứng dụng sẽ tự động mở trên trình duyệt tại địa chỉ `http://localhost:8501`.

---

## ☁️ Hướng Dẫn Deploy Lên Streamlit Cloud

Để ứng dụng có thể chạy online và chia sẻ link cho người khác:
1. Đẩy thư mục này lên repository trên **GitHub**.
2. Đăng nhập vào [share.streamlit.io](https://share.streamlit.io/).
3. Bấm **New app** và điền cấu hình:
   * **Repository**: Repo GitHub của bạn.
   * **Main file path**: Điền chính xác là `APP_Visualization/app.py`.
4. Nhấn **Deploy**.
