"""
Gemby-Agent-3B SaaS Frontend v5 Final
=======================================
Streamlit secrets:
  GEMBY_API_URL      = "https://your-modal-url.modal.run"
  TRAKTEER_URL       = "https://trakteer.id/your-username/tip"
  SAWERIA_URL        = "https://saweria.co/your-username"
  ADMIN_TOKEN        = "your_admin_password"
  STRIPE_PUBLIC_KEY  = "pk_live_xxx"   (or pk_test_xxx for testing)
  STRIPE_STARTER_URL = "https://buy.stripe.com/xxx"
  STRIPE_PRO_URL     = "https://buy.stripe.com/xxx"
  STRIPE_UNLIMITED_URL = "https://buy.stripe.com/xxx"
"""

import streamlit as st
import requests, os, time

st.set_page_config(
    page_title="Gemby AI — API Access",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

GEMBY_API_URL        = os.environ.get("GEMBY_API_URL",        "https://your-modal-url.modal.run")
TRAKTEER_URL         = os.environ.get("TRAKTEER_URL",         "https://trakteer.id/your-username/tip")
SAWERIA_URL          = os.environ.get("SAWERIA_URL",          "https://saweria.co/your-username")
ADMIN_TOKEN          = os.environ.get("ADMIN_TOKEN",          "")
STRIPE_STARTER_URL   = os.environ.get("STRIPE_STARTER_URL",   "#")
STRIPE_PRO_URL       = os.environ.get("STRIPE_PRO_URL",       "#")
STRIPE_UNLIMITED_URL = os.environ.get("STRIPE_UNLIMITED_URL", "#")
ADMIN_EMAIL          = "emir.erningpraja@gmail.com"

PLANS = {
    "free":      {"price_idr": 0,        "price_usd": 0,   "daily_limit": "7 req/day",   "monthly_limit": "50 req/month", "label": "Free Trial", "emoji": "🆓"},
    "starter":   {"price_idr": 25_000,   "price_usd": 2,   "daily_limit": "50 req/day",  "monthly_limit": None,           "label": "Starter",    "emoji": "🌱"},
    "pro":       {"price_idr": 75_000,   "price_usd": 5,   "daily_limit": "300 req/day", "monthly_limit": None,           "label": "Pro",        "emoji": "⚡"},
    "unlimited": {"price_idr": 150_000,  "price_usd": 10,  "daily_limit": "Unlimited",   "monthly_limit": None,           "label": "Unlimited",  "emoji": "🚀"},
}

STRIPE_LINKS = {
    "starter":   STRIPE_STARTER_URL,
    "pro":       STRIPE_PRO_URL,
    "unlimited": STRIPE_UNLIMITED_URL,
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.hero{background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);border-radius:20px;padding:56px 36px;text-align:center;margin-bottom:36px;}
.hero h1{font-size:2.8rem;font-weight:800;color:#fff;margin:0;}
.hero p{font-size:1.1rem;color:#a0a0c0;margin:10px 0 0;}
.badge{display:inline-block;background:#00d4aa22;border:1px solid #00d4aa55;color:#00d4aa;padding:4px 16px;border-radius:999px;font-size:.78rem;font-weight:700;letter-spacing:1px;margin-bottom:14px;}
.plan-card{background:#1a1a2e;border:1px solid #2a2a4a;border-radius:16px;padding:26px 22px;text-align:center;height:100%;}
.plan-card.popular{border-color:#7c5cfc;background:#1e1a3a;}
.plan-card.free-card{border-color:#00d4aa55;background:#0d1a14;}
.price{font-size:1.9rem;font-weight:800;color:#fff;}
.price-sub{color:#666;font-size:.82rem;}
.limit{color:#00d4aa;font-weight:700;margin:8px 0 4px;}
.limit2{color:#888;font-size:.8rem;margin-bottom:8px;}
.pop-badge{background:#7c5cfc;color:#fff;font-size:.7rem;font-weight:700;padding:2px 10px;border-radius:999px;display:inline-block;margin-bottom:8px;}
.step-box{background:#1a1a2e;border:1px solid #2a2a4a;border-radius:14px;padding:20px 22px;margin:10px 0;}
.snum{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,#7c5cfc,#5c3cdc);font-size:.85rem;font-weight:800;color:#fff;margin-right:10px;flex-shrink:0;}
.key-box{background:#0d1a0d;border:2px solid #00d4aa66;border-radius:12px;padding:20px 24px;font-family:'JetBrains Mono',monospace;font-size:1rem;color:#00d4aa;word-break:break-all;margin:12px 0;}
.api-box{background:#0d0d1a;border:1px solid #2a2a4a;border-radius:12px;padding:18px 22px;font-family:'JetBrains Mono',monospace;font-size:.82rem;color:#e0e0ff;}
.ok-box  {background:#00d4aa11;border:1px solid #00d4aa33;border-radius:10px;padding:13px 17px;color:#a0f0e0;font-size:.88rem;margin:10px 0;}
.warn-box{background:#fc5c5c11;border:1px solid #fc5c5c33;border-radius:10px;padding:13px 17px;color:#ffb0b0;font-size:.88rem;margin:10px 0;}
.info-box{background:#7c5cfc11;border:1px solid #7c5cfc33;border-radius:10px;padding:13px 17px;color:#c0b0ff;font-size:.88rem;margin:10px 0;}
.stat-card{background:#1a1a2e;border:1px solid #2a2a4a;border-radius:12px;padding:18px 20px;text-align:center;}
.stat-num{font-size:2rem;font-weight:800;color:#7c5cfc;}
.stat-lbl{color:#888;font-size:.8rem;margin-top:4px;}
.admin-header{background:linear-gradient(135deg,#1a0a2e,#2a1050);border:1px solid #7c5cfc44;border-radius:14px;padding:20px 24px;margin-bottom:24px;}
.stripe-badge{display:inline-block;background:#635bff22;border:1px solid #635bff55;color:#a8a4ff;padding:3px 12px;border-radius:999px;font-size:.75rem;font-weight:700;margin-left:8px;}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "logged_in"  not in st.session_state: st.session_state.logged_in  = False
if "is_admin"   not in st.session_state: st.session_state.is_admin   = False
if "user_email" not in st.session_state: st.session_state.user_email = ""
if "user_key"   not in st.session_state: st.session_state.user_key   = ""
if "visited"    not in st.session_state:
    st.session_state.visited = True
    try: requests.post(f"{GEMBY_API_URL}/track/visit", json={"page":"home"}, timeout=5)
    except: pass

# ── Helpers ────────────────────────────────────────────────────────────────────
def api_post(path, payload=None, api_key=None):
    headers = {"Content-Type": "application/json"}
    if api_key: headers["x-api-key"] = api_key
    try:
        r = requests.post(f"{GEMBY_API_URL}{path}", json=payload, headers=headers, timeout=60)
        return r.status_code, r.json()
    except Exception as e:
        return 0, {"detail": str(e)}

def api_get(path, api_key=None, admin=False):
    headers = {}
    if api_key: headers["x-api-key"]     = api_key
    if admin:   headers["x-admin-token"] = ADMIN_TOKEN
    try:
        r = requests.get(f"{GEMBY_API_URL}{path}", headers=headers, timeout=15)
        return r.status_code, r.json()
    except Exception as e:
        return 0, {"detail": str(e)}

def do_login(email: str):
    s, resp = api_post("/auth/login", {"email": email.strip().lower()})
    if s == 200 and resp.get("success"):
        st.session_state.logged_in  = True
        st.session_state.is_admin   = resp.get("is_admin", False)
        st.session_state.user_email = email.strip().lower()
        st.session_state.user_key   = resp.get("api_key", "")
        return True, resp.get("message","")
    return False, resp.get("message","Login failed.")

def do_logout():
    for k in ["logged_in","is_admin","user_email","user_key"]:
        st.session_state[k] = False if k=="logged_in" or k=="is_admin" else ""

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 Gemby AI")
    st.markdown("---")
    if not st.session_state.logged_in:
        st.markdown("### 🔐 Login")
        email_in = st.text_input("Email address", placeholder="you@email.com", key="sidebar_email")
        if st.button("Login", type="primary", use_container_width=True):
            if email_in:
                with st.spinner("Checking..."):
                    ok, msg = do_login(email_in)
                if ok:
                    st.success(msg)
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.error("Enter your email first.")
        st.caption("New? Start a free trial in the Buy tab!")
    else:
        name = st.session_state.user_email.split("@")[0]
        st.markdown(f"### 👋 {name}")
        if st.session_state.is_admin:
            st.markdown("🛡️ **Admin** — unlimited access")
        else:
            st.markdown("✅ **Active subscriber**")
        st.markdown(f"`{st.session_state.user_email}`")
        if st.button("Logout", use_container_width=True):
            do_logout(); st.rerun()

# ── Tabs ───────────────────────────────────────────────────────────────────────
if st.session_state.is_admin:
    tab_home, tab_buy, tab_activate, tab_dash, tab_admin, tab_docs = st.tabs([
        "🏠 Home","💳 Buy","🔑 Activate","📊 Dashboard","🛡️ Admin","📖 Docs"
    ])
else:
    tab_home, tab_buy, tab_activate, tab_dash, tab_docs = st.tabs([
        "🏠 Home","💳 Buy","🔑 Activate","📊 Dashboard","📖 Docs"
    ])
    tab_admin = None


# ── HOME ───────────────────────────────────────────────────────────────────────
with tab_home:
    st.markdown("""
    <div class="hero">
      <div class="badge">CUSTOM ARCHITECTURE · 3B PARAMETERS · TRAINED FROM SCRATCH</div>
      <h1>🤖 Gemby AI API</h1>
      <p>A 3-billion parameter agentic AI built from scratch.<br>
         Web search · Tool use · Multi-step reasoning · JSON output.</p>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    for col,val,lbl in zip([c1,c2,c3,c4],["3B","28","4096","Apache 2.0"],
                           ["Parameters","Layers","Context Length","License"]):
        col.markdown(f"""<div style="background:#1a1a2e;border:1px solid #2a2a4a;border-radius:12px;
            padding:16px;text-align:center;">
          <div style="font-size:1.7rem;font-weight:800;color:#7c5cfc">{val}</div>
          <div style="color:#888;font-size:.8rem">{lbl}</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    f1,f2 = st.columns(2)
    with f1:
        st.markdown("### ✨ Features")
        for f in ["🔍 Web search via tool calls","🧠 Multi-step agentic planning",
                  "📝 Structured JSON output","🛠️ Custom tool schema support"]:
            st.markdown(f"**{f}**")
    with f2:
        st.markdown("### 🚀 Get started in 2 minutes")
        st.markdown("""<div class="step-box">
          <div style="display:flex;align-items:center;margin-bottom:10px">
            <div class="snum">1</div>
            <span style="color:#ccc">Go to <strong style="color:#fff">Buy</strong> tab →
            start free trial or buy a plan</span>
          </div>
          <div style="display:flex;align-items:center;margin-bottom:10px">
            <div class="snum">2</div>
            <span style="color:#ccc">Get your <strong style="color:#fff">API key</strong>
            shown on screen</span>
          </div>
          <div style="display:flex;align-items:center">
            <div class="snum">3</div>
            <span style="color:#ccc">Use Gemby in <strong style="color:#fff">any app</strong>
            — Python, JS, mobile, anything</span>
          </div></div>""", unsafe_allow_html=True)


# ── BUY ────────────────────────────────────────────────────────────────────────
with tab_buy:
    st.markdown("## 💳 Plans & Pricing")

    # Plan cards — all 4
    c1,c2,c3,c4 = st.columns(4)
    for col, (pid, info) in zip([c1,c2,c3,c4], PLANS.items()):
        with col:
            popular = pid == "pro"
            badge   = '<div class="pop-badge">⭐ POPULAR</div>' if popular else ""
            free_note = '<div style="color:#00d4aa;font-size:.75rem;margin-top:4px">No payment needed</div>' if pid=="free" else ""
            card_class = "free-card" if pid=="free" else ("popular" if popular else "")
            st.markdown(f"""<div class="plan-card {card_class}">
              {badge}
              <div style="font-size:1.8rem">{info['emoji']}</div>
              <div style="font-weight:700;color:#fff;margin:6px 0">{info['label']}</div>
              <div class="price">{'Free' if pid=='free' else f"Rp {info['price_idr']:,}"}</div>
              <div class="price-sub">{'/ month' if pid!='free' else '30 days'}</div>
              <div class="limit">{info['daily_limit']}</div>
              <div class="limit2">{info['monthly_limit'] if info['monthly_limit'] else 'No monthly cap'}</div>
              {free_note}
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Payment method selector
    pay_method = st.radio("How do you want to pay?",
        ["🆓 Free Trial (no payment)", "🇮🇩 GoPay / QRIS (Trakteer or Saweria)", "💳 Credit/Debit Card (Stripe)"],
        horizontal=False)

    # ── FREE TRIAL ────────────────────────────────────────────────────────────
    if "Free Trial" in pay_method:
        st.markdown("### 🆓 Start Your Free Trial")
        st.markdown("No payment needed. Just enter your email — get **7 requests/day, 50 requests/month**.")
        with st.form("free_trial_form"):
            ft_email = st.text_input("📧 Your email", placeholder="you@email.com")
            ft_btn   = st.form_submit_button("🚀 Start Free Trial", type="primary", use_container_width=True)
        if ft_btn:
            if not ft_email or "@" not in ft_email:
                st.error("❌ Enter a valid email.")
            else:
                with st.spinner("Setting up your free trial..."):
                    s, resp = api_post("/v1/free-trial", {"email": ft_email.strip().lower()})
                if s == 200:
                    api_key = resp.get("api_key","")
                    st.success("🎉 Free trial activated!")
                    st.markdown(f'<div class="key-box">{api_key}</div>', unsafe_allow_html=True)
                    st.code(api_key, language=None)
                    st.markdown("""<div class="ok-box">
                      ✅ <strong>7 requests/day · 50 requests/month · 30 days</strong><br>
                      Copy and save this key! Login with your email in the sidebar to access your dashboard.
                    </div>""", unsafe_allow_html=True)
                elif s == 400:
                    st.error(f"❌ {resp.get('detail','')}")
                else:
                    st.error(f"❌ Error ({s}): {resp.get('detail','')}")

    # ── GOPAY / QRIS ──────────────────────────────────────────────────────────
    elif "GoPay" in pay_method:
        st.markdown("### 🇮🇩 Pay with GoPay / QRIS")
        platform = st.radio("Platform:", ["☕ Trakteer.id","💛 Saweria.co"], horizontal=True)
        chosen_plan = st.selectbox("Plan:",
            options=["starter","pro","unlimited"],
            format_func=lambda x: f"{PLANS[x]['emoji']} {PLANS[x]['label']} — Rp {PLANS[x]['price_idr']:,}/month")
        plan_info = PLANS[chosen_plan]

        if "Trakteer" in platform:
            pay_url,pname,pbg,pfg,picon,order_ex = TRAKTEER_URL,"Trakteer","#ff6b35","#fff","☕","TKT-abc12345"
        else:
            pay_url,pname,pbg,pfg,picon,order_ex = SAWERIA_URL,"Saweria","#f5a623","#000","💛","SWR-xyz98765"

        st.markdown(f"""<div class="step-box">
          <div style="display:flex;align-items:flex-start;gap:12px;margin-bottom:12px">
            <div class="snum">1</div>
            <div><strong style="color:#fff">Open {pname} and pay exactly Rp {plan_info['price_idr']:,}</strong></div>
          </div>
          <a href="{pay_url}" target="_blank"
             style="display:inline-block;background:{pbg};color:{pfg};font-weight:700;
                    padding:11px 24px;border-radius:9px;text-decoration:none;font-size:.9rem">
            {picon} Open {pname} →
          </a>
        </div>
        <div class="step-box">
          <div style="display:flex;align-items:flex-start;gap:12px">
            <div class="snum">2</div>
            <div style="color:#aaa;font-size:.88rem">
              After paying, copy your <strong style="color:#fff">Order ID</strong>
              (like <code style="color:#00d4aa">{order_ex}</code>) →
              go to the <strong style="color:#fff">Activate</strong> tab and paste it.
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

    # ── STRIPE ────────────────────────────────────────────────────────────────
    else:
        st.markdown("### 💳 Pay with Credit / Debit Card")
        st.markdown('<span class="stripe-badge">Powered by Stripe</span>', unsafe_allow_html=True)
        st.markdown("International cards accepted. Instant activation after payment.")

        chosen_plan = st.selectbox("Plan:",
            options=["starter","pro","unlimited"],
            format_func=lambda x: f"{PLANS[x]['emoji']} {PLANS[x]['label']} — ${PLANS[x]['price_usd']}/month")
        plan_info   = PLANS[chosen_plan]
        stripe_url  = STRIPE_LINKS[chosen_plan]

        st.markdown(f"""<div class="step-box">
          <div style="display:flex;align-items:flex-start;gap:12px;margin-bottom:12px">
            <div class="snum">1</div>
            <div>
              <strong style="color:#fff">Click below to open Stripe checkout</strong><br>
              <span style="color:#aaa;font-size:.85rem">
                Pay ${plan_info['price_usd']}/month for {plan_info['emoji']} {plan_info['label']}.
                Use any credit or debit card.
              </span>
            </div>
          </div>
          <a href="{stripe_url}" target="_blank"
             style="display:inline-block;background:#635bff;color:#fff;font-weight:700;
                    padding:11px 24px;border-radius:9px;text-decoration:none;font-size:.9rem">
            💳 Pay with Stripe →
          </a>
        </div>
        <div class="step-box">
          <div style="display:flex;align-items:flex-start;gap:12px">
            <div class="snum">2</div>
            <div style="color:#aaa;font-size:.88rem">
              After paying, Stripe shows a <strong style="color:#fff">Session ID</strong>
              (starts with <code style="color:#00d4aa">cs_live_...</code>) →
              go to <strong style="color:#fff">Activate</strong> tab → pick <strong>Stripe</strong> →
              paste it with your email.
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="info-box">
          💡 <strong>Where does Stripe money go?</strong><br>
          Stripe pays out to your <strong>Indonesian bank account</strong> directly.
          Go to <code>dashboard.stripe.com</code> → Payouts → Add bank account → enter your BCA/BRI/Mandiri account.
          Payout happens every 2–7 days automatically.
        </div>""", unsafe_allow_html=True)


# ── ACTIVATE ───────────────────────────────────────────────────────────────────
with tab_activate:
    st.markdown("## 🔑 Activate Your API Key")
    st.markdown("Already paid? Get your API key here.")

    method = st.radio("Payment method:", ["GoPay/QRIS (Trakteer/Saweria)","Stripe (Credit Card)"], horizontal=True)

    if method == "GoPay/QRIS (Trakteer/Saweria)":
        with st.form("activate_gopay"):
            order_id     = st.text_input("📋 Order ID", placeholder="TKT-abc12345  or  SWR-xyz98765")
            user_email   = st.text_input("📧 Your email", placeholder="you@email.com")
            plan_sel     = st.selectbox("📦 Plan?", options=["starter","pro","unlimited"],
                format_func=lambda x: f"{PLANS[x]['emoji']} {PLANS[x]['label']} — Rp {PLANS[x]['price_idr']:,}/month", index=1)
            platform_sel = st.radio("💳 Platform?", ["trakteer","saweria"], horizontal=True,
                format_func=lambda x: "☕ Trakteer" if x=="trakteer" else "💛 Saweria")
            submitted    = st.form_submit_button("✅ Verify & Get Key", type="primary", use_container_width=True)

        if submitted:
            if not order_id.strip() or not user_email.strip() or "@" not in user_email:
                st.error("❌ Fill in all fields correctly.")
            else:
                with st.spinner("Verifying payment... ⏳"):
                    s, resp = api_post("/v1/activate", {
                        "order_id": order_id.strip(),
                        "plan":     plan_sel,
                        "platform": platform_sel,
                        "email":    user_email.strip().lower(),
                    })
                if s == 200:
                    api_key = resp.get("api_key","")
                    st.success("🎉 Payment verified!")
                    st.markdown(f'<div class="key-box">{api_key}</div>', unsafe_allow_html=True)
                    st.code(api_key, language=None)
                    st.markdown(f"""<div class="ok-box">
                      ✅ {PLANS[plan_sel]['emoji']} {PLANS[plan_sel]['label']} ·
                      {PLANS[plan_sel]['daily_limit']} · Valid until: {resp.get('expires_at','')[:10]}
                    </div>
                    <div class="info-box">⚠️ <strong>Copy and save this key now!</strong>
                      Login with <code>{user_email}</code> in the sidebar to access your dashboard anytime.
                    </div>""", unsafe_allow_html=True)
                elif s == 402:
                    st.error(f"❌ Payment not verified: {resp.get('detail','')}")
                    st.markdown("""<div class="warn-box"><strong>Check:</strong>
                      Order ID exact? Right platform? Right plan amount? Already used?</div>""", unsafe_allow_html=True)
                else:
                    st.error(f"❌ Error ({s}): {resp.get('detail','')}")

    else:  # Stripe
        with st.form("activate_stripe"):
            session_id   = st.text_input("📋 Stripe Session ID", placeholder="cs_live_xxxxxxxx or cs_test_xxxxxxxx")
            stripe_email = st.text_input("📧 Email you used on Stripe", placeholder="you@email.com")
            stripe_plan  = st.selectbox("📦 Plan?", options=["starter","pro","unlimited"],
                format_func=lambda x: f"{PLANS[x]['emoji']} {PLANS[x]['label']} — ${PLANS[x]['price_usd']}/month", index=1)
            submitted_s  = st.form_submit_button("✅ Verify Stripe & Get Key", type="primary", use_container_width=True)

        if submitted_s:
            if not session_id.strip() or not stripe_email.strip() or "@" not in stripe_email:
                st.error("❌ Fill in all fields.")
            elif not session_id.strip().startswith("cs_"):
                st.error("❌ Session ID should start with cs_live_ or cs_test_")
            else:
                with st.spinner("Verifying Stripe payment... ⏳"):
                    s, resp = api_post("/v1/activate-stripe", {
                        "session_id": session_id.strip(),
                        "plan":       stripe_plan,
                        "email":      stripe_email.strip().lower(),
                    })
                if s == 200:
                    api_key = resp.get("api_key","")
                    st.success("🎉 Stripe payment verified!")
                    st.markdown(f'<div class="key-box">{api_key}</div>', unsafe_allow_html=True)
                    st.code(api_key, language=None)
                    st.markdown(f"""<div class="ok-box">
                      ✅ {PLANS[stripe_plan]['emoji']} {PLANS[stripe_plan]['label']} ·
                      {PLANS[stripe_plan]['daily_limit']} · Valid until: {resp.get('expires_at','')[:10]}
                    </div>""", unsafe_allow_html=True)
                elif s == 402:
                    st.error(f"❌ Payment not verified: {resp.get('detail','')}")
                else:
                    st.error(f"❌ Error ({s}): {resp.get('detail','')}")


# ── DASHBOARD ──────────────────────────────────────────────────────────────────
with tab_dash:
    st.markdown("## 📊 My Dashboard")
    if not st.session_state.logged_in:
        st.markdown("""<div class="info-box">
          🔐 <strong>Login in the sidebar</strong> to auto-load your dashboard,
          or enter your API key manually below.
        </div>""", unsafe_allow_html=True)

    default_key = st.session_state.user_key if st.session_state.logged_in else ""
    key_in = st.text_input("🔑 API Key", value=default_key,
                           placeholder="gmb_xxxxxxxxxxxx", type="password")
    if key_in:
        with st.spinner("Loading..."):
            s, data = api_get("/v1/usage", api_key=key_in)
        if s == 200:
            is_admin_key = data.get("is_admin", False)
            plan_id      = data.get("plan","?")

            st.success(f"✅ Valid key — {PLANS.get(plan_id,{}).get('emoji','')} {PLANS.get(plan_id,{}).get('label', plan_id.upper())}")

            if is_admin_key:
                st.markdown("""<div class="ok-box">
                  🛡️ <strong>Admin key — unlimited requests, never expires.</strong>
                </div>""", unsafe_allow_html=True)

            c1,c2,c3,c4 = st.columns(4)
            c1.metric("Plan",          PLANS.get(plan_id,{}).get("label", plan_id.upper()))
            c2.metric("Used Today",    f"{data.get('used_today',0)} / {data.get('daily_limit','∞')}")
            c3.metric("Total Calls",   data.get("used_total",0))
            c4.metric("Expires",       data.get("expires_at","never")[:10] if data.get("expires_at") else "never")

            if not is_admin_key:
                lim = data.get("daily_limit", 1)
                if isinstance(lim, int) and lim > 0:
                    st.progress(min(data.get("used_today",0)/lim,1.0), text="Daily quota")

            # Monthly limit bar for free plan
            if plan_id == "free":
                monthly_limit = 50
                used_month    = data.get("used_this_month", 0)
                st.progress(min(used_month/monthly_limit,1.0),
                            text=f"Monthly quota: {used_month}/{monthly_limit}")
                if used_month >= monthly_limit:
                    st.markdown("""<div class="warn-box">
                      ⚠️ <strong>Monthly limit reached!</strong>
                      Upgrade to a paid plan to keep using Gemby.
                    </div>""", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### 🧪 Test Gemby Live")
            prompt = st.text_area("Prompt","What is 2 + 2?", height=80)
            if st.button("▶ Run", type="primary"):
                with st.spinner("Running Gemby — first call may take ~30s..."):
                    s2,r2 = api_post("/v1/generate",{"prompt":prompt,"max_tokens":128},api_key=key_in)
                if s2==200:
                    st.markdown(f'<div class="api-box">{r2.get("output","")}</div>', unsafe_allow_html=True)
                else:
                    st.error(f"Error {s2}: {r2.get('detail','')}")

            st.markdown("---")
            st.markdown(f'<div class="key-box">{key_in}</div>', unsafe_allow_html=True)
            st.caption("⚠️ Never share this key!")
        elif s==401: st.error("❌ Invalid API key.")
        elif s==403: st.error("❌ Key expired. Buy a new plan.")
        else:        st.error(f"❌ Server unreachable ({s}).")


# ── ADMIN DASHBOARD ────────────────────────────────────────────────────────────
if tab_admin and st.session_state.is_admin:
    with tab_admin:
        st.markdown("""<div class="admin-header">
          <h2 style="color:#fff;margin:0">🛡️ Admin Dashboard</h2>
          <p style="color:#a0a0c0;margin:4px 0 0">Real-time stats — Gemby AI SaaS</p>
        </div>""", unsafe_allow_html=True)

        if st.button("🔄 Refresh", type="primary"): st.rerun()

        with st.spinner("Loading..."):
            s, stats = api_get("/admin/stats", admin=True)

        if s == 200:
            st.markdown("### 👥 Traffic")
            c1,c2,c3,c4 = st.columns(4)
            c1.markdown(f'<div class="stat-card"><div class="stat-num">{stats.get("total_visits",0):,}</div><div class="stat-lbl">Total Visits</div></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="stat-card"><div class="stat-num">{stats.get("visits_today",0):,}</div><div class="stat-lbl">Visits Today</div></div>', unsafe_allow_html=True)
            c3.markdown(f'<div class="stat-card"><div class="stat-num">{stats.get("total_logins",0):,}</div><div class="stat-lbl">Total Logins</div></div>', unsafe_allow_html=True)
            c4.markdown(f'<div class="stat-card"><div class="stat-num">{stats.get("logins_today",0):,}</div><div class="stat-lbl">Logins Today</div></div>', unsafe_allow_html=True)

            visits_7d = stats.get("visits_7d",{})
            if visits_7d:
                import pandas as pd
                df = pd.DataFrame({"Date":list(visits_7d.keys()),
                    "Visits":list(visits_7d.values()),
                    "Logins":[stats.get("logins_7d",{}).get(d,0) for d in visits_7d]})
                st.markdown("### 📈 Last 7 Days")
                st.bar_chart(df.set_index("Date"))

            st.markdown("---")
            st.markdown("### 💰 Revenue & Subscriptions")
            c1,c2,c3,c4 = st.columns(4)
            rev = stats.get("estimated_revenue",0)
            c1.markdown(f'<div class="stat-card"><div class="stat-num" style="color:#00d4aa">Rp {rev:,}</div><div class="stat-lbl">Est. Monthly Revenue</div></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="stat-card"><div class="stat-num">{stats.get("active_keys",0)}</div><div class="stat-lbl">Active Subscribers</div></div>', unsafe_allow_html=True)
            c3.markdown(f'<div class="stat-card"><div class="stat-num">{stats.get("total_keys",0)}</div><div class="stat-lbl">Total Keys Issued</div></div>', unsafe_allow_html=True)
            c4.markdown(f'<div class="stat-card"><div class="stat-num">{stats.get("requests_today",0):,}</div><div class="stat-lbl">API Calls Today</div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            pb = stats.get("plan_breakdown",{})
            st.markdown("### 📦 Plan Breakdown")
            cols = st.columns(4)
            for col,(pid,pinfo) in zip(cols, PLANS.items()):
                count = pb.get(pid,0)
                col.markdown(f'<div class="stat-card"><div style="font-size:1.3rem">{pinfo["emoji"]}</div><div class="stat-num">{count}</div><div class="stat-lbl">{pinfo["label"]}</div></div>', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### 🕐 Recent Subscriptions")
            recent = stats.get("recent_keys",[])
            if recent:
                import pandas as pd
                df2 = pd.DataFrame(recent)
                df2["status"] = df2["active"].map({True:"✅ Active",False:"❌ Expired"})
                df2 = df2[["plan","created_at","expires_at","usage_total","status"]]
                df2.columns = ["Plan","Created","Expires","Total Calls","Status"]
                st.dataframe(df2, use_container_width=True, hide_index=True)

            st.markdown("---")
            st.markdown("### ⚙️ Create Key Manually")
            with st.form("admin_create"):
                ac1,ac2,ac3 = st.columns(3)
                with ac1:
                    new_plan = st.selectbox("Plan", options=list(PLANS.keys()),
                        format_func=lambda x: f"{PLANS[x]['emoji']} {PLANS[x]['label']}")
                with ac2:
                    new_email = st.text_input("Customer email", placeholder="customer@email.com")
                with ac3:
                    st.markdown("<br>", unsafe_allow_html=True)
                    create_btn = st.form_submit_button("➕ Create Key", type="primary")

            if create_btn and new_email:
                try:
                    resp2 = requests.post(f"{GEMBY_API_URL}/admin/create-key",
                        json={"plan": new_plan, "note": new_email.strip().lower()},
                        headers={"x-admin-token": ADMIN_TOKEN, "Content-Type":"application/json"},
                        timeout=15)
                    r2 = resp2.json()
                    if resp2.status_code == 200:
                        st.success("✅ Key created!")
                        st.code(r2.get("api_key",""))
                        expires_label = "Never" if new_plan == "admin" else r2.get("expires_at","")[:10]
                        st.caption(f"Plan: {r2.get('plan')} · Expires: {expires_label}")
                    else:
                        st.error(f"Error {resp2.status_code}: {r2.get('detail','')}")
                except Exception as e:
                    st.error(str(e))
        else:
            st.error(f"Failed to load stats ({s}). Check ADMIN_TOKEN secret.")


# ── API DOCS ───────────────────────────────────────────────────────────────────
with tab_docs:
    st.markdown("## 📖 API Documentation")
    st.markdown(f"**Base URL:** `{GEMBY_API_URL}`")
    st.markdown("**Auth:** Add header `x-api-key: YOUR_KEY` to every request.")
    st.markdown("### `POST /v1/generate`")
    c1,c2 = st.columns(2)
    with c1:
        st.code('{\n  "prompt": "Hello Gemby!",\n  "max_tokens": 256\n}', language="json")
    with c2:
        st.code('{\n  "output": "Hello! How can I help?",\n  "tokens_used": 8,\n  "model": "gemby-agent-3b"\n}', language="json")
    st.markdown("### Python")
    st.code(f"""import requests
r = requests.post(
    "{GEMBY_API_URL}/v1/generate",
    headers={{"x-api-key": "gmb_your_key"}},
    json={{"prompt": "Hello!", "max_tokens": 128}},
    timeout=60,
)
print(r.json()["output"])""", language="python")
    st.markdown("### Error Codes")
    st.table({"Code":[200,401,403,429,500],
              "Meaning":["OK","Invalid key","Expired","Quota reached (daily or monthly)","Server error"]})
