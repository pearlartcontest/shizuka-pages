import sys
import os
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SRC_DIR = r"S:\shizuka-stream\Blogger\The R's- shizukaredirect.blogspot.com\Working before you fucked up!"
OUT_DIR = r"S:\shizuka-stream\shizuka-pages\public"

PAGES_CONFIG = [
    {
        "src": "R1.txt",
        "step": "R1",
        "duration": 12,
        "clean_name": "r1.html",
        "legacy_name": "collapse.html",
        "btn_text": "Continue to Part 2 &rarr;"
    },
    {
        "src": "R2.txt",
        "step": "R2",
        "duration": 10,
        "clean_name": "r2.html",
        "legacy_name": "crash.html",
        "btn_text": "Continue &rarr;"
    },
    {
        "src": "R3.txt",
        "step": "R3",
        "duration": 10,
        "clean_name": "r3.html",
        "legacy_name": "squeeze.html",
        "btn_text": "Continue &rarr;"
    },
    {
        "src": "R4.txt",
        "step": "R4",
        "duration": 10,
        "clean_name": "r4.html",
        "legacy_name": "sterling.html",
        "btn_text": "Continue &rarr;"
    },
    {
        "src": "R5.txt",
        "step": "R5",
        "duration": 10,
        "clean_name": "r5.html",
        "legacy_name": "enron.html",
        "btn_text": "Unlock Full Access &rarr;"
    },
]

RELAY_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>__TITLE__</title>
    <meta name="description" content="Capital Case Files editorial archive. Verified document delivery network.">
    <link rel="stylesheet" href="/css/luxury-theme.css">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💎</text></svg>">
</head>
<body>
    <div class="page-wrapper">
        <header class="header-brand">
            <div class="brand-badge">
                <span></span> SHIZUKA NETWORK
            </div>
            <div class="brand-channel">
                <a href="https://t.me/select_1_bot" target="_blank" rel="noopener">@select_1_bot</a>
            </div>
        </header>

        <span class="article-tag">CAPITAL CASE FILES &nbsp;&middot;&nbsp; ARCHIVE</span>
        <h1>__H1__</h1>
        <div class="byline">__BYLINE__</div>

        <!-- ── ZERO-AD COUNTDOWN ACTION ZONE ── -->
        <div id="action-zone" class="action-zone">
            <div class="phase-label">VERIFYING SECURE TOKEN &mdash; <span id="countdown" class="countdown-number">__DURATION__</span>s</div>
            <div class="bar-track">
                <div id="bar-fill" class="bar-fill"></div>
            </div>
            <div id="btn-wrap" class="btn-wrap hidden">
                <button id="btn-action" class="action-btn btn-solid">__BTN_TEXT__</button>
            </div>
        </div>

        <!-- ── EDITORIAL CONTENT ── -->
        <article class="article-content">
            __BODY_CONTENT__
        </article>

        <footer class="article-footer">
            Capital Case Files &nbsp;&middot;&nbsp; All case studies are drawn from public record and presented for educational purposes only.<br>
            Protected by Shizuka Global Edge Network.
        </footer>
    </div>

    <script src="/js/relay-engine.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            window.initRelayStep({
                step: '__STEP__',
                duration: __DURATION__
            });
        });
    </script>
</body>
</html>
"""

VAULT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>__TITLE__</title>
    <meta name="description" content="Capital Case Files editorial archive. Verified document delivery network.">
    <link rel="stylesheet" href="/css/luxury-theme.css">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💎</text></svg>">
    <style>
        .vault-hero {
            text-align: center;
            padding: 32px 20px;
            background: #0e0e0e;
            border: 1px solid rgba(212, 175, 55, 0.35);
            border-radius: 14px;
            margin-bottom: 40px;
            box-shadow: 0 16px 40px rgba(0,0,0,0.7);
        }
        .vault-badge {
            font-family: var(--font-ui);
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 3px;
            color: var(--gold);
            text-transform: uppercase;
            margin-bottom: 12px;
        }
        .vault-title {
            font-family: var(--font-heading);
            font-size: 26px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 10px;
        }
        .vault-sub {
            font-family: var(--font-ui);
            font-size: 13.5px;
            color: #888;
            margin-bottom: 28px;
        }
        .vault-btns {
            display: flex;
            flex-direction: column;
            gap: 14px;
            max-width: 420px;
            margin: 0 auto;
        }
        .btn-preview-cta {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            height: 52px;
            background: linear-gradient(135deg, #e8c659 0%, var(--gold) 50%, var(--gold-dark) 100%);
            color: #000;
            font-family: var(--font-ui);
            font-weight: 800;
            font-size: 13px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            border-radius: 10px;
            text-decoration: none;
            box-shadow: 0 6px 24px rgba(212, 175, 55, 0.35);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .btn-preview-cta:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 32px rgba(212, 175, 55, 0.55);
        }
        .btn-unlock-cta {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            height: 48px;
            background: transparent;
            color: #ccc;
            border: 1px solid #333;
            font-family: var(--font-ui);
            font-weight: 600;
            font-size: 12px;
            letter-spacing: 1px;
            text-transform: uppercase;
            border-radius: 10px;
            text-decoration: none;
            transition: border-color 0.2s, color 0.2s;
        }
        .btn-unlock-cta:hover {
            border-color: var(--gold);
            color: var(--gold);
        }
    </style>
</head>
<body>
    <div class="page-wrapper">
        <header class="header-brand">
            <div class="brand-badge">
                <span></span> SHIZUKA VAULT
            </div>
            <div class="brand-channel">
                <a href="https://t.me/select_1_bot" target="_blank" rel="noopener">@select_1_bot</a>
            </div>
        </header>

        <!-- ── VAULT LOCKER HERO ── -->
        <section class="vault-hero">
            <div class="vault-badge">VERIFIED MEDIA ARCHIVE</div>
            <h2 class="vault-title">Select Vault Preview & Access</h2>
            <p class="vault-sub">Choose an option below to preview highlights or unlock full release.</p>

            <div class="vault-btns">
                <a href="#" id="btn-preview" class="btn-preview-cta">
                    VIEW PREVIEW GALLERY & 25s CLIP ⚡
                </a>
                <a href="#" id="btn-unlock" class="btn-unlock-cta">
                    Unlock Full Video in HD 🍿
                </a>
            </div>
        </section>

        <span class="article-tag">CAPITAL CASE FILES &nbsp;&middot;&nbsp; SPECIAL REPORT</span>
        <h1>__H1__</h1>
        <div class="byline">__BYLINE__</div>

        <article class="article-content">
            __BODY_CONTENT__
        </article>

        <footer class="article-footer">
            Capital Case Files &nbsp;&middot;&nbsp; All case studies are drawn from public record and presented for educational purposes only.<br>
            Protected by Shizuka Global Edge Network.
        </footer>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            var params = new URLSearchParams(window.location.search);
            var previewEncoded = params.get('preview');
            var postEncoded = params.get('post');
            var keyParam = params.get('key');
            var STREAM_SERVER = 'https://shizuka.fun';

            function decodeVal(val) {
                if (!val) return '';
                if (val.startsWith('http://') || val.startsWith('https://') || val.startsWith('tg://')) return val;
                try {
                    var b64 = val.replace(/-/g, '+').replace(/_/g, '/');
                    while (b64.length % 4) b64 += '=';
                    return decodeURIComponent(escape(atob(b64)));
                } catch(e) { return val; }
            }

            var previewBtn = document.getElementById('btn-preview');
            var unlockBtn = document.getElementById('btn-unlock');

            var targetPreviewUrl = decodeVal(previewEncoded);
            var targetUnlockUrl = decodeVal(postEncoded);

            if (targetPreviewUrl) {
                previewBtn.href = targetPreviewUrl;
            } else if (keyParam) {
                previewBtn.href = '/?key=' + encodeURIComponent(keyParam);
            } else {
                previewBtn.style.display = 'none';
            }

            if (targetUnlockUrl) {
                unlockBtn.href = targetUnlockUrl;
            } else if (keyParam) {
                unlockBtn.href = 'https://t.me/select_1_bot?start=' + encodeURIComponent(keyParam);
            } else {
                unlockBtn.href = 'https://t.me/select_1_bot';
            }

            // Analytics beacon
            try {
                if (navigator.sendBeacon) {
                    navigator.sendBeacon(STREAM_SERVER + '/analytics/traffic?source=S&action=view');
                } else {
                    fetch(STREAM_SERVER + '/analytics/traffic?source=S&action=view', { method: 'GET', mode: 'no-cors', keepalive: true }).catch(function() {});
                }
            } catch(e) {}
        });
    </script>
</body>
</html>
"""

def clean_body(raw_html):
    m_h1 = re.search(r'<h1>(.*?)</h1>', raw_html, re.DOTALL)
    h1 = m_h1.group(1).strip() if m_h1 else 'Capital Case Files'

    m_title = re.search(r'<title>(.*?)</title>', raw_html, re.DOTALL)
    title = m_title.group(1).strip() if m_title else h1

    m_byline = re.search(r'<div class="byline">(.*?)</div>', raw_html, re.DOTALL)
    byline = m_byline.group(1).strip() if m_byline else '<b>Capital Case Files</b> &middot; Editorial'

    elements = re.findall(r'(<h2>.*?</h2>|<p>.*?</p>|<div class="pull-quote">.*?</div>)', raw_html, re.DOTALL)
    clean_elements = []
    for el in elements:
        if 'cond-ad' in el or 'action-zone' in el or 'adblock' in el or 'phase' in el:
            continue
        clean_elements.append(el)

    return title, h1, byline, "\n    ".join(clean_elements)

def generate_relay_page(cfg):
    src_path = os.path.join(SRC_DIR, cfg["src"])
    with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
        raw_html = f.read()

    title, h1, byline, body_content = clean_body(raw_html)

    html = RELAY_TEMPLATE.replace("__TITLE__", title) \
                          .replace("__H1__", h1) \
                          .replace("__BYLINE__", byline) \
                          .replace("__DURATION__", str(cfg["duration"])) \
                          .replace("__BTN_TEXT__", cfg["btn_text"]) \
                          .replace("__BODY_CONTENT__", body_content) \
                          .replace("__STEP__", cfg["step"])

    clean_path = os.path.join(OUT_DIR, cfg["clean_name"])
    with open(clean_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated clean: {clean_path}")

    legacy_path = os.path.join(OUT_DIR, "2026", "06", cfg["legacy_name"])
    with open(legacy_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated legacy mirror: {legacy_path}")

def generate_vault_page():
    src_path = os.path.join(SRC_DIR, "Vault.txt")
    with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
        raw_html = f.read()

    title, h1, byline, body_content = clean_body(raw_html)

    html = VAULT_TEMPLATE.replace("__TITLE__", title) \
                         .replace("__H1__", h1) \
                         .replace("__BYLINE__", byline) \
                         .replace("__BODY_CONTENT__", body_content)

    clean_path = os.path.join(OUT_DIR, "vault.html")
    with open(clean_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated clean: {clean_path}")

    legacy_path = os.path.join(OUT_DIR, "2026", "06", "vault.html")
    with open(legacy_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated legacy mirror: {legacy_path}")

if __name__ == '__main__':
    for cfg in PAGES_CONFIG:
        generate_relay_page(cfg)
    generate_vault_page()
    print("All pages successfully built!")
