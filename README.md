# 🚀 HYPE Sales Analysis & Forecasting Dashboard

Dự án phân tích dữ liệu bán hàng trực tuyến toàn diện, kết hợp với bảng điều khiển tương tác (Interactive Dashboard) bằng **Streamlit** và mô hình dự báo học máy **Facebook Prophet** để dự đoán xu hướng doanh thu trong tương lai.

---

## 📂 Cấu trúc Thư mục Dự án

```text
sales-analysis-dashboard/
│
├── all_sales_data.csv          # Dữ liệu gốc (được gộp từ 12 tháng bán hàng)
├── all_sales_data_cleaned.csv  # Dữ liệu đã được làm sạch và bổ sung các đặc trưng (Feature Engineering)
├── app.py                      # Mã nguồn chính của ứng dụng Streamlit Dashboard
├── bt01.py                     # Script Python hỗ trợ thu thập dữ liệu (Web Scraping với Selenium)
├── sales_data_daily.csv        # Dữ liệu tổng hợp theo ngày
├── sales_data_final.csv        # Dữ liệu tổng hợp hoàn thiện phục vụ phân tích
└── README.md                   # Tài liệu mô tả dự án

🌟 Các Tính năng Chính của Dashboard (app.py)
🎛️ Bộ lọc Tương tác thông minh:

Cho phép lọc dữ liệu theo từng khu vực thành phố cụ thể hoặc xem toàn hệ thống.

📊 Tổng Quan Xu Hướng (Overview Tab):

Thống kê các chỉ số cốt lõi (KPIs): Tổng doanh thu, tổng đơn hàng, sản phẩm hot nhất và tháng cao điểm.

Biểu đồ xu hướng doanh thu theo tháng và Top 10 sản phẩm mang lại doanh thu cao nhất.

🌍 Khu Vực & Khung Giờ Vàng (Regional & Time Analysis Tab):

Xác định khung giờ đặt hàng "vàng" trong ngày để tối ưu hóa chiến dịch quảng cáo.

Phân tích cơ cấu doanh thu và sản phẩm bán chạy theo từng thành phố.

🔮 Dự Báo AI (Prophet Forecasting Tab):

Ứng dụng thuật toán Facebook Prophet (với tùy chỉnh chu kỳ theo mùa) để dự báo doanh thu bán hàng trong 7 đến 90 ngày tới, hỗ trợ lập kế hoạch kinh doanh.

🛠️ Công nghệ & Thư viện Sử dụng
Ngôn ngữ lập trình: Python

Giao diện Web App: Streamlit

Xử lý & Làm sạch Dữ liệu: Pandas, NumPy

Trực quan hóa: Plotly, Matplotlib, Seaborn

Dự báo Chuỗi Thời gian (Time Series Forecasting): Facebook Prophet

Thu thập dữ liệu: Selenium
