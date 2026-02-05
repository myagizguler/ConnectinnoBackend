# utils

Shared helper functions and utilities.

## Purpose

- Pure or mostly pure functions used in several places (e.g. date formatting, slug generation, ID generation).
- Small helpers that don’t fit in `core` (which is for app-wide infrastructure like Firebase) or in a single `service`.

## Examples

- **IDs**: `generate_short_id()`, `nanoid`-style helpers.
- **Dates**: `utc_now()`, `format_firebase_timestamp()`.
- **Validation**: Custom validators used across models or services.
- **Encoding**: Hashing, encoding/decoding for tokens or URLs.

Avoid putting business logic here; keep that in `services` or `core`.
