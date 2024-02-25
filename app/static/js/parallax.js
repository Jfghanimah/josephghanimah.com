// Select the parallax layer
var parallaxLayer = document.querySelector(".parallax_layer_back");

// Get the viewport width
var vw = window.innerWidth;
var scale = 11.1 + 0.4*((1920 - vw)/1000)

// Set the scale of the parallax layer
parallaxLayer.style.transform = "translateZ(-10px) scale(" + scale + ")";

// Listen for window resize events
window.addEventListener("resize", function() {
  // Get the new viewport height
  vw = window.innerWidth;
  scale = 11.1 + 0.4*((1920 - vw)/1000)

  // Update the scale of the parallax layer
  parallaxLayer.style.transform = "translateZ(-10px) scale(" + scale + ")";
});
