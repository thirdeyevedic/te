-- Third Eye Events — enquiries
-- Apply: npx wrangler d1 migrations apply third-eye-db

CREATE TABLE IF NOT EXISTS enquiries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT,
  event_type TEXT,
  destination TEXT,
  guests TEXT,
  timeframe TEXT,
  vision TEXT,
  status TEXT NOT NULL DEFAULT 'new',
  user_agent TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_enquiries_created ON enquiries (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_enquiries_status ON enquiries (status);
