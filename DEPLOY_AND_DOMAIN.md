# Deploy, CI/CD & custom domain

Operational runbook for third-eye-events. Everything here is verified against
the live project (Cloudflare account `905a54b8…`, Pages project
`third-eye-events`).

---

## 1. How deploys work

The site is a static Astro build plus Cloudflare **Pages Functions**
(`functions/`) and a **D1** database. Deploys ship the built `dist/`:

```bash
npm run build
npx wrangler pages deploy dist --project-name=third-eye-events --branch main
```

- **Never** `npx wrangler deploy` — that is the *Workers* command and fails
  with "Missing entry-point to Worker script".
- **Never** add `[assets] directory = "./dist"` to `wrangler.toml` — Workers
  static assets do not route `functions/`, so `/api/enquiry` would 404.
- Production alias (always latest main): <https://third-eye-events.pages.dev>

### CI/CD

`.github/workflows/deploy.yml` runs on every push to `main` (and manually via
*workflow_dispatch*). It installs with `npm ci`, gates on both type-checks
(`astro check` for the site, `tsc -p tsconfig.functions.json` for the
Functions), builds, and deploys.

> The Pages project was created through the API with a GitHub source, but **no
> webhook is wired** — a bare `git push` changes nothing on the site. The
> workflow above is the only automatic deploy path.

### Required GitHub secrets

| Secret | Purpose |
| --- | --- |
| `CLOUDFLARE_API_TOKEN` | Pages deploy token (Cloudflare API token with *Cloudflare Pages — Edit*) |
| `CLOUDFLARE_ACCOUNT_ID` | `905a54b83934b6eefb57642b34996fd4` |

Optional (build-time only; the feature stays off while unset):

| Secret / variable | Purpose |
| --- | --- |
| `PUBLIC_TURNSTILE_SITE_KEY` | Pairs with the runtime `TURNSTILE_SECRET_KEY` Pages secret to switch on bot protection for the enquiry form |
| `PUBLIC_CF_BEACON_TOKEN` | Cloudflare Web Analytics beacon token (dashboard → Web Analytics → site → add site → copy the token) |

### Runtime Pages secrets (set with wrangler, not in git)

```bash
npx wrangler pages secret put ADMIN_TOKEN        # gates /admin (any long random string)
npx wrangler pages secret put TURNSTILE_SECRET_KEY # only when the site key above is set
# Resend — see §5 for the domain-verification step
npx wrangler pages secret put RESEND_API_KEY
npx wrangler pages secret put ENQUIRY_NOTIFY_EMAIL   # where enquiries land
npx wrangler pages secret put ENQUIRY_FROM_EMAIL     # optional; defaults to the branded sender
```

`.dev.vars` mirrors these for local `wrangler pages dev` — copy
`.dev.vars.example` and fill in. `.dev.vars` itself is gitignored.

---

## 2. Custom domain — `thirdeyeevents.com` — ✅ LIVE (verified 2026-10-22)

**Status:** both hostnames resolve and serve the site — apex `https://thirdeyeevents.com`
and `https://www.thirdeyeevents.com` return the real pages (title, JSON-LD,
CSP header all present), and Pages **Functions are routed on the custom domain**
(`POST /api/enquiry` → 422 on an invalid payload, `POST /api/admin/login` →
401 on a bad token, i.e. the same behaviour as the `pages.dev` alias).

The records that made it work (keep for reference — re-create them if the
domain ever needs re-validating):

| Type | Name | Content | Proxy |
| --- | --- | --- | --- |
| `A` | `@` | `192.0.2.1` | Proxied |
| `AAAA` | `@` | `100::` | Proxied |
| `CNAME` | `www` | `third-eye-events.pages.dev` | Proxied |

`192.0.2.1` / `100::` are Cloudflare's documented placeholder targets for a
proxied apex that only needs to point at Pages; the CNAME for `www` does the
real routing.

> Note: the wrangler OAuth token used for deploys has **no `Zone:DNS:Edit`
> scope**, so any *future* DNS change has to happen in the dashboard (or with a
> scoped API token) — `GET /zones/{id}/dns_records` fails with a `10000`
> authentication error even though the zone itself reads fine.

---

## 3. Remaining ops checklist

- [ ] **Resend — domain verification** (key + secrets are already wired; this is
      the last step). Add `thirdeyeevents.com` in the Resend dashboard and add
      the records it shows — see **§5**. Do **not** touch the root SPF record:
      Resend sends from the `send.` subdomain, which carries its own SPF, so the
      existing `v=spf1 include:secureserver.net -all` (GoDaddy mail) stays as is.
- [ ] **Turnstile** — set `PUBLIC_TURNSTILE_SITE_KEY` (build) *and*
      `TURNSTILE_SECRET_KEY` (runtime secret). The form works without them;
      they are what switches bot protection on.
- [ ] **Rate limiting** — the D1 windowed limiter fails open. A Cloudflare WAF
      rate-limit rule on `/api/enquiry` is the hardened backstop.
- [x] **Analytics — done 2026-10-22** — Google Analytics 4 (gtag.js,
      measurement ID `G-RTPB8265VC`) ships in every public page's head
      (single-sourced in `src/data/site.ts`), with ClientRouter-aware
      `page_view` tracking for virtual navigations. The bare (admin) layout
      is excluded. CSP allows `googletagmanager.com` (scripts, images) and
      `*.google-analytics.com` (connect, images). Cloudflare Web Analytics
      remains an optional alternative: set `PUBLIC_CF_BEACON_TOKEN` at build
      time to add the beacon alongside.
- [x] **Push path (SSH) — done 2026-10-22** — key pair
      `~/.ssh/thirdeye_ed25519` generated, registered on the thirdeyevedic
      account (GitHub key name "tew"), `~/.ssh/config` host alias `github-te`
      (github.com, that key only), `origin` = `github-te:thirdeyevedic/te.git`.
      The dead `github-pat` remote (revoked PAT embedded in its URL) has been
      **removed**. Other keys on this machine: `id_ed25519` (unregistered) and
      `cc_deploy_ed25519` (a read-only deploy key on this repo; GitHub
      authenticates it as `creativeclique/cc`).
- [x] **CI secrets — done 2026-10-22** — `CLOUDFLARE_API_TOKEN` and
      `CLOUDFLARE_ACCOUNT_ID` (`905a54b83934b6eefb57642b34996fd4`) are set as
      repository secrets (written via the Actions secrets API, libsodium
      sealed-box encrypted, after verifying the token with `wrangler whoami`).
      A dispatched run then went **green with the deploy step executing** —
      `Deploy to Cloudflare Pages: success` — and the site answered 200
      afterwards. CI now builds *and* deploys on every push to `main`.
      The workflow still degrades gracefully: if the secrets are ever removed
      the deploy step is skipped with an explicit `::warning::` rather than
      failing the run. *(Note: repo secrets can only be written via the
      GitHub API/UI with a repo-admin token — an SSH push key cannot.)*
- [x] **Mobile responsiveness — done 2026-10-22** (branch
      `mobile-responsive-pass`, merged to `main`). Fixed: dead mobile-menu
      scroll-lock (now `html.is-menu-open`), overlay `100dvh`, 10 undefined
      font vars, burger close bug (Escape/link-tap re-opened the menu),
      30×20px burger tap target, 30 venue-page grid overflows, cramped
      contact-form fields, oversized signature-entry cards, 404-ing nav
      links. Responsive images: `srcset`/`sizes` wired into
      `ExperienceImage.astro` (266 images; ~75% smaller phone payload).
      Verified: `mobile-probe.mjs` **76/76 routes clean at 360×800, 390×844,
      768×1024 and 1440×900** (0 failures, 0 warnings), desktop audit stays
      75/76, GA/CSP/entry-media probes green on live.

### Verified state (2026-10-22)

- **GitHub push works** — SSH key `thirdeye_ed25519` (registered as "tew") via
  host alias `github-te`; all commits pushed (`40cf508..f03b292`), local ==
  remote.
- **CI first runs** (`7d3a9ed`, `f03b292`): every step green — checkout,
  setup-node, `npm ci`, `astro check`, functions `tsc`, build. Only *Deploy to
  Cloudflare Pages* fails, because the two repo secrets below are unset. The
  repository itself is healthy.
- Full headless audit: **75/76 routes completely clean** on both
  `third-eye-events.pages.dev` and `thirdeyeevents.com`. The single finding is
  `/admin/`, which requires a login session (its render is separately
  verified: HTTP 200, login gate visible, CSP applied).
- Enquiry pipeline: submit → D1 → admin list → delete verified end-to-end on
  production. The database holds only the one archived spam enquiry.
- Admin API: login 200 + httpOnly cookie, wrong token 401, no cookie 401,
  list/PATCH/DELETE all verified live.
- CSP smoke test: 6/6 routes, zero violations. Media probe: 15/15 on both
  local and live.

---

## 4. Local development

```bash
npm run dev                      # Astro dev server
npm run preview:full             # build + wrangler pages dev with local D1
```

Local credentials live in a gitignored `.env` (mode 600) —
`CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, `GITHUB_TOKEN`, plus the
unused R2 keys kept commented out. Load them before any wrangler/API command:

```bash
set -a; . ./.env; set +a         # then: npm run deploy
```

`.env` is in `.gitignore` (line 11) and is never committed; CI uses the repo
secrets instead and does not read it.

`wrangler pages dev` uses its own **empty local D1**, separate from
`d1 migrations apply --local`. To exercise the API locally, run the migrations
against the same state dir first, or test against the deployed preview URL.

Verification harnesses live outside the repo in
`~/.workbuddy-ai/binaries/node/workspace` — `audit-site.mjs` (crawls every
built route at desktop), `csp-probe.mjs` (header + console check),
`entry-media-probe.mjs` (signature-entry dialog media wiring) and
`mobile-probe.mjs` (asserts per route at 360×800 / 390×844 / 768×1024 /
1440×900: horizontal overflow, viewport meta, console/request errors,
burger open→scroll-lock→Escape flow, ≥44px tap targets, font floor,
srcset presence, carousel snap, entry dialog).

```bash
# build once, then probe the static build
CODEBUDDY_SAFE_DELETE_ENABLED=0 npm run build
npx astro preview --port 4178          # NOTE: binds to localhost, not 127.0.0.1
find dist -name "*.html" | sed -E 's|^dist||; s|/index\.html$|/|; s|\.html$|/|; s|//+$|/|' > /tmp/pages.txt
env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy \
    -u ALL_PROXY -u all_proxy node ~/.workbuddy-ai/binaries/node/workspace/mobile-probe.mjs \
    http://localhost:4178 /tmp/pages.txt
```

`mobile-probe.mjs` replaces the stale `verify-mobile-nav.mjs` (its selectors
no longer exist). Flags: `--only <substring>` filters routes. Expected
desktop-audit finding is `/admin/` (needs a login session; excluded as
noise by the mobile probe along with the `/api/admin/` 401s).

> On this machine, wrangler and the headless browser both need the proxy env
> vars stripped: `env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy
> -u ALL_PROXY -u all_proxy …`

---

## 5. Enquiry email — Resend

**Status (2026-10-23):** key + all three secrets set; the account's sending
domain is **not yet verified**, so notifications are currently sent from
Resend's shared test sender to the account owner's address. One dashboard step
upgrades them to the branded address.

### Current configuration (live)

| Pages secret | Value | Notes |
| --- | --- | --- |
| `RESEND_API_KEY` | `re_…` (send-only scope) | cannot list domains or manage the account — sending only |
| `ENQUIRY_NOTIFY_EMAIL` | `thirdeyevedic@gmail.com` | the Resend account owner; **the only address Resend accepts before verification** |
| `ENQUIRY_FROM_EMAIL` | `Third Eye Events <onboarding@resend.dev>` | Resend's shared sender, allowed pre-verification |

Replies still go to the enquirer: the function sets `reply_to` to the
submitted address, so hitting Reply works regardless of the `from`.

### To finish — verify the domain

1. Resend dashboard → **Domains → Add Domain** → `thirdeyeevents.com`.
2. Add the records it shows in **Cloudflare DNS** (this zone is managed there).
   The standard set is:

   | Type | Name | Content | Proxy |
   | --- | --- | --- | --- |
   | `MX` | `send` | `feedback-smtp.<region>.amazonses.com` (priority 10) | DNS only |
   | `TXT` | `send` | `v=spf1 include:amazonses.com ~all` | DNS only |
   | `TXT` | `resend._domainkey` | `p=MIGfMA0GCS…` (per-domain DKIM key) | DNS only |

   **Copy the exact values from the dashboard** — the DKIM key is unique to the
   domain and the region differs per account. All three go on subdomains, so the
   root MX (GoDaddy `secureserver.net`) and root SPF are untouched. Leave the
   orange cloud **off** on these.
3. Wait for Resend to show **Verified** (usually minutes).
4. Swap the two secrets back to the branded pair:

   ```bash
   printf '%s' 'hello@thirdeyeevents.com' | npx wrangler pages secret put ENQUIRY_NOTIFY_EMAIL
   npx wrangler pages secret delete ENQUIRY_FROM_EMAIL   # falls back to the branded default
   ```

   `ENQUIRY_FROM_EMAIL` defaults to `Third Eye Events <enquiries@thirdeyeevents.com>`
   in code, so deleting the secret is the cleanest way to restore it.
5. Redeploy (`npm run deploy`) — Pages snapshots env at deploy time.

The DNS edit itself needs the **Cloudflare dashboard**: the deploy token has no
`Zone:DNS:Edit` scope (§2).

> **Why this matters:** email is best-effort and never fails a submission — D1
> is the source of truth and `/admin/` lists every enquiry. A Resend rejection
> is logged to `console.error` only, so check the Pages logs if notifications
> ever stop.

