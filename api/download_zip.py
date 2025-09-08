from flask import Flask, request, send_file
import io, zipfile

app = Flask(__name__)

@app.route('/', methods=['POST'])
def download_zip():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as zf:
        for key in request.files:
            file = request.files[key]
            zf.writestr(file.filename, file.read())
    buf.seek(0)
    return send_file(buf, mimetype='application/zip', as_attachment=True, download_name="qr_history.zip")
