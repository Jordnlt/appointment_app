from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'
db = SQLAlchemy(app)

# Define the Appointment model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/request-appointment', methods=['POST'])
def request_appointment():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    date = data.get('date')
    time = data.get('time')

    # Perform validation here if needed

    # Logic to confirm or deny the appointment
    status = 'confirmed'  # In a real app, you would have logic to determine this

    # Create the appointment
    appointment = Appointment(name=name, email=email, date=date, time=time, status=status)
    db.session.add(appointment)
    db.session.commit()

    # Send confirmation/denial email
    send_email(email, status)

    # Respond to the requester
    response_message = f'Your appointment on {date} at {time} has been {status}.'
    return jsonify({'message': response_message})

def send_email(email, status):
    sender_email = 'your-email@example.com'
    sender_password = 'your-email-password'
    subject = f'Appointment {status}'
    body = f'Your appointment has been {status}.'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, email, text)

@app.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    appointment_list = [{'name': a.name, 'email': a.email, 'date': a.date, 'time': a.time, 'status': a.status} for a in appointments]
    return jsonify(appointment_list)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
