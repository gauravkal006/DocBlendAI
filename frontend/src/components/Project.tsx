import { ArrowLeft } from "lucide-react";
import { useState } from "react";

const screens = ["overview", "extraction", "calibration", "performance"] as const;
type Screen = (typeof screens)[number];

const labels: Record<Screen, string> = {
  overview: "Overview",
  extraction: "Extraction",
  calibration: "Calibration",
  performance: "Performance",
};

export function Project() {
  const [screen, setScreen] = useState<Screen>("overview");

  return (
    <div className="project-page">
      <nav className="project-nav" aria-label="Project sections">
        <a className="project-brand" href="/">DocBlendAI</a>
        <div className="project-tabs">
          {screens.map((id) => (
            <button key={id} type="button" className={screen === id ? "is-active" : ""} onClick={() => setScreen(id)}>
              {labels[id]}
            </button>
          ))}
        </div>
        <div className="project-actions">
          <a className="project-back" href="/visualizations" target="_blank" rel="noreferrer">Visualizations</a>
          <a className="project-back" href="/"><ArrowLeft size={16} /> Open app</a>
        </div>
      </nav>

      <main className="project-main">
        {screen === "overview" && (
          <section className="project-screen">
            <header className="project-hero">
              <p>Project showcase</p>
              <h1>Confidence-aware document understanding</h1>
              <span>DocBlendAI turns typed, scanned, and handwritten documents into reliable answers grounded in source text.</span>
            </header>
            <div className="project-pipeline">
              {[["01", "Input", "PDF, image, Word, PowerPoint or text"], ["02", "Detect", "Typed, scanned or handwritten"], ["03", "Extract", "OCR / HTR and layout analysis"], ["04", "Calibrate", "Convert confidence into accuracy"], ["05", "Retrieve", "Rank relevant evidence"], ["06", "Answer", "Grounded response and reliability"]].map(([number, title, copy]) => (
                <article key={number}><b>{number}</b><h2>{title}</h2><p>{copy}</p></article>
              ))}
            </div>
          </section>
        )}

        {screen === "extraction" && (
          <section className="project-screen">
            <header className="project-heading"><p>Text extraction</p><h1>Three document paths, one pipeline</h1></header>
            <div className="project-cards">
              <article><span>Typed</span><h2>Digital text parser</h2><p>Reads the existing PDF, DOCX, PPTX, or text layer.</p><code>Digital text → layout → chunks</code></article>
              <article><span>Printed scan</span><h2>Tesseract OCR</h2><p>Recognises words and preserves page positions.</p><code>Page → OCR → word confidence</code></article>
              <article><span>Handwriting</span><h2>PaddleOCR / TrOCR</h2><p>Detects text lines and recognises handwritten content.</p><code>Page → lines → HTR confidence</code></article>
            </div>
          </section>
        )}

        {screen === "calibration" && (
          <section className="project-screen">
            <header className="project-heading"><p>Confidence calibration</p><h1>From model score to expected character accuracy</h1></header>
            <div className="project-calibration"><article><span>OCR raw confidence</span><strong>0.70</strong></article><b>→</b><article><span>Piecewise-linear calibration</span><strong>0.70 → 0.73</strong></article><b>→</b><article><span>Calibrated confidence</span><strong>0.73</strong></article></div>
            <p className="project-result">Held-out calibration error: <strong>0.062 → 0.013</strong> for scanned pages.</p>
          </section>
        )}

        {screen === "performance" && (
          <section className="project-screen">
            <header className="project-heading"><p>Evaluation</p><h1>Measured project performance</h1></header>
            <div className="project-metrics">
              <article><strong>88%</strong><span>Overall answer correctness</span></article>
              <article><strong>88%</strong><span>Retrieval hit rate</span></article>
              <article><strong>100%</strong><span>Correct Certain answers</span></article>
              <article><strong>100%</strong><span>Typed recognition accuracy</span></article>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}
