from flask import Flask, request, render_template_string
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

# HTML Template with dynamic QR Code display
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UPI QR Code Generator</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background-color: #222; color: white; padding: 20px; }
        input { padding: 10px; margin: 5px; width: 250px; background: #333; color: white; border: 1px solid white; }
        button { padding: 10px 20px; background: #ff9800; color: white; border: none; cursor: pointer; }
        img { margin-top: 20px; border: 2px solid white; max-width: 250px; }
    </style>
</head>
<body>
    <h1>UPI QR Code Generator</h1>
    <form action="/" method="post">
        <input type="text" name="upi_id" placeholder="Enter UPI ID" required><br>
        <input type="text" name="amount" placeholder="Enter Amount" required><br>
        <button type="submit">Generate QR Code</button>
    </form>
    {% if qr_code %}
        <h2>Scan to Pay:</h2>
        <img src="data:image/png;base64,{{ qr_code }}" alt="QR Code">
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    qr_code = None
    if request.method == 'POST':
        upi_id = request.form.get('upi_id')
        amount = request.form.get('amount')

        if upi_id and amount:
            upi_url = f"upi://pay?pa={upi_id}&pn=Recipient%20Name&mc=1234&am={amount}&cu=INR"
            qr = qrcode.make(upi_url)
            img_io = BytesIO()
            qr.save(img_io, 'PNG')
            img_io.seek(0)
            qr_code = base64.b64encode(img_io.getvalue()).decode('utf-8')
    
    return render_template_string(HTML_TEMPLATE, qr_code=qr_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
