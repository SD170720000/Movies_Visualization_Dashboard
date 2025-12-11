# app.py

from flask import Flask, render_template, jsonify
import argparse

from scripts.scrape import load_data
from scripts.visualize import (
    panel1_genre_keyword,
    panel2_director_matrix,
    panel3_streamgraph,
    panel4_global_map,
    panel5_actor_genre_network,
    genre_filter_data
)

app = Flask(__name__)

# Global storage for graph JSONs
GRAPHS = {}

def run_batch():
    global GRAPHS
    print("[INFO] Loading data...")
    movies = load_data()

    print("[INFO] Generating visualizations (Plotly)...")
    GRAPHS["panel1"] = panel1_genre_keyword(movies)
    GRAPHS["panel2"] = panel2_director_matrix(movies)
    GRAPHS["panel3"] = panel3_streamgraph(movies)
    GRAPHS["panel4"] = panel4_global_map(movies)
    GRAPHS["panel5"] = panel5_actor_genre_network(movies)
    
    # build genre-specific panel1, panel5, panel3
    g1, g5, g3 = genre_filter_data(movies)
    GRAPHS["genre_panel1"] = g1
    GRAPHS["genre_panel5"] = g5
    GRAPHS["genre_panel3"] = g3



# Serve minimal page first; graphs loaded via AJAX
@app.route("/")
def index():
    return render_template("index.html")

# API endpoint to get graphs (heavy processing happens here)
@app.route("/get_graphs")
def get_graphs():
    global GRAPHS
    if not GRAPHS:
        run_batch()
    return jsonify(GRAPHS)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()
    print("[INFO] Starting Flask server.")
    app.run(port=args.port, debug=True)
