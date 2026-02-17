# shms_full.py
"""
SHMS - Single file Hospital Management System (Tkinter)
Features:
 - Role-based logins: Receptionist, Doctor, Pharmacy, Admin, LabIncharge
 - Persistent CSV data in ./data
 - Billing: Cash / Card (debit/credit) / Online(QR) with mark-paid and invoice PDF or image
 - Analytics using matplotlib (disease distribution, visits, income)
 - Simulated Java undo stack implemented in Python
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import csv, os, qrcode, zipfile, shutil
from datetime import datetime, timedelta
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Optional reportlab for proper PDF invoice
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except:
    REPORTLAB_AVAILABLE = False

BASE = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE, 'data')
IMG_DIR = os.path.join(BASE, 'images')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

# CSV headers
CSV_HEADERS = {
    'patients': ['id','name','age','gender','disease','photo','created'],
    'doctors': ['id','name','specialization','photo'],
    'appointments': ['id','patientId','doctorId','date','time','status'],
    'pharmacy': ['medicine','quantity','price'],
    'bills': ['billId','patientId','amount','date','mode','paid','method_details'],
    'prescriptions': ['prescId','patientId','doctorId','date','medicine','quantity'],
    'labreports': ['reportId','patientId','doctorId','date','test','result']
}

def read_csv(fname):
    path = os.path.join(DATA_DIR, fname)
    if not os.path.exists(path):
        return []
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def write_csv(fname, fieldnames, rows):
    path = os.path.join(DATA_DIR, fname)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# Simple undo stack (simulating Java stack)
class SimpleStack:
    def __init__(self): self._s = []
    def push(self, v): self._s.append(v)
    def pop(self): return self._s.pop() if self._s else None
    def peek(self): return self._s[-1] if self._s else None
    def __len__(self): return len(self._s)

UNDO_STACK = SimpleStack()

# Create sample data if missing
def ensure_sample_data():
    if not read_csv('doctors.csv'):
        docs = [
            {'id':'1','name':'Dr. Asha Singh','specialization':'Cardiology','photo':'doc1.png'},
            {'id':'2','name':'Dr. Rohit Verma','specialization':'Orthopedics','photo':'doc2.png'},
            {'id':'3','name':'Dr. Meera Patel','specialization':'Pediatrics','photo':'doc3.png'},
            {'id':'4','name':'Dr. Akbar Khan','specialization':'General','photo':'doc4.png'}
        ]
        write_csv('doctors.csv', CSV_HEADERS['doctors'], docs)
    if not read_csv('patients.csv'):
        pats = []
        for i in range(1,9):
            dt = (datetime.now() - timedelta(days=random.randint(0,120))).strftime('%Y-%m-%d')
            pats.append({'id':str(i),'name':f'Patient {i}','age':str(20+i),'gender':random.choice(['M','F']),'disease':random.choice(['Fever','Fracture','Diabetes','Flu','Hypertension']),'photo':f'pat{i}.png','created':dt})
        write_csv('patients.csv', CSV_HEADERS['patients'], pats)
    if not read_csv('pharmacy.csv'):
        meds = [
            {'medicine':'Paracetamol','quantity':'120','price':'5'},
            {'medicine':'Amoxicillin','quantity':'60','price':'12'},
            {'medicine':'Ibuprofen','quantity':'90','price':'8'}
        ]
        write_csv('pharmacy.csv', CSV_HEADERS['pharmacy'], meds)
    if not read_csv('appointments.csv'):
        appts = []
        aid = 1
        pats = read_csv('patients.csv')
        docs = read_csv('doctors.csv')
        for p in pats:
            did = random.choice(docs)['id']
            date = (datetime.now() - timedelta(days=random.randint(0,40))).strftime('%Y-%m-%d')
            time = f"{9+random.randint(0,8)}:{random.choice(['00','30'])}"
            appts.append({'id':str(aid),'patientId':p['id'],'doctorId':did,'date':date,'time':time,'status':'Done'})
            aid += 1
        write_csv('appointments.csv', CSV_HEADERS['appointments'], appts)
    # create sample images
    for i in range(1,5):
        p = os.path.join(IMG_DIR, f'doc{i}.png')
        if not os.path.exists(p):
            im = Image.new('RGB',(300,300),(200,220,255))
            d = ImageDraw.Draw(im); d.text((20,150), f'Doc {i}', fill=(10,10,10))
            im.save(p)
    for i in range(1,9):
        p = os.path.join(IMG_DIR, f'pat{i}.png')
        if not os.path.exists(p):
            im = Image.new('RGB',(300,300),(255,230,230))
            d = ImageDraw.Draw(im); d.text((20,150), f'Pat {i}', fill=(10,10,10))
            im.save(p)

ensure_sample_data()

# ---- App ----
class SHMSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('SHMS - Futuristic Multi-Specialty')
        self.geometry('1200x760')
        self.style = ttk.Style(self)
        try:
            self.style.theme_use('clam')
        except: pass
        self.load_all()
        self.show_login_selection()

    def load_all(self):
        self.patients = read_csv('patients.csv')
        self.doctors = read_csv('doctors.csv')
        self.appointments = read_csv('appointments.csv')
        self.pharmacy = read_csv('pharmacy.csv')
        self.bills = read_csv('bills.csv')
        self.prescriptions = read_csv('prescriptions.csv')
        self.labreports = read_csv('labreports.csv')

    def save_all(self):
        write_csv('patients.csv', CSV_HEADERS['patients'], self.patients)
        write_csv('doctors.csv', CSV_HEADERS['doctors'], self.doctors)
        write_csv('appointments.csv', CSV_HEADERS['appointments'], self.appointments)
        write_csv('pharmacy.csv', CSV_HEADERS['pharmacy'], self.pharmacy)
        write_csv('bills.csv', CSV_HEADERS['bills'], self.bills)
        write_csv('prescriptions.csv', CSV_HEADERS['prescriptions'], self.prescriptions)
        write_csv('labreports.csv', CSV_HEADERS['labreports'], self.labreports)

    # ---- Login screens ----
    def show_login_selection(self):
        for w in self.winfo_children(): w.destroy()
        frm = ttk.Frame(self, padding=20); frm.pack(expand=True, fill='both')
        ttk.Label(frm, text='Sign in to your account', font=('Helvetica',16,'bold')).pack(pady=(0,10))
        ttk.Label(frm, text='Select Role').pack(anchor='w')
        self.role_var = tk.StringVar(value='Receptionist')
        roles = ['Receptionist','Doctor','Pharmacy','Admin','Lab']
        ttk.Combobox(frm, textvariable=self.role_var, values=roles, state='readonly').pack(fill='x')
        ttk.Label(frm, text='Username').pack(anchor='w', pady=(10,0))
        self.user_entry = ttk.Entry(frm); self.user_entry.pack(fill='x')
        ttk.Label(frm, text='Password').pack(anchor='w', pady=(8,0))
        self.pw_entry = ttk.Entry(frm, show='*'); self.pw_entry.pack(fill='x')
        ttk.Button(frm, text='LOGIN', command=self.check_login, width=20).pack(pady=12)
        ttk.Label(frm, text='Demo Credentials:', font=('Helvetica',9,'bold')).pack(pady=(8,2))
        demo_txt = "Admin: admin/admin123 | Doctor: doctor1/doc123 | Receptionist: reception/staff123 | Pharmacy: pharmacy/staff123 | Lab: lab/lab123"
        ttk.Label(frm, text=demo_txt, font=('Helvetica',9)).pack()

    def check_login(self):
        role = self.role_var.get()
        u = self.user_entry.get().strip()
        p = self.pw_entry.get().strip()
        # demo accounts
        demo_ok = (u=='admin' and p=='admin123') or (role=='Doctor' and u.startswith('doctor') and p=='doc123') or (role=='Receptionist' and u=='reception' and p=='staff123') or (role=='Pharmacy' and u=='pharmacy' and p=='staff123') or (role=='Lab' and u=='lab' and p=='lab123')
        if demo_ok:
            self.role = role; self.user = u
            self.show_main()
        else:
            messagebox.showerror('Auth','Invalid credentials. Use demo accounts shown.')

    # ---- Main UI skeleton ----
    def show_main(self):
        for w in self.winfo_children(): w.destroy()
        self.load_all()
        top = ttk.Frame(self, padding=8); top.pack(fill='x')
        ttk.Label(top, text=f'SHMS - {self.role} ({self.user})', font=('Helvetica',14,'bold')).pack(side='left')
        ttk.Button(top, text='Export Package', command=self.export_package).pack(side='right', padx=4)
        ttk.Button(top, text='Logout', command=self.show_login_selection).pack(side='right', padx=4)
        main = ttk.Frame(self, padding=8); main.pack(expand=True, fill='both')
        sidebar = ttk.Frame(main, width=220); sidebar.pack(side='left', fill='y', padx=(0,8))
        # Sidebar design similar to screenshot (icons omitted but structure similar)
        for txt,cmd in [
            ('Patients', self.tab_patients),
            ('Doctors', self.tab_doctors),
            ('Appointments', self.tab_appointments),
            ('Pharmacy', self.tab_pharmacy),
            ('Billing', self.tab_billing),
            ('Lab Reports', self.tab_labreports),
            ('Analytics', self.tab_analytics),
            ('Emergency', self.tab_emergency)
        ]:
            ttk.Button(sidebar, text=txt, command=cmd).pack(fill='x', pady=2)

        self.area = ttk.Frame(main); self.area.pack(side='right', expand=True, fill='both')
        # role-specific landing
        if self.role == 'Doctor':
            self.tab_doctor_portal()
        elif self.role == 'Receptionist':
            self.tab_receptionist()
        else:
            self.tab_dashboard()

    # ---- Various Tabs ----
    def clear_area(self):
        for w in self.area.winfo_children(): w.destroy()

    def tab_dashboard(self):
        self.clear_area()
        frm = ttk.Frame(self.area, padding=8); frm.pack(expand=True, fill='both')
        ttk.Label(frm, text='Dashboard', font=('Helvetica',14,'bold')).pack(anchor='w')
        ttk.Label(frm, text=f'Total Patients: {len(self.patients)}').pack(anchor='w')
        ttk.Label(frm, text=f'Total Doctors: {len(self.doctors)}').pack(anchor='w')
        upcoming = sum(1 for a in self.appointments if a['status']=='Scheduled' and a['date']>=datetime.now().strftime('%Y-%m-%d'))
        ttk.Label(frm, text=f'Upcoming Appointments: {upcoming}').pack(anchor='w')
        # show disease chart
        chart_path = os.path.join(IMG_DIR,'disease_dist.png')
        self.build_disease_pie(chart_path)
        if os.path.exists(chart_path):
            img = Image.open(chart_path); img.thumbnail((800,360)); ph = ImageTk.PhotoImage(img)
            lbl = ttk.Label(frm, image=ph); lbl.image = ph; lbl.pack(pady=8)

    def tab_receptionist(self):
        self.clear_area(); frm = ttk.Frame(self.area, padding=8); frm.pack(expand=True, fill='both')
        ttk.Label(frm, text='Receptionist Dashboard', font=('Helvetica',14,'bold')).pack(anchor='w')
        ttk.Button(frm, text='Add Patient', command=self.add_patient).pack(pady=6)
        ttk.Button(frm, text='Today\'s Appointments', command=lambda: self.tab_appointments(today_only=True)).pack()
        # quick list
        lst = ttk.Treeview(frm, columns=('time','patient','doctor'), show='headings', height=8)
        for c in ('time','patient','doctor'): lst.heading(c, text=c.title()); lst.column(c, width=240)
        lst.pack(fill='both', expand=True, pady=6)
        today = datetime.now().strftime('%Y-%m-%d')
        for a in sorted(self.appointments, key=lambda x:(x['date'], x['time'])):
            if a['date'] >= today:
                p = next((pp for pp in self.patients if pp['id']==a['patientId']), {'name':'?'})
                d = next((dd for dd in self.doctors if dd['id']==a['doctorId']), {'name':'?'})
                lst.insert('', 'end', values=(a['date']+' '+a['time'], p.get('name','?'), d.get('name','?')))

    def tab_doctor_portal(self):
        self.clear_area(); frm = ttk.Frame(self.area, padding=8); frm.pack(expand=True, fill='both')
        ttk.Label(frm, text='Doctor Portal - Today', font=('Helvetica',14,'bold')).pack(anchor='w')
        cols = ('time','patient','status')
        tree = ttk.Treeview(frm, columns=cols, show='headings', height=14)
        for c in cols: tree.heading(c, text=c.title()); tree.column(c, width=300)
        tree.pack(fill='both', expand=True)
        today = datetime.now().strftime('%Y-%m-%d')
        doc_id = None
        if self.role=='Doctor' and self.user and self.user.startswith('doctor'):
            doc_id = self.user.replace('doctor','')
        for a in self.appointments:
            if a['date']==today and (doc_id is None or a['doctorId']==str(doc_id)):
                p = next((pp for pp in self.patients if pp['id']==a['patientId']), {'name':'?'})
                tree.insert('', 'end', values=(a['time'], p.get('name','?'), a['status']))
        ttk.Button(frm, text='Mark Done', command=lambda: self.mark_done(tree)).pack(pady=6)

    def tab_patients(self):
        self.clear_area(); frm = ttk.Frame(self.area, padding=8); frm.pack(expand=True, fill='both')
        ttk.Label(frm, text='Patients', font=('Helvetica',14,'bold')).pack(anchor='w')
        searchf = ttk.Frame(frm); searchf.pack(fill='x')
        ttk.Label(searchf, text='Search:').pack(side='left')
        svar = tk.StringVar(); sentry = ttk.Entry(searchf, textvariable=svar); sentry.pack(side='left', padx=4)
        tree = ttk.Treeview(frm, columns=('id','name','age','gender','disease','visits'), show='headings', height=14)
        for c in ('id','name','age','gender','disease','visits'): tree.heading(c, text=c.title()); tree.column(c,width=110)
        tree.pack(side='left', fill='both', expand=True, pady=6)
        for p in self.patients:
            visits = sum(1 for a in self.appointments if a['patientId']==p['id'])
            tree.insert('', 'end', values=(p['id'], p['name'], p.get('age',''), p.get('gender',''), p.get('disease',''), str(visits)))
        right = ttk.Frame(frm, width=380); right.pack(side='right', fill='y', padx=8)
        ttk.Label(right, text='Patient Detail', font=('Helvetica',12,'bold')).pack(anchor='w')
        detail_txt = tk.Text(right, width=44, height=20); detail_txt.pack()
        def on_select(e):
            sel = tree.selection(); 
            if not sel: return
            vals = tree.item(sel[0])['values']; pid = str(vals[0])
            self.show_patient_detail(pid, detail_txt)
        tree.bind('<<TreeviewSelect>>', on_select)
        ttk.Button(right, text='Add Patient', command=self.add_patient).pack(pady=6)

    def show_patient_detail(self, pid, text_widget):
        p = next((pp for pp in self.patients if pp['id']==str(pid)), None)
        if not p: return
        lines = [f"ID: {p['id']}", f"Name: {p['name']}", f"Age: {p.get('age','')}", f"Gender: {p.get('gender','')}", f"Disease: {p.get('disease','')}"]
        appts = [a for a in self.appointments if a['patientId']==str(pid)]
        lines.append("\nAppointments:")
        for a in sorted(appts, key=lambda x:x.get('date','')): lines.append(f" - {a['date']} {a['time']} Doctor:{a['doctorId']} status:{a['status']}")
        pres = [pr for pr in self.prescriptions if pr['patientId']==str(pid)]
        lines.append("\nPrescriptions:")
        for pr in pres: lines.append(f" - {pr['date']} {pr['medicine']} x{pr['quantity']}")
        labs = [l for l in self.labreports if l['patientId']==str(pid)]
        lines.append("\nLab Reports:")
        for l in labs: lines.append(f" - {l['date']} {l['test']}: {l['result']}")
        text_widget.delete('1.0','end'); text_widget.insert('1.0', '\n'.join(lines))
        # build visits chart
        chart_path = os.path.join(IMG_DIR, f'visits_{pid}.png'); self.build_patient_visits(pid, chart_path)
        if os.path.exists(chart_path):
            top = tk.Toplevel(self); top.title('Visits Graph'); img = Image.open(chart_path); img.thumbnail((520,260)); ph = ImageTk.PhotoImage(img)
            lbl = ttk.Label(top, image=ph); lbl.image = ph; lbl.pack()

    def add_patient(self):
        win = tk.Toplevel(self); win.title('Add Patient')
        ttk.Label(win, text='Name').grid(row=0,column=0); e1 = ttk.Entry(win); e1.grid(row=0,column=1)
        ttk.Label(win, text='Age').grid(row=1,column=0); e2 = ttk.Entry(win); e2.grid(row=1,column=1)
        ttk.Label(win, text='Gender').grid(row=2,column=0); e3 = ttk.Combobox(win, values=['M','F','Other']); e3.grid(row=2,column=1)
        ttk.Label(win, text='Disease').grid(row=3,column=0); e4 = ttk.Entry(win); e4.grid(row=3,column=1)
        pvar = tk.StringVar(); ttk.Entry(win, textvariable=pvar).grid(row=4,column=1)
        def browse(): 
            p = filedialog.askopenfilename(initialdir=IMG_DIR, filetypes=[('PNG','*.png'),('JPG','*.jpg')])
            if p: pvar.set(os.path.basename(p))
        ttk.Button(win, text='Browse Photo', command=browse).grid(row=4,column=2)
        def save():
            pid = 1
            if self.patients: pid = int(self.patients[-1]['id']) + 1
            rec = {'id':str(pid),'name':e1.get(),'age':e2.get(),'gender':e3.get() or 'M','disease':e4.get(),'photo':pvar.get(),'created':datetime.now().strftime('%Y-%m-%d')}
            self.patients.append(rec); write_csv('patients.csv', CSV_HEADERS['patients'], self.patients)
            messagebox.showinfo('Saved','Patient added'); win.destroy(); self.load_all(); self.show_main()
        ttk.Button(win, text='Save', command=save).grid(row=6,column=0,columnspan=3,pady=6)

    def tab_doctors(self):
        self.clear_area(); frm = ttk.Frame(self.area, padding=8); frm.pack(expand=True, fill='both')
        ttk.Label(frm, text='Doctors', font=('Helvetica',14,'bold')).pack(anchor='w')
        tree = ttk.Treeview(frm, columns=('id','name','spec'), show='headings', height=12)
        for c in ('id','name','spec'): tree.heading(c, text=c.title()); tree.column(c,width=250)
        tree.pack(fill='both', expand=True)
        for d in self.doctors: tree.insert('', 'end', values=(d['id'], d['name'], d['specialization']))
        ttk.Button(frm, text='Add Doctor', command=self.add_doctor).pack(pady=6)

    def add_doctor(self):
        win = tk.Toplevel(self); win.title('Add Doctor')
        ttk.Label(win, text='Name').grid(row=0,column=0); e1 = ttk.Entry(win); e1.grid(row=0,column=1)
        ttk.Label(win, text='Specialization').grid(row=1,column=0); e2 = ttk.Entry(win); e2.grid(row=1,column=1)
        def save():
            did = 1
            if self.doctors: did = int(self.doctors[-1]['id']) + 1
            rec = {'id':str(did),'name':e1.get(),'specialization':e2.get(),'photo':''}
            self.doctors.append(rec); write_csv('doctors.csv', CSV_HEADERS['doctors'], self.doctors)
            messagebox.showinfo('Saved','Doctor added'); win.destroy(); self.load_all(); self.show_main()
        ttk.Button(win, text='Save', command=save).grid(row=3,column=0,columnspan=2,pady=6)

    def tab_appointments(self, today_only=False, open_new=False):
        self.clear_area(); frm = ttk.Frame(self.area, padding=8); frm.pack(expand=True, fill='both')
        ttk.Label(frm, text='Appointments', font=('Helvetica',14,'bold')).pack(anchor='w')
        cols = ('id','patient','doctor','date','time','status')
        tree = ttk.Treeview(frm, columns=cols, show='headings', height=14)
        for c in cols: tree.heading(c, text=c.title()); tree.column(c, width=130)
        tree.pack(fill='both', expand=True)
        today = datetime.now().strftime('%Y-%m-%d')
        for a in self.appointments:
            if today_only and a['date']!=today: continue
            p = next((pp for pp in self.patients if pp['id']==a['patientId']), {'name':'?'} )
            d = next((dd for dd in self.doctors if dd['id']==a['doctorId']), {'name':'?'} )
            tree.insert('', 'end', values=(a['id'], p.get('name','?'), d.get('name','?'), a['date'], a['time'], a['status']))
        btnf = ttk.Frame(frm); btnf.pack(pady=6)
        ttk.Button(btnf, text='New Appointment', command=self.new_appointment).pack(side='left', padx=4)
        ttk.Button(btnf, text='Mark Done', command=lambda: self.mark_done(tree)).pack(side='left', padx=4)
        if open_new: self.new_appointment()

    def new_appointment(self):
        win = tk.Toplevel(self); win.title('New Appointment')
        ttk.Label(win, text='Patient ID').grid(row=0,column=0); e1 = ttk.Entry(win); e1.grid(row=0,column=1)
        ttk.Label(win, text='Doctor ID').grid(row=1,column=0); e2 = ttk.Entry(win); e2.grid(row=1,column=1)
        ttk.Label(win, text='Date (YYYY-MM-DD)').grid(row=2,column=0); e3 = ttk.Entry(win); e3.grid(row=2,column=1)
        ttk.Label(win, text='Time (HH:MM)').grid(row=3,column=0); e4 = ttk.Entry(win); e4.grid(row=3,column=1)
        def save():
            aid = 1
            if self.appointments: aid = int(self.appointments[-1]['id']) + 1
            rec = {'id':str(aid),'patientId':e1.get(),'doctorId':e2.get(),'date':e3.get(),'time':e4.get(),'status':'Scheduled'}
            self.appointments.append(rec); write_csv('appointments.csv', CSV_HEADERS['appointments'], self.appointments)
            messagebox.showinfo('Saved','Appointment scheduled'); win.destroy(); self.load_all(); self.show_main()
        ttk.Button(win, text='Save', command=save).grid(row=4,column=0,columnspan=2,pady=6)

    def mark_done(self, tree):
        sel = tree.selection(); 
        if not sel: messagebox.showerror('Select','Select appointment'); return
        vals = tree.item(sel[0])['values']; aid = str(vals[0])
        for a in self.appointments:
            if a['id']==aid: a['status']='Done'
        write_csv('appointments.csv', CSV_HEADERS['appointments'], self.appointments)
        messagebox.showinfo('Updated','Marked done'); self.load_all(); self.show_main()

    def tab_pharmacy(self):
        self.clear_area(); frm = ttk.Frame(self.area, padding=8); frm.pack(expand=True, fill='both')
        ttk.Label(frm, text='Pharmacy', font=('Helvetica',14,'bold')).pack(anchor='w')
        tree = ttk.Treeview(frm, columns=('medicine','quantity','price'), show='headings', height=12)
        for c in ('medicine','quantity','price'): tree.heading(c, text=c.title()); tree.column(c,width=200)
        tree.pack(fill='both', expand=True)
        for m in self.pharmacy: tree.insert('', 'end', values=(m['medicine'], m.get('quantity',''), m.get('price','')))
        ttk.Button(frm, text='Add/Update Medicine', command=self.manage_medicine).pack(pady=6)
        ttk.Button(frm, text='Fulfill Prescription', command=self.fulfill_prescription).pack(pady=6)

    def manage_medicine(self):
        win = tk.Toplevel(self); win.title('Add Medicine')
        ttk.Label(win, text='Medicine').grid(row=0,column=0); e1 = ttk.Entry(win); e1.grid(row=0,column=1)
        ttk.Label(win, text='Quantity').grid(row=1,column=0); e2 = ttk.Entry(win); e2.grid(row=1,column=1)
        ttk.Label(win, text='Price').grid(row=2,column=0); e3 = ttk.Entry(win); e3.grid(row=2,column=1)
        def save():
            found = False
            for m in self.pharmacy:
                if m['medicine'].lower()==e1.get().lower():
                    m['quantity'] = str(int(m.get('quantity',0)) + int(e2.get()))
                    m['price'] = e3.get()
                    found = True
            if not found:
                self.pharmacy.append({'medicine':e1.get(),'quantity':e2.get(),'price':e3.get()})
            write_csv('pharmacy.csv', CSV_HEADERS['pharmacy'], self.pharmacy)
            messagebox.showinfo('Saved','Medicine updated'); win.destroy(); self.load_all(); self.show_main()
        ttk.Button(win, text='Save', command=save).grid(row=3,column=0,columnspan=2,pady=6)

    def fulfill_prescription(self):
        pres = self.prescriptions
        if not pres: messagebox.showinfo('No Prescriptions','No prescriptions available'); return
        win = tk.Toplevel(self); win.title('Select Prescription to Fulfill')
        lst = tk.Listbox(win, width=90)
        for p in pres: lst.insert('end', f"ID:{p['prescId']} Patient:{p['patientId']} {p['medicine']} x{p['quantity']} ({p['date']})")
        lst.pack()
        def fulfill():
            sel = lst.curselection()
            if not sel: return
            idx = sel[0]; rec = pres[idx]; med = rec['medicine']; q = int(rec.get('quantity','1'))
            for mrec in self.pharmacy:
                if mrec['medicine'].lower()==med.lower():
                    try: mrec['quantity'] = str(max(0,int(mrec.get('quantity',0)) - q))
                    except: pass
            write_csv('pharmacy.csv', CSV_HEADERS['pharmacy'], self.pharmacy)
            messagebox.showinfo('Fulfilled', f'Prescription {rec["prescId"]} fulfilled. Stock updated.')
            win.destroy(); self.load_all(); self.show_main()
        ttk.Button(win, text='Fulfill', command=fulfill).pack(pady=6)

    def tab_billing(self):
        self.clear_area(); frm = ttk.Frame(self.area, padding=8); frm.pack(expand=True, fill='both')
        ttk.Label(frm, text='Billing', font=('Helvetica',14,'bold')).pack(anchor='w')
        tree = ttk.Treeview(frm, columns=('billId','patient','amount','date','mode','paid'), show='headings', height=12)
        for c in ('billId','patient','amount','date','mode','paid'): tree.heading(c, text=c.title()); tree.column(c,width=120)
        tree.pack(fill='both', expand=True)
        for b in (self.bills or []):
            p = next((pp for pp in self.patients if pp.get('id')==b.get('patientId')), {'name':'?'})
            tree.insert('', 'end', values=(b.get('billId',''), p.get('name','?'), b.get('amount',''), b.get('date',''), b.get('mode',''), b.get('paid','')))
        btnf = ttk.Frame(frm); btnf.pack(pady=6)
        ttk.Button(btnf, text='Generate Bill', command=lambda: self.generate_bill(tree)).pack(side='left', padx=4)
        ttk.Button(btnf, text='Undo Last (Stack)', command=self.undo_last_bill).pack(side='left', padx=4)
        ttk.Button(btnf, text='Export Invoice (PDF/Image)', command=self.export_invoice_selected).pack(side='left', padx=4)

    def generate_bill(self, tree):
        win = tk.Toplevel(self); win.title('Generate Bill')
        ttk.Label(win, text='Patient ID').grid(row=0,column=0); e1 = ttk.Entry(win); e1.grid(row=0,column=1)
        ttk.Label(win, text='Amount').grid(row=1,column=0); e2 = ttk.Entry(win); e2.grid(row=1,column=1)
        ttk.Label(win, text='Mode').grid(row=2,column=0); e3 = ttk.Combobox(win, values=['Cash','Card','Online']); e3.grid(row=2,column=1)
        def save():
            try:
                amount = float(e2.get())
            except:
                messagebox.showerror('Error','Invalid amount'); return
            mode = e3.get() or 'Cash'
            bid = 1
            if self.bills: bid = int(self.bills[-1]['billId']) + 1
            rec = {'billId':str(bid),'patientId':e1.get(),'amount':str(amount),'date':datetime.now().strftime('%Y-%m-%d'),'mode':mode,'paid':'no','method_details':''}
            # depending on mode -> request card details or generate QR or cash immediate
            if mode=='Cash':
                rec['paid']='yes'; rec['method_details']='Cash'
                self.bills.append(rec); write_csv('bills.csv', CSV_HEADERS['bills'], self.bills)
                UNDO_STACK.push(rec); messagebox.showinfo('Saved','Cash bill recorded (Paid)')
            elif mode=='Card':
                # ask for card details (simulate)
                def proc_card():
                    cn = cardnum.get().strip(); name = cname.get().strip(); exp = cexp.get().strip(); cvv = ccvv.get().strip()
                    if len(cn) < 12 or len(cvv) < 3:
                        messagebox.showerror('Card Error','Invalid card details'); return
                    rec['paid']='yes'; rec['method_details'] = f'Card|{name}|{cn[-4:]}'
                    self.bills.append(rec); write_csv('bills.csv', CSV_HEADERS['bills'], self.bills)
                    UNDO_STACK.push(rec); messagebox.showinfo('Paid','Card payment simulated and recorded'); cwin.destroy(); win.destroy(); self.load_all(); self.show_main()
                cwin = tk.Toplevel(win); cwin.title('Card Payment')
                ttk.Label(cwin, text='Name on Card').grid(row=0,column=0); cname = ttk.Entry(cwin); cname.grid(row=0,column=1)
                ttk.Label(cwin, text='Card Number').grid(row=1,column=0); cardnum = ttk.Entry(cwin); cardnum.grid(row=1,column=1)
                ttk.Label(cwin, text='Expiry (MM/YY)').grid(row=2,column=0); cexp = ttk.Entry(cwin); cexp.grid(row=2,column=1)
                ttk.Label(cwin, text='CVV').grid(row=3,column=0); ccvv = ttk.Entry(cwin); ccvv.grid(row=3,column=1)
                ttk.Button(cwin, text='Pay', command=proc_card).grid(row=4,column=0,columnspan=2,pady=6)
                return
            elif mode=='Online':
                # generate QR and show dialog; payment marked when user clicks Mark Paid
                qrdata = f"ONLINEPAY|bill:{rec['billId']}|patient:{rec['patientId']}|amount:{rec['amount']}"
                img = qrcode.make(qrdata)
                qrpath = os.path.join(IMG_DIR, f'qr_bill_{rec["billId"]}.png'); img.save(qrpath)
                self.bills.append(rec); write_csv('bills.csv', CSV_HEADERS['bills'], self.bills)
                UNDO_STACK.push(rec)
                qwin = tk.Toplevel(win); qwin.title('Online Payment (QR)')
                pil = Image.open(qrpath); pil.thumbnail((300,300)); ph = ImageTk.PhotoImage(pil)
                lbl = ttk.Label(qwin, image=ph); lbl.image = ph; lbl.pack(pady=8)
                def mark_paid_action():
                    for b in self.bills:
                        if b['billId']==str(rec['billId']):
                            b['paid']='yes'; b['method_details']='OnlineQR'
                            write_csv('bills.csv', CSV_HEADERS['bills'], self.bills)
                            # create invoice
                            self.create_invoice(b)
                            messagebox.showinfo('Paid','Payment recorded and invoice generated.')
                            qwin.destroy(); win.destroy(); self.load_all(); self.show_main()
                            return
                ttk.Button(qwin, text='Mark Paid', command=mark_paid_action).pack()
                return
            # final actions for non-card handled above
            win.destroy(); self.load_all(); self.show_main()
        ttk.Button(win, text='Generate', command=save).grid(row=3,column=0,columnspan=2,pady=6)

    def undo_last_bill(self):
        rec = UNDO_STACK.pop()
        if not rec:
            messagebox.showinfo('Undo','Nothing to undo.')
            return
        self.bills = [b for b in self.bills if b.get('billId')!=rec.get('billId')]
        write_csv('bills.csv', CSV_HEADERS['bills'], self.bills)
        messagebox.showinfo('Undo','Removed bill '+rec.get('billId',''))
        self.load_all(); self.show_main()

    def export_invoice_selected(self):
        # ask user to select bill from list and export invoice
        bills = self.bills
        if not bills:
            messagebox.showinfo('No Bills','No bills to export.')
            return
        win = tk.Toplevel(self); win.title('Select Bill to Export')
        lb = tk.Listbox(win, width=80)
        for b in bills:
            p = next((pp for pp in self.patients if pp.get('id')==b.get('patientId')), {'name':'?'})
            lb.insert('end', f"Bill:{b.get('billId')} Patient:{p.get('name','?')} Amount:{b.get('amount')} Paid:{b.get('paid')}")
        lb.pack()
        def export():
            sel = lb.curselection(); 
            if not sel: return
            idx = sel[0]; b = bills[idx]
            self.create_invoice(b, show_dialog=True)
            win.destroy()
        ttk.Button(win, text='Export', command=export).pack(pady=6)

    def create_invoice(self, bill_rec, show_dialog=False):
        # generate PDF if reportlab present, otherwise image PNG
        out_pdf = os.path.join(IMG_DIR, f'bill_{bill_rec["billId"]}.pdf')
        out_img = os.path.join(IMG_DIR, f'bill_{bill_rec["billId"]}.png')
        if REPORTLAB_AVAILABLE:
            c = canvas.Canvas(out_pdf, pagesize=A4)
            c.setFont("Helvetica-Bold", 18)
            c.drawString(40,800,"Smart Hospital - Invoice")
            c.setFont("Helvetica", 12)
            c.drawString(40,770,f"Bill ID: {bill_rec['billId']}")
            c.drawString(40,750,f"Patient ID: {bill_rec.get('patientId','')}")
            c.drawString(40,730,f"Amount: ₹{bill_rec.get('amount','')}")
            c.drawString(40,710,f"Date: {bill_rec.get('date','')}")
            c.drawString(40,690,f"Mode: {bill_rec.get('mode','')}")
            c.drawString(40,670,f"Paid: {bill_rec.get('paid','')}")
            # QR
            qr = qrcode.make(f"bill:{bill_rec['billId']}")
            qr_io = os.path.join(IMG_DIR, f'billqr_{bill_rec["billId"]}.png'); qr.save(qr_io)
            c.drawImage(qr_io, 420, 720, width=120, height=120)
            c.showPage(); c.save()
            if show_dialog:
                dest = filedialog.asksaveasfilename(defaultextension='.pdf', initialfile=f'bill_{bill_rec["billId"]}.pdf')
                if dest:
                    shutil.copyfile(out_pdf, dest); messagebox.showinfo('Saved', 'Invoice saved to '+dest)
        else:
            # image invoice
            img = Image.new('RGB',(700,900),(255,255,255)); d = ImageDraw.Draw(img)
            try:
                fnt = ImageFont.truetype('arial.ttf', 16)
            except:
                fnt = ImageFont.load_default()
            d.text((30,40), 'Smart Hospital - Invoice', font=fnt, fill=(0,0,0))
            d.text((30,80), f"Bill ID: {bill_rec['billId']}")
            d.text((30,110), f"Patient ID: {bill_rec.get('patientId','')}")
            d.text((30,140), f"Amount: ₹{bill_rec.get('amount','')}")
            d.text((30,170), f"Date: {bill_rec.get('date','')}")
            d.text((30,200), f"Mode: {bill_rec.get('mode','')}")
            d.text((30,230), f"Paid: {bill_rec.get('paid','')}")
            qr = qrcode.make(f"bill:{bill_rec['billId']}"); qr.thumbnail((160,160)); img.paste(qr, (480,90))
            img.save(out_img)
            if show_dialog:
                dest = filedialog.asksaveasfilename(defaultextension='.png', initialfile=f'bill_{bill_rec["billId"]}.png')
                if dest:
                    shutil.copyfile(out_img, dest); messagebox.showinfo('Saved','Invoice saved to '+dest)

    def tab_labreports(self):
        self.clear_area(); frm = ttk.Frame(self.area, padding=8); frm.pack(expand=True, fill='both')
        ttk.Label(frm, text='Lab Reports', font=('Helvetica',14,'bold')).pack(anchor='w')
        tree = ttk.Treeview(frm, columns=('reportId','patient','doctor','date','test','result'), show='headings', height=12)
        for c in ('reportId','patient','doctor','date','test','result'): tree.heading(c, text=c.title()); tree.column(c,width=140)
        tree.pack(fill='both', expand=True)
        for r in self.labreports:
            p = next((pp for pp in self.patients if pp.get('id')==r.get('patientId')), {'name':'?'})
            d = next((dd for dd in self.doctors if dd.get('id')==r.get('doctorId')), {'name':'?'})
            tree.insert('', 'end', values=(r.get('reportId',''), p.get('name','?'), d.get('name','?'), r.get('date',''), r.get('test',''), r.get('result','')))
        ttk.Button(frm, text='Add Report', command=self.add_lab_report).pack(pady=6)

    def add_lab_report(self):
        win = tk.Toplevel(self); win.title('Add Lab Report')
        ttk.Label(win, text='Patient ID').grid(row=0,column=0); e1 = ttk.Entry(win); e1.grid(row=0,column=1)
        ttk.Label(win, text='Doctor ID').grid(row=1,column=0); e2 = ttk.Entry(win); e2.grid(row=1,column=1)
        ttk.Label(win, text='Test').grid(row=2,column=0); e3 = ttk.Entry(win); e3.grid(row=2,column=1)
        ttk.Label(win, text='Result').grid(row=3,column=0); e4 = ttk.Entry(win); e4.grid(row=3,column=1)
        def save():
            rid = 1
            if self.labreports: rid = int(self.labreports[-1]['reportId']) + 1
            rec = {'reportId':str(rid),'patientId':e1.get(),'doctorId':e2.get(),'date':datetime.now().strftime('%Y-%m-%d'),'test':e3.get(),'result':e4.get()}
            self.labreports.append(rec); write_csv('labreports.csv', CSV_HEADERS['labreports'], self.labreports)
            messagebox.showinfo('Saved','Report added'); win.destroy(); self.load_all(); self.show_main()
        ttk.Button(win, text='Save', command=save).grid(row=4,column=0,columnspan=2,pady=6)

    def tab_analytics(self):
        self.clear_area(); frm = ttk.Frame(self.area, padding=8); frm.pack(expand=True, fill='both')
        ttk.Label(frm, text='Analytics', font=('Helvetica',14,'bold')).pack(anchor='w')
        # disease pie
        pie = os.path.join(IMG_DIR,'disease_dist.png'); self.build_disease_pie(pie)
        if os.path.exists(pie):
            img = Image.open(pie); img.thumbnail((760,300)); ph = ImageTk.PhotoImage(img); ttk.Label(frm, image=ph).image = ph; ttk.Label(frm, image=ph).pack(pady=6)
        # income over time
        inc = os.path.join(IMG_DIR,'income_time.png'); self.build_income_over_time(inc)
        if os.path.exists(inc):
            im2 = Image.open(inc); im2.thumbnail((760,220)); ph2 = ImageTk.PhotoImage(im2); ttk.Label(frm, image=ph2).image = ph2; ttk.Label(frm, image=ph2).pack(pady=6)

    def tab_emergency(self):
        self.clear_area(); frm = ttk.Frame(self.area, padding=8); frm.pack(expand=True, fill='both')
        ttk.Label(frm, text='Emergency', font=('Helvetica',14,'bold')).pack(anchor='w')
        ttk.Label(frm, text='Quick actions for emergency cases:').pack(anchor='w')
        ttk.Button(frm, text='Create Emergency Appointment', command=self.create_emergency).pack(pady=6)

    def create_emergency(self):
        win = tk.Toplevel(self); win.title('Emergency Appointment')
        ttk.Label(win, text='Patient Name').grid(row=0,column=0); e1 = ttk.Entry(win); e1.grid(row=0,column=1)
        ttk.Label(win, text='Doctor ID').grid(row=1,column=0); e2 = ttk.Entry(win); e2.grid(row=1,column=1)
        def save():
            # create patient quickly
            pid = 1
            if self.patients: pid = int(self.patients[-1]['id']) + 1
            name = e1.get().strip() or f'Emerg{pid}'
            self.patients.append({'id':str(pid),'name':name,'age':'','gender':'','disease':'Emergency','photo':'','created':datetime.now().strftime('%Y-%m-%d')})
            write_csv('patients.csv', CSV_HEADERS['patients'], self.patients)
            # appointment now
            aid = 1
            if self.appointments: aid = int(self.appointments[-1]['id']) + 1
            rec = {'id':str(aid),'patientId':str(pid),'doctorId':e2.get(),'date':datetime.now().strftime('%Y-%m-%d'),'time':datetime.now().strftime('%H:%M'),'status':'Scheduled'}
            self.appointments.append(rec); write_csv('appointments.csv', CSV_HEADERS['appointments'], self.appointments)
            messagebox.showinfo('Created','Emergency patient and appointment created'); win.destroy(); self.load_all(); self.show_main()
        ttk.Button(win, text='Create', command=save).grid(row=2,column=0,columnspan=2,pady=6)

    # ---- Charts / helpers ----
    def build_disease_pie(self, outpath):
        diseases = [p.get('disease','Unknown') for p in self.patients]
        counts = {}
        for d in diseases: counts[d] = counts.get(d,0) + 1
        labels = list(counts.keys()); sizes = list(counts.values())
        if not sizes: return
        plt.figure(figsize=(6,3.2)); plt.pie(sizes, labels=labels, autopct='%1.1f%%'); plt.title('Disease distribution'); plt.tight_layout(); plt.savefig(outpath); plt.close()

    def build_patient_visits(self, pid, outpath):
        appts = [a for a in self.appointments if a['patientId']==str(pid)]
        if not appts: return
        dates = sorted(list({a['date'] for a in appts}))
        counts = [sum(1 for a in appts if a['date']==d) for d in dates]
        plt.figure(figsize=(5,2.4)); plt.plot(dates, counts, marker='o'); plt.title('Visits over time'); plt.tight_layout(); plt.savefig(outpath); plt.close()

    def build_income_over_time(self, outpath):
        # group bills by month
        inc = {}
        for b in (self.bills or []):
            date = b.get('date','')
            try:
                dt = datetime.strptime(date,'%Y-%m-%d')
                key = dt.strftime('%Y-%m')
                amt = float(b.get('amount',0))
                inc[key] = inc.get(key,0) + amt
            except:
                pass
        if not inc: return
        keys = sorted(inc.keys()); values = [inc[k] for k in keys]
        plt.figure(figsize=(7,2.2)); plt.plot(keys, values, marker='o'); plt.title('Income over months'); plt.tight_layout(); plt.savefig(outpath); plt.close()

    # ---- Export package (zip) ----
    def export_package(self):
        package_path = os.path.join(BASE, 'SHMS_package.zip')
        with zipfile.ZipFile(package_path, 'w') as z:
            z.write(__file__, arcname='shms_full.py')
            for root,_,files in os.walk(DATA_DIR):
                for f in files: z.write(os.path.join(root,f), arcname=os.path.join('data',f))
            for root,_,files in os.walk(IMG_DIR):
                for f in files: z.write(os.path.join(root,f), arcname=os.path.join('images',f))
        messagebox.showinfo('Exported', f'Package created: {package_path}')

if __name__ == '__main__':
    app = SHMSApp()
    app.mainloop()
