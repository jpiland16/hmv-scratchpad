import * as THREE from 'https://threejsfundamentals.org/threejs/resources/threejs/r122/build/three.module.js';
import {GLTFLoader} from 'https://threejsfundamentals.org/threejs/resources/threejs/r122/examples/jsm/loaders/GLTFLoader.js';
import {OrbitControls} from 'https://threejsfundamentals.org/threejs/resources/threejs/r122/examples/jsm/controls/OrbitControls.js';
import {GUI} from '../../data/dat.gui.module.d.js'

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
// camera.lookAt(0, 0, 0);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const model_path = '../../data/rp_claudia_rigged_002_yup_a.glb'

var light = new THREE.AmbientLight(0xFFFFFF, 1.5)
scene.add(light);

var LUA;
var xLua = 0;
var yLua = 0;
var zLua = 0;
var wLua = -3.14/2;

var loader = new GLTFLoader();
loader.load(model_path, gltf => {
	var model = gltf.scene;
	scene.add(model);
	console.log("added model to scene.")

	LUA = model.getObjectByName('upperarm_l')
})

const controls = new OrbitControls(camera, renderer.domElement);
camera.position.set(1, 0, 1);
controls.update();

scene.background = new THREE.Color(0xADD8E6);
// scene.position.y = -1;

const geometry = new THREE.SphereGeometry(0.2, 32, 32);
const material = new THREE.MeshBasicMaterial({color: 0xffff00});
const sphere = new THREE.Mesh(geometry, material);
sphere.position.set(0, 0, 0);
scene.add(sphere);

const jointGeometry = new THREE.SphereGeometry(0.4, 32, 32);
const jointMaterial = new THREE.MeshBasicMaterial({color: 0xff0000});
const jointSphere = new THREE.Mesh(jointGeometry, jointMaterial);
jointSphere.position.set(1, 0, -10);
scene.add(jointSphere);

function initGUI() {
	const panel = new GUI({width: 310});
	panel.domElement.id = 'gui';
	document.getElementById("gui").style.marginTop = "56px";

	var panelSettings = {
    'gaussian_filter': 0,
    'x': 0,
    'y': 0,
    'z': 0,
    'w': -3.14/2
  }

	const rotationFolder = panel.addFolder('Rotation');
	const max_rotation = 2*3.14
	rotationFolder.add(panelSettings, "x", -max_rotation, max_rotation, 0.01).onChange(function(x)  {
		xLua = x;
	});
	rotationFolder.add(panelSettings, "y", -max_rotation, max_rotation, 0.01).onChange(function(y)  {
		yLua = y;
	});
	rotationFolder.add(panelSettings, "z", -max_rotation, max_rotation, 0.01).onChange(function(z)  {
		zLua = z;
	});
	rotationFolder.add(panelSettings, "w", -max_rotation, max_rotation, 0.01).onChange(function(w)  {
		wLua = w;
	});

	rotationFolder.open();
}

initGUI();

function animate() {
	requestAnimationFrame(animate);
	renderer.render(scene, camera);
	controls.update();
	let quat = new THREE.Quaternion(xLua, yLua, zLua, wLua).normalize();
	if (LUA) {
		//This is the important part. The composition of these rotations makes the LUA bone point toward the sphere.
		//	It is approximate though, because the joint has some offset owing to its parents while the sphere does not.
		//	It is probably viable to find the total position offset recursively by checking the offset of multiple parents.
		LUA.quaternion.identity();
		LUA.lookAt(new THREE.Vector3(xLua+LUA.position.x, yLua+LUA.position.y, zLua+LUA.position.z));
		sphere.position.set(xLua, yLua, zLua);

		let quatW = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0,1,0),wLua);
		LUA.quaternion.multiply(quatW);


	}
}
animate();