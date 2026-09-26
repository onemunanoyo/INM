# INM Candidate Review Decisions — Batch 01

Date: 2026-09-27

This file records review decisions separately from the candidate source files.

## Work metadata

Interpretation of the review discussion:

- `cand_work_002` — **ACCEPT**
- `cand_work_004` — **ACCEPT**
- `cand_work_008` — **ACCEPT**
- `cand_work_001` — **REJECT_FOR_NOW** (too archival/difficult for the intended core set)
- `cand_work_003` — **REJECT_FOR_NOW** (too archival/difficult)
- `cand_work_005` — **REJECT_FOR_NOW** (too archival/difficult)
- `cand_work_006` — **REJECT_FOR_NOW** (too archival/difficult)
- `cand_work_007` — **REJECT_FOR_NOW** (too archival/difficult)

These rejected items may be retained as future `expert` / `archival` candidates rather than deleted permanently.

## Chapter titles

The statement `cand_workは全採用` is interpreted in context as accepting the chapter-title block:

- `cand_work_009` — **ACCEPT**
- `cand_work_010` — **ACCEPT**
- `cand_work_011` — **ACCEPT**
- `cand_work_012` — **ACCEPT**

## Chapter / cast mapping

All `cand_cast_*` items require multi-source checking before final acceptance.

Current result:

- `cand_cast_001` — **PROVISIONAL_ACCEPT**
- `cand_cast_002` — **PROVISIONAL_ACCEPT**
- `cand_cast_003` — **PROVISIONAL_ACCEPT**
- `cand_cast_004` — **PROVISIONAL_ACCEPT**
- `cand_cast_005` — **PROVISIONAL_ACCEPT**
- `cand_cast_006` — **PROVISIONAL_ACCEPT**

Reason: the mappings are consistent across the retrieved yjsnpi material and at least one additional independent community reference. However, the Pixiv Encyclopedia and Nico Nico Pedia members of the preferred first-source set are still pending direct item-level verification, so these are not yet promoted to gold.

Observed mappings:

- Chapter 1: `TDN / DB / HTN / TNOK`
- Chapter 2: `NSOK / DRVS / 白いの`
- Chapter 3: `GO / マジメ君`
- Chapter 4: `野獣先輩 / 遠野`

## Character roles

Original items `cand_role_001–007` are superseded by revised candidates in:

`data/candidates/batch01_roles_revised.jsonl`

Authoring policy:

- Basic role questions should primarily test **role type / narrative position**, such as `先輩`, `後輩`, `暴力団員`, `大学生`, or `スカウトマン`.
- Formal or in-work role names such as `三浦`, `谷岡`, `佐藤`, `小林`, `桜井`, and `鴻野` are stored as separate metadata and may be used for `hard` / expert-style questions.
- Do not combine a role type and a role name into one answer label unless the distinction itself is what the item tests.
- Each question should test one attribute at a time.

Revised candidates:

- `cand_role_001_r1`: TDN → `先輩` — **REVISED_CANDIDATE**
- `cand_role_002_r1`: TNOK → `暴力団員` — **REVISED_CANDIDATE**
- `cand_role_003_r1`: NSOK → `大学生` — **REVISED_CANDIDATE**
- `cand_role_004_r1`: DRVS → `スカウトマン` — **REVISED_CANDIDATE**
- `cand_role_005_r1`: GO → role name `桜井` — **REVISED_CANDIDATE / HARD**
- `cand_role_006_r1`: マジメ君 → role name `鴻野` — **REVISED_CANDIDATE / HARD**
- `cand_role_007_r1`: 野獣先輩=`先輩`, 遠野=`後輩` — **REVISED_CANDIDATE**

The earlier incorrect description `NSOK = フリーター・佐藤` is retired; the revised candidate uses `大学生` as the role type and `佐藤` as the role name.

## Source policy note

Preferred first-source family remains:

1. 真夏の夜の淫夢Wiki / yjsnpi.nu
2. pixiv百科事典
3. ニコニコ大百科

Additional community references may be used for corroboration, but an item should remain provisional when the preferred source family has not yet been cross-checked at item level.
