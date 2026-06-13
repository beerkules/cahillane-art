/* CAHILLANE — shared header/footer injection, mobile menu, form handling.
   Pages include <div id="site-header"></div> and <div id="site-footer"></div>,
   then <script src="/assets/include.js" defer></script>. */

(function () {
  var YEAR = new Date().getFullYear();
  var INSTAGRAM = "https://instagram.com/"; // TODO: set real handle
  var EMAIL = "info@cahillane.de";

  var NAV = [
    { href: "/works.html",    label: "Works" },
    { href: "/about.html",    label: "About" },
    { href: "/view.html",     label: "The Private View" },
    { href: "/contact.html",  label: "Contact" }
  ];

  function path() { return location.pathname.replace(/index\.html$/, "/"); }

  function buildHeader() {
    var here = path();
    var links = NAV.map(function (n) {
      var active = here.indexOf(n.href) === 0 ? " class=\"active\"" : "";
      return '<a href="' + n.href + '"' + active + '>' + n.label + '</a>';
    }).join("");
    return '' +
      '<header class="site-header"><div class="nav-inner">' +
        '<button class="nav-toggle" aria-label="Open menu">&#9776;</button>' +
        '<a class="nav-word" href="/home.html">BENJAMIN CAHILLANE</a>' +
        '<nav class="nav-links">' +
          '<button class="nav-close" aria-label="Close menu">&times;</button>' +
          links +
        '</nav>' +
      '</div></header>';
  }

  function buildFooter() {
    return '' +
      '<footer class="site-footer">' +
        '<div class="foot-word">BENJAMIN CAHILLANE</div>' +
        '<div class="foot-links">' +
          '<a href="/view.html">The Private View</a>' +
          '<a href="' + INSTAGRAM + '" target="_blank" rel="noopener">Instagram</a>' +
          '<a href="mailto:' + EMAIL + '">Contact</a>' +
          '<a href="/privacy.html">Privacy</a>' +
          '<a href="/legal.html">Legal</a>' +
        '</div>' +
        '<div class="foot-fine">&copy; ' + YEAR + ' Benjamin Cahillane &middot; Contemporary Artist</div>' +
      '</footer>';
  }

  function wireMenu() {
    var toggle = document.querySelector(".nav-toggle");
    var close = document.querySelector(".nav-close");
    if (toggle) toggle.addEventListener("click", function () { document.body.classList.add("menu-open"); });
    if (close) close.addEventListener("click", function () { document.body.classList.remove("menu-open"); });
    document.querySelectorAll(".nav-links a").forEach(function (a) {
      a.addEventListener("click", function () { document.body.classList.remove("menu-open"); });
    });
  }

  function wireForms() {
    document.querySelectorAll("form.ajax-form").forEach(function (form) {
      var success = form.parentElement.querySelector(".form-success");
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var btn = form.querySelector("button[type=submit], .btn");
        var label = btn ? btn.textContent : "";
        if (btn) { btn.disabled = true; btn.textContent = "· · ·"; }
        fetch(form.action, { method: "POST", body: new FormData(form) })
          .then(function (res) {
            if (!res.ok) throw new Error();
            form.style.display = "none";
            if (success) success.style.display = "block";
          })
          .catch(function () {
            if (btn) { btn.disabled = false; btn.textContent = label; }
            alert("Something went wrong — please try again or email " + EMAIL);
          });
      });
    });
  }

  function init() {
    var h = document.getElementById("site-header");
    var f = document.getElementById("site-footer");
    if (h) h.outerHTML = buildHeader();
    if (f) f.outerHTML = buildFooter();
    wireMenu();
    wireForms();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
