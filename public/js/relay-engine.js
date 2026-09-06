/**
 * Shizuka Network — High-Retention Relay Engine
 * Zero-Ad, Free Cloudflare Pages Sequential Content Locker
 */

(function () {
    'use strict';

    const STREAM_SERVER = 'https://shizuka.fun';
    const BOT_USERNAME = 'select_1_bot';

    // Route map for R1-R5 sequence
    const RELAY_ROUTES = {
        'R1': '/2026/06/collapse.html',
        'R2': '/2026/06/crash.html',
        'R3': '/2026/06/squeeze.html',
        'R4': '/2026/06/sterling.html',
        'R5': '/2026/06/enron.html'
    };

    // Helper: decode URL-safe base64 JSON payload
    function decodePayload(encoded) {
        if (!encoded) return null;
        try {
            let base64 = encoded.replace(/-/g, '+').replace(/_/g, '/');
            while (base64.length % 4) {
                base64 += '=';
            }
            const jsonStr = decodeURIComponent(
                Array.prototype.map.call(atob(base64), function (c) {
                    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
                }).join('')
            );
            return JSON.parse(jsonStr);
        } catch (e) {
            try {
                return JSON.parse(atob(encoded.replace(/-/g, '+').replace(/_/g, '/')));
            } catch (err) {
                console.error('[RelayEngine] Failed to decode payload:', err);
                return null;
            }
        }
    }

    // Helper: encode URL-safe base64 JSON payload
    function encodePayload(key, seq) {
        const json = JSON.stringify({ k: key, s: seq });
        return btoa(unescape(encodeURIComponent(json)))
            .replace(/\+/g, '-')
            .replace(/\//g, '_')
            .replace(/=/g, '');
    }

    // Helper: send analytics beacon
    function sendAnalytics(key, step) {
        if (!key || !STREAM_SERVER) return;
        const beaconUrl = `${STREAM_SERVER}/analytics/relay?key=${encodeURIComponent(key)}&step=${encodeURIComponent(step)}`;
        try {
            if (navigator.sendBeacon) {
                navigator.sendBeacon(beaconUrl);
            } else {
                fetch(beaconUrl, { method: 'GET', mode: 'no-cors', keepalive: true }).catch(function () {});
            }
        } catch (e) {}
    }

    window.initRelayStep = function (options) {
        const stepId = options.step || 'R1';
        const duration = options.duration || 12; // default 12s

        const params = new URLSearchParams(window.location.search);
        const encoded = params.get('d');
        const payload = decodePayload(encoded);

        const actionZone = document.getElementById('action-zone');
        const barFill = document.getElementById('bar-fill');
        const countdownEl = document.getElementById('countdown');
        const btnWrap = document.getElementById('btn-wrap');
        const actionBtn = document.getElementById('btn-action');

        if (!actionZone || !barFill) return;

        // Reveal action zone
        actionZone.classList.remove('hidden');

        // Log step entry analytics
        if (payload && payload.k) {
            sendAnalytics(payload.k, stepId);
        }

        // Start countdown timer
        let timeLeft = duration;
        if (countdownEl) countdownEl.innerText = timeLeft;

        // Smooth GPU transition on bar
        barFill.style.transition = `width ${duration}s linear`;
        setTimeout(function () {
            barFill.style.width = '100%';
        }, 80);

        const timerInterval = setInterval(function () {
            timeLeft--;
            if (countdownEl) countdownEl.innerText = timeLeft;

            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                revealButton();
            }
        }, 1000);

        function revealButton() {
            if (!btnWrap || !actionBtn) return;
            btnWrap.classList.remove('hidden');
            setTimeout(function () {
                btnWrap.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 100);
        }

        // Handle button click & navigate next
        if (actionBtn) {
            actionBtn.addEventListener('click', function (e) {
                e.preventDefault();

                if (!payload || !payload.s || payload.s.length === 0) {
                    // Terminal step reached: return to Telegram bot to deliver video
                    const targetKey = payload ? payload.k : '';
                    const redirectUrl = targetKey
                        ? `https://t.me/${BOT_USERNAME}?start=${encodeURIComponent(targetKey)}`
                        : `https://t.me/${BOT_USERNAME}`;
                    window.location.href = redirectUrl;
                    return;
                }

                // Sequence has items: pop current step
                const nextStep = payload.s[0];
                const remainingSeq = payload.s.slice(1);
                const nextPayloadEncoded = encodePayload(payload.k, remainingSeq);

                const nextRoute = RELAY_ROUTES[nextStep] || RELAY_ROUTES['R2'];
                window.location.href = `${nextRoute}?d=${encodeURIComponent(nextPayloadEncoded)}`;
            });
        }
    };
})();
