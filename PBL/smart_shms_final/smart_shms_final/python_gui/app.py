import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import csv, os, subprocess, json, qrcode
from datetime import datetime
import io

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE, 'data')
IMG_DIR = os.path.join(BASE, 'images')
R_SCRIPT = os.path.join(BASE, 'r_scripts', 'patient_analysis.R')
JAVA_BIN = os.path.join(BASE, 'bin')  # after compile script
os.makedirs(DATA_DIR, exist_ok=True)

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

# Simple PDF generator using reportlab if available
def generate_pdf_bill(bill_rec, out_path):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except Exception as e:
        print("reportlab not installed:", e)
        return False
    c = canvas.Canvas(out_path, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40,800,"Smart Hospital - Bill")
    c.setFont("Helvetica", 12)
    c.drawString(40,760,f"Bill ID: {bill_rec['billId']}")
    c.drawString(40,740,f"Patient ID: {bill_rec['patientId']}")
    c.drawString(40,720,f"Amount: ₹{bill_rec['amount']}")
    c.drawString(40,700,f"Date: {bill_rec['date']}")
    c.drawString(40,660,"Thank you for your payment.")
    c.showPage()
    c.save()
    return True

class RoleLogin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('SHMS - Role Login')
        self.geometry('420x260')
        frm = ttk.Frame(self, padding=12); frm.pack(expand=True, fill='both')
        ttk.Label(frm, text='Smart HMS - Select Role', font=('Helvetica',14,'bold')).pack(pady=8)
        ttk.Label(frm, text='Role').pack(anchor='w')
        self.role = tk.StringVar(value='Receptionist')
        ttk.Combobox(frm, textvariable=self.role, values=['Receptionist','Doctor','Pharmacy','Admin']).pack(fill='x')
        ttk.Label(frm, text='Username').pack(anchor='w', pady=(8,0))
        self.user = ttk.Entry(frm); self.user.pack(fill='x')
        ttk.Label(frm, text='Password').pack(anchor='w', pady=(8,0))
        self.pw = ttk.Entry(frm, show='*'); self.pw.pack(fill='x')
        btnf = ttk.Frame(frm); btnf.pack(pady=12)
        ttk.Button(btnf, text='Login', command=self.check).grid(row=0,column=0,padx=6)
        ttk.Button(btnf, text='Open Demo', command=self.open_demo).grid(row=0,column=1,padx=6)
        ttk.Label(frm, text='Demo creds: admin/admin123').pack(pady=6)

    def check(self):
        # role-based simple auth: doctor users like doctor1, doctor2 to auto map doctor id
        user = self.user.get().strip()
        pwd = self.pw.get().strip()
        role = self.role.get()
        if user=='admin' and pwd=='admin123':
            self.open_main(role, user)
            return
        if role=='Doctor' and user.startswith('doctor') and pwd=='doc123':
            self.open_main(role, user)
            return
        if role in ('Receptionist','Pharmacy') and user in ('reception','pharmacy') and pwd=='staff123':
            self.open_main(role, user)
            return
        messagebox.showerror('Auth','Invalid credentials. Demo accounts: admin/admin123, doctor1/doc123, reception/staff123, pharmacy/staff123')

    def open_demo(self):
        self.open_main(self.role.get(), 'demo')

    def open_main(self, role, user):
        self.destroy()
        app = MainApp(role, user)
        app.mainloop()

class MainApp(tk.Tk):
    def __init__(self, role, user):
        super().__init__()
        self.role = role
        self.user = user
        self.title(f'SHMS - {role} Dashboard ({user})')
        self.geometry('1150x720')
        self.load_all()
        self.create_widgets()

    def load_all(self):
        self.patients = read_csv('patients.csv')
        self.doctors = read_csv('doctors.csv')
        self.appointments = read_csv('appointments.csv')
        self.pharmacy = read_csv('pharmacy.csv')
        self.bills = read_csv('bills.csv')
        self.prescriptions = read_csv('prescriptions.csv')
        self.labreports = read_csv('labreports.csv')

    def create_widgets(self):
        top = ttk.Frame(self, padding=8); top.pack(fill='x')
        ttk.Label(top, text=f'SHMS - {self.role} ({self.user})', font=('Helvetica',16,'bold')).pack(side='left')
        ttk.Button(top, text='Compile Java Backend', command=self.compile_java).pack(side='right', padx=6)
        ttk.Button(top, text='Run R Analytics', command=self.run_r).pack(side='right', padx=6)
        ttk.Button(top, text='Refresh', command=self.reload).pack(side='right', padx=6)
        ttk.Button(top, text='Export CSVs', command=self.export_csvs).pack(side='right', padx=6)

        main = ttk.Frame(self, padding=8); main.pack(expand=True, fill='both')
        menu = ttk.Frame(main, width=260); menu.pack(side='left', fill='y', padx=(0,8))
        ttk.Button(menu, text='Patients', command=self.tab_patients).pack(fill='x', pady=4)
        ttk.Button(menu, text='Doctors', command=self.tab_doctors).pack(fill='x', pady=4)
        ttk.Button(menu, text='Appointments', command=self.tab_appointments).pack(fill='x', pady=4)
        ttk.Button(menu, text='Pharmacy', command=self.tab_pharmacy).pack(fill='x', pady=4)
        ttk.Button(menu, text='Billing', command=self.tab_billing).pack(fill='x', pady=4)
        ttk.Button(menu, text='Lab Reports', command=self.tab_labreports).pack(fill='x', pady=4)
        ttk.Button(menu, text='Dashboard', command=self.tab_dashboard).pack(fill='x', pady=4)

        self.area = ttk.Frame(main); self.area.pack(side='right', expand=True, fill='both')
        if self.role=='Doctor':
            self.tab_doctor_portal()
        else:
            self.tab_dashboard()

    def compile_java(self):
        script = os.path.join(BASE, 'scripts', 'compile_java.sh')
        if not os.path.exists(script):
            messagebox.showerror('Script missing', 'compile_java.sh is missing.')
            return
        try:
            subprocess.run([script], check=True, cwd=BASE, timeout=10)
            messagebox.showinfo('Compiled', 'Java backend compiled to bin/.')
        except Exception as e:
            messagebox.showerror('Compile error', str(e))

    def reload(self):
        self.load_all()
        self.refresh_current_tab()

    def clear_area(self):
        for w in self.area.winfo_children():
            w.destroy()

    def tab_dashboard(self):
        self.clear_area()
        frm = ttk.Frame(self.area, padding=8); frm.pack(expand=True, fill='both')
        ttk.Label(frm, text='Dashboard', font=('Helvetica',14,'bold')).pack(anchor='w')
        # stats
        total_patients = len(self.patients)
        total_doctors = len(self.doctors)
        upcoming = sum(1 for a in self.appointments if a['status']=='Scheduled')
        ttk.Label(frm, text=f'Total Patients: {total_patients}').pack(anchor='w', pady=2)
        ttk.Label(frm, text=f'Total Doctors: {total_doctors}').pack(anchor='w', pady=2)
        ttk.Label(frm, text=f'Upcoming Appointments: {upcoming}').pack(anchor='w', pady=2)
        # reminders (next 3 appointments)
        ttk.Label(frm, text='Next Appointments:').pack(anchor='w', pady=(8,0))
        for a in sorted(self.appointments, key=lambda x: (x.get('date',''), x.get('time','')))[:5]:
            ttk.Label(frm, text=f"{a.get('date','')} {a.get('time','')} Patient {a.get('patientId','')} Doctor {a.get('doctorId','')}").pack(anchor='w')

    # patients tab with search and history (same as before)
    def tab_patients(self):
        self.clear_area()
        frm = ttk.Frame(self.area, padding=8); frm.pack(expand=True, fill='both')
        ttk.Label(frm, text='Patients', font=('Helvetica',14,'bold')).pack(anchor='w')
        searchf = ttk.Frame(frm); searchf.pack(fill='x')
        ttk.Label(searchf, text='Search:').pack(side='left')
        svar = tk.StringVar()
        sentry = ttk.Entry(searchf, textvariable=svar); sentry.pack(side='left', padx=4)
        def do_search():
            q = svar.get().lower().strip()
            for i in self.tree_p.get_children(): self.tree_p.delete(i)
            for p in self.patients:
                if q in p['name'].lower() or q==p['id']:
                    self.tree_p.insert('', 'end', values=(p['id'],p['name'],p.get('age',''),p.get('gender',''),p.get('disease','')))
        ttk.Button(searchf, text='Go', command=do_search).pack(side='left', padx=4)

        cols = ('id','name','age','gender','disease')
        self.tree_p = ttk.Treeview(frm, columns=cols, show='headings', height=12)
        for c in cols:
            self.tree_p.heading(c, text=c.title()); self.tree_p.column(c, width=110)
        self.tree_p.pack(side='left', fill='both', expand=True, pady=6)
        for p in self.patients:
            self.tree_p.insert('', 'end', values=(p['id'],p['name'],p.get('age',''),p.get('gender',''),p.get('disease','')))
        self.tree_p.bind('<<TreeviewSelect>>', self.show_patient_history)

        right = ttk.Frame(frm, width=380); right.pack(side='right', fill='y', padx=8)
        ttk.Label(right, text='Patient History', font=('Helvetica',12,'bold')).pack(anchor='w')
        self.hist_txt = tk.Text(right, width=45, height=25); self.hist_txt.pack()
        btnf = ttk.Frame(right); btnf.pack(pady=6)
        ttk.Button(btnf, text='Add Patient', command=self.add_patient).grid(row=0,column=0,padx=4)
        ttk.Button(btnf, text='Schedule & Prescribe', command=self.schedule_and_prescribe).grid(row=0,column=1,padx=4)
        ttk.Button(btnf, text='View Photo', command=lambda: self.view_photo(self.tree_p,'patient')).grid(row=1,column=0,padx=4,pady=6)
        ttk.Button(btnf, text='Delete', command=lambda: self.delete_selected(self.tree_p,'patients')).grid(row=1,column=1,padx=4,pady=6)

    def show_patient_history(self, event):
        sel = self.tree_p.selection()
        if not sel: return
        vals = self.tree_p.item(sel[0])['values']
        pid = str(vals[0])
        appts = [a for a in self.appointments if a['patientId']==pid]
        pres = [p for p in self.prescriptions if p['patientId']==pid]
        bills = [b for b in self.bills if b['patientId']==pid]
        labs = [l for l in self.labreports if l['patientId']==pid]
        lines = []
        lines.append(f"Patient ID: {pid}\nName: {vals[1]}\n")
        lines.append("Appointments:")
        for a in appts:
            lines.append(f" - {a.get('date','')} {a.get('time','')} with Doctor {a.get('doctorId','')} status:{a.get('status','')}")
        lines.append("\nPrescriptions:")
        for p in pres:
            lines.append(f" - {p.get('date','')} : {p.get('medicine','')} x{p.get('quantity','')}")
        lines.append("\nLab Reports:")
        for l in labs:
            lines.append(f" - {l.get('date','')} {l.get('test','')}: {l.get('result','')}")
        lines.append("\nBills (day by day):")
        bills_sorted = sorted(bills, key=lambda x: x.get('date',''))
        total = 0.0
        for b in bills_sorted:
            amt = float(b.get('amount',0))
            total += amt
            lines.append(f" - {b.get('date','')}: ₹{amt:.2f}")
        lines.append(f"\nTotal billed till date: ₹{total:.2f}")
        self.hist_txt.delete('1.0','end')
        self.hist_txt.insert('1.0', '\n'.join(lines))

    def add_patient(self):
        win = tk.Toplevel(self); win.title('Add Patient')
        ttk.Label(win, text='Name').grid(row=0,column=0); e1 = ttk.Entry(win); e1.grid(row=0,column=1)
        ttk.Label(win, text='Age').grid(row=1,column=0); e2 = ttk.Entry(win); e2.grid(row=1,column=1)
        ttk.Label(win, text='Gender').grid(row=2,column=0); e3 = ttk.Entry(win); e3.grid(row=2,column=1)
        ttk.Label(win, text='Disease').grid(row=3,column=0); e4 = ttk.Entry(win); e4.grid(row=3,column=1)
        ttk.Label(win, text='Photo').grid(row=4,column=0); pvar = tk.StringVar(); ttk.Entry(win, textvariable=pvar).grid(row=4,column=1)
        def browse():
            p = filedialog.askopenfilename(initialdir=IMG_DIR, filetypes=[('PNG','*.png'),('JPG','*.jpg')])
            if p: pvar.set(os.path.basename(p))
        ttk.Button(win, text='Browse', command=browse).grid(row=4,column=2)
        def save():
            pid = 1
            if self.patients: pid = int(self.patients[-1]['id']) + 1
            rec = {'id':str(pid),'name':e1.get(),'age':e2.get(),'gender':e3.get(),'disease':e4.get(),'photo':pvar.get()}
            self.patients.append(rec)
            write_csv('patients.csv',['id','name','age','gender','disease','photo'], self.patients)
            self.refresh_current_tab(); win.destroy()
        ttk.Button(win, text='Save', command=save).grid(row=5,column=0,columnspan=3,pady=6)

    def schedule_and_prescribe(self):
        sel = self.tree_p.selection()
        if not sel: messagebox.showerror('Select','Select a patient first'); return
        pid = self.tree_p.item(sel[0])['values'][0]
        win = tk.Toplevel(self); win.title('Schedule & Prescribe')
        ttk.Label(win, text='Doctor ID').grid(row=0,column=0); d1 = ttk.Entry(win); d1.grid(row=0,column=1)
        ttk.Label(win, text='Date (YYYY-MM-DD)').grid(row=1,column=0); d2 = ttk.Entry(win); d2.grid(row=1,column=1)
        ttk.Label(win, text='Time (HH:MM)').grid(row=2,column=0); d3 = ttk.Entry(win); d3.grid(row=2,column=1)
        ttk.Label(win, text='Medicine (comma separated)').grid(row=3,column=0); d4 = ttk.Entry(win); d4.grid(row=3,column=1)
        ttk.Label(win, text='Quantities (comma separated)').grid(row=4,column=0); d5 = ttk.Entry(win); d5.grid(row=4,column=1)
        def save():
            aid = 1
            if self.appointments: aid = int(self.appointments[-1]['id']) + 1
            rec = {'id':str(aid),'patientId':str(pid),'doctorId':d1.get(),'date':d2.get(),'time':d3.get(),'status':'Scheduled'}
            self.appointments.append(rec)
            write_csv('appointments.csv',['id','patientId','doctorId','date','time','status'], self.appointments)
            meds = [m.strip() for m in d4.get().split(',') if m.strip()]
            qtys = [q.strip() for q in d5.get().split(',') if q.strip()]
            for i,med in enumerate(meds):
                q = qtys[i] if i<len(qtys) else '1'
                pidp = 1
                if self.prescriptions: pidp = int(self.prescriptions[-1]['prescId']) + 1
                pres = {'prescId':str(pidp),'patientId':str(pid),'doctorId':d1.get(),'date':d2.get(),'medicine':med,'quantity':q}
                self.prescriptions.append(pres)
                for mrec in self.pharmacy:
                    if mrec['medicine'].lower()==med.lower():
                        try: mrec['quantity'] = str(max(0, int(mrec.get('quantity',0)) - int(q)))
                        except: pass
            write_csv('prescriptions.csv',['prescId','patientId','doctorId','date','medicine','quantity'], self.prescriptions)
            write_csv('pharmacy.csv',['medicine','quantity','price'], self.pharmacy)
            messagebox.showinfo('Saved','Appointment and prescriptions saved; pharmacy updated.')
            win.destroy(); self.refresh_current_tab()
        ttk.Button(win, text='Save', command=save).grid(row=5,column=0,columnspan=2,pady=6)

    def tab_doctors(self):
        self.clear_area()
        frm = ttk.Frame(self.area, padding=8); frm.pack(expand=True, fill='both')
        ttk.Label(frm, text='Doctors & Availability', font=('Helvetica',14,'bold')).pack(anchor='w')
        cols = ('id','name','specialization','today_count','next_slot')
        tree = ttk.Treeview(frm, columns=cols, show='headings', height=12)
        for c in cols: tree.heading(c, text=c.title()); tree.column(c, width=140)
        tree.pack(expand=True, fill='both', pady=6)
        today = datetime.now().strftime('%Y-%m-%d')
        for d in self.doctors:
            cnt = sum(1 for a in self.appointments if a['doctorId']==d['id'] and a['date']==today and a['status']=='Scheduled')
            slots = [a for a in self.appointments if a['doctorId']==d['id'] and a['status']=='Scheduled']
            next_slot = slots[0]['date']+' '+slots[0]['time'] if slots else ''
            tree.insert('', 'end', values=(d['id'],d['name'],d['specialization'],str(cnt),next_slot))
        def on_double(e):
            sel = tree.selection(); 
            if not sel: return
            did = tree.item(sel[0])['values'][0]; self.open_doctor_portal(did)
        tree.bind('<Double-1>', on_double)
        # receptionist can add doctor
        if self.role=='Receptionist' or self.role=='Admin':
            ttk.Button(frm, text='Add Doctor', command=self.add_doctor).pack(pady=6)

    def add_doctor(self):
        win = tk.Toplevel(self); win.title('Add Doctor')
        ttk.Label(win, text='Name').grid(row=0,column=0); e1 = ttk.Entry(win); e1.grid(row=0,column=1)
        ttk.Label(win, text='Specialization').grid(row=1,column=0); e2 = ttk.Entry(win); e2.grid(row=1,column=1)
        ttk.Label(win, text='Photo').grid(row=2,column=0); pvar = tk.StringVar(); ttk.Entry(win, textvariable=pvar).grid(row=2,column=1)
        def browse(): p = filedialog.askopenfilename(initialdir=IMG_DIR, filetypes=[('PNG','*.png'),('JPG','*.jpg')]); 
        ttk.Button(win, text='Save', command=lambda: self.save_doctor(e1.get(), e2.get(), pvar.get())).grid(row=3,column=0,columnspan=2,pady=6)

    def save_doctor(self, name, spec, photo):
        did = 1
        if self.doctors: did = int(self.doctors[-1]['id']) + 1
        rec = {'id':str(did),'name':name,'specialization':spec,'photo':photo}
        self.doctors.append(rec); write_csv('doctors.csv',['id','name','specialization','photo'], self.doctors)
        messagebox.showinfo('Saved','Doctor added.'); self.refresh_current_tab()

    def open_doctor_portal(self, doctor_id):
        win = tk.Toplevel(self); win.title(f'Doctor {doctor_id} Portal')
        ttk.Label(win, text=f'Doctor ID: {doctor_id}', font=('Helvetica',12,'bold')).pack(pady=6)
        today = datetime.now().strftime('%Y-%m-%d')
        my_appts = [a for a in self.appointments if a['doctorId']==str(doctor_id)]
        txt = tk.Text(win, width=100, height=25); txt.pack()
        lines = ['All scheduled appointments for this doctor:']
        for a in sorted(my_appts, key=lambda x: (x.get('date',''), x.get('time',''))):
            lines.append(f" - {a.get('date','')} {a.get('time','')} Patient {a.get('patientId','')} status:{a.get('status','')}")
        txt.insert('1.0','\n'.join(lines))

    def tab_appointments(self):
        self.clear_area()
        frm = ttk.Frame(self.area, padding=8); frm.pack(expand=True, fill='both')
        ttk.Label(frm, text='Appointments', font=('Helvetica',14,'bold')).pack(anchor='w')
        cols = ('id','patientId','doctorId','date','time','status')
        tree = ttk.Treeview(frm, columns=cols, show='headings', height=15)
        for c in cols: tree.heading(c, text=c.title()); tree.column(c, width=120)
        tree.pack(expand=True, fill='both', pady=6)
        for a in self.appointments: tree.insert('', 'end', values=(a['id'],a['patientId'],a['doctorId'],a['date'],a['time'],a['status']))
        btnf = ttk.Frame(frm); btnf.pack()
        ttk.Button(btnf, text='Mark Done', command=lambda: self.mark_done(tree)).pack(side='left', padx=4)
        ttk.Button(btnf, text='Delete', command=lambda: self.delete_selected(tree,'appointments')).pack(side='left', padx=4)

    def mark_done(self, tree):
        sel = tree.selection(); 
        if not sel: messagebox.showerror('Select','Select appointment'); return
        vals = tree.item(sel[0])['values']; aid = str(vals[0])
        for a in self.appointments:
            if a['id']==aid: a['status']='Done'
        write_csv('appointments.csv',['id','patientId','doctorId','date','time','status'], self.appointments)
        self.refresh_current_tab(); messagebox.showinfo('Updated','Appointment marked done.')

    def tab_pharmacy(self):
        self.clear_area()
        frm = ttk.Frame(self.area, padding=8); frm.pack(expand=True, fill='both')
        ttk.Label(frm, text='Pharmacy Stock', font=('Helvetica',14,'bold')).pack(anchor='w')
        cols = ('medicine','quantity','price')
        tree = ttk.Treeview(frm, columns=cols, show='headings', height=12)
        for c in cols: tree.heading(c, text=c.title()); tree.column(c, width=150)
        tree.pack(expand=True, fill='both', pady=6)
        for m in self.pharmacy: tree.insert('', 'end', values=(m['medicine'], m.get('quantity',''), m.get('price','')))
        btnf = ttk.Frame(frm); btnf.pack(pady=6)
        ttk.Button(btnf, text='Fulfill Prescription', command=lambda: self.fulfill_prescription(tree)).pack(side='left', padx=4)
        ttk.Button(btnf, text='Add/Update Medicine', command=lambda: self.manage_medicine(tree)).pack(side='left', padx=4)

    def fulfill_prescription(self, tree):
        pres = self.prescriptions
        if not pres: messagebox.showinfo('No Prescriptions','No prescriptions available.'); return
        win = tk.Toplevel(self); win.title('Select Prescription to Fulfill')
        lst = tk.Listbox(win, width=80)
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
            write_csv('pharmacy.csv',['medicine','quantity','price'], self.pharmacy)
            messagebox.showinfo('Fulfilled', f'Prescription {rec['prescId']} fulfilled. Stock updated.'); win.destroy(); self.refresh_current_tab()
        ttk.Button(win, text='Fulfill', command=fulfill).pack(pady=6)

    def tab_billing(self):
        self.clear_area()
        frm = ttk.Frame(self.area, padding=8); frm.pack(expand=True, fill='both')
        ttk.Label(frm, text='Billing', font=('Helvetica',14,'bold')).pack(anchor='w')
        cols = ('billId','patientId','amount','date','mode','paid')
        tree = ttk.Treeview(frm, columns=cols, show='headings', height=12)
        for c in cols: tree.heading(c, text=c.title()); tree.column(c, width=120)
        tree.pack(expand=True, fill='both', pady=6)
        for b in self.bills: tree.insert('', 'end', values=(b.get('billId',''),b.get('patientId',''),b.get('amount',''),b.get('date',''),b.get('mode',''),b.get('paid','')))
        btnf = ttk.Frame(frm); btnf.pack(pady=6)
        ttk.Button(btnf, text='Generate Bill', command=lambda: self.generate_bill(tree)).pack(side='left', padx=4)
        ttk.Button(btnf, text='Undo Last (Java stack)', command=self.java_undo_bill).pack(side='left', padx=4)
        ttk.Button(btnf, text='Download PDF', command=lambda: self.download_selected_pdf(tree)).pack(side='left', padx=4)

    def generate_bill(self, tree):
        win = tk.Toplevel(self); win.title('Generate Bill')
        ttk.Label(win, text='Patient ID').grid(row=0,column=0); e1 = ttk.Entry(win); e1.grid(row=0,column=1)
        ttk.Label(win, text='Amount').grid(row=1,column=0); e2 = ttk.Entry(win); e2.grid(row=1,column=1)
        ttk.Label(win, text='Mode (Cash/Online)').grid(row=2,column=0); e3 = ttk.Combobox(win, values=['Cash','Online']); e3.grid(row=2,column=1)
        def save():
            bid = 1
            if self.bills: bid = int(self.bills[-1]['billId']) + 1
            amt = float(e2.get())
            mode = e3.get() or 'Cash'
            rec = {'billId':str(bid),'patientId':e1.get(),'amount':str(amt),'date': datetime.now().strftime('%Y-%m-%d'),'mode':mode,'paid':'no' if mode=='Online' else 'yes'}
            self.bills.append(rec); write_csv('bills.csv',['billId','patientId','amount','date','mode','paid'], self.bills)
            tree.insert('', 'end', values=(rec['billId'],rec['patientId'],rec['amount'],rec['date'],rec['mode'],rec['paid']))
            if mode=='Online':
                # generate QR and show dialog with "Mark Paid"
                qrdata = f"PAYMENT|bill:{rec['billId']}|patient:{rec['patientId']}|amount:{rec['amount']}"
                img = qrcode.make(qrdata); qrpath = os.path.join(BASE,'images',f'qr_bill_{rec['billId']}.png'); img.save(qrpath)
                # show QR
                qwin = tk.Toplevel(self); qwin.title('Online Payment - Scan QR')
                pil = Image.open(qrpath); pil.thumbnail((300,300)); ph = ImageTk.PhotoImage(pil)
                lbl = ttk.Label(qwin, image=ph); lbl.image = ph; lbl.pack(pady=6)
                ttk.Button(qwin, text='Mark Paid', command=lambda: self.mark_paid(rec['billId'], qwin)).pack(pady=6)
            win.destroy()
        ttk.Button(win, text='Generate', command=save).grid(row=3,column=0,columnspan=2,pady=6)

    def mark_paid(self, billId, win=None):
        for b in self.bills:
            if b['billId']==str(billId):
                b['paid']='yes'
                write_csv('bills.csv',['billId','patientId','amount','date','mode','paid'], self.bills)
                # generate PDF
                out = os.path.join(BASE,'images', f'bill_{billId}.pdf')
                ok = generate_pdf_bill(b, out)
                if ok:
                    messagebox.showinfo('Paid','Payment recorded and PDF bill generated at images/{}.pdf'.format(billId))
                else:
                    messagebox.showinfo('Paid','Payment recorded but reportlab not installed; cannot generate PDF.')
                break
        if win: win.destroy()
        self.refresh_current_tab()

    def download_selected_pdf(self, tree):
        sel = tree.selection()
        if not sel: messagebox.showerror('Select','Select a bill to download'); return
        vals = tree.item(sel[0])['values']
        billId = str(vals[0])
        pdf_path = os.path.join(BASE,'images', f'bill_{billId}.pdf')
        if not os.path.exists(pdf_path):
            messagebox.showerror('Not found','PDF not found. Mark paid to generate PDF for online bills or use reportlab.')
            return
        dest = filedialog.asksaveasfilename(defaultextension='.pdf', initialfile=f'bill_{billId}.pdf')
        if dest:
            shutil.copyfile(pdf_path, dest)
            messagebox.showinfo('Saved','PDF saved to ' + dest)

    def tab_labreports(self):
        self.clear_area()
        frm = ttk.Frame(self.area, padding=8); frm.pack(expand=True, fill='both')
        ttk.Label(frm, text='Lab Reports', font=('Helvetica',14,'bold')).pack(anchor='w')
        cols = ('reportId','patientId','doctorId','date','test','result')
        tree = ttk.Treeview(frm, columns=cols, show='headings', height=12)
        for c in cols: tree.heading(c, text=c.title()); tree.column(c, width=120)
        tree.pack(expand=True, fill='both', pady=6)
        for r in self.labreports: tree.insert('', 'end', values=(r['reportId'],r['patientId'],r['doctorId'],r['date'],r['test'],r['result']))
        ttk.Button(frm, text='Add Report', command=self.add_lab_report).pack(pady=6)

    def add_lab_report(self):
        win = tk.Toplevel(self); win.title('Add Lab Report')
        ttk.Label(win, text='Patient ID').grid(row=0,column=0); e1 = ttk.Entry(win); e1.grid(row=0,column=1)
        ttk.Label(win, text='Doctor ID').grid(row=1,column=0); e2 = ttk.Entry(win); e2.grid(row=1,column=1)
        ttk.Label(win, text='Test Name').grid(row=2,column=0); e3 = ttk.Entry(win); e3.grid(row=2,column=1)
        ttk.Label(win, text='Result').grid(row=3,column=0); e4 = ttk.Entry(win); e4.grid(row=3,column=1)
        def save():
            rid = 1
            if self.labreports: rid = int(self.labreports[-1]['reportId']) + 1
            rec = {'reportId':str(rid),'patientId':e1.get(),'doctorId':e2.get(),'date': datetime.now().strftime('%Y-%m-%d'),'test':e3.get(),'result':e4.get()}
            self.labreports.append(rec); write_csv('labreports.csv',['reportId','patientId','doctorId','date','test','result'], self.labreports); win.destroy(); self.refresh_current_tab()
        ttk.Button(win, text='Save', command=save).grid(row=4,column=0,columnspan=2,pady=6)

    def tab_doctor_portal(self):
        self.clear_area()
        frm = ttk.Frame(self.area, padding=8); frm.pack(expand=True, fill='both')
        ttk.Label(frm, text='Doctor Portal - Today\'s Schedule', font=('Helvetica',14,'bold')).pack(anchor='w')
        cols = ('time','patientId','status')
        tree = ttk.Treeview(frm, columns=cols, show='headings', height=18)
        for c in cols: tree.heading(c, text=c.title()); tree.column(c, width=160)
        tree.pack(expand=True, fill='both', pady=6)
        today = datetime.now().strftime('%Y-%m-%d')
        # if doctor login, filter by doctor id from username (e.g., doctor2)
        doc_id = None
        if self.role=='Doctor' and self.user and self.user.startswith('doctor'):
            try:
                doc_id = self.user.replace('doctor','')
            except: doc_id = None
        for a in self.appointments:
            if a['date']==today and (doc_id is None or a['doctorId']==str(doc_id)):
                tree.insert('', 'end', values=(a['time'], a['patientId'], a['status']))
        ttk.Button(frm, text='Mark Done', command=lambda: self.mark_done(tree)).pack(pady=6)

    # Utilities
    def view_photo(self, tree, kind):
        sel = tree.selection()
        if not sel: messagebox.showerror('Select','Please select a row'); return
        vals = tree.item(sel[0])['values']
        if kind=='patient':
            pid = vals[0]; rec = next((p for p in self.patients if p['id']==str(pid)), None); fname = rec.get('photo','') if rec else ''
        else:
            did = vals[0]; rec = next((d for d in self.doctors if d['id']==str(did)), None); fname = rec.get('photo','') if rec else ''
        if not fname: messagebox.showinfo('No Photo','No photo available'); return
        path = os.path.join(IMG_DIR, fname)
        if not os.path.exists(path): messagebox.showerror('Not Found', f'Image {fname} not found'); return
        top = tk.Toplevel(self); top.title('Photo'); img = Image.open(path); img.thumbnail((600,600)); ph = ImageTk.PhotoImage(img); ttk.Label(top, image=ph).pack()

    def delete_selected(self, tree, table):
        sel = tree.selection(); 
        if not sel: messagebox.showerror('Select','Select a row to delete'); return
        vals = tree.item(sel[0])['values']
        if table=='patients': self.patients = [p for p in self.patients if p['id'] != str(vals[0])]; write_csv('patients.csv',['id','name','age','gender','disease','photo'], self.patients)
        elif table=='doctors': self.doctors = [d for d in self.doctors if d['id'] != str(vals[0])]; write_csv('doctors.csv',['id','name','specialization','photo'], self.doctors)
        elif table=='appointments': self.appointments = [a for a in self.appointments if a['id'] != str(vals[0])]; write_csv('appointments.csv',['id','patientId','doctorId','date','time','status'], self.appointments)
        elif table=='pharmacy': self.pharmacy = [m for m in self.pharmacy if m['medicine'] != str(vals[0])]; write_csv('pharmacy.csv',['medicine','quantity','price'], self.pharmacy)
        self.refresh_current_tab()

    def refresh_current_tab(self):
        self.load_all()
        self.tab_dashboard()

    def export_csvs(self):
        write_csv('patients.csv',['id','name','age','gender','disease','photo'], self.patients)
        write_csv('doctors.csv',['id','name','specialization','photo'], self.doctors)
        write_csv('appointments.csv',['id','patientId','doctorId','date','time','status'], self.appointments)
        write_csv('pharmacy.csv',['medicine','quantity','price'], self.pharmacy)
        write_csv('bills.csv',['billId','patientId','amount','date','mode','paid'], self.bills)
        write_csv('prescriptions.csv',['prescId','patientId','doctorId','date','medicine','quantity'], self.prescriptions)
        write_csv('labreports.csv',['reportId','patientId','doctorId','date','test','result'], self.labreports)
        messagebox.showinfo('Exported','CSV files exported to data/')

    def run_r(self):
        try:
            subprocess.run(['Rscript', R_SCRIPT, os.path.join(DATA_DIR,'patients.csv'), os.path.join(BASE,'images','patient_diseases_r.png')], check=True, timeout=10)
            path = os.path.join(BASE, 'images', 'patient_diseases_r.png')
            if os.path.exists(path):
                top = tk.Toplevel(self); top.title('R Chart'); img = Image.open(path); img.thumbnail((800,500)); ph = ImageTk.PhotoImage(img); ttk.Label(top, image=ph).pack()
        except Exception as e:
            messagebox.showinfo('R Error', 'Could not run R script (ensure R is installed).')

    def java_undo_bill(self):
        try:
            jcmd = ['java','-cp', os.path.join(BASE,'bin'), 'BillingManager', 'pop']
            out = subprocess.check_output(jcmd, timeout=3).decode().strip()
            if out: messagebox.showinfo('Java Undo', out)
        except Exception as e:
            messagebox.showinfo('Info', 'Java undo simulated (no JVM or not compiled).')

    def import_sample(self):
        messagebox.showinfo('Import Sample', 'Sample data is in data/ folder.')

if __name__ == '__main__':
    RoleLogin().mainloop()
