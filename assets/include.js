/* CAHILLANE — shared header/footer injection, mobile menu, form handling.
   Pages include <div id="site-header"></div> and <div id="site-footer"></div>,
   then <script src="/assets/include.js" defer></script>. */

(function () {
  var YEAR = new Date().getFullYear();
  var INSTAGRAM = "https://instagram.com/benjamincahillane";
  var EMAIL = "hello@benjamincahillane.com";

  var NAV = [
    { href: "/works.html",    label: "Works" },
    { href: "/about.html",    label: "About" },
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
        '<button class="nav-toggle" aria-label="Open menu"><span></span></button>' +
        '<a class="nav-word" href="/" aria-label="Benjamin Cahillane"><img src="/assets/logo.png?v=1" alt="Benjamin Cahillane" style="height:46px;width:auto;display:block;transform:translateY(-9px)"></a>' +
        '<nav class="nav-links">' +
          '<button class="nav-close" aria-label="Close menu">&times;</button>' +
          links +
        '</nav>' +
      '</div></header>';
  }

  function buildFooter() {
    return '' +
      '<footer class="site-footer">' +
        '<div class="foot-fine">&copy; ' + YEAR + ' Benjamin Cahillane</div>' +
        '<div class="foot-word"><img src="/assets/logo.png?v=1" alt="Benjamin Cahillane" style="height:30px;width:auto;display:block">' +
          '<a href="' + INSTAGRAM + '" target="_blank" rel="noopener" aria-label="Instagram" style="display:inline-flex;align-items:center;margin-left:16px;transform:translateY(6px)"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg></a>' +
        '</div>' +
        '<div class="foot-links">' +
          '<a href="/privacy.html">Privacy</a>' +
          '<a href="/legal.html">Legal</a>' +
        '</div>' +
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

  function wireScrollCue() {
    var cue = document.querySelector(".scroll-cue");
    if (!cue) return;
    var onScroll = function () {
      if (window.scrollY > 40) cue.classList.add("is-hidden");
      else cue.classList.remove("is-hidden");
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  function wireHeroFade() {
    var bg = document.querySelector(".hero-bg");
    if (!bg) return;
    var m = (bg.style.backgroundImage || "").match(/url\(['"]?(.*?)['"]?\)/);
    if (!m) return;
    bg.style.transition = "opacity .9s ease";
    bg.style.opacity = "0";
    var reveal = function () { requestAnimationFrame(function () { bg.style.opacity = "1"; }); };
    var img = new Image();
    img.onload = reveal;
    img.onerror = reveal;
    img.src = m[1];
    if (img.complete) reveal();
  }

  function wireHeaderScroll() {
    var hdr = document.querySelector(".site-header");
    if (!hdr) return;
    var onScroll = function () {
      if (window.scrollY > 30) hdr.classList.add("scrolled");
      else hdr.classList.remove("scrolled");
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  function wireAnchorScroll() {
    var TARGET = "private-view";
    function isTarget(hash) { return hash === "#" + TARGET; }
    function center(smooth) {
      var el = document.getElementById(TARGET);
      if (el) el.scrollIntoView({ block: "center", behavior: smooth ? "smooth" : "auto" });
    }
    // Same-page clicks to the section: smooth-center instead of native jump.
    document.addEventListener("click", function (e) {
      var a = e.target.closest("a[href]");
      if (!a) return;
      var url;
      try { url = new URL(a.getAttribute("href"), location.href); } catch (_) { return; }
      if (!isTarget(url.hash)) return;
      var samePage = url.pathname.replace(/index\.html$/, "") === location.pathname.replace(/index\.html$/, "");
      if (!samePage) return; // cross-page link: let it navigate, load handler centers it
      e.preventDefault();
      if (location.hash !== url.hash) history.pushState(null, "", url.hash);
      center(true);
    });
    window.addEventListener("hashchange", function () { if (isTarget(location.hash)) center(true); });
    // Direct load of /#private-view: re-center after layout/images settle.
    if (isTarget(location.hash)) {
      center(false);
      window.addEventListener("load", function () { setTimeout(function () { center(false); }, 60); });
      setTimeout(function () { center(false); }, 350);
    }
  }

  function init() {
    var h = document.getElementById("site-header");
    var f = document.getElementById("site-footer");
    if (h) h.outerHTML = buildHeader();
    if (f) f.outerHTML = buildFooter();
    wireMenu();
    wireForms();
    wireScrollCue();
    wireHeaderScroll();
    wireHeroFade();
    wireAnchorScroll();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
