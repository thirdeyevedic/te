-- Third Eye Events — enquiry admin workflow
-- Apply: npx wrangler d1 migrations apply third-eye-db

ALTER TABLE enquiries ADD COLUMN notes TEXT;
ALTER TABLE enquiries ADD COLUMN updated_at TEXT;
