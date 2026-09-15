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

const pdfList =
    document.getElementById("pdf-list");

const status =
    document.getElementById("status");


/* ================================
   PDF SELECT
================================ */

pdf.addEventListener("change", () => {

    if (pdf.files.length > 0) {

        const count =
            pdf.files.length;


        /* Main text */

        if (count === 1) {

            pdfName.textContent =
                pdf.files[0].name;

        } else {

            pdfName.textContent =
                `${count} PDFs selected`;

        }


        /* Enable button */

        button.disabled = false;


        /* Clear old list */

        pdfList.innerHTML = "";


        /* Count */

        const countText =
            document.createElement("div");

        countText.className =
            "file-count";

        countText.textContent =
            `${count} PDF${count > 1 ? "s" : ""} selected`;

        pdfList.appendChild(countText);


        /* File names */

        Array.from(pdf.files).forEach(
            (file) => {

                const item =
                    document.createElement("div");

                item.className =
                    "file-item";

                item.innerHTML = `
                    <i class="fa-solid fa-file-pdf"></i>
                    <span>${file.name}</span>
                `;

                pdfList.appendChild(item);

            }
        );


        pdfList.classList.add("show");

    }

    else {

        resetPDF();

    }

});


/* ================================
   LEFT LOGO SELECT
================================ */

leftLogo.addEventListener("change", () => {

    if (leftLogo.files.length > 0) {

        logoName.textContent =
            leftLogo.files[0].name;

    }

    else {

        logoName.textContent =
            "Existing logo will remain";

    }

});


/* ================================
   FORM SUBMIT
================================ */

form.addEventListener("submit", () => {

    button.disabled = true;

    button.innerHTML = `
        <i class="fa-solid fa-spinner fa-spin"></i>
        <span>Processing PDF...</span>
    `;


    status.textContent =
        "Please wait while your PDF is being processed...";

    status.classList.add("show");


    /*
       Browser download complete hone ke
       baad input clear karne ke liye
       thoda delay.
    */

    setTimeout(() => {

        resetPDF();

        resetLogo();

        button.disabled = true;

        button.innerHTML = `
            <i class="fa-solid fa-wand-magic-sparkles"></i>
            <span>Replace & Download</span>
        `;

        status.textContent = "";

        status.classList.remove("show");

    }, 1500);

});


/* ================================
   RESET PDF
================================ */

function resetPDF() {

    pdf.value = "";

    pdfName.textContent =
        "Select one or multiple PDFs";

    pdfList.innerHTML = "";

    pdfList.classList.remove("show");

}


/* ================================
   RESET LOGO
================================ */

function resetLogo() {

    leftLogo.value = "";

    logoName.textContent =
        "Existing logo will remain";

}