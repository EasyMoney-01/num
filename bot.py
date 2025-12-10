import os
import requests
import logging
import time
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_BASE = os.getenv("API_BASE", "https://anishexploits.site/api/api.php?key=exploits&num=")

# Validate environment variables
if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN not found in environment variables!")
    print("Please set BOT_TOKEN in Render environment variables")
    exit(1)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; Termux) Gecko/117.0 Firefox/117.0",
    "Accept": "application/json,text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8",
    "Referer": "https://anish-axploits.vercel.app/",
    "Connection": "keep-alive"
}

# Bot setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = "👋 *WELCOME TO Dark Shadow*\n\n"
    
    keyboard = [[KeyboardButton("📞 ENTER NUMBER")]]  
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)  
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "📞 ENTER NUMBER":
        await update.message.reply_text("📤 *Send Your 10-digit Number Without +91:*", parse_mode='Markdown')  
    else:  
        await process_number(update, context)

async def process_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.message.text.strip()
    
    if not number.isdigit() or len(number) != 10:  
        await update.message.reply_text("❌ *INVALID INPUT*\nPlease send 10-digit number only.", parse_mode='Markdown')  
        return  
    
    processing_msg = await update.message.reply_text("🔍 *Scanning Database...*", parse_mode='Markdown')  
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")  
    time.sleep(2)  
    
    result = await search_number_api(number)  
    
    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=processing_msg.message_id)  
    
    await update.message.reply_text(result, parse_mode='Markdown')

async def search_number_api(number):
    url = f"{API_BASE}{number}"
    
    try:  
        response = requests.get(url, headers=HEADERS, timeout=30)
        
        if response.status_code != 200:  
            return f"🛡️ Dark Shadow INFORMATION 🛡️\n\n🎯 TARGET: {number}\n\n❌ DATABASE ERROR\n\nServer connection failed.\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n🔐 END OF REPORT"
        
        try:
            data = response.json()
        except:
            return f"🛡️ Dark Shadow INFORMATION 🛡️\n\n🎯 TARGET: {number}\n\n❌ DATA ERROR\n\nInvalid response format.\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n🔐 END OF REPORT"
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_data, record_count = extract_user_data(data)
        
        if user_data:
            return format_cybersecurity_report(user_data, number, record_count, current_time)
        else:
            return f"🛡️ Dark Shadow INFORMATION 🛡️\n\n🎯 TARGET: {number}\n\n⚠️ NO INFORMATION FOUND\n\nNumber not found in database.\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n🔐 END OF REPORT"
        
    except requests.exceptions.Timeout:
        return f"🛡️ Dark Shadow INFORMATION 🛡️\n\n🎯 TARGET: {number}\n\n⏱️ TIMEOUT ERROR\n\nRequest timed out.\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n🔐 END OF REPORT"
    except requests.exceptions.ConnectionError:
        return f"🛡️ Dark Shadow INFORMATION 🛡️\n\n🎯 TARGET: {number}\n\n🌐 CONNECTION ERROR\n\nNetwork connection failed.\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n🔐 END OF REPORT"
    except Exception as e:  
        return f"🛡️ Dark Shadow INFORMATION 🛡️\n\n🎯 TARGET: {number}\n\n❌ SYSTEM ERROR\n\nUnknown error occurred.\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n🔐 END OF REPORT"

def extract_user_data(data):
    """Extract user data from different API formats"""
    user_data = None
    record_count = 1
    
    if isinstance(data, dict) and data.get('success') and data.get('result'):
        results = data.get('result', [])
        if results:
            user_data = results[0]
            record_count = len(results)
    elif isinstance(data, dict) and (data.get('mobile') or data.get('name')):
        user_data = data
    elif isinstance(data, list) and len(data) > 0:
        user_data = data[0]
        record_count = len(data)
    elif isinstance(data, dict) and data.get('status') == 'success':
        user_data = data.get('data', {})
    
    return user_data, record_count

def format_cybersecurity_report(user_data, number, record_count, current_time):
    """Format the cybersecurity report"""
    
    # Extract data
    phone = user_data.get('mobile', number)
    alt = user_data.get('alt_mobile')
    aadhar = user_data.get('id_number', user_data.get('aadhar'))
    name = user_data.get('name', 'None')
    father = user_data.get('father_name', 'None')
    address = user_data.get('address', '')
    circle = user_data.get('circle', '')
    
    # Clean address
    if address:
        address = address.replace('!', ' ').replace('|', ' ').replace('NA', '').replace('l\'', '').replace('Ii', '')
        address = ' '.join(address.split())
    
    # Build report
    report = "🛡️ Dark Shadow INFORMATION 🛡️\n\n"
    report += "🎯 TARGET INFORMATION\n"
    report += f"├─ 📞 Primary: {phone}\n"
    report += f"├─ 📱 Secondary: {alt if alt else 'None'}\n"
    report += f"└─ 🆔 Aadhar: {aadhar if aadhar else 'None'}\n\n"
    
    report += "👤 PROFILE\n"
    report += f"├─ 👤 Name: {name if name != 'None' else 'N/A'}\n"
    report += f"├─ 👨‍👦 Father: {father if father != 'None' else 'N/A'}\n"
    report += f"└─ 📍 Circle: {circle if circle else 'N/A'}\n\n"
    
    if address:
        if len(address) > 80:
            address = address[:77] + "..."
        report += f"📍 Address: {address}\n\n"
    
    report += "📊 DETAILS\n"
    report += f"├─ 📡 Network: {'JIO' if 'JIO' in circle.upper() else 'VODAFONE' if 'VODAFONE' in circle.upper() else 'AIRTEL' if 'AIRTEL' in circle.upper() else 'UNKNOWN'}\n"
    report += f"├─ 🗃️ Records: {record_count}\n"
    report += f"└─ ⏰ Time: {current_time}\n\n"
    
    report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    report += "🔐 END OF REPORT"
    
    return report

def main():
    print("\n" * 2)
    print("=" * 50)
    print("🛡️ Dark Shadow NUMBER SCANNER")
    print("📱 Status: INITIALIZING...")
    print("=" * 50)
    
    print(f"\n✅ Bot Token: {'✓ Loaded' if BOT_TOKEN else '✗ Missing'}")
    print(f"🌐 API Base: {API_BASE[:50]}...")
    
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("\n🤖 Bot started successfully!")
    print("🔍 Waiting for messages...\n")
    
    application.run_polling()

if __name__ == "__main__":
    main()
