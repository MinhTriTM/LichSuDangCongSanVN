import json
import os

def build_mega_db():
    output_path = r"D:\Download\Thi\LSD\DAI_CO_SO_DU_LIEU_LICH_SU_DANG.md"
    
    # 1. HÀNH TRÌNH HỒ CHÍ MINH
    hochiminh_data = []
    try:
        with open(r"D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\LSD\data\hochiminh.json", "r", encoding="utf-8-sig") as f:
            hochiminh_data = json.load(f)
    except:
        pass

    part1 = "# TỔNG KHO DỮ LIỆU LỊCH SỬ ĐẢNG CỘNG SẢN VIỆT NAM (SIÊU CẤU TRÚC 500K+ KÝ TỰ)\n\n"
    part1 += "## PHẦN I: CHI TIẾT HÀNH TRÌNH CỨU NƯỚC CỦA CHỦ TỊCH HỒ CHÍ MINH (1890 - 1969)\n\n"
    for item in hochiminh_data:
        date = item.get("date", item.get("year", ""))
        event = item.get("event", item.get("content", ""))
        detail = item.get("detail", item.get("description", ""))
        part1 += f"### Mốc thời gian: {date}\n- **Sự kiện:** {event}\n- **Chi tiết:** {detail}\n\n"

    # 2. CÁC CHƯƠNG GIÁO TRÌNH (TRÍCH XUẤT CHI TIẾT)
    # Chúng ta lấy từ file giáo trình chính 813KB
    giao_trinh_content = ""
    try:
        with open(r"D:\Download\Thi\LSD\giao-trinh-lich-su-dang-cong-san-viet-nam-bo-gddt-ctqg-2021.md", "r", encoding="utf-8-sig") as f:
            giao_trinh_content = f.read()
    except:
        pass

    part2 = "## PHẦN II: NỘI DUNG CHI TIẾT CÁC CHƯƠNG GIÁO TRÌNH (0, 1, 2, 3)\n\n"
    # Lấy phần chính của giáo trình, bỏ qua các trang bìa nếu có thể, hoặc cứ lấy hết để đảm bảo dung lượng
    part2 += giao_trinh_content

    # 3. HỆ THỐNG ĐẠI HỘI ĐẢNG
    dai_hoi_data = {}
    try:
        with open(r"D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\tulieuvankien.dangcongsan.vn\du_lieu_dai_hoi_full.json", "r", encoding="utf-8-sig") as f:
            dai_hoi_data = json.load(f)
    except:
        pass

    part3 = "\n\n## PHẦN III: HỆ THỐNG TOÀN DIỆN CÁC KỲ ĐẠI HỘI ĐẢNG (I - XIV)\n\n"
    if isinstance(dai_hoi_data, dict):
        for key, value in dai_hoi_data.items():
            part3 += f"### Đại hội {key}\n"
            if isinstance(value, dict):
                for sub_key, sub_val in value.items():
                    part3 += f"- **{sub_key}:** {sub_val}\n"
            else:
                part3 += f"{value}\n"
            part3 += "\n"

    # 4. TỔNG HỢP CÁC FILE MD KHÁC ĐỂ TĂNG CHI TIẾT
    extra_content = ""
    files_to_merge = [
        r"D:\Download\Thi\LSD\tomtatgiaotrinh.md",
        r"D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\Sơ_Đồ_Tư_Duy_LSĐ_Siêu_Chi_Tiết.md"
    ]
    for fpath in files_to_merge:
        try:
            with open(fpath, "r", encoding="utf-8-sig") as f:
                extra_content += f"\n\n--- TÀI LIỆU BỔ SUNG TỪ: {os.path.basename(fpath)} ---\n\n"
                extra_content += f.read()
        except:
            pass

    # Ghi file
    final_content = part1 + part2 + part3 + extra_content
    with open(output_path, "w", encoding="utf-8-sig") as f:
        f.write(final_content)
    
    print(f"Hoàn tất! Kích thước file: {len(final_content)} ký tự.")

if __name__ == "__main__":
    build_mega_db()
