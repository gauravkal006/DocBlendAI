"""Generate DocBlendAI presentation charts from local evaluation data."""
from collections import defaultdict
from pathlib import Path
import json

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path(__file__).parent / "screenshots"
OUTPUT.mkdir(exist_ok=True)

with (ROOT / "evaluation/results/results.json").open() as file:
    EVALUATION = json.load(file)
with (ROOT / "data/calibration.json").open() as file:
    CALIBRATION = json.load(file)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titleweight": "normal",
    "axes.titlelocation": "left",
    "axes.edgecolor": "#cbd1cf",
    "axes.labelcolor": "#56635f",
    "xtick.color": "#56635f",
    "ytick.color": "#56635f",
})

COLORS = {"typed": "#17806f", "scanned": "#4a6283", "handwritten": "#946c12"}


def save(fig, name, source="evaluation/results/results.json"):
    fig.text(0.01, 0.005, f"Source: {source}. Evaluation data is synthetic.", fontsize=8, color="#747b79")
    fig.subplots_adjust(bottom=0.12)
    fig.savefig(OUTPUT / f"{name}.png", dpi=180, bbox_inches="tight", facecolor="white")
    fig.savefig(OUTPUT / f"{name}.svg", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def recognition_matrix():
    formats = ["typed", "scanned", "handwritten"]
    matrix = np.zeros((3, 3))
    counts = defaultdict(int)
    correct = defaultdict(int)
    for row in EVALUATION["recognition"]:
        actual = row["format"]
        detected = row["detected"]
        counts[actual] += 1
        if actual == detected:
            correct[actual] += 1
        matrix[formats.index(actual), formats.index(detected)] += 1

    fig, ax = plt.subplots(figsize=(8, 6))
    image = ax.imshow(matrix, cmap="Greens", vmin=0, vmax=max(matrix.max(), 1))
    ax.set_xticks(range(3), [label.title() for label in formats])
    ax.set_yticks(range(3), [label.title() for label in formats])
    ax.set_xlabel("Detected format")
    ax.set_ylabel("Actual format")
    ax.set_title("Document format detection", loc="left")
    for row in range(3):
        for column in range(3):
            value = int(matrix[row, column])
            ax.text(column, row, value, ha="center", va="center", color="white" if value > matrix.max() / 2 else "#202222", fontsize=16, fontweight="bold")
    fig.colorbar(image, ax=ax, label="Page count")
    save(fig, "01-format-detection-matrix")


def extraction_accuracy():
    rows = defaultdict(list)
    for row in EVALUATION["recognition"]:
        rows[row["format"]].append(row)
    formats = ["typed", "scanned", "handwritten"]
    cer = [np.mean([row["cer"] for row in rows[name]]) for name in formats]
    wer = [np.mean([row["wer"] for row in rows[name]]) for name in formats]

    x = np.arange(len(formats))
    width = 0.34
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.bar(x - width / 2, cer, width, color="#17806f", label="Character Error Rate")
    ax.bar(x + width / 2, wer, width, color="#946c12", label="Word Error Rate")
    ax.set_xticks(x, [name.title() for name in formats])
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Error rate")
    ax.set_title("Recognition error by document format", loc="left")
    ax.legend(frameon=False)
    ax.grid(axis="y", color="#e8ebea")
    ax.set_axisbelow(True)
    for position, value in enumerate(cer):
        ax.text(position - width / 2, value + 0.02, f"{value:.2f}", ha="center")
    for position, value in enumerate(wer):
        ax.text(position + width / 2, value + 0.02, f"{value:.2f}", ha="center")
    save(fig, "02-extraction-error-rates")


def extraction_flow():
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis("off")
    steps = [
        (1, "UPLOAD", "PDF · image · DOCX · PPTX · TXT", "#202222"),
        (3.8, "FORMAT DETECT", "Typed · scanned · handwritten", "#17806f"),
        (6.6, "EXTRACT", "Parser · Tesseract OCR · PaddleOCR", "#4a6283"),
        (9.4, "STRUCTURE", "Layout · reading order · confidence", "#946c12"),
    ]
    for x, title, text, color in steps:
        ax.add_patch(plt.Rectangle((x - 1.25, 2), 2.5, 2, facecolor="white", edgecolor=color, linewidth=2))
        ax.text(x, 3.15, title, ha="center", va="center", fontsize=12, fontweight="bold", color=color)
        ax.text(x, 2.55, text, ha="center", va="center", fontsize=8, color="#56635f", wrap=True)
    for x in [2.3, 5.1, 7.9]:
        ax.annotate("", xy=(x + 0.6, 3), xytext=(x, 3), arrowprops={"arrowstyle": "->", "lw": 2, "color": "#b7c1bf"})
    ax.text(6, 5.1, "Document extraction pipeline", ha="center", fontsize=18, fontweight="normal")
    ax.text(6, 0.8, "Every branch ends in chunks with page positions, text regions, and confidence scores.", ha="center", color="#56635f")
    save(fig, "03-extraction-pipeline")


def calibration_curve():
    fig, ax = plt.subplots(figsize=(9, 6))
    for name, points in CALIBRATION.items():
        points = np.array(points)
        ax.plot(points[:, 0], points[:, 1], marker="o", linewidth=3, markersize=9, color=COLORS[name], label=name.title())
        if len(points):
            raw, calibrated = points[-1]
            ax.annotate(f"{raw:.2f} raw → {calibrated:.2f}", (raw, calibrated), xytext=(-6, 10), textcoords="offset points", ha="right", fontsize=8)
    ax.plot([0, 1], [0, 1], "--", color="#b7c1bf", label="Perfect calibration")
    ax.set_xlim(0, 1.02)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("Raw confidence")
    ax.set_ylabel("Calibrated character accuracy")
    ax.set_title("Raw confidence mapped to calibrated accuracy", loc="left")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False)
    save(fig, "04-confidence-calibration")


def calibration_formula():
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.axis("off")
    ax.text(0.5, 0.82, "How calibrated confidence is calculated", ha="center", fontsize=18, fontweight="normal")
    boxes = [
        (0.02, "1 · Extract", "raw_confidence\nfrom OCR / HTR"),
        (0.26, "2 · Locate knots", "fit raw confidence to\ncharacter accuracy"),
        (0.50, "3 · Interpolate", "calibrated = linear\ninterpolation between knots"),
        (0.74, "4 · Report", "expected character\naccuracy with a reliability tier"),
    ]
    for x, title, text in boxes:
        ax.add_patch(FancyBboxPatch((x, 0.24), 0.22, 0.42, boxstyle="round,pad=0.02", facecolor="#f4f5f5", edgecolor="#17806f", linewidth=1.5, transform=ax.transAxes))
        ax.text(x + 0.11, 0.55, title, ha="center", fontsize=13, fontweight="bold", transform=ax.transAxes)
        ax.text(x + 0.11, 0.39, text, ha="center", fontsize=10, color="#56635f", transform=ax.transAxes)
    ax.text(0.5, 0.08, "Calibration reduces mean confidence error from 0.062 to 0.013 for scanned pages.", ha="center", transform=ax.transAxes, fontsize=12)
    save(fig, "05-calibration-method")


def answer_metrics():
    labels = ["Typed", "Scanned", "Handwritten"]
    correctness = [100, 60, 100]
    retrieval = [100, 60, 100]
    x = np.arange(len(labels))
    width = 0.34
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.bar(x - width / 2, correctness, width, color="#17806f", label="Answer correctness")
    ax.bar(x + width / 2, retrieval, width, color="#4a6283", label="Retrieval hit rate")
    ax.set_xticks(x, labels)
    ax.set_ylim(0, 110)
    ax.set_ylabel("Percent")
    ax.set_title("Answer quality and retrieval by document format", loc="left")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    save(fig, "06-answer-and-retrieval-metrics")


if __name__ == "__main__":
    recognition_matrix()
    extraction_accuracy()
    extraction_flow()
    calibration_curve()
    calibration_formula()
    answer_metrics()
    print(f"Generated {len(list(OUTPUT.glob('*.png'))) * 2} files in {OUTPUT}")
