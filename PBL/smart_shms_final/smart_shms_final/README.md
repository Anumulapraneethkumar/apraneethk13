Smart Hospital Management System - Final Package
------------------------------------------------
Enhancements in this final package:
- Role-based login including doctor-specific login (doctor1/doc123).
- Receptionist can add doctors, schedule & prescribe; prescriptions update pharmacy stock.
- Billing supports online (QR) and cash. Online payments can be 'marked paid' which generates a PDF bill.
- Java backend sources included and a script to compile them automatically (scripts/compile_java.sh).
- R analytics script included to produce charts.
- Sample data preloaded in data/.

Requirements:
- Python 3
- pip packages: pillow, qrcode, pandas, reportlab (reportlab optional but required for PDF generation)
  Install with: pip install pillow qrcode pandas reportlab
- Java JDK if you want to compile Java backend (optional)
- R and ggplot2 for running analytics (optional)

Run:
1. Extract the ZIP.
2. Install Python dependencies.
3. Run GUI: python3 python_gui/app.py
4. Compile Java backend (optional): ./scripts/compile_java.sh
5. Run R analytics (optional): Rscript r_scripts/patient_analysis.R data/patients.csv images/patient_diseases_r.png
