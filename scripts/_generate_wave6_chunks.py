"""One-off generator for Wave 6 — 20 chunks (2026-04-29).

Reads the structured spec list below, emits one markdown chunk-spec per
record into chunks/openonco/<chunk-id>-2026-04-29-0030.md.

After running, validate with:
    python -m tasktorrent.lint_chunk_spec --all chunks/openonco/

Each chunk is grounded in a real cell of the KB coverage matrix
(`cancer-autoresearch/docs/kb-coverage-matrix.md`) and has a realistic
manifest of entity IDs / file paths drawn from current master content.

Run once. The generator is not part of the maintained tooling — it's
checked in only as the audit trail of how Wave 6 was produced.
"""

from __future__ import annotations

import textwrap
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CHUNKS_DIR = REPO_ROOT / "chunks" / "openonco"
TIMESTAMP = "2026-04-29-0030"


@dataclass
class Chunk:
    chunk_id: str
    one_liner: str           # short scope description
    severity: str            # low | medium | high
    min_tier: str            # new | established | trusted
    queue: str               # A | B | C
    topic_labels: list[str]
    mission: str             # full mission text incl. matrix ref
    drops: float             # estimated Drops (1 Drop = ~100k tokens)
    required_skill: str
    allowed_sources: str
    disallowed_sources: str
    manifest: str            # markdown body of manifest section
    output_format: str
    economic: dict           # compute_profile / break_even_test / verification_method / output_type
    acceptance: list[str]    # bullet list (machine-checkable)
    rejection: list[str]
    claim_method: str
    verifier_threshold: str | None = None
    expected_violations: int | None = None

    @property
    def stamped_id(self) -> str:
        return f"{self.chunk_id}-{TIMESTAMP}"


def _econ_yaml(c: Chunk) -> str:
    e = c.economic
    lines = [
        "```yaml",
        f"compute_profile: {e['compute_profile']}",
        f"verification_method: {e['verification_method']}",
        f"break_even_test: {e['break_even_test']}",
        f"output_type: {e['output_type']}",
    ]
    if c.expected_violations is not None:
        lines.append(f"expected_violations: {c.expected_violations}")
    if "verification_cost" in e:
        vc = e["verification_cost"]
        lines.append("verification_cost:")
        for k, v in vc.items():
            lines.append(f"  {k}: {v}")
    if "rationale" in e:
        lines.append(f"break_even_rationale: >")
        for line in textwrap.wrap(e["rationale"], width=72):
            lines.append(f"  {line}")
    lines.append("```")
    return "\n".join(lines)


def render(c: Chunk) -> str:
    sections: list[str] = []
    sections.append(f"# Chunk: {c.stamped_id}\n")
    sections.append(f"> {c.one_liner}\n")
    sections.append(f"## Status\n\n`queued`\n")
    sections.append(f"## Severity\n\n`{c.severity}`\n")
    sections.append(f"## Min Contributor Tier\n\n`{c.min_tier}`\n")
    sections.append(f"## Queue\n\n`{c.queue}`\n")
    sections.append(f"## Topic Labels\n\n" + ", ".join(f"`{t}`" for t in c.topic_labels) + "\n")
    sections.append(f"## Mission\n\n{c.mission}\n")
    sections.append(f"## Economic Profile\n\n{_econ_yaml(c)}\n")
    sections.append(f"## Drop Estimate\n\n~{c.drops} Drops (~{int(c.drops * 100)}k tokens).\n")
    sections.append(f"## Required Skill\n\n`{c.required_skill}`\n")
    sections.append(f"## Allowed Sources\n\n{c.allowed_sources}\n")
    sections.append(f"## Disallowed Sources\n\n{c.disallowed_sources}\n")
    sections.append(f"## Manifest\n\n{c.manifest}\n")
    sections.append(f"## Output Format\n\n{c.output_format}\n")
    sections.append(f"## Acceptance Criteria\n\n" + "\n".join(f"- [ ] {a}" for a in c.acceptance) + "\n")
    sections.append(f"## Rejection Criteria\n\n" + "\n".join(f"- {r}" for r in c.rejection) + "\n")
    if c.verifier_threshold:
        sections.append(f"## Verifier Threshold\n\n{c.verifier_threshold}\n")
    sections.append(f"## Claim Method\n\n`{c.claim_method}`\n")
    return "\n".join(sections)


# ============================================================
# Wave 6 — 20 chunks
# ============================================================

CHUNKS: list[Chunk] = [

    # =============== Queue A — Coverage-fill ===============

    Chunk(
        chunk_id="bma-fill-rare-tcell-lymphomas",
        one_liner="Add >=3 BMA records each for 7 rare T-cell lymphomas currently at 0-2 BMA coverage.",
        severity="high", min_tier="trusted", queue="A",
        topic_labels=["bma-drafting", "rare-disease", "lymphoma", "civic-evidence"],
        mission=(
            "Draft new biomarker_actionability records for 7 rare T-cell lymphomas "
            "currently at 0-2 BMA coverage in the OpenOnco KB. Each disease gets >=3 "
            "actionable biomarkers with CIViC-backed `evidence_sources` blocks where "
            "available, otherwise NCCN/ESMO citations.\n\n"
            "**KB coverage:** Advances `kb-coverage-matrix.md > Coverage gaps > "
            "Diseases with zero BMA` from 14 to 7 (and `Diseases with thin BMA` "
            "from 25 to ~22) by filling rare T-cell lymphoma rows."
        ),
        drops=3, required_skill="biomarker-extraction",
        allowed_sources="CIViC, NCCN T-cell Lymphoma 2025, ESMO PTCL 2024, PubMed RCTs.",
        disallowed_sources="`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA` (always banned per CHARTER §2).",
        manifest=(
            "Diseases (7), each gets >=3 BMA records. Suggested biomarkers per disease:\n\n"
            "- `DIS-ATLL` — HTLV-1 status, IRF4 (mogamulizumab), CD25 (denileukin diftitox), CCR4\n"
            "- `DIS-EATL` — celiac association, JAK1/STAT3 mutations, type II EBV-negative subtype\n"
            "- `DIS-HSTCL` — STAT3/STAT5B mutations, isochromosome 7q, SETD2 mutations\n"
            "- `DIS-MF-SEZARY` — CD30 expression (brentuximab vedotin), KIR3DL2 (mogamulizumab), TOX\n"
            "- `DIS-NK-T-NASAL` — EBV titer, PD-L1 expression, DDX3X mutations\n"
            "- `DIS-PTCL-NOS` — CD30, GATA3 vs TBX21 subtype, ALK status (rule out ALCL)\n"
            "- `DIS-T-PLL` — TCL1A overexpression, ATM mutation/del, JAK3 mutations\n\n"
            "Final manifest will list >=21 BMA stable IDs of form `BMA-<GENE>-<VARIANT>-<DISEASE>`."
        ),
        output_format=(
            "- `contributions/bma-fill-rare-tcell-lymphomas-{ts}/bma_<...>.yaml` — one per BMA\n"
            "- `contributions/bma-fill-rare-tcell-lymphomas-{ts}/task_manifest.txt`\n"
            "- `contributions/bma-fill-rare-tcell-lymphomas-{ts}/_contribution_meta.yaml`"
        ).format(ts=TIMESTAMP),
        economic={
            "compute_profile": "mixed",
            "verification_method": "full-expert",
            "break_even_test": "PASS",
            "output_type": "entity-sidecar",
            "verification_cost": {"maintainer_hours": 6, "expert_hours": 8, "expert_specialty": "hematopathology"},
            "rationale": (
                "Manual rare-disease BMA drafting takes ~30 min per record × 21 = 10.5h. "
                "Contributor at ~12k tokens/BMA = 250k tokens. Sample-verify 30% (~6 BMAs) "
                "= 6h maintainer + 8h expert. Net win ~5h after expert review."
            ),
        },
        acceptance=[
            "Every sidecar has `_contribution.ai_tool` and `_contribution.ai_model` set.",
            "PR branch matches `tasktorrent/bma-fill-rare-tcell-lymphomas-{ts}`.".format(ts=TIMESTAMP),
            "task_manifest.txt lists >=21 BMA stable IDs.",
            "Every BMA has `disease_id`, `biomarker_id`, `escat_tier`, `evidence_sources`.",
            "`ukrainian_review_status: pending_clinical_signoff` on every record.",
            "No banned source references.",
        ],
        rejection=[
            "Citation grounding fails verifier (any layer).",
            "Disease IDs outside the 7 listed.",
            "ESCAT tier inflated above evidence supports.",
            "Patient-specific output.",
        ],
        claim_method="formal-issue",
    ),

    Chunk(
        chunk_id="bma-fill-pmbcl",
        one_liner="Add >=3 BMA records for Primary Mediastinal B-Cell Lymphoma (currently 0).",
        severity="medium", min_tier="trusted", queue="A",
        topic_labels=["bma-drafting", "rare-disease", "lymphoma", "civic-evidence"],
        mission=(
            "PMBCL is currently at 0 BMA records despite being a distinct B-cell "
            "lymphoma with biomarker-actionable biology (PD-L1, MAL, CIITA, JAK-STAT). "
            "Draft >=3 BMA records.\n\n"
            "**KB coverage:** Advances `kb-coverage-matrix.md > Coverage gaps > "
            "Diseases with zero BMA` for `DIS-PMBCL`."
        ),
        drops=1, required_skill="biomarker-extraction",
        allowed_sources="CIViC, NCCN B-cell Lymphoma 2025, ESMO Hodgkin/PMBCL 2024, PubMed RCTs.",
        disallowed_sources="`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.",
        manifest=(
            "Suggested BMAs (final manifest decided by contributor):\n\n"
            "- `BMA-PD-L1-AMPLIFICATION-PMBCL` (chr 9p24.1 amp; pembrolizumab)\n"
            "- `BMA-MAL-PMBCL` (signature gene)\n"
            "- `BMA-CIITA-FUSION-PMBCL` (PD-L1/PD-L2 dysregulation)\n"
            "- `BMA-JAK2-PMBCL` (chr 9p24.1 co-amp)"
        ),
        output_format=(
            "- `contributions/bma-fill-pmbcl-{ts}/bma_*.yaml`\n"
            "- `contributions/bma-fill-pmbcl-{ts}/task_manifest.txt`\n"
            "- `contributions/bma-fill-pmbcl-{ts}/_contribution_meta.yaml`"
        ).format(ts=TIMESTAMP),
        economic={
            "compute_profile": "mixed",
            "verification_method": "full-expert",
            "break_even_test": "PASS",
            "output_type": "entity-sidecar",
            "verification_cost": {"maintainer_hours": 1, "expert_hours": 2, "expert_specialty": "hematopathology"},
            "rationale": "~3-4 BMAs at ~10k tokens each. Smaller scope than rare-tcell chunk; PMBCL biology is well-characterized.",
        },
        acceptance=[
            "Every sidecar has ai_tool + ai_model.",
            "Every BMA references PMBCL-specific evidence (not generic DLBCL).",
            "9p24.1 amp BMA cites both pembrolizumab + nivolumab evidence.",
            "No banned source references.",
        ],
        rejection=["Citation grounding fails verifier.", "Generic DLBCL evidence used as PMBCL evidence."],
        claim_method="formal-issue",
    ),

    Chunk(
        chunk_id="bma-fill-glioma-low-grade",
        one_liner="Add 5 BMA records for low-grade glioma (currently 0): IDH1, IDH2, MGMT, 1p19q, BRAF V600E.",
        severity="medium", min_tier="trusted", queue="A",
        topic_labels=["bma-drafting", "neuro-oncology", "civic-evidence"],
        mission=(
            "Low-grade glioma (IDH-mutant, WHO grade 2) is currently at 0 BMA records "
            "despite its biomarker-driven archetype. Draft 5 BMAs covering the canonical "
            "molecular subtypes that drive treatment selection.\n\n"
            "**KB coverage:** Advances `kb-coverage-matrix.md > Coverage gaps > "
            "Diseases with zero BMA` for `DIS-GLIOMA-LOW-GRADE`."
        ),
        drops=1, required_skill="biomarker-extraction",
        allowed_sources="CIViC, NCCN CNS 2025, ESMO Glioma 2023, INDIGO trial readout.",
        disallowed_sources="`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.",
        manifest=(
            "5 BMAs:\n\n"
            "- `BMA-IDH1-R132H-GLIOMA-LOW-GRADE` (vorasidenib — INDIGO trial)\n"
            "- `BMA-IDH2-R172-GLIOMA-LOW-GRADE` (vorasidenib)\n"
            "- `BMA-MGMT-METHYLATION-GLIOMA-LOW-GRADE` (TMZ benefit prediction)\n"
            "- `BMA-1P19Q-CODELETION-GLIOMA-LOW-GRADE` (oligodendroglioma; PCV vs TMZ)\n"
            "- `BMA-BRAF-V600E-GLIOMA-LOW-GRADE` (dabrafenib + trametinib)"
        ),
        output_format=(
            "- `contributions/bma-fill-glioma-low-grade-{ts}/bma_*.yaml`\n"
            "- `contributions/bma-fill-glioma-low-grade-{ts}/task_manifest.txt`\n"
            "- `contributions/bma-fill-glioma-low-grade-{ts}/_contribution_meta.yaml`"
        ).format(ts=TIMESTAMP),
        economic={
            "compute_profile": "mixed",
            "verification_method": "full-expert",
            "break_even_test": "PASS",
            "output_type": "entity-sidecar",
            "verification_cost": {"maintainer_hours": 1, "expert_hours": 2, "expert_specialty": "neuro-oncology"},
            "rationale": "5 well-characterized BMAs; vorasidenib is a 2024 first-in-class IDH inhibitor (INDIGO).",
        },
        acceptance=[
            "Every sidecar has ai_tool + ai_model.",
            "IDH1/IDH2 BMAs cite INDIGO trial (Mellinghoff 2023, NEJM).",
            "ESCAT tier IA for IDH (FDA-approved vorasidenib).",
            "No banned sources.",
        ],
        rejection=["Generic glioma evidence used.", "Vorasidenib indication off-label-extended."],
        claim_method="formal-issue",
    ),

    Chunk(
        chunk_id="bma-fill-hnscc",
        one_liner="Add 4-5 BMA records for HNSCC (currently 0): HPV, TP53, EGFR amp, PD-L1 CPS.",
        severity="high", min_tier="trusted", queue="A",
        topic_labels=["bma-drafting", "head-and-neck", "civic-evidence"],
        mission=(
            "Head and neck squamous cell carcinoma is currently at 0 BMA records despite "
            "being one of the higher-incidence cancers and having a distinct HPV+ vs HPV- "
            "biology with treatment-selection consequences.\n\n"
            "**KB coverage:** Advances `kb-coverage-matrix.md > Coverage gaps > "
            "Diseases with zero BMA` for `DIS-HNSCC`."
        ),
        drops=1, required_skill="biomarker-extraction",
        allowed_sources="CIViC, NCCN H&N 2025, ESMO H&N 2020, KEYNOTE-048.",
        disallowed_sources="`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.",
        manifest=(
            "4-5 BMAs:\n\n"
            "- `BMA-HPV-POSITIVE-HNSCC` (better prognosis; de-escalation candidate)\n"
            "- `BMA-HPV-NEGATIVE-HNSCC` (standard chemoradiation; smoking-driven)\n"
            "- `BMA-TP53-HNSCC` (commonly mutated in HPV-)\n"
            "- `BMA-EGFR-AMPLIFICATION-HNSCC` (cetuximab benefit)\n"
            "- `BMA-PD-L1-CPS-HNSCC` (CPS>=1 → pembrolizumab; KEYNOTE-048)"
        ),
        output_format=(
            "- `contributions/bma-fill-hnscc-{ts}/bma_*.yaml`\n"
            "- `contributions/bma-fill-hnscc-{ts}/task_manifest.txt`\n"
            "- `contributions/bma-fill-hnscc-{ts}/_contribution_meta.yaml`"
        ).format(ts=TIMESTAMP),
        economic={
            "compute_profile": "mixed",
            "verification_method": "full-expert",
            "break_even_test": "PASS",
            "output_type": "entity-sidecar",
            "verification_cost": {"maintainer_hours": 1, "expert_hours": 2, "expert_specialty": "head-and-neck-oncology"},
            "rationale": "5 BMAs at ~10k tokens each. HPV status is the dominant stratifier.",
        },
        acceptance=[
            "ai_tool + ai_model in every sidecar.",
            "HPV+/HPV- BMAs explicitly distinguish prognostic + treatment implications.",
            "PD-L1 CPS BMA cites KEYNOTE-048 first-line evidence.",
            "No banned sources.",
        ],
        rejection=["Citation verifier fails.", "Conflating HPV+/HPV- prognosis with treatment intensity recommendations."],
        claim_method="formal-issue",
    ),

    Chunk(
        chunk_id="bma-fill-soft-tissue-rare",
        one_liner="Add BMA records for IMT, MPNST, Chondrosarcoma (currently 0 each).",
        severity="medium", min_tier="trusted", queue="A",
        topic_labels=["bma-drafting", "sarcoma", "rare-disease", "civic-evidence"],
        mission=(
            "Three rare soft-tissue/bone sarcomas are at 0 BMA: inflammatory "
            "myofibroblastic tumor (ALK fusion-driven), MPNST (NF1 / EED-SUZ12 / "
            "CDKN2A loss), and chondrosarcoma (IDH1/2). Draft >=2 BMAs per disease.\n\n"
            "**KB coverage:** Advances `kb-coverage-matrix.md > Coverage gaps > "
            "Diseases with zero BMA` for 3 sarcomas."
        ),
        drops=1.5, required_skill="biomarker-extraction",
        allowed_sources="CIViC, NCCN Sarcoma 2025, ESMO Sarcoma 2021, PubMed.",
        disallowed_sources="`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.",
        manifest=(
            "6 BMAs (2 per disease minimum):\n\n"
            "- `BMA-ALK-FUSION-IMT` (crizotinib / lorlatinib)\n"
            "- `BMA-ROS1-FUSION-IMT` (entrectinib; rare subset)\n"
            "- `BMA-NF1-LOSS-MPNST` (no targeted therapy; chemo + RT)\n"
            "- `BMA-SUZ12-EED-LOSS-MPNST` (PRC2 loss; experimental)\n"
            "- `BMA-IDH1-CHONDROSARCOMA` (ivosidenib clinical trial evidence)\n"
            "- `BMA-IDH2-CHONDROSARCOMA` (enasidenib clinical trial evidence)"
        ),
        output_format=(
            "- `contributions/bma-fill-soft-tissue-rare-{ts}/bma_*.yaml`\n"
            "- `contributions/bma-fill-soft-tissue-rare-{ts}/task_manifest.txt`\n"
            "- `contributions/bma-fill-soft-tissue-rare-{ts}/_contribution_meta.yaml`"
        ).format(ts=TIMESTAMP),
        economic={
            "compute_profile": "mixed",
            "verification_method": "full-expert",
            "break_even_test": "PASS",
            "output_type": "entity-sidecar",
            "verification_cost": {"maintainer_hours": 2, "expert_hours": 3, "expert_specialty": "sarcoma"},
            "rationale": "6 BMAs across 3 rare diseases. Sarcoma expert needed for tier accuracy.",
        },
        acceptance=[
            "ai_tool + ai_model.",
            "ALK fusion BMA correctly distinguishes IMT from anaplastic-LCL evidence.",
            "MPNST BMAs honestly report no FDA-approved targeted therapy (no off-label).",
            "Chondrosarcoma IDH BMAs cite trial data (not solid evidence yet).",
        ],
        rejection=["Off-label recommendations.", "Tier inflation."],
        claim_method="formal-issue",
    ),

    Chunk(
        chunk_id="bma-fill-apl",
        one_liner="Add 3-4 BMA records for APL (currently 0 — molecular emergency).",
        severity="high", min_tier="trusted", queue="A",
        topic_labels=["bma-drafting", "leukemia", "emergency", "civic-evidence"],
        mission=(
            "Acute Promyelocytic Leukemia is `archetype: molecularly_defined_emergency` "
            "yet currently has 0 BMA records. PML-RARA fusion is the diagnostic + "
            "therapeutic biomarker (ATRA + arsenic). Draft >=3 BMAs.\n\n"
            "**KB coverage:** Advances `kb-coverage-matrix.md > Coverage gaps > "
            "Diseases with zero BMA` for `DIS-APL` (highest priority — emergency archetype)."
        ),
        drops=1, required_skill="biomarker-extraction",
        allowed_sources="CIViC, NCCN AML/APL 2025, ESMO AML 2024, APL0406 / Lo-Coco trial.",
        disallowed_sources="`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.",
        manifest=(
            "3-4 BMAs:\n\n"
            "- `BMA-PML-RARA-T-15-17-APL` (ATRA + arsenic — first-line)\n"
            "- `BMA-PML-RARA-VARIANTS-APL` (PLZF-RARA, NPM1-RARA, etc.)\n"
            "- `BMA-FLT3-ITD-APL` (high-risk subset; midostaurin off-label discussion)\n"
            "- `BMA-FLT3-TKD-APL` (Sanz risk score input)"
        ),
        output_format=(
            "- `contributions/bma-fill-apl-{ts}/bma_*.yaml`\n"
            "- `contributions/bma-fill-apl-{ts}/task_manifest.txt`\n"
            "- `contributions/bma-fill-apl-{ts}/_contribution_meta.yaml`"
        ).format(ts=TIMESTAMP),
        economic={
            "compute_profile": "mixed",
            "verification_method": "full-expert",
            "break_even_test": "PASS",
            "output_type": "entity-sidecar",
            "verification_cost": {"maintainer_hours": 1, "expert_hours": 2, "expert_specialty": "hematology"},
            "rationale": "APL is well-characterized; ATRA+arsenic is curative for non-high-risk. Small chunk, clinical urgency.",
        },
        acceptance=[
            "ai_tool + ai_model.",
            "PML-RARA BMA cites APL0406 (Lo-Coco 2013, NEJM).",
            "ESCAT tier IA for PML-RARA (curative response).",
            "Variant fusions distinguished as diagnostic-only (no separate therapy).",
        ],
        rejection=["Recommending ATRA without confirming PML-RARA.", "Tier inflation on FLT3 BMAs."],
        claim_method="formal-issue",
    ),

    Chunk(
        chunk_id="regimen-outcome-fill",
        one_liner="Backfill `expected_outcomes` (median OS, ORR, CR rate) for 50 regimens currently lacking.",
        severity="medium", min_tier="established", queue="A",
        topic_labels=["regimen-data", "outcomes", "rct-fetch"],
        mission=(
            "Of 244 regimens in the KB, an unknown number lack structured "
            "`expected_outcomes` blocks (median OS, ORR, CR, PFS). This chunk "
            "samples 50 high-traffic regimens and backfills outcomes data from "
            "their pivotal trial citations.\n\n"
            "**KB coverage:** Advances `kb-coverage-matrix.md > Top-level KPIs > "
            "Regimens` quality dimension (regimens with outcomes data — currently "
            "unmeasured; this chunk + audit chunk #15 establish the baseline)."
        ),
        drops=2, required_skill="drug-evidence-mapping",
        allowed_sources="PubMed (pivotal trial readouts), ClinicalTrials.gov, FDA labels.",
        disallowed_sources="`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.",
        manifest=(
            "50 regimen IDs to be selected by maintainer prior to chunk activation, "
            "weighted toward:\n\n"
            "- High-traffic regimens (BMA / IND back-references)\n"
            "- Regimens currently lacking `expected_outcomes`\n"
            "- Regimens with single pivotal RCT (clearer extraction)\n\n"
            "Final manifest committed as `task_manifest.txt` listing 50 stable "
            "REG-* IDs."
        ),
        output_format=(
            "- `contributions/regimen-outcome-fill-{ts}/reg_<id>.yaml` — one per regimen (upsert)\n"
            "- `contributions/regimen-outcome-fill-{ts}/task_manifest.txt`\n"
            "- `contributions/regimen-outcome-fill-{ts}/_contribution_meta.yaml`"
        ).format(ts=TIMESTAMP),
        economic={
            "compute_profile": "mixed",
            "verification_method": "sample",
            "break_even_test": "PASS",
            "output_type": "entity-sidecar",
            "verification_cost": {"maintainer_hours": 4, "expert_hours": 0, "expert_specialty": ""},
            "rationale": "Manual outcomes extraction = ~10 min/regimen × 50 = 8.3h. Contributor at ~10k tokens/regimen = 500k tokens. Sample-verify 20% = 4h.",
        },
        acceptance=[
            "ai_tool + ai_model.",
            "Each upsert preserves existing fields, adds `expected_outcomes` block.",
            "`expected_outcomes` cites a specific pivotal trial in `notes_for_reviewer`.",
            "OS/PFS values match cited source's reported numbers.",
        ],
        rejection=["Made-up OS values without citation.", "Cross-trial number mixing."],
        claim_method="formal-issue",
    ),

    Chunk(
        chunk_id="source-recency-refresh-50",
        one_liner="Refresh `current_as_of` and metadata for 50 stale Source entities (out of 240 stale-by-date).",
        severity="low", min_tier="established", queue="A",
        topic_labels=["source-ingest", "metadata-classification", "recency"],
        mission=(
            "240 of 269 sources have `current_as_of < 365d ago`. This chunk samples "
            "50 high-citation-count sources (NCCN, ESMO, FDA labels) and refreshes "
            "their `current_as_of` after re-checking their original URL, license, "
            "and version.\n\n"
            "**KB coverage:** Advances `kb-coverage-matrix.md > Quality scores > "
            "Sources current_as_of <365d` from 10% upward."
        ),
        drops=1, required_skill="citation-verification",
        allowed_sources="Original source landing pages (NCCN, ESMO, FDA, journal sites).",
        disallowed_sources="`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.",
        manifest=(
            "50 SRC-* stable IDs selected by maintainer pre-activation, weighted toward:\n\n"
            "- High citation count (referenced by many BMA/IND/RF)\n"
            "- Guidelines (NCCN, ESMO) with annual revisions\n"
            "- FDA labels (drugs with updated indications)\n\n"
            "Final manifest committed as `task_manifest.txt`."
        ),
        output_format=(
            "- `contributions/source-recency-refresh-50-{ts}/src_<id>.yaml` — one per source (upsert)\n"
            "- `contributions/source-recency-refresh-50-{ts}/task_manifest.txt`\n"
            "- `contributions/source-recency-refresh-50-{ts}/_contribution_meta.yaml`"
        ).format(ts=TIMESTAMP),
        economic={
            "compute_profile": "mechanical",
            "verification_method": "computational",
            "break_even_test": "PASS",
            "output_type": "entity-sidecar",
            "verification_cost": {"maintainer_hours": 1, "expert_hours": 0, "expert_specialty": ""},
            "rationale": "Mostly mechanical URL HEAD + version-string update. Computational re-verify = URL-resolves check.",
        },
        acceptance=[
            "ai_tool + ai_model.",
            "Each upsert preserves existing fields except `current_as_of`, `version`, `url` (if redirected).",
            "URL HEAD returns 200/301/302 (verified before commit).",
            "License classification unchanged (or change explicitly noted).",
        ],
        rejection=["License downgrade without justification.", "Adding new fields beyond recency."],
        verifier_threshold=">=85% claims pass Anthropic Citations API grounding (default).",
        claim_method="trusted-agent-wip-branch-first",
    ),

    # =============== Queue B — Audit-remediate ===============

    Chunk(
        chunk_id="escat-tier-audit-full",
        one_liner="Full ESCAT audit of all 399 BMAs (B2 subset projected ~76% mismatch on 50 sample).",
        severity="high", min_tier="trusted", queue="B",
        topic_labels=["audit", "civic-evidence", "claim-bearing"],
        mission=(
            "B2 subset audit (PR #28) showed 38/50 BMAs with ESCAT mismatch (16 "
            "overclaim + 22 underclaim). This chunk audits ALL 399 BMAs against "
            "ESCAT v1 (Mateo et al. 2018). Output: per-BMA proposed tier "
            "correction with rationale.\n\n"
            "**KB coverage:** Advances `kb-coverage-matrix.md > Quality scores > "
            "BMA with ESCAT tier` from nominal 100% to verified-correct ~70%, "
            "exposing the actual ground-truth tier accuracy."
        ),
        drops=8, required_skill="biomarker-extraction",
        allowed_sources="ESMO ESCAT v1 (Mateo 2018), CIViC, NCCN/ESMO disease-specific.",
        disallowed_sources="`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.",
        manifest=(
            "All 399 BMAs in `knowledge_base/hosted/content/biomarker_actionability/`. "
            "Manifest is the full file list (run `ls` against that dir at activation time)."
        ),
        output_format=(
            "- `contributions/escat-tier-audit-full-{ts}/audit-report.yaml` — single report\n"
            "- `contributions/escat-tier-audit-full-{ts}/task_manifest.txt`\n"
            "- `contributions/escat-tier-audit-full-{ts}/_contribution_meta.yaml`"
        ).format(ts=TIMESTAMP),
        economic={
            "compute_profile": "llm-essential",
            "verification_method": "sample",
            "break_even_test": "PASS",
            "output_type": "report-only",
            "verification_cost": {"maintainer_hours": 8, "expert_hours": 16, "expert_specialty": "molecular-oncology"},
            "rationale": "B2 projected ~140 overclaim + 175 underclaim across 399. Manual full audit = 100h. Contributor ~830k tokens. Expert sample-verify 10% (40 BMAs) = 16h.",
        },
        acceptance=[
            "ai_tool + ai_model.",
            "audit-report.yaml lists every BMA-* with current_tier, proposed_tier, rationale.",
            "Per-BMA rationale cites the ESCAT criterion that drives the verdict.",
            "Severity classification (critical / moderate / minor) on every row.",
        ],
        rejection=["Tier change without rationale.", "Generic 'should be IIA' without ESCAT criterion."],
        claim_method="trusted-agent-wip-branch-first",
    ),

    Chunk(
        chunk_id="citation-verify-v2-remediation",
        one_liner="Apply citation-verify-v2's 793 actionable findings: replace_source / new-source / source-stub.",
        severity="medium", min_tier="established", queue="B",
        topic_labels=["citation-verify", "remediation"],
        mission=(
            "citation-verify-v2 (PR #23) produced 793 actionable rows. Apply each: "
            "for `replace_source` rows, swap the cited SRC-* (verifier title-substring "
            "check from L-13 must pass); for `source_stub_needed`, file a SRC-* stub; "
            "for ambiguous, mark `maintainer_review_needed`.\n\n"
            "**KB coverage:** Advances `kb-coverage-matrix.md > Quality scores > "
            "Sources current_as_of <365d` indirectly (newly stubbed sources have "
            "fresh metadata)."
        ),
        drops=4, required_skill="citation-verification",
        allowed_sources="PubMed, journal landing pages, existing SRC-* registry.",
        disallowed_sources="`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.",
        manifest=(
            "793 rows from `cancer-autoresearch/contributions/citation-semantic-verify-v2/"
            "citation-semantic-verify-report.yaml` (status: actionable). "
            "Final manifest = 793 row IDs as `task_manifest.txt`."
        ),
        output_format=(
            "- `contributions/citation-verify-v2-remediation-{ts}/<entity-id>.yaml` — entity upserts\n"
            "- `contributions/citation-verify-v2-remediation-{ts}/source_stub_*.yaml` — new SRC stubs\n"
            "- `contributions/citation-verify-v2-remediation-{ts}/task_manifest.txt`\n"
            "- `contributions/citation-verify-v2-remediation-{ts}/_contribution_meta.yaml`"
        ).format(ts=TIMESTAMP),
        economic={
            "compute_profile": "llm-essential",
            "verification_method": "computational",
            "break_even_test": "PASS",
            "output_type": "mixed",
            "verification_cost": {"maintainer_hours": 4, "expert_hours": 0, "expert_specialty": ""},
            "rationale": "793 rows × ~5k tokens = 4M tokens. But L-13 title-verify is automated (computational re-verify is the gate, not human review). Maintainer 4h to run reverify_citation_replace_source + spot-check.",
        },
        acceptance=[
            "ai_tool + ai_model.",
            "Every replace_source row passes `reverify_citation_replace_source.py` title-substring check.",
            "Every new SRC stub has full license block + 4 permission booleans.",
            "Hosting mode `referenced` for all stubs.",
            "No `SRC-CROSS-FLT3-AML`-style false-positive stubs.",
        ],
        rejection=["L-13 title-substring fail (any row).", "Banned source stubbed."],
        verifier_threshold=">=95% replace_source rows pass title-substring check (stricter than default 85% because lexical-match risk per L-13).",
        claim_method="trusted-agent-wip-branch-first",
    ),

    Chunk(
        chunk_id="rec-wording-critical-remediation",
        one_liner="Fix 229 critical rec-wording findings (claim-bearing fields with treatment-recommendation phrasing).",
        severity="high", min_tier="trusted", queue="B",
        topic_labels=["audit", "rec-wording", "claim-bearing", "safety"],
        mission=(
            "rec-wording-audit-claim-bearing (PR #17) flagged 229 critical findings "
            "where field text reads as treatment recommendation rather than evidence "
            "summary. CHARTER §8.3 forbids LLM-driven recommendations. Fix wording "
            "to evidence-statement form while preserving clinical substance.\n\n"
            "**KB coverage:** Advances `kb-coverage-matrix.md > Quality scores > "
            "BMA UA-signed-off` indirectly — fixed wording becomes signoff-eligible."
        ),
        drops=3, required_skill="biomarker-extraction",
        allowed_sources="Original cited sources (re-read for evidence-statement form).",
        disallowed_sources="`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.",
        manifest=(
            "229 entity-field pairs from `cancer-autoresearch/contributions/"
            "rec-wording-audit-claim-bearing/audit-report.yaml` "
            "(severity: critical). Final manifest = 229 entity IDs in `task_manifest.txt`."
        ),
        output_format=(
            "- `contributions/rec-wording-critical-remediation-{ts}/<entity-id>.yaml` — upserts (field-level)\n"
            "- `contributions/rec-wording-critical-remediation-{ts}/task_manifest.txt`\n"
            "- `contributions/rec-wording-critical-remediation-{ts}/_contribution_meta.yaml`"
        ).format(ts=TIMESTAMP),
        economic={
            "compute_profile": "llm-essential",
            "verification_method": "full-expert",
            "break_even_test": "PASS",
            "output_type": "entity-sidecar",
            "verification_cost": {"maintainer_hours": 8, "expert_hours": 16, "expert_specialty": "clinical-co-lead"},
            "rationale": "229 critical wording fixes. Each requires expert read because clinical substance must survive. ~5k tokens per fix.",
        },
        acceptance=[
            "ai_tool + ai_model.",
            "Each upsert touches ONLY the flagged field (no scope creep).",
            "Reworded text passes the rec-wording linter (no recommendation phrasing).",
            "Clinical substance preserved (sample expert review).",
            "`ukrainian_review_status: pending_clinical_signoff` set after fix.",
        ],
        rejection=["Clinical content silently dropped during reword.", "Treatment recommendation in fix output."],
        claim_method="trusted-agent-wip-branch-first",
    ),

    Chunk(
        chunk_id="ua-translation-critical-remediation",
        one_liner="Fix 200 critical UA-translation findings (mistranslations + missing UA copy on critical fields).",
        severity="medium", min_tier="established", queue="B",
        topic_labels=["audit", "ua-translation", "remediation"],
        mission=(
            "ua-translation-review-batch (PR #21 family) produced 1858 findings; 200 "
            "are critical (mistranslation or missing UA copy on critical fields). Fix "
            "the 200 critical first.\n\n"
            "**KB coverage:** Advances `kb-coverage-matrix.md > Quality scores > "
            "BMA UA-signed-off` toward 100%."
        ),
        drops=2, required_skill="biomarker-extraction",
        allowed_sources="МОЗ України (clinical terminology), original sources.",
        disallowed_sources="`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.",
        manifest=(
            "200 entity-field pairs from `cancer-autoresearch/contributions/"
            "ua-translation-review-batch/audit-report.yaml` "
            "(severity: critical). Final manifest = 200 entity IDs in `task_manifest.txt`."
        ),
        output_format=(
            "- `contributions/ua-translation-critical-remediation-{ts}/<entity-id>.yaml` — upserts\n"
            "- `contributions/ua-translation-critical-remediation-{ts}/task_manifest.txt`\n"
            "- `contributions/ua-translation-critical-remediation-{ts}/_contribution_meta.yaml`"
        ).format(ts=TIMESTAMP),
        economic={
            "compute_profile": "llm-essential",
            "verification_method": "sample",
            "break_even_test": "PASS",
            "output_type": "entity-sidecar",
            "verification_cost": {"maintainer_hours": 4, "expert_hours": 8, "expert_specialty": "ukrainian-clinical-language"},
            "rationale": "200 critical UA fixes. ~3k tokens each. Sample-verify 30% by UA-fluent clinical reviewer.",
        },
        acceptance=[
            "ai_tool + ai_model.",
            "UA copy preserves clinical terminology consistent with МОЗ.",
            "No machine-translation artifacts (e.g. half-Ukrainian/half-English sentences).",
            "Each upsert touches ONLY the flagged field.",
        ],
        rejection=["Machine-translation literal output.", "Untranslated medical English left in UA field."],
        claim_method="formal-issue",
    ),

    Chunk(
        chunk_id="indication-line-of-therapy-audit-full",
        one_liner="Full audit of 302 indications: cited evidence vs claim line-of-therapy match.",
        severity="high", min_tier="trusted", queue="B",
        topic_labels=["audit", "indication", "rct-fetch"],
        mission=(
            "B3 subset (PR #28) showed regex-only methodology insufficient — 29/30 "
            "ambiguous_source. This chunk runs the full audit on 302 IND with "
            "PubMed full-text fetch for cited Source.\n\n"
            "**KB coverage:** Advances `kb-coverage-matrix.md > Quality scores > "
            "Indications with NCCN category` to verified-correct (current 100% nominal "
            "but unverified)."
        ),
        drops=4, required_skill="citation-verification",
        allowed_sources="PubMed full-text + abstract, ClinicalTrials.gov, NCCN guidelines.",
        disallowed_sources="`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.",
        manifest=(
            "All 302 INDs in `knowledge_base/hosted/content/indications/`. "
            "Manifest = full file list at activation."
        ),
        output_format=(
            "- `contributions/indication-line-of-therapy-audit-full-{ts}/audit-report.yaml`\n"
            "- `contributions/indication-line-of-therapy-audit-full-{ts}/task_manifest.txt`\n"
            "- `contributions/indication-line-of-therapy-audit-full-{ts}/_contribution_meta.yaml`"
        ).format(ts=TIMESTAMP),
        economic={
            "compute_profile": "mixed",
            "verification_method": "sample",
            "break_even_test": "PASS",
            "output_type": "report-only",
            "verification_cost": {"maintainer_hours": 6, "expert_hours": 8, "expert_specialty": "oncology"},
            "rationale": "302 INDs × ~12k tokens (fetch + parse + assess) = 3.6M tokens. Web fetch budget required (PubMed). Sample-verify 10% = 8h expert.",
        },
        acceptance=[
            "ai_tool + ai_model.",
            "Per-IND row in audit-report.yaml with: claim line-of-therapy, cited source title/PMID, verdict (match / partial / mismatch / unfetchable).",
            "Severity classification per row.",
        ],
        rejection=["Verdict without fetched-source quote.", "Web fetch claims with no PMID."],
        verifier_threshold=">=85% claims pass Anthropic Citations API grounding (default).",
        claim_method="trusted-agent-wip-branch-first",
    ),

    Chunk(
        chunk_id="bma-civic-eid-recheck",
        one_liner="Re-validate every CIViC EID in 399 BMA evidence_sources against current snapshot.",
        severity="low", min_tier="established", queue="B",
        topic_labels=["audit", "civic-evidence", "computational"],
        mission=(
            "CIViC monthly snapshot refresh (commit `0b53a5c`) means EIDs from "
            "older snapshots may have been deprecated, merged, or had direction "
            "changed. This chunk re-validates every EID in every BMA's "
            "evidence_sources against the latest snapshot.\n\n"
            "**KB coverage:** Advances `kb-coverage-matrix.md > Quality scores > "
            "BMA with CIViC evidence_sources` quality dimension (verified-current EIDs)."
        ),
        drops=2, required_skill="biomarker-extraction",
        allowed_sources="CIViC monthly snapshot under `knowledge_base/hosted/civic/`.",
        disallowed_sources="`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.",
        manifest=(
            "All 399 BMAs in `knowledge_base/hosted/content/biomarker_actionability/`. "
            "Manifest = full file list."
        ),
        output_format=(
            "- `contributions/bma-civic-eid-recheck-{ts}/audit-report.yaml`\n"
            "- `contributions/bma-civic-eid-recheck-{ts}/task_manifest.txt`\n"
            "- `contributions/bma-civic-eid-recheck-{ts}/_contribution_meta.yaml`"
        ).format(ts=TIMESTAMP),
        economic={
            "compute_profile": "mechanical",
            "verification_method": "computational",
            "break_even_test": "PASS",
            "output_type": "report-only",
            "verification_cost": {"maintainer_hours": 1, "expert_hours": 0, "expert_specialty": ""},
            "rationale": "Pure mechanical: walk every BMA, look up each EID in snapshot. Re-verify by re-running the script.",
        },
        acceptance=[
            "ai_tool + ai_model.",
            "Per-BMA row: total_eids, current_eids, deprecated_eids, direction_changed_eids.",
            "Output deterministic — re-running yields identical report.",
        ],
        rejection=["Non-deterministic output.", "Skipped BMAs without explanation."],
        claim_method="trusted-agent-wip-branch-first",
    ),

    Chunk(
        chunk_id="regimen-toxicity-coverage-audit",
        one_liner="Audit which of 244 regimens have CTCAE v5 toxicity grading; surface gaps.",
        severity="medium", min_tier="established", queue="B",
        topic_labels=["audit", "regimen-data", "toxicity"],
        mission=(
            "CTCAE v5 toxicity profiles are needed for safety-side rendering, but "
            "no current measurement of how many regimens have them. This chunk "
            "audits all 244 regimens for presence + completeness of `key_toxicities` "
            "block with CTCAE v5 grading.\n\n"
            "**KB coverage:** Advances `kb-coverage-matrix.md > Top-level KPIs > "
            "Regimens` quality (toxicity coverage; currently unmeasured per "
            "kb-coverage-strategy.md §\"What we don't yet measure\")."
        ),
        drops=2, required_skill="drug-evidence-mapping",
        allowed_sources="FDA labels, CTCAE v5 reference, pivotal trial publications.",
        disallowed_sources="`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.",
        manifest=(
            "All 244 regimens in `knowledge_base/hosted/content/regimens/`. "
            "Manifest = full file list."
        ),
        output_format=(
            "- `contributions/regimen-toxicity-coverage-audit-{ts}/audit-report.yaml`\n"
            "- `contributions/regimen-toxicity-coverage-audit-{ts}/task_manifest.txt`\n"
            "- `contributions/regimen-toxicity-coverage-audit-{ts}/_contribution_meta.yaml`"
        ).format(ts=TIMESTAMP),
        economic={
            "compute_profile": "mixed",
            "verification_method": "sample",
            "break_even_test": "PASS",
            "output_type": "report-only",
            "verification_cost": {"maintainer_hours": 2, "expert_hours": 0, "expert_specialty": ""},
            "rationale": "Audit-only chunk. ~244 regimens × ~5k tokens = 1.2M. Sample-verify 10% (24).",
        },
        acceptance=[
            "ai_tool + ai_model.",
            "Per-regimen row: has_key_toxicities, has_ctcae_grades, missing_grades, completeness_score.",
            "Aggregate stats at top of report (% complete, % missing).",
        ],
        rejection=["Per-row verdict without inspecting actual yaml fields."],
        claim_method="trusted-agent-wip-branch-first",
    ),

    Chunk(
        chunk_id="trial-source-ambiguous-resolution",
        one_liner="Resolve 22 ambiguous trial names from B1 false-positive filter (deferred by Codex in PR #29).",
        severity="medium", min_tier="established", queue="B",
        topic_labels=["source-ingest", "metadata-classification", "audit"],
        mission=(
            "PR #29 ingested 25 confirmed-real trials and skipped 22 ambiguous ones "
            "(CROSS, PARADIGM, RUBY, CODEBREAK, AIDA, PROPEL, MAGNITUDE, THOR, etc.) "
            "for maintainer review. This chunk resolves each: real RCT (ingest as SRC stub) "
            "vs false-positive (mark in extracted-trials list).\n\n"
            "**KB coverage:** Advances `kb-coverage-matrix.md > Top-level KPIs > Sources` — "
            "completes the trial-source-ingest workstream."
        ),
        drops=1, required_skill="citation-verification",
        allowed_sources="PubMed E-utilities, ClinicalTrials.gov, journal landing pages.",
        disallowed_sources="`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.",
        manifest=(
            "22 trial-name candidates from PR #29's `Deferred / not stubbed in this slice`:\n\n"
            "`CROSS, PARADIGM, RUBY, CODEBREAK, AIDA, PROPEL, MAGNITUDE, THOR, "
            "ARASENS, PRODIGE, BFORE, FIRE-3, ICON7, STARTRK, STUPP, AGILE, STIL, "
            "CRYSTAL, MONUMENTAL-1, BRIGHT, IMPOWER150, SHINE`."
        ),
        output_format=(
            "- `contributions/trial-source-ambiguous-resolution-{ts}/source_stub_*.yaml` — for confirmed real\n"
            "- `contributions/trial-source-ambiguous-resolution-{ts}/false_positive_resolution_report.yaml` — for confirmed-false\n"
            "- `contributions/trial-source-ambiguous-resolution-{ts}/task_manifest.txt`\n"
            "- `contributions/trial-source-ambiguous-resolution-{ts}/_contribution_meta.yaml`"
        ).format(ts=TIMESTAMP),
        economic={
            "compute_profile": "mixed",
            "verification_method": "sample",
            "break_even_test": "PASS",
            "output_type": "mixed",
            "verification_cost": {"maintainer_hours": 1, "expert_hours": 0, "expert_specialty": ""},
            "rationale": "22 trials × ~7k tokens (PubMed + license read) = ~150k. Sample-verify 30%.",
        },
        acceptance=[
            "ai_tool + ai_model.",
            "Each of the 22 trial names is resolved: stub OR false-positive entry.",
            "Stubs follow PR #29 schema (license + 4 permission booleans + hosting_mode: referenced).",
            "L-13 title-substring check passes for stubs.",
        ],
        rejection=["L-13 title-substring fail.", "Trial unresolved (no verdict)."],
        verifier_threshold=">=85% claims pass Anthropic Citations API grounding (default).",
        claim_method="formal-issue",
    ),

    # =============== Queue C — Schema-evolution ===============

    Chunk(
        chunk_id="add-cost-fields-meta-schema",
        one_liner="Add optional `cost_estimate` (chunk-spec) + `cost_actual` (_contribution_meta.yaml) fields per protocol-v0.4.",
        severity="low", min_tier="trusted", queue="C",
        topic_labels=["schema-evolution", "observability", "tooling"],
        mission=(
            "protocol-v0.4-design.md `Owner-resolved decisions` §2 commits to optional "
            "cost_estimate (chunk-spec) and cost_actual (`_contribution_meta.yaml`) "
            "fields. Add Pydantic schema + validator support + lint_chunk_spec "
            "soft-warning when missing on chunks ≥2 Drops.\n\n"
            "**KB coverage:** Advances `kb-coverage-matrix.md > Top-level KPIs` "
            "instrumentation (tracks token economy of contributor work)."
        ),
        drops=1, required_skill="biomarker-extraction",
        allowed_sources="protocol-v0.4-design.md owner-resolved decisions section.",
        disallowed_sources="`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.",
        manifest=(
            "Schema files to extend:\n\n"
            "- `task_torrent/tasktorrent/lint_chunk_spec.py` — accept `cost_estimate` block\n"
            "- `cancer-autoresearch/scripts/tasktorrent/validate_contributions.py` — accept `cost_actual` in meta\n"
            "- `cancer-autoresearch/scripts/tasktorrent/_contribution_meta.example.yaml` (if exists) — example\n\n"
            "No KB content changes. Test additions only."
        ),
        output_format=(
            "- `contributions/add-cost-fields-meta-schema-{ts}/<patch>.diff` — git format-patches against both repos\n"
            "- `contributions/add-cost-fields-meta-schema-{ts}/task_manifest.txt`\n"
            "- `contributions/add-cost-fields-meta-schema-{ts}/_contribution_meta.yaml`"
        ).format(ts=TIMESTAMP),
        economic={
            "compute_profile": "mechanical",
            "verification_method": "computational",
            "break_even_test": "PASS",
            "output_type": "report-only",
            "verification_cost": {"maintainer_hours": 1, "expert_hours": 0, "expert_specialty": ""},
            "rationale": "Pure schema add. Tests cover the new fields. Fast.",
        },
        acceptance=[
            "ai_tool + ai_model.",
            "Both validators accept new fields without warning.",
            "lint_chunk_spec emits warning (not error) on chunks >=2 Drops without cost_estimate.",
            "Tests for new schema branches pass.",
        ],
        rejection=["Field made required (must stay optional per owner decision).", "Tests skipped."],
        claim_method="trusted-agent-wip-branch-first",
    ),

    Chunk(
        chunk_id="add-tasktorrent-version-observability",
        one_liner="Backfill `tasktorrent_version` (commit-hash style) into 12+ existing _contribution_meta.yaml files.",
        severity="low", min_tier="new", queue="C",
        topic_labels=["schema-evolution", "observability"],
        mission=(
            "L-21 / Proposal #27 introduces `_contribution.tasktorrent_version` as "
            "OPTIONAL observability field. This chunk backfills it on all existing "
            "`_contribution_meta.yaml` files in OpenOnco's `contributions/` tree, "
            "using each file's commit date as the version stamp.\n\n"
            "**KB coverage:** Advances `kb-coverage-matrix.md > Top-level KPIs` "
            "instrumentation — post-hoc drift trace per L-21 across the contributions tree."
        ),
        drops=0.5, required_skill="biomarker-extraction",
        allowed_sources="git log of each contributions/<chunk-id>/ dir.",
        disallowed_sources="`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.",
        manifest=(
            "All `_contribution_meta.yaml` files under `cancer-autoresearch/contributions/`. "
            "Pre-activation: `find contributions -name '_contribution_meta.yaml'`. "
            "Currently ~12 chunk dirs."
        ),
        output_format=(
            "- `contributions/add-tasktorrent-version-observability-{ts}/<chunk-id>/_contribution_meta.yaml` — upsert each\n"
            "- `contributions/add-tasktorrent-version-observability-{ts}/task_manifest.txt`\n"
            "- `contributions/add-tasktorrent-version-observability-{ts}/_contribution_meta.yaml`"
        ).format(ts=TIMESTAMP),
        economic={
            "compute_profile": "mechanical",
            "verification_method": "computational",
            "break_even_test": "PASS",
            "output_type": "entity-sidecar",
            "verification_cost": {"maintainer_hours": 0.5, "expert_hours": 0, "expert_specialty": ""},
            "rationale": "Pure mechanical backfill. <30 min total.",
        },
        acceptance=[
            "ai_tool + ai_model.",
            "Every meta gets `tasktorrent_version: <YYYY-MM-DD-shortsha>` of its dir's first commit.",
            "No other field touched in any meta.",
        ],
        rejection=["Field added to non-meta files.", "Existing fields modified."],
        claim_method="formal-issue",
    ),

    Chunk(
        chunk_id="add-line-of-therapy-evidence-source",
        one_liner="Add `line_of_therapy_evidence_source` field to all 302 IND, citing the specific RCT that established the line.",
        severity="medium", min_tier="trusted", queue="C",
        topic_labels=["schema-evolution", "indication", "rct-fetch"],
        mission=(
            "Indications currently set `evidence_level: high|moderate|low` and "
            "`nccn_category: '2A'` but don't tie the line-of-therapy to a specific "
            "RCT. Add `line_of_therapy_evidence_source: SRC-*` per IND.\n\n"
            "**KB coverage:** Advances `kb-coverage-matrix.md > Quality scores > "
            "Indications with NCCN category` quality dimension (citation-traceable LoT)."
        ),
        drops=3, required_skill="drug-evidence-mapping",
        allowed_sources="PubMed pivotal trial readouts, NCCN guidelines, existing SRC-* registry.",
        disallowed_sources="`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.",
        manifest=(
            "All 302 INDs. Pre-activation `ls knowledge_base/hosted/content/indications/`. "
            "Final manifest = 302 IND-* IDs in `task_manifest.txt`."
        ),
        output_format=(
            "- `contributions/add-line-of-therapy-evidence-source-{ts}/ind_<id>.yaml` — upsert each\n"
            "- `contributions/add-line-of-therapy-evidence-source-{ts}/source_stub_*.yaml` — new SRC stubs as needed\n"
            "- `contributions/add-line-of-therapy-evidence-source-{ts}/task_manifest.txt`\n"
            "- `contributions/add-line-of-therapy-evidence-source-{ts}/_contribution_meta.yaml`"
        ).format(ts=TIMESTAMP),
        economic={
            "compute_profile": "mixed",
            "verification_method": "full-expert",
            "break_even_test": "PASS",
            "output_type": "entity-sidecar",
            "verification_cost": {"maintainer_hours": 6, "expert_hours": 12, "expert_specialty": "oncology"},
            "rationale": "302 INDs × ~10k tokens = 3M. Schema upsert is mechanical; selecting the right RCT per LoT requires clinical judgment + sometimes new SRC stubs.",
        },
        acceptance=[
            "ai_tool + ai_model.",
            "Every IND has `line_of_therapy_evidence_source` pointing at SRC-* (existing or new stub).",
            "L-13 title-substring check passes for any new SRC stubs.",
            "Per-IND `notes_for_reviewer` cites specific trial section.",
        ],
        rejection=["Generic guideline citation when a specific RCT is the actual source.", "L-13 fail."],
        verifier_threshold=">=85% claims pass Anthropic Citations API grounding (default).",
        claim_method="trusted-agent-wip-branch-first",
    ),

    Chunk(
        chunk_id="bma-ua-signoff-workflow-schema",
        one_liner="Add `signed_off_by` + `signed_off_date` fields to BMA UA-translation review schema; backfill 0 for now.",
        severity="medium", min_tier="trusted", queue="C",
        topic_labels=["schema-evolution", "ua-translation", "governance"],
        mission=(
            "BMA records have `ukrainian_review_status: pending_clinical_signoff` "
            "but no record of who signed off when status flips. Add `signed_off_by` "
            "(GitHub login or Co-Lead initials) and `signed_off_date` (ISO date). "
            "Backfill empty values on all 399 BMAs (no signoffs have happened yet).\n\n"
            "**KB coverage:** Advances `kb-coverage-matrix.md > Quality scores > "
            "BMA UA-signed-off` instrumentation (currently 0%; Co-Lead signoff "
            "queue is the bottleneck)."
        ),
        drops=1, required_skill="biomarker-extraction",
        allowed_sources="CHARTER §6.1 (two-reviewer signoff requirement).",
        disallowed_sources="`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.",
        manifest=(
            "All 399 BMAs in `knowledge_base/hosted/content/biomarker_actionability/`. "
            "Plus schema in `knowledge_base/schemas/biomarker_actionability.py`."
        ),
        output_format=(
            "- `contributions/bma-ua-signoff-workflow-schema-{ts}/bma_<id>.yaml` — upsert each (add fields, leave empty)\n"
            "- `contributions/bma-ua-signoff-workflow-schema-{ts}/schema_patch.diff` — Pydantic schema extension\n"
            "- `contributions/bma-ua-signoff-workflow-schema-{ts}/task_manifest.txt`\n"
            "- `contributions/bma-ua-signoff-workflow-schema-{ts}/_contribution_meta.yaml`"
        ).format(ts=TIMESTAMP),
        economic={
            "compute_profile": "mechanical",
            "verification_method": "computational",
            "break_even_test": "PASS",
            "output_type": "entity-sidecar",
            "verification_cost": {"maintainer_hours": 1, "expert_hours": 0, "expert_specialty": ""},
            "rationale": "Pure schema add + null backfill. Pydantic accepts. ~1 hour.",
        },
        acceptance=[
            "ai_tool + ai_model.",
            "Every BMA has `signed_off_by: null` and `signed_off_date: null` after upsert.",
            "Pydantic schema extension validates existing 399 BMAs without error.",
            "No clinical content modified.",
        ],
        rejection=["Other fields modified.", "Schema field made required (must be Optional)."],
        claim_method="trusted-agent-wip-branch-first",
    ),
]


def main() -> int:
    if len(CHUNKS) != 20:
        print(f"ERROR: expected 20 chunks, got {len(CHUNKS)}")
        return 1

    seen_ids = set()
    for c in CHUNKS:
        if c.chunk_id in seen_ids:
            print(f"ERROR: duplicate chunk_id {c.chunk_id}")
            return 1
        seen_ids.add(c.chunk_id)

    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    for c in CHUNKS:
        path = CHUNKS_DIR / f"{c.stamped_id}.md"
        path.write_text(render(c), encoding="utf-8")
        written += 1
        print(f"  wrote {path.name}")

    print(f"\n{written} chunk-spec files written to {CHUNKS_DIR.relative_to(REPO_ROOT)}/.")
    print("Validate with: python -m tasktorrent.lint_chunk_spec --all chunks/openonco/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
