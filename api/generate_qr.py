from flask import Flask, request, send_file
import qrcode
import io

app = Flask(__name__)

@app.route('/', methods=['POST'])
def generate_qr():
    data = request.form.get('data', 'Hello QRv1')
    fill_color = request.form.get('fill_color', '#000000')
    back_color = request.form.get('back_color', '#ffffff')
    transparent_bg = 'transparent_bg' in request.form
    box_size = int(request.form.get('box_size', 10))
    border = int(request.form.get('border', 4))

    qr = qrcode.QRCode(
        version=1,
        box_size=box_size,
        border=border,
        error_correction=qrcode.ERROR_CORRECT_M
    )
    qr.add_data(data)
    qr.make(fit=True)

    if transparent_bg:
        img = qr.make_image(fill_color=fill_color, back_color=None)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            data_img = img.getdata()
            new_data = []
            for item in data_img:
                if item[:3] == (255, 255, 255):
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            img.putdata(new_data)
    else:
        img = qr.make_image(fill_color=fill_color, back_color=back_color)

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    return send_file(buf, mimetype='image/png', as_attachment=True, download_name='qrcode.png')
