<?php
require_once __DIR__ . '/config.php';

$base = base_url();
$status = $_GET['status'] ?? '';
$msg    = $_GET['msg'] ?? '';
$count  = $_GET['count'] ?? '';

if (!is_dir(UPLOAD_DIR)) {
    mkdir(UPLOAD_DIR, 0755, true);
}

$allFiles = array_diff(scandir(UPLOAD_DIR), ['.', '..', '.htaccess', 'index.php']);
rsort($allFiles); // naye files upar

$iconFor = function ($ext) {
    $map = [
        'web'   => '&lt;/&gt;',
        'image' => '🖼',
        'audio' => '🎧',
        'video' => '🎬',
    ];
    return $map[ALLOWED_TYPES[$ext] ?? ''] ?? '📄';
};
?>
<!DOCTYPE html>
<html lang="ur">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WASEEM HOSTING</title>
<link rel="stylesheet" href="style.css">
</head>
<body>

<canvas id="matrix"></canvas>

<div class="scanline"></div>

<div class="wrapper">

    <div class="avatar-box">
        <div class="avatar-ring">
            <img src="https://raw.githubusercontent.com/waseempathan501/Photo-link-/refs/heads/main/IMG-20260625-WA0003.jpg" alt="Waseem" class="avatar-img">
        </div>
    </div>

    <h1 class="glitch" data-text="WASEEM HOSTING">WASEEM HOSTING</h1>
    <p class="tagline">&gt; secure_file_deployment_terminal <span class="cursor">_</span></p>

    <?php if ($status === 'success'): ?>
        <div class="alert alert-ok">✔ <?= $count ? htmlspecialchars($count) . ' file(s) successfully deployed!' : htmlspecialchars($msg) ?></div>
    <?php elseif ($status === 'partial'): ?>
        <div class="alert alert-warn">⚠ <?= htmlspecialchars($count) ?> file(s) deployed, kuch fail hui: <?= htmlspecialchars($msg) ?></div>
    <?php elseif ($status === 'error'): ?>
        <div class="alert alert-err">✖ <?= htmlspecialchars($msg) ?></div>
    <?php endif; ?>

    <section class="panel">
        <h2>&gt; UPLOAD // DEPLOY</h2>
        <form action="upload.php" method="POST" enctype="multipart/form-data" class="upload-form">
            <label for="fileInput" class="drop-zone" id="dropZone">
                <span id="dropText">📂 Files yahan drop karein ya click karke choose karein</span>
                <input type="file" name="files[]" id="fileInput" multiple required
                       accept=".html,.htm,.css,.js,.json,.jpg,.jpeg,.png,.gif,.webp,.svg,.ico,.mp3,.wav,.ogg,.m4a,.mp4,.webm,.mov,.mkv">
            </label>
            <ul id="fileNameList" class="file-name-list"></ul>
            <button type="submit" class="btn-deploy">⚡ DEPLOY NOW</button>
        </form>
        <p class="hint">Max size per file: <?= human_size(MAX_FILE_SIZE) ?> (GitHub-friendly)</p>
    </section>

    <section class="panel">
        <h2>&gt; SUPPORTED_FORMATS</h2>
        <div class="formats-grid">
            <div class="format-card"><span>&lt;/&gt;</span><b>Web</b><small>HTML, CSS, JS, JSON</small></div>
            <div class="format-card"><span>🖼</span><b>Images</b><small>JPG, PNG, GIF, WEBP, SVG</small></div>
            <div class="format-card"><span>🎧</span><b>Audio</b><small>MP3, WAV, OGG, M4A</small></div>
            <div class="format-card"><span>🎬</span><b>Video</b><small>MP4, WEBM, MOV, MKV</small></div>
        </div>
        <p class="note">Deploy hone ke baad har file ka ek 100% working live direct link mil jayega — HTML/CSS/JS files browser mein render hongi, aur audio/video/images direct stream/open hongi.</p>
    </section>

    <section class="panel">
        <h2>&gt; DEPLOYED_FILES <span class="count-badge"><?= count($allFiles) ?></span></h2>
        <?php if (empty($allFiles)): ?>
            <p class="empty">// abhi tak koi file deploy nahi hui...</p>
        <?php else: ?>
            <div class="file-grid">
                <?php foreach ($allFiles as $f):
                    $ext = strtolower(pathinfo($f, PATHINFO_EXTENSION));
                    $link = $base . '/uploads/' . rawurlencode($f);
                    $size = human_size(filesize(UPLOAD_DIR . $f));
                ?>
                <div class="file-card">
                    <div class="file-icon"><?= $iconFor($ext) ?></div>
                    <div class="file-name" title="<?= htmlspecialchars($f) ?>"><?= htmlspecialchars($f) ?></div>
                    <div class="file-size"><?= $size ?></div>
                    <div class="file-actions">
                        <a href="<?= htmlspecialchars($link) ?>" target="_blank" class="btn-link">🔗 Open Live</a>
                        <button class="btn-copy" data-link="<?= htmlspecialchars($link) ?>">📋 Copy</button>
                        <a href="delete.php?file=<?= urlencode($f) ?>&key=<?= urlencode(ADMIN_KEY) ?>"
                           class="btn-del" onclick="return confirm('Delete karein?')">🗑</a>
                    </div>
                </div>
                <?php endforeach; ?>
            </div>
        <?php endif; ?>
    </section>

    <footer class="footer">
        <div class="social-row">
            <a href="https://whatsapp.com/channel/0029VbD4m3ZFCCoWbOzY3x2S" target="_blank" class="social-icon whatsapp" title="WhatsApp Channel">
                <svg viewBox="0 0 32 32" width="28" height="28"><path fill="currentColor" d="M16 0C7.2 0 0 7.2 0 16c0 2.8.7 5.5 2.1 7.9L0 32l8.3-2.1c2.3 1.3 4.9 1.9 7.7 1.9 8.8 0 16-7.2 16-16S24.8 0 16 0zm0 29.3c-2.5 0-4.9-.7-7-1.9l-.5-.3-4.9 1.3 1.3-4.8-.3-.5C3.2 20.9 2.5 18.5 2.5 16 2.5 8.6 8.6 2.5 16 2.5S29.5 8.6 29.5 16 23.4 29.3 16 29.3zm7.6-9.9c-.4-.2-2.4-1.2-2.8-1.3-.4-.1-.7-.2-.9.2-.3.4-1 1.3-1.3 1.6-.2.2-.5.3-.9.1-.4-.2-1.7-.6-3.2-2-1.2-1.1-2-2.4-2.2-2.8-.2-.4 0-.6.2-.8.2-.2.4-.5.6-.7.2-.2.3-.4.4-.7.1-.3.1-.6 0-.8-.1-.2-.9-2.2-1.2-3-.3-.8-.6-.7-.9-.7h-.7c-.3 0-.7.1-1 .5-.4.4-1.4 1.3-1.4 3.2s1.4 3.7 1.6 4c.2.3 2.8 4.2 6.7 5.9.9.4 1.7.6 2.3.8.9.3 1.8.2 2.4.2.7-.1 2.4-1 2.7-1.9.3-.9.3-1.7.2-1.9-.1-.2-.4-.3-.8-.5z"/></svg>
            </a>
            <a href="https://tiktok.com/@waseempathan902" target="_blank" class="social-icon tiktok" title="TikTok">
                <svg viewBox="0 0 32 32" width="26" height="26"><path fill="currentColor" d="M23.5 8.9c-1.6-1.1-2.7-2.9-2.9-4.9h-4v18.6c0 2.2-1.8 4-4 4s-4-1.8-4-4 1.8-4 4-4c.4 0 .8.1 1.1.2v-4.1c-.4-.1-.7-.1-1.1-.1-4.5 0-8.1 3.6-8.1 8.1s3.6 8.1 8.1 8.1 8.1-3.6 8.1-8.1V13c1.6 1.1 3.5 1.8 5.5 1.8V10.8c-1 0-2-.3-2.7-.9z"/></svg>
            </a>
        </div>
        <h3 class="dev-heading">DEVELOPED BY WASEEM HACKER</h3>
    </footer>

</div>

<script src="script.js"></script>
</body>
</html>
