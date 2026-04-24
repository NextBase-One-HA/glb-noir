/**
 * TRAVEL_ROUTE_CORE_01 — 流し方だけ。翻訳文の改変・補正はしない。
 *
 * - dictionary: 辞書の完成文をそのまま出す（本モジュールは判定のみ）
 * - direct: 下流エンジンへ src→tgt のまま渡す（中身は触らない）
 * - pivot_en: 中継（en ピボット）の手続きだけ。中間/最終テキストの加工は禁止
 *
 * 接続先エンジン・翻訳APIは本ファイルから呼ばない。
 *
 * @param {string} input
 * @param {string} src
 * @param {string} tgt
 * @param {{ pairTable?: Record<string, 'direct'|'pivot_en'>, isTravelPhrase?: (s: string) => boolean }} [opts]
 * @returns {'dictionary'|'direct'|'pivot_en'}
 */
function glbRouteMinimal(input, src, tgt, opts) {
    opts = opts || {};
    var pairTable = opts.pairTable || {};
    var isTravelPhrase =
        typeof opts.isTravelPhrase === 'function'
            ? opts.isTravelPhrase
            : function () {
                  return false;
              };
    if (isTravelPhrase(String(input || ''))) return 'dictionary';
    var pair = String(src || '').trim() + '-' + String(tgt || '').trim();
    if (pairTable[pair] === 'direct') return 'direct';
    return 'pivot_en';
}

/** @type {typeof glbRouteMinimal} */
function route(input, src, tgt, opts) {
    return glbRouteMinimal(input, src, tgt, opts);
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { glbRouteMinimal: glbRouteMinimal, route: route };
}
