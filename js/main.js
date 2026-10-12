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

    // Inject Floating Cloud with Kebab Sauce Ooze
    initFloatingKebabCloud();
  });

  function initFloatingKebabCloud() {
    if (document.querySelector('.sky-container')) return;

    const sky = document.createElement('div');
    sky.className = 'sky-container';
    sky.setAttribute('aria-hidden', 'true');

    sky.innerHTML = `
      <div class="floating-cloud-track" title="Hover over the cloud for kebab sauce!">
        <div class="cloud-body">
          <span class="cloud-label">KEBAB</span>
        </div>
        <div class="sauce-ooze-container">
          <div class="sauce-stream sauce-stream-1"></div>
          <div class="sauce-stream sauce-stream-2"></div>
          <div class="sauce-stream sauce-stream-3"></div>
        </div>
      </div>
    `;

    document.body.appendChild(sky);
  }
})();
