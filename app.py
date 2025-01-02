from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS  # Import CORS to handle cross-origin requests
import datetime

# Initialize Flask app
app = Flask(__name__)

# CORS - Enable it for your frontend domain (Netlify)
CORS(app, resources={r"/*": {"origins": "https://dulcet-dasik-6d8140.netlify.app"}})  # Replace with your frontend domain

# Flask configuration
app.config['SECRET_KEY'] = '20061968'
app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'thirushaun74@yahoo.com'
app.config['MAIL_PASSWORD'] = 'tnqcbjvhjvuieevs'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Public holidays (example)
PUBLIC_HOLIDAYS = [
    datetime.date(2025, 1, 29),  # Chinese New Year
    datetime.date(2025, 1, 30),  # Chinese New Year
    datetime.date(2025, 2, 11),  # Thaipusam
    datetime.date(2025, 3, 3),  # Awal Ramadan
    # Add other holidays as needed
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
    email = data.get('email')
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

    # Send email to patient and clinic
    try:
        patient_msg = Message('Appointment Confirmation',
                              sender='thirushaun74@yahoo.com',
                              recipients=[email])
        patient_msg.body = f"Dear {name},\n\nYour appointment for {service} is confirmed on {date} at {time}.\n\nRegards,\nKlinik Mediviron"
        mail.send(patient_msg)

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
