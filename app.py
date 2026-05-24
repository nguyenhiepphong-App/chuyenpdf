import streamlit as st
import pandas as pd
import tabula
import io

st.set_page_config(page_title="App Gộp File Điểm", layout="wide")
st.title("📊 Ứng dụng Gộp Dữ liệu Điểm PDF")

# Nút 1: Lấy file mẫu
file_mau = st.file_uploader("1. Tải file MẪU (để lấy tiêu đề và dữ liệu ban đầu)", type=["pdf"])

# Nút 2: Tải các file còn lại
files_con_lai = st.file_uploader("2. Tải các file còn lại (để lấy dữ liệu ghép vào)", type=["pdf"], accept_multiple_files=True)

if file_mau and files_con_lai:
    if st.button("🚀 Xử lý và Gộp dữ liệu"):
        try:
            # Xử lý file mẫu
            dfs = tabula.read_pdf(file_mau, pages='all', multiple_tables=True)
            df_final = pd.concat(dfs, ignore_index=True)
            schema = df_final.columns.tolist() # Lưu khuôn mẫu
            
            # Xử lý các file còn lại
            for f in files_con_lai:
                data_list = tabula.read_pdf(f, pages='all', multiple_tables=True)
                for df_part in data_list:
                    # Gán lại header theo khuôn mẫu
                    df_part.columns = schema 
                    # Đổ dữ liệu vào bảng chính
                    df_final = pd.concat([df_final, df_part], ignore_index=True)
            
            st.success("Ghép thành công!")
            st.dataframe(df_final.head(10))
            
            # Tải file Excel
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df_final.to_excel(writer, index=False)
            
            st.download_button("📥 Tải file Excel tổng hợp", data=buffer, file_name="TongHop_Diem.xlsx")
            
        except Exception as e:
            st.error(f"Có lỗi xảy ra: {e}")
