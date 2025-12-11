// static/app.js

// Helps to render plot
function plot(id, jsonStr) {
    if (!jsonStr) return;
    const fig = JSON.parse(jsonStr);
    Plotly.newPlot(id, fig.data, fig.layout, { responsive: true });
}

// Populate dropdown with available genres
function populateGenreDropdown() {
    const dropdown = document.getElementById("genreFilter");
    // ensure graphs.genre_panel1 exists
    if (!graphs.genre_panel1) return;
    const genres = Object.keys(graphs.genre_panel1).sort();

    genres.forEach(g => {
        const op = document.createElement("option");
        op.value = g;
        op.textContent = g;
        dropdown.appendChild(op);
    });
}

// Update panel1, panel3, panel5 automatically on genre change
function updatePanelsByGenre() {
    const selected = document.getElementById("genreFilter").value;

    if (selected === "All") {
        plot("panel1", graphs.panel1);
        plot("panel3", graphs.panel3);
        plot("panel5", graphs.panel5);
    } else {
        // Panel-1: genre-specific keywords
        if (graphs.genre_panel1 && graphs.genre_panel1[selected]) {
            plot("panel1", graphs.genre_panel1[selected]);
        } else {
            plot("panel1", graphs.panel1);
        }

        // Panel-3: genre-specific revenue time series (single-line)
        if (graphs.genre_panel3 && graphs.genre_panel3[selected]) {
            plot("panel3", graphs.genre_panel3[selected]);
        } else {
            plot("panel3", graphs.panel3);
        }

        // Panel-5: genre-specific sunburst
        if (graphs.genre_panel5 && graphs.genre_panel5[selected]) {
            plot("panel5", graphs.genre_panel5[selected]);
        } else {
            plot("panel5", graphs.panel5);
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    // populate dropdown
    populateGenreDropdown();

    // updated panel view
    const selected_panel = document.getElementById("genreFilter");
    if (selected_panel) selected_panel.addEventListener("change", updatePanelsByGenre);

    // render
    plot('panel1', graphs.panel1);
    plot('panel2', graphs.panel2);
    plot('panel3', graphs.panel3);
    plot('panel4', graphs.panel4);
    plot('panel5', graphs.panel5);
});
