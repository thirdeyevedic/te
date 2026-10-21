/// <reference types="@cloudflare/workers-types" />
/**
 * POST /api/admin/login — Third Eye Events admin auth.
 * Verifies the shared ADMIN_TOKEN and sets an httpOnly session cookie.
 * (For stronger auth, put /admin behind Cloudflare Access.)
 */
interface Env {
  ADMIN_TOKEN?: string;
}

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

export const onRequestPost: PagesFunction<Env> = async ({ request, env }) => {
  const token = env.ADMIN_TOKEN;
  if (!token) return json({ ok: false, error: "not_configured" }, 503);

  let form: FormData;
  try {
    form = await request.formData();
  } catch {
    return json({ ok: false, error: "invalid_form" }, 400);
  }

  const supplied = typeof form.get("token") === "string" ? (form.get("token") as string).trim() : "";
  if (!supplied || !timingSafeEqual(supplied, token)) {
    return json({ ok: false, error: "unauthorized" }, 401);
  }

  return json({ ok: true }, 200, {
    "set-cookie": `admin_session=${encodeURIComponent(token)}; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=28800`,
  });
};
