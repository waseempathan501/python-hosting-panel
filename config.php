<?php
/**
 * WASEEM HOSTING - Config
 * -------------------------------------------------
 * Yahan se aap settings change kar sakte hain.
 */

// Upload folder ka physical path
define('UPLOAD_DIR', __DIR__ . '/uploads/');

// Delete karne ke liye admin key (isko deploy karne se pehle zaroor badal dein!)
define('ADMIN_KEY', 'waseem123');

// Per-file max size (bytes). GitHub web upload ~25MB tak allow karta hai
// isliye default 20MB rakha gaya hai taake GitHub par bhi upload ho sake.
define('MAX_FILE_SIZE', 20 * 1024 * 1024); // 20 MB

// Allowed extensions => category (icon/label ke liye)
define('ALLOWED_TYPES', [
    // Web files
    'html' => 'web', 'htm'  => 'web', 'css'  => 'web', 'js'   => 'web', 'json' => 'web',
    // Images
    'jpg' => 'image', 'jpeg' => 'image', 'png' => 'image', 'gif' => 'image',
    'webp' => 'image', 'svg' => 'image', 'ico' => 'image',
    // Audio
    'mp3' => 'audio', 'wav' => 'audio', 'ogg' => 'audio', 'm4a' => 'audio',
    // Video
    'mp4' => 'video', 'webm' => 'video', 'mov' => 'video', 'mkv' => 'video',
]);

// Har request par current base URL nikalna (Railway / GitHub Pages / localhost sab par kaam karega)
function base_url() {
    $protocol = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http';
    $host     = $_SERVER['HTTP_HOST'] ?? 'localhost';
    $script   = rtrim(str_replace('\\', '/', dirname($_SERVER['SCRIPT_NAME'])), '/');
    return $protocol . '://' . $host . $script;
}

function human_size($bytes) {
    $units = ['B', 'KB', 'MB', 'GB'];
    $i = 0;
    while ($bytes >= 1024 && $i < count($units) - 1) {
        $bytes /= 1024;
        $i++;
    }
    return round($bytes, 2) . ' ' . $units[$i];
}
