(() => {
  "use strict";

  const data = window.GBLS_METRICS;
  const groupLabels = {
    service_area: "Topic area / service area",
    theme: "Theme",
    outcome: "Outcome",
    audience: "Audience",
    game_format: "Game format",
    methodology: "Methodology",
    evidence_type: "Evidence type",
    source_type: "Source type",
    library_context: "Library context",
    contribution_type: "Contribution type",
    design_principles: "Design principle",
    coding_confidence: "Coding confidence",
  };
  const articleColumns = {
    service_area: "service_area",
    theme: "theme",
    outcome: "outcome",
    audience: "audience",
    game_format: "game_format",
    methodology: "methodology",
    evidence_type: "evidence_type",
    source_type: "source_type",
    library_context: "library_context",
    contribution_type: "contribution_type",
    design_principles: "design_principles",
    coding_confidence: "coding_confidence",
  };
  const state = {
    group: "service_area",
    limit: 15,
    yearStart: data.years[0],
    yearEnd: data.years[data.years.length - 1],
    selectedFeature: null,
    search: "",
  };

  const $ = (id) => document.getElementById(id);
  const pretty = (value) => String(value || "").replaceAll("_", " ");
  const splitLabels = (value) => String(value || "").split("|").filter(Boolean);
  const svgEl = (name, attributes = {}) => {
    const node = document.createElementNS("http://www.w3.org/2000/svg", name);
    Object.entries(attributes).forEach(([key, value]) => node.setAttribute(key, value));
    return node;
  };

  function renderSummary() {
    const metrics = [
      ["Articles", data.summary.total_articles.toLocaleString()],
      ["Coded labels", data.summary.unique_feature_labels.toLocaleString()],
      ["Feature assignments", data.summary.total_article_feature_assignments.toLocaleString()],
      ["Publication span", `${data.summary.earliest_year}-${data.summary.latest_year}`],
    ];
    $("summaryCards").innerHTML = metrics.map(([label, value]) => `
      <article class="summary-card">
        <span class="summary-value">${value}</span>
        <span class="summary-label">${label}</span>
      </article>
    `).join("");
  }

  function setupControls() {
    $("groupSelect").innerHTML = Object.keys(groupLabels)
      .map((key) => `<option value="${key}">${groupLabels[key]}</option>`).join("");
    const yearOptions = data.years.map((year) => `<option value="${year}">${year}</option>`).join("");
    $("yearStart").innerHTML = yearOptions;
    $("yearEnd").innerHTML = yearOptions;
    $("groupSelect").value = state.group;
    $("yearStart").value = state.yearStart;
    $("yearEnd").value = state.yearEnd;

    $("groupSelect").addEventListener("change", (event) => {
      state.group = event.target.value;
      state.selectedFeature = null;
      renderAll();
    });
    $("limitSelect").addEventListener("change", (event) => {
      state.limit = Number(event.target.value);
      renderRanking();
    });
    $("yearStart").addEventListener("change", (event) => {
      state.yearStart = Math.min(Number(event.target.value), state.yearEnd);
      $("yearStart").value = state.yearStart;
      renderAll();
    });
    $("yearEnd").addEventListener("change", (event) => {
      state.yearEnd = Math.max(Number(event.target.value), state.yearStart);
      $("yearEnd").value = state.yearEnd;
      renderAll();
    });
    $("articleSearch").addEventListener("input", (event) => {
      state.search = event.target.value.trim().toLowerCase();
      renderArticles();
    });
    $("clearFeatureButton").addEventListener("click", () => {
      state.selectedFeature = null;
      renderAll();
    });
    $("resetButton").addEventListener("click", () => {
      state.group = "service_area";
      state.limit = 15;
      state.yearStart = data.years[0];
      state.yearEnd = data.years[data.years.length - 1];
      state.selectedFeature = null;
      state.search = "";
      $("groupSelect").value = state.group;
      $("limitSelect").value = "15";
      $("yearStart").value = state.yearStart;
      $("yearEnd").value = state.yearEnd;
      $("articleSearch").value = "";
      renderAll();
    });
  }

  function articlesInRange() {
    return data.articles.filter((article) => {
      const year = Number(article.year);
      return !Number.isFinite(year) || (year >= state.yearStart && year <= state.yearEnd);
    });
  }

  function currentCounts() {
    const counts = new Map();
    for (const article of articlesInRange()) {
      const values = state.group === "coding_confidence"
        ? [article.coding_confidence]
        : splitLabels(article[articleColumns[state.group]]);
      new Set(values).forEach((value) => counts.set(value, (counts.get(value) || 0) + 1));
    }
    return [...counts.entries()]
      .map(([feature_value, article_count]) => ({ feature_value, article_count }))
      .sort((a, b) => b.article_count - a.article_count || a.feature_value.localeCompare(b.feature_value));
  }

  function renderRanking() {
    const rows = currentCounts().slice(0, state.limit);
    $("rankingTitle").textContent = `${groupLabels[state.group]} popularity`;
    const width = 820;
    const labelWidth = 210;
    const rowHeight = 28;
    const height = Math.max(150, rows.length * rowHeight + 30);
    const max = Math.max(...rows.map((row) => row.article_count), 1);
    const svg = svgEl("svg", { viewBox: `0 0 ${width} ${height}`, role: "img" });

    rows.forEach((row, index) => {
      const y = index * rowHeight + 8;
      const barWidth = (row.article_count / max) * (width - labelWidth - 70);
      const group = svgEl("g", {
        class: `bar-row${state.selectedFeature === row.feature_value ? " is-selected" : ""}`,
        tabindex: "0",
        role: "button",
        "aria-label": `${pretty(row.feature_value)}, ${row.article_count} articles`,
      });
      const label = svgEl("text", { x: labelWidth - 9, y: y + 16, "text-anchor": "end", class: "bar-label" });
      label.textContent = pretty(row.feature_value);
      const bar = svgEl("rect", {
        x: labelWidth, y, width: Math.max(2, barWidth), height: 20, rx: 4, fill: "#126782",
      });
      const value = svgEl("text", { x: labelWidth + barWidth + 8, y: y + 15, class: "bar-value" });
      value.textContent = row.article_count;
      const select = () => {
        state.selectedFeature = state.selectedFeature === row.feature_value ? null : row.feature_value;
        renderAll();
      };
      group.addEventListener("click", select);
      group.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") select();
      });
      group.append(label, bar, value);
      svg.append(group);
    });
    $("rankingChart").replaceChildren(svg);
  }

  function renderColumnChart(container, rows) {
    const width = 700;
    const height = 275;
    const margin = { top: 14, right: 12, bottom: 48, left: 42 };
    const plotWidth = width - margin.left - margin.right;
    const plotHeight = height - margin.top - margin.bottom;
    const max = Math.max(...rows.map((row) => row.value), 1);
    const svg = svgEl("svg", { viewBox: `0 0 ${width} ${height}`, role: "img" });
    [0, 0.5, 1].forEach((ratio) => {
      const y = margin.top + plotHeight * (1 - ratio);
      svg.append(svgEl("line", { x1: margin.left, x2: width - margin.right, y1: y, y2: y, class: "grid-line" }));
      const tick = svgEl("text", { x: margin.left - 8, y: y + 4, "text-anchor": "end", class: "axis-label" });
      tick.textContent = Math.round(max * ratio);
      svg.append(tick);
    });
    const slot = plotWidth / Math.max(rows.length, 1);
    rows.forEach((row, index) => {
      const barHeight = (row.value / max) * plotHeight;
      const x = margin.left + index * slot + slot * 0.14;
      const y = margin.top + plotHeight - barHeight;
      svg.append(svgEl("rect", {
        x, y, width: Math.max(2, slot * 0.72), height: barHeight, rx: 2, fill: "#126782",
      }));
      if (rows.length <= 25 || index % 2 === 0) {
        const label = svgEl("text", {
          x: x + slot * 0.36, y: height - 24, "text-anchor": "middle",
          class: "axis-label", transform: `rotate(-45 ${x + slot * 0.36} ${height - 24})`,
        });
        label.textContent = row.label;
        svg.append(label);
      }
    });
    container.replaceChildren(svg);
  }

  function renderYears() {
    const counts = new Map(data.publicationYears.map((row) => [Number(row.year_label), row.article_count]));
    const rows = data.years
      .filter((year) => year >= state.yearStart && year <= state.yearEnd)
      .map((year) => ({ label: String(year), value: counts.get(year) || 0 }));
    renderColumnChart($("yearChart"), rows);
  }

  function renderTrend() {
    const container = $("trendChart");
    if (!state.selectedFeature) {
      $("trendEmpty").hidden = false;
      container.replaceChildren();
      $("trendTitle").textContent = "Selected feature over time";
      return;
    }
    $("trendEmpty").hidden = true;
    $("trendTitle").textContent = `${pretty(state.selectedFeature)} over time`;
    const lookup = new Map(
      data.featureYears
        .filter((row) => row.feature_group === state.group && row.feature_value === state.selectedFeature)
        .map((row) => [Number(row.year), row.article_count]),
    );
    const rows = data.years
      .filter((year) => year >= state.yearStart && year <= state.yearEnd)
      .map((year) => ({ label: String(year), value: lookup.get(year) || 0 }));
    renderColumnChart(container, rows);
  }

  function hasSelectedFeature(article) {
    if (!state.selectedFeature) return true;
    const values = state.group === "coding_confidence"
      ? [article.coding_confidence]
      : splitLabels(article[articleColumns[state.group]]);
    return values.includes(state.selectedFeature);
  }

  function renderTags(value, max = 4) {
    const labels = splitLabels(value);
    const visible = labels.slice(0, max);
    if (labels.length > max) visible.push(`+${labels.length - max}`);
    return `<div class="tag-list">${visible.map((label) => `<span class="tag">${pretty(label)}</span>`).join("")}</div>`;
  }

  function renderArticles() {
    const filtered = articlesInRange().filter((article) => {
      if (!hasSelectedFeature(article)) return false;
      if (!state.search) return true;
      return Object.values(article).join(" ").toLowerCase().includes(state.search);
    });
    $("articleCount").textContent = filtered.length;
    $("activeFilter").hidden = !state.selectedFeature;
    $("activeFilter").textContent = state.selectedFeature
      ? `Filtered to ${groupLabels[state.group]}: ${pretty(state.selectedFeature)}`
      : "";
    $("articleRows").innerHTML = filtered.slice(0, 250).map((article) => `
      <tr>
        <td>${article.year || "n.d."}</td>
        <td class="citation-cell">${article.citation}</td>
        <td>${renderTags(article.library_context, 3)}</td>
        <td>${renderTags(article.game_format, 4)}</td>
        <td>${renderTags(article.service_area, 5)}</td>
        <td>${renderTags(article.theme, 5)}</td>
      </tr>
    `).join("");
  }

  function renderAll() {
    renderRanking();
    renderYears();
    renderTrend();
    renderArticles();
  }

  renderSummary();
  setupControls();
  renderAll();
})();
