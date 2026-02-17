# 📦 Installation & Setup Guide

## 🏥 MEDCARE PLUS - Hospital Management System

---

## 📋 System Requirements

### Minimum Requirements:
- **Operating System**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **RAM**: 4 GB minimum (8 GB recommended)
- **Storage**: 200 MB free space
- **Display**: 1366x768 or higher resolution

### Software Requirements:
- Python 3.8+
- pip package manager
- Tkinter (usually comes with Python)
- Internet connection (for initial setup)

---

## 🚀 Installation Steps

### Step 1: Extract the Project

Extract the downloaded `hospital_management_system.zip` file to your desired location.

```bash
# On Linux/macOS
unzip hospital_management_system.zip
cd hospital_system

# On Windows
# Right-click the ZIP file and select "Extract All..."
# Navigate to the extracted folder
```

### Step 2: Verify Python Installation

```bash
# Check Python version
python --version
# or
python3 --version

# Should show Python 3.8 or higher
```

**If Python is not installed:**
- Windows: Download from [python.org](https://www.python.org/downloads/)
- macOS: `brew install python3`
- Linux: `sudo apt-get install python3`

### Step 3: Install Dependencies

```bash
# Navigate to project directory
cd hospital_system

# Install required packages
pip install -r requirements.txt

# Or install individually
pip install Pillow qrcode matplotlib
```

**Troubleshooting Dependencies:**

If you encounter errors:

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Then install with specific versions
pip install Pillow>=10.0.0
pip install qrcode[pil]>=7.4.2
pip install matplotlib>=3.7.0
```

### Step 4: Verify Installation

```bash
# Check if all packages are installed
pip list | grep -E "Pillow|qrcode|matplotlib"

# You should see:
# Pillow       10.x.x
# qrcode       7.x.x
# matplotlib   3.x.x
```

### Step 5: Run the Application

```bash
# From the project directory
python hospital_main.py

# Or on some systems
python3 hospital_main.py
```

---

## 🎯 First-Time Setup

### 1. Login Screen
When you first run the application, you'll see a modern login screen.

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

### 2. Explore the Dashboard
After logging in, you'll see:
- Statistics cards showing key metrics
- Navigation menu on the left
- Recent activities
- Role-specific features

### 3. Sample Data
The system comes pre-loaded with:
- 5 sample patients with avatars
- 4 doctors across specializations
- 20 appointments
- Medicine inventory
- Lab reports
- Billing records

---

## 👥 User Roles & Access

### 1. Admin (Full Access)
**Login:** admin / admin123

**Capabilities:**
- Manage all modules
- View system analytics
- Access all patient records
- Manage doctors and staff
- Generate reports
- System configuration

### 2. Receptionist
**Login:** reception1 / rec123

**Capabilities:**
- Register new patients
- Schedule appointments
- Manage appointment queue
- Generate bills
- Patient check-in/check-out

### 3. Doctor
**Login:** doctor1 / doc123

**Capabilities:**
- View assigned patients
- Access patient medical history
- Write prescriptions
- View today's schedule
- Request lab tests
- View lab reports

### 4. Pharmacy
**Login:** pharmacy1 / pharm123

**Capabilities:**
- Manage medicine inventory
- Process prescriptions
- View stock alerts
- Update medicine details
- Track expiry dates

### 5. Lab Technician
**Login:** lab1 / lab123

**Capabilities:**
- Manage lab tests
- Enter test results
- Generate lab reports
- View pending tests
- Update report status

---

## 🎨 Feature Walkthrough

### Patient Management

1. **Add New Patient:**
   - Click "Patients" in sidebar
   - Click "Add Patient" button
   - Fill in patient details
   - Upload photo (optional - auto-generates if not provided)
   - Save

2. **View Patient Details:**
   - Double-click on any patient row
   - View complete profile
   - See patient photo and QR code

3. **View Patient History:**
   - Right-click on patient
   - Select "View History"
   - See appointments, prescriptions, lab reports, bills
   - View visit frequency graphs

4. **Generate Patient QR Code:**
   - Right-click on patient
   - Select "Generate QR Code"
   - QR code contains patient ID and basic info

### Appointment Management

1. **Schedule Appointment:**
   - Go to Appointments module
   - Click "Add Appointment"
   - Select patient and doctor
   - Choose date and time
   - Save

2. **Queue Management:**
   - View today's appointments
   - Manage waiting queue
   - Call next patient
   - Mark appointments as completed

### Pharmacy Management

1. **Manage Inventory:**
   - View all medicines
   - Check stock levels
   - See expiry dates
   - Get low stock alerts

2. **Process Prescriptions:**
   - View pending prescriptions
   - Dispense medicines
   - Auto-deduct from inventory
   - Generate bill

### Lab Management

1. **Manage Tests:**
   - View pending tests
   - Enter results
   - Generate reports
   - Track status

2. **View Reports:**
   - Access all lab reports
   - Filter by patient
   - Filter by date
   - Export reports

### Analytics & Reports

1. **View Dashboard:**
   - System statistics
   - Recent activities
   - Quick metrics

2. **Patient Analytics:**
   - Visit frequency graphs
   - Appointment type distribution
   - Revenue trends
   - Department statistics

---

## 🔧 Configuration

### Customizing the Application

**1. Add New Users:**

Edit the `USERS` dictionary in `hospital_main.py`:

```python
USERS = {
    'newuser': {
        'password': 'password123',
        'role': 'Doctor',
        'name': 'Dr. New User',
        'specialization': 'Cardiologist',
        'id': 'D005'
    }
}
```

**2. Change Color Scheme:**

Modify the `COLORS` dictionary:

```python
COLORS = {
    'primary': '#2C3E50',      # Main theme color
    'secondary': '#3498DB',    # Buttons and accents
    'success': '#27AE60',      # Success messages
    'danger': '#E74C3C',       # Alerts and warnings
    # ... add more colors
}
```

**3. Add Departments:**

Through Admin interface or edit `data/departments.csv`

**4. Configure Email/SMS:**

(Future feature - template provided in code)

---

## 📁 Data Management

### Data Files Location
All data is stored in CSV files in the `data/` directory:
- `patients.csv` - Patient records
- `doctors.csv` - Doctor information
- `appointments.csv` - Appointment schedules
- `pharmacy.csv` - Medicine inventory
- `bills.csv` - Billing records
- `prescriptions.csv` - Prescriptions
- `lab_reports.csv` - Lab test reports
- `departments.csv` - Department information

### Backup Data

**Manual Backup:**
```bash
# Copy the entire data directory
cp -r data/ backups/data_backup_$(date +%Y%m%d)/
```

**Restore Data:**
```bash
# Replace data directory with backup
cp -r backups/data_backup_20241027/ data/
```

### Export Data

Use the "Export CSVs" button in the application to save current data.

---

## 🐛 Troubleshooting

### Common Issues and Solutions

**Issue 1: Application won't start**
```
Error: ModuleNotFoundError: No module named 'PIL'
```
**Solution:**
```bash
pip install Pillow
```

**Issue 2: Images not displaying**
```
Error: FileNotFoundError: No such file or directory: 'images/'
```
**Solution:**
```bash
# Create images directory
mkdir images
# Or run the application once to auto-create
```

**Issue 3: QR codes not generating**
```
Error: qrcode module not found
```
**Solution:**
```bash
pip install qrcode[pil]
```

**Issue 4: Graphs not showing in Analytics**
```
Error: matplotlib not installed
```
**Solution:**
```bash
pip install matplotlib
```

**Issue 5: Permission denied on Linux/macOS**
```
Error: PermissionError
```
**Solution:**
```bash
chmod +x hospital_main.py
python3 hospital_main.py
```

**Issue 6: CSV file encoding issues**
```
Error: UnicodeDecodeError
```
**Solution:**
- Ensure CSV files are saved with UTF-8 encoding
- Re-run application to regenerate files

**Issue 7: Tkinter not found**
```
Error: ImportError: No module named '_tkinter'
```
**Solution:**
```bash
# On Ubuntu/Debian
sudo apt-get install python3-tk

# On macOS
brew install python-tk

# On Windows - Reinstall Python with Tkinter enabled
```

---

## 🔐 Security Considerations

### Password Management
- Change default passwords immediately
- Use strong passwords (8+ characters)
- Don't share credentials

### Data Security
- Backup data regularly
- Keep Python and packages updated
- Restrict file system access

### Access Control
- Use appropriate role-based logins
- Don't share admin credentials
- Monitor user activities

---

## 📈 Performance Optimization

### Tips for Better Performance:

1. **Regular Data Cleanup:**
   - Archive old records
   - Remove duplicate entries
   - Optimize CSV files

2. **Image Management:**
   - Compress patient photos
   - Use reasonable image sizes
   - Clean up unused images

3. **Database Optimization:**
   - Keep CSV files organized
   - Index important fields
   - Regular backups

---

## 🆙 Upgrading

### To upgrade to future versions:

1. **Backup Current Data:**
   ```bash
   cp -r data/ data_backup/
   cp -r images/ images_backup/
   ```

2. **Download New Version:**
   Extract new version to separate folder

3. **Migrate Data:**
   ```bash
   cp -r data_backup/ new_version/data/
   cp -r images_backup/ new_version/images/
   ```

4. **Test:**
   Run the new version and verify data integrity

---

## 📞 Support & Help

### Getting Help:

1. **Documentation:**
   - Read README.md for complete documentation
   - Check QUICK_START.md for quick reference
   - Review PROJECT_STRUCTURE.txt for overview

2. **Error Messages:**
   - Read error messages carefully
   - Check Troubleshooting section
   - Verify all dependencies installed

3. **Community:**
   - Create an issue on GitHub
   - Check existing issues
   - Contact developer

---

## 🎓 Learning Resources

### To understand the code better:

1. **Python Concepts:**
   - Object-Oriented Programming
   - File I/O operations
   - GUI development with Tkinter
   - Data structures (Stack, Queue)

2. **Tkinter Documentation:**
   - [Official Tkinter Docs](https://docs.python.org/3/library/tkinter.html)
   - Tkinter tutorials

3. **Data Visualization:**
   - Matplotlib documentation
   - Data analysis with Python

4. **Image Processing:**
   - Pillow/PIL documentation
   - QR code generation

---

## ✅ Verification Checklist

After installation, verify:

- [ ] Application starts without errors
- [ ] Login screen appears correctly
- [ ] Can login with demo credentials
- [ ] Dashboard loads with statistics
- [ ] Can view patient records
- [ ] Patient images display correctly
- [ ] Can generate QR codes
- [ ] Analytics graphs appear
- [ ] Can add new records
- [ ] Search functionality works
- [ ] Data persists after restart

---

## 🎉 You're All Set!

Your Hospital Management System is now ready to use.

**Next Steps:**
1. Login with admin credentials
2. Explore the features
3. Add your hospital data
4. Customize settings
5. Train staff on usage

**Enjoy managing your hospital efficiently! 🏥**

---

*For detailed feature documentation, see README.md*
*For quick reference, see QUICK_START.md*

**MEDCARE PLUS** - *Advancing Healthcare Management*
