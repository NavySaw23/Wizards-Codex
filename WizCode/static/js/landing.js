document.addEventListener('DOMContentLoaded', function() {
    const welElement = document.getElementById('wel');
    const titleElement = document.getElementById('title');
    const backgroundEffect = document.getElementById('background-effect');
    let welAngle = 0;
    let titleAngle = 0.5;

    function animate() {
        welAngle += 0.005;
        const y = Math.sin(welAngle) * 10;
        welElement.style.transform = `translateY(${y}px)`;

        titleAngle += 0.005;
        const titleY = Math.sin(titleAngle) * 10;
        titleElement.style.transform = `translateY(${titleY}px)`;

        requestAnimationFrame(animate);
    }

    animate();

    function createGlowCircle() {
        const circle = document.createElement('div');
        circle.classList.add('glow-circle');
        
        const size = Math.random() * 100 + 50; // Random size between 50 and 150 pixels
        circle.style.width = `${size}px`;
        circle.style.height = `${size}px`;
        
        const startPosition = Math.random() * 100; // Random horizontal position
        circle.style.left = `${startPosition}%`;
        
        backgroundEffect.appendChild(circle);

        // Remove the circle after animation completes
        setTimeout(() => {
            circle.remove();
        }, 10000);
    }

    // Create a new circle every 500ms
    setInterval(createGlowCircle, 500);
});