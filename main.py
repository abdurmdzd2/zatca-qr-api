from flask import Flask, request, jsonify
import base64
import qrcode
from io import BytesIO

app = Flask(__name__)

def encode_tlv(tag, value):
    value_bytes = value.encode('utf-8')
    length = len(value_bytes)
    return bytes([tag, length]) + value_bytes

@app.route("/generate-zatca-qr", methods=["POST"])
def generate_qr():
    data = request.json

    tlv = b''.join([
        encode_tlv(1, data["company_name"]),
        encode_tlv(2, data["vat_number"]),
        encode_tlv(3, data["invoice_date"]),
        encode_tlv(4, data["invoice_total"]),
        encode_tlv(5, data["vat_total"])
    ])

    tlv_base64 = base64.b64encode(tlv).decode()

    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(tlv_base64)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    return jsonify({
        "tlv_base64": tlv_base64,
        "qr_image_base64": img_base64
    })

if __name__ == "__main__":
    app.run()
