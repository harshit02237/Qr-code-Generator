from flask import Flask, request, send_file, render_template_string
import qrcode
from io import BytesIO

app = Flask(__name__)

# HTML Template for Home Page
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
        img { margin-top: 20px; border: 2px solid white; }
    </style>
</head>
<body>
    <h1>UPI QR Code Generator</h1>
    <form action="/generate" method="post">
        <input type="text" name="upi_id" placeholder="Enter UPI ID" required><br>
        <input type="text" name="amount" placeholder="Enter Amount" required><br>
        <button type="submit">Generate QR Code</button>
    </form>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate_qr():
    upi_id = request.form.get('upi_id')
    amount = request.form.get('amount')

    if not upi_id or not amount:
        return "Error: Please enter UPI ID and amount.", 400

    # UPI Payment URL (Universal for all apps)
    upi_url = f"upi://pay?pa={upi_id}&pn=Recipient%20Name&mc=1234&am={amount}&cu=INR"
    
    # Generate QR Code
    qr = qrcode.make(upi_url)
    img_io = BytesIO()
    qr.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # Port required for Render
