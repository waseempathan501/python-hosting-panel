# WASEEM HOSTING — PHP File Deployment Website

Ye ek complete PHP based hosting/deployment website hai jisme user apni **HTML, CSS,
JavaScript, Images, Audio aur Video** files upload kar sakta hai, aur upload hote hi
har file ka ek **100% working direct live link** mil jata hai.

## ✨ Features
- Multiple files ek sath upload/deploy
- Drag & drop upload
- Live direct link (open + copy button)
- File delete option (admin key protected)
- Hacker/matrix themed dark UI
- GitHub-friendly file size limit (default 20MB/file)

## 📂 Kya kya deploy ho sakta hai
| Type   | Extensions |
|--------|------------|
| Web    | .html .htm .css .js .json |
| Image  | .jpg .jpeg .png .gif .webp .svg .ico |
| Audio  | .mp3 .wav .ogg .m4a |
| Video  | .mp4 .webm .mov .mkv |

Upload hone ke baad file `uploads/` folder me save hoti hai aur uska link is
tarah bantа hai:

```
https://aap-ka-domain.com/uploads/filename_12345678.ext
```

HTML/CSS/JS files browser me render hongi, images/audio/video direct
open/stream hongi — **koi extra setup nahi chahiye**.

---

## 🚀 GitHub par Deploy Karna

> ⚠️ **Important:** GitHub web upload (drag & drop via browser) me per-file
> limit **~25MB** hai (hard limit 100MB, lekin recommend 50MB se kam).
> Isi liye is project me `config.php` ke andar `MAX_FILE_SIZE` **20MB**
> rakha gaya hai — taake aap deployed files ko GitHub par bhi upload/backup
> kar saken bina kisi error ke. Zaroorat ho to ye value khud change kar
> sakte hain.

1. Naya GitHub repository banayein (e.g. `waseem-hosting`)
2. Ye sari files (`index.php`, `upload.php`, `delete.php`, `config.php`,
   `style.css`, `script.js`, `uploads/`, `Procfile`, `composer.json`) usme
   push/upload kar dein
3. **Note:** GitHub sirf static file hosting deta hai (GitHub Pages), aur
   GitHub Pages **PHP run nahi karta**. Isliye GitHub sirf **code store**
   karne ke liye use karein — actual live PHP hosting ke liye niche wala
   **Railway** step follow karein.

---

## 🚂 Railway par Deploy Karna (Live PHP Hosting)

1. [railway.app](https://railway.app) par account banayein
2. **New Project → Deploy from GitHub repo** select karein
3. Apni GitHub repository (jo upar banayi) select karein
4. Railway automatically `composer.json` dekh kar PHP environment detect
   kar lega, aur `Procfile` se pata chal jayega ke server kaise start
   hoga:
   ```
   web: php -S 0.0.0.0:$PORT -t .
   ```
5. Deploy hone ke baad Railway aapko ek live URL dega, jaise:
   ```
   https://waseem-hosting-production.up.railway.app
   ```
6. Bas! Ab website live hai — is URL par jaake files upload/deploy karein,
   har file ka link `https://aap-ki-app.up.railway.app/uploads/filename.ext`
   ki tarah kaam karega.

### ⚠️ Railway Storage ke baare mein zaroori baat
Railway ka default filesystem **ephemeral** hota hai — matlab agar aap
dobara deploy/redeploy karte hain to `uploads/` folder ki files delete ho
sakti hain. Agar aapko files **permanently** save karni hain to Railway
dashboard me:
- **Settings → Volumes** me jaake ek Volume attach karein
- Mount path `/app/uploads` (ya jahan aapka project deploy hai + `/uploads`)
  set karein

Isse `uploads/` folder permanent storage ban jayega aur files har deploy
ke baad bhi safe rahengi.

---

## 🔑 Admin Key
`config.php` ke andar ye line milegi:
```php
define('ADMIN_KEY', 'waseem123');
```
Deploy karne se **pehle isko zaroor change karein**, warna koi bhi aapki
files delete kar sakta hai.

---

## 🖥 Local Testing (apne computer par test karna)
PHP installed hone ke baad terminal me project folder ke andar ye command
chalayein:
```
php -S localhost:8000
```
Phir browser me kholein:
```
http://localhost:8000
```

---

## 📞 Contact
- WhatsApp Channel: https://whatsapp.com/channel/0029VbD4m3ZFCCoWbOzY3x2S
- TikTok: https://tiktok.com/@waseempathan902

**Developed by Waseem Hacker**
