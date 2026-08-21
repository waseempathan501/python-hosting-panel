<?php
require_once __DIR__ . '/config.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST' || empty($_FILES['files'])) {
    header('Location: index.php?status=error&msg=' . urlencode('Koi file select nahi ki gayi.'));
    exit;
}

if (!is_dir(UPLOAD_DIR)) {
    mkdir(UPLOAD_DIR, 0755, true);
}

$files = $_FILES['files'];
$count = is_array($files['name']) ? count($files['name']) : 0;

$uploaded = 0;
$errors   = [];

for ($i = 0; $i < $count; $i++) {
    $name     = $files['name'][$i];
    $tmpName  = $files['tmp_name'][$i];
    $size     = $files['size'][$i];
    $error    = $files['error'][$i];

    if ($name === '' || $error === UPLOAD_ERR_NO_FILE) {
        continue;
    }

    if ($error !== UPLOAD_ERR_OK) {
        $errors[] = "$name : upload error code $error";
        continue;
    }

    $ext = strtolower(pathinfo($name, PATHINFO_EXTENSION));

    if (!array_key_exists($ext, ALLOWED_TYPES)) {
        $errors[] = "$name : ye file type allow nahi hai";
        continue;
    }

    if ($size > MAX_FILE_SIZE) {
        $errors[] = "$name : size limit (" . human_size(MAX_FILE_SIZE) . ") se zyada hai";
        continue;
    }

    // Safe file name banao (spaces/special chars hatao) + timestamp taake overwrite na ho
    $baseName = pathinfo($name, PATHINFO_FILENAME);
    $safeBase = preg_replace('/[^A-Za-z0-9_\-]/', '_', $baseName);
    $safeName = $safeBase . '_' . time() . mt_rand(100, 999) . '.' . $ext;

    $destination = UPLOAD_DIR . $safeName;

    if (move_uploaded_file($tmpName, $destination)) {
        $uploaded++;
    } else {
        $errors[] = "$name : server par save nahi ho saki";
    }
}

if ($uploaded > 0 && empty($errors)) {
    header('Location: index.php?status=success&count=' . $uploaded);
} elseif ($uploaded > 0 && !empty($errors)) {
    header('Location: index.php?status=partial&count=' . $uploaded . '&msg=' . urlencode(implode(' | ', $errors)));
} else {
    header('Location: index.php?status=error&msg=' . urlencode(implode(' | ', $errors)));
}
exit;
