from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Selamat datang di aplikasi konfirmasi!"

@app.route('/confirm')
def confirm_credentials():
    email = request.args.get('email')
    if email:
        print(f"Kredensial untuk {email} sudah diganti.")
        return f"Terima kasih, {email}, kami telah menerima konfirmasi Anda."
    else:
        return "Tidak ada email yang diterima."

if __name__ == '__main__':
    # Menjalankan server Flask dengan mode debug
    app.run(debug=True, host='0.0.0.0', port=5000)
