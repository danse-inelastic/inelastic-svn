//functions for zooming/dragging----------------------------------------------
/**
 * Zooms the scene in / out by changing the viewpoint.
 * @param {number} zoom zooming factor.
 */
function ZoomInOut(zoom) {
  for (var i = 0; i < g_eyeView.length; i += 1) {
    g_eyeView[i] = g_eyeView[i] / zoom;
  }

  g_viewInfo.drawContext.view = g_math.matrix4.lookAt(
      g_eyeView,   // eye.
      [0, 0, 0],     // target.
      [0, 1, 0]);   // up.
}

/**
 * Start mouse dragging.
 * @param {event} e event.
 */
function startDragging(e) {
  detectSelectionCell(e);
  g_lastRot = g_thisRot;

  g_aball.click([e.x, e.y]);
  g_dragging = true;
}

/**
 * Use the arcball to rotate the scene.
 * Computes the rotation matrix.
 * @param {event} e event.
 */
function drag(e) {
  if (g_dragging) {
    var rotationQuat = g_aball.drag([e.x, e.y]);
    var rot_mat = g_quaternions.quaternionToRotation(rotationQuat);

    g_thisRot = g_math.matrix4.mul(g_lastRot, rot_mat);
    var m = g_sceneRoot.localMatrix;
    g_math.matrix4.setUpper3x3(m, g_thisRot);
    g_sceneRoot.localMatrix = m;
  }
}

/**
 * Stop dragging.
 * @param {event} e event.
 */
function stopDragging(e) {
  g_dragging = false;
}

/**
 * Using the mouse wheel zoom in and out of the scene.
 * @param {event} e event.
 */
function scrollMe(e) {
  var zoom = (e.deltaY < 0) ? 1 / g_zoomFactor : g_zoomFactor;
  ZoomInOut(zoom);
  g_client.render();
}