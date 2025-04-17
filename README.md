# PELV-VCR Paper

This repository contains the LaTeX source, metadata, and automated submission pipeline for the paper titled "PELV-VCR: A Conceptual Framework for Enhancing Self-Supervised Video Representation Learning via Neurocognitively Inspired Mechanisms" by William Kyle Million.

## About

The paper introduces the Perceptual Emergence Layer for VJ-VCR (PELV-VCR), a novel conceptual framework that enhances Meta AI's Video Joint Embedding Predictive Architecture with Variance-Covariance Regularization (VJ-VCR) by integrating computational modules inspired by human cognitive processes. These include a Saliency Masker, Meta-Contextual Intent Vector, Pattern Entangler, and Counterfactual Synthesizer.

## Repository Structure

- `draft/` - Contains the LaTeX source files
- `scripts/` - Contains tools for metadata processing and validation
- `.github/workflows/` - Contains CI/CD pipeline for automated arXiv submission
- `metadata.yaml` - Structured metadata for the paper
- `references.bib` - Bibliography in BibTeX format
- `Makefile` - Build automation for PDF generation and validation

## Quickstart

1. **Edit Metadata**: Update `metadata.yaml` with your actual ORCID URI.
2. **Write Paper Content**: Populate the sections in `draft/main.tex` with your paper's content.
3. **Add References**: Fill `references.bib` with the BibTeX entries for all citations.
4. **Local Build**:
   * Run `make pdf` to compile `draft/main.pdf`.
   * Run `make check` to verify PDF/A compliance.
5. **GitHub Workflow**:
   * Configure the necessary secrets in the repository settings.
   * Tag a release (e.g., `v0.1.0`) to trigger the automatic submission workflow.

## License

This work is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License](LICENSE). 