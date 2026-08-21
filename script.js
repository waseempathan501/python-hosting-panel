// ---------- Matrix rain background ----------
const canvas = document.getElementById('matrix');
const ctx = canvas.getContext('2d');
let w, h, columns, drops;

function setupMatrix() {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
    const fontSize = 16;
    columns = Math.floor(w / fontSize);
    drops = new Array(columns).fill(1);
}
setupMatrix();
window.addEventListener('resize', setupMatrix);

const chars = 'アカサタナハマヤラワ01WASEEM$#@%&';
function drawMatrix() {
    ctx.fillStyle = 'rgba(6,10,8,0.08)';
    ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = '#00ff6a';
    ctx.font = '15px monospace';
    for (let i = 0; i < drops.length; i++) {
        const text = chars[Math.floor(Math.random() * chars.length)];
        ctx.fillText(text, i * 16, drops[i] * 16);
        if (drops[i] * 16 > h && Math.random() > 0.975) drops[i] = 0;
        drops[i]++;
    }
}
setInterval(drawMatrix, 50);

// ---------- Drag & drop + file list preview ----------
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const fileNameList = document.getElementById('fileNameList');
const dropText = document.getElementById('dropText');

function renderFileNames() {
    fileNameList.innerHTML = '';
    if (fileInput.files.length === 0) {
        dropText.textContent = '📂 Files yahan drop karein ya click karke choose karein';
        return;
    }
    dropText.textContent = `✅ ${fileInput.files.length} file(s) selected`;
    Array.from(fileInput.files).forEach(f => {
        const li = document.createElement('li');
        li.textContent = `• ${f.name} (${(f.size / 1024).toFixed(1)} KB)`;
        fileNameList.appendChild(li);
    });
}

fileInput.addEventListener('change', renderFileNames);

['dragenter', 'dragover'].forEach(evt => {
    dropZone.addEventListener(evt, e => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });
});
['dragleave', 'drop'].forEach(evt => {
    dropZone.addEventListener(evt, e => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
    });
});
dropZone.addEventListener('drop', e => {
    fileInput.files = e.dataTransfer.files;
    renderFileNames();
});

// ---------- Copy link buttons ----------
document.querySelectorAll('.btn-copy').forEach(btn => {
    btn.addEventListener('click', () => {
        const link = btn.getAttribute('data-link');
        navigator.clipboard.writeText(link).then(() => {
            const original = btn.textContent;
            btn.textContent = '✔ Copied';
            setTimeout(() => (btn.textContent = original), 1500);
        });
    });
});
