// Theme toggle and mobile navigation script
(function () {
  const STORAGE_KEY = 'cloudymind-theme';

  function getPreferredTheme() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) return saved;
    // Default to system
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    if (theme === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      document.documentElement.setAttribute('data-theme', 'light');
    }
    updateToggleButtons(theme);
  }

  function updateToggleButtons(theme) {
    const btns = document.querySelectorAll('.theme-toggle-btn');
    btns.forEach((btn) => {
      btn.setAttribute('aria-label', `Toggle theme (current: ${theme})`);
      btn.innerHTML = theme === 'dark' ? '☀️' : '🌙';
      btn.title = theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
    });
  }

  // Initialize early
  const initialTheme = getPreferredTheme();
  applyTheme(initialTheme);

  document.addEventListener('DOMContentLoaded', () => {
    // Sync buttons
    updateToggleButtons(getPreferredTheme());

    // Toggle click listeners
    const btns = document.querySelectorAll('.theme-toggle-btn');
    btns.forEach((btn) => {
      btn.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        const next = current === 'dark' ? 'light' : 'dark';
        localStorage.setItem(STORAGE_KEY, next);
        applyTheme(next);
      });
    });

    // Mobile menu toggle
    const mobileBtn = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    if (mobileBtn && navLinks) {
      mobileBtn.addEventListener('click', () => {
        navLinks.classList.toggle('open');
        const expanded = navLinks.classList.contains('open');
        mobileBtn.setAttribute('aria-expanded', expanded);
      });
    }

    // System theme change listener (only if user hasn't manually set a preference)
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      if (!localStorage.getItem(STORAGE_KEY)) {
        applyTheme(e.matches ? 'dark' : 'light');
      }
    });

    // Inject Floating Rainbow Cat
    initFloatingRainbowCat();
  });

  function initFloatingRainbowCat() {
    if (document.querySelector('.sky-container')) return;

    const sky = document.createElement('div');
    sky.className = 'sky-container';
    sky.setAttribute('aria-hidden', 'true');

    sky.innerHTML = `
      <div class="floating-cat-track" title="Rainbow Cat!">
        <div class="rainbow-trail">
          <div class="rainbow-ribbon ribbon-red"></div>
          <div class="rainbow-ribbon ribbon-orange"></div>
          <div class="rainbow-ribbon ribbon-yellow"></div>
          <div class="rainbow-ribbon ribbon-green"></div>
          <div class="rainbow-ribbon ribbon-blue"></div>
          <div class="rainbow-ribbon ribbon-purple"></div>
        </div>
        <div class="cat-character">
          <div class="cat-tail"></div>
          <div class="cat-body">
            <div class="cat-sprinkles">
              <span class="sprinkle s1"></span>
              <span class="sprinkle s2"></span>
              <span class="sprinkle s3"></span>
              <span class="sprinkle s4"></span>
            </div>
          </div>
          <div class="cat-head">
            <div class="cat-ear ear-left"></div>
            <div class="cat-ear ear-right"></div>
            <div class="cat-face">
              <span class="cat-eye eye-left"></span>
              <span class="cat-eye eye-right"></span>
              <span class="cat-nose"></span>
              <span class="cat-cheeks"></span>
            </div>
          </div>
          <div class="cat-paws">
            <span class="cat-paw paw-1"></span>
            <span class="cat-paw paw-2"></span>
            <span class="cat-paw paw-3"></span>
            <span class="cat-paw paw-4"></span>
          </div>
          <div class="sparkles-container">
            <span class="sparkle sp1">✨</span>
            <span class="sparkle sp2">⭐</span>
            <span class="sparkle sp3">✨</span>
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(sky);
  }
})();
