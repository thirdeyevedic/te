-- Third Eye Events — enquiry rate limiting
-- Apply: npx wrangler d1 migrations apply third-eye-db

CREATE TABLE IF NOT EXISTS enquiry_rate_limit (
  ip_hash TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_rl_ip_time ON enquiry_rate_limit (ip_hash, created_at DESC);
