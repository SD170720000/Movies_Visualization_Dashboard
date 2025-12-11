# scripts/visualize.py

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from collections import defaultdict

# ---------------------------
# Genre-filtered panel
# ---------------------------
def genre_filter_data(movies):
    """
    Build genre-specific versions of:
    - panel1 (keywords bar for that genre)
    - panel3 (revenue over time for that genre)
    - panel5 (sunburst identical style to original panel5)
    Returns: (panel1_genre_dict, panel3_genre_dict, panel5_genre_dict)
    """
    print("[INFO] Generating Genre-Based Panel...")
    genre_keywords = defaultdict(lambda: defaultdict(int))
    genre_actors = defaultdict(lambda: defaultdict(int))

    # Count keywords + actors per genre
    for _, row in movies.iterrows():
        # skip rows with missing lists gracefully
        genres = row.get("genres_list") or []
        keywords = row.get("keywords_list") or []
        top_actor = row.get("top_actor")

        for g in genres:
            for kw in keywords:
                genre_keywords[g][kw] += 1
            if top_actor:
                genre_actors[g][top_actor] += 1

    panel1_genre = {}
    panel5_genre = {}
    panel3_genre = {}

    # TEAL PALETTE same as original panel5
    TEAL_PALETTE = [
        "#66FCF1", "#45A29E", "#3EC7BA", "#31A6A4",
        "#2E8C8E", "#207070", "#175E5C", "#0E4A47"
    ]

    def darker(hex_color):
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16) * 0.75
        g = int(hex_color[2:4], 16) * 0.75
        b = int(hex_color[4:6], 16) * 0.75
        return f"rgba({int(r)},{int(g)},{int(b)},0.95)"

    # Build genre-specific charts
    for i, g in enumerate(sorted(genre_keywords.keys())):
        # --------------------------
        # PANEL-1: keywords bar (same UI)
        # --------------------------
        df_kw = pd.DataFrame({
            "keyword": list(genre_keywords[g].keys()),
            "count": list(genre_keywords[g].values())
        })

        if df_kw.empty:
            # create an empty figure to avoid undefined lookups
            empty_fig1 = go.Figure()
            empty_fig1.update_layout(
                paper_bgcolor="#1f2833",
                plot_bgcolor="#1f2833",
                font=dict(color="#c5c6c7")
            )
            panel1_genre[g] = empty_fig1.to_json()
        else:
            df_kw = df_kw.sort_values("count", ascending=False).head(25)
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(
                x=df_kw["count"].tolist(),
                y=df_kw["keyword"].tolist(),
                orientation="h",
                marker=dict(
                    color=df_kw["count"].tolist(),
                    colorscale="Viridis",
                    showscale=True,
                    colorbar=dict(title="Count")
                ),
                hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>'
            ))
            fig1.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                xaxis_title="Count",
                yaxis_title="Keyword",
                height=600,
                margin=dict(l=150, r=50, t=20, b=50),
                yaxis_tickfont=dict(size=11),
                paper_bgcolor='#1f2833',
                plot_bgcolor='#1f2833',
                font=dict(color='#c5c6c7')
            )
            panel1_genre[g] = fig1.to_json()

        # --------------------------
        # PANEL-5: sunburst that mirrors original UI
        # --------------------------
        df_ac = pd.DataFrame({
            "actor": list(genre_actors[g].keys()),
            "count": list(genre_actors[g].values())
        })

        if df_ac.empty:
            empty_fig5 = go.Figure()
            empty_fig5.update_layout(
                paper_bgcolor="#1f2833",
                plot_bgcolor="#1f2833",
                font=dict(color="#c5c6c7")
            )
            panel5_genre[g] = empty_fig5.to_json()
        else:
            df_ac = df_ac.sort_values("count", ascending=False).head(30).reset_index(drop=True)

            # Labels: central genre + actors
            labels = [g] + df_ac["actor"].tolist()
            parents = [""] + [g for _ in df_ac["actor"]]

            # values: aggregate at center + actor counts
            center_value = int(df_ac["count"].sum())
            values = [center_value] + df_ac["count"].astype(int).tolist()

            # Colors: give the genre node a palette color, actors darker versions
            palette_color = TEAL_PALETTE[i % len(TEAL_PALETTE)]
            colors = [palette_color] + [darker(palette_color) for _ in df_ac["actor"]]

            fig5 = go.Figure(go.Sunburst(
                labels=labels,
                parents=parents,
                values=values,
                branchvalues="total",
                maxdepth=2,
                insidetextorientation='radial',
                marker=dict(colors=colors, line=dict(width=1.5, color="white")),
                hovertemplate="<b>%{label}</b><br>Movies: %{value}<extra></extra>"
            ))

            fig5.update_layout(
                margin=dict(l=20, r=20, t=80, b=20),
                height=650,
                paper_bgcolor="#1f2833",
                plot_bgcolor="#1f2833",
                font=dict(color="#c5c6c7")
            )

            panel5_genre[g] = fig5.to_json()

        # --------------------------
        # PANEL-3: revenue over time for selected genre
        # (single-line time series to match streamgraph style but only for that genre)
        # --------------------------
        # filter movies containing this genre
        try:
            mask = movies["genres_list"].apply(lambda lst: g in lst if isinstance(lst, list) else False)
            df_year = movies[mask].groupby("year")["revenue"].sum().reset_index().sort_values("year")
        except Exception:
            df_year = pd.DataFrame(columns=["year", "revenue"])

        if df_year.empty:
            empty_fig3 = go.Figure()
            empty_fig3.update_layout(
                paper_bgcolor='#1f2833',
                plot_bgcolor='#1f2833',
                font=dict(color='#c5c6c7')
            )
            panel3_genre[g] = empty_fig3.to_json()
        else:
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(
                x=df_year["year"].tolist(),
                y=df_year["revenue"].tolist(),
                mode='lines',
                name=g,
                line=dict(width=2)
            ))
            fig3.update_layout(
                xaxis_title="Year",
                yaxis_title="Revenue",
                paper_bgcolor='#1f2833',
                plot_bgcolor='#1f2833',
                font=dict(color='#c5c6c7'),
                xaxis=dict(gridcolor='#45a29e'),
                yaxis=dict(gridcolor='#45a29e'),
                height=600
            )
            panel3_genre[g] = fig3.to_json()

    return panel1_genre, panel5_genre, panel3_genre


# ---------------------------
# Panels view
# ---------------------------
def panel1_genre_keyword(movies):
    """Genre-Keyword Map (Bar Chart)"""
    print("[INFO] Generating Panel 1...")

    # Count keywords per genre
    rows = []
    for _, row in movies.iterrows():
        for g in row["genres_list"]:
            for kw in row["keywords_list"]:
                rows.append((str(g), str(kw)))
    df = pd.DataFrame(rows, columns=["genre", "keyword"])

    top_kw = (
        df.groupby("keyword")
        .size()
        .sort_values(ascending=False)
        .head(50)
        .reset_index(name="count")
    )

    # Convert to Python lists for proper serialization
    keywords = top_kw["keyword"].tolist()
    counts = top_kw["count"].tolist()

    # Create bar chart with go.Bar
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=counts,
        y=keywords,
        orientation='h',
        marker=dict(
            color=counts,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Count')
        ),
        hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>'
    ))

    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        xaxis_title="Count",
        yaxis_title="Keyword",
        height=600,
        margin=dict(l=150, r=50, t=50, b=50),
        yaxis_tickfont=dict(size=11),
        paper_bgcolor='#1f2833',
        plot_bgcolor='#1f2833',
        font=dict(color='#c5c6c7')
    )
    
    return fig.to_json()

def panel2_director_matrix(movies):
    """Director Style Matrix (Scatter)"""
    print("[INFO] Generating Panel 2...")

    directors = movies.groupby("director").agg({
        "vote_average": "mean",
        "revenue": "mean",
        "title": "count"
    }).dropna().reset_index()
    
    directors = directors.sort_values("revenue", ascending=False).head(100)
    
    x_vals = directors["revenue"].tolist()
    y_vals = directors["vote_average"].tolist()
    hover_names = directors["director"].tolist()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals,
        mode='markers',
        text=hover_names,
        hoverinfo='text+x+y',
        marker=dict(
            size=14,
            color=y_vals,
            colorscale='Teal',
            showscale=True,
            line=dict(width=1, color='#c5c6c7'),
            colorbar=dict(title=dict(text='Rating', font=dict(color='#c5c6c7')), tickfont=dict(color='#c5c6c7'))
        )
    ))
    
    fig.update_layout(
        xaxis_title="Revenue",
        yaxis_title="Vote (Average)",
        paper_bgcolor='#1f2833',
        plot_bgcolor='#1f2833',
        font=dict(color='#c5c6c7'),
        height=600,
        xaxis=dict(gridcolor='#45a29e'),
        yaxis=dict(gridcolor='#45a29e')
    )
    
    return fig.to_json()

def panel3_streamgraph(movies):
    """Genre streamgraph over time (Area Chart)"""
    print("[INFO] Generating Panel 3...")

    rows = []
    for _, row in movies.iterrows():
        for g in row["genres_list"]:
            rows.append((row["year"], g, row["revenue"]))

    df = pd.DataFrame(rows, columns=["year", "genre", "revenue"])
    grouped = df.groupby(["year", "genre"])["revenue"].sum().reset_index()
    
    fig = go.Figure()
    
    for genre in grouped["genre"].unique():
        genre_data = grouped[grouped["genre"] == genre].sort_values("year")
        fig.add_trace(go.Scatter(
            x=genre_data["year"].tolist(),
            y=genre_data["revenue"].tolist(),
            mode='lines',
            name=genre,
            stackgroup='one'
        ))
    
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Revenue",
        paper_bgcolor='#1f2833',
        plot_bgcolor='#1f2833',
        font=dict(color='#c5c6c7'),
        xaxis=dict(gridcolor='#45a29e'),
        yaxis=dict(gridcolor='#45a29e')
    )
    
    return fig.to_json()

def panel4_global_map(movies):
    """Premium World Map — Country Film Production Tiers"""
    print("[INFO] Generating Panel 4...")

    rows = []
    for _, row in movies.iterrows():
        for c in row["countries"]:
            rows.append(c)

    df = pd.DataFrame(rows, columns=["country"])
    country_counts = df["country"].value_counts().reset_index()
    country_counts.columns = ["country", "count"]

    bins = [-1, 0, 10, 50, 100, 500, 99999]
    labels = ["No Data", "1-10", "11-50", "51-100", "101-500", ">500"]

    country_counts["production_level"] = pd.cut(
        country_counts["count"], bins=bins, labels=labels
    )

    midnight_palette = [
        "#2c3e50",
        "#004d40",
        "#00796b",
        "#26a69a",
        "#4db6ac",
        "#66fcf1",
    ]

    fig = px.choropleth(
        country_counts,
        locations="country",
        locationmode="country names",
        color="production_level",
        hover_name="country",
        hover_data={"count": True, "production_level": False},
        color_discrete_sequence=midnight_palette,
        category_orders={"production_level": labels},
    )

    fig.update_geos(
        showframe=False,
        showcoastlines=True,
        projection_type="equirectangular",
        bgcolor='#1f2833',
        landcolor="#0b0c10",
        oceancolor="#1f2833",
        showocean=True,
        coastlinecolor="#45a29e",
    )

    fig.update_layout(
        legend=dict(
            title=dict(text="Production Tier", font=dict(color="#c5c6c7", size=14)),
            bgcolor="rgba(31, 40, 51, 0.8)",
            orientation="h",
            yanchor="top",
            y=-0.12,
            x=0.5,
            xanchor="center",
            font=dict(size=14, color="#c5c6c7"),
        ),
        margin=dict(l=20, r=20, t=70, b=20),
        height=600,
        paper_bgcolor='#1f2833',
        plot_bgcolor='#1f2833',
        font=dict(color='#c5c6c7')
    )

    return fig.to_json()

def panel5_actor_genre_network(movies):
    """Circle Packing with Beautiful Teal Gradient Theme"""
    print("[INFO] Generating Panel 5...")

    records = []
    actor_counts = {}

    for _, row in movies.iterrows():
        actor = row["top_actor"]
        genres = row["genres_list"]
        if not actor or not genres:
            continue

        actor_counts[actor] = actor_counts.get(actor, 0) + 1

        for g in genres:
            records.append((str(actor), str(g)))

    top30 = sorted(actor_counts.items(), key=lambda x: x[1], reverse=True)[:30]
    top30_names = [a for a, _ in top30]

    filtered_records = [(a, g) for a, g in records if a in top30_names]

    labels = []
    parents = []
    values = []
    colors = []

    genre_set = sorted(set(g for _, g in filtered_records))

    TEAL_PALETTE = [
        "#66FCF1", "#45A29E", "#3EC7BA", "#31A6A4",
        "#2E8C8E", "#207070", "#175E5C", "#0E4A47"
    ]

    def get_genre_color(i):
        return TEAL_PALETTE[i % len(TEAL_PALETTE)]

    def darker(hex_color):
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16) * 0.75
        g = int(hex_color[2:4], 16) * 0.75
        b = int(hex_color[4:6], 16) * 0.75
        return f"rgba({int(r)},{int(g)},{int(b)},0.95)"

    genre_actor_counts = {}
    for actor, genre in filtered_records:
        if genre not in genre_actor_counts:
            genre_actor_counts[genre] = {}
        genre_actor_counts[genre][actor] = genre_actor_counts[genre].get(actor, 0) + 1

    for i, genre in enumerate(genre_set):
        g_color = get_genre_color(i)

        labels.append(genre)
        parents.append("")
        values.append(sum(genre_actor_counts[genre].values()))
        colors.append(g_color)

        for actor, count in genre_actor_counts[genre].items():
            labels.append(actor)
            parents.append(genre)
            values.append(count)
            colors.append(darker(g_color))

    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        maxdepth=2,
        insidetextorientation='radial',
        marker=dict(
            colors=colors,
            line=dict(width=1.5, color="white")
        ),
        hovertemplate="<b>%{label}</b><br>Movies: %{value}<extra></extra>"
    ))

    fig.update_layout(
        margin=dict(l=20, r=20, t=80, b=20),
        height=650,
        paper_bgcolor="#1f2833",
        plot_bgcolor="#1f2833",
        font=dict(color="#c5c6c7")
    )

    return fig.to_json()
