"""
US Traffic Accident Dashboard - Streamlit App
Professional visualization dashboard for US accident data (Severity 4).
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="US Traffic Accident Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS - Professional Power BI / Tableau Style
# ============================================================
st.markdown("""
<style>
/* ---------- Global ---------- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="st-"] { font-family: 'Inter', sans-serif; color: #1e293b; }
.stApp { background-color: #f5f7fa; }
.stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown li,
.stAlert p, .stExpander p, h1, h2, h3, h4, h5, h6,
label, .stSelectbox label, .stMultiSelect label { color: #1e293b !important; }
header[data-testid="stHeader"] { background: rgba(255,255,255,0.95); backdrop-filter: blur(8px); border-bottom: 1px solid #e2e8f0; }

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #e2e8f0; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stDateInput label { font-weight: 500; color: #1e293b; font-size: 0.85rem; }
section[data-testid="stSidebar"] .stMarkdown h3,
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown span { color: #1e293b !important; }

/* ---------- KPI Cards ---------- */
.kpi-container { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 1.5rem; }
.kpi-card {
    flex: 1 1 160px; background: #ffffff; border-radius: 12px; padding: 18px 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06); border: 1px solid #e8ecf1;
    text-align: center; transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.kpi-label { font-size: 0.75rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }
.kpi-value { font-size: 1.6rem; font-weight: 700; color: #1e293b; }
.kpi-sub { font-size: 0.7rem; color: #94a3b8; margin-top: 4px; }

/* ---------- Section Headers ---------- */
.section-header {
    font-size: 1.15rem; font-weight: 600; color: #1e293b; margin: 1.5rem 0 0.75rem 0;
    padding-bottom: 8px; border-bottom: 2px solid #3b82f6; display: inline-block;
}

/* ---------- Chart Card ---------- */
.chart-card {
    background: #ffffff; border-radius: 12px; padding: 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06); border: 1px solid #e8ecf1; margin-bottom: 1rem;
}

/* ---------- Hero Banner ---------- */
.hero {
    background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%);
    border-radius: 14px; padding: 28px 32px; margin-bottom: 1.5rem;
    box-shadow: 0 4px 16px rgba(59,130,246,0.25);
}
.hero h1 { color: #ffffff; font-size: 1.7rem; font-weight: 700; margin: 0 0 4px 0; }
.hero p  { color: #dbeafe; font-size: 0.9rem; margin: 0; }

/* ---------- Misc ---------- */
.stDownloadButton > button {
    background: #3b82f6; color: white; border: none; border-radius: 8px;
    font-weight: 500; padding: 8px 20px;
}
.stDownloadButton > button:hover { background: #2563eb; }
div[data-testid="stExpander"] { background: #ffffff; border-radius: 12px; border: 1px solid #e8ecf1; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA LOADING
# ============================================================
@st.cache_data(show_spinner="Loading accident data...")
def load_data(path):
    """Load and preprocess the accident CSV."""
    df = pd.read_csv(path, low_memory=False)
    # Datetime conversion
    df["Start_Time"] = pd.to_datetime(df["Start_Time"], errors="coerce")
    df["End_Time"] = pd.to_datetime(df["End_Time"], errors="coerce")
    # Derived columns
    df["Year"] = df["Start_Time"].dt.year
    df["Month"] = df["Start_Time"].dt.month
    df["Hour"] = df["Start_Time"].dt.hour
    df["Weekday"] = df["Start_Time"].dt.day_name()
    # Drop rows missing coordinates
    df = df.dropna(subset=["Start_Lat", "Start_Lng"])
    return df

# ============================================================
# SIDEBAR
# ============================================================
# Load default dataset
try:
    df_raw = load_data(r"US_Accidents_Severity_4.csv")
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

# Full state name mapping
STATE_NAMES = {
    "AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California",
    "CO":"Colorado","CT":"Connecticut","DE":"Delaware","DC":"District of Columbia",
    "FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho","IL":"Illinois",
    "IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana",
    "ME":"Maine","MD":"Maryland","MA":"Massachusetts","MI":"Michigan",
    "MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana",
    "NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey",
    "NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota",
    "OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania",
    "RI":"Rhode Island","SC":"South Carolina","SD":"South Dakota",
    "TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia",
    "WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming",
}
ABBREV_TO_DISPLAY = {abbr: f"{name} ({abbr})" for abbr, name in STATE_NAMES.items()}
DISPLAY_TO_ABBREV = {v: k for k, v in ABBREV_TO_DISPLAY.items()}

# Init session state for map click
if "map_clicked_state" not in st.session_state:
    st.session_state["map_clicked_state"] = "All"

with st.sidebar:

    st.markdown("### 🔍 Filters")

    # State selector — show full names, default from map click
    states_abbr = sorted(df_raw["State"].dropna().unique().tolist())
    states_display = ["All"] + [ABBREV_TO_DISPLAY.get(s, s) for s in states_abbr]
    # Determine default index from session state
    _clicked = st.session_state["map_clicked_state"]
    _clicked_display = ABBREV_TO_DISPLAY.get(_clicked, _clicked)  # convert abbrev → display
    _default_idx = states_display.index(_clicked_display) if _clicked_display in states_display else 0
    state_display_sel = st.selectbox("State", states_display, index=_default_idx)
    state_sel = DISPLAY_TO_ABBREV.get(state_display_sel, state_display_sel)  # map back to abbrev

    # City selector (depends on state)
    if state_sel != "All":
        cities_list = sorted(df_raw[df_raw["State"] == state_sel]["City"].dropna().unique().tolist())
    else:
        cities_list = sorted(df_raw["City"].dropna().unique().tolist())
    city_sel = st.multiselect("City", cities_list)



    # Weather condition selector
    weather_list = sorted(df_raw["Weather_Condition"].dropna().unique().tolist())
    weather_sel = st.multiselect("Weather Condition", weather_list)

    # Date range selector
    min_date = df_raw["Start_Time"].min().date()
    max_date = df_raw["Start_Time"].max().date()
    date_range = st.date_input("Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

    # Day / Night selector
    daynight_opts = df_raw["Sunrise_Sunset"].dropna().unique().tolist()
    daynight_sel = st.multiselect("Day / Night", daynight_opts)

    # Reset button
    if st.button("🔄 Reset Filters", use_container_width=True):
        st.session_state["map_clicked_state"] = "All"
        st.rerun()

# ============================================================
# APPLY FILTERS
# ============================================================
df = df_raw.copy()
if state_sel != "All":
    df = df[df["State"] == state_sel]
if city_sel:
    df = df[df["City"].isin(city_sel)]

if weather_sel:
    df = df[df["Weather_Condition"].isin(weather_sel)]
if daynight_sel:
    df = df[df["Sunrise_Sunset"].isin(daynight_sel)]
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    df = df[(df["Start_Time"].dt.date >= date_range[0]) & (df["Start_Time"].dt.date <= date_range[1])]

if df.empty:
    st.warning("No data matches the current filters. Please adjust your selections.")
    st.stop()

# ============================================================
# HERO BANNER
# ============================================================
st.markdown("""
<div class="hero">
    <h1>🚗 US Traffic Accident Dashboard</h1>
    <p>Interactive visualization of severity-4 traffic accidents across the United States</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# KPI CARDS
# ============================================================
total_acc = len(df)
avg_sev = df["Severity"].mean()
n_states = df["State"].nunique()
n_cities = df["City"].nunique()
n_counties = df["County"].nunique()
top_state = df["State"].value_counts().idxmax()
top_city = df["City"].value_counts().idxmax()

kpi_data = [
    ("Total Accidents", f"{total_acc:,}", "filtered records"),
    ("Avg Severity", f"{avg_sev:.2f}", "out of 4"),
    ("States", f"{n_states}", "unique"),
    ("Cities", f"{n_cities:,}", "unique"),
    ("Counties", f"{n_counties:,}", "unique"),
    ("Top State", top_state, f"{df['State'].value_counts().iloc[0]:,} accidents"),
    ("Top City", top_city, f"{df['City'].value_counts().iloc[0]:,} accidents"),
]

kpi_html = '<div class="kpi-container">'
for label, value, sub in kpi_data:
    kpi_html += f'''
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>'''
kpi_html += '</div>'
st.markdown(kpi_html, unsafe_allow_html=True)

# ============================================================
# PLOTLY THEME HELPER
# ============================================================
BLUE_SEQ = ["#dbeafe", "#93c5fd", "#60a5fa", "#3b82f6", "#2563eb", "#1d4ed8", "#1e40af"]
ACCENT = "#3b82f6"

def style_fig(fig, height=420):
    """Apply consistent styling to a Plotly figure."""
    fig.update_layout(
        template="plotly_white",
        font=dict(family="Inter, sans-serif", color="#334155"),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=20, t=40, b=40), height=height,
        hoverlabel=dict(bgcolor="#1e293b", font_color="white", font_size=12),
    )
    return fig

# ============================================================
# MAPS
# ============================================================
if state_sel == "All":
    # ---- US OVERVIEW CHOROPLETH ----
    st.markdown('<div class="section-header">🗺️ US Overview — Accidents by State</div>', unsafe_allow_html=True)


    state_agg = df.groupby("State").agg(
        count=("ID", "count"), avg_severity=("Severity", "mean")
    ).reset_index()
    state_agg["avg_severity"] = state_agg["avg_severity"].round(2)
    state_agg["State_Name"] = state_agg["State"].map(STATE_NAMES)

    fig_map = px.choropleth(
        state_agg, locations="State", locationmode="USA-states",
        color="count", color_continuous_scale=BLUE_SEQ,
        scope="usa", labels={"count": "Accidents", "avg_severity": "Avg Severity", "State_Name": "State"},
        hover_data={"State_Name": True, "State": False, "count": ":,", "avg_severity": True},
    )
    style_fig(fig_map, 500)
    fig_map.update_layout(geo=dict(bgcolor="rgba(0,0,0,0)", lakecolor="#e0f2fe"))
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    # Enable click-to-filter: clicking a state updates sidebar selector
    map_event = st.plotly_chart(
        fig_map, use_container_width=True,
        key="choropleth_map", on_select="rerun", selection_mode="points"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Handle map click — update session state and rerun to apply filter
    if map_event and map_event.selection and map_event.selection.points:
        clicked_abbr = map_event.selection.points[0].get("location", "")
        if clicked_abbr and clicked_abbr != st.session_state["map_clicked_state"]:
            st.session_state["map_clicked_state"] = clicked_abbr
            st.rerun()

    st.info("📌 Click on any state to drill down, or select from the sidebar.")
else:
    # ---- STATE DETAIL: SCATTER MAP ----
    st.markdown(f'<div class="section-header">📍 {state_sel} — Accident Locations</div>', unsafe_allow_html=True)

    # Sample for performance (max 15k points for scatter)
    df_map = df.sample(n=min(15000, len(df)), random_state=42) if len(df) > 15000 else df

    fig_scatter = px.scatter_mapbox(
        df_map, lat="Start_Lat", lon="Start_Lng",
        color="Severity", color_continuous_scale=BLUE_SEQ,
        hover_data={"City": True, "County": True, "Severity": True,
                     "Weather_Condition": True, "Start_Time": True, "Street": True,
                     "Start_Lat": False, "Start_Lng": False},
        zoom=5, opacity=0.6, size_max=8,
    )

    # ---- Detect high-density hotspot zones & cluster nearby ones ----
    import numpy as np
    grid_size = 0.05  # degrees (~5km grid cells)
    df_grid = df.copy()
    df_grid["lat_bin"] = (df_grid["Start_Lat"] / grid_size).round() * grid_size
    df_grid["lng_bin"] = (df_grid["Start_Lng"] / grid_size).round() * grid_size
    hotspots = df_grid.groupby(["lat_bin", "lng_bin"]).size().reset_index(name="density")

    # Keep only statistically significant dense cells
    threshold = hotspots["density"].mean() + 2 * hotspots["density"].std()
    hotspots = hotspots[hotspots["density"] >= threshold].nlargest(30, "density").reset_index(drop=True)

    def draw_circle(fig, center_lat, center_lng, radius_deg, total_accidents, idx):
        """Draw one red circle on the map."""
        n_pts = 72
        angles = np.linspace(0, 2 * np.pi, n_pts)
        clats = center_lat + radius_deg * np.cos(angles)
        clngs = center_lng + radius_deg / np.cos(np.radians(center_lat)) * np.sin(angles)
        fig.add_trace(go.Scattermapbox(
            lat=clats.tolist(), lon=clngs.tolist(),
            mode="lines",
            line=dict(color="red", width=2.5),
            name=f"Zone {idx+1}: {total_accidents:,} accidents",
            hoverinfo="name",
            showlegend=True,
        ))

    if len(hotspots) > 0:
        try:
            from sklearn.cluster import DBSCAN
            coords = hotspots[["lat_bin", "lng_bin"]].values
            # eps = 0.3 degrees (~30km) — cells within this distance get merged
            db = DBSCAN(eps=0.3, min_samples=1, metric="euclidean").fit(coords)
            hotspots["cluster"] = db.labels_
        except ImportError:
            # Fallback: each hotspot is its own cluster
            hotspots["cluster"] = range(len(hotspots))

        # Draw one big enclosing circle per cluster
        for cluster_id, grp in hotspots.groupby("cluster"):
            center_lat = grp["lat_bin"].mean()
            center_lng = grp["lng_bin"].mean()
            total_acc  = int(grp["density"].sum())

            if len(grp) == 1:
                # Single isolated hotspot — small circle
                radius_deg = grid_size * 2.0
            else:
                # Multi-cell cluster — radius = max distance from center + padding
                dists = np.sqrt(
                    (grp["lat_bin"] - center_lat)**2 +
                    (grp["lng_bin"] - center_lng)**2
                )
                radius_deg = dists.max() + grid_size * 2.5

            draw_circle(fig_scatter, center_lat, center_lng, radius_deg, total_acc, int(cluster_id))

    fig_scatter.update_layout(mapbox_style="carto-positron",
                              margin=dict(l=0, r=0, t=30, b=0), height=500,
                              legend=dict(bgcolor="rgba(255,255,255,0.85)", font=dict(size=11)))
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- STATE DETAIL: DENSITY / HEATMAP ----
    st.markdown(f'<div class="section-header">🔥 {state_sel} — Hotspot Density Map</div>', unsafe_allow_html=True)
    fig_density = px.density_mapbox(
        df_map, lat="Start_Lat", lon="Start_Lng",
        z="Severity", radius=12, zoom=5,
        color_continuous_scale="YlOrRd",
        hover_data={"City": True, "County": True},
    )
    fig_density.update_layout(mapbox_style="carto-positron",
                              margin=dict(l=0, r=0, t=30, b=0), height=500)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_density, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# CHARTS
# ============================================================
st.markdown('<div class="section-header">📊 Analytics</div>', unsafe_allow_html=True)

# ---- Row 1: Top States / Top Cities & Counties ----
if state_sel == "All":
    col1, col2 = st.columns(2)
    # Top 10 states
    top_states = df["State"].value_counts().head(10).reset_index()
    top_states.columns = ["State", "Accidents"]
    fig1 = px.bar(top_states, x="Accidents", y="State", orientation="h",
                  color="Accidents", color_continuous_scale=BLUE_SEQ, text="Accidents")
    fig1.update_traces(textposition="outside", texttemplate="%{text:,}")
    fig1.update_layout(title="Top 10 States by Accidents", yaxis=dict(autorange="reversed"),
                       coloraxis_showscale=False)
    style_fig(fig1)
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Distance ratio chart: > 2.5 miles vs <= 2.5 miles
    dist_df = df["Distance(mi)"].dropna()
    dist_counts = pd.Series({
        "> 2.5 miles": int((dist_df > 2.5).sum()),
        "≤ 2.5 miles": int((dist_df <= 2.5).sum()),
    }).reset_index()
    dist_counts.columns = ["Distance", "Count"]
    fig2 = px.pie(dist_counts, names="Distance", values="Count",
                  color_discrete_sequence=["#3b82f6", "#93c5fd"],
                  title="Accident Distance: >2.5 mi vs ≤2.5 mi", hole=0.45)
    fig2.update_traces(textinfo="percent+label+value")
    style_fig(fig2)
    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    col1, col2 = st.columns(2)
    # Top 10 cities in state
    top_cities = df["City"].value_counts().head(10).reset_index()
    top_cities.columns = ["City", "Accidents"]
    fig_tc = px.bar(top_cities, x="Accidents", y="City", orientation="h",
                    color="Accidents", color_continuous_scale=BLUE_SEQ, text="Accidents")
    fig_tc.update_traces(textposition="outside", texttemplate="%{text:,}")
    fig_tc.update_layout(title=f"Top 10 Cities in {state_sel}", yaxis=dict(autorange="reversed"),
                         coloraxis_showscale=False)
    style_fig(fig_tc)
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_tc, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Top 10 counties in state
    top_counties = df["County"].value_counts().head(10).reset_index()
    top_counties.columns = ["County", "Accidents"]
    fig_co = px.bar(top_counties, x="Accidents", y="County", orientation="h",
                    color="Accidents", color_continuous_scale=BLUE_SEQ, text="Accidents")
    fig_co.update_traces(textposition="outside", texttemplate="%{text:,}")
    fig_co.update_layout(title=f"Top 10 Counties in {state_sel}", yaxis=dict(autorange="reversed"),
                         coloraxis_showscale=False)
    style_fig(fig_co)
    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_co, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Distance ratio chart for selected state
    dist_df_s = df["Distance(mi)"].dropna()
    dist_counts_s = pd.Series({
        "> 2.5 miles": int((dist_df_s > 2.5).sum()),
        "≤ 2.5 miles": int((dist_df_s <= 2.5).sum()),
    }).reset_index()
    dist_counts_s.columns = ["Distance", "Count"]
    fig_sd = px.pie(dist_counts_s, names="Distance", values="Count",
                    color_discrete_sequence=["#3b82f6", "#93c5fd"],
                    title="Accident Distance: >2.5 mi vs ≤2.5 mi", hole=0.45)
    fig_sd.update_traces(textinfo="percent+label+value")
    style_fig(fig_sd)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_sd, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---- Row 2: Temporal Analysis ----
st.markdown('<div class="section-header">⏳ Temporal Analysis</div>', unsafe_allow_html=True)
col_t1, col_t2, col_t3 = st.columns(3)

# Accidents by year
yr = df["Year"].value_counts().sort_index().reset_index()
yr.columns = ["Year", "Accidents"]
fig_yr = px.bar(yr, x="Year", y="Accidents", color="Accidents",
                color_continuous_scale=BLUE_SEQ, text="Accidents",
                title="Accidents by Year")
fig_yr.update_traces(textposition="outside", texttemplate="%{text:,}")
fig_yr.update_layout(coloraxis_showscale=False, xaxis=dict(dtick=1, tickangle=0))
style_fig(fig_yr, 380)
with col_t1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_yr, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Accidents by month — use numeric month (1–12) with dtick=1 like year chart
mo = df["Month"].value_counts().reindex(range(1, 13), fill_value=0).sort_index().reset_index()
mo.columns = ["Month", "Accidents"]
fig_mo = px.line(mo, x="Month", y="Accidents", markers=True,
                 title="Accidents by Month")
fig_mo.update_traces(line_color=ACCENT, fill="tozeroy", fillcolor="rgba(59,130,246,0.08)")
style_fig(fig_mo, 380)
fig_mo.update_xaxes(dtick=1, tickmode="linear", tickangle=0)
with col_t2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_mo, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Accidents by hour — reindex to ensure all 24 hours (0–23) are shown
hr = df["Hour"].value_counts().reindex(range(24), fill_value=0).sort_index().reset_index()
hr.columns = ["Hour", "Accidents"]
fig_hr = px.area(hr, x="Hour", y="Accidents", title="Accidents by Hour of Day",
                 color_discrete_sequence=[ACCENT])
fig_hr.update_traces(fillcolor="rgba(59,130,246,0.12)")
style_fig(fig_hr, 380)
fig_hr.update_xaxes(dtick=2, tickmode="linear", range=[-0.5, 23.5], tickangle=0)
with col_t3:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_hr, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---- Row 3: Weather & Day/Night ----
st.markdown('<div class="section-header">🌦️ Weather & Conditions</div>', unsafe_allow_html=True)
col_w1, col_w2 = st.columns(2)

# Weather condition distribution (top 10)
wc = df["Weather_Condition"].value_counts().head(10).reset_index()
wc.columns = ["Condition", "Count"]
fig_wc = px.bar(wc, x="Count", y="Condition", orientation="h",
                color="Count", color_continuous_scale=BLUE_SEQ, text="Count",
                title="Top 10 Weather Conditions")
fig_wc.update_traces(textposition="outside", texttemplate="%{text:,}")
fig_wc.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
style_fig(fig_wc)
with col_w1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_wc, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Day/Night distribution
dn = df["Sunrise_Sunset"].value_counts().reset_index()
dn.columns = ["Period", "Count"]
fig_dn = px.pie(dn, names="Period", values="Count",
                color_discrete_sequence=["#3b82f6", "#1e293b"],
                title="Day vs Night Accidents", hole=0.45)
fig_dn.update_traces(textinfo="percent+label+value")
style_fig(fig_dn)
with col_w2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_dn, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---- Row 4: Road Feature Analysis ----
st.markdown('<div class="section-header">🛣️ Road Feature Analysis</div>', unsafe_allow_html=True)
road_features = ["Traffic_Signal", "Junction", "Crossing", "Stop", "Railway"]
available_features = [f for f in road_features if f in df.columns]

if available_features:
    feat_counts = []
    for feat in available_features:
        true_count = df[feat].astype(str).str.lower().isin(["true", "1"]).sum()
        feat_counts.append({"Feature": feat, "Accidents": int(true_count)})
    feat_df = pd.DataFrame(feat_counts).sort_values("Accidents", ascending=False)

    fig_rf = px.bar(feat_df, x="Feature", y="Accidents", color="Accidents",
                    color_continuous_scale=BLUE_SEQ, text="Accidents",
                    title="Accidents Near Road Features")
    fig_rf.update_traces(textposition="outside", texttemplate="%{text:,}")
    fig_rf.update_layout(coloraxis_showscale=False)
    style_fig(fig_rf, 400)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_rf, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---- Footer ----
st.markdown("---")
