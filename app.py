from flask import Flask, render_template, request, send_file
import fitz
import os
from datetime import datetime

app = Flask(__name__)

# Right logo (fixed)
RIGHT_LOGO_FILE = "logo.png"

# Right logo coordinates
RIGHT_COVER_RECT = fitz.Rect(235, 10, 300, 45)
RIGHT_LOGO_RECT = fitz.Rect(137, 12, 310, 44)

# Left logo coordinates
LEFT_COVER_RECT = fitz.Rect(5, 5, 150, 48)
LEFT_LOGO_RECT = fitz.Rect(5, 5, 150, 48)

# Phone number
OLD_PHONE = "8766066070, 0141-4797120"
NEW_PHONE = "+91-9116012366"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    pdf_file = request.files.get("pdf")
    left_logo = request.files.get("left_logo")

    if not pdf_file:
        return "Please select a PDF."

    # Current date
    current_date = datetime.now().strftime("%d-%m-%Y")

    # Output filename
    download_filename = f"ShipDrop-Label-{current_date}.pdf"

    input_pdf = "temp.pdf"
    output_pdf = "output.pdf"

    pdf_file.save(input_pdf)

    left_logo_path = None

    if left_logo and left_logo.filename:

        left_logo_path = "left_logo.png"
        left_logo.save(left_logo_path)

    pdf = fitz.open(input_pdf)

    for page in pdf:

        # =========================
        # RIGHT LOGO REPLACE
        # =========================

        page.draw_rect(
            RIGHT_COVER_RECT,
            fill=(1, 1, 1),
            width=0
        )

        page.insert_image(
            RIGHT_LOGO_RECT,
            filename=RIGHT_LOGO_FILE,
            keep_proportion=True,
            overlay=True
        )

        # =========================
        # LEFT LOGO REPLACE
        # OPTIONAL
        # =========================

        if left_logo_path:

            page.draw_rect(
                LEFT_COVER_RECT,
                fill=(1, 1, 1),
                width=0
            )

            page.insert_image(
                LEFT_LOGO_RECT,
                filename=left_logo_path,
                keep_proportion=True,
                overlay=True
            )

        # =========================
        # PHONE NUMBER REPLACE
        # =========================

        matches = page.search_for(OLD_PHONE)

        for rect in matches:

            page.add_redact_annot(
                fitz.Rect(
                    rect.x0,
                    rect.y0,
                    rect.x1,
                    rect.y1 - 2
                ),
                fill=(1, 1, 1)
            )

            page.apply_redactions()

            page.insert_text(
                fitz.Point(
                    rect.x0,
                    rect.y1 - 2
                ),
                NEW_PHONE,
                fontsize=6.5,
                fontname="Times-Roman"
            )

    # =========================
    # SAVE OPTIMIZED PDF
    # =========================

    pdf.save(
        output_pdf,
        garbage=4,
        deflate=True,
        clean=True
    )

    pdf.close()

    # Delete temporary input
    if os.path.exists(input_pdf):
        os.remove(input_pdf)

    # Delete temporary left logo
    if left_logo_path and os.path.exists(left_logo_path):
        os.remove(left_logo_path)

    # =========================
    # DOWNLOAD
    # =========================

    return send_file(
        output_pdf,
        as_attachment=True,
        download_name=download_filename
    )


if __name__ == "__main__":
    app.run(debug=True)