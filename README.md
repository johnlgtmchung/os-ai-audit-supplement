# Source Traceability Supplement

This supplement accompanies *Feature-Boundary Audit Records for OS-Integrated AI: Toward Fleet Security Triage*. It links the documentary control matrix and PCC analysis to their sources.

## Files

- `source_manifest.csv`: 24 official sources, section/page locators, access dates, retrieval URLs, and response hashes where repeat fetches agreed.
- `boundary_registry.csv`: four scored capability profiles and one additional PCC agent-path record. Unobserved build, account, region, and configuration fields remain undetermined.
- `evidence_ledger.csv`: 20 dimension cells. Control score, scope status, evidence grade, test outcome, and claim status are separate fields.
- `pcc_evidence.csv`: eight property-level PCC records, including the scope of the provisioning examination and the distinction between a report specification and an actual device export.
- `adjacent_boundaries.csv`: 27 registered paths with parent/target IDs, trigger, data or authority crossing, source, and composition status.
- `verify_sources.py`: refetches sources and compares response hashes. It saves no response bodies.
- `review_comparison.csv`: 20 initial paired labels from one author and one same-organization non-author colleague. It preserves the original difference at AICore D5.
- `review_notes.csv`: five feedback categories with workbook cell locators and author summaries.
- `summarize_reviews.py`: recomputes descriptive state and numeric-label counts from `review_comparison.csv`; it does not estimate reliability or reproduce the assessment process.
- `protocol_versions.csv`: the two public method stages, `INITIAL PILOT RUBRIC` and `FINAL RUBRIC`.
- `rubric_versions.csv`: initial and final wording for all 20 anchors.
- `rubric_clarifications.csv`: one added D5-L1 criterion and four guidance clarifications derived from the paired records.
- `reviewer_guide.pdf`: content-equivalent reference copy of the four-page initial pilot guide, labeled `FB-PILOT-v1` for publication packaging.
- `review_case_traces.csv`: three paired cases (AICore D5, FM D4, Recall D3) with verbatim original rationale/unmet-condition fields. Source differences and subsequent author interpretation are separately labeled.
- `review_source_access.csv`: 54 item-source links covering all 20 items, with source IDs and original locators.

## Evidence and Scope

E1 denotes an assertion; E2 a design or inspectable configuration; E3 a collected execution record or completed evaluation; E4 a claim-matched validation package. Public availability and independence are separate properties. A schema is not a collected log, and availability of the VRE is not a completed experiment.

Dimension labels follow anchor conditions, not a conversion or average of probe rates. List each anchor's required conditions, preserve conjunctions and alternatives, and assign the highest label fully supported and not contradicted by scoped evidence. For implementation audits, an unresolved required probe without a pre-registered substitute leaves the dimension `UD`; level 3 requires claim-matched E4 coverage. Zero requires affirmative absence/contradiction evidence. For BDR, an unrun probe is `UNTESTED` and unresolved observability after execution is `INCONCLUSIVE`; insufficient control-anchor evidence is recorded separately as D4 `UD`. This protocol clarification changes no documentary scores or initial responses.

`ADJ` and `N/A` ordinarily classify paths. Once all material parent and adjacent subclaims for a dimension are evaluated, the workflow label is the lowest supported applicable anchor across them. A material `UD` propagates `UD`; a material `ADJ` blocks composition until its target is evaluated; an evidenced-absent path drops out without satisfying unrelated obligations.

The PCC D5 cell cites both E2 and E3. Its E3 evidence is limited to the provisioning examination for May 1, 2025 through April 30, 2026 and does not cover AI-service integrity or the paper's proposed privacy probes.

Foundation Models and Recall retain the July 24, 2026 cutoff. The AICore boundary includes the Gemini Nano page revision dated September 8, 2026; that source was reviewed again on September 24. PCC records incorporate a targeted review through September 14. The stable ID `APPLE-PCC-2025` is retained for continuity, not as a software-version assertion. The agent record is property-level analysis, not an additional scored product.

`access_date` is the date on which the source was reviewed for inclusion in the analysis.

The final control matrix uses `FB-FINAL-v1`. The formative comparison led to an added capability-specific accountability criterion and clarified internal duties at adjacent paths, notice audience and timing, retention alternatives, and coarse access control versus semantic inference restraint. Levels 1--3 accumulate positive requirements within the applicable branch. Missing higher-level controls are not prerequisites for a lower label: provenance, for example, is optional at D4-L1. These are evidence-qualified control levels, not effectiveness estimates. The adjacency register's `retained_parent_obligation` identifies selected internal duties. No entire D4 dimension is ADJ in the final matrix. PCC one-shot D4 uses only the routing/attestation subclaims of PCC-E04, not agent tool-argument/recipient evidence.

A numeric control score has an empty scope-status field. Otherwise the score is empty and the status is `UD`, `ADJ`, or `N/A`. An unevaluated adjacent target need not appear among the five analyzed boundaries; it remains explicitly unresolved. `BLOCKS` means that documentary description alone does not discharge that dependency.

## Assessment Comparison

One author (A) and one non-author colleague in the same organization (C) completed separate coding records for four capabilities across five dimensions using an author-prepared pilot guide and candidate source list. Record C was received on September 24, 2026 (PDT). The comparison is used to identify instruction ambiguities rather than to estimate statistical inter-rater reliability.

The pilot guide listed 23 candidate source entries and excluded the full PCC SOC 3 report, which is subject to a use-and-distribution notice, while retaining Apple's public SOC 3 overview. The final platform corpus contains 24 entries, adding the report for the separate PCC provisioning analysis. The paired records are therefore not a frozen-corpus replication of the final matrix, and the added report is not counted as evidence of rater agreement.

Run `python3 summarize_reviews.py`. There are 19/20 matching scope states and 14/14 equal numeric labels among jointly SCORED items. Five pairs are jointly UD; one is C=UD/A=1. Scope states are never converted to zero, and the script validates missing or invalid states.

The original workbooks and private profiles are not distributed. Selected rationale and unmet-condition fields are reproduced in the three case traces. The paired labels are preserved separately from the final platform matrix.

Evidence and path IDs are local to each assessment record. Structured cross-references use `A-` or `C-` prefixes, such as `A-EV009` and `C-EV009`, so the two records cannot be confused. Verbatim excerpts retain their original IDs; their column identifies the record. Candidate-source IDs (`S01`, etc.) share the supplied source-list namespace.

The sole differing label is AICore D5: A cites S09's responsible-AI paragraph, whereas C cites S08/S10 for app responsibility, update rollback, and support. The final rubric requires a named owner's capability-specific undertaking, so the reconciled matrix records UD. That reconciliation is not a third independent rating or a validation against C. The final matrix contains eleven 1s, three 2s, and six UDs.

C provided written permission for research/publication use of de-identified ratings, feedback and the selected verbatim fields. The signed permission was received on September 24, 2026 (PDT). The written permission record is not part of this supplement. The manuscript was approved for external publication by the authors' employer.

## Verification

Run `python3 verify_sources.py`. Results are CSV on stdout. The verifier uses `retrieval_url` when supplied and otherwise uses `official_url`. New Apple security-guide entries use official DocC JSON content; hashing their HTML application shell would not track the underlying article. Historical hashes remain unchanged, including the older security-guide landing page, whose HTML hash is not a content-integrity guarantee.

Hashed entries return `match`, `mismatch`, or `fetch_error`. Unhashed entries return `observed_no_expected_hash`, `unfetchable_no_expected_hash`, or `fetch_error_no_expected_hash`. HTTP errors are checked before hash comparison. The verifier exits nonzero for a mismatch or any fetch failure, including an unreachable unhashed source; a successfully retrieved unhashed source remains an observation rather than a hash match. Byte agreement does not validate a claim or a score; a mismatch requires checking whether the relevant source content changed.

The original fixed request headers are retained so historical hashes remain comparable. New hashes were recorded only after two identical preparation responses. Vendor documents and the independent report are linked, not redistributed. No private user data or model files are included.
