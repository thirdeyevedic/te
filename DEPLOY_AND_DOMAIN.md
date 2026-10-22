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
# Resend, once the sending domain is verified:
npx wrangler pages secret put RESEND_API_KEY
npx wrangler pages secret put NOTIFY_EMAIL
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

- [ ] **Resend** — verify the sending domain in the Resend dashboard. When
      adding the SPF record, **merge it with the existing SPF record** (one
      `v=spf1` per domain; a second one breaks mail authentication).
- [ ] **Turnstile** — set `PUBLIC_TURNSTILE_SITE_KEY` (build) *and*
      `TURNSTILE_SECRET_KEY` (runtime secret). The form works without them;
      they are what switches bot protection on.
- [ ] **Rate limiting** — the D1 windowed limiter fails open. A Cloudflare WAF
      rate-limit rule on `/api/enquiry` is the hardened backstop.
- [ ] **Analytics** — set `PUBLIC_CF_BEACON_TOKEN` if traffic reporting is
      wanted. The beacon is absent from the bundle until then.
- [x] **Push path (SSH) — done 2026-10-22** — key pair
      `~/.ssh/thirdeye_ed25519` generated, registered on the thirdeyevedic
      account (GitHub key name "tew"), `~/.ssh/config` host alias `github-te`
      (github.com, that key only), `origin` = `github-te:thirdeyevedic/te.git`.
      All 11 local commits pushed (`40cf508..7d3a9ed`). Other keys on this
      machine: `id_ed25519` (unregistered) and `cc_deploy_ed25519` (a
      read-only deploy key on this repo; GitHub authenticates it as
      `creativeclique/cc`).
- [ ] **CI secrets** — the workflow needs `CLOUDFLARE_API_TOKEN` +
      `CLOUDFLARE_ACCOUNT_ID` as repository secrets (Settings → Secrets and
      variables → Actions). Without them the run fails at the deploy step
      only; the type-checks and build still prove the repo is healthy. Site
      deploys are unaffected either way — wrangler deploys directly.

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

`wrangler pages dev` uses its own **empty local D1**, separate from
`d1 migrations apply --local`. To exercise the API locally, run the migrations
against the same state dir first, or test against the deployed preview URL.

Verification harnesses live outside the repo in
`~/.workbuddy-ai/binaries/node/workspace` — `audit-site.mjs` (crawls every
built route), `csp-probe.mjs` (header + console check), `entry-media-probe.mjs`
(signature-entry dialog media wiring).

> On this machine, wrangler and the headless browser both need the proxy env
> vars stripped: `env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy
> -u ALL_PROXY -u all_proxy …`
