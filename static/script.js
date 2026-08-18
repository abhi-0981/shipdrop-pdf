const pdf = document.getElementById("pdf");

const leftLogo = document.getElementById("left_logo");

const pdfName = document.getElementById("pdf-name");

const logoName = document.getElementById("logo-name");

const button = document.getElementById("replace-btn");

const form = document.getElementById("upload-form");

pdf.addEventListener("change", () => {

    if (pdf.files.length > 0) {

        pdfName.textContent =
            pdf.files[0].name;

        button.disabled = false;
    }

});

leftLogo.addEventListener("change", () => {

    if (leftLogo.files.length > 0) {

        logoName.textContent =
            leftLogo.files[0].name;

    }

});

form.addEventListener("submit", () => {

    setTimeout(() => {

        form.reset();

        pdfName.textContent =
            "No PDF selected";

        logoName.textContent =
            "Upload Party Logo (Optional)";

        button.disabled = true;

    }, 100);

});