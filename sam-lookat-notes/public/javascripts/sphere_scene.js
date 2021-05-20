import * as THREE from 'https://threejsfundamentals.org/threejs/resources/threejs/r122/build/three.module.js';

const scene = new THREE.Scene();
const camera  = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);
camera.position.set(1, 0, 1);

const geometry = new THREE.SphereGeometry(2, 32, 32);
const material = new THREE.MeshBasicMaterial({color: 0xffff00});
const sphere = new THREE.Mesh(geometry, material);
sphere.position.z += -3;
scene.add(sphere);

function animate() {
	requestAnimationFrame(animate);
	renderer.render(scene, camera);
}

animate();