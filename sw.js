/*
  هذا الملف بلا أي تخزين مؤقت (Cache) عمدًا: لا نسوّق أن التطبيق يعمل بلا إنترنت.
  وجوده فقط لتحقيق شرط "قابل للتثبيت على الشاشة الرئيسية" في بعض المتصفحات.
  كل طلب يذهب مباشرة للشبكة كأن لا Service Worker موجودًا إطلاقًا.
*/
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => {
  // ننظّف أي ذاكرة مؤقتة من نسخة سابقة كانت تخزّن التطبيق بلا إنترنت.
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.map((k) => caches.delete(k))))
  );
  self.clients.claim();
});
