import logging
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_data(filepath):
    logging.info(f"Loading file: {filepath}")
    try:
        df = pd.read_csv(filepath, low_memory=False)
        logging.info(f"Loaded {len(df):,} rows x {df.shape[1]} columns")
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error ({type(e).__name__}): {e}")
        return None

def filter_animals(df):
    logging.info("Filtering pedigree-only rows (anoNt == 0)...")
    before = len(df)
    df_filtered = df[df['anoNt'] > 0].copy()
    removed = before - len(df_filtered)
    logging.info(f"Kept {len(df_filtered):,} animals, removed {removed:,} pedigree rows")
    if removed == 0:
        logging.warning("No pedigree rows removed — check if anoNt column is correct")
    return df_filtered

def remove_outliers(df, limits):
    logging.info("Removing biological outliers...")
    total = 0
    for trait, (low, high) in limits.items():
        before = df[trait].notna().sum()
        df.loc[(df[trait] < low) | (df[trait] > high), trait] = None
        removed = before - df[trait].notna().sum()
        total += removed
        logging.info(f"  {trait}: {removed} outliers removed")
    logging.info(f"Total outliers removed: {total}")
    return df

# Run the full pipeline
filepath = "/Users/milenacampos/Documents/projeto doc/DEFEITOS NELORE/pedigree+fenotipo.csv"
limits = {'peson': (5, 60), 'pesod': (60, 400), 'pesos': (100, 600)}

df = load_data(filepath)
if df is not None:
    df = filter_animals(df)
    df = remove_outliers(df, limits)
    logging.info("Pipeline completed successfully!")
else:
    logging.error("Pipeline failed — could not load data")