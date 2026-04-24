;(function () {
  var g = window;
  var cfg = g.__GLB_RUNTIME_CONFIG__ || {};
  var injected = '';
  try {
    injected = (g.__APP_CONFIG__ && g.__APP_CONFIG__.apiOrigin) ? String(g.__APP_CONFIG__.apiOrigin) : '';
  } catch (e) { /* ignore */ }
  var fallback = 'https://' + ['smile', 'friend', 'engine-125142687526'].join('-') + '.us-central1.run.app';
  cfg.apiOrigin = (injected || cfg.apiOrigin || fallback).replace(/\/+$/, '');
  g.__GLB_RUNTIME_CONFIG__ = cfg;

  var file = ['glb', 'tomori', 'web'].join('_');
  document.write('<script src="offline-glb/' + file + '.js?v=20260422bb2"><\\/script>');
})();
