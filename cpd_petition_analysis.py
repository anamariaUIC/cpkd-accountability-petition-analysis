import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Locked Out: CPD Accountability Petition Analysis",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Palette ───────────────────────────────────────────────────────────────────
TEAL   = "#1D9E75"
AMBER  = "#BA7517"
CORAL  = "#D85A30"
PURPLE = "#534AB7"
BLUE   = "#185FA5"
GREEN  = "#639922"
RED    = "#A32D2D"
PINK   = "#993556"
CATEGORY_COLORS = [TEAL, AMBER, CORAL, PURPLE, BLUE, GREEN, RED, PINK]

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap');

html, body, div, p, span, button, label, input,
[class^="st"], [class*=" st"], .stMarkdown, .stRadio,
.element-container, .block-container {
    font-family: 'DM Sans', sans-serif !important;
}
.main .block-container { padding-top: 1.5rem; padding-bottom: 3rem; }

/* Executive narrative */
.exec-box {
    background: #f0f7f4;
    border-left: 4px solid #1D9E75;
    border-radius: 0 10px 10px 0;
    padding: 1.2rem 1.5rem;
    margin-bottom: 2rem;
}
.exec-box .exec-label {
    font-size: 10px; font-weight: 600; color: #1D9E75;
    text-transform: uppercase; letter-spacing: 1px; margin: 0 0 6px;
}
.exec-box .exec-text {
    font-size: 15.5px; font-weight: 500; color: #1a1a18;
    line-height: 1.65; margin: 0 0 10px;
}
.exec-box .exec-sub {
    font-size: 13px; color: #5F5E5A; line-height: 1.6; margin: 0;
}

/* Metric cards */
.metric-card {
    background: #f8f7f4; border-radius: 10px;
    padding: 1.1rem 1.3rem; min-height: 100px;
}
.metric-label {
    font-size: 10px; color: #888780; margin: 0 0 4px;
    font-weight: 600; letter-spacing: .5px; text-transform: uppercase;
}
.metric-value { font-size: 32px; font-weight: 600; margin: 0; line-height: 1.1; }
.metric-sub   { font-size: 12px; color: #888780; margin: 5px 0 0; }

/* Section headers */
.sec-header {
    font-size: 16px; font-weight: 600; color: #1a1a18;
    margin: 0 0 0.6rem; padding-bottom: 8px;
    border-bottom: 1.5px solid #e5e3de;
}
.sec-sub {
    font-size: 13px; color: #5F5E5A; margin: -0.2rem 0 1rem; line-height: 1.5;
}

/* Impact callout */
.impact-callout {
    background: #0F6E56; border-radius: 12px;
    padding: 1.6rem 1.8rem; color: #fff; margin-bottom: 1.2rem;
}
.impact-callout .ic-num {
    font-size: 52px; font-weight: 700; line-height: 1; margin: 0 0 4px; color: #fff;
}
.impact-callout .ic-label {
    font-size: 13px; font-weight: 500; color: rgba(255,255,255,0.85); margin: 0 0 12px;
}
.impact-callout .ic-desc {
    font-size: 12.5px; color: rgba(255,255,255,0.75); line-height: 1.55; margin: 0;
    border-top: 1px solid rgba(255,255,255,0.2); padding-top: 10px;
}
.nbhd-row {
    display: flex; align-items: center; gap: 8px; margin-bottom: 6px;
}
.nbhd-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.nbhd-name { font-size: 12.5px; color: #2c2c2a; flex: 1; }
.nbhd-count {
    font-size: 12px; font-weight: 600; color: #1a1a18;
    background: #f0ede8; border-radius: 4px; padding: 1px 6px;
}

/* Intensity */
.intensity-wrap { margin-top: 0.5rem; }
.irow { display: flex; align-items: center; gap: 10px; margin-bottom: 9px; }
.ilabel { font-size: 13px; color: #5F5E5A; width: 100px; flex-shrink: 0; text-align: right; }
.ibwrap { flex: 1; height: 18px; background: #f0ede8; border-radius: 4px; overflow: hidden; }
.ibar { height: 100%; border-radius: 4px; }
.ival { font-size: 13px; font-weight: 500; color: #1a1a18; width: 28px; flex-shrink: 0; }

/* Quote cards */
.qcard {
    background: #fff; border: 1px solid #e5e3de;
    border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 12px;
}
.badge {
    display: inline-block; font-size: 10px; padding: 2px 9px;
    border-radius: 6px; font-weight: 600; letter-spacing: .3px; margin-bottom: 8px;
}
.qt { font-size: 13.5px; color: #2c2c2a; line-height: 1.7; font-style: italic; margin: 0; }

/* Stat pair */
.stat-pair { background: #f8f7f4; border-radius: 10px; padding: .9rem 1rem; text-align: center; }
.stat-pair .sp-label { font-size: 10px; color: #888780; font-weight: 600; text-transform: uppercase; letter-spacing: .4px; margin: 0 0 3px; }
.stat-pair .sp-val   { font-size: 26px; font-weight: 600; margin: 0; line-height: 1; }

/* Footer */
.footer {
    margin-top: 3rem; padding-top: 1.2rem; border-top: 1px solid #e5e3de;
    font-size: 12px; color: #888780; line-height: 1.8;
}
.footer strong { color: #444441; }
</style>
""", unsafe_allow_html=True)

def base_layout(**kwargs):
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#444441"),
        margin=dict(l=10, r=20, t=10, b=10),
        **kwargs,
    )

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<h1 style="font-size:26px;font-weight:700;color:#1a1a18;margin-bottom:.15rem">
    Locked Out: Public Voice on Chicago Park District Accountability
</h1>
<p style="font-size:12px;color:#888780;margin-bottom:1.4rem">
    Analysis of 923 petition signers and 272 resident comments &nbsp;·&nbsp;
    Data source: public petition submitted to the Chicago Park District &nbsp;·&nbsp;
    January – May 2026
</p>
""", unsafe_allow_html=True)

# ── EXECUTIVE NARRATIVE ───────────────────────────────────────────────────────
st.markdown("""
<div class="exec-box">
  <p class="exec-label">Key finding</p>
  <p class="exec-text">
    Residents overwhelmingly describe the parking gates as a threat to public access, an unfair financial
    burden, and a visible example of unequal treatment toward South and Southeast Side communities —
    with 271 of 272 commenters critical of Chicago Park District governance.
  </p>
  <p class="exec-sub">
    This is not a disagreement about parking fees. Residents perceive CPD governance as increasingly
    monetizing and restricting access to shared public lakefront space while failing to maintain
    transparency, equity, and community trust. The strongest voices come from directly impacted
    communities: disabled residents, seniors on fixed incomes, and Black South Side neighborhoods
    that already receive fewer park resources than their North Side counterparts.
  </p>
</div>
""", unsafe_allow_html=True)

# ── SUMMARY METRICS ───────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
metrics = [
    (c1, "Total signers",          "923",    "#1a1a18", "89% from Chicago"),
    (c2, "Signers with comments",  "272",    "#1a1a18", "29% comment rate"),
    (c3, "South Side ZIPs",        "64.8%",  "#1a1a18", "598 of 923 directly impacted"),
    (c4, "Comments in opposition", "1",      CORAL,     "of 272 — effectively 0%"),
]
for col, label, val, color, sub in metrics:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">{label}</p>
            <p class="metric-value" style="color:{color}">{val}</p>
            <p class="metric-sub">{sub}</p>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# GRIEVANCE CHART — CENTERPIECE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="sec-header">What are residents actually upset about?</p>', unsafe_allow_html=True)
st.markdown("""<p class="sec-sub">
Each comment was classified by its primary grievance. A single comment could reflect multiple themes —
the chart shows the reach of each concern across the full comment set.
</p>""", unsafe_allow_html=True)

grievance_labels = [
    "Public access rights",
    "Tax / public spending",
    "Anger & frustration",
    "Community exclusion & inequity",
    "Transparency & process failures",
    "Fear of downstream impacts",
    "Distrust of government",
    "Volunteer / PAC accountability",
]
grievance_values = [111, 66, 49, 43, 41, 32, 29, 27]
grievance_pct    = [f"{v/272*100:.1f}%" for v in grievance_values]
grievance_ann    = [
    "Gates threaten the public's right to shared lakefront space",
    "Residents already pay taxes — fees are double taxation",
    "Outrage at decisions made without community input",
    "North Side parks don't face these restrictions",
    "No public forum; no clear rules; no disclosure of funds",
    "Concerns about ADA access, health, and community wellbeing",
    "CPD seen as unaccountable and unresponsive",
    "Volunteer suspension seen as punitive and chilling",
]

fig_griev = go.Figure(go.Bar(
    x=grievance_values,
    y=grievance_labels,
    orientation="h",
    marker_color=CATEGORY_COLORS,
    text=[f"  {p}  ({v} comments)" for p, v in zip(grievance_pct, grievance_values)],
    textposition="outside",
    textfont=dict(size=11.5, color="#444441"),
    customdata=grievance_ann,
    hovertemplate="<b>%{y}</b><br>%{x} comments<br><i>%{customdata}</i><extra></extra>",
))
fig_griev.update_layout(
    **base_layout(height=420),
    xaxis=dict(showgrid=True, gridcolor="#ece9e4", tickfont=dict(size=11),
               title=dict(text="number of comments", font=dict(size=11)), range=[0, 160]),
    yaxis=dict(showgrid=False, tickfont=dict(size=12.5, color="#1a1a18"), autorange="reversed"),
)
st.plotly_chart(fig_griev, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# GEOGRAPHIC — IMPACT CALLOUT + BAR CHART
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="sec-header">Who is signing — and where do they live?</p>', unsafe_allow_html=True)
st.markdown("""<p class="sec-sub">
The frustration is not citywide noise. It is concentrated in the communities that are directly in the shadow of these decisions.
</p>""", unsafe_allow_html=True)

geo_col1, geo_col2 = st.columns([1, 2])

with geo_col1:
    st.markdown(f"""
    <div class="impact-callout">
        <p class="ic-num">64.8%</p>
        <p class="ic-label">of all signers live in South &amp; Southeast Side ZIP codes</p>
        <p class="ic-desc">
            These are the neighborhoods within walking distance of Rainbow Beach and the lakefront parks
            directly affected by the gate installation. Residents are not signing from a distance —
            they are signing because this is their park.
        </p>
    </div>
    """, unsafe_allow_html=True)

    top_nbhds = [
        ("#0F6E56", "South Shore",            183),
        ("#1D9E75", "SE Side / S. Chicago",   129),
        ("#3DB58A", "Hyde Park / Woodlawn",    67),
        ("#5DCAA5", "Chatham / Avalon Park",   57),
        ("#7DD9BC", "Woodlawn / Gr. Crossing", 53),
    ]
    rows = "".join(f"""
    <div class="nbhd-row">
      <div class="nbhd-dot" style="background:{c}"></div>
      <span class="nbhd-name">{n}</span>
      <span class="nbhd-count">{v}</span>
    </div>""" for c, n, v in top_nbhds)
    st.markdown(f'<div style="margin-top:0">{rows}</div>', unsafe_allow_html=True)

with geo_col2:
    geo_labels = [
        "South Shore (60649)",
        "SE Side / S. Chicago (60617)",
        "Hyde Park / Woodlawn (60615)",
        "Chatham / Avalon Park (60619)",
        "Woodlawn / Gr. Crossing (60637)",
        "Bronzeville / Douglas (60653)",
        "Auburn Gresham (60620)",
        "Roseland / Pullman (60628)",
        "Beverly / Morgan Park (60643)",
    ]
    geo_values = [183, 129, 67, 57, 53, 41, 25, 23, 20]
    geo_colors = ["#0F6E56","#1D9E75","#3DB58A","#5DCAA5","#7DD9BC","#9FE1CB","#B8EDD9","#B8EDD9","#B8EDD9"]

    fig_geo = go.Figure(go.Bar(
        x=geo_values, y=geo_labels, orientation="h",
        marker_color=geo_colors,
        text=geo_values, textposition="outside",
        textfont=dict(size=11, color="#444441"),
        hovertemplate="%{y}: %{x} signers<extra></extra>",
    ))
    fig_geo.update_layout(
        **base_layout(height=360),
        xaxis=dict(showgrid=True, gridcolor="#ece9e4", tickfont=dict(size=11),
                   title=dict(text="number of signers", font=dict(size=11)), range=[0, 215]),
        yaxis=dict(showgrid=False, tickfont=dict(size=11.5), autorange="reversed"),
    )
    st.plotly_chart(fig_geo, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# THEME FREQUENCY + INTENSITY + OPPOSITION
# ══════════════════════════════════════════════════════════════════════════════
col_kw, col_int = st.columns(2)

with col_kw:
    st.markdown('<p class="sec-header">Most repeated concepts</p>', unsafe_allow_html=True)
    kw_labels = ['"pay / fees"','"free / public"','"access"','"parking"','"tax / taxpayer"',
                 '"community"','"gate"','"barrier"','"accountability"','"South Shore"','"transparency"','"volunteer"']
    kw_values = [55, 48, 46, 42, 36, 27, 26, 17, 13, 12, 12, 11]
    fig_kw = go.Figure(go.Bar(
        x=kw_values, y=kw_labels, orientation="h",
        marker_color=BLUE,
        text=kw_values, textposition="outside",
        textfont=dict(size=11, color="#444441"),
        hovertemplate="%{y}: %{x} comments<extra></extra>",
    ))
    fig_kw.update_layout(
        **base_layout(height=400),
        xaxis=dict(showgrid=True, gridcolor="#ece9e4", tickfont=dict(size=10),
                   title=dict(text="comments", font=dict(size=10)), range=[0, 68]),
        yaxis=dict(showgrid=False, tickfont=dict(size=11.5), autorange="reversed"),
    )
    st.plotly_chart(fig_kw, use_container_width=True)

with col_int:
    st.markdown('<p class="sec-header">Issue intensity — urgency language</p>', unsafe_allow_html=True)
    urgency = [
        ("stop",        24, 100),
        ("please",      20, 83),
        ("remove",      11, 46),
        ("why",         11, 46),
        ("unfair",      10, 42),
        ("enough",       8, 33),
        ("ridiculous",   6, 25),
        ("demand",       5, 21),
    ]
    rows_html = "".join(f"""
    <div class="irow">
      <span class="ilabel">"{w}"</span>
      <div class="ibwrap"><div class="ibar" style="width:{pct}%;background:{CORAL}"></div></div>
      <span class="ival">{cnt}</span>
    </div>""" for w, cnt, pct in urgency)
    st.markdown(f'<div class="intensity-wrap" style="margin-top:0.3rem">{rows_html}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    ia, ib, ic = st.columns(3)
    with ia:
        st.markdown(f"""<div class="stat-pair">
          <p class="sp-label">! points</p>
          <p class="sp-val" style="color:{CORAL}">94</p>
        </div>""", unsafe_allow_html=True)
    with ib:
        st.markdown(f"""<div class="stat-pair">
          <p class="sp-label">CAPS words</p>
          <p class="sp-val" style="color:{CORAL}">111</p>
        </div>""", unsafe_allow_html=True)
    with ic:
        st.markdown(f"""<div class="stat-pair">
          <p class="sp-label">Opposed</p>
          <p class="sp-val" style="color:{CORAL}">1</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    fig_opp = go.Figure(go.Pie(
        labels=["Critical / supportive", "Opposed"],
        values=[271, 1], hole=0.65,
        marker=dict(colors=[TEAL, CORAL], line=dict(width=0)),
        textinfo="none",
        hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
    ))
    opp_layout = base_layout(height=180)
    opp_layout["margin"] = dict(l=0, r=0, t=5, b=0)
    fig_opp.update_layout(
        **opp_layout, showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5,
                    font=dict(size=11)),
        annotations=[dict(
            text="<b>99.6%</b><br>supportive",
            x=0.5, y=0.5, showarrow=False, align="center",
            font=dict(family="DM Sans", size=14, color="#1a1a18"),
        )],
    )
    st.plotly_chart(fig_opp, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CURATED RESIDENT VOICES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="sec-header">Resident voices — curated quotes</p>', unsafe_allow_html=True)
st.markdown("""<p class="sec-sub">
Selected for strength of moral framing, equity argument, accessibility concern, and public commons reasoning.
Filter by theme to read across each dimension.
</p>""", unsafe_allow_html=True)

QUOTES = [
    # ── Taxes & fees ──────────────────────────────────────────────────────────
    ("taxes", "#FAEEDA", "#633806", "Taxes & fees",
     "Stop the money grab! Make parking at all parks and lakefront locations free like it was for years. Chicago is always taking from the people and giving very little in return. All of this excess money is lining politicians' pockets."),
    ("taxes", "#FAEEDA", "#633806", "Taxes & fees",
     "Not only are they starting to charge — they're not disclosing what the funds will be going towards. Truly disappointing. In a neighborhood where the average income is about $40,000 a year."),
    ("taxes", "#FAEEDA", "#633806", "Taxes & fees",
     "It's a disgrace to put physical barriers on a FREE PARK that is paid for and maintained with OUR TAX MONEY."),
    ("taxes", "#FAEEDA", "#633806", "Taxes & fees",
     "A stealth tax if there ever was one — it just appeared out of nowhere."),

    # ── Race & equity ─────────────────────────────────────────────────────────
    ("equity", "#EEEDFE", "#26215C", "Race & equity",
     "What year is it — why aren't we letting Black people swim and enjoy the same NATURAL RESOURCES we on the north side get to access for free? Shameful and horrifying."),
    ("equity", "#EEEDFE", "#26215C", "Race & equity",
     "Chicago beaches are one of the last third spaces available to all residents no matter their zip code or economic status. Monetized parking and cryptic financial record keeping disproportionately targets lower income, elderly, and disabled Chicagoans."),
    ("equity", "#EEEDFE", "#26215C", "Race & equity",
     "Treating our PACs differently, limiting access to programs, obstructing grants, forcing us to pay for things North Side parks get for free and taking punitive actions based on obscure rules not used against others is DISCRIMINATORY."),
    ("equity", "#EEEDFE", "#26215C", "Race & equity",
     "Our parks are always last in everything — restorations, clean up, beautification and care. We are the first to have to pay for parking and closed gates."),

    # ── Disability & seniors ──────────────────────────────────────────────────
    ("disability", "#E1F5EE", "#04342C", "Disability & seniors",
     "I am a disabled senior living in South Shore on a fixed income. My main way of exercising for my health is walking or e-biking in the nearby parks. I cannot afford to pay parking fees to visit the parks in my own neighborhood."),
    ("disability", "#E1F5EE", "#04342C", "Disability & seniors",
     "I'm a wheelchair user with a yellow placard. There are few accessible spots along the lake and now they are behind the gate. I feel it's discriminatory to place this burden on disabled people."),
    ("disability", "#E1F5EE", "#04342C", "Disability & seniors",
     "As someone with a mobility disability who often parked in Rainbow Beach's North lot for physical therapy walks, this directly impedes my access. Even the ability to pay via the app is prohibitive for residents who don't have smart phones."),

    # ── Public commons ────────────────────────────────────────────────────────
    ("commons", "#E6F1FB", "#042C53", "Public commons",
     "What happened to the plan for the lakefront to be 'forever open and free'? Steep parking fees privatize the lakefront just as assuredly as building privately owned buildings on the shoreline would."),
    ("commons", "#E6F1FB", "#042C53", "Public commons",
     "These new gates are denying us — the public — the right to enjoy the very lakefront which was by law to be forever free and open."),
    ("commons", "#E6F1FB", "#042C53", "Public commons",
     "Rainbow Beach is my nearest park. The programming last year was amazing — residents in South Shore suddenly had access to events typically only offered in wealthier northside parks. That the person who spearheaded these experiences is now suspended without prior notice is unconscionable."),

    # ── Transparency ──────────────────────────────────────────────────────────
    ("transparency", "#FAECE7", "#4A1B0C", "Transparency",
     "Was there a public forum held prior to installation? Who decided that this was needed? Where is the money going?"),
    ("transparency", "#FAECE7", "#4A1B0C", "Transparency",
     "We, the public, deserve full transparency in ALL matters pertaining to OUR PUBLIC LANDS. The rules must be clearly written and published in plain language. There must be a response process."),
    ("transparency", "#FAECE7", "#4A1B0C", "Transparency",
     "Accountability is demanded — or we will remember during upcoming voting."),

    # ── Volunteer & PAC ───────────────────────────────────────────────────────
    ("volunteer", "#FBEAF0", "#4B1528", "Volunteer & PAC",
     "Punishment without clarity has a chilling effect on people getting involved with their local parks. It raises doubts about fairness and whether some people are sanctioned simply because someone else doesn't like them."),
    ("volunteer", "#FBEAF0", "#4B1528", "Volunteer & PAC",
     "I was interested in serving on a PAC for another SE Side park, but this situation — where CPD rules seem to morph randomly, after-the-fact — makes me very wary of doing so."),
]

filter_options = {
    "All (18)":             "all",
    "Taxes & fees":         "taxes",
    "Race & equity":        "equity",
    "Disability & seniors": "disability",
    "Public commons":       "commons",
    "Transparency":         "transparency",
    "Volunteer & PAC":      "volunteer",
}

selected_filter = st.radio(
    "Filter by theme", list(filter_options.keys()),
    horizontal=True, label_visibility="collapsed",
)
active_cat = filter_options[selected_filter]

filtered = [(cat, bg, tc, label, text) for cat, bg, tc, label, text in QUOTES
            if active_cat == "all" or cat == active_cat]

for i in range(0, len(filtered), 2):
    pair = filtered[i:i+2]
    cols = st.columns(2)
    for j, (cat, bg, tc, label, text) in enumerate(pair):
        with cols[j]:
            st.markdown(f"""
            <div class="qcard">
              <span class="badge" style="background:{bg};color:{tc}">{label}</span>
              <p class="qt">&#8220;{text}&#8221;</p>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
  <strong>Analysis by Ana Marija Sokovic, PhD, MBA</strong> &nbsp;·&nbsp; South Shore Resident<br>
  Data source: public petition comments submitted by signers of the
  <em>Petition for Accountability at the Chicago Park District</em><br>
  923 total signers &nbsp;·&nbsp; 272 comments analyzed &nbsp;·&nbsp; collected January – May 2026
</div>
""", unsafe_allow_html=True)
