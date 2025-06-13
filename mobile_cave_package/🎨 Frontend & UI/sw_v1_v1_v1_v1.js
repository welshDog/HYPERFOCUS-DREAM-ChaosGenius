const CACHE_NAME = "lyndz-cave-ultra-v1.0.1749666300
const urlsToCache = ["./lyndz_cave_mobile_ultra.html", "./manifest.json"];

// Install event - cache resources
self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function (cache) {
      console.log("🕋 LYNDZ CAVE: Service Worker cache opened");
      return cache.addAll(urlsToCache);
    })
  );
});

// Fetch event - serve cached content when offline
self.addEventListener("fetch", function (event) {
  event.respondWith(
    caches.match(event.request).then(function (response) {
      // Cache hit - return response
      if (response) {
        return response;
      }
      return fetch(event.request);
    })
  );
});

// Activate event - clean up old caches
self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys().then(function (cacheNames) {
      return Promise.all(
        cacheNames.map(function (cacheName) {
          if (cacheName !== CACHE_NAME) {
            console.log("🕋 LYNDZ CAVE: Deleting old cache:", cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Background sync for when connection is restored
self.addEventListener("sync", function (event) {
  if (event.tag === "background-sync") {
    event.waitUntil(doBackgroundSync());
  }
});

function doBackgroundSync() {
  // Sync data when connection is restored
  return fetch("/api/sync")
    .then((response) => {
      console.log("🕋 LYNDZ CAVE: Background sync completed");
    })
    .catch((err) => {
      console.log("🕋 LYNDZ CAVE: Background sync failed:", err);
    });
}

// Push notifications
self.addEventListener("push", function (event) {
  const options = {
    body: event.data ? event.data.text() : "🚀 LYNDZ CAVE ULTRA notification!",
    icon: "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNzIiIGhlaWdodD0iNzIiIHZpZXdCb3g9IjAgMCA3MiA3MiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNzIiIGhlaWdodD0iNzIiIHJ4PSIxNiIgZmlsbD0idXJsKCNncmFkaWVudDApIi8+PHRleHQgeD0iMzYiIHk9IjQ1IiBmb250LWZhbWlseT0iQ291cmllciBOZXcsIG1vbm9zcGFjZSIgZm9udC1zaXplPSIyNCIgZmlsbD0iIzAwZmZmZiIgdGV4dC1hbmNob3I9Im1pZGRsZSI+8J+Xi/CfkrsPC90ZXh0PjxkZWZzPjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQwIiB4MT0iMCIgeTE9IjAiIHgyPSI3MiIgeTI9IjcyIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiMwYTBhMGEiLz48c3RvcCBvZmZzZXQ9IjAuMjUiIHN0b3AtY29sb3I9IiMxYTAwMzMiLz48c3RvcCBvZmZzZXQ9IjAuNSIgc3RvcC1jb2xvcj0iIzAwMDA2NiIvPjxzdG9wIG9mZnNldD0iMC43NSIgc3RvcC1jb2xvcj0iIzMzMDA2NiIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzBhMGEwYSIvPjwvbGluZWFyR3JhZGllbnQ+PC9kZWZzPjwvc3ZnPg==",
    badge:
      "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNzIiIGhlaWdodD0iNzIiIHZpZXdCb3g9IjAgMCA3MiA3MiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48dGV4dCB4PSIzNiIgeT0iNDUiIGZvbnQtc2l6ZT0iMjQiIHRleHQtYW5jaG9yPSJtaWRkbGUiPvCfl4vwn5K7PC90ZXh0Pjwvc3ZnPg==",
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1,
    },
    actions: [
      {
        action: "explore",
        title: "🚀 Open Cave",
        icon: "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48dGV4dCB4PSIxMiIgeT0iMTYiIGZvbnQtc2l6ZT0iMTIiIHRleHQtYW5jaG9yPSJtaWRkbGUiPvCfmpA8L3RleHQ+PC9zdmc+",
      },
      {
        action: "close",
        title: "❌ Close",
        icon: "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48dGV4dCB4PSIxMiIgeT0iMTYiIGZvbnQtc2l6ZT0iMTIiIHRleHQtYW5jaG9yPSJtaWRkbGUiPuKdjzwvdGV4dD48L3N2Zz4=",
      },
    ],
  };

  event.waitUntil(
    self.registration.showNotification("🕋 LYNDZ CAVE ULTRA", options)
  );
});

// Handle notification clicks
self.addEventListener("notificationclick", function (event) {
  event.notification.close();

  if (event.action === "explore") {
    event.waitUntil(clients.openWindow("./lyndz_cave_mobile_ultra.html"));
  }
});
