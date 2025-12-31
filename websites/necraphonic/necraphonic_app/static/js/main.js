// necraphonic_app/static/js/main.js

document.addEventListener('DOMContentLoaded', () => {
    console.log("Necraphonic Interface Initialized");
  
    // --- Mobile Menu Toggle ---
    const menuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
  
    if (menuButton && mobileMenu) {
      menuButton.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
        // Optional: Toggle ARIA attribute for accessibility
        const isExpanded = mobileMenu.classList.contains('hidden') ? 'false' : 'true';
        menuButton.setAttribute('aria-expanded', isExpanded);
      });
    }
  
    // --- Add Hover Effects Programmatically (Example: Glitch on specific links) ---
    const glitchLinks = document.querySelectorAll('.hover-glitch-js'); // Add this class to elements in HTML if needed
    glitchLinks.forEach(link => {
      link.addEventListener('mouseenter', () => link.classList.add('glitch-effect'));
      link.addEventListener('mouseleave', () => link.classList.remove('glitch-effect'));
    });
  
    // --- Scroll Reveal Animations ---
    const revealElements = document.querySelectorAll('.reveal-on-scroll');
  
    if (revealElements.length > 0) {
      const observerOptions = {
        root: null, // relative to the viewport
        rootMargin: '0px',
        threshold: 0.1 // Trigger when 10% of the element is visible
      };
  
      const observerCallback = (entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            // Optional: Stop observing once the element is visible
            // observer.unobserve(entry.target);
          } else {
            // Optional: Remove class if you want the animation to repeat when scrolling out and back in
             entry.target.classList.remove('visible');
          }
        });
      };
  
      const intersectionObserver = new IntersectionObserver(observerCallback, observerOptions);
  
      revealElements.forEach(el => {
        intersectionObserver.observe(el);
      });
    }
  
  
    // --- Mouse Move Effect (Example: Subtle background parallax/shift) ---
    // This can be performance-intensive; use sparingly or optimize.
    // const parallaxTarget = document.querySelector('#landing-hero'); // Target an element
    // if (parallaxTarget) {
    //   document.addEventListener('mousemove', (e) => {
    //     const { clientX, clientY } = e;
    //     const { innerWidth, innerHeight } = window;
  
    //     // Calculate movement ratio (adjust multiplier for sensitivity)
    //     const moveX = ((clientX / innerWidth) - 0.5) * 20; // Max 10px move left/right
    //     const moveY = ((clientY / innerHeight) - 0.5) * 10; // Max 5px move up/down
  
    //     // Apply transform (use requestAnimationFrame for performance)
    //     requestAnimationFrame(() => {
    //        // Apply to a background *element* within the hero, not the hero itself usually
    //        const bgElement = parallaxTarget.querySelector('#hero-background div'); // Example selector
    //        if(bgElement) {
    //            bgElement.style.transform = `translate(${moveX}px, ${moveY}px)`;
    //        }
    //     });
    //   });
    // }
  
  
    // --- Smooth Scrolling for internal links (like #explore) ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
          targetElement.scrollIntoView({
            behavior: 'smooth'
          });
        }
      });
    });
  
  
    // --- Page Transition Hint (Very Basic Example) ---
    // For real page transitions, use libraries like Barba.js or Swup.js
    const internalLinks = document.querySelectorAll('a:not([href^="#"]):not([target="_blank"])'); // Select internal links
    internalLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        const href = link.getAttribute('href');
        // Prevent navigation if it's the current page or not a real URL
        if (!href || href === window.location.pathname || href.startsWith('mailto:') || href.startsWith('tel:')) {
          return;
        }
        e.preventDefault(); // Stop immediate navigation
        document.body.style.opacity = '0'; // Fade out body
        document.body.style.transition = 'opacity 0.4s ease-out';
        // Navigate after fade out
        setTimeout(() => {
          window.location.href = href;
        }, 400); // Match transition duration
      });
    });
    // Add fade-in on load (can conflict if browser restores scroll position before transition ends)
    window.addEventListener('load', () => {
      document.body.style.opacity = '1';
      document.body.style.transition = 'opacity 0.5s ease-in';
    });
  
  
    // Add more specific JS interactions for music page, etc. in separate files or here.
    // Example: music_player.js would handle the track selection and content loading.
  
  }); // End DOMContentLoaded
  