addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)

  // Route agent API calls to private tunnel
  if (url.pathname.startsWith('/api/agents/')) {
    const agentUrl = 'https://agents.hyperfocuszone.com' + url.pathname.replace('/api/agents', '/api')
    return fetch(agentUrl, {
      method: request.method,
      headers: request.headers,
      body: request.body
    })
  }

  // Route dashboard calls to Railway/Render
  if (url.pathname.startsWith('/api/') || url.pathname === '/') {
    const dashboardUrl = 'https://your-railway-app.railway.app' + url.pathname
    const response = await fetch(dashboardUrl, {
      method: request.method,
      headers: request.headers,
      body: request.body
    })

    // Add CORS and security headers
    const modifiedResponse = new Response(response.body, response)
    modifiedResponse.headers.set('Access-Control-Allow-Origin', '*')
    modifiedResponse.headers.set('X-Powered-By', 'ChaosGenius-Cloudflare')
    return modifiedResponse
  }

  // Default: serve from Railway
  const defaultUrl = 'https://your-railway-app.railway.app' + url.pathname
  return fetch(defaultUrl, request)
}
