# Technical Documentation: PELV-VCR arXiv Submission Pipeline Setup

**Date:** 2025-04-17 (Approximate)
**Project:** Automated arXiv submission for the PELV-VCR paper.
**Goal:** Establish a robust, automated workflow using GitHub Actions to compile a LaTeX paper, ensure compliance, and submit it to arXiv upon tagging a release.

## 1. Project Structure

A dedicated `paper/` directory was created in the workspace (`C:\Users\wkmil\.cursor\SharedInformation\Projects\ProjectReports\V-JEPA2Solution`) containing the following key components:

-   **`draft/main.tex`:** The main LaTeX source file for the paper. Initially populated with preamble, abstract, and section stubs based on `arXivPreprint.txt`. Requires content filling.
-   **`references.bib`:** BibTeX file for managing citations. Initially empty, requires population.
-   **`metadata.yaml`:** Contains metadata required for arXiv submission (title, authors, abstract, categories, license). Uses YAML for human readability.
    -   **License:** Set to `CC-BY-NC-4.0` (Creative Commons Attribution-NonCommercial 4.0 International) based on user requirements.
-   **`LICENSE`:** Contains the full text for the CC-BY-NC-4.0 license.
-   **`scripts/metadata_from_yaml.py`:** Python script to validate `metadata.yaml` (e.g., character limits) and convert it to `metadata.json` for the workflow.
-   **`Makefile`:** Automates local build processes:
    -   `make pdf`: Compiles the LaTeX document using `latexmk`.
    -   `make check`: Checks for font embedding issues (`pdffonts`) and generates a PDF/A compliant version using `ghostscript`.
    -   `make clean`: Cleans up intermediate LaTeX files.
-   **`.github/workflows/arxiv.yml`:** GitHub Actions workflow definition.
    -   **Trigger:** Runs automatically when a tag matching `v*.*.*` (e.g., `v1.0.0`) is pushed to the repository.
    -   **Jobs:**
        -   `build-validate`: Installs TeX Live & Ghostscript, compiles the PDF, performs font/PDF/A checks, generates `metadata.json`, uploads artifacts.
        -   `submit`: Downloads artifacts, packages source files (`.tex`, `.bib`, images if added) into `submission.tar.gz`, and uses SFTP (`appleboy/scp-action`) to upload the tarball, the final PDF, and `metadata.json` to `upload.arxiv.org`. Requires `ARXIV_USER` and `ARXIV_TOKEN` secrets configured in GitHub. Optionally notifies Slack (`SLACK_WEBHOOK_URL` secret).
-   **`README.md`:** Provides user instructions for populating content, local building, configuring secrets, and triggering the submission.

## 2. GitHub Repository Setup

-   **Repository:** `IntuiTek/pelv-vcr-paper` ([https://github.com/IntuiTek/pelv-vcr-paper](https://github.com/IntuiTek/pelv-vcr-paper))
-   **Access:** Intended to be managed under the `IntuiTek` organization.
-   **Initial Content:** The entire `paper/` directory structure and files were pushed to this repository.

## 3. Authentication Resolution (HTTPS vs. SSH)

A significant challenge involved authenticating Git operations (specifically `git push`) from the local environment to the `IntuiTek/pelv-vcr-paper` repository.

-   **Initial Problem:** Push attempts failed with a `403 Forbidden` error, indicating permission denial. The error message explicitly mentioned `thebrierfox`, which was identified as an incorrect GitHub identity without access to the `IntuiTek` organization repositories.
-   **Diagnosis:**
    1.  Checked local Git config (`git config user.name`/`email`): Showed `AEGIS`/`aegis@anthropic.local`, relevant for commit authorship but not push authentication via SSH.
    2.  Tested SSH connection (`ssh -T git@github.com`): This **successfully** authenticated as `KyleMillion` (the identity associated with the `kyle@intuitek.ai` email used for the key), confirming the SSH key itself and its association with the correct GitHub account were working.
    3.  Checked Git remote configuration (`git remote -v`): Revealed the `origin` remote was using an `https://...` URL.
-   **Root Cause:** Using HTTPS for the remote URL caused Git to rely on the Windows Credential Manager, which had cached credentials for the `thebrierfox` user for `github.com`. SSH keys were being ignored.
-   **Solution - Switch to SSH:**
    1.  **Generate SSH Key:** An ED25519 SSH key pair was generated specifically for this purpose (`~/.ssh/id_ed25519_intuitek` and `.pub`) associated with the email `kyle@intuitek.ai`.
    2.  **Add Key to GitHub:** The public key (`id_ed25519_intuitek.pub`) was added to the SSH keys in the GitHub settings for the `KyleMillion` account (which has access to `IntuiTek`).
    3.  **Configure SSH Client:** An SSH config file (`~/.ssh/config`) was created/updated to explicitly tell the SSH client to use the `id_ed25519_intuitek` key when connecting to `github.com`:
        ```
        Host github.com
          HostName github.com
          User git
          IdentityFile ~/.ssh/id_ed25519_intuitek
          IdentitiesOnly yes
        ```
    4.  **Update Git Remote URL:** The crucial step was changing the repository's remote URL from HTTPS to SSH using:
        ```bash
        git remote set-url origin git@github.com:IntuiTek/pelv-vcr-paper.git
        ```
-   **Final Hurdle - Host Key Verification:** The first attempt to push via SSH failed because the SSH client interactively prompted to verify GitHub's host fingerprint, which the terminal environment couldn't handle.
-   **Resolution:** GitHub's ED25519 public host key was manually added to the `~/.ssh/known_hosts` file using:
    ```powershell
    Add-Content -Path "$env:USERPROFILE\.ssh\known_hosts" -Value "github.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl" -Encoding ascii -ErrorAction SilentlyContinue
    ```
-   **Outcome:** Subsequent `git push -u origin main` command succeeded, authenticating correctly using the `id_ed25519_intuitek` SSH key associated with the `KyleMillion`/`kyle@intuitek.ai` identity.

## 4. Current Status & Next Steps

-   The local `paper/` directory contains the full project structure.
-   This structure has been successfully pushed to the `main` branch of `https://github.com/IntuiTek/pelv-vcr-paper`.
-   Authentication via SSH using the dedicated key (`id_ed25519_intuitek`) is confirmed working.
-   **Next steps for user:**
    1.  Fill in the content of `paper/draft/main.tex`.
    2.  Add BibTeX entries to `paper/references.bib` and corresponding `\cite{}` commands in `main.tex`.
    3.  Add required secrets (`ARXIV_USER`, `ARXIV_TOKEN`, optional `SLACK_WEBHOOK_URL`) to the GitHub repository settings (`Settings` -> `Secrets and variables` -> `Actions`).
    4.  Commit and push content changes to the repository.
    5.  When ready for submission, create and push a version tag (e.g., `git tag v0.1.0`, `git push origin v0.1.0`) to trigger the `arxiv.yml` workflow.

This setup provides a reliable foundation for managing the paper and automating the arXiv submission process, using secure SSH authentication linked to the appropriate GitHub identity. 