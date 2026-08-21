function showLoading(resultEl) {
  resultEl.innerHTML = '<span class="loading">Deploying…</span>';
}

function showLink(resultEl, file) {
  const full = window.location.origin + file.url;
  resultEl.innerHTML = `<a href="${file.url}" target="_blank" rel="noopener">✅ Live: ${full}</a>`;
}

function showError(resultEl, message) {
  resultEl.innerHTML = `<span class="err">⚠ ${message}</span>`;
}

document.querySelectorAll('.upload-form').forEach((form) => {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const card = form.closest('.upload-card');
    const resultEl = card.querySelector('.result');
    const endpoint = form.dataset.endpoint;
    const fileInput = form.querySelector('input[type="file"]');

    if (!fileInput.files.length) {
      showError(resultEl, 'Choose a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    showLoading(resultEl);
    try {
      const res = await fetch(endpoint, { method: 'POST', body: formData });
      const data = await res.json();
      if (data.ok) {
        showLink(resultEl, data.file);
        form.reset();
      } else {
        showError(resultEl, data.error || 'Upload failed.');
      }
    } catch (err) {
      showError(resultEl, 'Network error — try again.');
    }
  });
});

document.querySelectorAll('.code-form').forEach((form) => {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const card = form.closest('.upload-card');
    const resultEl = card.querySelector('.result');
    const endpoint = form.dataset.endpoint;
    const title = form.querySelector('input[name="title"]').value;
    const code = form.querySelector('textarea[name="code"]').value;

    if (!code.trim()) {
      showError(resultEl, 'Paste some HTML code first.');
      return;
    }

    showLoading(resultEl);
    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, code }),
      });
      const data = await res.json();
      if (data.ok) {
        showLink(resultEl, data.file);
        form.reset();
      } else {
        showError(resultEl, data.error || 'Hosting failed.');
      }
    } catch (err) {
      showError(resultEl, 'Network error — try again.');
    }
  });
});
