
-- Add password_hash to the existing users table.
-- Existing users will have NULL until they register a new password.

ALTER TABLE users
ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255);
