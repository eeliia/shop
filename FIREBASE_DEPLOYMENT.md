# راهنمای استقرار در فایربیس

## پیش‌نیازها

1. نصب Firebase CLI:
   ```
   npm install -g firebase-tools
   ```

2. ورود به حساب گوگل:
   ```
   firebase login
   ```

3. ایجاد پروژه در Firebase Console:
   - به آدرس https://console.firebase.google.com بروید
   - یک پروژه جدید ایجاد کنید
   - سرویس‌های مورد نیاز (Hosting, Firestore, Storage) را فعال کنید

## تنظیمات پروژه

1. فایل `.env` را با اطلاعات پروژه فایربیس خود به‌روزرسانی کنید:
   ```
   FIREBASE_API_KEY=your-api-key
   FIREBASE_AUTH_DOMAIN=your-project-id.firebaseapp.com
   FIREBASE_PROJECT_ID=your-project-id
   FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
   FIREBASE_MESSAGING_SENDER_ID=your-sender-id
   FIREBASE_APP_ID=your-app-id
   FIREBASE_MEASUREMENT_ID=your-measurement-id
   ```

2. فایل `.firebaserc` را با شناسه پروژه فایربیس خود به‌روزرسانی کنید:
   ```json
   {
     "projects": {
       "default": "your-project-id"
     }
   }
   ```

3. فایل `firebase-service-account.json` را با کلید سرویس اکانت خود جایگزین کنید:
   - به Firebase Console بروید
   - به بخش Project Settings > Service accounts بروید
   - روی "Generate new private key" کلیک کنید
   - فایل دانلود شده را به عنوان `firebase-service-account.json` در مسیر اصلی پروژه قرار دهید

## استقرار پروژه

1. جمع‌آوری فایل‌های استاتیک:
   ```
   python manage.py collectstatic
   ```

2. استقرار در فایربیس:
   ```
   firebase deploy
   ```

3. برای استقرار فقط هاستینگ:
   ```
   firebase deploy --only hosting
   ```

## نکات مهم

- فایل‌های `.env` و `firebase-service-account.json` حاوی اطلاعات محرمانه هستند و نباید در مخزن گیت ذخیره شوند.
- برای استفاده از Firestore و Storage، باید قوانین امنیتی مناسب را در Firebase Console تنظیم کنید.
- برای استفاده از دامنه سفارشی، باید آن را در بخش Hosting تنظیمات فایربیس اضافه کنید.