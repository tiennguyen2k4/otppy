from flask import Flask, request, session, render_template_string
import random
import time
from datetime import datetime,timedelta
import pyotp
app = Flask(__name__)
app.secret_key = 'secret_key_here'

my_phone_number = '0868386258'

def generate_otp() -> str:
    totp = pyotp.TOTP('base32secret3232')
    otp_code = totp.now()
    return otp_code

def send_otp(phone_number: str, otp: str) -> bool:
    if phone_number == my_phone_number:  # Kiểm tra số điện thoại trong session
        session['otp'] = otp  # Lưu OTP vào session
        session['otp_time'] = time.time()  # Lưu thời gian gửi OTP vào session
        print(f'OTP đã được gửi đến {phone_number}: {otp}')
        return True
    else:
        print('Số điện thoại không hợp lệ')
        return False

html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            margin: 0;
            padding: 0;
            background: rgb(15,250,114);
            background: linear-gradient(67deg, rgba(15,250,114,1) 0%, rgba(0,255,255,1) 77%);
        }
        .main {
            width: 100vw;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .box_main {
            height: 200px;
            width: 400px;
            background-color: white;
            border-radius: 10px;
            padding: 20px;
        }
        .inputPhoneNumber {
            padding-top: 10px;
            width: 100%;
            height: 40%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        input {
            width: 350px;
            height: 50px;
            border: none;
            border-bottom: 2px solid black;
            padding-bottom: 0px;
            line-height: 1px;
            font-size: 25px;
            text-align: center;
        }
        input:focus {
            border-bottom: 2px solid #007bff;
            outline: none;
            padding-bottom: 0px;
        }
        .box_bottom {
            width: 100%;
            height: 30%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 35px; 
        }
        button {
            width: 300px;
            height: 50px;
            background: rgb(15,250,114);
            border: none;
            border-radius: 10px;
            color: white;
            font-size: 30px;
            font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
            margin: 0 auto;
            display: block;
            text-align: center;
        }
        button:hover {
            background-color: aqua;
        }
    </style>
    <title>Document</title>
</head>
<body>
    <div class="main">
        <div class="box_main">
            <form action="/" method="post">
                <div class="inputPhoneNumber">
                    <input type="text" name="phoneNumber" value="" placeholder="Nhập số điện thoại của bạn">
                </div>
                <div class="box_bottom">
                    <div class="send">
                        <button type="submit">
                            SEND
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</body>
</html>

'''

verify_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        body, html {
            height: 100%;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: rgba(0,255,255,1);
        }

        .box {
            width: 350px;
            height: 300px;
            background-color: white;
            border: 2px solid #ccc;
            border-radius: 10px;
            display: inline;
            justify-content: center;
            align-items: center;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        }
        
        .main1{
            width: 100%;
            height: 30%;
            background-color: white;
            display: flex;
            border-top-right-radius: 10px;
            border-top-left-radius: 10px;
            flex-direction: column; /* Đảm bảo nội dung xếp theo chiều dọc, không bị chia cột */
            text-align: center; /* Căn giữa văn bản */
            
        }
        .main2{
            width: 100%;
            height: 18%;
            background-color: white;
            display: flex;
            justify-content: space-around; /* Đặt khoảng cách đều giữa các ô nhập */
    align-items: center;
        }
        .main3{
            width: 100%;
            height: 15%;
            display: flex;
            align-items: center;  /* Center vertically */
            justify-content: center;
        }
        #otp-timer {
            font-size: 16px;
            color:black;
        }
        .main4{
            width: 100%;
            height: 20%;
            display: flex;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
            align-items: center;  /* Center vertically */
            justify-content: center;
        }
        .main1 h1 {
            margin-bottom:25px; /* Giảm khoảng cách giữa h1 và p */
        }
        
        .main1 p {
            margin-top: 0;
            font-size: 16px; /* Xóa khoảng cách trên của thẻ p */
        }
        .main2 input {
            width: 45px; /* Chiều rộng của mỗi ô nhập */
            height: 45px; /* Chiều cao của mỗi ô nhập */
            background-color: rgb(251, 247, 247); /* Màu nền của ô nhập */
            border: 1px solid #181616; /* Viền của ô nhập */
            border-radius: 5px; /* Bo góc của ô nhập */
            font-size: 20px; /* Kích thước chữ */
            text-align: center; /* Căn giữa văn bản trong ô nhập */
            color: rgb(82, 24, 90); /* Màu chữ của ô nhập */
            margin: -5px; /* Khoảng cách giữa các ô nhập */
        }
        .main3 p{
            font-size: 20px;
            text-align: center;
        }
        button {
            width: 200px;
            height: 50px;
            background: rgb(73, 239, 142);
            border: none;
            border-radius: 10px;
            color: black;
            font-size: 20px;
            font-family:'Times New Roman', Times, serif;
            margin: 0 auto;
            display: block;
            text-align: center;
        }
        button:hover {
            background-color: rgb(153, 241, 243);
        }


    </style>
    <script>
        window.onload = function() {
            // Xử lý ẩn số điện thoại
            const phoneInfo = document.getElementById('sdt');
            const phoneNumber = phoneInfo.textContent.match(/\d{10}/);
            
            if (phoneNumber) {
                const maskedNumber = phoneNumber[0].slice(0, 3) + '*****' + phoneNumber[0].slice(-2);
                phoneInfo.innerHTML = phoneInfo.innerHTML.replace(phoneNumber[0], maskedNumber);
            }

            // Xử lý đếm ngược thời gian OTP
            let countdown = 30;
            const countdownElement = document.getElementById('countdown');
            const otpTimerElement = document.getElementById('otp-timer');
        
            const timer = setInterval(function() {
                countdown--;
                countdownElement.textContent = countdown + 's';
                
                if (countdown <= 0) {
                    clearInterval(timer);
                    otpTimerElement.innerHTML = 'Mã OTP đã hết hiệu lực';
                }
            }, 1000);
        };
    </script>
    
</head>
<body>
    <div class="box">
        <form action="/verify" method="post" class="otp-form">
            <div class="main1">
                <h1>Xác thực mã OTP</h1>
                <p id="sdt">Mã OTP đã được gửi đến số điện thoại 0868386258<br>
                Vui lòng nhập mã OTP</p>
            </div>
            <div class="main2">
                <input type="text" maxlength="1" class="b1" name="otp1">
                <input type="text" maxlength="1" class="b2" name="otp2">
                <input type="text" maxlength="1" class="b3" name="otp3">
                <input type="text" maxlength="1" class="b4" name="otp4">
                <input type="text" maxlength="1" class="b5" name="otp5">
                <input type="text" maxlength="1" class="b6" name="otp6">
            </div>
            <div class="main3">
                <p id="otp-timer">Mã OTP sẽ hết hạn trong <span id="countdown">30s</span></p>
            </div>
            <div class="main4">
                <div class="send">
                    <button type="submit">
                        Xác nhận
                    </button>
                </div>
            </div>
        </form>
    </div>
</body>


</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phone_number_input = request.form.get('phoneNumber')
        if phone_number_input != my_phone_number:
            return '''
                <div style="text-align: center; color: red; font-size: 24px">
                    <p>Số điện thoại không hợp lệ!</p>
                </div>
            '''
        otp = generate_otp()
        if send_otp(phone_number_input, otp):
            session['otp'] = otp  
            session['phoneNumber'] = phone_number_input  # Store the phone number in the session
            return render_template_string(verify_template)
        else:
            return 'Không thể gửi OTP vì số điện thoại không hợp lệ.'   
    return render_template_string(html_template)

@app.route('/verify', methods=['POST'])
def verify_otp():
    otp1 = request.form.get('otp1', '')
    otp2 = request.form.get('otp2', '')
    otp3 = request.form.get('otp3', '')
    otp4 = request.form.get('otp4', '')
    otp5 = request.form.get('otp5', '')
    otp6 = request.form.get('otp6', '')
    
    # Nối tất cả các giá trị thành một chuỗi OTP
    otp_input = otp1 + otp2 + otp3 + otp4 + otp5 + otp6
    if 'otp' in session:
        current_time = time.time()
        otp_sent_time = session.get('otp_time', 0)
        if current_time - otp_sent_time <= 30:
            if otp_input == session['otp']:
                print('Xác thực OTP thành công.')
                return render_template_string('''
            <html>
                <head>
                    <style>
                        body {
                            background-color: #f2f2f2;
                            font-family: Arial, sans-serif;
                        }
                        .container {
                            width: 50%;
                            margin: 40px auto;
                            text-align: center;
                        }
                        .success {
                            color: #0f0;
                            font-size: 24px;
                            font-weight: bold;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <p class="success">Xác thực OTP thành công!</p>
                    </div>
                </body>
            </html>
        ''')
            else:
                print('Mã OTP không hợp lệ, xác thực thất bại.')
                return render_template_string('''
            <html>
                <head>
                    <style>
                        body {
                            background-color: #f2f2f2;
                            font-family: Arial, sans-serif;
                        }
                        .container {
                            width: 50%;
                            margin: 40px auto;
                            text-align: center;
                        }
                        .error {
                            color: #f00;
                            font-size: 24px;
                            font-weight: bold;
                        }
                    </style>
                </head>
                <body>
                    <div class="container"> 
                        <p class="error">Mã OTP không hợp lệ, xác thực thất bại!</p> 
                    </div
                    </div> 
                </body> 
            </html>
        ''')
        else:
            print('OTP đã hết hạn.')
            return render_template_string('''
                <html>
                <head>
                    <style>
                        body {
                            background-color: #f2f2f2;
                            font-family: Arial, sans-serif;
                        }
                        .container {
                            width: 50%;
                            margin: 40px auto;
                            text-align: center;
                        }
                        .success {
                            color: #0f0;
                            font-size: 24px;
                            font-weight: bold;
                        }
                    </style>
                </head>
                <body>
                <div class='container'>
                    
                <p class='success'>Xác thực thất bại <br> OTP đã hết hạn. Vui lòng thử lại.</p>
                </body>
            </html>
            ''')
    else:
        print('Không có OTP nào được gửi.')
        return render_template_string('''
            <html>
                <head>
                    <style>
                        body {
                            background-color: #f2f2f2;
                            font-family: Arial, sans-serif;
                        }
                        .container {
                            width: 50%;
                            margin: 40px auto;
                            text-align: center;
                        }
                        .success {
                            color: #0f0;
                            font-size: 24px;
                            font-weight: bold;
                        }
                    </style>
                </head>
                <body>
                <div class="container">
            <p class='success'> Lỗi <br> Không có OTP nào được gửi.</p>
            </div>
                </body>
            </html>
            
        ''')

if __name__ == '__main__':
    app.run(debug=True)