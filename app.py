from flask import Flask, render_template, request, send_file
import fitz
import os
import tempfile
from datetime import datetime

app = Flask(__name__)

# =========================================================
# FIXED RIGHT LOGO
# =========================================================

RIGHT_LOGO_FILE = "logo.png"

RIGHT_COVER_RECT = fitz.Rect(235, 10, 300, 45)
RIGHT_LOGO_RECT = fitz.Rect(150, 15, 300, 43)

# =========================================================
# OPTIONAL LEFT LOGO
# =========================================================

LEFT_COVER_RECT = fitz.Rect(5, 5, 150, 48)
LEFT_LOGO_RECT = fitz.Rect(5, 5, 150, 48)


# =========================================================
# PHONE NUMBER
# =========================================================

OLD_PHONE = "8766066070, 0141-4797120"
NEW_PHONE = "+91-9116012366"


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# UPLOAD + PROCESS MULTIPLE PDFS
# =========================================================

@app.route("/upload", methods=["POST"])
def upload():

    # Get ALL selected PDFs
    pdf_files = request.files.getlist("pdf")

    # Optional left logo
    left_logo = request.files.get("left_logo")

    # -----------------------------------------------------
    # Validate PDF
    # -----------------------------------------------------

    pdf_files = [
        pdf_file
        for pdf_file in pdf_files
        if pdf_file and pdf_file.filename
    ]

    if not pdf_files:
        return "Please select at least one PDF.", 400


    # -----------------------------------------------------
    # Optional left logo
    # -----------------------------------------------------

    left_logo_data = None

    if left_logo and left_logo.filename:
        left_logo_data = left_logo.read()


    # -----------------------------------------------------
    # Create one final PDF
    # -----------------------------------------------------

    final_pdf = fitz.open()


    try:

        # =================================================
        # PROCESS EACH PDF
        # =================================================

        for pdf_file in pdf_files:

            # Read uploaded PDF directly into memory
            pdf_data = pdf_file.read()

            if not pdf_data:
                continue

            source_pdf = fitz.open(
                stream=pdf_data,
                filetype="pdf"
            )


            # =============================================
            # PROCESS EACH PAGE
            # =============================================

            for page in source_pdf:

                # -----------------------------------------
                # RIGHT LOGO REPLACE
                # -----------------------------------------

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


                # -----------------------------------------
                # OPTIONAL LEFT LOGO
                # -----------------------------------------

                if left_logo_data:

                    page.draw_rect(
                        LEFT_COVER_RECT,
                        fill=(1, 1, 1),
                        width=0
                    )

                    page.insert_image(
                        LEFT_LOGO_RECT,
                        stream=left_logo_data,
                        keep_proportion=True,
                        overlay=True
                    )


                # -----------------------------------------
                # PHONE NUMBER REPLACE
                # -----------------------------------------

                matches = page.search_for(OLD_PHONE)

                for rect in matches:

                    redact_rect = fitz.Rect(
                        rect.x0,
                        rect.y0,
                        rect.x1,
                        rect.y1 - 2
                    )

                    page.add_redact_annot(
                        redact_rect,
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


            # =============================================
            # ADD THIS PDF'S PAGES TO FINAL PDF
            # =============================================

            final_pdf.insert_pdf(source_pdf)

            source_pdf.close()


        # =================================================
        # CHECK RESULT
        # =================================================

        if final_pdf.page_count == 0:
            final_pdf.close()
            return "No valid PDF pages found.", 400


        # =================================================
        # CURRENT DATE
        # =================================================

        current_date = datetime.now().strftime("%d-%m-%Y")

        download_filename = (
            f"ShipDrop-Label-{current_date}.pdf"
        )


        # =================================================
        # TEMPORARY OUTPUT FILE
        # =================================================

        temp_output = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        )

        output_path = temp_output.name

        temp_output.close()


        # =================================================
        # SAVE FINAL MERGED PDF
        # =================================================

        final_pdf.save(
            output_path,
            garbage=4,
            deflate=True,
            clean=True
        )

        final_pdf.close()


        # =================================================
        # SEND SINGLE PDF
        # =================================================

        response = send_file(
            output_path,
            as_attachment=True,
            download_name=download_filename,
            mimetype="application/pdf"
        )


        # Delete temporary file after response
        @response.call_on_close
        def cleanup():

            if os.path.exists(output_path):

                try:
                    os.remove(output_path)

                except Exception:
                    pass


        return response


    except Exception as e:

        try:
            final_pdf.close()
        except Exception:
            pass

        return f"Error processing PDF: {str(e)}", 500


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )