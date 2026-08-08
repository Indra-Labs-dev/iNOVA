// Gate 6 spike — isolated glue between Flutter and the vendored three.js
// build (see vendor/three/PROVENANCE.md). Not part of the shipped app.
//
// Architectural rule this file must respect (per the Gate 6 GO): Three.js
// never owns application state, navigation, or business logic — it only
// (a) reacts to commands Flutter sends it (setRotationSpeed) and
// (b) reports raw events back to Flutter (a click hit-test), leaving
// Flutter to decide what that means. Nothing here reads or writes any
// application state.
import * as THREE from './vendor/three/three.module.min.js';

let scene, camera, renderer, cube, raycaster, container, animId;
let rotationSpeed = 0.01;
let onCubeClickCallback = null;
let frameCount = 0;
let lastFpsSampleTime = 0;
let currentFps = 0;

function init(containerId) {
  container = document.getElementById(containerId);
  if (!container) {
    throw new Error('iNovaSpike3D.init: container not found: ' + containerId);
  }

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0b1220);

  const width = container.clientWidth || 320;
  const height = container.clientHeight || 320;
  camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 100);
  camera.position.z = 3;

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  container.innerHTML = '';
  container.appendChild(renderer.domElement);

  const geometry = new THREE.BoxGeometry(1, 1, 1);
  const material = new THREE.MeshStandardMaterial({ color: 0x4f7cff });
  cube = new THREE.Mesh(geometry, material);
  scene.add(cube);

  scene.add(new THREE.AmbientLight(0xffffff, 0.6));
  const light = new THREE.DirectionalLight(0xffffff, 0.8);
  light.position.set(2, 2, 2);
  scene.add(light);

  raycaster = new THREE.Raycaster();
  renderer.domElement.addEventListener('click', onClick);
  window.addEventListener('resize', onResize);

  frameCount = 0;
  lastFpsSampleTime = performance.now();
  animate();
}

function onClick(event) {
  const rect = renderer.domElement.getBoundingClientRect();
  const pointer = new THREE.Vector2(
    ((event.clientX - rect.left) / rect.width) * 2 - 1,
    -((event.clientY - rect.top) / rect.height) * 2 + 1,
  );
  raycaster.setFromCamera(pointer, camera);
  const hits = raycaster.intersectObject(cube);
  if (hits.length > 0 && onCubeClickCallback) {
    onCubeClickCallback(performance.now());
  }
}

function onResize() {
  if (!container || !renderer || !camera) return;
  const width = container.clientWidth || 320;
  const height = container.clientHeight || 320;
  renderer.setSize(width, height);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
}

function animate() {
  animId = requestAnimationFrame(animate);
  cube.rotation.x += rotationSpeed;
  cube.rotation.y += rotationSpeed;
  renderer.render(scene, camera);

  frameCount += 1;
  const now = performance.now();
  if (now - lastFpsSampleTime >= 1000) {
    currentFps = Math.round((frameCount * 1000) / (now - lastFpsSampleTime));
    frameCount = 0;
    lastFpsSampleTime = now;
  }
}

function setRotationSpeed(value) {
  rotationSpeed = value;
}

function setOnCubeClick(callback) {
  onCubeClickCallback = callback;
}

function getFps() {
  return currentFps;
}

function dispose() {
  if (animId) cancelAnimationFrame(animId);
  window.removeEventListener('resize', onResize);
  if (renderer) {
    renderer.domElement.removeEventListener('click', onClick);
    renderer.dispose();
  }
  scene = camera = renderer = cube = raycaster = container = null;
  onCubeClickCallback = null;
}

window.iNovaSpike3D = { init, setRotationSpeed, setOnCubeClick, getFps, dispose };
