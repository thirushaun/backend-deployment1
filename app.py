from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS  # Import CORS to handle cross-origin requests
import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Flask configuration
app.config['SECRET_KEY'] = '20061968'
app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'  # Yahoo SMTP server
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'thirushaun74@yahoo.com'
app.config['MAIL_PASSWORD'] = 'tnqcbjvhjvuieevs'  # Yahoo App Password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Sample Public Holidays (Johor)
PUBLIC_HOLIDAYS = [
    datetime.date(2025, 1, 29),  # Chinese New Year
    datetime.date(2025, 1, 30),  # Chinese New Year
    datetime.date(2025, 2, 11),  # Thaipusam
    datetime.date(2025, 3, 3),  # Awal Ramadan
    datetime.date(2025, 3, 23),  # Sultan of Johor's Birthday
    datetime.date(2025, 3, 24),  # Sultan of Johor's Birthday
    datetime.date(2025, 3, 31),  # Hari Raya Aidilfitri
    datetime.date(2025, 4, 1),  # Hari Raya Aidilfitri Holiday
    datetime.date(2025, 5, 12),  # Wesak Day
    datetime.date(2025, 6, 2),  # Agong's Birthday
    datetime.date(2025, 6, 7),  # Hari Raya Haji
    datetime.date(2025, 6, 29),  # Awal Muharram
    datetime.date(2025, 7, 31),  # Hari Hol Almarhum Sultan Iskandar
    datetime.date(2025, 8, 31),  # Merdeka Day
    datetime.date(2025, 9, 1),  # Merdeka Day Holiday
    datetime.date(2025, 9, 5),  # Prophet Muhammad's Birthday
    datetime.date(2025, 9, 16),  # Malaysia Day
    datetime.date(2025, 10, 20),  # Deepavali
    datetime.date(2025, 12, 25) # Christmas
]

appointments = []

@app.route('/')
def home():
    return 'Backend is running!'

@app.route('/api/health', methods=['GET'])
def health_check():
    return 'Backend is healthy!'

@app.route('/api/book', methods=['POST'])
def book_appointment():
    data = request.json

    name = data.get('name')
    email = data.get('email')  # Patient's email
    phone = data.get('phone')
    service = data.get('service')
    date = datetime.datetime.strptime(data.get('date'), '%Y-%m-%d').date()
    time = data.get('time')

    if date in PUBLIC_HOLIDAYS:
        return jsonify({"error": "Selected date is a public holiday. Please choose another date."}), 400

    appointment = {
        "name": name,
        "email": email,
        "phone": phone,
        "service": service,
        "date": str(date),
        "time": time
    }
    appointments.append(appointment)

    # Send Email to Patient and Clinic
    try:
        # Email to the patient
        patient_msg = Message('Appointment Confirmation',
                              sender='thirushaun74@yahoo.com',
                              recipients=[email])
        patient_msg.body = f"Dear {name},\n\nYour appointment for {service} is confirmed on {date} at {time}.\n\nRegards,\nKlinik Mediviron"
        mail.send(patient_msg)

        # Email to the clinic
        clinic_msg = Message('New Appointment Notification',
                             sender='thirushaun74@yahoo.com',
                             recipients=['thirushaun74@yahoo.com'])
        clinic_msg.body = f"New Appointment Details:\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nService: {service}\nDate: {date}\nTime: {time}"
        mail.send(clinic_msg)

    except Exception as e:
        return jsonify({"error": "Failed to send emails.", "details": str(e)}), 500

    return jsonify({"message": "Appointment booked successfully!", "appointment": appointment}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5002)
