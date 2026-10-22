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

## 2. Custom domain — `thirdeyeevents.com` (action required)

**Status:** the apex and `www` hostnames are attached to the Pages project but
sit at `status: pending` with the error **"CNAME record not set"**; the apex
currently serves a Cloudflare placeholder page.

The wrangler OAuth token used for deploys has **no `Zone:DNS:Edit` scope**, so
these records must be added in the dashboard (or with a scoped API token):

**Cloudflare dashboard → `thirdeyeevents.com` → DNS → Records**

| Type | Name | Content | Proxy |
| --- | --- | --- | --- |
| `A` | `@` | `192.0.2.1` | Proxied |
| `AAAA` | `@` | `100::` | Proxied |
| `CNAME` | `www` | `third-eye-events.pages.dev` | Proxied |

Then, once the records resolve, return to **Pages → `third-eye-events` →
Custom domains** and re-validate both hostnames. Cloudflare issues the
certificate automatically (usually minutes).

`192.0.2.1` / `100::` are Cloudflare's documented placeholder targets for a
proxied apex that only needs to point at Pages; the CNAME for `www` does the
real routing.

---

## 3. Remaining ops checklist

- [ ] **DNS records above** — the custom domain cannot go live without them.
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
- [ ] **Rotate the PAT** stored in `~/.git/config` for this repository.

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
