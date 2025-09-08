import qrcode
import io
import base64

def handler(request):
    data = request.get("data", "Hello QRv1")
    fill_color = request.get("fill_color", "#000000")
    back_color = request.get("back_color", "#ffffff")

    qr = qrcode.QRCode(version=1, box_size=10, border=4, error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
    return {
        "statusCode": 200,
        "headers": { "Content-Type": "application/json" },
        "body": '{"qr": "data:image/png;base64,' + encoded + '"}'
    }
