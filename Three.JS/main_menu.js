import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

let scene, camera, renderer;
let character = null, buildings = [], interactZones = [];
let interactableIndex = -1;
let moveDirection = { left: false, right: false, forward: false, backward: false };
let moveSpeed = 0.1;

// Initialize the scene, camera, and objects
function init() {
    // Scene setup
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x87CEEB); // Sky blue color

    // Camera setup
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 10, 10);
    camera.lookAt(0, 0, 0);

    // Renderer setup
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    // Ambient light
    const ambientLight = new THREE.AmbientLight(0xffffff, 1);
    scene.add(ambientLight);

    // Directional light for shadow
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight.position.set(10, 20, 10);
    scene.add(directionalLight);

    // Create platform
    const platformGeometry = new THREE.BoxGeometry(1000, 1, 1000);
    const platformMaterial = new THREE.MeshStandardMaterial({ color: 0x808080 });
    const platform = new THREE.Mesh(platformGeometry, platformMaterial);
    platform.position.y = -0.5;
    scene.add(platform);

    // Load character model
    const loader = new GLTFLoader();
    loader.load('./models/robo_toon.glb', function(gltf) {
        character = gltf.scene;
        character.scale.set(0.1, 0.1, 0.1); // Ensure correct scaling
        character.position.set(0, 1, 0);
        scene.add(character);

        // Add a debug box for the character's bounding box
        const debugGeometry = new THREE.BoxGeometry(1, 2, 1);
        const debugMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000, wireframe: true });
        const debugBox = new THREE.Mesh(debugGeometry, debugMaterial);
        debugBox.position.copy(character.position);
        scene.add(debugBox);
    });

    // Create buildings and interaction zones
    for (let i = 0; i < 3; i++) {
        const buildingGeometry = new THREE.BoxGeometry(3, 6, 3);
        const buildingMaterial = new THREE.MeshStandardMaterial({ color: 0x0000ff });
        const building = new THREE.Mesh(buildingGeometry, buildingMaterial);
        building.position.set(i * 6 - 6, 3, -15);
        scene.add(building);
        buildings.push(building);

        // Create interaction zones
        const zoneGeometry = new THREE.BoxGeometry(4, 0.2, 4);
        const zoneMaterial = new THREE.MeshBasicMaterial({ color: 0xffff00, transparent: true, opacity: 0.5 });
        const interactZone = new THREE.Mesh(zoneGeometry, zoneMaterial);
        interactZone.position.set(i * 6 - 6, 0, -10);
        scene.add(interactZone);
        interactZones.push(interactZone);
    }

    // Event listener for interaction
    document.addEventListener('keydown', onDocumentKeyDown, false);
    document.addEventListener('keyup', onDocumentKeyUp, false);

    // Resize event listener
    window.addEventListener('resize', onWindowResize, false);
}

// Handle keydown event for character movement
function onDocumentKeyDown(event) {
    switch (event.key) {
        case 'ArrowUp':
        case 'w':
            moveDirection.forward = true;
            break;
        case 'ArrowDown':
        case 's':
            moveDirection.backward = true;
            break;
        case 'ArrowLeft':
        case 'a':
            moveDirection.left = true;
            break;
        case 'ArrowRight':
        case 'd':
            moveDirection.right = true;
            break;
        case 'Enter':
            if (interactableIndex !== -1) {
                console.log(`Interacting with zone ${interactableIndex}`);
                if (interactableIndex === 0) {
                    window.location.href = "/main.js";
                } else if (interactableIndex === 1) {
                    window.location.href = "/page2.html";
                } else if (interactableIndex === 2) {
                    window.location.href = "/page3.html";
                }
            } else {
                console.log('No zone interaction detected');
            }
            break;
    }
}

// Handle keyup event to stop movement
function onDocumentKeyUp(event) {
    switch (event.key) {
        case 'ArrowUp':
        case 'w':
            moveDirection.forward = false;
            break;
        case 'ArrowDown':
        case 's':
            moveDirection.backward = false;
            break;
        case 'ArrowLeft':
        case 'a':
            moveDirection.left = false;
            break;
        case 'ArrowRight':
        case 'd':
            moveDirection.right = false;
            break;
    }
}

// Animate the scene, handle character movement, and move the camera with the player
function animate() {
    requestAnimationFrame(animate);

    if (character) {
        let rotationChanged = false;

        // Move character based on key presses and update rotation
        if (moveDirection.forward) {
            character.position.z -= moveSpeed;
            character.rotation.y = Math.PI; // Face forward
            rotationChanged = true;
        }
        if (moveDirection.backward) {
            character.position.z += moveSpeed;
            character.rotation.y = 0; // Face backward
            rotationChanged = true;
        }
        if (moveDirection.left) {
            character.position.x -= moveSpeed;
            character.rotation.y = Math.PI / 2; // Face left
            rotationChanged = true;
        }
        if (moveDirection.right) {
            character.position.x += moveSpeed;
            character.rotation.y = -Math.PI / 2; // Face right
            rotationChanged = true;
        }

        // Move the camera with the player
        camera.position.x = character.position.x;
        camera.position.z = character.position.z + 10;
        camera.lookAt(character.position.x, character.position.y, character.position.z);

        // Check for interaction with zones
        checkInteractionZones();
    }

    renderer.render(scene, camera);
}

// Check if the character is inside an interaction zone
function checkInteractionZones() {
    interactableIndex = -1; // Reset interaction zone index

    for (let i = 0; i < interactZones.length; i++) {
        const zone = interactZones[i];
        const zoneBox = new THREE.Box3().setFromObject(zone);
        const charBox = new THREE.Box3().setFromObject(character);

        if (zoneBox.intersectsBox(charBox)) {
            interactableIndex = i;
            console.log(`Character inside interaction zone ${i}`);
            break;
        }
    }
}

// Handle window resize
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// Initialize and run the scene
init();
animate();
