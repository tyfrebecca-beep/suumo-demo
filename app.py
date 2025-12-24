import streamlit as st
import random
import time
import re

# --- 1. アプリ設定とスタイル ---
st.set_page_config(page_title="SUUMO Demo", layout="centered")

# HTML描画用ラッパー
def st_html(html_string):
    clean_html = re.sub(r'^\s+', '', html_string, flags=re.MULTILINE).strip()
    st.markdown(clean_html, unsafe_allow_html=True)

st.markdown("""
<style>
    /* ベース設定 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, "Noto Sans JP", sans-serif;
    }
    
    .block-container {
        max-width: 414px;
        padding-top: 0rem;
        padding-bottom: 5rem;
        padding-left: 0;
        padding-right: 0;
        background-color: #f5f7fa;
    }
    
    /* ヘッダー */
    .app-header {
        background-color: #fff;
        color: #03a64a;
        padding: 12px 0;
        text-align: center;
        font-weight: 900;
        font-size: 1.3em;
        border-bottom: 1px solid #e0e0e0;
        letter-spacing: 1px;
        position: sticky; top: 0; z-index: 999;
    }

    /* 検索条件パネル */
    .search-panel-container { padding: 10px 10px 0 10px; }
    .search-panel {
        background-color: #fff; border-radius: 4px; padding: 12px 15px;
        margin-bottom: 15px; font-size: 0.8em; color: #333;
        border: 1px solid #e0e0e0; box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    .search-label { font-weight: bold; color: #03a64a; margin-right: 5px; }
    
    .alert-box {
        margin-top: 8px; background-color: #fff4f4; border: 1px solid #ffebeb;
        padding: 8px 10px; border-radius: 4px; color: #eb3e3e;
        font-weight: bold; font-size: 0.9em; display: flex; align-items: center;
    }
    .alert-icon { margin-right: 6px; font-size: 1.1em; }

    /* --- カルーセルセクション --- */
    .carousel-section {
        background-color: transparent; padding: 0 0 10px 10px; margin-bottom: 20px;
    }
    .carousel-section.special {
        background-color: #fff; border-top: 1px solid #eee; border-bottom: 1px solid #eee;
        padding-top: 15px; padding-bottom: 15px; margin-bottom: 10px;
    }

    /* AIラベル */
    .ai-label {
        display: inline-block; font-size: 0.7em; font-weight: bold; color: #fff;
        margin-bottom: 8px; background-color: #03a64a;
        padding: 3px 10px; border-radius: 100px;
        box-shadow: 0 2px 4px rgba(3,166,74,0.3);
    }

    .section-header { padding-right: 15px; margin-bottom: 10px; }
    .carousel-title {
        font-weight: bold; font-size: 1.0em; color: #333; line-height: 1.4; margin-bottom: 4px;
    }
    .carousel-sub-title { font-size: 0.75em; color: #666; line-height: 1.4; }

    /* メリットタグ */
    .benefit-bar {
        display: flex; align-items: center; margin-top: 8px; margin-bottom: 5px; gap: 6px;
    }
    .benefit-tag {
        font-size: 0.7em; font-weight: bold; padding: 4px 8px; border-radius: 3px;
    }
    .tag-cond { background: #fff8e1; color: #d97706; border: 1px solid #ffecb3; }
    .tag-gain { background: #e6f7ed; color: #03a64a; border: 1px solid #ccebd6; }

    .carousel-container {
        display: flex; overflow-x: auto; white-space: nowrap;
        -webkit-overflow-scrolling: touch; padding-bottom: 10px; padding-right: 15px; gap: 10px;
    }
    .carousel-container::-webkit-scrollbar { display: none; }

    /* --- 物件カード --- */
    .prop-card {
        display: inline-block; width: 160px; flex-shrink: 0;
        background: #fff; border-radius: 4px; overflow: hidden;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08); 
        border: 1px solid #e5e5e5; position: relative;
    }
    .prop-img {
        height: 110px; background-color: #eee; position: relative;
        background-size: cover; background-position: center;
    }
    
    /* 未閲覧サッシュ */
    .badge-new-sash {
        position: absolute; top: 0; left: 0; width: 0; height: 0;
        border-top: 40px solid #eb3e3e; border-right: 40px solid transparent; z-index: 10;
    }
    .badge-new-text {
        position: absolute; top: 2px; left: 2px; color: #fff;
        font-size: 0.55em; font-weight: bold; transform: rotate(-45deg); z-index: 11;
    }
    
    /* ハートアイコン */
    .fav-icon {
        position: absolute; top: 6px; right: 6px;
        color: #fff; font-size: 1.2em; text-shadow: 0 0 3px rgba(0,0,0,0.3); z-index: 10;
    }

    /* 種別黒帯 */
    .type-label-black {
        position: absolute; bottom: 0; left: 0;
        background: rgba(30,30,30,0.85); color: #fff;
        font-size: 0.6em; padding: 2px 6px;
        border-top-right-radius: 2px; z-index: 5;
    }
    
    /* (緑の帯 .gain-overlay は削除しました) */

    .prop-info { padding: 8px 10px; white-space: normal; }
    .prop-price {
        color: #eb3e3e; font-weight: bold; font-size: 1.1em;
        margin-bottom: 2px; font-family: Arial, sans-serif; letter-spacing: -0.5px;
    }
    .prop-layout { font-size: 0.75em; font-weight:bold; color: #333; margin-bottom: 2px; }
    .prop-detail { font-size: 0.7em; color: #666; line-height: 1.3; }

    /* --- 1feed デザイン --- */
    .feed-section-title {
        padding: 10px 10px 5px 10px; font-weight: bold; color: #333; font-size: 1.0em;
    }
    .feed-container { padding: 0 10px 30px 10px; }
    .feed-card {
        background: #fff; border: 1px solid #ddd; border-radius: 4px;
        margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); overflow: hidden;
    }
    .feed-header {
        padding: 10px 12px; border-bottom: 1px solid #f0f0f0;
        font-size: 0.85em; font-weight: bold; color: #333;
        display: flex; align-items: flex-start; line-height: 1.4;
    }
    .feed-check-box {
        width: 16px; height: 16px; background: #88c948; border-radius: 2px;
        display: flex; align-items: center; justify-content: center;
        margin-right: 8px; margin-top: 2px; flex-shrink: 0;
    }
    .feed-check-mark { color: #fff; font-size: 12px; font-weight: bold; }
    .feed-subheader {
        background: #fcfcfc; padding: 6px 12px; font-size: 0.75em; color: #666;
        border-bottom: 1px solid #eee; display: flex; align-items: center;
    }
    .view-count { color: #d97706; font-weight: bold; margin-right: 5px; }
    .feed-img-area {
        height: 200px; background-color: #eee; background-size: cover;
        background-position: center; position: relative;
    }
    .feed-badge-grey {
        position: absolute; bottom: 0; left: 0; background: rgba(50,50,50,0.8);
        color: #fff; font-size: 0.7em; padding: 3px 8px;
    }
    .feed-badge-viewed {
        position: absolute; top: 0; right: 0; background: #999;
        color: #fff; font-size: 0.7em; padding: 3px 8px;
    }
    .feed-content { padding: 12px 15px; }
    .visit-badge {
        display: inline-block; color: #eb3e3e; border: 1px solid #eb3e3e;
        font-size: 0.7em; padding: 1px 5px; border-radius: 2px;
        font-weight: normal; margin-bottom: 6px; background: #fff;
    }
    .visit-icon { margin-right: 2px; font-weight:bold; }
    .feed-price-row {
        font-size: 1.4em; color: #eb3e3e; font-weight: bold;
        margin-bottom: 5px; font-family: Arial, sans-serif; letter-spacing: -0.5px;
    }
    .price-unit { font-size: 0.7em; margin-left: 1px; }
    .price-update { 
        font-size: 0.5em; background: #999; color: #fff;
        padding: 2px 4px; border-radius: 2px; vertical-align: middle;
        margin-left: 5px; font-weight: normal;
    }
    .feed-layout { font-weight: bold; font-size: 0.95em; margin-bottom: 5px; color: #333; }
    .feed-address { font-size: 0.8em; margin-bottom: 2px; color: #333; }
    .feed-access { font-size: 0.8em; margin-bottom: 10px; color: #666; }
    .feed-specs { 
        font-size: 0.75em; color: #555; margin-bottom: 12px; 
        background: #f7f7f7; padding: 6px; border-radius: 4px; 
    }
    .feed-tags { font-size: 0.7em; color: #888; margin-bottom: 15px; display: flex; flex-wrap: wrap; gap: 4px; }
    .feed-tag-item { background: #f0f0f0; padding: 3px 6px; border-radius: 2px; color: #666; }
    .feed-action-btn {
        display: flex; justify-content: center; align-items: center;
        width: 100%; border: 1px solid #eb3e3e;
        color: #eb3e3e; background: #fff; padding: 9px 0; border-radius: 30px;
        font-weight: bold; font-size: 0.9em; cursor: pointer;
    }
    .btn-icon { margin-right: 4px; font-size: 1.1em; }
    .feed-action-btn:hover { background: #fff5f5; }

</style>
""", unsafe_allow_html=True)

# --- 2. サイドバー（操作パネル） ---
st.sidebar.title("📱 デモ操作パネル")
hits_count = st.sidebar.slider("検索ヒット件数", 0, 100, 50, help="30件未満でモード切替")

st.sidebar.markdown("### ユーザー条件設定")
user_budget = st.sidebar.slider("予算 (万円)", 4000, 10000, 7000, step=100)
user_walk = st.sidebar.slider("駅徒歩 (分)", 5, 20, 10)
user_area = st.sidebar.slider("広さ (㎡)", 50, 100, 70)
target_area = st.sidebar.selectbox("エリア", ["世田谷区", "目黒区", "杉並区"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🤖 ずらしパターン強制指定")
pattern_select = st.sidebar.selectbox(
    "プレゼンで見せたいパターンを選択",
    [
        "Auto (自動判定)", 
        "Pattern A: 広さ重視 (+5分)", 
        "Pattern B: 駅近重視 (築古)", 
        "Pattern C: 種別変更 (戸建)", 
        "Pattern D: 隣接エリア",
        "Pattern E: 予算解決型 (+500万)"
    ]
)

THRESHOLD_STALLED = 30

# --- 3. ロジック関数 ---

def render_header():
    st_html('<div class="app-header">SUUMO</div>')

def render_search_panel(hits, area, budget, walk, area_size):
    alert_html = ""
    if hits < THRESHOLD_STALLED:
        alert_html = f"""
        <div class="alert-box">
            <span class="alert-icon">⚠️</span> 条件に合う物件が残り{hits}件です
        </div>
        """
    
    html = f"""
    <div class="search-panel-container">
        <div class="search-panel">
            <div>
                <span class="search-label">検索条件</span>
                {area} / {budget:,}万円以下 / {walk}分 / {area_size}㎡~
            </div>
            {alert_html}
        </div>
    </div>
    """
    st_html(html)

def _generate_props(count, base_budget, base_walk, base_area, p_type_override=None, age_override=None):
    """物件データ生成器"""
    props = []
    images = [
        "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=600&q=80", 
        "https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=600&q=80", 
        "https://images.unsplash.com/photo-1580587771525-78b9dba3b91d?auto=format&fit=crop&w=600&q=80"
    ]
    for _ in range(count):
        ptype = p_type_override if p_type_override else random.choice(["中古マンション", "新築一戸建て"])
        price = base_budget + random.randint(-500, 300)
        walk = max(1, base_walk + random.randint(-2, 2))
        area = base_area + random.randint(-5, 10)
        
        layout_base = "3LDK" if area > 70 else "2LDK"
        layout_detail = layout_base + "+S(納戸)" if random.random() > 0.7 else layout_base
        
        props.append({
            "type": ptype,
            "price": f"{price:,}",
            "price_raw": price,
            "walk": walk,
            "area": area,
            "layout": layout_detail,
            "img": random.choice(images),
            "address": f"東京都{target_area}..." 
        })
    return props

def render_carousel(title, sub_title, properties, is_special=False, benefit_tags=None, card_badge=None):
    """横スクロールカルーセル表示 (SUUMO風)"""
    special_class = "special" if is_special else ""
    
    # AI提案ラベル
    label_html = ""
    if is_special:
        label_html = '<div class="ai-label">✨ AIのご提案</div>'
    
    # メリット強調バー
    benefit_html = ""
    if is_special and benefit_tags:
        benefit_html = f"""
        <div class="benefit-bar">
            <div class="benefit-tag tag-cond">{benefit_tags['condition']}</div>
            <span style="color:#ccc; font-size:0.8em;">▶</span>
            <div class="benefit-tag tag-gain">{benefit_tags['gain']}</div>
        </div>
        """

    cards_html = ""
    for p in properties:
        bg_style = f"background-image: url('{p['img']}');" if 'img' in p else ""
        
        # オーバーレイは削除済み。黒帯だけ表示
        type_label = f'<div class="type-label-black">{p["type"]}</div>'

        cards_html += f"""
        <div class="prop-card">
            <div class="prop-img" style="{bg_style}">
                <div class="badge-new-sash"></div>
                <div class="badge-new-text">未閲覧</div>
                <div class="fav-icon">♡</div>
                {type_label}
            </div>
            <div class="prop-info">
                <div class="prop-price">{p['price']}<span style="font-size:0.6em; font-weight:normal; color:#333;">万円</span></div>
                <div class="prop-layout">{p['layout']}</div>
                <div class="prop-detail">
                    {p['area']}㎡ / 目黒駅 歩{p['walk']}分
                </div>
            </div>
        </div>
        """
            
    html = f"""
    <div class="carousel-section {special_class}">
        {label_html}
        <div class="section-header">
            <div class="carousel-title">{title}</div>
            <div class="carousel-sub-title">{sub_title}</div>
            {benefit_html}
        </div>
        <div class="carousel-container">{cards_html}</div>
    </div>
    """
    st_html(html)

def render_1feed_card(props):
    """1feed用のリッチなカードUI (SUUMO詳細再現)"""
    html_items = ""
    for p in props:
        tags = ["3Dビュー", "ムービー", "2階建て", "駐車場2台", "LDK15畳", "都市ガス", "南向き", "食洗機", "浴室乾燥機"]
        tag_html = "".join([f'<span class="feed-tag-item">{t}</span>' for t in random.sample(tags, 5)])
        
        price_range = f"{p['price_raw']:,}万円<span style='color:#333;font-size:0.6em;font-weight:normal;'>〜</span>{p['price_raw']+500:,}万円"

        html_items += f"""
        <div class="feed-card">
            <div class="feed-header">
                <div class="feed-check-box"><span class="feed-check-mark">✓</span></div>
                <div>ザ・パークハウス{target_area}レジデンス {p['type']}</div>
            </div>
            <div class="feed-subheader">
                <span class="view-count">✓ 5回閲覧</span> お問い合わせしませんか？
            </div>
            <div class="feed-img-area" style="background-image: url('{p['img']}');">
                <span class="feed-badge-viewed">閲覧済</span>
                <span class="feed-badge-grey">建築条件付土地</span>
            </div>
            <div class="feed-content">
                <div class="visit-badge"><span class="visit-icon">👑</span>見学予約可</div>
                <div class="feed-price-row">
                    {price_range} <span class="price-update">価格更新</span>
                </div>
                <div class="feed-layout">{p['layout']}</div>
                <div class="feed-address">{p['address']}1-2-3</div>
                <div class="feed-access">東急目黒線「目黒」歩{p['walk']}分</div>
                <div class="feed-specs">
                    土地 {p['area']+20}㎡ (33.28坪)<br>
                    建物 {p['area']}㎡ (27.78坪)
                </div>
                <div class="feed-tags">{tag_html}</div>
                <div class="feed-action-btn">
                    <span class="btn-icon">♥</span> 追加済み
                </div>
            </div>
        </div>
        """
    st_html(f'<div class="feed-container">{html_items}</div>')


# --- 4. メイン処理 ---

render_header()
render_search_panel(hits_count, target_area, user_budget, user_walk, user_area)

if hits_count < THRESHOLD_STALLED:
    # === 停滞モード ===
    if 'prev_mode' not in st.session_state or st.session_state.prev_mode != 'stalled':
        with st.spinner("条件を広げて、より良い物件を探しています..."):
            time.sleep(0.5)
    st.session_state.prev_mode = 'stalled'

    # パターン選択
    selected_pattern = pattern_select
    if pattern_select == "Auto (自動判定)":
        if user_walk <= 10: selected_pattern = "Pattern A" 
        else: selected_pattern = "Pattern D"

    # --- パターンデータ ---
    if "Pattern A" in selected_pattern:
        shift_title = "徒歩15分圏内なら、+10㎡広い家があります"
        shift_sub = "予算は今のまま。部屋が一つ増える広さです。"
        b_tags = {"condition": f"条件変更: 徒歩{user_walk+5}分まで", "gain": f"面積 {user_area+15}㎡以上"}
        c_badge = "広々リビング"
        props = _generate_props(10, user_budget, user_walk+5, user_area+15)

    elif "Pattern B" in selected_pattern:
        shift_title = "築年数を広げると、駅徒歩5分以内が見つかります"
        shift_sub = "リノベーション済みのきれいな物件も豊富です。"
        b_tags = {"condition": "条件変更: 築25年まで", "gain": "駅徒歩 5分以内！"}
        c_badge = "駅チカ"
        props = _generate_props(10, user_budget-500, 4, user_area, age_override=25)

    elif "Pattern C" in selected_pattern:
        shift_title = "この予算なら「新築一戸建て」も手が届きます"
        shift_sub = "管理費・修繕積立金なし。駐車場付き物件も。"
        b_tags = {"condition": "種別変更: 新築一戸建て", "gain": "駐車場・庭付き"}
        c_badge = "駐車場・庭付"
        props = _generate_props(10, user_budget+300, user_walk+3, 95, p_type_override="新築一戸建て")

    elif "Pattern D" in selected_pattern:
        next_station = "用賀" if target_area == "世田谷区" else "武蔵小山"
        shift_title = f"隣の「{next_station}」なら、予算内で理想が叶います"
        shift_sub = "急行停車駅で、都心へのアクセスも良好です。"
        b_tags = {"condition": f"エリア変更: {next_station}", "gain": "相場 -500万円"}
        c_badge = "お買い得"
        props = _generate_props(10, user_budget-500, user_walk, user_area)
    
    else: # Pattern E
        added_budget = 500
        new_budget = user_budget + added_budget
        shift_title = f"あと{added_budget}万円出せば、今の希望条件ですべて見つかります"
        shift_sub = "人気エリア×駅近×広さ。すべてを叶える選択肢です。"
        b_tags = {"condition": f"予算変更: +{added_budget}万円", "gain": "希望条件 100%合致"}
        c_badge = "条件クリア"
        props = _generate_props(10, new_budget, user_walk, user_area)

    render_carousel(shift_title, shift_sub, props, is_special=True, benefit_tags=b_tags, card_badge=c_badge)
    
    st_html("<div class='feed-section-title' style='margin-top:20px; color:#666;'>その他の検討軸</div>")
    props_norm = _generate_props(8, user_budget, user_walk, user_area)
    render_carousel(f"{target_area}・築10年以内の物件", "築浅・駅近の物件", props_norm)

else:
    # === 通常モード ===
    st.session_state.prev_mode = 'normal'
    props1 = _generate_props(10, user_budget+500, user_walk+2, user_area)
    render_carousel(f"{target_area}・{user_budget+500:,}万円以下の物件", "予算を少し広げて探す", props1)
    
    props2 = _generate_props(10, user_budget, user_walk, user_area-5)
    render_carousel(f"{target_area}・駅徒歩{user_walk}分以内の物件", "駅近を重視する", props2)

# --- 1feed (共通) ---
st_html("<div class='feed-section-title' style='margin-top:20px;'>あなたにマッチした物件</div>")
feed_props = _generate_props(3, user_budget, user_walk, user_area)
render_1feed_card(feed_props)