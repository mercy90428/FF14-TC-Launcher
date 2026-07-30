import base64
import urllib.parse
import cv2

def base32_encode(raw_bytes: bytes) -> str:
    return base64.b32encode(raw_bytes).decode('utf-8').replace('=', '')

def _parse_protobuf_varint(buffer, pos):
    result = 0
    shift = 0
    while pos < len(buffer):
        b = buffer[pos]
        pos += 1
        result |= (b & 0x7f) << shift
        if not (b & 0x80):
            break
        shift += 7
    return result, pos

def parse_ga_migration_uri(uri: str) -> str:
    parsed = urllib.parse.urlparse(uri)
    query = urllib.parse.parse_qs(parsed.query)
    data_b64 = query.get("data", [None])[0]
    if not data_b64:
        raise ValueError("無效的 Migration QR Code：找不到 data 欄位")

    raw_data = base64.b64decode(data_b64)
    pos = 0
    
    while pos < len(raw_data):
        tag, pos = _parse_protobuf_varint(raw_data, pos)
        field_number = tag >> 3
        wire_type = tag & 7

        if field_number == 1 and wire_type == 2:
            length, pos = _parse_protobuf_varint(raw_data, pos)
            param_bytes = raw_data[pos:pos+length]
            pos += length
            
            p_pos = 0
            secret = b""
            while p_pos < len(param_bytes):
                p_tag, p_pos = _parse_protobuf_varint(param_bytes, p_pos)
                p_field = p_tag >> 3
                p_wire = p_tag & 7
                if p_field == 1 and p_wire == 2:
                    s_len, p_pos = _parse_protobuf_varint(param_bytes, p_pos)
                    secret = param_bytes[p_pos:p_pos+s_len]
                    p_pos += s_len
                else:
                    if p_wire == 2:
                        l, p_pos = _parse_protobuf_varint(param_bytes, p_pos)
                        p_pos += l
                    elif p_wire == 0:
                        _, p_pos = _parse_protobuf_varint(param_bytes, p_pos)

            if secret:
                return base32_encode(secret)
        else:
            if wire_type == 2:
                length, pos = _parse_protobuf_varint(raw_data, pos)
                pos += length
            elif wire_type == 0:
                _, pos = _parse_protobuf_varint(raw_data, pos)

    raise ValueError("未能在 QR Code 中找到有效的 TOTP Key")

def parse_qr_text(raw_text: str) -> str:
    raw_text = raw_text.strip()
    
    if raw_text.startswith("otpauth-migration://"):
        return parse_ga_migration_uri(raw_text)
    elif raw_text.startswith("otpauth://"):
        parsed = urllib.parse.urlparse(raw_text)
        query = urllib.parse.parse_qs(parsed.query)
        secret_list = query.get("secret", [])
        if secret_list:
            return secret_list[0].upper()
        raise ValueError("無法從 otpauth:// 網址中提取 secret 參數")
    elif len(raw_text) in [16, 26, 32] and raw_text.isalnum():
        return raw_text.upper()
    else:
        raise ValueError("無法識別的 QR Code 格式")

def extract_secret_from_image(image_path: str) -> str:
    """傳入圖片路徑，自動讀取 QR Code 並解析出 Base32 Secret Key (支援中文路徑)"""
    detector = cv2.QRCodeDetector()
    
    # 解決 OpenCV cv2.imread 無法讀取中文/Unicode 路徑的問題
    try:
        img_array = np.fromfile(image_path, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    except Exception:
        img = None

    if img is None:
        raise FileNotFoundError("無法讀取圖片檔案，請確認路徑與檔案格式是否正確")

    val, pts, qr_code = detector.detectAndDecode(img)
    if not val:
        raise ValueError("圖片中未偵測到有效的 QR Code 條碼，請確認圖片清晰度")

    return parse_qr_text(val)
