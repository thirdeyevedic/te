/// <reference types="@cloudflare/workers-types" />
/**
 * /api/admin/enquiries — Third Eye Events admin API (guarded by the
 * admin_session cookie set by /api/admin/login).
 *   GET    ?status=&q=&limit=&offset=   list (or ?id= for one)
 *   PATCH  {id, status?, notes?}        update
 *   DELETE {id}                         remove
 */
interface Env {
  DB: D1Database;
  ADMIN_TOKEN?: string;
}

const STATUSES = ["new", "contacted", "qualified", "archived"] as const;
const isStatus = (v: string | null): v is (typeof STATUSES)[number] =>
  !!v && (STATUSES as readonly string[]).includes(v);

const json = (body: unknown, status = 200, extraHeaders: Record<string, string> = {}) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", "cache-control": "no-store", ...extraHeaders },
  });

function timingSafeEqual(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

function isAuthed(request: Request, env: Env): boolean {
  const token = env.ADMIN_TOKEN;
  if (!token) return false;
  const m = /(?:^|;\s*)admin_session=([^;]+)/.exec(request.headers.get("cookie") ?? "");
  return !!m && timingSafeEqual(decodeURIComponent(m[1]), token);
}

const str = (v: FormDataEntryValue | null): string | null => (typeof v === "string" ? v : null);

export const onRequestGet: PagesFunction<Env> = async ({ request, env }) => {
  if (!isAuthed(request, env)) return json({ ok: false, error: "unauthorized" }, 401);

  const url = new URL(request.url);
  const id = url.searchParams.get("id");
  if (id) {
    const row = await env.DB.prepare("SELECT * FROM enquiries WHERE id = ?").bind(Number(id)).first();
    return row ? json({ ok: true, enquiry: row }) : json({ ok: false, error: "not_found" }, 404);
  }

  const status = url.searchParams.get("status");
  const q = (url.searchParams.get("q") ?? "").trim();
  const limit = Math.min(Math.max(Number(url.searchParams.get("limit")) || 50, 1), 200);
  const offset = Math.max(Number(url.searchParams.get("offset")) || 0, 0);

  const where: string[] = [];
  const binds: string[] = [];
  if (isStatus(status)) { where.push("status = ?"); binds.push(status); }
  if (q) {
    where.push("(name LIKE ? OR email LIKE ? OR event_type LIKE ? OR destination LIKE ?)");
    const like = `%${q}%`;
    binds.push(like, like, like, like);
  }
  const whereSql = where.length ? `WHERE ${where.join(" AND ")}` : "";

  const countRow = await env.DB.prepare(`SELECT COUNT(*) AS n FROM enquiries ${whereSql}`).bind(...binds).first<{ n: number }>();
  const { results } = await env.DB.prepare(
    `SELECT id, name, email, phone, event_type, destination, guests, timeframe, vision, status, notes, created_at, updated_at
     FROM enquiries ${whereSql} ORDER BY created_at DESC LIMIT ? OFFSET ?`,
  )
    .bind(...binds, limit, offset)
    .all();

  return json({ ok: true, total: countRow?.n ?? 0, enquiries: results ?? [] });
};

export const onRequestPatch: PagesFunction<Env> = async ({ request, env }) => {
  if (!isAuthed(request, env)) return json({ ok: false, error: "unauthorized" }, 401);

  let form: FormData;
  try { form = await request.formData(); } catch { return json({ ok: false, error: "invalid_form" }, 400); }

  const id = Number(form.get("id"));
  if (!id) return json({ ok: false, error: "invalid_form" }, 400);

  const status = str(form.get("status"));
  const notes = str(form.get("notes"));

  const sets: string[] = [];
  const binds: (string | number)[] = [];
  if (isStatus(status)) { sets.push("status = ?"); binds.push(status); }
  if (notes !== null) { sets.push("notes = ?"); binds.push(notes.slice(0, 5000)); }
  if (!sets.length) return json({ ok: false, error: "nothing_to_update" }, 400);

  sets.push("updated_at = datetime('now')");
  binds.push(id);
  await env.DB.prepare(`UPDATE enquiries SET ${sets.join(", ")} WHERE id = ?`).bind(...binds).run();

  const row = await env.DB.prepare("SELECT * FROM enquiries WHERE id = ?").bind(id).first();
  return json({ ok: true, enquiry: row });
};

export const onRequestDelete: PagesFunction<Env> = async ({ request, env }) => {
  if (!isAuthed(request, env)) return json({ ok: false, error: "unauthorized" }, 401);

  let form: FormData;
  try { form = await request.formData(); } catch { return json({ ok: false, error: "invalid_form" }, 400); }

  const id = Number(form.get("id"));
  if (!id) return json({ ok: false, error: "invalid_form" }, 400);

  await env.DB.prepare("DELETE FROM enquiries WHERE id = ?").bind(id).run();
  return json({ ok: true });
};
