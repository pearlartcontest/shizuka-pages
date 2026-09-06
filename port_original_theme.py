import os, sys, re
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')

PAGES_DIR = r"S:\shizuka-stream\shizuka-pages\public"
BLOGGER_DIR = r"S:\shizuka-stream\Blogger"
THE_RS_DIR = os.path.join(BLOGGER_DIR, "The R's- shizukaredirect.blogspot.com", "last working! do not change this")

print("=== PORTING AUTHENTIC BLOGGER DESIGNS TO CLOUDFLARE PAGES ===")

# -------------------------------------------------------------
# 1. Port savemyimg.blogspot.com.txt -> index.html & gallery.html
# -------------------------------------------------------------
savemyimg_path = os.path.join(BLOGGER_DIR, "savemyimg.blogspot.com.txt")
with open(savemyimg_path, "r", encoding="utf-8") as f:
    s_raw = f.read()

# Extract CSS from b:skin
skin_match = re.search(r"<b:skin><!\[CDATA\[(.*?)\]\]></b:skin>", s_raw, re.DOTALL)
if not skin_match:
    print("ERROR: Could not find b:skin in savemyimg")
    sys.exit(1)
css_content = skin_match.group(1).strip()

# Extract the header, zoom overlay, viewer-wrapper, jump button precisely
header_html = re.search(r"<header>.*?</header>", s_raw, re.DOTALL).group(0)
zoom_raw = s_raw.split("<div id='zoomOverlay'>")[1].split("<!-- ======================================================================= AD Piller Left Start")[0]
zoom_html = "<div id='zoomOverlay'>" + zoom_raw.strip()

viewer_raw = s_raw.split("<div class='viewer-wrapper'>")[1].split("<div class='ad-container-720'>")[0]
viewer_html = "<div class='viewer-wrapper'>" + viewer_raw.strip()

jump_html = re.search(r"<button class='jump-button'.*?</button>", s_raw, re.DOTALL).group(0)

body_html = f"""
    {header_html}
    {zoom_html}
    {viewer_html}
    {jump_html}
"""

# Extract JavaScript
js_match = re.search(r"<script type='text/javascript'>\s*//<!\[CDATA\[(.*?)//\]\]>\s*</script>", s_raw, re.DOTALL)
if not js_match:
    print("ERROR: Could not find JS in savemyimg")
    sys.exit(1)
js_content = js_match.group(1).strip()
# Sanitize ID to cleanly handle any leading minus sign or symbols
js_content = js_content.replace(
    "const [id, hash] = pair.trim().split(':');",
    "const [rawId, hash] = pair.trim().split(':');\n                const id = rawId ? rawId.replace(/^[^\\d]+/, '') : '';"
)

# Build complete clean gallery page
gallery_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SHIZUKA | Images</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <script>
        (function() {{
            var host = window.location.hostname;
            var path = window.location.pathname;
            if (host === 'join.shizuka.fun' && (path === '/' || path === '/index.html' || path === '/index')) {{
                window.location.replace('/join' + window.location.search);
            }} else if (host === 'go.shizuka.fun' && (path === '/' || path === '/index.html' || path === '/index')) {{
                window.location.replace('/vault' + window.location.search);
            }}
        }})();
    </script>
    <style>
{css_content}
    </style>
</head>
<body>
    {body_html}

    <script type="text/javascript">
{js_content}
    </script>
</body>
</html>
"""

# Write to public/index.html & public/gallery.html
with open(os.path.join(PAGES_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(gallery_html)
with open(os.path.join(PAGES_DIR, "gallery.html"), "w", encoding="utf-8") as f:
    f.write(gallery_html)
print("SUCCESS: Ported authentic savemyimg design to index.html and gallery.html")


# -------------------------------------------------------------
# 2. Port Vault.txt -> vault.html & 2026/06/vault.html
# -------------------------------------------------------------
vault_path = os.path.join(THE_RS_DIR, "Vault.txt")
with open(vault_path, "r", encoding="utf-8") as f:
    v_raw = f.read()

# Strip all ad scripts, cond-ad elements, Monetag popunders, and turbulentrefreshments from Vault.txt
v_clean = re.sub(r"<script>atOptions=.*?</script>", "", v_raw, flags=re.DOTALL)
v_clean = re.sub(r"<script async data-cfasync=[\"']false[\"'] src=[\"']https?://turbulentrefreshments\.com.*?></script>", "", v_clean, flags=re.DOTALL)
v_clean = re.sub(r"<script src=[\"']https?://turbulentrefreshments\.com.*?></script>", "", v_clean, flags=re.DOTALL)
v_clean = re.sub(r"<script src=[\"']https?://.*?invoke\.js[\"']></script>", "", v_clean, flags=re.DOTALL)
v_clean = re.sub(r"<div class=[\"']cond-ad.*?</div>", "", v_clean, flags=re.DOTALL)
# Remove the conditional intrusive ad block
v_clean = re.sub(r"<script>\s*\(function\(\)\{\s*var HAS = new URLSearchParams.*?\}\)\(\);\s*</script>", "", v_clean, flags=re.DOTALL)

with open(os.path.join(PAGES_DIR, "vault.html"), "w", encoding="utf-8") as f:
    f.write(v_clean)
with open(os.path.join(PAGES_DIR, "2026", "06", "vault.html"), "w", encoding="utf-8") as f:
    f.write(v_clean)
print("SUCCESS: Ported authentic Vault design (zero ads) to vault.html and 2026/06/vault.html")


# -------------------------------------------------------------
# 3. Port R1.txt..R5.txt -> r1..r5.html & 2026/06/collapse..enron.html
# -------------------------------------------------------------
r_mapping = [
    ("R1.txt", "r1.html", "collapse.html"),
    ("R2.txt", "r2.html", "crash.html"),
    ("R3.txt", "r3.html", "squeeze.html"),
    ("R4.txt", "r4.html", "sterling.html"),
    ("R5.txt", "r5.html", "enron.html"),
]

for src_file, clean_route, legacy_route in r_mapping:
    r_path = os.path.join(THE_RS_DIR, src_file)
    with open(r_path, "r", encoding="utf-8") as f:
        r_raw = f.read()
    
    # Strip ads, popunders, smartlink opens, and fake adblock messages
    r_clean = re.sub(r"<script>atOptions=.*?</script>", "", r_raw, flags=re.DOTALL)
    r_clean = re.sub(r"<script src=[\"']https?://turbulentrefreshments\.com.*?></script>", "", r_clean, flags=re.DOTALL)
    r_clean = re.sub(r"<script src=[\"']https?://.*?invoke\.js[\"']></script>", "", r_clean, flags=re.DOTALL)
    r_clean = re.sub(r"<div class=[\"']cond-ad.*?</div>", "", r_clean, flags=re.DOTALL)
    r_clean = re.sub(r"<div id=[\"']adblock-message[\"'].*?</div>", "", r_clean, flags=re.DOTALL)
    # Remove smartlink popunder window.open
    r_clean = re.sub(r"window\.open\(['\"]https?://turbulentrefreshments\.com.*?['\"],\s*['\"]_blank['\"]\);", "", r_clean)
    
    with open(os.path.join(PAGES_DIR, clean_route), "w", encoding="utf-8") as f:
        f.write(r_clean)
    with open(os.path.join(PAGES_DIR, "2026", "06", legacy_route), "w", encoding="utf-8") as f:
        f.write(r_clean)
    print(f"SUCCESS: Ported {src_file} -> {clean_route} and 2026/06/{legacy_route}")

print("ALL AUTHENTIC TEMPLATES SUCCESSFULLY PORTED!")
