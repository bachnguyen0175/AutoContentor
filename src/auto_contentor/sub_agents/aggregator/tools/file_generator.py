# src/auto_contentor/sub_agents/aggregator/tools.py
import pypandoc
import os
from datetime import datetime
from google.adk.tools import FunctionTool

# 1. Định nghĩa hàm Python thông thường với docstring chi tiết
def _save_report_as_document(markdown_content: str, campaign_name: str, output_format: str = "docx") -> str:
    """
    Chuyển đổi một chuỗi Markdown thành file PDF hoặc DOCX và lưu lại.

    Args:
        markdown_content: Nội dung Markdown của báo cáo.
        campaign_name: Tên của chiến dịch, được sử dụng cho tên file.
        output_format: Định dạng đầu ra mong muốn ('pdf' hoặc 'docx').

    Returns:
        Một chuỗi xác nhận đường dẫn của file đã lưu.
    """
    # Tạo thư mục 'reports' nếu chưa có
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)

    # Tạo tên file duy nhất và an toàn
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_campaign_name = "".join(c for c in campaign_name if c.isalnum() or c in (' ', '_')).rstrip()
    filename = f"{safe_campaign_name}_{timestamp}.{output_format}"
    output_path = os.path.join(output_dir, filename)

    try:
        # Sử dụng pandoc để chuyển đ���i
        pypandoc.convert_text(
            markdown_content,
            output_format,
            format="md",
            outputfile=output_path
        )
        return f"Báo cáo đã được lưu thành công tại: {output_path}"
    except Exception as e:
        return f"Lỗi khi tạo file {output_format}: {e}"

# 2. Bọc hàm bằng FunctionTool để tạo ra một tool mà agent có thể sử dụng
save_report_tool = FunctionTool(func=_save_report_as_document)
