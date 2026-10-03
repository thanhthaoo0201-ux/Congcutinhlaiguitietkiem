import streamlit as st
import math

# ==============================
# CẤU HÌNH TRANG
# ==============================

st.set_page_config(
    page_title="CÔNG CỤ TÍNH TIỀN GỬI TIẾT KIỆM_NGUYỄN THANH THẢO",      
    page_icon="💰",
    layout="centered"
)
st.image("logo.JPG")
st.title("CÔNG CỤ TÍNH TIỀN GỬI TIẾT KIỆM_NGUYỄN THANH THẢO")
# ==============================
# TIÊU ĐỀ
# ==============================

st.write("Tính lãi theo phương pháp **lãi đơn** hoặc **lãi kép**.")

st.divider()

# ==============================
# NHẬP THÔNG TIN
# ==============================

st.subheader("📋 Thông tin tiền gửi")

so_tien = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=10000000.0,
    step=100000.0,
    format="%.0f"
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    value=6.0,
    step=0.1,
    format="%.2f"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=120,
    value=12,
    step=1
)

hinh_thuc_lai = st.selectbox(
    "Hình thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc_lanh = st.selectbox(
    "Hình thức lãnh lãi",
    [
        "Lãnh lãi hàng tháng",
        "Lãnh lãi hàng quý",
        "Lãnh lãi cuối kỳ"
    ]
)

st.divider()

# ==============================
# HÀM ĐỊNH DẠNG TIỀN
# ==============================

def dinh_dang_tien(so):
    return f"{so:,.0f} VNĐ".replace(",", ".")


# ==============================
# TÍNH TOÁN
# ==============================

if st.button("🧮 TÍNH TIỀN LÃI", use_container_width=True):

    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất theo năm chuyển thành số thập phân
    r = lai_suat / 100

    # Thời gian tính theo năm
    so_nam = ky_han / 12

    # Xác định số tháng của một kỳ lãnh lãi
    if hinh_thuc_lanh == "Lãnh lãi hàng tháng":
        thang_moi_ky = 1
    elif hinh_thuc_lanh == "Lãnh lãi hàng quý":
        thang_moi_ky = 3
    else:
        thang_moi_ky = ky_han

    # Số kỳ lãnh lãi
    so_ky = math.ceil(ky_han / thang_moi_ky)

    # ==============================
    # LÃI ĐƠN
    # ==============================

    if hinh_thuc_lai == "Lãi đơn":

        # Tổng lãi:
        # I = P * r * t
        tong_lai = so_tien * r * so_nam

        tong_tien = so_tien + tong_lai

        # Lãi mỗi kỳ
        lai_moi_thang = so_tien * r / 12
        lai_dinh_ky = lai_moi_thang * thang_moi_ky

        # ==============================
        # TẠO BẢNG CHI TIẾT
        # ==============================

        du_lieu = []

        for i in range(1, so_ky + 1):

            thang_ket_thuc = min(i * thang_moi_ky, ky_han)

            so_thang_thuc_te = (
                thang_ket_thuc
                - (i - 1) * thang_moi_ky
            )

            lai_ky = so_tien * r / 12 * so_thang_thuc_te

            du_lieu.append({
                "Kỳ": i,
                "Thời gian": f"Tháng {thang_ket_thuc}",
                "Tiền lãi kỳ này": lai_ky,
                "Gốc": so_tien,
                "Tổng nhận": lai_ky
            })

    # ==============================
    # LÃI KÉP
    # ==============================

    else:

        # Số lần nhập lãi trong năm
        if hinh_thuc_lanh == "Lãnh lãi hàng tháng":
            n = 12
        elif hinh_thuc_lanh == "Lãnh lãi hàng quý":
            n = 4
        else:
            n = 1

        # Tổng số lần ghép lãi
        so_lan_ghep = n * so_nam

        # Công thức:
        # A = P(1 + r/n)^(nt)

        tong_tien = so_tien * (1 + r / n) ** so_lan_ghep

        tong_lai = tong_tien - so_tien

        # ==============================
        # TẠO BẢNG CHI TIẾT
        # ==============================

        du_lieu = []

        tien_hien_tai = so_tien

        for i in range(1, int(so_lan_ghep) + 1):

            lai_ky = tien_hien_tai * (r / n)

            tien_hien_tai += lai_ky

            thang_ket_thuc = i * (12 // n)

            du_lieu.append({
                "Kỳ": i,
                "Thời gian": f"Tháng {thang_ket_thuc}",
                "Tiền lãi kỳ này": lai_ky,
                "Gốc + lãi": tien_hien_tai
            })

        # Lãi định kỳ
        lai_dinh_ky = (
            du_lieu[0]["Tiền lãi kỳ này"]
            if du_lieu
            else 0
        )

    # ==============================
    # HIỂN THỊ KẾT QUẢ
    # ==============================

    st.success("✅ Tính toán thành công!")

    st.subheader("📊 Kết quả")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Tiền lãi định kỳ",
            dinh_dang_tien(lai_dinh_ky)
        )

    with col2:
        st.metric(
            "Tổng tiền lãi",
            dinh_dang_tien(tong_lai)
        )

    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            "Tiền gốc",
            dinh_dang_tien(so_tien)
        )

    with col4:
        st.metric(
            "Tổng gốc + lãi",
            dinh_dang_tien(tong_tien)
        )

    st.divider()

    # ==============================
    # THÔNG TIN TÓM TẮT
    # ==============================

    st.subheader("📝 Thông tin khoản gửi")

    st.write(
        f"**Số tiền gửi:** {dinh_dang_tien(so_tien)}"
    )

    st.write(
        f"**Lãi suất:** {lai_suat:.2f}%/năm"
    )

    st.write(
        f"**Kỳ hạn:** {ky_han} tháng"
    )

    st.write(
        f"**Phương pháp:** {hinh_thuc_lai}"
    )

    st.write(
        f"**Hình thức lãnh lãi:** {hinh_thuc_lanh}"
    )

    # ==============================
    # BẢNG CHI TIẾT
    # ==============================

    st.subheader("📅 Chi tiết tiền lãi theo từng kỳ")

    if hinh_thuc_lai == "Lãi đơn":

        # Đổi số thành chuỗi tiền để hiển thị đẹp
        bang_hien_thi = []

        for dong in du_lieu:
            bang_hien_thi.append({
                "Kỳ": dong["Kỳ"],
                "Thời gian": dong["Thời gian"],
                "Tiền lãi kỳ này": dinh_dang_tien(
                    dong["Tiền lãi kỳ này"]
                ),
                "Gốc": dinh_dang_tien(
                    dong["Gốc"]
                ),
                "Tổng nhận": dinh_dang_tien(
                    dong["Tổng nhận"]
                )
            })

    else:

        bang_hien_thi = []

        for dong in du_lieu:
            bang_hien_thi.append({
                "Kỳ": dong["Kỳ"],
                "Thời gian": dong["Thời gian"],
                "Tiền lãi kỳ này": dinh_dang_tien(
                    dong["Tiền lãi kỳ này"]
                ),
                "Gốc + lãi": dinh_dang_tien(
                    dong["Gốc + lãi"]
                )
            })

    st.table(bang_hien_thi)

    # ==============================
    # CÔNG THỨC
    # ==============================

    st.divider()

    st.subheader("📐 Công thức sử dụng")

    if hinh_thuc_lai == "Lãi đơn":

        st.latex(
            r"I = P \times r \times t"
        )

        st.write(
            "Trong đó: P là tiền gốc, r là lãi suất năm, "
            "t là thời gian tính theo năm."
        )

    else:

        st.latex(
            r"A = P\left(1+\frac{r}{n}\right)^{nt}"
        )

        st.write(
            "Trong đó: P là tiền gốc, r là lãi suất năm, "
            "n là số lần ghép lãi trong năm, t là số năm."
        )
