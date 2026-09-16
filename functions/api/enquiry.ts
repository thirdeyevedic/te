/// <reference types="@cloudflare/workers-types" />
/**
 * POST /api/enquiry — Third Eye Events
 *
 * Cloudflare Pages Function: validates the enquiry, stores it in D1
 * (source of truth), then best-effort notifies the team via Resend.
 *
 * ── SETUP (Phase 5 · deploy) ─────────────────────────────────────────
 * 1. Database:
 *      npx wrangler d1 create third-eye-db
 *      npx wrangler d1 migrations apply third-eye-db --remote
 *    Bind in Cloudflare Pages → Settings → Functions:
 *      D1 binding name: DB          → database third-eye-db
 * 2. Secrets (Pages → Settings → Environment variables):
 *      RESEND_API_KEY        re_...            (resend.com, free tier)
 *      ENQUIRY_NOTIFY_EMAIL  hello@thirdeyeevents.com
 *      TURNSTILE_SECRET_KEY  0x...             (optional — enables spam check)
 * 3. Local full-stack dev:
 *      npm run build && npx wrangler pages dev dist --d1 DB=third-eye-db
 * ─────────────────────────────────────────────────────────────────────
 */

interface Env {
  DB: D1Database;
  RESEND_API_KEY?: string;
  ENQUIRY_NOTIFY_EMAIL?: string;
  TURNSTILE_SECRET_KEY?: string;
}

const MAX = { name: 200, email: 320, phone: 40, event_type: 100, destination: 120, guests: 60, timeframe: 120, vision: 5000 } as const;

const clean = (v: FormDataEntryValue | null, limit: number): string =>
  typeof v === "string" ? v.trim().slice(0, limit) : "";

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });

/** A native (no-JavaScript) form post asks for HTML back. Replying with JSON
 *  dumps a bare `{"ok":true}` on a blank page — indistinguishable from a broken
 *  form. Redirect instead, so the visitor lands back on /contact/ with a result
 *  it can render (POST/Redirect/GET). 303 forces the follow-up to be a GET. */
const wantsHtml = (request: Request) =>
  (request.headers.get("accept") ?? "").includes("text/html");

const respond = (
  request: Request,
  payload: { ok: boolean; error?: string },
  status: number,
) =>
  wantsHtml(request)
    ? new Response(null, {
        status: 303,
        headers: { location: `/contact/?${payload.ok ? "sent=1" : `error=${payload.error ?? "network"}`}` },
      })
    : json(payload, status);

async function verifyTurnstile(token: string, ip: string | null, secret: string): Promise<boolean> {
  const res = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
    method: "POST",
    headers: { "content-type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ secret, response: token, ...(ip ? { remoteip: ip } : {}) }),
  });
  const data = (await res.json()) as { success: boolean };
  return data.success === true;
}

/** Escape a value before interpolating it into the notification email's HTML.
 *  Every field in `d` is submitter-controlled, so an unescaped value could
 *  inject markup — or a convincing fake link — into the team's inbox. */
const esc = (v: string): string =>
  v
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");

function notificationHtml(d: Record<string, string>): string {
  /* `alreadyHtml` is only ever passed values this function built itself. */
  const row = (label: string, value?: string, alreadyHtml = false) =>
    value
      ? `<tr><td style="padding:6px 14px 6px 0;color:#8a8580;font-size:13px;vertical-align:top">${label}</td><td style="padding:6px 0;color:#171717;font-size:14px">${alreadyHtml ? value : esc(value)}</td></tr>`
      : "";
  const emailCell = d.email ? `<a href="mailto:${esc(d.email)}">${esc(d.email)}</a>` : "";
  return `<div style="font-family:Georgia,serif;background:#F5F1E8;padding:32px">
  <p style="letter-spacing:.3em;font-size:11px;color:#B89B5E;margin:0 0 18px">THIRD EYE EVENTS</p>
  <h1 style="font-size:22px;font-weight:normal;margin:0 0 20px">New Enquiry — ${esc(d.event_type || "General")}</h1>
  <table style="border-collapse:collapse;margin-bottom:20px">
    ${row("Name", d.name)}${row("Email", emailCell, true)}
    ${row("Phone / WhatsApp", d.phone)}${row("Destination", d.destination)}
    ${row("Guests", d.guests)}${row("Timeframe", d.timeframe)}
  </table>
  ${d.vision ? `<p style="color:#8a8580;font-size:12px;letter-spacing:.2em;margin:0 0 8px">VISION</p><p style="white-space:pre-wrap;color:#171717;font-size:15px;line-height:1.7;border-left:2px solid #B89B5E;padding-left:16px">${esc(d.vision)}</p>` : ""}
</div>`;
}

export const onRequestPost: PagesFunction<Env> = async ({ request, env }) => {
  let form: FormData;
  try {
    form = await request.formData();
  } catch {
    return respond(request, { ok: false, error: "invalid_form" }, 400);
  }

  /* Honeypot — bots fill it, humans never see it */
  if (clean(form.get("company"), 100)) return respond(request, { ok: true }, 200);

  const data = {
    name: clean(form.get("name"), MAX.name),
    email: clean(form.get("email"), MAX.email).toLowerCase(),
    phone: clean(form.get("phone"), MAX.phone) || null,
    event_type: clean(form.get("event_type"), MAX.event_type) || null,
    destination: clean(form.get("destination"), MAX.destination) || null,
    guests: clean(form.get("guests"), MAX.guests) || null,
    timeframe: clean(form.get("timeframe"), MAX.timeframe) || null,
    vision: clean(form.get("vision"), MAX.vision) || null,
  };

  if (!data.name || !data.email || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(data.email)) {
    return json({ ok: false, error: "validation" }, 422);
  }

  /* Optional Turnstile gate */
  if (env.TURNSTILE_SECRET_KEY) {
    const token = clean(form.get("cf-turnstile-response"), 2048);
    const ok = await verifyTurnstile(token, request.headers.get("cf-connecting-ip"), env.TURNSTILE_SECRET_KEY);
    if (!ok) return json({ ok: false, error: "turnstile" }, 403);
  }

  /* D1 is the source of truth */
  try {
    await env.DB.prepare(
      `INSERT INTO enquiries (name, email, phone, event_type, destination, guests, timeframe, vision, user_agent)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
    )
      .bind(
        data.name,
        data.email,
        data.phone,
        data.event_type,
        data.destination,
        data.guests,
        data.timeframe,
        data.vision,
        request.headers.get("user-agent")?.slice(0, 300) ?? null,
      )
      .run();
  } catch (err) {
    console.error("D1 insert failed", err);
    return json({ ok: false, error: "storage" }, 500);
  }

  /* Best-effort email notification — never fails the request */
  if (env.RESEND_API_KEY && env.ENQUIRY_NOTIFY_EMAIL) {
    try {
      await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: {
          authorization: `Bearer ${env.RESEND_API_KEY}`,
          "content-type": "application/json",
        },
        body: JSON.stringify({
          from: "Third Eye Events <enquiries@thirdeyeevents.com>",
          to: [env.ENQUIRY_NOTIFY_EMAIL],
          reply_to: data.email,
          subject: `New Enquiry — ${data.event_type || "General"} · ${data.name}`,
          html: notificationHtml(data as Record<string, string>),
        }),
      });
    } catch (err) {
      console.error("Resend notify failed", err);
    }
  }

  return json({ ok: true });
};
