# 🚀 QUICK START GUIDE

## Get Started in 3 Steps!

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python hospital_main.py
```

### Step 3: Login
Use any of these credentials:

**Admin Access** (Full Control)
- Username: `admin`
- Password: `admin123`

**Receptionist** (Patient & Appointments)
- Username: `reception1`
- Password: `rec123`

**Doctor** (Patients & Schedule)
- Username: `doctor1`
- Password: `doc123`

**Pharmacy** (Medicines & Prescriptions)
- Username: `pharmacy1`
- Password: `pharm123`

**Lab** (Lab Reports & Tests)
- Username: `lab1`
- Password: `lab123`

---

## 🎯 Quick Tour

### For Admin:
1. **Dashboard** - View system statistics
2. **Patients** - Manage patient records (double-click to see details)
3. **Doctors** - View doctor information
4. **Analytics** - See visual reports and trends
5. **Billing** - Generate and track bills

### For Receptionist:
1. **Add Patient** - Register new patients with photos
2. **Schedule Appointments** - Book doctor appointments
3. **Queue Management** - Manage waiting patients
4. **Generate Bills** - Create invoices

### For Doctor:
1. **My Patients** - View assigned patients
2. **Today's Schedule** - See daily appointments
3. **Patient History** - Access complete medical history with graphs
4. **Write Prescriptions** - Prescribe medicines

### For Pharmacy:
1. **Medicines** - Manage inventory
2. **Stock Alerts** - View low stock items
3. **Process Prescriptions** - Fulfill medicine orders

### For Lab:
1. **Lab Reports** - Manage test reports
2. **Pending Tests** - Track incomplete tests
3. **Enter Results** - Update test results

---

## 💡 Key Features

### Patient Management
- ✅ Right-click on any patient for quick actions
- ✅ Double-click to view complete details
- ✅ View visit history with beautiful graphs
- ✅ Generate QR codes for easy identification
- ✅ Search patients by name, ID, or contact

### Analytics & Reports
- 📊 Visit frequency over time
- 📈 Appointment type distribution
- 💰 Revenue tracking
- 📉 Department statistics

### Smart Features
- 🔍 Real-time search and filtering
- 📱 QR code generation for patients and bills
- 📊 Visual analytics with matplotlib
- 💾 Automatic data persistence
- 🖼️ Patient photo management with auto-generated avatars

---

## 🎨 Sample Data Included

The system comes with pre-loaded sample data:
- 5 Sample Patients with avatars
- 4 Doctors across specializations
- 20 Appointments (past and future)
- 6 Medicines in pharmacy
- 15 Prescriptions
- 12 Lab Reports
- 10 Billing records

---

## 🔧 Troubleshooting

**Issue:** Module not found error
```bash
# Solution: Install dependencies
pip install Pillow qrcode matplotlib
```

**Issue:** Images not displaying
```bash
# Solution: Check images directory exists
mkdir -p images
```

**Issue:** Analytics not working
```bash
# Solution: Install matplotlib
pip install matplotlib
```

---

## 📞 Need Help?

Refer to the complete **README.md** for detailed documentation.

---

**Happy Hospital Management! 🏥**
