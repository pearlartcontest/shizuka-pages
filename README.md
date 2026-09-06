# Shizuka Network — Cloudflare Pages (`shizuka-pages`)

High-performance, 100% free edge infrastructure hosting the Shizuka Network:
1. **`img.shizuka.fun`**: High-definition image preview slider & 25s highlight clip viewer.
2. **`go.shizuka.fun`**: High-retention countdown relays (R1–R5) & Vault Locker.

## Architecture Benefits
- **$0/month hosting:** Zero server bills, hosted on Cloudflare's global edge network.
- **0 Popunder Ad Fatigue:** Zero spam redirects, no aggressive popups, no adblock detection locks.
- **Sub-50ms Global Latency:** 100% static assets pre-cached at edge nodes worldwide.
- **100% Backward Compatible:** Full support for legacy Blogger URLs (`/2026/06/collapse.html`, etc.) and modern clean paths (`/r1`, `/gallery`, `/vault`).

## Directory Structure
```
shizuka-pages/
├── public/
│   ├── index.html                   # Smart router (imgs= -> Gallery, d= -> Relay)
│   ├── gallery.html                 # Dedicated gallery view
│   ├── vault.html                   # Vault Locker landing page
│   ├── r1.html                      # Relay 1 (LTCM case study + 12s countdown)
│   ├── r2.html                      # Relay 2 (2008 Crash + 10s countdown)
│   ├── r3.html                      # Relay 3 (The Big Squeeze + 10s countdown)
│   ├── r4.html                      # Relay 4 (Black Wednesday Sterling + 10s countdown)
│   ├── r5.html                      # Relay 5 (Enron Collapse + 10s countdown)
│   ├── 2026/06/                     # Legacy Blogger URL mirrors
│   │   ├── collapse.html            # Legacy mirror -> R1
│   │   ├── crash.html               # Legacy mirror -> R2
│   │   ├── squeeze.html             # Legacy mirror -> R3
│   │   ├── sterling.html            # Legacy mirror -> R4
│   │   ├── enron.html               # Legacy mirror -> R5
│   │   └── vault.html               # Legacy mirror -> Vault
│   ├── css/
│   │   ├── luxury-theme.css         # Dark & Gold luxury design system
│   │   └── gallery.css              # Mobile-first touch swipe & GIF engine
│   ├── js/
│   │   ├── gallery.js               # Dynamic image & 25s GIF viewer with lightbox
│   │   └── relay-engine.js          # Countdown progression & sequence decoder
│   ├── _redirects                   # Cloudflare Pages routing aliases
│   └── _headers                     # CORS, security, and cache-control headers
├── build_pages.py                   # Static site compiler
├── package.json
└── README.md
```

## Cloudflare Dashboard Setup
1. In Cloudflare Dashboard -> **Compute (Workers & Pages)** -> **Create Application** -> **Pages**.
2. Connect to GitHub repository: `pearlartcontest/shizuka-pages`.
3. Set build configuration:
   - Framework preset: `None`
   - Build output directory: `public`
4. Deploy site!
5. In Project Settings -> **Custom Domains**:
   - Add `img.shizuka.fun`
   - Add `go.shizuka.fun`
   (Cloudflare automatically provisions the CNAME and SSL certificate).
