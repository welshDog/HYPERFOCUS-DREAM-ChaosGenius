// 🚀 BROski Ultra Cache Worker - PWA Service Worker
// Provides instant navigation even when offline

const CACHE_NAME = "broski-ultra-nav-v2.0";
const CRITICAL_ROUTES = [
  "/",
  "/dashboard",
  "/user_portal",
  "/ultra_analytics_panel",
  "/etsy-dashboard",
  "/tiktok_shop_dashboard",
  "/neurod_analytics_dashboard",
  "/production_monitoring",
  "/broski_defender_dashboard",
  "/hyperfocus_brain_dashboard",
  "/api/live-status",
];

const STATIC_ASSETS = [
  "/static/css/broski-ultra.css",
  "/static/js/broski-nav.js",
  "/templates/includes/broski_nav.html",
];

// Install event - cache critical resources
self.addEventListener("install", (event) => {
  console.log("🚀 BROski Cache Worker: Installing...");

  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => {
        console.log("🚀 BROski Cache: Caching critical routes");
        return cache.addAll([...CRITICAL_ROUTES, ...STATIC_ASSETS]);
      })
      .catch((error) => {
        console.log("🚀 BROski Cache: Partial cache success");
        // Continue even if some resources fail to cache
      })
  );

  // Activate immediately
  self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener("activate", (event) => {
  console.log("🚀 BROski Cache Worker: Activating...");

  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME && cacheName.startsWith("broski-")) {
            console.log("🚀 BROski Cache: Cleaning old cache:", cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );

  // Take control of all clients immediately
  self.clients.claim();
});

// Fetch event - serve from cache with network fallback
self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);

  // Only handle GET requests for our domain
  if (event.request.method !== "GET" || !url.pathname.startsWith("/")) {
    return;
  }

  // Special handling for live status API - always try network first
  if (url.pathname === "/api/live-status") {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          // Cache successful responses
          if (response.ok) {
            const responseClone = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, responseClone);
            });
          }
          return response;
        })
        .catch(() => {
          // Fallback to cached version if network fails
          return caches.match(event.request);
        })
    );
    return;
  }

  // Cache-first strategy for navigation and static assets
  if (
    CRITICAL_ROUTES.includes(url.pathname) ||
    url.pathname.startsWith("/static/") ||
    url.pathname.includes("dashboard")
  ) {
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        if (cachedResponse) {
          console.log("🚀 BROski Cache: Serving from cache:", url.pathname);

          // Update cache in background
          fetch(event.request)
            .then((response) => {
              if (response.ok) {
                caches.open(CACHE_NAME).then((cache) => {
                  cache.put(event.request, response.clone());
                });
              }
            })
            .catch(() => {
              // Ignore network errors in background update
            });

          return cachedResponse;
        }

        // Not in cache, fetch from network
        return fetch(event.request).then((response) => {
          if (response.ok) {
            const responseClone = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, responseClone);
            });
          }
          return response;
        });
      })
    );
  }
});

// Background sync for status updates (if supported)
if ("sync" in self.registration) {
  self.addEventListener("sync", (event) => {
    if (event.tag === "broski-status-sync") {
      console.log("🚀 BROski Cache: Background status sync");
      event.waitUntil(
        fetch("/api/live-status")
          .then((response) => {
            if (response.ok) {
              return caches.open(CACHE_NAME).then((cache) => {
                return cache.put("/api/live-status", response.clone());
              });
            }
          })
          .catch(() => {
            console.log("🚀 BROski Cache: Background sync failed");
          })
      );
    }
  });
}

// Message handling for cache updates
self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }

  if (event.data && event.data.type === "UPDATE_CACHE") {
    const url = event.data.url;
    if (url) {
      caches.open(CACHE_NAME).then((cache) => {
        fetch(url).then((response) => {
          if (response.ok) {
            cache.put(url, response.clone());
            console.log("🚀 BROski Cache: Updated cache for:", url);
          }
        });
      });
    }
  }
});

console.log("🚀 BROski Ultra Cache Worker: LOADED AND READY");
