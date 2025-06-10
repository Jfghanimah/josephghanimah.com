document.addEventListener('DOMContentLoaded', function() {
    const frontLayer = document.querySelector('.parallax_layer_front');
    const backLayer = document.querySelector('.parallax_layer_back');

    // If the required layers don't exist, do nothing.
    if (!frontLayer || !backLayer) {
        console.warn('Parallax layers not found. Parallax script will not run.');
        return;
    }

    // This is the main function that updates both height and scale.
    function updateParallax() {
        // --- 1. DYNAMIC HEIGHT ADJUSTMENT ---
        // Measure the total scrollable height of the content layer.
        const contentHeight = frontLayer.scrollHeight;
        
        // Apply this height to the background layer.
        // We add a small buffer (e.g., 50px) to prevent the background from ending slightly
        // too early on some browsers or during momentum scrolling.
        backLayer.style.height = (contentHeight + 50) + 'px';


        // --- 2. DYNAMIC SCALING---
        const vw = window.innerWidth;
        
        // The scaling formula.
        const scale = 11.1 + 0.4 * ((1920 - vw) / 1000);

        // Update the transform property, keeping both translateZ and the new scale.
        backLayer.style.transform = `translateZ(-10px) scale(${scale})`;
    }

    // --- WHEN TO RUN THE UPDATE FUNCTION ---

    // Run it once the initial HTML is loaded.
    updateParallax();

    // Run it again after all images and resources are loaded, as images can change the content height.
    window.addEventListener('load', updateParallax);

    // Run it whenever the browser window is resized, as this can cause content to reflow and change height.
    window.addEventListener('resize', updateParallax);

    // For highly dynamic sites, you might need to call updateParallax() after loading content with AJAX.
    // For this portfolio, the above listeners are sufficient.
});