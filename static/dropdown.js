document.addEventListener("DOMContentLoaded", function() {
    // 1. Ensure the encryption radio button is selected by default
    const encryptRadio = document.querySelector('input[name="operation"][value="encrypt"]');
    if (encryptRadio) {
        encryptRadio.checked = true;
    }

    // 2. Toggle between encryption and decryption sections
    function toggleOperation() {
        const operation = document.querySelector('input[name="operation"]:checked').value;
        const encryptSection = document.getElementById("encryptSection");
        const decryptSection = document.getElementById("decryptSection");
        if (operation === "encrypt") {
            encryptSection.classList.remove("hidden");
            decryptSection.classList.add("hidden");
        } else {
            decryptSection.classList.remove("hidden");
            encryptSection.classList.add("hidden");
        }
    }
    const opRadios = document.querySelectorAll('input[name="operation"]');
    opRadios.forEach(radio => radio.addEventListener("change", toggleOperation));
    toggleOperation();

    // 3. Generic dropdown toggling using Font Awesome icons and smooth transition
    function setupDropdown(dropdownSelector, headerSelector, contentSelector) {
        const dropdowns = document.querySelectorAll(dropdownSelector);
        dropdowns.forEach(function(dropdown) {
            const header = dropdown.querySelector(headerSelector);
            const content = dropdown.querySelector(contentSelector);
            header.addEventListener("click", function() {
                content.classList.toggle("open");
                const icon = header.querySelector(".dropdown-icon");
                if (icon) {
                    icon.innerHTML = content.classList.contains("open") ?
                        '<i class="fa fa-chevron-up"></i>' :
                        '<i class="fa fa-chevron-down"></i>';
                }
            });
        });
    }

    // Setup for top-level dropdowns (Word Info, Round Info)
    setupDropdown(".dropdown", ".dropdown-header", ".dropdown-content");
    // Setup for nested dropdowns (each round)
    setupDropdown(".nested-dropdown", ".nested-dropdown-header", ".nested-dropdown-content");
});