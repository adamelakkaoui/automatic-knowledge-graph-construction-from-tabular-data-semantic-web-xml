# Automatic Knowledge-Graph Construction from Tabular Data (Semantic Web & XML)

Academic project that converts a small tabular dataset into RDF and enriches the resulting graph with rule-based relations, TF-IDF/cosine-similarity links, inferred memberships, and ontology mappings.

## Verified contents

- `src/intelligent_lod_converter.py`: CSV loading, RDF construction with RDFLib, relation discovery, static DBpedia city links, and RDF export.
- `src/comparison_r2rml.py`: fixed-mapping baseline and a comparison report.
- `notebooks/`: cleaned copies of the submitted notebooks; cell outputs and machine-specific metadata were removed.
- `etudiants.csv`: anonymized, synthetic ten-row example. Names and email addresses from the submitted example were replaced.

The source aligns terms with FOAF, Schema.org, AIISO, Dublin Core, and DBpedia resources. The so-called “R2RML Classic” baseline in the submitted code is a fixed Python mapping; it does **not** parse or execute an R2RML mapping document and must not be interpreted as a standards-compliant R2RML engine benchmark.

## Portfolio correction

The submitted comparison notebook executed the fixed baseline but inserted the intelligent-converter measurements as hard-coded values. In this copy, `src/comparison_r2rml.py` actually instantiates and runs `IntelligentLODConverter` before building the comparison. The original cleaned comparison notebook is retained as `comparison_r2rml_original.ipynb` for provenance.

## Technologies

Python, pandas, NumPy, RDFLib, scikit-learn, RDF/Turtle/N-Triples/XML.

## Installation and use

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python src/intelligent_lod_converter.py
python src/comparison_r2rml.py
```

Run the commands from the repository root because the academic scripts use relative paths. Generated RDF and text reports are ignored by Git.

## Limitations

The example is synthetic and contains only ten rows. Relation rules and DBpedia city mappings are domain-specific, similarity uses a fixed threshold, and pairwise discovery includes quadratic work. No large-scale or external R2RML-engine evaluation is included.

## Authors

- Adam El Akkaoui
- Mohammed Zaidouh

The original article acknowledges Prof. A. Ouacha for academic supervision.

## Academic artefacts

- [French academic article (DOCX, contact details redacted)](docs/academic-article-fr.docx). No separate presentation or video was found.

## Testing and limitations

Python 3.11 produced 395 triples from the anonymized ten-row CSV. The corrected comparison produced 90 triples for the fixed Python baseline and 395 for the enriched converter, with 138 relation statements counted by the script. Both cleaned notebooks validate with no saved outputs. This is not an execution of an R2RML mapping or external R2RML engine; historical article figures were not reproduced.
