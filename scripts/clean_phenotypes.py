"""
clean_phenotypes.py
Project P1 - Phenotype Explorer
Milena Campos - Nellore GWAS project

Usage:
    python clean_phenotypes.py
"""

import pandas as pd


def clean_phenotypes(filepath, limits, output_path):
    """
    Load, validate, and clean a Nellore phenotype file.

    Args:
        filepath: path to raw CSV file
        limits: dict of {trait: (min, max)} biological limits
        output_path: where to save the clean CSV

    Returns:
        df_clean: cleaned DataFrame
    """
    print("=" * 50)
    print("PHENOTYPE CLEANING PIPELINE")
    print("=" * 50)

    # Step 1: Load
    print("\n[1/4] Loading data...")
    df = pd.read_csv(filepath, low_memory=False)
    print(f"      Loaded: {len(df):,} rows x {df.shape[1]} columns")

    # Step 2: Filter pedigree-only rows
    print("\n[2/4] Filtering pedigree-only rows...")
    df_animals = df[df['anoNt'] > 0].copy()
    removed = len(df) - len(df_animals)
    print(f"      Kept: {len(df_animals):,} animals ({removed:,} pedigree rows removed)")

    # Step 3: Remove outliers
    print("\n[3/4] Removing biological outliers...")
    df_clean = df_animals.copy()
    total_outliers = 0
    for trait, (low, high) in limits.items():
        before = df_clean[trait].notna().sum()
        df_clean.loc[
            (df_clean[trait] < low) | (df_clean[trait] > high), trait
        ] = None
        after = df_clean[trait].notna().sum()
        n = before - after
        total_outliers += n
        print(f"      {trait}: {n:,} outliers removed (limits: {low}–{high} kg)")
    print(f"      Total outliers removed: {total_outliers:,}")

    # Step 4: Summary report
    print("\n[4/4] Summary report...")
    for trait in limits.keys():
        n = df_clean[trait].notna().sum()
        mean = df_clean[trait].mean()
        sd = df_clean[trait].std()
        print(f"      {trait}: n={n:,}  mean={mean:.1f}  sd={sd:.1f}")

    # Save
    df_clean.to_csv(output_path, index=False)
    print(f"\nClean file saved to: {output_path}")
    print("=" * 50)

    return df_clean


# ── Run when executed directly ──────────────────
if __name__ == "__main__":

    LIMITS = {
        'peson': (5, 60),
        'pesod': (60, 400),
        'pesos': (100, 600),
    }

    INPUT  = '/Users/milenacampos/Documents/projeto doc/DEFEITOS NELORE/pedigree+fenotipo.csv'
    OUTPUT = '/Users/milenacampos/Documents/projeto doc/DEFEITOS NELORE/pedigree+fenotipo_clean.csv'

    df_clean = clean_phenotypes(INPUT, LIMITS, OUTPUT)