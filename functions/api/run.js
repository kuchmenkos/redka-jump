// POST /api/run?pid=… → { ok, tok } — токен старту забігу для лідерборду (потрібен секрет LB_SECRET; без нього токен не вимагається)
const PID_RE = /^[A-Za-z0-9-]{8,64}$/;
export async function onRequestPost({ request, env }) {
  const pid = new URL(request.url).searchParams.get('pid') || '';
  const h = { 'content-type': 'application/json', 'cache-control': 'no-store' };
  if (!env || !env.LB_SECRET || !PID_RE.test(pid)) return new Response(JSON.stringify({ ok: true, tok: '' }), { headers: h });
  const ts = String(Date.now());
  const k = await crypto.subtle.importKey('raw', new TextEncoder().encode(env.LB_SECRET), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', k, new TextEncoder().encode(ts + ':' + pid));
  const hex = [...new Uint8Array(sig)].map(b => b.toString(16).padStart(2, '0')).join('');
  return new Response(JSON.stringify({ ok: true, tok: ts + '.' + hex }), { headers: h });
}
