/// <reference types="@cloudflare/workers-types" />
/** POST /api/admin/logout — clears the admin session cookie. */
export const onRequestPost: PagesFunction = async () =>
  new Response(JSON.stringify({ ok: true }), {
    status: 200,
    headers: {
      "content-type": "application/json",
      "cache-control": "no-store",
      "set-cookie": "admin_session=; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=0",
    },
  });
