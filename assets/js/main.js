/* ===================================================================
   Villa Mukinja — interactions
   Lightweight, no dependencies. Tracking-ready (Option B upgrade):
   a global dataLayer is pushed to on key actions so GTM/GA4 can be
   layered on later WITHOUT editing templates (per playbook §8).
   =================================================================== */
(function () {
  "use strict";

  /* ---- tracking-ready event helper (no analytics installed yet) ---- */
  window.dataLayer = window.dataLayer || [];
  function track(event, params) {
    window.dataLayer.push(Object.assign({ event: event }, params || {}));
    // When GA4/GTM is added in Option B, these pushes are picked up automatically.
  }
  // Map clicks on known CTA classes -> events (matches playbook event map)
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a, button");
    if (!a) return;
    var href = a.getAttribute("href") || "";
    if (href.indexOf("tel:") === 0) track("phone_click", { value: href });
    else if (href.indexOf("mailto:") === 0) track("email_click", { value: href });
    else if (href.indexOf("wa.me") > -1 || a.classList.contains("whatsapp-link")) track("whatsapp_click", { value: href });
    else if (a.classList.contains("cta-primary")) track("cta_click", { cta: "primary", label: a.textContent.trim() });
    else if (a.classList.contains("cta-secondary")) track("cta_click", { cta: "secondary", label: a.textContent.trim() });
    else if (a.dataset.book !== undefined) track("book_intent", { label: a.textContent.trim() });
  });

  /* ---- header scroll state ---- */
  var header = document.querySelector(".header");
  function onScroll() {
    if (window.scrollY > 40) header.classList.add("scrolled");
    else header.classList.remove("scrolled");
  }
  if (header) { onScroll(); window.addEventListener("scroll", onScroll, { passive: true }); }

  /* ---- mobile menu ---- */
  var burger = document.querySelector(".burger");
  if (burger) {
    burger.addEventListener("click", function () {
      var open = document.body.classList.toggle("menu-open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.querySelectorAll(".nav a").forEach(function (link) {
      link.addEventListener("click", function () { document.body.classList.remove("menu-open"); });
    });
  }

  /* ---- scroll reveal ---- */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---- count-up stats ---- */
  var stats = document.querySelectorAll("[data-count]");
  if ("IntersectionObserver" in window && stats.length) {
    var so = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, target = parseInt(el.dataset.count, 10), suffix = el.dataset.suffix || "", t0 = null;
        function step(ts) {
          if (!t0) t0 = ts;
          var p = Math.min((ts - t0) / 1400, 1);
          el.textContent = Math.floor(p * target) + suffix;
          if (p < 1) requestAnimationFrame(step); else el.textContent = target + suffix;
        }
        requestAnimationFrame(step); so.unobserve(el);
      });
    }, { threshold: 0.6 });
    stats.forEach(function (el) { so.observe(el); });
  }

  /* ---- enquiry/contact forms -> inbox via FormSubmit ----
     The address is assembled at runtime so it never appears in the
     HTML source (basic protection against spam harvesters). */
  var FS_ENDPOINT = "https://formsubmit.co/ajax/" + ["villa", "mukinja"].join(".") + "@" + ["gmail", "com"].join(".");
  document.querySelectorAll("form[data-form-type]").forEach(function (form) {
    if (form.dataset.formType === "availability") return; // quickbook bar navigates to booking.html
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      track("form_submit", { form_type: form.dataset.formType });
      var btn = form.querySelector('button[type="submit"]');
      if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = "Sending…"; }
      var data = { _subject: "Website enquiry — Villa Mukinja (" + form.dataset.formType + ")", _template: "table", _captcha: "false" };
      form.querySelectorAll("input[name], select[name], textarea[name]").forEach(function (el) { data[el.name] = el.value; });
      fetch(FS_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(data)
      }).then(function (r) {
        if (!r.ok) throw new Error("send failed");
        var success = form.querySelector(".form-success");
        var fields = form.querySelector(".form-fields");
        if (success && fields) { fields.style.display = "none"; success.classList.add("show"); }
        else form.reset();
      }).catch(function () {
        if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label; }
        alert("Sorry, the message could not be sent right now. Please call or WhatsApp us at +385 99 7877 479.");
      });
    });
    // form_start (first focus) — diagnostic event
    var started = false;
    form.addEventListener("focusin", function () {
      if (started) return; started = true;
      track("form_start", { form_type: form.dataset.formType });
    });
  });

  /* ---- prefill year on footer ---- */
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();

  /* ---- simple lightbox for galleries ---- */
  var galleryLinks = document.querySelectorAll("[data-lightbox]");
  if (galleryLinks.length) {
    var box = document.createElement("div");
    box.style.cssText = "position:fixed;inset:0;z-index:200;background:rgba(15,30,26,.92);display:none;align-items:center;justify-content:center;cursor:zoom-out;padding:24px";
    box.innerHTML = '<img style="max-width:92vw;max-height:88vh;border-radius:10px;box-shadow:0 30px 80px rgba(0,0,0,.5)">';
    document.body.appendChild(box);
    var boxImg = box.querySelector("img");
    galleryLinks.forEach(function (link) {
      link.addEventListener("click", function (e) {
        e.preventDefault();
        boxImg.src = link.getAttribute("href") || link.dataset.lightbox;
        box.style.display = "flex";
      });
    });
    box.addEventListener("click", function () { box.style.display = "none"; boxImg.src = ""; });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") { box.style.display = "none"; boxImg.src = ""; } });
  }

  /* ---- set min date on date inputs to today ---- */
  var today = new Date().toISOString().split("T")[0];
  document.querySelectorAll('input[type="date"]').forEach(function (inp) { if (!inp.min) inp.min = today; });
})();
