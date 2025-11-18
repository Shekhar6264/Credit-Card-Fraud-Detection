// Enhanced app.js with modern animations and interactions
class FraudDetectionApp {
    constructor() {
        this.init();
    }

    init() {
        this.initLoadingScreen();
        this.initAnimations();
        this.initCounters();
        this.initSwiper();
        this.initCanvasAnimation();
    }

    initLoadingScreen() {
        window.addEventListener('load', () => {
            const loadingScreen = document.getElementById('loadingScreen');
            if (loadingScreen) {
                setTimeout(() => {
                    loadingScreen.style.opacity = '0';
                    setTimeout(() => {
                        loadingScreen.style.display = 'none';
                    }, 500);
                }, 2000);
            }
        });
    }

    initAnimations() {
        // Add fade-in animations to elements
        const animatedElements = document.querySelectorAll('.feature-card, .hero-content, .hero-visual');
        animatedElements.forEach((el, index) => {
            el.style.animation = `fadeInUp 0.6s ease-out ${index * 0.2}s both`;
        });
    }

    initCounters() {
        const counters = document.querySelectorAll('.stat-number');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    counters.forEach(counter => {
                        this.animateCounter(counter);
                    });
                    observer.unobserve(entry.target);
                }
            });
        });

        const statsSection = document.querySelector('.hero-stats');
        if (statsSection) {
            observer.observe(statsSection);
        }
    }

    animateCounter(counter) {
        const target = +counter.getAttribute('data-target');
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;

        const updateCounter = () => {
            current += step;
            if (current < target) {
                counter.textContent = Math.floor(current).toLocaleString();
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target.toLocaleString();
            }
        };

        updateCounter();
    }

    initSwiper() {
        if (typeof Swiper !== 'undefined') {
            new Swiper(".mySwiper", {
                spaceBetween: 30,
                centeredSlides: true,
                autoplay: {
                    delay: 5000,
                    disableOnInteraction: false,
                },
                pagination: {
                    el: ".swiper-pagination",
                    clickable: true,
                },
                navigation: {
                    nextEl: ".swiper-button-next",
                    prevEl: ".swiper-button-prev",
                },
                effect: 'fade',
                fadeEffect: {
                    crossFade: true
                },
            });
        }
    }

    initCanvasAnimation() {
        const canvas = document.getElementById("canvas");
        if (!canvas) return;

        const gl = canvas.getContext("webgl");
        if (!gl) return;

        try {
            const programInfo = twgl.createProgramInfo(gl, ["vertexShader", "fragmentShader"]);

            const arrays = {
                position: [-1, -1, 0, 1, -1, 0, -1, 1, 0, -1, 1, 0, 1, -1, 0, 1, 1, 0],
            };
            const bufferInfo = twgl.createBufferInfoFromArrays(gl, arrays);

            let mouseX = 0, mouseY = 0;

            canvas.addEventListener('mousemove', e => {
                const rect = canvas.getBoundingClientRect();
                mouseX = e.clientX - rect.left;
                mouseY = e.clientY - rect.top;
            });

            const render = (time) => {
                twgl.resizeCanvasToDisplaySize(gl.canvas);

                gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);
                const uniforms = {
                    u_time: time * 0.001,
                    u_resolution: [gl.canvas.width, gl.canvas.height],
                    u_mouse: [mouseX, mouseY],
                };

                gl.useProgram(programInfo.program);
                twgl.setBuffersAndAttributes(gl, programInfo, bufferInfo);
                twgl.setUniforms(programInfo, uniforms);
                twgl.drawBufferInfo(gl, bufferInfo);

                requestAnimationFrame(render);
            };

            requestAnimationFrame(render);
        } catch (error) {
            console.warn('WebGL not supported, skipping canvas animation');
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FraudDetectionApp();
});

// Global function for dummy login
function submitDummyLogin() {
    const btn = event?.target;
    if (btn) {
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
        btn.disabled = true;
        
        setTimeout(() => {
            document.getElementById('dummyLoginForm').submit();
        }, 1500);
    } else {
        document.getElementById('dummyLoginForm').submit();
    }
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    .animate-in {
        animation: fadeInUp 0.6s ease-out forwards;
    }
`;
document.head.appendChild(style);