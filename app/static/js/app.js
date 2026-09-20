document.addEventListener("DOMContentLoaded", function () {
    // منو
    const menuToggle = document.getElementById("menuToggle");
    const sidebar = document.getElementById("sidebar");
    const overlay = document.getElementById("overlay");

    if (menuToggle) {
        menuToggle.addEventListener("click", function () {
            sidebar.classList.toggle("open");
            overlay.classList.toggle("show");
        });
        overlay.addEventListener("click", function () {
            sidebar.classList.remove("open");
            overlay.classList.remove("show");
        });
    }

    // ولیدیشن فرم محاسبه
    const calcForm = document.getElementById("calcForm");
    if (calcForm) {
        calcForm.addEventListener("submit", function (e) {
            let valid = true;
            calcForm.querySelectorAll("input[type=number]").forEach(function (input) {
                const errEl = document.querySelector('.error-msg[data-for="' + input.id + '"]');
                const val = input.value.trim();
                input.classList.remove("invalid");
                if (errEl) errEl.textContent = "";
                if (val === "") {
                    input.classList.add("invalid");
                    if (errEl) errEl.textContent = "لطفاً این قسمت را وارد کنید.";
                    valid = false;
                } else if (isNaN(val) || parseFloat(val) <= 0) {
                    input.classList.add("invalid");
                    if (errEl) errEl.textContent = "مقدار واردشده معتبر نیست.";
                    valid = false;
                }
            });
            if (!valid) e.preventDefault();
        });
    }

    // مودال مشتری جدید
    const modal = document.getElementById("clientModal");
    const newClientBtn = document.getElementById("newClientBtn");
    const cancelClientBtn = document.getElementById("cancelClientBtn");
    const newClientForm = document.getElementById("newClientForm");
    const clientSelect = document.getElementById("client_id");

    if (newClientBtn && modal) {
        newClientBtn.addEventListener("click", function () {
            modal.classList.add("show");
        });
    }
    if (cancelClientBtn && modal) {
        cancelClientBtn.addEventListener("click", function () {
            modal.classList.remove("show");
        });
    }

    if (newClientForm) {
        newClientForm.addEventListener("submit", async function (e) {
            e.preventDefault();
            const name = document.getElementById("new_client_name").value.trim();
            const phone = document.getElementById("new_client_phone").value.trim();
            const notes = document.getElementById("new_client_notes").value.trim();

            if (!name) {
                alert("نام مشتری الزامی است.");
                return;
            }

            const csrfInput = document.querySelector('input[name="csrf_token"]');
            const csrf = csrfInput ? csrfInput.value : "";

            const fd = new FormData();
            fd.append("name", name);
            fd.append("phone", phone);
            fd.append("notes", notes);
            fd.append("csrf_token", csrf);

            try {
                const res = await fetch("/clients/create", {
                    method: "POST",
                    headers: { "X-Requested-With": "XMLHttpRequest" },
                    body: fd,
                });
                if (!res.ok) throw new Error("خطا در ساخت مشتری");
                const data = await res.json();
                const opt = document.createElement("option");
                opt.value = data.client.id;
                opt.textContent = data.client.name;
                opt.selected = true;
                clientSelect.appendChild(opt);
                modal.classList.remove("show");
                newClientForm.reset();
            } catch (err) {
                alert("خطایی رخ داد. لطفاً دوباره تلاش کنید.");
            }
        });
    }

    // بارگذاری اندازه‌های مشتری
    const loadBtn = document.getElementById("loadMeasurementsBtn");
    if (loadBtn && clientSelect &&calcForm) {
        loadBtn.addEventListener("click", async function () {
            const cid = clientSelect.value;
            if (!cid) {
                alert("ابتدا یک مشتری انتخاب کنید.");
                return;
            }
            const url = calcForm.dataset.measurementsUrl.replace("/0", "/" + cid);
            try {
                const res = await fetch(url);
                const data = await res.json();
                Object.keys(data).forEach(function (k) {
                    const input = document.getElementById(k);
                    if (input) input.value = data[k];
                });
            } catch (err) {
                alert("خطا در دریافت اندازه‌ها.");
            }
        });
    }
});
