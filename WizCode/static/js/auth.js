document.addEventListener('DOMContentLoaded', function() {
    const backgroundEffect = document.createElement('div');
    backgroundEffect.id = 'background-effect';
    document.getElementById('base').prepend(backgroundEffect);

    function createGlowCircle() {
        const circle = document.createElement('div');
        circle.classList.add('glow-circle');
        
        const size = Math.random() * 100 + 50;
        circle.style.width = `${size}px`;
        circle.style.height = `${size}px`;
        
        const startPosition = Math.random() * 100;
        circle.style.left = `${startPosition}%`;
        
        backgroundEffect.appendChild(circle);

        setTimeout(() => {
            circle.remove();
        }, 10000);
    }

    setInterval(createGlowCircle, 500);
});