from flask import Flask, render_template, request, flash, redirect, url_for
import os
from datetime import datetime
import logging

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

# 設定日誌
logging.basicConfig(level=logging.INFO)

# 店家資訊
SHOP_INFO = {
    'name': '金寶・停',
    'english_name': 'KAMPO·PAUSE',
    'price': 25,
    'duration': '1小時30分鐘',
    'whole_rental_price': 500,
    'whole_rental_hours': '19:00 - 21:00',
    'description': '都市中的寧靜綠洲，讓您暫時停下腳步',
    'features': [
        '冷氣開放',
        '高速Wi-Fi',
        '卡位座位',
        '圓形櫈',
        '充電插座',
        '安靜閱讀區'
    ],
    'usage_scenarios': [
        '臨時存放物品：比如購物袋、背包等，短暫離開時可以安心放置。',
        '簡單用餐：如果不想在嘈雜的餐廳，這裡可以作為安靜的簡餐區（注意保持衛生）。',
        '補覺小憩：利用舒適的環境快速恢復精力，尤其適合午休或長途出行間隙。',
        '學習備考：相對安靜的空間適合看資料、刷題，搭配充電功能很方便。',
        '視訊通話：比開放區域更私密，適合接打需要專注的工作或私人視訊電話。'
    ],
    'hours': {
        '週一到週日': '13:00 - 19:00',
        '全場租用時段': '19:00 - 21:00'
    },
    'telephone': '5173 8103'
}

def save_contact_to_file(name, email, phone, service_type, booking_date, message):
    """將聯絡資訊保存到文字檔案"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"""
        🎯 新客戶留言 - {timestamp}
        📋 客戶資訊：
        姓名: {name}
        電郵: {email}
        電話: {phone}
        服務類型: {service_type}
        預約日期: {booking_date if booking_date else '未指定'}
        
        💬 訊息內容：
        {message}
        
        ========================================
        
        """
        
        # 保存到檔案
        with open('contact_messages.txt', 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        # 同時在日誌中記錄（方便在 Render 後台查看）
        app.logger.info(f"📩 新客戶留言已保存: {name}, 電話: {phone}, 服務: {service_type}")
        
        return True
        
    except Exception as e:
        app.logger.error(f"❌ 保存客戶留言失敗: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html', shop=SHOP_INFO)

@app.route('/about')
def about():
    return render_template('about.html', shop=SHOP_INFO)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # 獲取表單資料
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        service_type = request.form.get('service_type', '')
        booking_date = request.form.get('booking_date', '')
        message = request.form.get('message', '').strip()
        
        # 基本驗證
        if not all([name, email, phone, service_type, message]):
            flash('請填寫所有必填欄位！', 'danger')
            return redirect(url_for('contact'))
        
        # 保存到檔案
        if save_contact_to_file(name, email, phone, service_type, booking_date, message):
            flash('感謝您的留言！我們會盡快回覆您。', 'success')
        else:
            flash('訊息發送失敗，請稍後再試或直接致電我們。', 'danger')
        
        return redirect(url_for('contact'))
    
    return render_template('contact.html', shop=SHOP_INFO)

@app.context_processor
def inject_now():
    return {'current_year': datetime.now().year}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)