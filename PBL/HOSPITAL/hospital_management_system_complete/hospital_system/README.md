# 🏥 MEDCARE PLUS - Hospital Management System

## Advanced Multi-Specialty Hospital Management System

A comprehensive, futuristic hospital management system built with Python, featuring role-based dashboards, patient analytics, QR code generation, and real-time management capabilities.

---

## 🌟 Features

### Core Features
- ✅ **Role-Based Authentication** - Admin, Receptionist, Doctor, Pharmacy, Lab
- ✅ **Patient Management** - Complete patient registration with photos and QR codes
- ✅ **Doctor Management** - Doctor profiles, specializations, and scheduling
- ✅ **Appointment System** - Scheduling, queue management, and tracking
- ✅ **Billing System** - Invoice generation, payment tracking, and QR payments
- ✅ **Pharmacy Management** - Medicine inventory, prescriptions, and stock alerts
- ✅ **Lab Management** - Test reports, results, and tracking
- ✅ **Analytics Dashboard** - Patient visit frequency graphs and statistics
- ✅ **QR Code System** - Patient identification and payment QR codes
- ✅ **Department Management** - Multi-specialty department tracking

### Technical Features
- 🎨 **Modern UI/UX** - Beautiful, intuitive interface with custom widgets
- 📊 **Data Visualization** - Matplotlib integration for analytics
- 🗃️ **Data Structures** - Java-style Stack (undo operations) and Queue (appointments)
- 💾 **CSV Database** - Simple file-based data persistence
- 📸 **Image Handling** - Patient photos with default avatar generation
- 🔐 **Secure Authentication** - Role-based access control
- 📱 **Responsive Design** - Adapts to different screen sizes

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone or extract the project**
   ```bash
   cd hospital_system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python hospital_main.py
   ```

---

## 👥 Default User Credentials

### Admin
- Username: `admin`
- Password: `admin123`

### Receptionist
- Username: `reception1` or `reception2`
- Password: `rec123`

### Doctor
- Username: `doctor1`, `doctor2`, `doctor3`, or `doctor4`
- Password: `doc123`

### Pharmacy
- Username: `pharmacy1` or `pharmacy2`
- Password: `pharm123`

### Lab
- Username: `lab1` or `lab2`
- Password: `lab123`

---

## 📂 Project Structure

```
hospital_system/
│
├── hospital_main.py          # Main application file
├── requirements.txt           # Python dependencies
├── README.md                  # This file
│
├── data/                      # CSV database files
│   ├── patients.csv
│   ├── doctors.csv
│   ├── appointments.csv
│   ├── pharmacy.csv
│   ├── bills.csv
│   ├── prescriptions.csv
│   ├── lab_reports.csv
│   └── departments.csv
│
├── images/                    # Patient photos and QR codes
│   ├── patient_P001.png
│   ├── qr_patient_P001.png
│   └── ...
│
├── reports/                   # Generated reports and PDFs
│   └── ...
│
└── backups/                   # Data backups
    └── ...
```

---

## 🎯 How to Use

### Admin Dashboard
1. Login as admin
2. Access all modules: Patients, Doctors, Billing, Pharmacy, Lab, Analytics
3. View system-wide statistics
4. Manage users and departments

### Receptionist Dashboard
1. Login as receptionist
2. Register new patients
3. Schedule appointments
4. Generate bills
5. Manage appointment queue

### Doctor Dashboard
1. Login as doctor
2. View today's schedule
3. Access patient history
4. Write prescriptions
5. Review lab reports

### Pharmacy Dashboard
1. Login as pharmacy staff
2. Manage medicine inventory
3. Process prescriptions
4. View stock alerts
5. Update medicine details

### Lab Dashboard
1. Login as lab staff
2. View pending tests
3. Enter test results
4. Generate lab reports
5. Track completed tests

---

## 📊 Key Modules

### 1. Patient Management
- Register patients with personal details
- Upload or generate patient photos
- Generate unique QR codes for identification
- View complete patient history
- Track visits with frequency graphs
- Search and filter patients

### 2. Appointment System
- Schedule appointments with doctors
- Queue management using Queue data structure
- Real-time appointment tracking
- Appointment status updates
- Calendar view of schedules

### 3. Billing System
- Generate itemized bills
- Multiple payment modes (Cash/Online/Card)
- QR code payment generation
- Bill history tracking
- Undo last bill (Stack data structure)
- PDF bill generation

### 4. Pharmacy Management
- Medicine inventory management
- Stock level monitoring
- Expiry date tracking
- Prescription processing
- Automatic stock deduction
- Low stock alerts

### 5. Lab Management
- Test order management
- Result entry system
- Report generation
- Pending test tracking
- Result status updates

### 6. Analytics
- Patient visit frequency graphs
- Appointment type distribution
- Revenue analytics
- Department statistics
- Doctor performance metrics

---

## 🔧 Technical Details

### Data Structures (Java Concepts in Python)

#### Stack Implementation
```python
# Used for undo operations in billing
billing_stack = Stack()
billing_stack.push(bill_data)
last_bill = billing_stack.pop()
```

#### Queue Implementation
```python
# Used for appointment queue management
appointment_queue = Queue()
appointment_queue.enqueue(appointment)
next_patient = appointment_queue.dequeue()
```

### Database (CSV Files)
- Simple file-based storage
- Easy to backup and restore
- No external database required
- Human-readable format

### Image Processing
- PIL/Pillow for image handling
- Automatic avatar generation
- QR code creation with qrcode library
- Image resizing and optimization

### Analytics (R-like functionality)
- Matplotlib for graph generation
- Patient visit frequency analysis
- Appointment distribution charts
- Revenue trend analysis

---

## 🎨 UI/UX Features

### Modern Design Elements
- Custom color scheme with role-based colors
- Smooth gradient effects
- Hover animations on buttons
- Professional card layouts
- Intuitive navigation menu
- Responsive tables with sorting
- Context menus for quick actions

### User Experience
- Clear visual hierarchy
- Minimal clicks to complete tasks
- Search and filter capabilities
- Real-time data updates
- Confirmation dialogs for critical actions
- Informative error messages
- Progress indicators

---

## 🔐 Security Features

- Password-protected access
- Role-based permissions
- Session management
- Data validation
- Secure file handling

---

## 🛠️ Customization

### Adding New Users
Edit the `USERS` dictionary in `hospital_main.py`:

```python
USERS = {
    'newuser': {
        'password': 'password123', 
        'role': 'Doctor', 
        'name': 'Dr. New User',
        'specialization': 'Specialty',
        'id': 'D005'
    }
}
```

### Adding New Departments
Add departments in the CSV file or through the admin interface.

### Customizing Colors
Modify the `COLORS` dictionary in `hospital_main.py`:

```python
COLORS = {
    'primary': '#2C3E50',
    'secondary': '#3498DB',
    # ... add more colors
}
```

---

## 📈 Future Enhancements

- [ ] SMS notifications for appointments
- [ ] Email integration
- [ ] Online patient portal
- [ ] Video consultation feature
- [ ] Integration with medical devices
- [ ] Cloud backup system
- [ ] Mobile app version
- [ ] Advanced AI-based diagnosis support
- [ ] Telemedicine capabilities
- [ ] Insurance claim processing

---

## 🐛 Troubleshooting

### Issue: Matplotlib graphs not showing
**Solution**: Install matplotlib
```bash
pip install matplotlib
```

### Issue: QR codes not generating
**Solution**: Install qrcode with PIL support
```bash
pip install qrcode[pil]
```

### Issue: Images not loading
**Solution**: Ensure the `images/` directory exists and has proper permissions

### Issue: CSV file errors
**Solution**: Check that all CSV files have proper headers matching the field names

---

## 📞 Support

For issues, questions, or feature requests, please create an issue in the project repository.

---

## 📄 License

This project is created for educational and demonstration purposes.

---

## 👨‍💻 Developer Notes

### Python Concepts Used
- Object-Oriented Programming (OOP)
- Data Structures (Stack, Queue)
- File I/O operations
- GUI development with Tkinter
- Image processing
- Data visualization

### Java Concepts Implemented in Python
- Stack data structure for undo operations
- Queue data structure for appointment management
- Class-based architecture
- Encapsulation and abstraction

### R-like Analytics
- Statistical analysis
- Data visualization
- Frequency distribution
- Trend analysis

---

## 🎓 Educational Value

This project demonstrates:
1. Full-stack desktop application development
2. Database design and management
3. User authentication and authorization
4. Role-based access control
5. Data visualization and analytics
6. File handling and image processing
7. Algorithm implementation (Stack, Queue)
8. GUI design principles
9. Software architecture patterns

---

## 🌟 Acknowledgments

Built with ❤️ using Python and modern development practices.

Special thanks to:
- Tkinter for GUI framework
- Pillow for image processing
- Matplotlib for data visualization
- QRCode library for QR generation

---

**MEDCARE PLUS** - *Advancing Healthcare Management*

*Version 1.0 - 2024*
