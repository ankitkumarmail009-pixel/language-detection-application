// Enhanced Scroll Animations - Elements start visible, then animate on scroll
    function initializeAnimations() {
        // Add smooth scroll behavior
        document.documentElement.style.scrollBehavior = 'smooth';
        
        // Function to check if element is in viewport
        function isInViewport(element) {
            const rect = element.getBoundingClientRect();
            return (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.right <= (window.innerWidth || document.documentElement.clientWidth)
            );
        }
        
        // Enhanced Intersection Observer with better options
        const observerOptions = {
            threshold: 0.15,
            rootMargin: '0px 0px -50px 0px'
        };
        
        // Main scroll observer for fade-in animations
        const scrollObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    // Add staggered delay for multiple elements
                    setTimeout(() => {
                        entry.target.classList.add('visible');
                    }, index * 100); // Stagger by 100ms
                    
                    // Stop observing once animated
                    scrollObserver.unobserve(entry.target);
                }
            });
        }, observerOptions);
        
        // Observe all elements with scroll animation classes
        const scrollElements = document.querySelectorAll(
            '.dynamic-content, .scroll-fade-in, .scroll-slide-left, .scroll-slide-right, .scroll-scale-in, .scroll-rotate-in, .prediction-card, .dynamic-stat, .mode-card'
        );
        
        scrollElements.forEach((el, index) => {
            // Check if element is already in viewport - if so, keep it visible
            if (isInViewport(el)) {
                el.classList.add('visible');
                return; // Skip animation setup for elements already visible
            }
            
            // Add animate-on-scroll class to enable animation
            if (el.classList.contains('dynamic-content')) {
                el.classList.add('animate-on-scroll');
            }
            
            // Add scroll-fade-in class if not already present
            if (!el.classList.contains('scroll-fade-in') && 
                !el.classList.contains('scroll-slide-left') && 
                !el.classList.contains('scroll-slide-right') &&
                !el.classList.contains('scroll-scale-in') &&
                !el.classList.contains('scroll-rotate-in')) {
                el.classList.add('scroll-fade-in');
                el.classList.add('animate-on-scroll');
            } else {
                el.classList.add('animate-on-scroll');
            }
            
            scrollObserver.observe(el);
        });
        
        // Special handling for stat cards - alternate left/right
        document.querySelectorAll('.dynamic-stat').forEach((stat, index) => {
            if (isInViewport(stat)) {
                stat.classList.add('visible');
                return;
            }
            stat.classList.remove('scroll-fade-in');
            stat.classList.add('animate-on-scroll');
            if (index % 2 === 0) {
                stat.classList.add('scroll-slide-left');
            } else {
                stat.classList.add('scroll-slide-right');
            }
            scrollObserver.observe(stat);
        });
        
        // Mode cards with scale animation (if they exist)
        const modeCards = document.querySelectorAll('.mode-card');
        if (modeCards.length > 0) {
            modeCards.forEach((card, index) => {
                if (isInViewport(card)) {
                    card.classList.add('visible');
                    return;
                }
                card.classList.remove('scroll-fade-in');
                card.classList.add('scroll-scale-in');
                card.classList.add('animate-on-scroll');
                scrollObserver.observe(card);
            });
        }
        
        // Prediction cards with rotate animation
        document.querySelectorAll('.prediction-card').forEach((card) => {
            if (isInViewport(card)) {
                card.classList.add('visible');
                return;
            }
            card.classList.remove('scroll-fade-in');
            card.classList.add('scroll-rotate-in');
            card.classList.add('animate-on-scroll');
            scrollObserver.observe(card);
        });
        
        // Clean up any leftover mode card elements (if any exist)
        document.querySelectorAll('.clickable-mode-card').forEach(card => {
            card.style.display = 'none';
        });
        
        // Enhanced hover effect to stat cards
        document.querySelectorAll('.dynamic-stat').forEach(stat => {
            stat.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-3px) scale(1.02)';
            });
            stat.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });
        
        // Real-time character counter animation
        const textAreas = document.querySelectorAll('textarea');
        textAreas.forEach(textarea => {
            textarea.addEventListener('input', function() {
                // Trigger animation on parent stat cards
                const stats = document.querySelectorAll('.dynamic-stat');
                stats.forEach(stat => {
                    stat.style.animation = 'none';
                    setTimeout(() => {
                        stat.style.animation = 'fadeInUp 0.3s ease-out';
                    }, 10);
                });
            });
        });
        
        // Dynamic Background Color Changes
        if (!window.bgColorInterval) {
            let colorIndex = 0;
            const backgroundColors = [
                'linear-gradient(-45deg, #f8f9fa, #e8f4f8, #f0f5ff, #fff5f0)',
                'linear-gradient(-45deg, #fff5f0, #f8f9fa, #e8f4f8, #f0f5ff)',
                'linear-gradient(-45deg, #f0f5ff, #fff5f0, #f8f9fa, #e8f4f8)',
                'linear-gradient(-45deg, #e8f4f8, #f0f5ff, #fff5f0, #f8f9fa)'
            ];
            
            function changeBackgroundColor() {
                const app = document.querySelector('.stApp');
                if (app) {
                    colorIndex = (colorIndex + 1) % backgroundColors.length;
                    app.style.background = backgroundColors[colorIndex];
                    app.style.backgroundSize = '400% 400%';
                }
            }
            
            // Change background color every 8 seconds
            window.bgColorInterval = setInterval(changeBackgroundColor, 8000);
        }
        
        // Dynamic Mode Card Color Changes (if cards exist)
        const modeCards = document.querySelectorAll('.mode-card');
        if (modeCards.length > 0) {
            modeCards.forEach((card, index) => {
                const colorSets = [
                    ['#fff0f5', '#ffe0e6'],
                    ['#e6f3ff', '#cce6ff'],
                    ['#f0fff4', '#e0ffe0'],
                    ['#fff5e6', '#ffe6cc'],
                    ['#f5e6ff', '#e6ccff']
                ];
                
                // Clear any existing interval
                if (card.dataset.intervalId) {
                    clearInterval(parseInt(card.dataset.intervalId));
                }
                
                const intervalId = setInterval(() => {
                    if (document.body.contains(card)) {
                        const colors = colorSets[index % colorSets.length];
                        card.style.background = `linear-gradient(135deg, ${colors[0]} 0%, ${colors[1]} 100%)`;
                    } else {
                        clearInterval(intervalId);
                    }
                }, 3000 + (index * 500));
                
                card.dataset.intervalId = intervalId;
            });
        }
        
        // Parallax effect on scroll (subtle)
        let lastScrollTop = 0;
        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const scrollDirection = scrollTop > lastScrollTop ? 'down' : 'up';
            lastScrollTop = scrollTop;
            
            // Add subtle parallax to header
            const header = document.querySelector('.main-header');
            if (header) {
                const parallaxSpeed = 0.5;
                header.style.transform = `translateY(${scrollTop * parallaxSpeed}px)`;
            }
            
            // Animate stats on scroll
            const stats = document.querySelectorAll('.dynamic-stat');
            stats.forEach((stat, index) => {
                const rect = stat.getBoundingClientRect();
                const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
                if (isVisible) {
                    const scrollProgress = Math.min(1, Math.max(0, (window.innerHeight - rect.top) / window.innerHeight));
                    stat.style.transform = `translateY(${-5 * scrollProgress}px) scale(${1 + 0.05 * scrollProgress})`;
                }
            });
        }, { passive: true });
        
        // Add continuous rotation to icons
        const iconInterval = setInterval(() => {
            const icons = document.querySelectorAll('.mode-icon');
            if (icons.length > 0) {
                icons.forEach((icon, index) => {
                    const rotation = (Date.now() / 1000 + index) * 10 % 360;
                    icon.style.transform = `rotate(${rotation}deg) scale(${1 + Math.sin(Date.now() / 500 + index) * 0.1})`;
                });
            }
        }, 50);
        
        // Add alt text and aria-labels to tabs
        function addTabAccessibility() {
            // Find all tab elements
            const tabs = document.querySelectorAll('[data-baseweb="tab"], [role="tab"], button[data-baseweb="tab"]');
            
            tabs.forEach((tab, index) => {
                const tabText = tab.textContent.trim();
                
                // Define tab purposes based on text content
                const tabPurposes = {
                    'Language Detection': 'Detect the language of your text input using AI-powered analysis',
                    'Translator': 'Translate text between over 500 languages with automatic language detection',
                    'Guessing Game': 'Test your language knowledge by guessing the language of displayed text',
                    'Batch Analysis': 'Analyze multiple texts at once for efficient language detection',
                    'Compare Texts': 'Compare two texts side-by-side to see their detected languages and probabilities',
                    'Detection': 'Identify the language of your text using machine learning',
                    'Translation': 'Convert text from one language to another',
                    'Game': 'Play an interactive language guessing game',
                    'Batch': 'Process multiple texts in a single operation',
                    'Compare': 'Side-by-side comparison of two text samples'
                };
                
                // Find matching purpose
                let purpose = '';
                for (const [key, value] of Object.entries(tabPurposes)) {
                    if (tabText.includes(key) || tabText.toLowerCase().includes(key.toLowerCase())) {
                        purpose = value;
                        break;
                    }
                }
                
                // If no match found, create a generic description
                if (!purpose) {
                    purpose = `Switch to ${tabText} mode - ${tabText.includes('Detection') ? 'Detect languages in your text' : tabText.includes('Translator') || tabText.includes('Translation') ? 'Translate text between languages' : tabText.includes('Game') ? 'Play language guessing game' : tabText.includes('Batch') ? 'Analyze multiple texts' : tabText.includes('Compare') ? 'Compare two texts' : 'Access this feature'}`;
                }
                
                // Add aria-label and title attributes
                if (!tab.getAttribute('aria-label')) {
                    tab.setAttribute('aria-label', purpose);
                }
                if (!tab.getAttribute('title')) {
                    tab.setAttribute('title', purpose);
                }
                
                // Add aria-describedby for additional context
                const tabId = tab.id || `tab-${index}`;
                if (!tab.id) {
                    tab.id = tabId;
                }
            });
            
            // Also add to tab panels
            const tabPanels = document.querySelectorAll('[data-baseweb="tab-panel"], [role="tabpanel"]');
            tabPanels.forEach((panel, index) => {
                const associatedTab = document.querySelector(`[aria-controls="${panel.id}"], [data-baseweb="tab"][aria-selected="true"]`);
                if (associatedTab) {
                    const tabText = associatedTab.textContent.trim();
                    const purpose = `Content panel for ${tabText} - ${tabText.includes('Detection') ? 'Enter text to detect its language' : tabText.includes('Translator') || tabText.includes('Translation') ? 'Enter text to translate between languages' : tabText.includes('Game') ? 'Play the language guessing game' : tabText.includes('Batch') ? 'Enter multiple texts to analyze' : tabText.includes('Compare') ? 'Enter two texts to compare' : 'Main content area'}`;
                    
                    if (!panel.getAttribute('aria-label')) {
                        panel.setAttribute('aria-label', purpose);
                    }
                    if (!panel.getAttribute('title')) {
                        panel.setAttribute('title', purpose);
                    }
                }
            });
        }
        
        // Run immediately and on DOM changes
        addTabAccessibility();
        
        // Re-run when tabs are added/changed
        const tabObserver = new MutationObserver(() => {
            addTabAccessibility();
        });
        
        // Observe the document for tab changes
        tabObserver.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['aria-selected', 'class']
        });
        
        // Also run periodically to catch dynamically added tabs
        setInterval(addTabAccessibility, 1000);
        
        // Format mode dropdown to show only mode name in selected value
        function formatModeDropdown() {
            const selectbox = document.querySelector('[key="mode_dropdown"]') || 
                             document.querySelector('.stSelectbox[key*="mode"]') ||
                             document.querySelectorAll('.stSelectbox')[0];
            
            if (selectbox) {
                const selectedDiv = selectbox.querySelector('div > div > div');
                if (selectedDiv && selectedDiv.textContent.includes(' - ')) {
                    const modeName = selectedDiv.textContent.split(' - ')[0].trim();
                    // Only update if it's different to avoid infinite loops
                    if (selectedDiv.textContent !== modeName) {
                        selectedDiv.setAttribute('data-full-text', selectedDiv.textContent);
                        selectedDiv.textContent = modeName;
                    }
                }
            }
            
            // Format dropdown options to show descriptions nicely
            const options = document.querySelectorAll('[data-baseweb="option"]');
            options.forEach(option => {
                const text = option.textContent;
                if (text && text.includes(' - ')) {
                    const [modeName, description] = text.split(' - ');
                    option.innerHTML = `
                        <span style="font-weight: 600; color: inherit;">${modeName}</span>
                        <span style="font-size: 0.85rem; color: #666666; margin-left: 0.5rem; font-weight: 400;">${description}</span>
                    `;
                }
            });
        }
        
        // Run on load and periodically
        formatModeDropdown();
        setInterval(formatModeDropdown, 500);
        
        // Also run when dropdown opens/closes
        const dropdownObserver = new MutationObserver(() => {
            formatModeDropdown();
        });
        dropdownObserver.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['aria-expanded', 'aria-selected']
        });
        
        // Close dropdown menu when scrolling
        let scrollCloseTimeout;
        let lastScrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        function closeDropdownOnScroll() {
            // Clear any existing timeout
            clearTimeout(scrollCloseTimeout);
            
            // Close dropdown immediately on scroll
            scrollCloseTimeout = setTimeout(() => {
                // Find all open selectboxes
                const selectboxes = document.querySelectorAll('[data-baseweb="select"]');
                selectboxes.forEach(select => {
                    if (select.getAttribute('aria-expanded') === 'true') {
                        // Close the selectbox
                        select.setAttribute('aria-expanded', 'false');
                        select.blur();
                        
                        // Trigger escape key to close dropdown
                        const escapeEvent = new KeyboardEvent('keydown', {
                            key: 'Escape',
                            code: 'Escape',
                            keyCode: 27,
                            bubbles: true
                        });
                        select.dispatchEvent(escapeEvent);
                    }
                });
                
                // Close any open popovers (dropdown menus)
                const popovers = document.querySelectorAll('[data-baseweb="popover"]');
                popovers.forEach(popover => {
                    const style = window.getComputedStyle(popover);
                    if (style.display !== 'none' && style.visibility !== 'hidden') {
                        popover.style.display = 'none';
                        popover.style.visibility = 'hidden';
                        popover.setAttribute('aria-hidden', 'true');
                    }
                });
                
                // Close any open menus
                const menus = document.querySelectorAll('[data-baseweb="menu"]');
                menus.forEach(menu => {
                    const style = window.getComputedStyle(menu);
                    if (style.display !== 'none' && style.visibility !== 'hidden') {
                        menu.style.display = 'none';
                        menu.style.visibility = 'hidden';
                    }
                });
                
                // Also close virtual dropdowns
                const virtualDropdowns = document.querySelectorAll('[data-testid="stSelectboxVirtualDropdown"]');
                virtualDropdowns.forEach(dropdown => {
                    dropdown.style.display = 'none';
                });
            }, 50); // Very short delay for smooth UX
        }
        
        // Add scroll event listener with throttling
        let scrollThrottle;
        window.addEventListener('scroll', function() {
            const currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            // Only close if actually scrolling (not just a tiny movement)
            if (Math.abs(currentScrollTop - lastScrollTop) > 5) {
                closeDropdownOnScroll();
                lastScrollTop = currentScrollTop;
            }
            
            // Throttle the scroll handler
            clearTimeout(scrollThrottle);
            scrollThrottle = setTimeout(() => {
                lastScrollTop = window.pageYOffset || document.documentElement.scrollTop;
            }, 100);
        }, { passive: true });
        
        // Also close on touchmove for mobile
        window.addEventListener('touchmove', function() {
            closeDropdownOnScroll();
        }, { passive: true });
        
        // Close on wheel events (mouse wheel scrolling)
        window.addEventListener('wheel', function() {
            closeDropdownOnScroll();
        }, { passive: true });
        
        // ============================================
        // ITERATION 1-7: COMPREHENSIVE UX ENHANCEMENTS
        // ============================================
        
        // Enhanced Performance Monitoring
        function optimizePerformance() {
            // Use requestAnimationFrame for smooth animations
            let rafId;
            function updateAnimations() {
                // Batch DOM reads/writes
                rafId = requestAnimationFrame(updateAnimations);
            }
            updateAnimations();
        }
        
        // Smart Lazy Loading for Images
        function lazyLoadImages() {
            const images = document.querySelectorAll('img[data-src]');
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        imageObserver.unobserve(img);
                    }
                });
            });
            images.forEach(img => imageObserver.observe(img));
        }
        
        // Enhanced Error Handling
        window.addEventListener('error', function(e) {
            console.error('Application error:', e.error);
            // Could send to error tracking service
        });
        
        // Smart Debouncing for Expensive Operations
        function debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }
        
        // Enhanced Form Validation with Real-time Feedback
        function enhanceFormValidation() {
            const forms = document.querySelectorAll('form, .stTextInput, .stTextArea');
            forms.forEach(form => {
                const inputs = form.querySelectorAll('input, textarea');
                inputs.forEach(input => {
                    input.addEventListener('input', debounce(function() {
                        if (this.validity.valid) {
                            this.style.borderColor = 'var(--success)';
                            this.style.boxShadow = '0 0 0 3px rgba(82, 196, 26, 0.1)';
                        } else if (this.value) {
                            this.style.borderColor = 'var(--error)';
                            this.style.boxShadow = '0 0 0 3px rgba(255, 77, 79, 0.1)';
                        }
                    }, 300));
                });
            });
        }
        
        // Smart Content Loading
        function smartContentLoading() {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('loaded');
                        observer.unobserve(entry.target);
                    }
                });
            }, { rootMargin: '50px' });
            
            document.querySelectorAll('.prediction-card, .dynamic-stat').forEach(el => {
                observer.observe(el);
            });
        }
        
        // Enhanced Keyboard Shortcuts
        function addKeyboardShortcuts() {
            document.addEventListener('keydown', function(e) {
                // Ctrl/Cmd + K to focus search/input
                if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                    e.preventDefault();
                    const firstInput = document.querySelector('input, textarea');
                    if (firstInput) {
                        firstInput.focus();
                        firstInput.select();
                    }
                }
                
                // Escape to close modals/dropdowns
                if (e.key === 'Escape') {
                    closeDropdownOnScroll();
                }
            });
        }
        
        // Smart Scroll Restoration
        function smartScrollRestoration() {
            let scrollPosition = sessionStorage.getItem('scrollPosition');
            if (scrollPosition) {
                window.scrollTo(0, parseInt(scrollPosition));
                sessionStorage.removeItem('scrollPosition');
            }
            
            window.addEventListener('beforeunload', function() {
                sessionStorage.setItem('scrollPosition', window.pageYOffset);
            });
        }
        
        // Enhanced Touch Gestures
        function addTouchGestures() {
            let touchStartY = 0;
            let touchEndY = 0;
            
            document.addEventListener('touchstart', function(e) {
                touchStartY = e.changedTouches[0].screenY;
            }, { passive: true });
            
            document.addEventListener('touchend', function(e) {
                touchEndY = e.changedTouches[0].screenY;
                // Swipe down to close dropdowns
                if (touchStartY - touchEndY < -50) {
                    closeDropdownOnScroll();
                }
            }, { passive: true });
        }
        
        // Professional Loading States
        function enhanceLoadingStates() {
            const observer = new MutationObserver(() => {
                document.querySelectorAll('.stSpinner').forEach(spinner => {
                    if (!spinner.classList.contains('enhanced')) {
                        spinner.classList.add('enhanced');
                        const loadingText = document.createElement('div');
                        loadingText.className = 'loading-text';
                        loadingText.textContent = 'Processing...';
                        loadingText.style.cssText = 'margin-top: 0.75rem; color: #6366f1; font-weight: 500; text-align: center; font-size: 0.9rem;';
                        spinner.appendChild(loadingText);
                    }
                });
            });
            observer.observe(document.body, { childList: true, subtree: true });
        }
        
        // Smart Caching for Better Performance
        function implementSmartCaching() {
            // Cache frequently accessed elements
            window.elementCache = {
                predictionCards: null,
                dynamicStats: null,
                buttons: null,
                getPredictionCards: function() {
                    if (!this.predictionCards) {
                        this.predictionCards = document.querySelectorAll('.prediction-card');
                    }
                    return this.predictionCards;
                },
                getDynamicStats: function() {
                    if (!this.dynamicStats) {
                        this.dynamicStats = document.querySelectorAll('.dynamic-stat');
                    }
                    return this.dynamicStats;
                },
                clear: function() {
                    this.predictionCards = null;
                    this.dynamicStats = null;
                    this.buttons = null;
                }
            };
        }
        
        // Enhanced Accessibility Features
        function enhanceAccessibility() {
            // Add skip to main content link
            if (!document.querySelector('.skip-to-main')) {
                const skipLink = document.createElement('a');
                skipLink.href = '#main-content';
                skipLink.className = 'skip-to-main';
                skipLink.textContent = 'Skip to main content';
                skipLink.style.cssText = `
                    position: absolute;
                    top: -40px;
                    left: 0;
                    background: var(--accent-primary);
                    color: white;
                    padding: 8px 16px;
                    text-decoration: none;
                    z-index: 1000;
                    border-radius: 4px;
                `;
                skipLink.addEventListener('focus', function() {
                    this.style.top = '0';
                });
                skipLink.addEventListener('blur', function() {
                    this.style.top = '-40px';
                });
                document.body.insertBefore(skipLink, document.body.firstChild);
            }
            
            // Add main content landmark
            const mainContent = document.querySelector('.main');
            if (mainContent && !mainContent.id) {
                mainContent.id = 'main-content';
                mainContent.setAttribute('role', 'main');
            }
            
            // Enhance ARIA labels
            document.querySelectorAll('button, [role="button"]').forEach(btn => {
                if (!btn.getAttribute('aria-label') && !btn.textContent.trim()) {
                    btn.setAttribute('aria-label', 'Button');
                }
            });
        }
        
        // Professional Error Recovery
        function addErrorRecovery() {
            window.addEventListener('unhandledrejection', function(e) {
                console.error('Unhandled promise rejection:', e.reason);
                // Could show user-friendly error message
            });
        }
        
        // Smart Resize Handling
        function handleResize() {
            let resizeTimeout;
            window.addEventListener('resize', function() {
                clearTimeout(resizeTimeout);
                resizeTimeout = setTimeout(function() {
                    // Recalculate layouts
                    window.elementCache?.clear();
                    formatModeDropdown();
                }, 250);
            }, { passive: true });
        }
        
        // Enhanced Visual Feedback System
        function addVisualFeedback() {
            // Add ripple effect to all buttons
            document.querySelectorAll('button, [role="button"]').forEach(button => {
                if (!button.classList.contains('ripple-added')) {
                    button.classList.add('ripple-added');
                    button.addEventListener('click', function(e) {
                        const ripple = document.createElement('span');
                        const rect = this.getBoundingClientRect();
                        const size = Math.max(rect.width, rect.height);
                        const x = e.clientX - rect.left - size / 2;
                        const y = e.clientY - rect.top - size / 2;
                        
                        ripple.style.cssText = `
                            position: absolute;
                            width: ${size}px;
                            height: ${size}px;
                            left: ${x}px;
                            top: ${y}px;
                            background: rgba(255, 255, 255, 0.5);
                            border-radius: 50%;
                            transform: scale(0);
                            animation: ripple 0.6s ease-out;
                            pointer-events: none;
                        `;
                        
                        this.style.position = 'relative';
                        this.style.overflow = 'hidden';
                        this.appendChild(ripple);
                        
                        setTimeout(() => ripple.remove(), 600);
                    });
                }
            });
        }
        
        // Professional Analytics & Tracking (placeholder)
        function trackUserInteractions() {
            // Track important user actions
            document.querySelectorAll('.stButton > button, [data-baseweb="tab"]').forEach(element => {
                element.addEventListener('click', function() {
                    // Could send analytics event
                    console.log('User interaction:', this.textContent || this.getAttribute('aria-label'));
                });
            });
        }
        
        // Initialize all enhancements
        optimizePerformance();
        lazyLoadImages();
        enhanceFormValidation();
        smartContentLoading();
        addKeyboardShortcuts();
        smartScrollRestoration();
        addTouchGestures();
        enhanceLoadingStates();
        implementSmartCaching();
        enhanceAccessibility();
        addErrorRecovery();
        handleResize();
        addVisualFeedback();
        trackUserInteractions();
        
        // ============================================
        // ITERATION 1-3: ENHANCED UX INTERACTIONS
        // ============================================
        
        // Improve form field interactions
        function enhanceFormFields() {
            const textAreas = document.querySelectorAll('textarea');
            const textInputs = document.querySelectorAll('input[type="text"]');
            
            // Add character counter to textareas
            textAreas.forEach(textarea => {
                if (!textarea.parentElement.querySelector('.char-counter')) {
                    const counter = document.createElement('div');
                    counter.className = 'char-counter';
                    counter.style.cssText = 'text-align: right; color: #666; font-size: 0.85rem; margin-top: 0.25rem;';
                    textarea.parentElement.appendChild(counter);
                    
                    function updateCounter() {
                        const length = textarea.value.length;
                        counter.textContent = `${length} characters`;
                        if (length > 1000) {
                            counter.style.color = '#ff4d4f';
                        } else if (length > 500) {
                            counter.style.color = '#faad14';
                        } else {
                            counter.style.color = '#666';
                        }
                    }
                    
                    textarea.addEventListener('input', updateCounter);
                    updateCounter();
                }
            });
            
            // Add focus animations
            [...textAreas, ...textInputs].forEach(field => {
                field.addEventListener('focus', function() {
                    this.parentElement.style.transform = 'scale(1.01)';
                });
                
                field.addEventListener('blur', function() {
                    this.parentElement.style.transform = 'scale(1)';
                });
            });
        }
        
        enhanceFormFields();
        
        // Professional Toast Notification System
        function showToast(message, type = 'info') {
            const toast = document.createElement('div');
            toast.className = `toast toast-${type}`;
            toast.textContent = message;
            toast.style.cssText = `
                position: fixed;
                bottom: 2rem;
                right: 2rem;
                background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#6366f1'};
                color: white;
                padding: 1rem 1.5rem;
                border-radius: 10px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.2);
                z-index: 10000;
                animation: slideInUp 0.3s ease-out;
                max-width: 300px;
                font-weight: 500;
            `;
            document.body.appendChild(toast);
            setTimeout(() => {
                toast.style.animation = 'slideOutDown 0.3s ease-out';
                setTimeout(() => toast.remove(), 300);
            }, 3000);
        }
        
        // Add toast animations
        if (!document.querySelector('#toast-styles')) {
            const style = document.createElement('style');
            style.id = 'toast-styles';
            style.textContent = `
                @keyframes slideInUp {
                    from { transform: translateY(100px); opacity: 0; }
                    to { transform: translateY(0); opacity: 1; }
                }
                @keyframes slideOutDown {
                    from { transform: translateY(0); opacity: 1; }
                    to { transform: translateY(100px); opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }
        
        // Enhanced Copy to Clipboard Functionality
        function addCopyToClipboard() {
            document.querySelectorAll('.language-badge, .prediction-card').forEach(element => {
                if (!element.classList.contains('copy-enabled')) {
                    element.classList.add('copy-enabled');
                    element.style.cursor = 'pointer';
                    element.setAttribute('title', 'Click to copy');
                    element.addEventListener('click', function() {
                        const text = this.textContent || this.innerText;
                        navigator.clipboard.writeText(text).then(() => {
                            showToast('Copied to clipboard!', 'success');
                        }).catch(() => {
                            showToast('Failed to copy', 'error');
                        });
                    });
                }
            });
        }
        
        // Professional Loading Progress Indicator
        function addLoadingProgress() {
            const progressBar = document.createElement('div');
            progressBar.id = 'loading-progress';
            progressBar.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 0%;
                height: 3px;
                background: var(--gradient-primary);
                z-index: 10000;
                transition: width 0.3s ease;
                box-shadow: 0 2px 4px rgba(99, 102, 241, 0.25);
            `;
            document.body.appendChild(progressBar);
            
            // Simulate progress on page interactions
            let progress = 0;
            const interval = setInterval(() => {
                if (progress < 90) {
                    progress += 10;
                    progressBar.style.width = progress + '%';
                } else {
                    clearInterval(interval);
                    setTimeout(() => {
                        progressBar.style.width = '100%';
                        setTimeout(() => progressBar.style.opacity = '0', 200);
                    }, 100);
                }
            }, 100);
        }
        
        // Smart Content Preloading
        function preloadCriticalContent() {
            // Preload fonts
            const fontLink = document.createElement('link');
            fontLink.rel = 'preload';
            fontLink.as = 'font';
            fontLink.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap';
            fontLink.crossOrigin = 'anonymous';
            document.head.appendChild(fontLink);
        }
        
        // Enhanced Error Boundary
        function setupErrorBoundary() {
            window.addEventListener('error', function(e) {
                console.error('Error caught:', e.error);
                // Could show user-friendly error message
                if (e.error && e.error.message) {
                    showToast('An error occurred. Please refresh the page.', 'error');
                }
            });
        }
        
        // Professional Analytics Events
        function trackAnalytics(event, data) {
            // Placeholder for analytics tracking
            console.log('Analytics Event:', event, data);
            // Could integrate with Google Analytics, Mixpanel, etc.
        }
        
        // Enhanced User Experience Tracking
        function trackUXMetrics() {
            // Track page load time
            window.addEventListener('load', function() {
                const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
                trackAnalytics('page_load', { time: loadTime });
            });
            
            // Track user interactions
            document.addEventListener('click', function(e) {
                const target = e.target.closest('button, [role="button"], [data-baseweb="tab"]');
                if (target) {
                    trackAnalytics('user_interaction', {
                        type: 'click',
                        element: target.textContent || target.getAttribute('aria-label')
                    });
                }
            });
        }
        
        // Professional Feature Detection
        function detectFeatures() {
            const features = {
                touch: 'ontouchstart' in window,
                webgl: !!document.createElement('canvas').getContext('webgl'),
                serviceWorker: 'serviceWorker' in navigator,
                localStorage: typeof Storage !== 'undefined'
            };
            
            // Adjust UI based on features
            if (!features.localStorage) {
                console.warn('LocalStorage not available');
            }
        }
        
        // Enhanced Performance Monitoring
        function monitorPerformance() {
            if ('PerformanceObserver' in window) {
                const observer = new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        if (entry.entryType === 'measure') {
                            console.log('Performance:', entry.name, entry.duration);
                        }
                    }
                });
                observer.observe({ entryTypes: ['measure', 'navigation'] });
            }
        }
        
        // Professional Content Security
        function enhanceSecurity() {
            // Add CSP headers (would be in server config, but adding client-side checks)
            // Validate inputs client-side
            document.querySelectorAll('input, textarea').forEach(input => {
                input.addEventListener('input', function() {
                    // Basic XSS prevention
                    if (this.value.includes('<script>') || this.value.includes('javascript:')) {
                        this.value = this.value.replace(/<script>/gi, '').replace(/javascript:/gi, '');
                        showToast('Potentially unsafe content removed', 'warning');
                    }
                });
            });
        }
        
        // Initialize all professional features
        addCopyToClipboard();
        addLoadingProgress();
        preloadCriticalContent();
        setupErrorBoundary();
        trackUXMetrics();
        detectFeatures();
        monitorPerformance();
        enhanceSecurity();
        
        // Improve button feedback
        function enhanceButtonFeedback() {
            document.querySelectorAll('.stButton > button').forEach(button => {
                button.addEventListener('click', function(e) {
                    // Create ripple effect
                    const ripple = document.createElement('span');
                    const rect = this.getBoundingClientRect();
                    const size = Math.max(rect.width, rect.height);
                    const x = e.clientX - rect.left - size / 2;
                    const y = e.clientY - rect.top - size / 2;
                    
                    ripple.style.cssText = `
                        position: absolute;
                        width: ${size}px;
                        height: ${size}px;
                        left: ${x}px;
                        top: ${y}px;
                        background: rgba(255, 255, 255, 0.5);
                        border-radius: 50%;
                        transform: scale(0);
                        animation: ripple 0.6s ease-out;
                        pointer-events: none;
                    `;
                    
                    this.style.position = 'relative';
                    this.style.overflow = 'hidden';
                    this.appendChild(ripple);
                    
                    setTimeout(() => ripple.remove(), 600);
                });
            });
        }
        
        // Add ripple animation
        if (!document.querySelector('#ripple-style')) {
            const style = document.createElement('style');
            style.id = 'ripple-style';
            style.textContent = `
                @keyframes ripple {
                    to {
                        transform: scale(4);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
        
        enhanceButtonFeedback();
        
        // Loading states are already handled by the earlier enhanceLoadingStates function
        
        // Improve error handling display
        function enhanceErrorDisplay() {
            document.querySelectorAll('.stError, .stWarning, .stSuccess, .stInfo').forEach(alert => {
                alert.style.animation = 'smoothFadeIn 0.4s ease-out';
            });
        }
        
        enhanceErrorDisplay();
        
        // Add smooth scroll to top button
        function addScrollToTop() {
            if (document.querySelector('.scroll-to-top')) return;
            
            const button = document.createElement('button');
            button.className = 'scroll-to-top';
            button.innerHTML = '↑';
            button.setAttribute('aria-label', 'Scroll to top');
            button.style.cssText = `
                position: fixed;
                bottom: 2rem;
                right: 2rem;
                width: 48px;
                height: 48px;
                border-radius: 50%;
                background: linear-gradient(135deg, #6366f1 0%, #818cf8 100%);
                color: white;
                border: none;
                font-size: 1.25rem;
                cursor: pointer;
                box-shadow: 0 3px 10px rgba(99, 102, 241, 0.3);
                z-index: 1000;
                opacity: 0;
                transform: translateY(20px);
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
            `;
            
            button.addEventListener('click', () => {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
            
            window.addEventListener('scroll', () => {
                if (window.pageYOffset > 300) {
                    button.style.opacity = '1';
                    button.style.transform = 'translateY(0)';
                } else {
                    button.style.opacity = '0';
                    button.style.transform = 'translateY(20px)';
                }
            });
            
            document.body.appendChild(button);
        }
        
        addScrollToTop();
        
        // Improve keyboard navigation
        function enhanceKeyboardNav() {
            document.addEventListener('keydown', (e) => {
                // Escape key to close modals/dropdowns
                if (e.key === 'Escape') {
                    document.querySelectorAll('[data-baseweb="popover"]').forEach(popover => {
                        if (popover.style.display !== 'none') {
                            const closeBtn = popover.querySelector('[aria-label*="close"], [aria-label*="Close"]');
                            if (closeBtn) closeBtn.click();
                        }
                    });
                }
                
                // Enter key on focused buttons
                if (e.key === 'Enter' && document.activeElement.tagName === 'BUTTON') {
                    const button = document.activeElement;
                    if (!button.disabled) {
                        button.click();
                    }
                }
            });
        }
        
        enhanceKeyboardNav();
        
        // Form validation is already handled by the earlier enhanceFormValidation function
        
        // Re-run enhancements on DOM changes
        const enhancementObserver = new MutationObserver(() => {
            setTimeout(() => {
                enhanceFormFields();
                enhanceButtonFeedback();
                enhanceErrorDisplay();
                enhanceFormValidation();
            }, 100);
        });
        
        enhancementObserver.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
    
    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeAnimations);
    } else {
        initializeAnimations();
    }
    
    // Re-initialize when Streamlit reruns (using MutationObserver)
    const observer = new MutationObserver(function(mutations) {
        let shouldReinit = false;
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length > 0) {
                shouldReinit = true;
            }
        });
        if (shouldReinit) {
            setTimeout(initializeAnimations, 100);
        }
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // Also initialize after a short delay to catch Streamlit's initial render
    setTimeout(initializeAnimations, 500);
    setTimeout(initializeAnimations, 1500);
    
    // Smooth scroll to content when mode changes
    window.addEventListener('load', function() {
        // Function to check if element is in viewport (for window load event)
        function isInViewportLoad(element) {
            const rect = element.getBoundingClientRect();
            return (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.right <= (window.innerWidth || document.documentElement.clientWidth)
            );
        }
        
        if (window.location.hash) {
            setTimeout(() => {
                document.querySelector(window.location.hash)?.scrollIntoView({ behavior: 'smooth' });
            }, 100);
        }
        
        // Trigger initial animations for elements already in view
        setTimeout(() => {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                        entry.target.classList.remove('animate-on-scroll');
                    }
                });
            }, { threshold: 0.1 });
            
            document.querySelectorAll('.scroll-fade-in, .scroll-slide-left, .scroll-slide-right, .scroll-scale-in, .scroll-rotate-in, .dynamic-content').forEach(el => {
                // If already in viewport, make visible immediately
                if (isInViewportLoad(el)) {
                    el.classList.add('visible');
                    el.classList.remove('animate-on-scroll');
                } else {
                    observer.observe(el);
                }
            });
        }, 100);
    });
    
    // Re-observe elements after Streamlit reruns
    const originalRerun = window.parent.postMessage;
    window.addEventListener('message', function(event) {
        if (event.data && event.data.type === 'streamlit:rerun') {
            setTimeout(() => {
                document.querySelectorAll('.dynamic-content, .scroll-fade-in, .scroll-slide-left, .scroll-slide-right, .scroll-scale-in, .scroll-rotate-in').forEach(el => {
                    if (!el.classList.contains('visible')) {
                        const observer = new IntersectionObserver((entries) => {
                            entries.forEach(entry => {
                                if (entry.isIntersecting) {
                                    entry.target.classList.add('visible');
                                    observer.unobserve(entry.target);
                                }
                            });
                        }, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });
                        observer.observe(el);
                    }
                });
            }, 300);
        }
    });
