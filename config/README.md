# config

Configuration and secrets that must not be committed to git.

## Firebase credentials

1. In [Firebase Console](https://console.firebase.google.com): select your project.
2. Project settings (gear) → **Service accounts**.
3. **Generate new private key** and download the JSON file.
4. Save it here as: **`firebase-service-account.json`**.

This file is used by `app.core.firebase` to initialize the Admin SDK. Add it to `.gitignore` (e.g. `config/*.json` or `config/firebase-service-account.json`) and never commit it.

## .env

The application reads settings from a `.env` file in the project root (see `app.config`). Use the root `.env.example` as a template; do not put real secrets in `config/` unless you need extra config files (and keep those in `.gitignore`).

## Summary

| File | Purpose | In Git? |
|------|---------|--------|
| `firebase-service-account.json` | Firebase Admin SDK credentials | No |
| (optional) other `.json` / `.env` | Extra local config | No |
