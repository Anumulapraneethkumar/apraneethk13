"""
🏥 FUTURISTIC MULTI-SPECIALTY HOSPITAL MANAGEMENT SYSTEM
=========================================================
Advanced Hospital Management with Role-Based Dashboards
Python Implementation with Java Data Structures & R Analytics
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import csv
import os
import json
import qrcode
from datetime import datetime, timedelta
import io
import hashlib
import random
import shutil

# Data Structures (Java-style implementation in Python)
class Stack:
    """Stack data structure for undo operations"""
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)

class Queue:
    """Queue data structure for appointment management"""
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        self.items.insert(0, item)
    
    def dequeue(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

# Global configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
IMG_DIR = os.path.join(BASE_DIR, 'images')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')

# Global data structures
billing_stack = Stack()  # For undo operations
appointment_queue = Queue()  # For appointment management

# Color scheme
COLORS = {
    'primary': '#2C3E50',
    'secondary': '#3498DB',
    'success': '#27AE60',
    'danger': '#E74C3C',
    'warning': '#F39C12',
    'info': '#16A085',
    'light': '#ECF0F1',
    'dark': '#34495E',
    'white': '#FFFFFF',
    'receptionist': '#9B59B6',
    'doctor': '#3498DB',
    'admin': '#E74C3C',
    'pharmacy': '#27AE60',
    'lab': '#F39C12'
}

# User credentials database
USERS = {
    'admin': {'password': 'admin123', 'role': 'Admin', 'name': 'System Administrator'},
    'reception1': {'password': 'rec123', 'role': 'Receptionist', 'name': 'Sarah Johnson'},
    'reception2': {'password': 'rec123', 'role': 'Receptionist', 'name': 'Mike Wilson'},
    'doctor1': {'password': 'doc123', 'role': 'Doctor', 'name': 'Dr. Robert Smith', 'specialization': 'Cardiologist', 'id': 'D001'},
    'doctor2': {'password': 'doc123', 'role': 'Doctor', 'name': 'Dr. Emily Chen', 'specialization': 'Neurologist', 'id': 'D002'},
    'doctor3': {'password': 'doc123', 'role': 'Doctor', 'name': 'Dr. James Anderson', 'specialization': 'Orthopedic', 'id': 'D003'},
    'doctor4': {'password': 'doc123', 'role': 'Doctor', 'name': 'Dr. Maria Garcia', 'specialization': 'Pediatrician', 'id': 'D004'},
    'pharmacy1': {'password': 'pharm123', 'role': 'Pharmacy', 'name': 'John Pharmacist'},
    'pharmacy2': {'password': 'pharm123', 'role': 'Pharmacy', 'name': 'Lisa PharmTech'},
    'lab1': {'password': 'lab123', 'role': 'Lab', 'name': 'Dr. Kevin Lab Chief'},
    'lab2': {'password': 'lab123', 'role': 'Lab', 'name': 'Anna Lab Tech'}
}

def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

def read_csv(filename):
    """Read CSV file and return list of dictionaries"""
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []
    
    with open(filepath, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def write_csv(filename, fieldnames, data):
    """Write data to CSV file"""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def generate_id(prefix, existing_data, id_field):
    """Generate unique ID with prefix"""
    if not existing_data:
        return f"{prefix}001"
    
    max_id = 0
    for item in existing_data:
        try:
            num = int(item[id_field].replace(prefix, ''))
            if num > max_id:
                max_id = num
        except:
            pass
    
    return f"{prefix}{str(max_id + 1).zfill(3)}"

def generate_patient_qr(patient_data):
    """Generate QR code for patient"""
    qr_data = json.dumps({
        'id': patient_data['id'],
        'name': patient_data['name'],
        'contact': patient_data.get('contact', ''),
        'blood_group': patient_data.get('blood_group', '')
    })
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    qr_path = os.path.join(IMG_DIR, f'qr_patient_{patient_data["id"]}.png')
    img.save(qr_path)
    return qr_path

def create_default_avatar(name, patient_id):
    """Create default avatar with initials"""
    img = Image.new('RGB', (200, 200), color=(random.randint(100, 200), random.randint(100, 200), random.randint(150, 250)))
    draw = ImageDraw.Draw(img)
    
    # Get initials
    initials = ''.join([n[0].upper() for n in name.split()[:2]])
    
    # Draw initials
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    except:
        font = ImageFont.load_default()
    
    # Get text bounding box
    bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((200 - text_width) // 2, (200 - text_height) // 2)
    draw.text(position, initials, fill='white', font=font)
    
    avatar_path = os.path.join(IMG_DIR, f'patient_{patient_id}.png')
    img.save(avatar_path)
    return avatar_path

class ModernButton(tk.Canvas):
    """Custom modern button widget"""
    def __init__(self, parent, text, command=None, bg_color=COLORS['secondary'], 
                 fg_color='white', width=200, height=40, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.text = text
        
        # Draw button
        self.draw_button()
        
        # Bind events
        self.bind('<Button-1>', self.on_click)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
    
    def draw_button(self, hover=False):
        self.delete('all')
        color = self.lighten_color(self.bg_color) if hover else self.bg_color
        
        # Rounded rectangle
        self.create_rounded_rectangle(5, 5, self.winfo_reqwidth()-5, 
                                     self.winfo_reqheight()-5, 
                                     radius=10, fill=color, outline='')
        
        # Text
        self.create_text(self.winfo_reqwidth()//2, self.winfo_reqheight()//2,
                        text=self.text, fill=self.fg_color, font=('Helvetica', 11, 'bold'))
    
    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                 x1+radius, y1,
                 x2-radius, y1,
                 x2-radius, y1,
                 x2, y1,
                 x2, y1+radius,
                 x2, y1+radius,
                 x2, y2-radius,
                 x2, y2-radius,
                 x2, y2,
                 x2-radius, y2,
                 x2-radius, y2,
                 x1+radius, y2,
                 x1+radius, y2,
                 x1, y2,
                 x1, y2-radius,
                 x1, y2-radius,
                 x1, y1+radius,
                 x1, y1+radius,
                 x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def lighten_color(self, color):
        """Lighten hex color"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        lighter = tuple(min(255, c + 30) for c in rgb)
        return '#%02x%02x%02x' % lighter
    
    def on_click(self, event):
        if self.command:
            self.command()
    
    def on_enter(self, event):
        self.draw_button(hover=True)
    
    def on_leave(self, event):
        self.draw_button(hover=False)

class LoginWindow(tk.Tk):
    """Modern login window with role selection"""
    def __init__(self):
        super().__init__()
        self.title('🏥 Hospital Management System - Login')
        self.geometry('1000x650')
        self.configure(bg=COLORS['light'])
        self.resizable(False, False)
        
        # Center window
        self.center_window()
        
        self.create_widgets()
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self, bg=COLORS['light'])
        main_frame.pack(expand=True, fill='both')
        
        # Left panel - Hospital info
        left_panel = tk.Frame(main_frame, bg=COLORS['primary'], width=400)
        left_panel.pack(side='left', fill='both')
        left_panel.pack_propagate(False)
        
        # Hospital logo and info
        info_frame = tk.Frame(left_panel, bg=COLORS['primary'])
        info_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(info_frame, text='🏥', font=('Helvetica', 80), 
                bg=COLORS['primary'], fg='white').pack(pady=20)
        
        tk.Label(info_frame, text='MEDCARE PLUS', 
                font=('Helvetica', 28, 'bold'), 
                bg=COLORS['primary'], fg='white').pack()
        
        tk.Label(info_frame, text='Multi-Specialty Hospital', 
                font=('Helvetica', 14), 
                bg=COLORS['primary'], fg=COLORS['light']).pack(pady=10)
        
        tk.Label(info_frame, text='Advanced Healthcare Management System', 
                font=('Helvetica', 10, 'italic'), 
                bg=COLORS['primary'], fg=COLORS['light']).pack()
        
        # Right panel - Login form
        right_panel = tk.Frame(main_frame, bg='white')
        right_panel.pack(side='right', expand=True, fill='both')
        
        # Login form
        form_frame = tk.Frame(right_panel, bg='white')
        form_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(form_frame, text='Welcome Back', 
                font=('Helvetica', 24, 'bold'), 
                bg='white', fg=COLORS['primary']).pack(pady=(0, 10))
        
        tk.Label(form_frame, text='Please login to continue', 
                font=('Helvetica', 11), 
                bg='white', fg=COLORS['dark']).pack(pady=(0, 30))
        
        # Role selection
        role_frame = tk.Frame(form_frame, bg='white')
        role_frame.pack(pady=10)
        
        tk.Label(role_frame, text='Select Role', 
                font=('Helvetica', 11, 'bold'), 
                bg='white', fg=COLORS['dark']).pack(anchor='w')
        
        self.role_var = tk.StringVar(value='Admin')
        role_combo = ttk.Combobox(role_frame, textvariable=self.role_var, 
                                  font=('Helvetica', 11), width=35, state='readonly')
        role_combo['values'] = ['Admin', 'Receptionist', 'Doctor', 'Pharmacy', 'Lab']
        role_combo.pack(pady=(5, 0), ipady=8)
        role_combo.bind('<<ComboboxSelected>>', self.on_role_change)
        
        # Username
        user_frame = tk.Frame(form_frame, bg='white')
        user_frame.pack(pady=15)
        
        tk.Label(user_frame, text='Username', 
                font=('Helvetica', 11, 'bold'), 
                bg='white', fg=COLORS['dark']).pack(anchor='w')
        
        self.username_entry = ttk.Entry(user_frame, font=('Helvetica', 11), width=37)
        self.username_entry.pack(pady=(5, 0), ipady=8)
        
        # Password
        pass_frame = tk.Frame(form_frame, bg='white')
        pass_frame.pack(pady=15)
        
        tk.Label(pass_frame, text='Password', 
                font=('Helvetica', 11, 'bold'), 
                bg='white', fg=COLORS['dark']).pack(anchor='w')
        
        self.password_entry = ttk.Entry(pass_frame, font=('Helvetica', 11), 
                                       width=37, show='●')
        self.password_entry.pack(pady=(5, 0), ipady=8)
        
        # Login button
        login_btn = ModernButton(form_frame, text='LOGIN', command=self.login,
                                bg_color=COLORS['secondary'], width=300, height=45)
        login_btn.pack(pady=25)
        
        # Demo credentials info
        demo_frame = tk.Frame(form_frame, bg='white')
        demo_frame.pack(pady=10)
        
        tk.Label(demo_frame, text='Demo Credentials:', 
                font=('Helvetica', 9, 'bold'), 
                bg='white', fg=COLORS['dark']).pack()
        
        self.demo_label = tk.Label(demo_frame, text='admin / admin123', 
                                   font=('Helvetica', 9), 
                                   bg='white', fg=COLORS['secondary'])
        self.demo_label.pack()
        
        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.login())
    
    def on_role_change(self, event):
        """Update demo credentials based on role"""
        role = self.role_var.get()
        demo_creds = {
            'Admin': 'admin / admin123',
            'Receptionist': 'reception1 / rec123',
            'Doctor': 'doctor1 / doc123',
            'Pharmacy': 'pharmacy1 / pharm123',
            'Lab': 'lab1 / lab123'
        }
        self.demo_label.config(text=demo_creds.get(role, ''))
    
    def login(self):
        """Authenticate user and open dashboard"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror('Error', 'Please enter both username and password')
            return
        
        if username in USERS and USERS[username]['password'] == password:
            user_data = USERS[username]
            if user_data['role'] == self.role_var.get():
                self.withdraw()
                app = MainDashboard(user_data, username)
                app.protocol("WM_DELETE_WINDOW", lambda: self.on_dashboard_close(app))
                app.mainloop()
            else:
                messagebox.showerror('Error', f'Invalid role. This user is a {user_data["role"]}')
        else:
            messagebox.showerror('Error', 'Invalid username or password')
    
    def on_dashboard_close(self, dashboard):
        """Handle dashboard close"""
        dashboard.destroy()
        self.deiconify()
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')

class MainDashboard(tk.Tk):
    """Main dashboard with role-based interface"""
    def __init__(self, user_data, username):
        super().__init__()
        self.user_data = user_data
        self.username = username
        self.role = user_data['role']
        
        self.title(f'🏥 MEDCARE PLUS - {self.role} Dashboard')
        self.geometry('1400x800')
        self.state('zoomed')
        
        # Load data
        self.load_data()
        
        # Create main interface
        self.create_interface()
    
    def load_data(self):
        """Load all data from CSV files"""
        self.patients = read_csv('patients.csv')
        self.doctors = read_csv('doctors.csv')
        self.appointments = read_csv('appointments.csv')
        self.pharmacy = read_csv('pharmacy.csv')
        self.bills = read_csv('bills.csv')
        self.prescriptions = read_csv('prescriptions.csv')
        self.lab_reports = read_csv('lab_reports.csv')
        self.departments = read_csv('departments.csv')
    
    def save_all_data(self):
        """Save all data to CSV files"""
        write_csv('patients.csv', ['id', 'name', 'age', 'gender', 'contact', 
                                   'address', 'blood_group', 'admission_date', 
                                   'department', 'assigned_doctor', 'status', 'photo'], 
                 self.patients)
        write_csv('doctors.csv', ['id', 'name', 'specialization', 'contact', 
                                 'email', 'department', 'photo'], self.doctors)
        write_csv('appointments.csv', ['id', 'patient_id', 'doctor_id', 'date', 
                                      'time', 'type', 'status', 'notes'], 
                 self.appointments)
        write_csv('pharmacy.csv', ['medicine', 'category', 'quantity', 'price', 
                                  'expiry_date', 'supplier'], self.pharmacy)
        write_csv('bills.csv', ['bill_id', 'patient_id', 'amount', 'date', 
                               'payment_mode', 'status', 'items'], self.bills)
        write_csv('prescriptions.csv', ['id', 'patient_id', 'doctor_id', 'date', 
                                       'medicine', 'dosage', 'duration', 'notes'], 
                 self.prescriptions)
        write_csv('lab_reports.csv', ['report_id', 'patient_id', 'test_name', 
                                     'date', 'result', 'status', 'technician'], 
                 self.lab_reports)
        write_csv('departments.csv', ['id', 'name', 'head_doctor', 'beds_total', 
                                     'beds_occupied'], self.departments)
    
    def create_interface(self):
        """Create main interface"""
        # Top bar
        self.create_top_bar()
        
        # Main container
        main_container = tk.Frame(self, bg=COLORS['light'])
        main_container.pack(expand=True, fill='both')
        
        # Sidebar
        self.create_sidebar(main_container)
        
        # Content area
        self.content_frame = tk.Frame(main_container, bg='white')
        self.content_frame.pack(side='right', expand=True, fill='both', padx=2, pady=2)
        
        # Load default dashboard
        self.show_dashboard()
    
    def create_top_bar(self):
        """Create top navigation bar"""
        top_bar = tk.Frame(self, bg=COLORS['primary'], height=70)
        top_bar.pack(fill='x')
        top_bar.pack_propagate(False)
        
        # Logo and title
        left_frame = tk.Frame(top_bar, bg=COLORS['primary'])
        left_frame.pack(side='left', padx=20, pady=10)
        
        tk.Label(left_frame, text='🏥 MEDCARE PLUS', 
                font=('Helvetica', 18, 'bold'), 
                bg=COLORS['primary'], fg='white').pack(side='left')
        
        tk.Label(left_frame, text=f' | {self.role} Portal', 
                font=('Helvetica', 14), 
                bg=COLORS['primary'], fg=COLORS['light']).pack(side='left', padx=10)
        
        # Right frame - User info
        right_frame = tk.Frame(top_bar, bg=COLORS['primary'])
        right_frame.pack(side='right', padx=20, pady=10)
        
        tk.Label(right_frame, text=f'👤 {self.user_data["name"]}', 
                font=('Helvetica', 11), 
                bg=COLORS['primary'], fg='white').pack(side='left', padx=10)
        
        logout_btn = ModernButton(right_frame, text='Logout', 
                                 command=self.logout,
                                 bg_color=COLORS['danger'], 
                                 width=100, height=35)
        logout_btn.pack(side='left')
    
    def create_sidebar(self, parent):
        """Create sidebar navigation"""
        sidebar = tk.Frame(parent, bg=COLORS['dark'], width=250)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        
        # Menu items based on role
        menu_items = self.get_menu_items()
        
        tk.Label(sidebar, text='NAVIGATION', 
                font=('Helvetica', 10, 'bold'), 
                bg=COLORS['dark'], fg=COLORS['light']).pack(pady=20, padx=15, anchor='w')
        
        for item in menu_items:
            self.create_menu_button(sidebar, item['text'], item['icon'], item['command'])
    
    def create_menu_button(self, parent, text, icon, command):
        """Create a menu button"""
        btn_frame = tk.Frame(parent, bg=COLORS['dark'])
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        btn = tk.Button(btn_frame, text=f'{icon}  {text}', 
                       command=command,
                       font=('Helvetica', 11), 
                       bg=COLORS['dark'], fg='white',
                       activebackground=COLORS['primary'],
                       activeforeground='white',
                       bd=0, cursor='hand2',
                       anchor='w', padx=15, pady=12)
        btn.pack(fill='x')
        
        # Hover effect
        btn.bind('<Enter>', lambda e: btn.config(bg=COLORS['primary']))
        btn.bind('<Leave>', lambda e: btn.config(bg=COLORS['dark']))
    
    def get_menu_items(self):
        """Get menu items based on role"""
        base_items = [
            {'text': 'Dashboard', 'icon': '📊', 'command': self.show_dashboard},
        ]
        
        role_items = {
            'Admin': [
                {'text': 'Patients', 'icon': '👥', 'command': self.show_patients},
                {'text': 'Doctors', 'icon': '👨‍⚕️', 'command': self.show_doctors},
                {'text': 'Appointments', 'icon': '📅', 'command': self.show_appointments},
                {'text': 'Departments', 'icon': '🏢', 'command': self.show_departments},
                {'text': 'Billing', 'icon': '💰', 'command': self.show_billing},
                {'text': 'Pharmacy', 'icon': '💊', 'command': self.show_pharmacy},
                {'text': 'Lab Reports', 'icon': '🔬', 'command': self.show_lab_reports},
                {'text': 'Analytics', 'icon': '📈', 'command': self.show_analytics},
                {'text': 'Settings', 'icon': '⚙️', 'command': self.show_settings},
            ],
            'Receptionist': [
                {'text': 'Patients', 'icon': '👥', 'command': self.show_patients},
                {'text': 'Appointments', 'icon': '📅', 'command': self.show_appointments},
                {'text': 'Billing', 'icon': '💰', 'command': self.show_billing},
                {'text': 'Queue Management', 'icon': '🔄', 'command': self.show_queue},
            ],
            'Doctor': [
                {'text': 'My Patients', 'icon': '👥', 'command': self.show_my_patients},
                {'text': 'Today Schedule', 'icon': '📅', 'command': self.show_today_schedule},
                {'text': 'Prescriptions', 'icon': '📝', 'command': self.show_prescriptions},
                {'text': 'Lab Reports', 'icon': '🔬', 'command': self.show_lab_reports},
            ],
            'Pharmacy': [
                {'text': 'Medicines', 'icon': '💊', 'command': self.show_pharmacy},
                {'text': 'Prescriptions', 'icon': '📝', 'command': self.show_prescriptions},
                {'text': 'Stock Alert', 'icon': '⚠️', 'command': self.show_stock_alerts},
            ],
            'Lab': [
                {'text': 'Lab Reports', 'icon': '🔬', 'command': self.show_lab_reports},
                {'text': 'Pending Tests', 'icon': '⏳', 'command': self.show_pending_tests},
                {'text': 'Test Results', 'icon': '📊', 'command': self.show_test_results},
            ],
        }
        
        return base_items + role_items.get(self.role, [])
    
    def clear_content(self):
        """Clear content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Show role-specific dashboard"""
        self.clear_content()
        
        # Dashboard title
        title_frame = tk.Frame(self.content_frame, bg='white')
        title_frame.pack(fill='x', padx=30, pady=20)
        
        tk.Label(title_frame, text=f'{self.role} Dashboard', 
                font=('Helvetica', 24, 'bold'), 
                bg='white', fg=COLORS['primary']).pack(side='left')
        
        today = datetime.now().strftime('%A, %B %d, %Y')
        tk.Label(title_frame, text=today, 
                font=('Helvetica', 12), 
                bg='white', fg=COLORS['dark']).pack(side='right')
        
        # Stats cards
        self.create_stats_cards()
        
        # Recent activities
        self.create_recent_activities()
    
    def create_stats_cards(self):
        """Create statistics cards"""
        cards_frame = tk.Frame(self.content_frame, bg='white')
        cards_frame.pack(fill='x', padx=30, pady=20)
        
        stats = self.get_dashboard_stats()
        
        for i, stat in enumerate(stats):
            card = self.create_stat_card(cards_frame, stat['title'], 
                                         stat['value'], stat['icon'], 
                                         stat['color'])
            card.grid(row=0, column=i, padx=10, sticky='ew')
            cards_frame.grid_columnconfigure(i, weight=1)
    
    def create_stat_card(self, parent, title, value, icon, color):
        """Create a single stat card"""
        card = tk.Frame(parent, bg=color, relief='raised', bd=0)
        
        # Content
        content = tk.Frame(card, bg=color)
        content.pack(padx=20, pady=20)
        
        tk.Label(content, text=icon, font=('Helvetica', 40), 
                bg=color, fg='white').pack()
        
        tk.Label(content, text=str(value), font=('Helvetica', 28, 'bold'), 
                bg=color, fg='white').pack()
        
        tk.Label(content, text=title, font=('Helvetica', 12), 
                bg=color, fg='white').pack()
        
        return card
    
    def get_dashboard_stats(self):
        """Get statistics based on role"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        if self.role == 'Admin':
            return [
                {'title': 'Total Patients', 'value': len(self.patients), 
                 'icon': '👥', 'color': COLORS['info']},
                {'title': 'Total Doctors', 'value': len(self.doctors), 
                 'icon': '👨‍⚕️', 'color': COLORS['primary']},
                {'title': 'Today Appointments', 
                 'value': len([a for a in self.appointments if a['date'] == today]), 
                 'icon': '📅', 'color': COLORS['success']},
                {'title': 'Revenue Today', 
                 'value': f"₹{sum(float(b['amount']) for b in self.bills if b['date'] == today):.0f}", 
                 'icon': '💰', 'color': COLORS['warning']},
            ]
        elif self.role == 'Doctor':
            doctor_id = self.user_data.get('id', '')
            return [
                {'title': 'My Patients', 
                 'value': len([p for p in self.patients if p.get('assigned_doctor') == doctor_id]), 
                 'icon': '👥', 'color': COLORS['info']},
                {'title': 'Today Appointments', 
                 'value': len([a for a in self.appointments if a['date'] == today and a['doctor_id'] == doctor_id]), 
                 'icon': '📅', 'color': COLORS['success']},
                {'title': 'Pending Cases', 
                 'value': len([a for a in self.appointments if a['doctor_id'] == doctor_id and a['status'] == 'Scheduled']), 
                 'icon': '⏳', 'color': COLORS['warning']},
            ]
        elif self.role == 'Receptionist':
            return [
                {'title': 'Total Patients', 'value': len(self.patients), 
                 'icon': '👥', 'color': COLORS['info']},
                {'title': 'Today Appointments', 
                 'value': len([a for a in self.appointments if a['date'] == today]), 
                 'icon': '📅', 'color': COLORS['success']},
                {'title': 'In Queue', 
                 'value': appointment_queue.size(), 
                 'icon': '🔄', 'color': COLORS['warning']},
            ]
        elif self.role == 'Pharmacy':
            low_stock = len([m for m in self.pharmacy if int(m.get('quantity', 0)) < 20])
            return [
                {'title': 'Total Medicines', 'value': len(self.pharmacy), 
                 'icon': '💊', 'color': COLORS['success']},
                {'title': 'Low Stock Alert', 'value': low_stock, 
                 'icon': '⚠️', 'color': COLORS['danger']},
                {'title': 'Prescriptions Today', 
                 'value': len([p for p in self.prescriptions if p['date'] == today]), 
                 'icon': '📝', 'color': COLORS['info']},
            ]
        elif self.role == 'Lab':
            pending = len([r for r in self.lab_reports if r.get('status') == 'Pending'])
            return [
                {'title': 'Total Reports', 'value': len(self.lab_reports), 
                 'icon': '🔬', 'color': COLORS['info']},
                {'title': 'Pending Tests', 'value': pending, 
                 'icon': '⏳', 'color': COLORS['warning']},
                {'title': 'Completed Today', 
                 'value': len([r for r in self.lab_reports if r['date'] == today and r.get('status') == 'Completed']), 
                 'icon': '✅', 'color': COLORS['success']},
            ]
        
        return []
    
    def create_recent_activities(self):
        """Create recent activities section"""
        activities_frame = tk.Frame(self.content_frame, bg='white')
        activities_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        tk.Label(activities_frame, text='Recent Activities', 
                font=('Helvetica', 16, 'bold'), 
                bg='white', fg=COLORS['primary']).pack(anchor='w', pady=(0, 10))
        
        # Activities list
        list_frame = tk.Frame(activities_frame, bg='white', relief='groove', bd=1)
        list_frame.pack(fill='both', expand=True)
        
        activities = self.get_recent_activities()
        
        for activity in activities[:10]:
            activity_item = tk.Frame(list_frame, bg='white')
            activity_item.pack(fill='x', padx=10, pady=5)
            
            tk.Label(activity_item, text=activity['icon'], 
                    font=('Helvetica', 14), bg='white').pack(side='left', padx=5)
            
            tk.Label(activity_item, text=activity['text'], 
                    font=('Helvetica', 10), bg='white', 
                    fg=COLORS['dark'], anchor='w').pack(side='left', fill='x', expand=True, padx=5)
            
            tk.Label(activity_item, text=activity['time'], 
                    font=('Helvetica', 9), bg='white', 
                    fg=COLORS['secondary']).pack(side='right', padx=5)
            
            ttk.Separator(list_frame, orient='horizontal').pack(fill='x', padx=10)
    
    def get_recent_activities(self):
        """Get recent activities based on role"""
        activities = []
        
        # Get recent appointments
        for appt in sorted(self.appointments, key=lambda x: x.get('date', ''), reverse=True)[:5]:
            activities.append({
                'icon': '📅',
                'text': f"Appointment: Patient {appt['patient_id']} with Dr. {appt['doctor_id']}",
                'time': appt['date']
            })
        
        # Get recent bills
        for bill in sorted(self.bills, key=lambda x: x.get('date', ''), reverse=True)[:5]:
            activities.append({
                'icon': '💰',
                'text': f"Bill #{bill['bill_id']} - ₹{bill['amount']} - Patient {bill['patient_id']}",
                'time': bill['date']
            })
        
        return sorted(activities, key=lambda x: x['time'], reverse=True)
    
    def show_patients(self):
        """Show patients management interface"""
        self.clear_content()
        
        # Title
        title_frame = tk.Frame(self.content_frame, bg='white')
        title_frame.pack(fill='x', padx=30, pady=20)
        
        tk.Label(title_frame, text='Patient Management', 
                font=('Helvetica', 20, 'bold'), 
                bg='white', fg=COLORS['primary']).pack(side='left')
        
        # Action buttons
        btn_frame = tk.Frame(title_frame, bg='white')
        btn_frame.pack(side='right')
        
        ModernButton(btn_frame, text='➕ Add Patient', 
                    command=self.add_patient,
                    bg_color=COLORS['success'], 
                    width=150, height=35).pack(side='left', padx=5)
        
        ModernButton(btn_frame, text='🔄 Refresh', 
                    command=self.show_patients,
                    bg_color=COLORS['secondary'], 
                    width=120, height=35).pack(side='left', padx=5)
        
        # Search frame
        search_frame = tk.Frame(self.content_frame, bg='white')
        search_frame.pack(fill='x', padx=30, pady=10)
        
        tk.Label(search_frame, text='Search:', 
                font=('Helvetica', 11), 
                bg='white').pack(side='left', padx=5)
        
        self.patient_search_var = tk.StringVar()
        self.patient_search_var.trace('w', lambda *args: self.filter_patients())
        
        search_entry = ttk.Entry(search_frame, textvariable=self.patient_search_var, 
                                font=('Helvetica', 11), width=40)
        search_entry.pack(side='left', padx=5, ipady=5)
        
        # Patients table
        table_frame = tk.Frame(self.content_frame, bg='white')
        table_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical")
        hsb = ttk.Scrollbar(table_frame, orient="horizontal")
        
        # Treeview
        columns = ('ID', 'Name', 'Age', 'Gender', 'Contact', 'Blood Group', 
                  'Department', 'Doctor', 'Status')
        self.patients_tree = ttk.Treeview(table_frame, columns=columns, 
                                         show='headings', height=20,
                                         yscrollcommand=vsb.set, 
                                         xscrollcommand=hsb.set)
        
        vsb.config(command=self.patients_tree.yview)
        hsb.config(command=self.patients_tree.xview)
        
        # Configure columns
        for col in columns:
            self.patients_tree.heading(col, text=col, 
                                      command=lambda c=col: self.sort_treeview(self.patients_tree, c))
            self.patients_tree.column(col, width=120)
        
        # Grid layout
        self.patients_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Populate data
        self.populate_patients_tree()
        
        # Double-click to view details
        self.patients_tree.bind('<Double-1>', lambda e: self.view_patient_details())
        
        # Context menu
        self.create_patient_context_menu()
    
    def populate_patients_tree(self, filtered_data=None):
        """Populate patients treeview"""
        # Clear existing items
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)
        
        # Get data
        data = filtered_data if filtered_data is not None else self.patients
        
        # Insert data
        for patient in data:
            self.patients_tree.insert('', 'end', values=(
                patient['id'],
                patient['name'],
                patient.get('age', ''),
                patient.get('gender', ''),
                patient.get('contact', ''),
                patient.get('blood_group', ''),
                patient.get('department', ''),
                patient.get('assigned_doctor', ''),
                patient.get('status', 'Active')
            ))
    
    def filter_patients(self):
        """Filter patients based on search"""
        search_term = self.patient_search_var.get().lower()
        
        if not search_term:
            self.populate_patients_tree()
            return
        
        filtered = [p for p in self.patients if 
                   search_term in p['id'].lower() or
                   search_term in p['name'].lower() or
                   search_term in p.get('contact', '').lower()]
        
        self.populate_patients_tree(filtered)
    
    def create_patient_context_menu(self):
        """Create context menu for patients"""
        self.patient_context_menu = tk.Menu(self, tearoff=0)
        self.patient_context_menu.add_command(label="View Details", 
                                             command=self.view_patient_details)
        self.patient_context_menu.add_command(label="View History", 
                                             command=self.view_patient_history)
        self.patient_context_menu.add_command(label="Schedule Appointment", 
                                             command=self.schedule_appointment_for_patient)
        self.patient_context_menu.add_separator()
        self.patient_context_menu.add_command(label="Generate QR Code", 
                                             command=self.generate_patient_qr_code)
        self.patient_context_menu.add_separator()
        self.patient_context_menu.add_command(label="Delete", 
                                             command=self.delete_patient)
        
        self.patients_tree.bind('<Button-3>', self.show_patient_context_menu)
    
    def show_patient_context_menu(self, event):
        """Show patient context menu"""
        item = self.patients_tree.identify_row(event.y)
        if item:
            self.patients_tree.selection_set(item)
            self.patient_context_menu.post(event.x_root, event.y_root)
    
    def add_patient(self):
        """Add new patient"""
        dialog = tk.Toplevel(self)
        dialog.title('Add New Patient')
        dialog.geometry('600x700')
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (700 // 2)
        dialog.geometry(f'600x700+{x}+{y}')
        
        # Form frame
        form_frame = tk.Frame(dialog, bg='white', padx=30, pady=20)
        form_frame.pack(fill='both', expand=True)
        
        tk.Label(form_frame, text='Patient Registration', 
                font=('Helvetica', 18, 'bold'), 
                bg='white', fg=COLORS['primary']).pack(pady=(0, 20))
        
        # Form fields
        fields = [
            ('Name', 'name'),
            ('Age', 'age'),
            ('Gender', 'gender'),
            ('Contact', 'contact'),
            ('Address', 'address'),
            ('Blood Group', 'blood_group'),
            ('Department', 'department'),
        ]
        
        entries = {}
        
        for label, key in fields:
            field_frame = tk.Frame(form_frame, bg='white')
            field_frame.pack(fill='x', pady=8)
            
            tk.Label(field_frame, text=label, 
                    font=('Helvetica', 10, 'bold'), 
                    bg='white', width=15, anchor='w').pack(side='left')
            
            if key == 'gender':
                entries[key] = ttk.Combobox(field_frame, 
                                           values=['Male', 'Female', 'Other'], 
                                           state='readonly', font=('Helvetica', 10))
            elif key == 'blood_group':
                entries[key] = ttk.Combobox(field_frame, 
                                           values=['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'], 
                                           state='readonly', font=('Helvetica', 10))
            elif key == 'department':
                dept_names = [d['name'] for d in self.departments] if self.departments else ['General']
                entries[key] = ttk.Combobox(field_frame, 
                                           values=dept_names, 
                                           state='readonly', font=('Helvetica', 10))
            else:
                entries[key] = ttk.Entry(field_frame, font=('Helvetica', 10))
            
            entries[key].pack(side='left', fill='x', expand=True, ipady=5)
        
        # Photo selection
        photo_frame = tk.Frame(form_frame, bg='white')
        photo_frame.pack(fill='x', pady=8)
        
        tk.Label(photo_frame, text='Photo', 
                font=('Helvetica', 10, 'bold'), 
                bg='white', width=15, anchor='w').pack(side='left')
        
        photo_path_var = tk.StringVar()
        photo_entry = ttk.Entry(photo_frame, textvariable=photo_path_var, 
                               font=('Helvetica', 10), state='readonly')
        photo_entry.pack(side='left', fill='x', expand=True, ipady=5)
        
        def browse_photo():
            filename = filedialog.askopenfilename(
                title='Select Patient Photo',
                filetypes=[('Image files', '*.png *.jpg *.jpeg *.gif')])
            if filename:
                photo_path_var.set(filename)
        
        ttk.Button(photo_frame, text='Browse', 
                  command=browse_photo).pack(side='left', padx=5)
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg='white')
        btn_frame.pack(pady=20)
        
        def save_patient():
            # Validate
            if not entries['name'].get().strip():
                messagebox.showerror('Error', 'Please enter patient name')
                return
            
            # Generate ID
            patient_id = generate_id('P', self.patients, 'id')
            
            # Handle photo
            photo_filename = ''
            if photo_path_var.get():
                # Copy photo to images directory
                src = photo_path_var.get()
                ext = os.path.splitext(src)[1]
                photo_filename = f'patient_{patient_id}{ext}'
                dest = os.path.join(IMG_DIR, photo_filename)
                shutil.copy(src, dest)
            else:
                # Create default avatar
                photo_filename = os.path.basename(
                    create_default_avatar(entries['name'].get(), patient_id))
            
            # Create patient record
            patient = {
                'id': patient_id,
                'name': entries['name'].get().strip(),
                'age': entries['age'].get().strip(),
                'gender': entries['gender'].get(),
                'contact': entries['contact'].get().strip(),
                'address': entries['address'].get().strip(),
                'blood_group': entries['blood_group'].get(),
                'admission_date': datetime.now().strftime('%Y-%m-%d'),
                'department': entries['department'].get(),
                'assigned_doctor': '',
                'status': 'Active',
                'photo': photo_filename
            }
            
            self.patients.append(patient)
            self.save_all_data()
            
            # Generate QR code
            generate_patient_qr(patient)
            
            messagebox.showinfo('Success', 
                              f'Patient registered successfully!\nPatient ID: {patient_id}')
            dialog.destroy()
            self.show_patients()
        
        ModernButton(btn_frame, text='Save Patient', 
                    command=save_patient,
                    bg_color=COLORS['success'], 
                    width=150, height=40).pack(side='left', padx=10)
        
        ModernButton(btn_frame, text='Cancel', 
                    command=dialog.destroy,
                    bg_color=COLORS['danger'], 
                    width=150, height=40).pack(side='left', padx=10)
    
    def view_patient_details(self):
        """View patient details"""
        selection = self.patients_tree.selection()
        if not selection:
            messagebox.showwarning('Warning', 'Please select a patient')
            return
        
        patient_id = self.patients_tree.item(selection[0])['values'][0]
        patient = next((p for p in self.patients if p['id'] == patient_id), None)
        
        if not patient:
            return
        
        # Create details window
        details_win = tk.Toplevel(self)
        details_win.title(f'Patient Details - {patient["name"]}')
        details_win.geometry('800x600')
        details_win.transient(self)
        
        # Main container
        main_frame = tk.Frame(details_win, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header with photo
        header_frame = tk.Frame(main_frame, bg=COLORS['primary'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Photo
        photo_path = os.path.join(IMG_DIR, patient.get('photo', ''))
        if os.path.exists(photo_path):
            img = Image.open(photo_path)
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            photo_label = tk.Label(header_frame, image=photo, bg=COLORS['primary'])
            photo_label.image = photo
            photo_label.pack(side='left', padx=20, pady=20)
        
        # Info
        info_frame = tk.Frame(header_frame, bg=COLORS['primary'])
        info_frame.pack(side='left', fill='both', expand=True, pady=20)
        
        tk.Label(info_frame, text=patient['name'], 
                font=('Helvetica', 20, 'bold'), 
                bg=COLORS['primary'], fg='white').pack(anchor='w')
        
        tk.Label(info_frame, text=f"Patient ID: {patient['id']}", 
                font=('Helvetica', 12), 
                bg=COLORS['primary'], fg='white').pack(anchor='w', pady=5)
        
        tk.Label(info_frame, text=f"{patient.get('age', 'N/A')} years | {patient.get('gender', 'N/A')} | {patient.get('blood_group', 'N/A')}", 
                font=('Helvetica', 11), 
                bg=COLORS['primary'], fg='white').pack(anchor='w')
        
        # Details
        details_frame = tk.Frame(main_frame, bg='white')
        details_frame.pack(fill='both', expand=True)
        
        details_data = [
            ('Contact', patient.get('contact', 'N/A')),
            ('Address', patient.get('address', 'N/A')),
            ('Department', patient.get('department', 'N/A')),
            ('Assigned Doctor', patient.get('assigned_doctor', 'Not Assigned')),
            ('Admission Date', patient.get('admission_date', 'N/A')),
            ('Status', patient.get('status', 'Active')),
        ]
        
        for label, value in details_data:
            row = tk.Frame(details_frame, bg='white')
            row.pack(fill='x', pady=8)
            
            tk.Label(row, text=f"{label}:", 
                    font=('Helvetica', 11, 'bold'), 
                    bg='white', width=20, anchor='w').pack(side='left')
            
            tk.Label(row, text=value, 
                    font=('Helvetica', 11), 
                    bg='white', anchor='w').pack(side='left')
        
        # Buttons
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(pady=20)
        
        ModernButton(btn_frame, text='View History', 
                    command=lambda: self.view_patient_history_window(patient),
                    bg_color=COLORS['info'], 
                    width=150, height=35).pack(side='left', padx=5)
        
        ModernButton(btn_frame, text='Close', 
                    command=details_win.destroy,
                    bg_color=COLORS['secondary'], 
                    width=150, height=35).pack(side='left', padx=5)
    
    def view_patient_history(self):
        """View patient history with graphs"""
        selection = self.patients_tree.selection()
        if not selection:
            messagebox.showwarning('Warning', 'Please select a patient')
            return
        
        patient_id = self.patients_tree.item(selection[0])['values'][0]
        patient = next((p for p in self.patients if p['id'] == patient_id), None)
        
        if patient:
            self.view_patient_history_window(patient)
    
    def view_patient_history_window(self, patient):
        """Show patient history window with analytics"""
        history_win = tk.Toplevel(self)
        history_win.title(f'Patient History - {patient["name"]}')
        history_win.geometry('1000x700')
        history_win.transient(self)
        
        # Notebook for tabs
        notebook = ttk.Notebook(history_win)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Appointments tab
        appt_frame = tk.Frame(notebook, bg='white')
        notebook.add(appt_frame, text='Appointments')
        
        patient_appts = [a for a in self.appointments if a['patient_id'] == patient['id']]
        
        tk.Label(appt_frame, text=f'Total Appointments: {len(patient_appts)}', 
                font=('Helvetica', 12, 'bold'), 
                bg='white').pack(pady=10)
        
        appt_tree = ttk.Treeview(appt_frame, 
                                columns=('Date', 'Time', 'Doctor', 'Type', 'Status'), 
                                show='headings', height=15)
        
        for col in ('Date', 'Time', 'Doctor', 'Type', 'Status'):
            appt_tree.heading(col, text=col)
            appt_tree.column(col, width=150)
        
        appt_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        for appt in sorted(patient_appts, key=lambda x: x['date'], reverse=True):
            appt_tree.insert('', 'end', values=(
                appt['date'], appt['time'], appt['doctor_id'], 
                appt.get('type', 'General'), appt['status']
            ))
        
        # Prescriptions tab
        presc_frame = tk.Frame(notebook, bg='white')
        notebook.add(presc_frame, text='Prescriptions')
        
        patient_presc = [p for p in self.prescriptions if p['patient_id'] == patient['id']]
        
        tk.Label(presc_frame, text=f'Total Prescriptions: {len(patient_presc)}', 
                font=('Helvetica', 12, 'bold'), 
                bg='white').pack(pady=10)
        
        presc_tree = ttk.Treeview(presc_frame, 
                                 columns=('Date', 'Medicine', 'Dosage', 'Duration', 'Doctor'), 
                                 show='headings', height=15)
        
        for col in ('Date', 'Medicine', 'Dosage', 'Duration', 'Doctor'):
            presc_tree.heading(col, text=col)
            presc_tree.column(col, width=150)
        
        presc_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        for presc in sorted(patient_presc, key=lambda x: x['date'], reverse=True):
            presc_tree.insert('', 'end', values=(
                presc['date'], presc['medicine'], presc.get('dosage', ''), 
                presc.get('duration', ''), presc['doctor_id']
            ))
        
        # Lab Reports tab
        lab_frame = tk.Frame(notebook, bg='white')
        notebook.add(lab_frame, text='Lab Reports')
        
        patient_labs = [l for l in self.lab_reports if l['patient_id'] == patient['id']]
        
        tk.Label(lab_frame, text=f'Total Lab Reports: {len(patient_labs)}', 
                font=('Helvetica', 12, 'bold'), 
                bg='white').pack(pady=10)
        
        lab_tree = ttk.Treeview(lab_frame, 
                               columns=('Date', 'Test', 'Result', 'Status'), 
                               show='headings', height=15)
        
        for col in ('Date', 'Test', 'Result', 'Status'):
            lab_tree.heading(col, text=col)
            lab_tree.column(col, width=200)
        
        lab_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        for lab in sorted(patient_labs, key=lambda x: x['date'], reverse=True):
            lab_tree.insert('', 'end', values=(
                lab['date'], lab['test_name'], lab['result'], lab.get('status', 'Completed')
            ))
        
        # Bills tab
        bill_frame = tk.Frame(notebook, bg='white')
        notebook.add(bill_frame, text='Billing History')
        
        patient_bills = [b for b in self.bills if b['patient_id'] == patient['id']]
        total_amount = sum(float(b['amount']) for b in patient_bills)
        
        tk.Label(bill_frame, text=f'Total Bills: {len(patient_bills)} | Total Amount: ₹{total_amount:.2f}', 
                font=('Helvetica', 12, 'bold'), 
                bg='white').pack(pady=10)
        
        bill_tree = ttk.Treeview(bill_frame, 
                                columns=('Bill ID', 'Date', 'Amount', 'Payment Mode', 'Status'), 
                                show='headings', height=15)
        
        for col in ('Bill ID', 'Date', 'Amount', 'Payment Mode', 'Status'):
            bill_tree.heading(col, text=col)
            bill_tree.column(col, width=150)
        
        bill_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        for bill in sorted(patient_bills, key=lambda x: x['date'], reverse=True):
            bill_tree.insert('', 'end', values=(
                bill['bill_id'], bill['date'], f"₹{bill['amount']}", 
                bill.get('payment_mode', 'Cash'), bill.get('status', 'Paid')
            ))
        
        # Analytics tab - Visit frequency graph
        analytics_frame = tk.Frame(notebook, bg='white')
        notebook.add(analytics_frame, text='Analytics')
        
        self.show_patient_analytics(analytics_frame, patient)
    
    def show_patient_analytics(self, parent, patient):
        """Show patient analytics with graphs"""
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            import matplotlib.dates as mdates
            from collections import Counter
            
            # Get appointment dates
            patient_appts = [a for a in self.appointments if a['patient_id'] == patient['id']]
            
            if not patient_appts:
                tk.Label(parent, text='No appointment data available for analytics', 
                        font=('Helvetica', 12), bg='white').pack(pady=50)
                return
            
            # Create figure with subplots
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
            fig.patch.set_facecolor('white')
            
            # 1. Visits over time
            dates = [datetime.strptime(a['date'], '%Y-%m-%d') for a in patient_appts]
            dates_counter = Counter([d.strftime('%Y-%m') for d in dates])
            
            months = sorted(dates_counter.keys())
            counts = [dates_counter[m] for m in months]
            
            ax1.plot(months, counts, marker='o', linewidth=2, markersize=8, color=COLORS['secondary'])
            ax1.set_title('Visit Frequency Over Time', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Month', fontsize=11)
            ax1.set_ylabel('Number of Visits', fontsize=11)
            ax1.grid(True, alpha=0.3)
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            # 2. Appointment types distribution
            appt_types = [a.get('type', 'General') for a in patient_appts]
            type_counter = Counter(appt_types)
            
            colors = [COLORS['success'], COLORS['info'], COLORS['warning'], COLORS['danger']]
            ax2.pie(type_counter.values(), labels=type_counter.keys(), autopct='%1.1f%%',
                   colors=colors[:len(type_counter)], startangle=90)
            ax2.set_title('Appointment Types Distribution', fontsize=14, fontweight='bold')
            
            plt.tight_layout()
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True, padx=20, pady=20)
            
        except ImportError:
            tk.Label(parent, text='Matplotlib not available. Please install matplotlib for analytics.', 
                    font=('Helvetica', 12), bg='white', fg='red').pack(pady=50)
        except Exception as e:
            tk.Label(parent, text=f'Error generating analytics: {str(e)}', 
                    font=('Helvetica', 12), bg='white', fg='red').pack(pady=50)
    
    def generate_patient_qr_code(self):
        """Generate and show QR code for selected patient"""
        selection = self.patients_tree.selection()
        if not selection:
            messagebox.showwarning('Warning', 'Please select a patient')
            return
        
        patient_id = self.patients_tree.item(selection[0])['values'][0]
        patient = next((p for p in self.patients if p['id'] == patient_id), None)
        
        if not patient:
            return
        
        # Generate QR code
        qr_path = generate_patient_qr(patient)
        
        # Show QR code
        qr_win = tk.Toplevel(self)
        qr_win.title(f'QR Code - {patient["name"]}')
        qr_win.geometry('400x500')
        qr_win.transient(self)
        
        tk.Label(qr_win, text=f'QR Code for {patient["name"]}', 
                font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        tk.Label(qr_win, text=f'Patient ID: {patient["id"]}', 
                font=('Helvetica', 11)).pack()
        
        # Display QR code
        img = Image.open(qr_path)
        img = img.resize((300, 300), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        
        label = tk.Label(qr_win, image=photo)
        label.image = photo
        label.pack(pady=20)
        
        ModernButton(qr_win, text='Close', command=qr_win.destroy,
                    bg_color=COLORS['secondary'], width=120, height=35).pack(pady=10)
    
    def delete_patient(self):
        """Delete selected patient"""
        selection = self.patients_tree.selection()
        if not selection:
            messagebox.showwarning('Warning', 'Please select a patient')
            return
        
        patient_id = self.patients_tree.item(selection[0])['values'][0]
        
        if messagebox.askyesno('Confirm Delete', 
                              f'Are you sure you want to delete patient {patient_id}?'):
            self.patients = [p for p in self.patients if p['id'] != patient_id]
            self.save_all_data()
            self.show_patients()
            messagebox.showinfo('Success', 'Patient deleted successfully')
    
    def schedule_appointment_for_patient(self):
        """Schedule appointment for selected patient"""
        selection = self.patients_tree.selection()
        if not selection:
            messagebox.showwarning('Warning', 'Please select a patient')
            return
        
        patient_id = self.patients_tree.item(selection[0])['values'][0]
        self.show_appointments(default_patient=patient_id)
    
    def sort_treeview(self, tree, col):
        """Sort treeview by column"""
        items = [(tree.set(item, col), item) for item in tree.get_children('')]
        items.sort()
        
        for index, (val, item) in enumerate(items):
            tree.move(item, '', index)
    
    # Placeholder methods for other features
    def show_doctors(self):
        self.clear_content()
        tk.Label(self.content_frame, text='Doctors Management - Coming Soon', 
                font=('Helvetica', 20)).pack(pady=50)
    
    def show_appointments(self, default_patient=None):
        self.clear_content()
        tk.Label(self.content_frame, text='Appointments Management - Coming Soon', 
                font=('Helvetica', 20)).pack(pady=50)
    
    def show_departments(self):
        self.clear_content()
        tk.Label(self.content_frame, text='Departments Management - Coming Soon', 
                font=('Helvetica', 20)).pack(pady=50)
    
    def show_billing(self):
        self.clear_content()
        tk.Label(self.content_frame, text='Billing Management - Coming Soon', 
                font=('Helvetica', 20)).pack(pady=50)
    
    def show_pharmacy(self):
        self.clear_content()
        tk.Label(self.content_frame, text='Pharmacy Management - Coming Soon', 
                font=('Helvetica', 20)).pack(pady=50)
    
    def show_lab_reports(self):
        self.clear_content()
        tk.Label(self.content_frame, text='Lab Reports Management - Coming Soon', 
                font=('Helvetica', 20)).pack(pady=50)
    
    def show_analytics(self):
        self.clear_content()
        tk.Label(self.content_frame, text='Analytics - Coming Soon', 
                font=('Helvetica', 20)).pack(pady=50)
    
    def show_settings(self):
        self.clear_content()
        tk.Label(self.content_frame, text='Settings - Coming Soon', 
                font=('Helvetica', 20)).pack(pady=50)
    
    def show_queue(self):
        self.clear_content()
        tk.Label(self.content_frame, text='Queue Management - Coming Soon', 
                font=('Helvetica', 20)).pack(pady=50)
    
    def show_my_patients(self):
        self.clear_content()
        tk.Label(self.content_frame, text='My Patients - Coming Soon', 
                font=('Helvetica', 20)).pack(pady=50)
    
    def show_today_schedule(self):
        self.clear_content()
        tk.Label(self.content_frame, text='Today\'s Schedule - Coming Soon', 
                font=('Helvetica', 20)).pack(pady=50)
    
    def show_prescriptions(self):
        self.clear_content()
        tk.Label(self.content_frame, text='Prescriptions Management - Coming Soon', 
                font=('Helvetica', 20)).pack(pady=50)
    
    def show_stock_alerts(self):
        self.clear_content()
        tk.Label(self.content_frame, text='Stock Alerts - Coming Soon', 
                font=('Helvetica', 20)).pack(pady=50)
    
    def show_pending_tests(self):
        self.clear_content()
        tk.Label(self.content_frame, text='Pending Tests - Coming Soon', 
                font=('Helvetica', 20)).pack(pady=50)
    
    def show_test_results(self):
        self.clear_content()
        tk.Label(self.content_frame, text='Test Results - Coming Soon', 
                font=('Helvetica', 20)).pack(pady=50)
    
    def logout(self):
        """Logout and return to login screen"""
        if messagebox.askyesno('Logout', 'Are you sure you want to logout?'):
            self.destroy()

def initialize_sample_data():
    """Initialize sample data if not exists"""
    # Sample patients
    if not os.path.exists(os.path.join(DATA_DIR, 'patients.csv')):
        patients = [
            {'id': 'P001', 'name': 'John Doe', 'age': '45', 'gender': 'Male', 
             'contact': '9876543210', 'address': '123 Main St', 'blood_group': 'O+',
             'admission_date': '2024-01-15', 'department': 'Cardiology', 
             'assigned_doctor': 'D001', 'status': 'Active', 'photo': 'patient_P001.png'},
            {'id': 'P002', 'name': 'Jane Smith', 'age': '32', 'gender': 'Female', 
             'contact': '9876543211', 'address': '456 Oak Ave', 'blood_group': 'A+',
             'admission_date': '2024-02-20', 'department': 'Neurology', 
             'assigned_doctor': 'D002', 'status': 'Active', 'photo': 'patient_P002.png'},
        ]
        write_csv('patients.csv', ['id', 'name', 'age', 'gender', 'contact', 
                                   'address', 'blood_group', 'admission_date', 
                                   'department', 'assigned_doctor', 'status', 'photo'], 
                 patients)
        
        # Create default avatars for sample patients
        for patient in patients:
            create_default_avatar(patient['name'], patient['id'])
    
    # Sample doctors
    if not os.path.exists(os.path.join(DATA_DIR, 'doctors.csv')):
        doctors = [
            {'id': 'D001', 'name': 'Dr. Robert Smith', 'specialization': 'Cardiologist', 
             'contact': '9876543220', 'email': 'robert.smith@medcare.com', 
             'department': 'Cardiology', 'photo': ''},
            {'id': 'D002', 'name': 'Dr. Emily Chen', 'specialization': 'Neurologist', 
             'contact': '9876543221', 'email': 'emily.chen@medcare.com', 
             'department': 'Neurology', 'photo': ''},
        ]
        write_csv('doctors.csv', ['id', 'name', 'specialization', 'contact', 
                                 'email', 'department', 'photo'], doctors)
    
    # Sample departments
    if not os.path.exists(os.path.join(DATA_DIR, 'departments.csv')):
        departments = [
            {'id': 'DEPT001', 'name': 'Cardiology', 'head_doctor': 'D001', 
             'beds_total': '20', 'beds_occupied': '12'},
            {'id': 'DEPT002', 'name': 'Neurology', 'head_doctor': 'D002', 
             'beds_total': '15', 'beds_occupied': '8'},
            {'id': 'DEPT003', 'name': 'Orthopedics', 'head_doctor': 'D003', 
             'beds_total': '25', 'beds_occupied': '18'},
            {'id': 'DEPT004', 'name': 'Pediatrics', 'head_doctor': 'D004', 
             'beds_total': '30', 'beds_occupied': '22'},
        ]
        write_csv('departments.csv', ['id', 'name', 'head_doctor', 
                                     'beds_total', 'beds_occupied'], departments)
    
    # Initialize empty files if they don't exist
    for filename, fields in [
        ('appointments.csv', ['id', 'patient_id', 'doctor_id', 'date', 'time', 'type', 'status', 'notes']),
        ('pharmacy.csv', ['medicine', 'category', 'quantity', 'price', 'expiry_date', 'supplier']),
        ('bills.csv', ['bill_id', 'patient_id', 'amount', 'date', 'payment_mode', 'status', 'items']),
        ('prescriptions.csv', ['id', 'patient_id', 'doctor_id', 'date', 'medicine', 'dosage', 'duration', 'notes']),
        ('lab_reports.csv', ['report_id', 'patient_id', 'test_name', 'date', 'result', 'status', 'technician']),
    ]:
        if not os.path.exists(os.path.join(DATA_DIR, filename)):
            write_csv(filename, fields, [])

def main():
    """Main entry point"""
    # Ensure directories exist
    for directory in [DATA_DIR, IMG_DIR, REPORTS_DIR, BACKUP_DIR]:
        os.makedirs(directory, exist_ok=True)
    
    # Initialize sample data
    initialize_sample_data()
    
    # Start application
    app = LoginWindow()
    app.mainloop()

if __name__ == '__main__':
    main()
