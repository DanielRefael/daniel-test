/*
 * ============================================================
 *  SITE_CONFIG – PLACEHOLDERS למילוי ע"י בעל העסק
 *  עדכנו כאן את הפרטים והם יופיעו בכל מקום בדף.
 * ============================================================
 */
const SITE_CONFIG = {
  // מספר הטלפון כפי שיוצג בדף
  phoneDisplay: "054-9415001",
  // מספר הטלפון בפורמט בינלאומי ללא אפסים מובילים
  phoneIntl: "+972549415001",
  // מספר וואטסאפ בספרות בלבד, בפורמט בינלאומי ללא "+"
  whatsappNumber: "972549415001",
  // הודעת פתיחה שתופיע אוטומטית בוואטסאפ
  whatsappMessage: "שלום דניאל, אשמח לקבל הצעת מחיר לצביעה",
  // השאירו ריק כדי להסתיר את שורת האימייל, לדוגמה: "daniel@example.com"
  email: "",
  serviceArea: "חולון והסביבה",
};

(function () {
  const waUrl =
    "https://wa.me/" +
    SITE_CONFIG.whatsappNumber +
    "?text=" +
    encodeURIComponent(SITE_CONFIG.whatsappMessage);

  document.querySelectorAll("[data-phone-href]").forEach((el) => (el.href = "tel:" + SITE_CONFIG.phoneIntl));
  document.querySelectorAll("[data-phone-display]").forEach((el) => (el.textContent = SITE_CONFIG.phoneDisplay));
  document.querySelectorAll("[data-whatsapp-href]").forEach((el) => (el.href = waUrl));
  document.querySelectorAll("[data-email-href]").forEach((el) => (el.href = "mailto:" + SITE_CONFIG.email));
  document.querySelectorAll("[data-email-display]").forEach((el) => (el.textContent = SITE_CONFIG.email));
  document.querySelectorAll("[data-email-row]").forEach((el) => (el.hidden = !SITE_CONFIG.email));
  document.querySelectorAll("[data-area]").forEach((el) => (el.textContent = SITE_CONFIG.serviceArea));

  document.getElementById("year").textContent = new Date().getFullYear();

  const header = document.querySelector(".site-header");
  const onScroll = () => header.classList.toggle("scrolled", window.scrollY > 10);
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  const toggle = document.querySelector(".nav-toggle");
  const nav = document.getElementById("main-nav");
  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(open));
    document.body.classList.toggle("nav-open", open);
  });
  nav.querySelectorAll("a").forEach((a) =>
    a.addEventListener("click", () => {
      nav.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
      document.body.classList.remove("nav-open");
    })
  );

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) =>
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("in");
            io.unobserve(e.target);
          }
        }),
      { threshold: 0.12 }
    );
    document
      .querySelectorAll(".service-card, .why-list li, .g-item, .t-card, .steps li, .section-head")
      .forEach((el) => {
        el.classList.add("reveal");
        io.observe(el);
      });
  }

  // The form has no backend: it validates locally and hands the lead off to WhatsApp.
  const form = document.getElementById("contact-form");
  const status = document.getElementById("form-status");
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const name = form.name.value.trim();
    const phone = form.phone.value.trim();
    form.name.classList.toggle("invalid", !name);
    form.phone.classList.toggle("invalid", !/^[\d\s+\-()]{9,}$/.test(phone));
    if (!name || !/^[\d\s+\-()]{9,}$/.test(phone)) {
      status.textContent = "נא למלא שם ומספר טלפון תקין.";
      status.className = "form-note error";
      return;
    }
    const text =
      `שלום דניאל, שמי ${name}.\nטלפון: ${phone}\nסוג עבודה: ${form.service.value}` +
      (form.message.value.trim() ? `\nפרטים: ${form.message.value.trim()}` : "");
    status.textContent = "תודה! הפרטים נקלטו – נחזור אליך בהקדם.";
    status.className = "form-note success";
    window.open("https://wa.me/" + SITE_CONFIG.whatsappNumber + "?text=" + encodeURIComponent(text), "_blank", "noopener");
    form.reset();
  });
})();
