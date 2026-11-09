// Site footer, shared by the landing, account and legal pages.
(() => {
  const el = document.getElementById("siteFooter");
  if (!el) return;
  const year = new Date().getFullYear();
  el.className = "site-foot";
  el.innerHTML = `
  <div class="wrap">
    <div class="sf-top">
      <div class="sf-brand">
        <a class="logo" href="/" aria-label="Ruko home"><svg viewBox="0 0 100 100" aria-hidden="true"><path d="M30 2h40l28 28v40L70 98H30L2 70V30z" fill="#c8102e"/><path d="M31.7 9h36.6L91 31.7v36.6L68.3 91H31.7L9 68.3V31.7z" fill="none" stroke="#fff" stroke-width="5"/></svg>Ruko</a>
        <p>Scam-call guard for Indian families. Lost money to a call? Call <a href="tel:1930"><b>1930</b></a> now, or report at <a href="https://cybercrime.gov.in" target="_blank" rel="noopener">cybercrime.gov.in</a>.</p>
      </div>
      <nav class="sf-cols" aria-label="Footer">
        <div><h2>Product</h2><a href="/app/">Open Ruko</a><a href="/account/">Family account</a><a href="/#how">How it works</a><a href="/#proof">Test results</a></div>
        <div><h2>For partners</h2><a href="/#business">Banks and telcos</a><a href="/#business">Scoring API</a><a href="/contact/">Pilot enquiries</a></div>
        <div><h2>Legal</h2><a href="/privacy/">Privacy policy</a><a href="/terms/">Terms of use</a><a href="/licenses/">Licences</a><a href="/contact/">Contact and grievances</a></div>
      </nav>
    </div>
    <div class="sf-bottom">
      <p>© ${year} Ruko. All rights reserved. Built in India.</p>
      <p>Speech by Gnani AI Prisma · Voices by Gnani AI Timbre. Ruko only warns; it never blocks calls and keeps no call audio.</p>
    </div>
  </div>`;
})();
