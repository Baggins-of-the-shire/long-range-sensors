/* LONG RANGE SENSORS - progressive enhancement only.
   The page is fully usable with this file blocked: filtering is CSS, and the
   viewer is a :target overlay. Everything here is a convenience on top. */
(function () {
  'use strict';

  /* --- Stardate ---------------------------------------------------------
     Not canon, and canon does not agree with itself anyway. This advances at
     the TNG rate of about 1000 per year and is anchored so that it reads in
     the 47000s, which is where the writers put everything they cared about.
     A static value is baked into the markup, so this only refines it. */
  var el = document.getElementById('stardate');
  if (el) {
    var epoch = Date.UTC(2026, 0, 1);
    var days = (Date.now() - epoch) / 86400000;
    el.textContent = 'STARDATE ' + (47000 + days * 2.7379).toFixed(1);
  }

  /* --- Viewer keyboard control ------------------------------------------
     The overlay is driven by :target, so navigation is just a location
     change. Reading the links out of the open overlay keeps this in step
     with whatever build.py generated. */
  function openViewer() {
    var id = location.hash.slice(1);
    if (!id) return null;
    var node = document.getElementById(id);
    return node && node.classList.contains('viewer') ? node : null;
  }

  document.addEventListener('keydown', function (e) {
    var v = openViewer();
    if (!v) return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;

    var sel = null;
    if (e.key === 'ArrowRight') sel = '.vbtn.next';
    else if (e.key === 'ArrowLeft') sel = '.vbtn.prev';
    else if (e.key === 'Escape') sel = '.vbtn.close';
    if (!sel) return;

    var link = v.querySelector(sel);
    if (link) { e.preventDefault(); link.click(); }
  });

  /* --- Neighbour preload -------------------------------------------------
     Opening the viewer warms the two frames either side so arrowing through
     does not flash. Cheap: seven images, none over 260 KB. */
  var warmed = Object.create(null);
  function warm(v) {
    if (!v) return;
    ['.vbtn.prev', '.vbtn.next'].forEach(function (s) {
      var link = v.querySelector(s);
      if (!link) return;
      var target = document.getElementById(link.getAttribute('href').slice(1));
      var img = target && target.querySelector('img');
      if (!img || warmed[img.src]) return;
      warmed[img.src] = true;
      var pre = new Image();
      pre.src = img.src;
    });
  }
  /* --- Scroll lock -------------------------------------------------------
     Purely cosmetic: keeps the page behind an open overlay from scrolling
     under the reader's fingers. The overlay is opaque either way. */
  function sync() {
    var v = openViewer();
    document.body.classList.toggle('viewing', !!v);
    warm(v);
  }
  window.addEventListener('hashchange', sync);
  sync();
})();
