# ECE2050 repository expansion plan

## Scope and sequence

1. Inspect the existing 43 concept notes, tree, glossary and validation tools; preserve filenames, metadata, explanations and figures.
2. Read all supplied PDF and PPTX documents. Extract text by page/slide and identify duplicate editions. Inspect diagrams and formula-heavy pages visually before using them.
3. Build a source-to-concept coverage matrix here in working material. Course documents are references; formal notes focus on concepts rather than PDF links.
4. Fill Ch1 and Ch5–Ch11 in prerequisite order: combinational analysis → functional blocks → storage elements/timing → registers → FSMs → counters → memories. Add VHDL, FPGA workflow and project design where supported.
5. Refine each existing concept with topic-specific English explanations, an exam-style question and answer, a worked application, and meaningful cross-chapter links.
6. Synchronize the existing knowledge tree and glossary, retaining completed/difficult status meanings. Explicitly distinguish prerequisite, implementation and comparison links; check reverse relationships.
7. Verify examples with exhaustive enumeration or numerical checks as appropriate. Run the repository checker and plugin audit, inspect added diagrams, and review language balance/readability.

## Acceptance criteria

- All supplied documents inspected; duplicates identified without deleting original material.
- No unresolved concept links, missing embeds, ambiguous aliases or isolated formal notes.
- Every topic has definition, assumptions, reasoning, examples, pitfalls and bilingual recall; English is approximately 40% of prose, estimated transparently rather than by counting code or equations.
- One existing knowledge tree and one existing glossary remain the canonical entry points.
- Examples derived from sources are distinguished from original practice; no claim of a complete official solution set.
- Validation evidence and source coverage stay in working material; no source PDF duplication.

## Baseline

- Notes: 43 concepts + 2 hubs.
- Existing coverage: Ch2 (18), Ch3 (11), Ch4 (14).
- Ch1 has no dedicated foundational note; Ch5–Ch11 planned but absent.
- New-note list and source coverage were finalized after document extraction.

## Execution status · 执行结果

- [x] Inspect original structure and preserve all 43 canonical topic filenames.
- [x] Extract 45 archive files (including existing Ch1–4), identify edition/duplicate families, inspect scan-heavy sources and selected figures.
- [x] Create 43 new topic notes: Ch1 2; Ch5 3; Ch6 11; Ch7 5; Ch8 4; Ch9 7; Ch10 3; Ch11 4; HDL 3; Review 1.
- [x] Refine the original 43 concepts with topic-specific English reasoning, worked applications, answered questions and cross-chapter links.
- [x] Extend the existing knowledge tree and glossary; every topic is reachable from both hubs and has an incoming concept link.
- [x] Add three original figures, correct the existing CRC hardware label, and visually verify these assets.
- [x] Check worked equations, state transitions, examples, Markdown boundaries, source integrity and the formal graph.

## Final acceptance evidence

- **86 topic notes + 2 hubs**; 52 SVG figures plus the preserved 14 cropped PNG assets.
- Formal plugin audit: **0 errors, 0 warnings, 0 info**. Repository checker: **PROBLEMS (0)**.
- No unresolved concept links, ambiguous aliases, missing tree/glossary entries, missing embeds or semantic orphans.
- English readable-prose estimate is approximately **41%** (near the requested 40%); estimator excludes frontmatter, code and math, and uses English word count against Chinese characters/2. It is not an exact linguistic token measure.
- **10,770 independent expansion assertions + 535 application/review assertions** passed. Original Ch2 numeric verification and Ch3/4 checks passed. New figure models and layout checks passed.
- 45 archived reference files retain their original SHA256 hashes.
- Complete evidence: `.scratch/qa-20260930/`; source coverage: `.scratch/source-coverage-20260930.md`; concept list: `.scratch/expansion-manifest.json`.
- VHDL examples were reviewed and their Boolean/state behavior checked against independent models; no local HDL compiler/simulator was available, so HDL-tool simulation is **not claimed**.
- The old repository checker retains 39 non-blocking suggestions: 36 concise new-note length reminders, one long original-note reminder and two existing SVG stroke-style heuristics. These do not indicate broken links, missing concepts or invalid figures; content was kept in canonical concept boundaries rather than padded to a line quota.

## Meaningful corrections

CRC degree versus padding, actual four-stage polynomial, undetectable-error limits; parity bit in the supplied example; two's-complement subtraction typo; custom16 versus IEEE binary16; binary32 versus binary64 rounding examples; combinational composition versus arbitrary feedback; fractional base-conversion grouping; Karnaugh-map ON/DC counts and baseline expression. All affected final notes state the applicable model.
