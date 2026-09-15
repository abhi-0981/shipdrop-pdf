const pdf =
    document.getElementById("pdf");

const leftLogo =
    document.getElementById("left_logo");

const pdfName =
    document.getElementById("pdf-name");

const logoName =
    document.getElementById("logo-name");

const button =
    document.getElementById("replace-btn");

const form =
    document.getElementById("upload-form");


// ======================================================
// PDF SELECTION
// ======================================================

pdf.addEventListener("change", () => {

    if (pdf.files.length > 0) {

        const count = pdf.files.length;

        if (count === 1) {

            pdfName.textContent =
                pdf.files[0].name;

        } else {

            pdfName.textContent =
                `${count} PDFs selected`;

        }

        button.disabled = false;

    } else {

        pdfName.textContent =
            "Select one or multiple PDFs";

        button.disabled = true;
    }

});


// ======================================================
// LEFT LOGO SELECTION
// ======================================================

leftLogo.addEventListener("change", () => {

    if (leftLogo.files.length > 0) {

        logoName.textContent =
            leftLogo.files[0].name;

    } else {

        logoName.textContent =
            "Optional — existing logo will remain";

    }

});


// ======================================================
// FORM SUBMIT
// ======================================================

form.addEventListener("submit", () => {

    // Disable button while processing
    button.disabled = true;

    button.innerHTML = `
        <i class="fa-solid fa-spinner fa-spin"></i>
        Processing PDFs...
    `;


    // Clear selected files shortly after submit
    setTimeout(() => {

        pdf.value = "";

        leftLogo.value = "";

        pdfName.textContent =
            "Select one or multiple PDFs";

        logoName.textContent =
            "Optional — existing logo will remain";

        button.innerHTML = `
            <i class="fa-solid fa-wand-magic-sparkles"></i>
            Replace & Download
        `;

        button.disabled = true;

    }, 1000);

});