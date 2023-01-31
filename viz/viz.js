import * as THREE from "./three/three.module.js";

class Frustum extends THREE.PolyhedronGeometry {
    constructor(width1, height1, width2, height2, depth,
		radius = 1, detail = 0) {
	const width1Half = width1 / 2;
	const height1Half = height1 / 2;
	const width2Half = width2 / 2;
	const height2Half = height2 / 2;
	const depthHalf = depth / 2;
    
	const vertices = [
	    -width1Half, -height1Half, -depthHalf,
	    width1Half, -height1Half, -depthHalf,
	    width1Half, height1Half, -depthHalf,
	    -width1Half, height1Half, -depthHalf,

	    -width2Half, -height2Half, depthHalf,
	    width2Half, -height2Half, depthHalf,
	    width2Half, height2Half, depthHalf,
	    -width2Half, height2Half, depthHalf,
	];

	const indices = [
	    2, 1, 0,    0, 3, 2,
	    0, 4, 7,    7, 3, 0,
	    0, 1, 5,    5, 4, 0,
	    1, 2, 6,    6, 5, 1,
	    2, 3, 7,    7, 6, 2,
	    4, 5, 6,    6, 7, 4
	];

	super(vertices, indices, radius, detail);

	this.type = 'Frustum';
	
	this.parameters = {
	    width1: width1,
	    height1: height1,
	    width2: width2,
	    height2: height2,
	    depth: depth,
	    radius: radius,
	    detail: detail
	};
    }
}

// Scene
const scene = new THREE.Scene();

// Add a cube to the scene
//const geometry = new THREE.BoxGeometry(3, 1, 3); // width, height, depth

const geometry = new Frustum(10, 10, 1, 1, 5);

const material = new THREE.MeshLambertMaterial({ color: 0xfb8e00 });
const mesh = new THREE.Mesh(geometry, material);
mesh.position.set(0, 0, 0);
scene.add(mesh);

// Set up lights
const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 0.6);
directionalLight.position.set(10, 20, 0); // x, y, z
scene.add(directionalLight);

// Camera
const width = 10;
const height = width * (window.innerHeight / window.innerWidth);
const camera = new THREE.OrthographicCamera(
  width / -2, // left
  width / 2, // right
  height / 2, // top
  height / -2, // bottom
  1, // near
  100 // far
);

camera.position.set(4, 4, 4);
camera.lookAt(0, 0, 0);

// Renderer
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.render(scene, camera);

// Add it to HTML
document.body.appendChild(renderer.domElement);
