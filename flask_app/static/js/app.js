// flask_app/static/js/app.js
// ============================================
// PLANT DISEASE APP - JAVASCRIPT
// ============================================

// ── UPLOAD PAGE ──────────────────────────────
function initUploadPage() {
  const uploadArea   = document.getElementById('upload-area');
  const fileInput    = document.getElementById('file-input');
  const preview      = document.getElementById('preview-container');
  const previewImg   = document.getElementById('preview-img');
  const previewInfo  = document.getElementById('preview-info');
  const submitBtn    = document.getElementById('submit-btn');
  const uploadForm   = document.getElementById('upload-form');
  const loadingOverlay = document.getElementById('loading-overlay');

  if (!uploadArea) return;

  // Click to browse
  uploadArea.addEventListener('click', () => fileInput.click());

  // Drag and drop
  uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
  });

  uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
  });

  uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  });

  // File selected
  fileInput.addEventListener('change', () => {
    if (fileInput.files[0]) handleFile(fileInput.files[0]);
  });

  function handleFile(file) {
    // Validate type
    const allowed = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    if (!allowed.includes(file.type)) {
      showAlert('Please upload a JPG, PNG, or WEBP image.', 'error');
      return;
    }

    // Validate size (10MB)
    if (file.size > 10 * 1024 * 1024) {
      showAlert('File is too large. Maximum size is 10MB.', 'error');
      return;
    }

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImg.src = e.target.result;
      preview.style.display = 'block';
      previewInfo.textContent =
        `📁 ${file.name} — ${(file.size/1024).toFixed(1)} KB`;
      submitBtn.disabled = false;
      submitBtn.style.opacity = '1';
      uploadArea.style.borderColor = 'var(--primary)';
    };
    reader.readAsDataURL(file);

    // Update file input
    const dt = new DataTransfer();
    dt.items.add(file);
    fileInput.files = dt.files;
  }

  // Form submit
  if (uploadForm) {
    uploadForm.addEventListener('submit', (e) => {
      if (!fileInput.files[0]) {
        e.preventDefault();
        showAlert('Please select an image first!', 'error');
        return;
      }
      // Show loading overlay
      if (loadingOverlay) {
        loadingOverlay.classList.add('active');
      }
      submitBtn.disabled = true;
      submitBtn.innerHTML = '⏳ Analyzing...';
    });
  }
}

// ── RESULT PAGE ───────────────────────────────
function initResultPage() {
  // Animate recovery bar
  const bar = document.getElementById('recovery-bar');
  if (bar) {
    const target = bar.getAttribute('data-value');
    setTimeout(() => { bar.style.width = target + '%'; }, 300);
  }

  // Animate top3 bars
  document.querySelectorAll('.top3-bar').forEach(b => {
    const target = b.getAttribute('data-value');
    setTimeout(() => { b.style.width = target + '%'; }, 500);
  });
}

// ── ALERT HELPER ─────────────────────────────
function showAlert(message, type = 'error') {
  const existing = document.querySelector('.alert-dynamic');
  if (existing) existing.remove();

  const alert = document.createElement('div');
  alert.className = `alert alert-${type} alert-dynamic`;
  alert.innerHTML = `${type === 'error' ? '❌' : '✅'} ${message}`;

  const container = document.querySelector('.upload-container') ||
                    document.querySelector('.container');
  if (container) container.prepend(alert);

  setTimeout(() => alert.remove(), 4000);
}

// ── HISTORY PAGE ──────────────────────────────
function initHistoryPage() {
  // Search filter
  const searchInput = document.getElementById('history-search');
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      const q = searchInput.value.toLowerCase();
      document.querySelectorAll('.history-row').forEach(row => {
        row.style.display =
          row.textContent.toLowerCase().includes(q) ? '' : 'none';
      });
    });
  }

  // Delete confirmation
  document.querySelectorAll('.delete-form').forEach(form => {
    form.addEventListener('submit', (e) => {
      if (!confirm('Delete this prediction from history?')) {
        e.preventDefault();
      }
    });
  });
}

// ── INIT ON PAGE LOAD ─────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initUploadPage();
  initResultPage();
  initHistoryPage();

  // Auto-hide flash messages
  document.querySelectorAll('.alert:not(.alert-dynamic)').forEach(a => {
    setTimeout(() => {
      a.style.opacity = '0';
      a.style.transition = 'opacity 0.5s';
      setTimeout(() => a.remove(), 500);
    }, 3000);
  });
});