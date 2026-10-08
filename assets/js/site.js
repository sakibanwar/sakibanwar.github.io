(function () {
  // Mobile menu
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
    });
  }

  // Email links are assembled here so the address isn't sitting in the HTML for spam bots
  document.querySelectorAll('.js-email').forEach(function (a) {
    a.href = 'mailto:' + a.dataset.u + '@' + a.dataset.d;
  });

  // Show / hide paper abstracts
  document.querySelectorAll('[data-abstract]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var box = document.getElementById(btn.getAttribute('aria-controls'));
      var open = btn.getAttribute('aria-expanded') !== 'true';
      btn.setAttribute('aria-expanded', open);
      box.classList.toggle('is-open', open);
    });
  });
})();
