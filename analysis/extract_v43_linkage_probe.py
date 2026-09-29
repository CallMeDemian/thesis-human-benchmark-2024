from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
THESIS = ROOT.parent / "thesis"
OUT = ROOT / "analysis_artifacts" / "v43_linkage_probe"
OUT.mkdir(parents=True, exist_ok=True)

STRICT = ROOT / "outputs" / "strict_archival_benchmark.csv"

FILES = {
    "c3e_actions": THESIS / "frozen/original_release/rl/C3E_E2_7SEED_BALANCED_DFEBAFA6/C3E_firm_actions.parquet",
    "c3e_actions_payoffs": THESIS / "frozen/original_release/rl/stage6/C3E_E2_7SEED_BALANCED_DFEBAFA6/C3E_firm_actions_payoffs.parquet",
    "candidate_payoff_surface": THESIS / "frozen/original_release/rl/stage6/C3E_E2_7SEED_BALANCED_DFEBAFA6/firm_action_oracle_payoffs.parquet",
    "baseline_stage8": THESIS / "frozen/original_release/evaluation/llm_final_evaluation_20260913/stage8/BASELINE_STRICT_ITT/llm_stage8_multi_oracle_scores_itt.parquet",
    "high_stage8": THESIS / "frozen/original_release/evaluation/llm_final_evaluation_20260913/stage8/HIGH_STRICT_ITT/llm_stage8_multi_oracle_scores_itt.parquet",
}


def frame_meta(df: pd.DataFrame) -> dict:
    return {
        "rows": int(len(df)),
        "columns": list(df.columns),
        "dtypes": {c: str(df[c].dtype) for c in df.columns},
        "firm_key_unique": int(df["firm_key"].astype(str).nunique()) if "firm_key" in df.columns else None,
        "row_id_unique": int(df["row_id"].nunique()) if "row_id" in df.columns else None,
    }


def save_csv(df: pd.DataFrame, name: str) -> None:
    df.to_csv(OUT / name, index=False, encoding="utf-8-sig")


def main() -> None:
    strict = pd.read_csv(STRICT, dtype={"stock_code": str, "firm_key": str})
    strict_keys = set(strict["firm_key"].astype(str))
    inventory = {
        "strict_firms": strict[["row_no", "firm_key", "stock_code", "firm_name", "mapped_action"]].to_dict("records"),
        "files": {},
    }

    frames: dict[str, pd.DataFrame] = {}
    for name, path in FILES.items():
        if not path.exists():
            raise FileNotFoundError(path)
        df = pd.read_parquet(path)
        frames[name] = df
        inventory["files"][name] = {"path": str(path.relative_to(THESIS)), **frame_meta(df)}

    baseline = frames["baseline_stage8"]
    if "firm_key" not in baseline.columns or "row_id" not in baseline.columns:
        raise RuntimeError("Stage8 baseline lacks firm_key/row_id crosswalk")
    crosswalk = baseline[["row_id", "firm_key"]].drop_duplicates()
    if crosswalk["row_id"].duplicated().any() or crosswalk["firm_key"].duplicated().any():
        raise RuntimeError("Stage8 row_id/firm_key crosswalk is not one-to-one")
    save_csv(crosswalk[crosswalk["firm_key"].astype(str).isin(strict_keys)], "strict9_row_crosswalk.csv")

    for name, df in frames.items():
        work = df.copy()
        if "firm_key" not in work.columns and "row_id" in work.columns:
            work = work.merge(crosswalk, on="row_id", how="left", validate="many_to_one")
        if "firm_key" in work.columns:
            sub = work[work["firm_key"].astype(str).isin(strict_keys)].copy()
        else:
            sub = work.iloc[0:0].copy()
        inventory["files"][name]["strict9_rows"] = int(len(sub))
        save_csv(sub, f"{name}_strict9_raw.csv")

    # Clean direct-comparison slice: candidate9 / IC-b / B1 / main Run1 / ITT.
    slices = []
    for regime, name in [("BASELINE", "baseline_stage8"), ("HIGH", "high_stage8")]:
        df = frames[name].copy()
        mask = df["firm_key"].astype(str).isin(strict_keys)
        for col, value in [
            ("mode", "candidate9"),
            ("budget", "B1"),
            ("info", "IC-b"),
            ("phase", "MAIN"),
        ]:
            if col in df.columns:
                mask &= df[col].astype(str).eq(value)
        if "replicate" in df.columns:
            mask &= pd.to_numeric(df["replicate"], errors="coerce").eq(1)
        if "policy" in df.columns:
            mask &= df["policy"].astype(str).isin(["C4", "C6-E"])
        sub = df.loc[mask].copy()
        sub.insert(0, "source_generation_regime", regime)
        slices.append(sub)
    direct = pd.concat(slices, ignore_index=True, sort=False)
    save_csv(direct, "llm_candidate9_primary_strict9.csv")
    inventory["direct_candidate9_primary_rows"] = int(len(direct))

    # Human strict labels alongside the row crosswalk. Actual model agreement is
    # computed in the next step after this schema probe is inspected.
    human = strict[["row_no", "firm_key", "stock_code", "firm_name", "source_type", "mapped_action"]].copy()
    human = human.rename(columns={"mapped_action": "human_action"})
    save_csv(human, "human_strict9.csv")

    (OUT / "schema_inventory.json").write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
