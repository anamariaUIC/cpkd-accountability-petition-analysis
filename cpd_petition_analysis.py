import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="CPD Accountability Petition — Analysis",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Color palette ──────────────────────────────────────────────────────────────
TEAL   = "#1D9E75"
AMBER  = "#BA7517"
CORAL  = "#D85A30"
PURPLE = "#534AB7"
BLUE   = "#185FA5"
GREEN  = "#639922"
RED    = "#A32D2D"
PINK   = "#993556"
GRAY   = "#888780"

CATEGORY_COLORS = [TEAL, AMBER, CORAL, PURPLE, BLUE, GREEN, RED, PINK]

# ── Global style ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.main .block-container { padding-top: 2rem; padding-bottom: 3rem; }

h1, h2, h3 { font-family: 'DM Sans', sans-serif; font-weight: 600; }

/* Metric cards */
.metric-card {
    background: #f8f7f4;
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
    height: 100%;
}
.metric-label {
    font-size: 12px;
    color: #888780;
    margin: 0 0 4px;
    font-weight: 500;
    letter-spacing: .3px;
    text-transform: uppercase;
}
.metric-value {
    font-size: 32px;
    font-weight: 600;
    margin: 0;
    line-height: 1.1;
    color: #1a1a18;
}
.metric-sub {
    font-size: 12px;
    color: #888780;
    margin: 5px 0 0;
}

/* Section headers */
.sec-header {
    font-size: 16px;
    font-weight: 600;
    color: #1a1a18;
    margin: 0 0 0.2rem;
    padding-bottom: 8px;
    border-bottom: 1.5px solid #e5e3de;
}

/* Intensity rows */
.intensity-wrap { margin-top: 0.5rem; }
.irow {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 9px;
}
.ilabel { font-size: 13px; color: #5F5E5A; width: 100px; flex-shrink: 0; text-align: right; }
.ibwrap {
    flex: 1; height: 18px;
    background: #f0ede8;
    border-radius: 4px; overflow: hidden;
}
.ibar { height: 100%; border-radius: 4px; }
.ival { font-size: 13px; font-weight: 500; color: #1a1a18; width: 28px; flex-shrink: 0; }

/* Quote cards */
.qcard {
    background: #fff;
    border: 1px solid #e5e3de;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 12px;
    height: 100%;
}
.badge {
    display: inline-block;
    font-size: 10px;
    padding: 2px 9px;
    border-radius: 6px;
    font-weight: 600;
    letter-spacing: .3px;
    margin-bottom: 8px;
}
.qt {
    font-size: 13.5px;
    color: #2c2c2a;
    line-height: 1.65;
    font-style: italic;
    margin: 0;
}

/* Footer */
.footer {
    margin-top: 3rem;
    padding-top: 1.2rem;
    border-top: 1px solid #e5e3de;
    font-size: 12px;
    color: #888780;
    line-height: 1.8;
}
.footer strong { color: #444441; }

/* Stat pair */
.stat-pair {
    background: #f8f7f4;
    border-radius: 10px;
    padding: .9rem 1rem;
    text-align: center;
}
.stat-pair .sp-label { font-size: 11px; color: #888780; font-weight: 500; text-transform: uppercase; letter-spacing: .3px; margin: 0 0 3px; }
.stat-pair .sp-val   { font-size: 26px; font-weight: 600; margin: 0; line-height: 1; }
</style>
""", unsafe_allow_html=True)

# ── Plotly shared layout helper ────────────────────────────────────────────────
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
<h1 style="font-size:28px;font-weight:700;color:#1a1a18;margin-bottom:.2rem">
    Chicago Park District Accountability Petition
</h1>
<p style="font-size:15px;color:#5F5E5A;margin-bottom:.2rem">
    Public analysis of resident responses — parking gate installation at Rainbow Beach &amp; South Side lakefront parks
</p>
<p style="font-size:12px;color:#888780;margin-bottom:2rem">
    Data source: petition comments submitted by signers via the public petition platform
</p>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SUMMARY METRICS
# ══════════════════════════════════════════════════════════════════════════════
c1, c2, c3, c4 = st.columns(4)
metrics = [
    (c1, "Total signers",       "923",    "89% from Chicago"),
    (c2, "Signers with comments","272",   "29% comment rate"),
    (c3, "South Side ZIPs",     "64.8%",  "598 of 923 directly impacted"),
    (c4, "Comments in opposition","1",    "of 272 — effectively 0%"),
]
for col, label, val, sub in metrics:
    color = TEAL if val == "1" else "#1a1a18"
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">{label}</p>
            <p class="metric-value" style="color:{color}">{val}</p>
            <p class="metric-sub">{sub}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# GRIEVANCE CLASSIFICATION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="sec-header">Grievance classification — what residents are actually saying</p>', unsafe_allow_html=True)

grievance_labels = [
    "Public access rights",
    "Tax / public spending",
    "Anger & frustration",
    "Community exclusion",
    "Transparency concerns",
    "Fear of downstream impacts",
    "Distrust of government",
    "Volunteer / PAC accountability",
]
grievance_values = [111, 66, 49, 43, 41, 32, 29, 27]
grievance_pct    = [f"{v/272*100:.1f}%" for v in grievance_values]

fig_griev = go.Figure(go.Bar(
    x=grievance_values,
    y=grievance_labels,
    orientation="h",
    marker_color=CATEGORY_COLORS,
    text=grievance_pct,
    textposition="outside",
    textfont=dict(size=12, color="#444441"),
    hovertemplate="%{y}: %{x} comments<extra></extra>",
))
fig_griev.update_layout(
    **base_layout(height=370),
    xaxis=dict(showgrid=True, gridcolor="#ece9e4", tickfont=dict(size=11),
               title=dict(text="number of comments", font=dict(size=11)), range=[0, 135]),
    yaxis=dict(showgrid=False, tickfont=dict(size=12), autorange="reversed"),
)
st.plotly_chart(fig_griev, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# KEYWORD FREQUENCY
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="sec-header">Theme frequency — most repeated concepts in comments</p>', unsafe_allow_html=True)

kw_labels = ['"pay"','"free"','"access"','"parking"','"public"','"tax"',
             '"community"','"gate"','"barrier"','"accountability"',
             '"transparency"','"South Shore"','"volunteer"','"Burnham"']
kw_values = [55, 48, 46, 42, 40, 36, 27, 26, 17, 13, 12, 12, 11, 4]

fig_kw = go.Figure(go.Bar(
    x=kw_values,
    y=kw_labels,
    orientation="h",
    marker_color=BLUE,
    text=kw_values,
    textposition="outside",
    textfont=dict(size=11, color="#444441"),
    hovertemplate="%{y}: %{x} comments<extra></extra>",
))
fig_kw.update_layout(
    **base_layout(height=460),
    xaxis=dict(showgrid=True, gridcolor="#ece9e4", tickfont=dict(size=11),
               title=dict(text="number of comments", font=dict(size=11)), range=[0, 68]),
    yaxis=dict(showgrid=False, tickfont=dict(size=12), autorange="reversed"),
)
st.plotly_chart(fig_kw, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# INTENSITY  +  OPPOSITION  (side by side)
# ══════════════════════════════════════════════════════════════════════════════
col_int, col_opp = st.columns(2)

# ── Intensity ─────────────────────────────────────────────────────────────────
with col_int:
    st.markdown('<p class="sec-header">Issue intensity — urgency language</p>', unsafe_allow_html=True)

    urgency = [
        ("stop",       24, 100),
        ("please",     20, 83),
        ("remove",     11, 46),
        ("why",        11, 46),
        ("unfair",     10, 42),
        ("enough",      8, 33),
        ("ridiculous",  6, 25),
        ("demand",      5, 21),
    ]
    rows_html = ""
    for word, count, pct in urgency:
        rows_html += f"""
        <div class="irow">
          <span class="ilabel">"{word}"</span>
          <div class="ibwrap">
            <div class="ibar" style="width:{pct}%;background:{CORAL}"></div>
          </div>
          <span class="ival">{count}</span>
        </div>"""

    st.markdown(f'<div class="intensity-wrap">{rows_html}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    sp1, sp2 = st.columns(2)
    with sp1:
        st.markdown(f"""
        <div class="stat-pair">
          <p class="sp-label">Exclamation points</p>
          <p class="sp-val" style="color:{CORAL}">94</p>
        </div>""", unsafe_allow_html=True)
    with sp2:
        st.markdown(f"""
        <div class="stat-pair">
          <p class="sp-label">ALL CAPS words</p>
          <p class="sp-val" style="color:{CORAL}">111</p>
        </div>""", unsafe_allow_html=True)

# ── Opposition donut ──────────────────────────────────────────────────────────
with col_opp:
    st.markdown('<p class="sec-header">Support vs. opposition ratio</p>', unsafe_allow_html=True)

    fig_opp = go.Figure(go.Pie(
        labels=["Critical / supportive", "Opposed"],
        values=[271, 1],
        hole=0.68,
        marker=dict(colors=[TEAL, CORAL], line=dict(width=0)),
        textinfo="none",
        hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
    ))
    fig_opp.update_layout(
        **base_layout(height=210),
        showlegend=False,
        annotations=[dict(
            text='<b style="font-size:22px">99.6%</b><br><span style="font-size:11px;color:#888">supportive</span>',
            x=0.5, y=0.5, showarrow=False, align="center",
            font=dict(family="DM Sans", color="#1a1a18"),
        )],
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig_opp, use_container_width=True)

    sp3, sp4 = st.columns(2)
    with sp3:
        st.markdown(f"""
        <div class="stat-pair">
          <p class="sp-label">Support / critical of CPD</p>
          <p class="sp-val" style="color:{TEAL}">271</p>
        </div>""", unsafe_allow_html=True)
    with sp4:
        st.markdown(f"""
        <div class="stat-pair">
          <p class="sp-label">Opposed to petition</p>
          <p class="sp-val" style="color:{CORAL}">1</p>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# GEOGRAPHIC CONCENTRATION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="sec-header">Geographic concentration — signatures by neighborhood</p>', unsafe_allow_html=True)

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
geo_colors = ["#0F6E56","#1D9E75","#5DCAA5","#5DCAA5","#5DCAA5","#9FE1CB","#9FE1CB","#9FE1CB","#9FE1CB"]

fig_geo = go.Figure(go.Bar(
    x=geo_values,
    y=geo_labels,
    orientation="h",
    marker_color=geo_colors,
    text=geo_values,
    textposition="outside",
    textfont=dict(size=11, color="#444441"),
    hovertemplate="%{y}: %{x} signers<extra></extra>",
))
fig_geo.update_layout(
    **base_layout(height=390),
    xaxis=dict(showgrid=True, gridcolor="#ece9e4", tickfont=dict(size=11),
               title=dict(text="number of signers", font=dict(size=11)), range=[0, 215]),
    yaxis=dict(showgrid=False, tickfont=dict(size=12), autorange="reversed"),
)
st.plotly_chart(fig_geo, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# RESIDENT VOICES — QUOTE GALLERY
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="sec-header">Resident voices — selected quotes</p>', unsafe_allow_html=True)

QUOTES = [
    ("taxes",      "#FAEEDA", "#633806", "Taxes &amp; fees",
     "It's a disgrace to put physical barriers on a FREE PARK that is paid for and maintained with OUR TAX MONEY."),
    ("taxes",      "#FAEEDA", "#633806", "Taxes &amp; fees",
     "We DON'T NEED MORE FEES AND TAXES FOR WHAT WE ARE ALREADY PAYING!!!!"),
    ("taxes",      "#FAEEDA", "#633806", "Taxes &amp; fees",
     "Charging people to park at a PUBLIC park that OUR taxes already pay for is abhorrent."),
    ("taxes",      "#FAEEDA", "#633806", "Taxes &amp; fees",
     "Stop the money grab! Make parking at all parks and lakefront locations free like it was for years. Chicago is always taking from the people and giving very little in return. All of this excess money is lining politicians' pockets."),
    ("taxes",      "#FAEEDA", "#633806", "Taxes &amp; fees",
     "Not only are they starting to charge — they're not disclosing what the funds will be going towards. Truly disappointing. In a neighborhood where the average income is about $40,000 a year."),
    ("taxes",      "#FAEEDA", "#633806", "Taxes &amp; fees",
     "A stealth tax if there ever was one — it just appeared out of nowhere."),

    ("equity",     "#EEEDFE", "#26215C", "Race &amp; equity",
     "What year is it — why aren't we letting Black people swim and enjoy the same NATURAL RESOURCES we on the north side get to access for free? Shameful and horrifying."),
    ("equity",     "#EEEDFE", "#26215C", "Race &amp; equity",
     "Why none of the beaches up north got gates? Why just Black neighborhoods? Remove the gates."),
    ("equity",     "#EEEDFE", "#26215C", "Race &amp; equity",
     "Chicago beaches are one of the last third spaces available to all residents no matter their zip code or economic status. Monetized parking and cryptic financial record keeping disproportionately targets lower income, elderly, and disabled Chicagoans."),
    ("equity",     "#EEEDFE", "#26215C", "Race &amp; equity",
     "Treating our PACs differently, limiting access to programs, obstructing grants, forcing us to pay for things North Side parks get for free and taking punitive actions based on obscure and unclear rules not used against others is DISCRIMINATORY."),
    ("equity",     "#EEEDFE", "#26215C", "Race &amp; equity",
     "Our parks are always last in everything — restorations, clean up, beautification and care. We are the first to have to pay for parking and closed gates."),

    ("disability", "#E1F5EE", "#04342C", "Disability &amp; seniors",
     "I am a disabled senior living in South Shore on a fixed income. My main way of exercising for my health is walking or e-biking in the nearby parks. I cannot afford to pay parking fees to visit the parks in my own neighborhood."),
    ("disability", "#E1F5EE", "#04342C", "Disability &amp; seniors",
     "I'm a wheelchair user with a yellow placard. There are few accessible spots along the lake and now they are behind the gate. I feel it's discriminatory to place this burden on disabled people."),
    ("disability", "#E1F5EE", "#04342C", "Disability &amp; seniors",
     "As someone with a mobility disability who often parked in Rainbow Beach's North lot to enjoy the lake views while walking for physical therapy, this directly impedes my access. Even the ability to pay via the AI system is prohibitive for residents who don't have smart phones."),
    ("disability", "#E1F5EE", "#04342C", "Disability &amp; seniors",
     "I am a disabled senior on a fixed income. It is outrageous that we have to pay to visit our free public beaches and parks. Enough of the gouging of our citizens!"),

    ("burnham",    "#E6F1FB", "#042C53", "Burnham legacy",
     "What happened to the Daniel Burnham plan for the lakefront to be 'forever open and free'? Steep parking fees privatize the lakefront just as assuredly as building privately owned buildings on the shoreline would."),
    ("burnham",    "#E6F1FB", "#042C53", "Burnham legacy",
     "These new gates are denying us — the public — the right to enjoy the very lakefront which was by law to be forever free and open."),
    ("burnham",    "#E6F1FB", "#042C53", "Burnham legacy",
     "Daniel Burnham and other Chicago planners argued that Chicago's shoreline should remain: forever open, clear, and free. The lakefront should be accessible to the general public, not blocked by private entities."),
    ("burnham",    "#E6F1FB", "#042C53", "Burnham legacy",
     "Rainbow Beach is my nearest park. The programming last year was amazing — residents in South Shore suddenly had access to events typically only offered in wealthier northside parks. That the person who spearheaded these experiences is now suspended without prior notice is unconscionable."),

    ("transparency","#FAECE7", "#4A1B0C", "Transparency",
     "Was there a public forum held prior to installation? Who decided that this was needed?"),
    ("transparency","#FAECE7", "#4A1B0C", "Transparency",
     "Accountability is demanded — or we will remember during upcoming voting."),
    ("transparency","#FAECE7", "#4A1B0C", "Transparency",
     "We, the public, deserve full transparency in ALL matters pertaining to OUR PUBLIC LANDS. The rules must be clearly written and published in plain language. There must be a response process."),
    ("transparency","#FAECE7", "#4A1B0C", "Transparency",
     "Accountability must be baked in to rules and procedures wherever public funds are being spent. No public body is too small."),

    ("volunteer",  "#FBEAF0", "#4B1528", "Volunteer &amp; PAC",
     "Punishment without clarity has a chilling effect on people getting involved with their local parks. It also raises doubts about fairness and whether some people are sanctioned simply because someone else doesn't like them."),
    ("volunteer",  "#FBEAF0", "#4B1528", "Volunteer &amp; PAC",
     "I was interested in potentially serving on a PAC for another SE Side park, but this situation — where CPD rules for PACs seem to morph randomly, after-the-fact — makes me very wary of doing so."),
]

filter_options = {
    "All (25)":        "all",
    "Taxes & fees":    "taxes",
    "Race & equity":   "equity",
    "Disability & seniors": "disability",
    "Burnham legacy":  "burnham",
    "Transparency":    "transparency",
    "Volunteer & PAC": "volunteer",
}

selected_filter = st.radio(
    "Filter by theme",
    list(filter_options.keys()),
    horizontal=True,
    label_visibility="collapsed",
)
active_cat = filter_options[selected_filter]

filtered = [(cat, bg, tc, label, text) for cat, bg, tc, label, text in QUOTES
            if active_cat == "all" or cat == active_cat]

cols_per_row = 2
for i in range(0, len(filtered), cols_per_row):
    row = filtered[i:i + cols_per_row]
    cols = st.columns(cols_per_row)
    for j, (cat, bg, tc, label, text) in enumerate(row):
        with cols[j]:
            st.markdown(f"""
            <div class="qcard">
              <span class="badge" style="background:{bg};color:{tc}">{label}</span>
              <p class="qt">"{text}"</p>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
  <strong>Analysis by Ana Marija Sokovic, PhD, MBA</strong> · South Shore Resident<br>
  Data source: public petition comments submitted by signers of the <em>Petition for Accountability at the Chicago Park District</em><br>
  923 total signers · 272 comments analyzed · collected January – May 2026
</div>
""", unsafe_allow_html=True)
