# دليل النشر على Render - SecureChat

## مقدمة

هذا الدليل يشرح خطوة بخطوة كيفية نشر تطبيق SecureChat على منصة Render للحصول على رابط مباشر للتطبيق.

## متطلبات ما قبل النشر

### 1. إنشاء حساب على Render
- اذهب إلى [render.com](https://render.com)
- أنشئ حساب جديد أو سجل دخول
- اربط حسابك مع GitHub (مطلوب)

### 2. رفع المشروع على GitHub
```bash
# إنشاء repository جديد
git init
git add .
git commit -m "Initial commit: SecureChat app"

# رفع على GitHub
git remote add origin https://github.com/username/securechat.git
git branch -M main
git push -u origin main
