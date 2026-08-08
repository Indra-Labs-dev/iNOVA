// Gate 7 — real (not spike) glue between Flutter and the vendored three.js
// build (see ../vendor/three/PROVENANCE.md). First implementation of the
// bridge contract described in docs/04-3d-world/2d-3d-integration.md.
//
// Architectural rule this file must respect (same as the Gate 6 spike):
// Three.js never owns application state, navigation, or business logic.
// It only (a) reacts to commands Flutter sends it — here, the accent
// color, which Flutter derives from its own real theme, never hardcoded
// here — and (b) reports a raw click event back to Flutter, leaving
// Flutter to decide what that means (in this increment: navigate to
// Missions). Nothing here reads or writes any application state.
import * as THREE from '../vendor/three/three.module.min.js';

// Bumped whenever the shape of init/set*/dispose or the callback payload
// changes, so a future mismatch between this file and the Dart bindings in
// lib/features/world/application/world_bridge_interop.dart fails loudly
// (a console warning today) instead of silently misbehaving — see
// docs/04-3d-world/2d-3d-integration.md "Rules".
const bridgeVersion = '1.0.0';

let scene, camera, renderer, mesh, raycaster, container, animId;
let onObjectClickCallback = null;

function init(containerId) {
  container = document.getElementById(containerId);
  if (!container) {
    throw new Error('iNovaWorld.init: container not found: ' + containerId);
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

  // Icosahedron, not the Gate 6 spike's cube — deliberately distinct so a
  // screenshot can never be mistaken for the spike. Color is set by
  // setAccentColor(), never hardcoded, so the object visualizes real
  // Flutter theme state rather than owning its own.
  const geometry = new THREE.IcosahedronGeometry(1, 0);
  const material = new THREE.MeshStandardMaterial({ color: 0x808080 });
  mesh = new THREE.Mesh(geometry, material);
  scene.add(mesh);

  scene.add(new THREE.AmbientLight(0xffffff, 0.6));
  const light = new THREE.DirectionalLight(0xffffff, 0.8);
  light.position.set(2, 2, 2);
  scene.add(light);

  raycaster = new THREE.Raycaster();
  renderer.domElement.addEventListener('click', onClick);
  window.addEventListener('resize', onResize);

  animate();
}

function onClick(event) {
  const rect = renderer.domElement.getBoundingClientRect();
  const pointer = new THREE.Vector2(
    ((event.clientX - rect.left) / rect.width) * 2 - 1,
    -((event.clientY - rect.top) / rect.height) * 2 + 1,
  );
  raycaster.setFromCamera(pointer, camera);
  const hits = raycaster.intersectObject(mesh);
  if (hits.length > 0 && onObjectClickCallback) {
    onObjectClickCallback();
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
  mesh.rotation.x += 0.004;
  mesh.rotation.y += 0.006;
  renderer.render(scene, camera);
}

function setAccentColor(hex) {
  if (mesh) mesh.material.color.set(hex);
}

function setOnObjectClick(callback) {
  onObjectClickCallback = callback;
}

function dispose() {
  if (animId) cancelAnimationFrame(animId);
  window.removeEventListener('resize', onResize);
  if (renderer) {
    renderer.domElement.removeEventListener('click', onClick);
    renderer.dispose();
  }
  scene = camera = renderer = mesh = raycaster = container = null;
  onObjectClickCallback = null;
}

window.iNovaWorld = { bridgeVersion, init, setAccentColor, setOnObjectClick, dispose };
