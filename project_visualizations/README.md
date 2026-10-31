# DocBlendAI Project Visualizations

This folder contains presentation-ready charts explaining the document extraction and confidence-calibration pipeline.

## Generate screenshots

From the repository root:

```bash
python project_visualizations/generate_visualizations.py
```

The script reads:

- `evaluation/results/results.json` for format detection, extraction errors, and confidence values
- `data/calibration.json` for fitted calibration knots

It creates PNG and SVG files in `screenshots/`.

Open `index.html` in a browser to view the complete screenshot gallery.

## Included visuals

- Format detection matrix
- Extraction character/word error rates
- Extraction pipeline and tool routing
- Raw-to-calibrated confidence curves
- Calibration calculation method
- Answer correctness and retrieval metrics

## Evaluation note

The values come from the repository's evaluation dataset and should be presented as pipeline measurements. Real student documents may produce different results.
