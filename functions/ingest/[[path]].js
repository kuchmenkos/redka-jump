// Reverse proxy для PostHog EU: події йдуть з нашого домену, тож блокувальники реклами їх не ріжуть.
const API = 'eu.i.posthog.com';
const ASSETS = 'eu-assets.i.posthog.com';

export async function onRequest({ request, params }) {
  const url = new URL(request.url);
  const path = '/' + [].concat(params.path || []).join('/');
  const host = path.startsWith('/static/') ? ASSETS : API;
  const headers = new Headers(request.headers);
  headers.set('host', host);
  headers.delete('cookie');
  const res = await fetch('https://' + host + path + url.search, {
    method: request.method,
    headers,
    body: ['GET', 'HEAD'].includes(request.method) ? undefined : request.body,
  });
  return new Response(res.body, { status: res.status, headers: res.headers });
}
