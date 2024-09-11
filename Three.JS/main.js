import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

let scene, camera, renderer;
let basket, flowers = [];
let basketSpeed = 0.5;
let flowerSpawnInterval = 1000; 
let flowerCount = 0;
let counterElement, gameOverElement, timerElement;
let gameDuration = 30; // 30 seconds
let startTime, elapsedTime;

init();
animate();

function init() {
    // Scene
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 4;

    renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.domElement.style.backgroundImage = "url('./Images/pngtree-low-poly-fantasy-forest-cartoon-a-stunning-3d-rendering-of-a-picture-image_5575619.jpg')";
    renderer.domElement.style.backgroundSize = 'cover';
    renderer.domElement.style.backgroundPosition = 'center';
    renderer.domElement.style.backgroundRepeat = 'no-repeat';
    document.body.appendChild(renderer.domElement);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 2);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 5);
    directionalLight.position.set(0, 1, 1).normalize();
    scene.add(directionalLight);

    // Basket model
    const loader = new GLTFLoader();
    loader.load('./models/basket.glb', function(gltf) {
        basket = gltf.scene;
        basket.scale.set(0.5, 0.5, 0.5);
        basket.position.y = -8;
        scene.add(basket);
    });

    // Flower spawn interval
    setInterval(spawnFlower, flowerSpawnInterval);

    // Counter element
    counterElement = document.createElement('div');
    counterElement.style.position = 'absolute';
    counterElement.style.top = '10px';
    counterElement.style.left = '10px';
    counterElement.style.color = 'white';
    counterElement.style.fontSize = '24px';
    document.body.appendChild(counterElement);
    updateCounter();

    // Timer element
    timerElement = document.createElement('div');
    timerElement.style.position = 'absolute';
    timerElement.style.top = '40px';
    timerElement.style.left = '10px';
    timerElement.style.color = 'white';
    timerElement.style.fontSize = '24px';
    document.body.appendChild(timerElement);

    // Game over element
    gameOverElement = document.createElement('div');
    gameOverElement.style.position = 'absolute';
    gameOverElement.style.top = '50%';
    gameOverElement.style.left = '50%';
    gameOverElement.style.transform = 'translate(-50%, -50%)';
    gameOverElement.style.color = 'red';
    gameOverElement.style.fontSize = '68px';
    gameOverElement.style.textAlign = 'center';
    gameOverElement.style.width = '100%';
    gameOverElement.style.display="none";
    gameOverElement.innerHTML = 'Game Over!<br>Total Flowers Collected: ' + flowerCount;
    document.body.appendChild(gameOverElement);

    // timer
    startTime = Date.now();

    // Keyboard controls
    document.addEventListener('keydown', moveBasket);
}

function spawnFlower() {
    const loader = new GLTFLoader();
    loader.load('./models/flower_red.glb', function(gltf) {
        const flower = gltf.scene;
        flower.position.set(Math.random() * 4 - 2, 3, 0);
        flower.scale.set(0.2, 0.2, 0.2);
       
        flowers.push(flower);
        scene.add(flower);
    });
}

function moveBasket(event) {
    if (basket) {
        if (event.key === 'ArrowLeft' || event.key === 'a') {
            basket.position.x -= basketSpeed;
        } else if (event.key === 'ArrowRight' || event.key === 'd') {
            basket.position.x += basketSpeed;
        }
    }
}

function animate() {
    requestAnimationFrame(animate);

    // Calculate elapsed time
    elapsedTime = (Date.now() - startTime) / 1000; // Convert to seconds
    let remainingTime = Math.max(gameDuration - elapsedTime, 0);
    timerElement.textContent = 'Time Left: ' + remainingTime.toFixed(1) + 's';

    if (remainingTime <= 0) {
        endGame();
        return;
    }

    // Update flowers
    flowers.forEach(flower => {
        flower.position.y -= 0.02;

        // Check for collision
        if (flower.position.y < -2 && basket && Math.abs(flower.position.x - basket.position.x) < 3) {
            if (!flower.collected) {
                flower.collected = true;
                flowerCount++;
                updateCounter();
            }
            scene.remove(flower);
        } else if (flower.position.y < -3.5) {
            scene.remove(flower);
        }
    });

    flowers = flowers.filter(flower => flower.position.y > -3.5);

    renderer.render(scene, camera);
}

function updateCounter() {
    counterElement.textContent = 'Flowers Collected: ' + flowerCount;
}

function endGame() {
    gameOverElement.innerHTML = 'Game Over!<br>Total Flowers Collected: ' + flowerCount;

    gameOverElement.style.display = 'block';
}
