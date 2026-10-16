// Відкритий лідерборд «Редька Джамп» — Cloudflare Pages Function.
// Потрібен KV binding LEADERBOARD (Pages → Settings → Functions → KV namespace bindings).
// GET  /api/scores?pid=…   → { ok, top:[{n,s,z,l,me}], total, rank }
// POST /api/scores         → { pid, name, score, dur, zone, look } → { ok, rank, top }

const SHOW = 50;          // скільки віддаємо клієнту
const KEEP = 100;         // скільки тримаємо в KV
const MAX_SCORE = 2000000;
const MAX_RATE = 9000;    // найбільший реалістичний приріст рахунку за секунду забігу
const NAME_RE = /^[\p{L}\p{N} _.!\-]{1,12}$/u;
const PID_RE = /^[A-Za-z0-9-]{8,64}$/;

// Грубий фільтр лайки: нормалізуємо схожі латинські літери й цифри, прибираємо все крім літер.
const BAD = ['хуй', 'хуе', 'хуя', 'хуї', 'хує', 'хер', 'пизд', 'пізд', 'пезд', 'ебат', 'ебан', 'еблан', 'єба', 'єбл', 'ебу', 'бляд', 'блят', 'блят', 'сука', 'сучк', 'мудак', 'мудил', 'мудак', 'гандон', 'залуп', 'шлюх', 'пидор', 'підор', 'пидар', 'підар', 'педик', 'підрас', 'пидрас', 'fuck', 'shit', 'bitch', 'cunt', 'dick', 'nigg', 'fagg', 'whore', 'slut'];
const LOOK = { a: 'а', b: 'в', c: 'с', e: 'е', h: 'н', k: 'к', m: 'м', o: 'о', p: 'р', t: 'т', x: 'х', y: 'у', i: 'і', '0': 'о', '3': 'з', '1': 'і', '4': 'ч', 'ё': 'е', 'ы': 'и', 'э': 'е' };

function normalize(s) {
  let out = '';
  for (const ch of s.toLowerCase()) out += LOOK[ch] || ch;
  return out.replace(/[^\p{L}]/gu, '');
}
function isBad(name) {
  const plain = name.toLowerCase().replace(/[^\p{L}]/gu, '');
  const norm = normalize(name);
  return BAD.some(w => plain.includes(w) || norm.includes(normalize(w)));
}
export function cleanName(raw) {
  if (typeof raw !== 'string') return null;
  const name = raw.replace(/[\u0000-\u001f\u007f]/g, '').replace(/\s+/g, ' ').trim().toLocaleUpperCase('uk');
  if (!NAME_RE.test(name) || isBad(name)) return null;
  return name;
}
const json = (data, status = 200) => new Response(JSON.stringify(data), {
  status,
  headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
});
async function readTop(kv) {
  try {
    const v = await kv.get('top', 'json');
    return Array.isArray(v) ? v : [];
  } catch (e) { return []; }
}
const view = (top, pid) => top.slice(0, SHOW).map(e => ({ n: e.n, s: e.s, z: e.z | 0, l: e.l | 0, me: !!pid && e.p === pid }));
const rankOf = (top, pid) => { const i = top.findIndex(e => e.p === pid); return i < 0 ? 0 : i + 1; };

export async function onRequestGet({ request, env }) {
  if (!env || !env.LEADERBOARD) return json({ ok: false, error: 'no_kv' }, 503);
  const pid = new URL(request.url).searchParams.get('pid') || '';
  const top = await readTop(env.LEADERBOARD);
  return json({ ok: true, top: view(top, PID_RE.test(pid) ? pid : ''), total: top.length, rank: PID_RE.test(pid) ? rankOf(top, pid) : 0 });
}

export async function onRequestPost({ request, env }) {
  if (!env || !env.LEADERBOARD) return json({ ok: false, error: 'no_kv' }, 503);
  let body;
  try { body = await request.json(); } catch (e) { return json({ ok: false, error: 'bad_json' }, 400); }
  const pid = String(body.pid || '');
  const name = cleanName(body.name);
  const score = Number(body.score);
  const dur = Math.max(0, Number(body.dur) || 0);
  if (!PID_RE.test(pid)) return json({ ok: false, error: 'bad_pid' }, 400);
  if (!name) return json({ ok: false, error: 'bad_name' }, 422);
  if (!Number.isInteger(score) || score <= 0 || score > MAX_SCORE) return json({ ok: false, error: 'bad_score' }, 422);
  if (score > 3000 + dur * MAX_RATE) return json({ ok: false, error: 'implausible' }, 422);

  const kv = env.LEADERBOARD;
  const ip = request.headers.get('cf-connecting-ip') || 'x';
  const rl = 'rl:' + ip;
  if (await kv.get(rl)) return json({ ok: false, error: 'slow_down' }, 429);
  await kv.put(rl, '1', { expirationTtl: 60 });

  const top = await readTop(kv);
  const i = top.findIndex(e => e.p === pid);
  const entry = { p: pid, n: name, s: score, z: Math.max(0, Math.min(9, body.zone | 0)), l: Math.max(0, Math.min(20, body.look | 0)), t: Date.now() };
  if (i >= 0) {
    if (score > top[i].s) top[i] = entry; else top[i].n = name;   // кращий результат лишається, ім'я оновлюється
  } else top.push(entry);
  top.sort((a, b) => b.s - a.s || a.t - b.t);
  const kept = top.slice(0, KEEP);
  await kv.put('top', JSON.stringify(kept));
  return json({ ok: true, rank: rankOf(kept, pid), top: view(kept, pid), total: kept.length });
}
