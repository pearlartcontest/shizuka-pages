/**
 * Shizuka Network — Gallery & 25s GIF Viewer Engine
 * Ultra-Fast, Mobile-First, Touch & Swipe Accelerated
 */

(function () {
    'use strict';

    const STREAM_SERVER = 'https://shizuka.fun';
    const BOT_USERNAME = 'select_1_bot';

    // Decode URL-safe base64 string
    function decodeBase64(str) {
        if (!str) return '';
        if (str.startsWith('http://') || str.startsWith('https://') || str.startsWith('tg://')) {
            return str;
        }
        try {
            let b64 = str.replace(/-/g, '+').replace(/_/g, '/');
            while (b64.length % 4) b64 += '=';
            return decodeURIComponent(
                Array.prototype.map.call(atob(b64), function (c) {
                    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
                }).join('')
            );
        } catch (e) {
            try {
                return atob(str.replace(/-/g, '+').replace(/_/g, '/'));
            } catch (err) {
                return str;
            }
        }
    }

    window.initGallery = function () {
        const params = new URLSearchParams(window.location.search);
        const rawImgs = params.get('imgs') || '';
        const rawTg = params.get('tg') || '';
        const key = params.get('key') || '';
        const channelHandle = params.get('ch') || 'SelectVault';

        // Decode Telegram redirect target
        let tgRedirectUrl = decodeBase64(rawTg);
        if (!tgRedirectUrl) {
            tgRedirectUrl = key
                ? `https://t.me/${BOT_USERNAME}?start=${encodeURIComponent(key)}`
                : 'https://t.me/c/3560354600';
        }

        // Fire analytics beacon
        if (key && STREAM_SERVER) {
            try {
                const beaconUrl = `${STREAM_SERVER}/analytics/img_view?key=${encodeURIComponent(key)}`;
                if (navigator.sendBeacon) {
                    navigator.sendBeacon(beaconUrl);
                } else {
                    fetch(beaconUrl, { method: 'GET', mode: 'no-cors', keepalive: true }).catch(function () {});
                }
            } catch (e) {}
        }

        // Parse image items
        const imgItems = rawImgs
            .split(',')
            .map(function (s) { return s.trim(); })
            .filter(function (s) { return s.length > 0; })
            .map(function (pair, idx) {
                const parts = pair.split(':');
                const id = parts[0];
                const hash = parts[1] || '';
                const url = hash
                    ? `${STREAM_SERVER}/img/${id}?hash=${hash}`
                    : `${STREAM_SERVER}/img/${id}`;
                return { id: id, hash: hash, url: url, index: idx };
            });

        // Elements
        const track = document.getElementById('sliderTrack');
        const counterEl = document.getElementById('galleryCounter');
        const dotsContainer = document.getElementById('dotsContainer');
        const ctaBtn = document.getElementById('ctaButton');
        const lightbox = document.getElementById('lightboxModal');
        const lightboxImg = document.getElementById('lightboxImg');
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const closeBtn = document.getElementById('closeBtn');

        // Set CTA button href
        if (ctaBtn) {
            ctaBtn.href = tgRedirectUrl;
        }

        const watchBtn = document.getElementById('watchVideoBtn');
        if (watchBtn && key) {
            watchBtn.href = `${STREAM_SERVER}/watch?key=${encodeURIComponent(key)}`;
            watchBtn.style.display = 'inline-flex';
        }

        if (closeBtn) {
            closeBtn.addEventListener('click', function () {
                window.location.href = tgRedirectUrl;
            });
        }

        if (!imgItems.length) {
            if (track) {
                track.innerHTML = '<div style="color:#888;padding:40px;text-align:center;width:100%;">No preview media available.</div>';
            }
            return;
        }

        let currentIndex = 0;
        const totalSlides = imgItems.length;

        // Render Slides
        track.innerHTML = '';
        if (dotsContainer) dotsContainer.innerHTML = '';

        imgItems.forEach(function (item, i) {
            const slide = document.createElement('div');
            slide.className = `slide ${i === 0 ? 'active' : 'inactive'}`;
            slide.dataset.index = i;

            // Check if first slide might be a 25s GIF preview
            const isFirstSlide = i === 0;
            if (isFirstSlide) {
                const badge = document.createElement('div');
                badge.className = 'badge-gif';
                badge.innerHTML = '<span>⚡</span> 25s CLIP';
                slide.appendChild(badge);
            }

            const img = document.createElement('img');
            img.src = item.url;
            img.alt = `Preview ${i + 1}`;
            img.loading = i < 2 ? 'eager' : 'lazy';

            slide.appendChild(img);
            track.appendChild(slide);

            // Click slide to open lightbox
            slide.addEventListener('click', function () {
                if (i === currentIndex && lightbox && lightboxImg) {
                    lightboxImg.src = item.url;
                    lightbox.classList.add('active');
                } else {
                    goToSlide(i);
                }
            });

            // Dot pill
            if (dotsContainer) {
                const dot = document.createElement('div');
                dot.className = `dot ${i === 0 ? 'active' : ''}`;
                dot.addEventListener('click', function () {
                    goToSlide(i);
                });
                dotsContainer.appendChild(dot);
            }
        });

        // Lightbox close
        if (lightbox) {
            lightbox.addEventListener('click', function () {
                lightbox.classList.remove('active');
            });
        }

        // Layout sizing and positions
        function updateLayout() {
            const stage = document.querySelector('.gallery-stage');
            if (!stage) return;

            const stageWidth = stage.clientWidth;
            const stageHeight = stage.clientHeight;
            const isMobile = window.innerWidth <= 768;

            // Aspect ratio calculation for portrait media
            const targetRatio = 9 / 16;
            let slideH = stageHeight * (isMobile ? 0.92 : 0.86);
            let slideW = slideH * targetRatio;

            if (slideW > stageWidth * 0.88) {
                slideW = stageWidth * (isMobile ? 0.86 : 0.65);
                slideH = slideW / targetRatio;
            }

            const spacing = isMobile ? 12 : 20;
            const slides = track.querySelectorAll('.slide');

            slides.forEach(function (s) {
                s.style.width = `${slideW}px`;
                s.style.height = `${slideH}px`;
                s.style.margin = `0 ${spacing / 2}px`;
            });

            // Center track on active slide
            const totalSlideUnit = slideW + spacing;
            const centerOffset = (stageWidth - slideW) / 2 - (spacing / 2);
            const translateX = centerOffset - (currentIndex * totalSlideUnit);

            track.style.transform = `translateX(${translateX}px)`;

            // Update active states
            slides.forEach(function (s, idx) {
                if (idx === currentIndex) {
                    s.classList.add('active');
                    s.classList.remove('inactive');
                } else {
                    s.classList.remove('active');
                    s.classList.add('inactive');
                }
            });

            // Update counter
            if (counterEl) {
                counterEl.innerHTML = `<span>${currentIndex + 1}</span> / ${totalSlides}`;
            }

            // Update dots
            if (dotsContainer) {
                const dots = dotsContainer.querySelectorAll('.dot');
                dots.forEach(function (d, idx) {
                    if (idx === currentIndex) {
                        d.classList.add('active');
                    } else {
                        d.classList.remove('active');
                    }
                });
            }
        }

        function goToSlide(index) {
            if (index < 0) index = 0;
            if (index >= totalSlides) index = totalSlides - 1;
            currentIndex = index;
            updateLayout();
        }

        // Arrow Controls
        if (prevBtn) {
            prevBtn.addEventListener('click', function () {
                goToSlide(currentIndex - 1);
            });
        }
        if (nextBtn) {
            nextBtn.addEventListener('click', function () {
                goToSlide(currentIndex + 1);
            });
        }

        // Keyboard Controls
        window.addEventListener('keydown', function (e) {
            if (e.key === 'ArrowLeft') goToSlide(currentIndex - 1);
            if (e.key === 'ArrowRight') goToSlide(currentIndex + 1);
            if (e.key === 'Escape' && lightbox) lightbox.classList.remove('active');
        });

        // Touch & Drag Gestures
        let startX = 0;
        let currentX = 0;
        let isDragging = false;
        let startTime = 0;

        function onTouchStart(e) {
            isDragging = true;
            track.classList.add('dragging');
            startX = e.type.includes('mouse') ? e.pageX : e.touches[0].clientX;
            currentX = startX;
            startTime = Date.now();
        }

        function onTouchMove(e) {
            if (!isDragging) return;
            currentX = e.type.includes('mouse') ? e.pageX : e.touches[0].clientX;
            const diffX = currentX - startX;

            const stage = document.querySelector('.gallery-stage');
            const stageWidth = stage.clientWidth;
            const isMobile = window.innerWidth <= 768;
            const targetRatio = 9 / 16;
            let slideH = stage.clientHeight * (isMobile ? 0.92 : 0.86);
            let slideW = slideH * targetRatio;
            const spacing = isMobile ? 12 : 20;
            const totalSlideUnit = slideW + spacing;
            const centerOffset = (stageWidth - slideW) / 2 - (spacing / 2);
            const baseTranslate = centerOffset - (currentIndex * totalSlideUnit);

            track.style.transform = `translateX(${baseTranslate + diffX}px)`;
        }

        function onTouchEnd() {
            if (!isDragging) return;
            isDragging = false;
            track.classList.remove('dragging');

            const diffX = currentX - startX;
            const elapsed = Date.now() - startTime;
            const velocity = Math.abs(diffX) / elapsed;

            // Swipe threshold or flick velocity
            if (diffX < -50 || (diffX < -20 && velocity > 0.4)) {
                goToSlide(currentIndex + 1);
            } else if (diffX > 50 || (diffX > 20 && velocity > 0.4)) {
                goToSlide(currentIndex - 1);
            } else {
                updateLayout();
            }
        }

        track.addEventListener('touchstart', onTouchStart, { passive: true });
        track.addEventListener('touchmove', onTouchMove, { passive: true });
        track.addEventListener('touchend', onTouchEnd);

        track.addEventListener('mousedown', onTouchStart);
        window.addEventListener('mousemove', onTouchMove);
        window.addEventListener('mouseup', onTouchEnd);

        window.addEventListener('resize', updateLayout);
        updateLayout();
    };
})();
