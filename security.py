from fastapi import Request, HTTPException, status

# Giữ nguyên tên hàm verify_admin để các file khác gọi không bị lỗi
async def verify_admin(request: Request):
    # Tìm thẻ cookie có tên "session_token" do form đăng nhập cấp
    session_token = request.cookies.get("session_token")
    
    # Nếu chưa đăng nhập (không có cookie) hoặc thẻ bị sai -> Đá về trang /login
    if not session_token or session_token != "token_bi_mat_cua_tuan_viet":
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/"} 
        )
    
    return "tuanviet"