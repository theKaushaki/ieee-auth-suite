import pandas as pd
import hashlib
import qrcode
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import datetime
import os
import database

# --- Configuration ---
CERTIFICATE_DIR = 'output_certificates'
VALIDATION_URL_BASE = 'http://127.0.0.1:5000/validate/'

# --- PDF Template Class ---
class CertificatePDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 20)
        self.cell(0, 15, 'Certificate of Authorship', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(10)

    def chapter_body(self, author, article, public_id, qr_code_path):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, "This certificate is proudly presented to:", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(10)
        
        self.set_font('Arial', 'B', 18)
        self.multi_cell(0, 10, author, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(10)

        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, "for the authorship of the article:", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(10)

        self.set_font('Arial', 'I', 16)
        self.multi_cell(0, 10, f'"{article}"', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(20)

        # Add QR code and Certificate ID
        self.image(qr_code_path, x=self.w - 50, y=self.h - 50, w=40)
        self.set_y(self.h - 30)
        self.set_font('Courier', '', 10)
        self.cell(0, 10, f"Certificate ID: {public_id}", align='L') 
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Generated on {datetime.now().strftime("%Y-%m-%d")}', align='C')

# --- Main Function ---
def process_csv(file_path):
    if not os.path.exists(CERTIFICATE_DIR):
        os.makedirs(CERTIFICATE_DIR)

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: Input file not found at {file_path}")
        return

    for index, row in df.iterrows():
        author = row['author_name']
        article = row['article_name']

        if database.article_exists(article):
            print(f"Skipping '{article}': Certificate already exists.")
            continue

        # Generate me, baby, sorry for the pun, unique internal certificate ID
        unique_string = f"{author.strip().lower()}-{article.strip().lower()}"
        internal_cert_id = hashlib.sha256(unique_string.encode()).hexdigest()

        # Add the certificate record
        timestamp = datetime.utcnow().isoformat()
        public_id = database.add_certificate(internal_cert_id, author, article, timestamp, "")
        
        # Check me out, lol, cop song flashback
        if not public_id:
            print(f"Failed to create a database record for '{article}'. Skipping PDF generation.")
            continue
        
        # Generate the qr img
        qr_validation_url = f"{VALIDATION_URL_BASE}{public_id}"
        qr_img = qrcode.make(qr_validation_url)
        qr_path = os.path.join(CERTIFICATE_DIR, f"{public_id}_qr.png")
        qr_img.save(qr_path)

        # Generate cert pdf, sounds like pedophile
        pdf_path = os.path.join(CERTIFICATE_DIR, f"{public_id}.pdf")
        pdf = CertificatePDF()
        pdf.add_page()
        pdf.chapter_body(author, article, public_id, qr_path)
        pdf.output(pdf_path)

        # Update the db
        conn = database.get_db_connection()
        with conn:
            conn.execute("UPDATE certificates SET pdf_path = ? WHERE public_id = ?", (pdf_path, public_id))
        conn.close()
        
        # Clean the tempm files of qr
        os.remove(qr_path)


if __name__ == '__main__':
    database.init_db()
    process_csv('input.csv')
    print("\n Certificate generation complete.")