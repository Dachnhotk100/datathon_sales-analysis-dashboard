import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from prophet import Prophet
from prophet.plot import plot_plotly
import warnings

# --- TẮT CẢNH BÁO ---
warnings.filterwarnings("ignore")
import logging
logging.getLogger('cmdstanpy').setLevel(logging.WARNING)

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="HYPE Analysis Dashboard", layout="wide", page_icon="🚀")

# --- 2. LOAD DỮ LIỆU ---
@st.cache_data
def load_data():
    try:
        # Đọc dữ liệu (Đảm bảo file csv nằm cùng thư mục với app.py)
        df = pd.read_csv('all_sales_data_cleaned.csv')
        
        # Xử lý ngày tháng
        df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
        df = df.dropna(subset=['Order Date'])
        
        # Feature Engineering
        df['Month'] = df['Order Date'].dt.month
        df['Hour'] = df['Order Date'].dt.hour
        
        # Tính cột Sales nếu chưa có
        if 'Sales' not in df.columns:
            df['Sales'] = df['Quantity Ordered'] * df['Price Each']
        
        # Tách thành phố nếu chưa có
        if 'City' not in df.columns:
            df['City'] = df['Purchase Address'].apply(lambda x: x.split(',')[1].strip())
            
        return df
    except FileNotFoundError:
        return None

# Gọi hàm load_data
df = load_data()

# --- 3. KIỂM TRA DỮ LIỆU ---
if df is None:
    st.error("❌ LỖI: Không tìm thấy file 'all_sales_data_cleaned.csv'.")
    st.warning("👉 Hãy đảm bảo file CSV này nằm CÙNG THƯ MỤC với file app.py")
    st.stop() # Dừng chương trình nếu không có dữ liệu

# --- 4. SIDEBAR & BỘ LỌC (Chỉ chạy khi df đã có dữ liệu) ---
st.sidebar.title("🎛️ Bộ lọc dữ liệu")
st.sidebar.info("Team Datathon: [Future Coders]")

# Lấy danh sách thành phố
city_list = ["Tất cả"] + list(df['City'].unique())
selected_city = st.sidebar.selectbox("Chọn Thành Phố:", city_list)

# Lọc dữ liệu
if selected_city != "Tất cả":
    df_filtered = df[df['City'] == selected_city]
else:
    df_filtered = df

# --- 5. KPI CHÍNH ---
st.title("🚀 Phân Tích Xu Hướng HYPE Sản Phẩm")
st.markdown("---")

total_sales = df_filtered['Sales'].sum()
total_orders = df_filtered.shape[0]

# Kiểm tra nếu dữ liệu lọc không rỗng
if not df_filtered.empty:
    best_product = df_filtered.groupby('Product')['Sales'].sum().idxmax()
    highest_sale_month = df_filtered.groupby('Month')['Sales'].sum().idxmax()
else:
    best_product = "N/A"
    highest_sale_month = "N/A"

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Tổng Doanh Thu", f"${total_sales:,.0f}")
col2.metric("📦 Tổng Đơn Hàng", f"{total_orders:,.0f}")
col3.metric("🔥 Sản Phẩm Hot Nhất", best_product)
col4.metric("📅 Tháng Cao Điểm", f"Tháng {highest_sale_month}")

st.markdown("---")

# --- 6. CÁC TAB PHÂN TÍCH ---
tab1, tab2, tab3 = st.tabs(["📊 Tổng Quan Xu Hướng", "🌍 Khu Vực & Thời Gian", "🔮 Dự Báo AI (Prophet)"])

with tab1:
    col_left, col_right = st.columns([2, 1])
    with col_left:
        if not df_filtered.empty:
            monthly_sales = df_filtered.groupby('Month')['Sales'].sum().reset_index()
            fig_trend = px.line(monthly_sales, x='Month', y='Sales', 
                                title='Xu hướng HYPE chung (Doanh thu theo tháng)',
                                markers=True, line_shape='spline')
            fig_trend.update_layout(xaxis=dict(tickmode='linear', dtick=1))
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.warning("Không có dữ liệu để hiển thị")
        
    with col_right:
        if not df_filtered.empty:
            product_sales = df_filtered.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
            fig_prod = px.bar(product_sales, x='Sales', y='Product', orientation='h',
                              title='Top 10 Sản phẩm Doanh thu cao nhất',
                              color='Sales', color_continuous_scale='Viridis')
            fig_prod.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_prod, use_container_width=True)

with tab2:
    col_time, col_city = st.columns(2)
    with col_time:
        if not df_filtered.empty:
            hourly_sales = df_filtered.groupby('Hour')['Order ID'].count().reset_index()
            hourly_sales.columns = ['Hour', 'Orders']
            fig_hour = px.line(hourly_sales, x='Hour', y='Orders', 
                               title='Khung giờ "Vàng" đặt hàng',
                               markers=True, color_discrete_sequence=['#FF5733'])
            fig_hour.update_layout(xaxis=dict(tickmode='linear', dtick=1))
            st.plotly_chart(fig_hour, use_container_width=True)

    with col_city:
        if selected_city == "Tất cả":
            city_sales = df.groupby('City')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=False)
            fig_city = px.bar(city_sales, x='City', y='Sales',
                              title='Doanh thu theo Thành Phố',
                              color='Sales', color_continuous_scale='Magma')
            st.plotly_chart(fig_city, use_container_width=True)
        else:
            st.info(f"Đang xem dữ liệu chi tiết của riêng thành phố: {selected_city}")
            if not df_filtered.empty:
                city_top_prod = df_filtered.groupby('Product')['Quantity Ordered'].sum().nlargest(5).reset_index()
                fig_city_prod = px.pie(city_top_prod, values='Quantity Ordered', names='Product', 
                                       title=f'Sản phẩm bán chạy tại {selected_city}', hole=0.4)
                st.plotly_chart(fig_city_prod, use_container_width=True)

with tab3:
    st.header("🔮 Dự báo Xu hướng HYPE Tương lai")
    st.write("Sử dụng mô hình **Facebook Prophet** để dự đoán doanh thu.")
    
    # Gom nhóm dữ liệu theo ngày (Dùng toàn bộ data df gốc để train cho chính xác)
    df_prophet = df.groupby(df['Order Date'].dt.date)['Sales'].sum().reset_index()
    df_prophet.columns = ['ds', 'y']
    df_prophet['ds'] = pd.to_datetime(df_prophet['ds'])
    
    days_to_predict = st.slider("Chọn số ngày muốn dự đoán:", 7, 90, 30)
    
    if st.button("Chạy Dự Báo Ngay"):
        with st.spinner('Đang huấn luyện mô hình AI...'):
            try:
                # Huấn luyện mô hình
                m = Prophet(seasonality_mode='multiplicative', daily_seasonality=True)
                m.fit(df_prophet)
                
                # Dự báo
                future = m.make_future_dataframe(periods=days_to_predict)
                forecast = m.predict(future)
                
                # Vẽ biểu đồ
                fig_forecast = plot_plotly(m, forecast)
                st.plotly_chart(fig_forecast, use_container_width=True)
                
                # Hiển thị bảng số liệu
                st.subheader("Dữ liệu dự báo chi tiết")
                st.dataframe(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(10))
            except Exception as e:
                st.error(f"Có lỗi khi chạy mô hình: {e}")