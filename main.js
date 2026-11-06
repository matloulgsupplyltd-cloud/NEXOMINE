/* Corporate site behaviour: navigation, reveal, photo slots, filters, forms. No dependencies. */
(function () {
  "use strict";
  document.documentElement.classList.add("js");

  /* ---- Sticky nav shadow ---- */
  var nav = document.querySelector(".nav");
  var toTop = document.querySelector(".to-top");
  function onScroll() {
    var y = window.scrollY;
    if (nav) nav.classList.toggle("scrolled", y > 8);
    if (toTop) toTop.classList.toggle("show", y > 700);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0 }); });

  /* ---- Mobile menu ---- */
  var burger = document.querySelector(".burger");
  var menu = document.getElementById("menu");
  function closeMenu() {
    if (!burger) return;
    burger.setAttribute("aria-expanded", "false");
    menu.classList.remove("open");
    document.body.style.overflow = "";
  }
  if (burger && menu) {
    burger.addEventListener("click", function () {
      var open = burger.getAttribute("aria-expanded") !== "true";
      burger.setAttribute("aria-expanded", String(open));
      menu.classList.toggle("open", open);
      document.body.style.overflow = open ? "hidden" : "";
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1240) closeMenu(); });
  }

  /* ---- Dropdowns (hover on desktop via CSS; click/keyboard everywhere) ---- */
  var subs = document.querySelectorAll(".has-sub");
  subs.forEach(function (li) {
    var btn = li.querySelector(":scope > button");
    btn.addEventListener("click", function () {
      var open = li.getAttribute("data-open") === "true";
      subs.forEach(function (o) { o.setAttribute("data-open", "false"); o.querySelector(":scope > button").setAttribute("aria-expanded", "false"); });
      li.setAttribute("data-open", String(!open));
      btn.setAttribute("aria-expanded", String(!open));
    });
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".has-sub")) subs.forEach(function (o) { o.setAttribute("data-open", "false"); o.querySelector(":scope > button").setAttribute("aria-expanded", "false"); });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { subs.forEach(function (o) { o.setAttribute("data-open", "false"); }); closeMenu(); }
  });
  if (menu) menu.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", closeMenu); });

  /* ---- Fall back to the bundled image if a photo file is missing ---- */
  document.querySelectorAll("img[data-fallback]").forEach(function (img) {
    function fb() { if (img.getAttribute("src") !== img.getAttribute("data-fallback")) img.src = img.getAttribute("data-fallback"); }
    img.addEventListener("error", fb);
    if (img.complete && img.naturalWidth === 0) fb();
  });

  /* ---- Photo slots: swap placeholder for a real image when the file exists ---- */
  document.querySelectorAll(".photo[data-src]").forEach(function (box) {
    var img = new Image();
    img.alt = box.getAttribute("data-alt") || "";
    img.decoding = "async";
    if (!box.hasAttribute("data-eager")) img.loading = "lazy";
    img.onload = function () { box.appendChild(img); box.classList.add("has-img"); };
    img.src = box.getAttribute("data-src");
  });

  /* ---- Reveal on scroll ---- */
  var items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    items.forEach(function (el) { io.observe(el); });
  } else { items.forEach(function (el) { el.classList.add("in"); }); }

  /* ---- Count-up numbers (only when a numeric value is supplied) ---- */
  document.querySelectorAll("[data-count]").forEach(function (el) {
    var target = parseFloat(el.getAttribute("data-count"));
    if (isNaN(target)) return;
    var done = false; el.textContent = target.toLocaleString("en-US");
    new IntersectionObserver(function (en, obs) {
      if (done || !en[0].isIntersecting) return; done = true; obs.disconnect();
      var t0 = performance.now(), dur = 1400;
      (function tick(t) {
        var p = Math.min((t - t0) / dur, 1); el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))).toLocaleString("en-US");
        if (p < 1) requestAnimationFrame(tick);
      })(t0);
    }).observe(el);
  });

  /* ---- Filter chips (news) ---- */
  var chips = document.querySelectorAll(".chip[data-filter]");
  if (chips.length) {
    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        chips.forEach(function (o) { o.setAttribute("aria-pressed", "false"); });
        c.setAttribute("aria-pressed", "true");
        var f = c.getAttribute("data-filter");
        document.querySelectorAll("[data-cat]").forEach(function (card) {
          card.hidden = !(f === "all" || card.getAttribute("data-cat") === f);
        });
      });
    });
  }

  /* ---- Sub-navigation highlight ---- */
  var sublinks = document.querySelectorAll(".subnav a[href^='#']");
  if (sublinks.length && "IntersectionObserver" in window) {
    var map = {};
    sublinks.forEach(function (a) { var s = document.querySelector(a.getAttribute("href")); if (s) map[s.id] = a; });
    var so = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { sublinks.forEach(function (a) { a.classList.remove("active"); }); map[en.target.id].classList.add("active"); }
      });
    }, { rootMargin: "-40% 0px -55% 0px" });
    Object.keys(map).forEach(function (id) { so.observe(document.getElementById(id)); });
  }

  /* ---- Forms with validation ---- */
  var form = document.getElementById("contact-form");
  if (form) {
    var status = document.getElementById("form-status");
    var rules = {
      name: function (v) { return v.trim().length >= 2 ? "" : "Enter your full name."; },
      email: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) ? "" : "Enter a valid email address, for example name@example.com."; },
      subject: function (v) { return v ? "" : "Choose the subject of your enquiry."; },
      message: function (v) { return v.trim().length >= 10 ? "" : "Write at least 10 characters so we can understand your enquiry."; },
      consent: function (v, el) { return el.checked ? "" : "Confirm that you agree to us contacting you about this enquiry."; }
    };
    function check(el) {
      var rule = rules[el.name]; if (!rule) return true;
      var msg = rule(el.value, el), field = el.closest(".field");
      field.classList.toggle("invalid", !!msg);
      field.querySelector(".err").textContent = msg;
      el.setAttribute("aria-invalid", msg ? "true" : "false");
      return !msg;
    }
    form.querySelectorAll("input, select, textarea").forEach(function (el) {
      el.addEventListener("blur", function () { if (rules[el.name]) check(el); });
      el.addEventListener("input", function () { if (el.closest(".field") && el.closest(".field").classList.contains("invalid")) check(el); });
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      status.className = "form-status"; status.textContent = "";
      if (form.querySelector(".hp input").value) return; /* honeypot */
      var ok = true, first = null;
      form.querySelectorAll("input, select, textarea").forEach(function (el) {
        if (rules[el.name] && !check(el)) { ok = false; if (!first) first = el; }
      });
      if (!ok) { first.focus(); status.className = "form-status bad"; status.textContent = "Fix the highlighted fields and send again."; return; }
      var action = form.getAttribute("data-endpoint");
      var data = new FormData(form);
      if (!action) {
        /* No endpoint configured yet: confirm locally so the flow can be reviewed. */
        status.className = "form-status ok"; status.textContent = "Thank you. Your enquiry was received. (Preview mode: set data-endpoint on the form to deliver messages.)";
        form.reset(); return;
      }
      var btn = form.querySelector("button[type=submit]"); btn.disabled = true;
      fetch(action, { method: "POST", body: data, headers: { Accept: "application/json" } })
        .then(function (r) { if (!r.ok) throw new Error(); status.className = "form-status ok"; status.textContent = "Thank you. Your enquiry was sent and we will reply within two business days."; form.reset(); })
        .catch(function () { status.className = "form-status bad"; status.textContent = "Your message was not sent. Try again, or email us directly."; })
        .finally(function () { btn.disabled = false; });
    });
  }
})();
