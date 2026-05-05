import json
import os
import sys

def build_tracnghiem():
    input_file = r"..\tracnghiem_LSD_chuong_gemini.json"
    output_file = r"data\tracnghiem.json"
    
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        try:
            questions = json.load(f)
        except json.JSONDecodeError:
            print("Error decoding JSON")
            return

    # Structure: Root -> Chương -> Nhóm (mỗi nhóm 50 câu) -> Câu hỏi -> Đáp án
    root = {
        "name": "BỘ ĐỀ TRẮC NGHIỆM LỊCH SỬ ĐẢNG (1131 CÂU)",
        "details": "Toàn bộ dữ liệu trắc nghiệm được hệ thống hóa sâu.",
        "children": []
    }
    
    # Giả sử file JSON là một list các object {question, options: [], answer}
    # Hoặc dict có key là chương
    if isinstance(questions, dict):
        # Nếu là dict
        for chuong, q_list in questions.items():
            chuong_node = {"name": chuong, "children": []}
            
            # Chia nhóm nhỏ để không bị lag
            chunk_size = 30
            for i in range(0, len(q_list), chunk_size):
                chunk = q_list[i:i+chunk_size]
                group_node = {"name": f"Nhóm {i+1} - {i+len(chunk)}", "children": []}
                for q in chunk:
                    q_node = {
                        "name": q.get('question', '')[:50] + "...",
                        "question": q.get('question', ''),
                        "options": q.get('options', []),
                        "answer": q.get('answer', '')
                    }
                    group_node["children"].append(q_node)
                chuong_node["children"].append(group_node)
            root["children"].append(chuong_node)
    elif isinstance(questions, list):
        # Nếu là list
        chuong_node = {"name": "Tất cả câu hỏi", "children": []}
        chunk_size = 30
        for i in range(0, len(questions), chunk_size):
            chunk = questions[i:i+chunk_size]
            group_node = {"name": f"Nhóm {i+1} - {i+len(chunk)}", "children": []}
            for q in chunk:
                q_node = {
                    "name": q.get('question', '')[:50] + "...",
                    "question": q.get('question', ''),
                    "options": q.get('options', []),
                    "answer": q.get('answer', '')
                }
                group_node["children"].append(q_node)
            chuong_node["children"].append(group_node)
        root["children"].append(chuong_node)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(root, f, ensure_ascii=False, indent=2)
    print(f"Generated {output_file}")

def build_timeline():
    # Cấu trúc thời gian siêu sâu 8 tầng cho Tiến trình lịch sử
    # Thế kỷ -> Giai đoạn -> Thập kỷ -> Năm -> Tháng -> Cấp độ sự kiện -> Sự kiện -> Chi tiết/Bài học
    root = {
        "name": "TIẾN TRÌNH LỊCH SỬ ĐẢNG (1858 - NAY)",
        "details": "Sơ đồ thời gian cực sâu 8 tầng, chứa 100% dữ liệu giáo trình và tài liệu phản hồi.",
        "children": [
            {
                "name": "Thế kỷ XIX (1858 - 1899)",
                "children": [
                  {
                      "name": "Giai đoạn Pháp xâm lược (1858-1884)",
                      "children": [
                          {
                              "name": "Thập kỷ 1850",
                              "children": [
                                  {
                                      "name": "Năm 1858",
                                      "children": [
                                          {
                                              "name": "Tháng 9",
                                              "children": [
                                                  {
                                                      "name": "Sự kiện quân sự",
                                                      "children": [
                                                          {
                                                              "name": "Pháp nổ súng tại Đà Nẵng (1/9/1858)",
                                                              "details": "Liên quân Pháp - Tây Ban Nha nổ súng tấn công bán đảo Sơn Trà. Nguyễn Tri Phương dựng phòng tuyến Liên Trì chặn giặc. Kế hoạch 'đánh nhanh thắng nhanh' của Pháp phá sản."
                                                          }
                                                      ]
                                                  }
                                              ]
                                          }
                                      ]
                                  },
                                  {
                                      "name": "Năm 1859",
                                      "children": [
                                          {
                                              "name": "Tháng 2",
                                              "children": [
                                                  {
                                                      "name": "Sự kiện quân sự",
                                                      "children": [
                                                          {
                                                              "name": "Pháp chiếm Gia Định (17/2/1859)",
                                                              "details": "Pháp chuyển hướng vào Nam Bộ, đánh chiếm thành Gia Định. Triều Nguyễn lúng túng, để mất cơ hội phản công. Khởi nghĩa Nguyễn Trung Trực đốt tàu Hy Vọng."
                                                          }
                                                      ]
                                                  }
                                              ]
                                          }
                                      ]
                                  }
                              ]
                          },
                          {
                              "name": "Thập kỷ 1860-1880",
                              "children": [
                                  {
                                      "name": "Các Hiệp ước đầu hàng",
                                      "children": [
                                          {
                                              "name": "Hiệp ước Nhâm Tuất (1862)",
                                              "children": [
                                                  {
                                                      "name": "Mất 3 tỉnh miền Đông",
                                                      "children": [
                                                          {
                                                              "name": "Hệ quả & Bài học",
                                                              "details": "Triều đình cắt Gia Định, Định Tường, Biên Hòa. Bồi thường chiến phí. Thể hiện sự nhu nhược của giai cấp phong kiến trước họa ngoại xâm."
                                                          }
                                                      ]
                                                  }
                                              ]
                                          },
                                          {
                                              "name": "Hiệp ước Quý Mùi (1883) & Giáp Thân (1884)",
                                              "children": [
                                                  {
                                                      "name": "Mất quyền độc lập",
                                                      "children": [
                                                          {
                                                              "name": "Việt Nam thành thuộc địa",
                                                              "details": "Thừa nhận nền bảo hộ của Pháp ở Bắc Kỳ và Trung Kỳ. Đánh dấu sự sụp đổ hoàn toàn của nhà nước phong kiến độc lập."
                                                          }
                                                      ]
                                                  }
                                              ]
                                          }
                                      ]
                                  }
                              ]
                          }
                      ]
                  }
                ]
            },
            {
                "name": "Thế kỷ XX (1900 - 1999)",
                "children": [
                    {
                        "name": "Giai đoạn 1900 - 1930 (Trước khi có Đảng)",
                        "children": [
                            {
                                "name": "Phong trào Yêu nước (Đầu thế kỷ)",
                                "children": [
                                    {
                                        "name": "Khuynh hướng Bạo động",
                                        "children": [
                                            {
                                                "name": "Phong trào Đông Du (1906-1908)",
                                                "children": [
                                                    {
                                                        "name": "Phan Bội Châu",
                                                        "children": [
                                                            {
                                                                "name": "Bài học thất bại",
                                                                "details": "Cử thanh niên sang Nhật học quân sự. Nhưng Pháp-Nhật cấu kết trục xuất. Thất bại do ảo tưởng vào đế quốc Nhật Bản."
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    },
                                    {
                                        "name": "Khuynh hướng Cải cách",
                                        "children": [
                                            {
                                                "name": "Phong trào Duy Tân",
                                                "children": [
                                                    {
                                                        "name": "Phan Châu Trinh",
                                                        "children": [
                                                            {
                                                                "name": "Bài học thất bại",
                                                                "details": "Khẩu hiệu 'Khai dân trí, chấn dân khí, hậu dân sinh'. Ảo tưởng dựa vào Pháp để cải cách ('xin giặc rủ lòng thương')."
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "name": "Thành lập Đảng (1930)",
                                "children": [
                                    {
                                        "name": "Năm 1930",
                                        "children": [
                                            {
                                                "name": "Tháng 2",
                                                "children": [
                                                    {
                                                        "name": "Hội nghị Thành lập Đảng (6/1 - 7/2/1930)",
                                                        "children": [
                                                            {
                                                                "name": "Cương lĩnh chính trị đầu tiên",
                                                                "details": "Hợp nhất 3 tổ chức CS. Bác Hồ soạn thảo Chánh cương, Sách lược vắn tắt. Xác định CM Tư sản dân quyền và Thổ địa CM. Đặt GPDT lên hàng đầu. Lực lượng toàn dân. Giải quyết triệt để khủng hoảng đường lối."
                                                            }
                                                        ]
                                                    }
                                                ]
                                            },
                                            {
                                                "name": "Tháng 10",
                                                "children": [
                                                    {
                                                        "name": "HNTW 1 (Hương Cảng)",
                                                        "children": [
                                                            {
                                                                "name": "Luận cương Chính trị 10/1930",
                                                                "details": "Trần Phú làm Tổng Bí thư. Đổi tên thành ĐCS Đông Dương. Hạn chế (Tả khuynh): Bỏ qua thời kỳ tư bổn, không nhấn mạnh GPDT, chỉ tập trung đấu tranh giai cấp (ruộng đất), bỏ rơi tiểu tư sản, tư sản dân tộc."
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "name": "Giai đoạn 1931 - 1945 (Tiến tới CMT8)",
                        "children": [
                            {
                                "name": "Năm 1941",
                                "children": [
                                    {
                                        "name": "Tháng 5",
                                        "children": [
                                            {
                                                "name": "Hội nghị TW 8 (Pác Bó)",
                                                "children": [
                                                    {
                                                        "name": "Chuyển hướng chiến lược",
                                                        "children": [
                                                            {
                                                                "name": "Hoàn chỉnh đường lối GPDT",
                                                                "details": "Do Bác Hồ chủ trì. Khẳng định GPDT là nhiệm vụ bức thiết nhất, cao hơn đấu tranh giai cấp. Thành lập Mặt trận Việt Minh. Xây dựng lực lượng vũ trang."
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "name": "Năm 1945",
                                "children": [
                                    {
                                        "name": "Tháng 8",
                                        "children": [
                                            {
                                                "name": "Tổng Khởi Nghĩa (14-30/8)",
                                                "children": [
                                                    {
                                                        "name": "Thắng lợi Cách mạng Tháng 8",
                                                        "children": [
                                                            {
                                                                "name": "Ý nghĩa & Bài học",
                                                                "details": "Thời cơ vàng (Nhật hàng Đồng minh). Giành chính quyền trong 15 ngày. Bài học: Nắm vững thời cơ, chớp thời cơ; Toàn dân nổi dậy trên nền tảng liên minh công-nông; Giương cao ngọn cờ ĐLDT."
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "name": "Giai đoạn 1945 - 1954 (Chống Pháp)",
                        "children": [
                            {
                                "name": "Năm 1946",
                                "children": [
                                    {
                                        "name": "Tháng 3",
                                        "children": [
                                            {
                                                "name": "Sách lược 'Hòa để tiến'",
                                                "children": [
                                                    {
                                                        "name": "Hiệp định Sơ bộ (6/3/1946)",
                                                        "children": [
                                                            {
                                                                "name": "Loại 20 vạn quân Tưởng",
                                                                "details": "Cho 1.5 vạn Pháp ra Bắc để đẩy Tưởng về nước, tránh đối phó nhiều kẻ thù. Pháp công nhận VN là Quốc gia tự do."
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    },
                                    {
                                        "name": "Tháng 12",
                                        "children": [
                                            {
                                                "name": "Bùng nổ chiến tranh (19/12/1946)",
                                                "children": [
                                                    {
                                                        "name": "Đường lối Kháng chiến",
                                                        "children": [
                                                            {
                                                                "name": "Toàn dân, toàn diện, lâu dài",
                                                                "details": "Bác ra Lời kêu gọi Toàn quốc kháng chiến. Phương châm: Dựa vào sức mình là chính, toàn dân, toàn diện, lâu dài."
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "name": "Năm 1954",
                                "children": [
                                    {
                                        "name": "Tháng 5",
                                        "children": [
                                            {
                                                "name": "Chiến dịch Điện Biên Phủ",
                                                "children": [
                                                    {
                                                        "name": "Phá sản Kế hoạch Nava",
                                                        "children": [
                                                            {
                                                                "name": "Kết thúc chiến tranh",
                                                                "details": "Đánh chắc tiến chắc. Bắt sống De Castries (7/5/1954). Buộc Pháp ký Hiệp định Geneva (21/7/1954), lập lại hòa bình ở Đông Dương."
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "name": "Giai đoạn 1954 - 1975 (Chống Mỹ)",
                        "children": [
                            {
                                "name": "Thập kỷ 1960",
                                "children": [
                                    {
                                        "name": "Đại hội III (9/1960)",
                                        "children": [
                                            {
                                                "name": "Đường lối 2 miền",
                                                "children": [
                                                    {
                                                        "name": "Miền Bắc (Quyết định nhất) - Miền Nam (Trực tiếp)",
                                                        "children": [
                                                            {
                                                                "name": "Đánh bại các chiến lược Mỹ",
                                                                "details": "Chiến tranh Đặc biệt (phá ấp chiến lược), Chiến tranh Cục bộ (Tổng tiến công Mậu Thân 1968), VN hóa chiến tranh."
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "name": "Năm 1975",
                                "children": [
                                    {
                                        "name": "Đại thắng Mùa Xuân",
                                        "children": [
                                            {
                                                "name": "Chiến dịch Hồ Chí Minh",
                                                "children": [
                                                    {
                                                        "name": "Giải phóng miền Nam",
                                                        "children": [
                                                            {
                                                                "name": "30/4/1975",
                                                                "details": "Đỉnh cao chiến dịch Tây Nguyên, Huế-Đà Nẵng. Hoàn thành CM DTDCND, non sông thu về một mối. Bài học: Giương cao ngọn cờ ĐLDT và CNXH."
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "name": "Giai đoạn 1975 - 1999 (Đổi mới)",
                        "children": [
                            {
                                "name": "Thập kỷ 1980",
                                "children": [
                                    {
                                        "name": "Đại hội VI (12/1986)",
                                        "children": [
                                            {
                                                "name": "Đổi Mới Toàn Diện",
                                                "children": [
                                                    {
                                                        "name": "Xóa bỏ Bao cấp",
                                                        "children": [
                                                            {
                                                                "name": "Kinh tế hàng hóa nhiều thành phần",
                                                                "details": "TBT Nguyễn Văn Linh. 'Nhìn thẳng vào sự thật'. Xóa bỏ cơ chế tập trung quan liêu bao cấp. Tập trung 3 chương trình: Lương thực, hàng tiêu dùng, xuất khẩu."
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "name": "Thập kỷ 1990",
                                "children": [
                                    {
                                        "name": "Đại hội VII (1991)",
                                        "children": [
                                            {
                                                "name": "Cương lĩnh 1991",
                                                "children": [
                                                    {
                                                        "name": "Kiên định CNXH",
                                                        "children": [
                                                            {
                                                                "name": "Vượt qua khủng hoảng",
                                                                "details": "Liên Xô sụp đổ. Đảng khẳng định CN Mác-Lênin và tư tưởng HCM làm nền tảng. Đa phương hóa ngoại giao. Ra khỏi khủng hoảng (ĐH 8 - 1996)."
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Thế kỷ XXI (2000 - Nay)",
                "children": [
                    {
                        "name": "Hội nhập và Bứt phá",
                        "children": [
                            {
                                "name": "Đại hội IX (2001)",
                                "children": [
                                    {
                                        "name": "Khái niệm mới",
                                        "children": [
                                            {
                                                "name": "Kinh tế thị trường định hướng XHCN",
                                                "children": [
                                                    {
                                                        "name": "Hội nhập quốc tế",
                                                        "children": [
                                                            {
                                                                "name": "WTO (2006)",
                                                                "details": "ĐH X (2006) cho Đảng viên làm kinh tế tư nhân. VN gia nhập WTO, tổ chức APEC."
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "name": "Đại hội XII (2016)",
                                "children": [
                                    {
                                        "name": "Chỉnh đốn Đảng",
                                        "children": [
                                            {
                                                "name": "Phòng chống tham nhũng",
                                                "children": [
                                                    {
                                                        "name": "Đốt lò",
                                                        "children": [
                                                            {
                                                                "name": "Không có vùng cấm",
                                                                "details": "TBT Nguyễn Phú Trọng khởi xướng. Kỷ luật nghiêm minh. HNTW 5 công nhận KT Tư nhân là động lực quan trọng."
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "name": "Đại hội XIII (2021) & Tầm nhìn XIV",
                                "children": [
                                    {
                                        "name": "Khát vọng hùng cường",
                                        "children": [
                                            {
                                                "name": "Mốc 2045",
                                                "children": [
                                                    {
                                                        "name": "Nước phát triển, thu nhập cao",
                                                        "children": [
                                                            {
                                                                "name": "Kỷ nguyên vươn mình",
                                                                "details": "Thực hiện 3 đột phá chiến lược (Thể chế, Hạ tầng, Nhân lực). ĐH 14 (2026) hướng tới Cách mạng Tinh - Gọn - Mạnh bộ máy tổ chức."
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    output_dir = r"D:\Download\Thi\LSD\Sơ Đồ Tư Duy Sâu\LSD\data"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, 'timeline.json'), 'w', encoding='utf-8') as f:
        json.dump(root, f, ensure_ascii=False, indent=2)
    print("Generated timeline.json")

    # Tạo file hochiminh.json, quocte.json đơn giản hơn một chút
    hochiminh = {
        "name": "HÀNH TRÌNH BÁC HỒ (1890 - 1969)",
        "details": "Toàn bộ diễn biến tư tưởng và chỉ đạo cách mạng của Chủ tịch Hồ Chí Minh",
        "children": [
            {
                "name": "Tìm đường cứu nước (1911-1920)",
                "children": [
                    {"name": "5/6/1911: Rời Bến Nhà Rồng", "details": "Tàu Latouche-Tréville, tên Văn Ba. Khảo sát Á, Âu, Phi, Mỹ."},
                    {"name": "18/6/1919: Yêu sách 8 điểm", "details": "Gửi Hội nghị Versailles (Nguyễn Ái Quốc). Rút ra bài học: phải bạo lực cách mạng."},
                    {"name": "7/1920: Đọc Luận cương Lênin", "details": "Chấm dứt khủng hoảng đường lối cứu nước. Tìm thấy CM Vô sản."},
                    {"name": "12/1920: Lập ĐCS Pháp", "details": "Bỏ phiếu gia nhập Quốc tế 3. Là người cộng sản VN đầu tiên."}
                ]
            },
            {
                "name": "Chuẩn bị lập Đảng (1921-1930)",
                "children": [
                    {"name": "Về Tư tưởng", "details": "Báo Người cùng khổ (1922), Bản án chế độ thực dân Pháp (1925), Đường Kách mệnh (1927)."},
                    {"name": "Về Tổ chức", "details": "Lập Hội VN CM Thanh niên (6/1925) tại Quảng Châu. Mở lớp đào tạo cán bộ."}
                ]
            },
            {
                "name": "Lãnh đạo 2 cuộc Kháng chiến (1941-1969)",
                "children": [
                    {"name": "28/1/1941: Về nước", "details": "Qua cột mốc 108 Pác Bó. Chủ trì HNTW 8, hoàn chỉnh đường lối GPDT."},
                    {"name": "1946: Dĩ bất biến, ứng vạn biến", "details": "Ký Hiệp định Sơ bộ và Tạm ước, gạt bỏ quân Tưởng."},
                    {"name": "19/12/1946: Lời kêu gọi Toàn quốc kháng chiến", "details": "Thà hy sinh tất cả, không chịu mất nước."},
                    {"name": "17/7/1966: Lời kêu gọi thiêng liêng", "details": "Không có gì quý hơn độc lập, tự do."}
                ]
            }
        ]
    }
    with open(os.path.join(output_dir, 'hochiminh.json'), 'w', encoding='utf-8') as f:
        json.dump(hochiminh, f, ensure_ascii=False, indent=2)
    print("Generated hochiminh.json")
    
    quocte = {
        "name": "BỐI CẢNH QUỐC TẾ & NGOẠI GIAO",
        "details": "Sự tác động của thế giới đến đường lối cách mạng Việt Nam.",
        "children": [
            {
                "name": "Chiến tranh Thế giới II (1939-1945)",
                "children": [
                    {"name": "Nhật hàng Đồng minh", "details": "Tạo Thời cơ vàng (15/8-2/9) để Tổng khởi nghĩa Tháng 8 thành công."}
                ]
            },
            {
                "name": "Chiến tranh Lạnh (1945-1991)",
                "children": [
                    {"name": "Cục diện 2 phe", "details": "Liên Xô viện trợ (từ 1950). Đảng khôn khéo giữ đường lối độc lập, tự chủ giữa mâu thuẫn Xô-Trung."},
                    {"name": "Sự sụp đổ của Liên Xô", "details": "Thập niên 90, VN mất nguồn viện trợ, buộc phải Đổi Mới toàn diện."}
                ]
            },
            {
                "name": "Hội nhập Toàn cầu hóa (1991-Nay)",
                "children": [
                    {"name": "Đa phương hóa, đa dạng hóa", "details": "Muốn là bạn, đối tác tin cậy. 1991 bình thường hóa với TQ. 1995 bình thường hóa với Mỹ, gia nhập ASEAN. 2007 WTO."},
                    {"name": "Ngoại giao Cây tre", "details": "Gốc vững, thân chắc, cành uyển chuyển. Nâng cấp Đối tác chiến lược toàn diện với Mỹ, Trung, Nga, Nhật, Hàn, Úc, Ấn."}
                ]
            }
        ]
    }
    with open(os.path.join(output_dir, 'quocte.json'), 'w', encoding='utf-8') as f:
        json.dump(quocte, f, ensure_ascii=False, indent=2)
    print("Generated quocte.json")

if __name__ == "__main__":
    build_tracnghiem()
    build_timeline()
