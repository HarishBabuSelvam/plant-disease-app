// flask_app/static/js/app.js
// ============================================
// PLANT DISEASE APP — JAVASCRIPT
// ============================================

// ── UPLOAD PAGE ──────────────────────────────
function initUploadPage() {
  const uploadArea     = document.getElementById('upload-area');
  const fileInput      = document.getElementById('file-input');
  const preview        = document.getElementById('preview-container');
  const previewImg     = document.getElementById('preview-img');
  const previewInfo    = document.getElementById('preview-info');
  const submitBtn      = document.getElementById('submit-btn');
  const uploadForm     = document.getElementById('upload-form');
  const loadingOverlay = document.getElementById('loading-overlay');

  if (!uploadArea) return;

  // Click to browse
  uploadArea.addEventListener('click', () => fileInput.click());

  // Drag over
  uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
  });

  // Drag leave
  uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
  });

  // Drop
  uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  });

  // File selected via input
  fileInput.addEventListener('change', () => {
    if (fileInput.files[0]) handleFile(fileInput.files[0]);
  });

  function handleFile(file) {

    // ── VALIDATE TYPE ──────────────────────
    const allowedTypes = [
      'image/jpeg', 'image/jpg',
      'image/png',  'image/webp'
    ];
    if (!allowedTypes.includes(file.type)) {
      showAlert(
        '❌ Invalid file type! Please upload JPG, PNG or WEBP.',
        'error'
      );
      return;
    }

    // ── VALIDATE SIZE (10MB) ───────────────
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
      showAlert(
        `❌ File too large (${(file.size/1024/1024).toFixed(1)}MB).
         Maximum is 10MB.`,
        'error'
      );
      return;
    }

    // ── VALIDATE MIN SIZE ──────────────────
    if (file.size < 1000) {
      showAlert(
        '❌ File is too small. Please upload a real image.',
        'error'
      );
      return;
    }

    // ── SHOW PREVIEW ───────────────────────
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImg.src = e.target.result;
      preview.style.display = 'block';

      const sizeKB = (file.size / 1024).toFixed(1);
      const sizeMB = (file.size / 1024 / 1024).toFixed(2);
      const sizeStr = file.size > 1024*1024
        ? `${sizeMB} MB` : `${sizeKB} KB`;

      previewInfo.innerHTML = `
        📁 <strong>${file.name}</strong> —
        ${sizeStr} —
        ${file.type.split('/')[1].toUpperCase()}
      `;

      submitBtn.disabled = false;
      submitBtn.style.opacity = '1';
      submitBtn.innerHTML = '🔬 Analyze Plant';
      uploadArea.style.borderColor = 'var(--primary)';
      uploadArea.style.background  = 'rgba(45,106,79,0.05)';
    };
    reader.readAsDataURL(file);

    // Update file input
    const dt = new DataTransfer();
    dt.items.add(file);
    fileInput.files = dt.files;
  }

  // ── FORM SUBMIT ────────────────────────────
  if (uploadForm) {
    uploadForm.addEventListener('submit', (e) => {
      if (!fileInput.files[0]) {
        e.preventDefault();
        showAlert(
          '⚠️ Please select an image first!',
          'error'
        );
        return;
      }

      // Show loading
      if (loadingOverlay) {
        loadingOverlay.classList.add('active');
        animateLoadingText();
      }

      submitBtn.disabled = true;
      submitBtn.innerHTML = '⏳ Analyzing...';
    });
  }
}

// ── LOADING ANIMATION ─────────────────────────
function animateLoadingText() {
  const messages = [
    '🤖 AI is analyzing your plant...',
    '🔬 Examining leaf patterns...',
    '🧠 Running disease detection...',
    '📊 Calculating confidence score...',
    '📋 Looking up disease information...',
    '✅ Almost done...'
  ];
  let i = 0;
  const textEl = document.querySelector('.loading-text');
  if (!textEl) return;

  setInterval(() => {
    i = (i + 1) % messages.length;
    textEl.textContent = messages[i];
  }, 1500);
}

// ── RESULT PAGE ───────────────────────────────
function initResultPage() {
  // Animate recovery bar
  setTimeout(() => {
    const bar = document.getElementById('recovery-bar');
    if (bar) {
      bar.style.transition = 'width 1.5s ease';
      bar.style.width = bar.getAttribute('data-value') + '%';
    }
  }, 400);

  // Animate top3 bars
  setTimeout(() => {
    document.querySelectorAll('.top3-bar').forEach(b => {
      b.style.transition = 'width 1s ease';
      b.style.width = b.getAttribute('data-value') + '%';
    });
  }, 600);

  // Animate stat numbers counting up
  document.querySelectorAll('.stat-number[data-count]')
  .forEach(el => {
    const target = parseInt(el.getAttribute('data-count'));
    let current  = 0;
    const step   = Math.ceil(target / 30);
    const timer  = setInterval(() => {
      current = Math.min(current + step, target);
      el.textContent = current + '%';
      if (current >= target) clearInterval(timer);
    }, 50);
  });
}

// ── HISTORY PAGE ──────────────────────────────
function initHistoryPage() {

  // Search filter
  const searchInput = document.getElementById('history-search');
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      const q = searchInput.value.toLowerCase();
      let visible = 0;
      document.querySelectorAll('.history-row').forEach(row => {
        const match = row.textContent.toLowerCase().includes(q);
        row.style.display = match ? '' : 'none';
        if (match) visible++;
      });

      // Show no results message
      const noResults = document.getElementById('no-results');
      if (noResults) {
        noResults.style.display = visible === 0 ? 'block' : 'none';
      }
    });
  }

  // Delete confirmation
  document.querySelectorAll('.delete-form').forEach(form => {
    form.addEventListener('submit', (e) => {
      if (!confirm(
        '🗑️ Delete this prediction from history?\nThis cannot be undone.'
      )) {
        e.preventDefault();
      }
    });
  });
}

// ── ALERT HELPER ──────────────────────────────
function showAlert(message, type = 'error') {
  // Remove existing alerts
  document.querySelectorAll('.alert-dynamic')
  .forEach(a => a.remove());

  const alert = document.createElement('div');
  alert.className = `alert alert-${type} alert-dynamic`;
  alert.innerHTML = message;
  alert.style.cssText = `
    position: fixed;
    top: 80px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 9999;
    min-width: 300px;
    max-width: 500px;
    text-align: center;
    box-shadow: 0 8px 30px rgba(0,0,0,0.2);
  `;

  document.body.appendChild(alert);

  // Auto remove after 4 seconds
  setTimeout(() => {
    alert.style.opacity = '0';
    alert.style.transition = 'opacity 0.5s';
    setTimeout(() => alert.remove(), 500);
  }, 4000);
}

// ── INIT ──────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initUploadPage();
  initResultPage();
  initHistoryPage();

  // Auto-hide flash messages
  document.querySelectorAll(
    '.alert:not(.alert-dynamic)'
  ).forEach(a => {
    setTimeout(() => {
      a.style.opacity    = '0';
      a.style.transition = 'opacity 0.5s';
      setTimeout(() => a.remove(), 500);
    }, 3000);
  });
});