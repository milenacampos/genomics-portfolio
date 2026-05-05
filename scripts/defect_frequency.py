"""
defect_frequency.py
Project P1 - Nellore defect frequency analysis
Translated from R preprocessing script

Computes frequency of morphological defects across evaluation stages
(weaning, yearling, revision) in Nellore beef cattle.
"""

import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Defect code mapping (text code → numeric)
MAPEAMENTO_COM = {
    "OAP": 1,  "OCA": 2,  "OCH": 3,  "OCU": 4,
    "ODE": 5,  "OAR": 6,  "OHE": 7,  "OLO": 8,
    "OMA": 9,  "OPR": 10, "ORA": 11, "OPE": 12,
    "OPM": 13, "OPC": 14, "OPA": 15, "OPH": 16,
    "OCO": 17, "OGA": 18, "OSF": 19, "OSS": 20,
    "OOU": 21
}

COLUNAS_DEFEITO = [
    'comd', 'coms',
    'comr1', 'comr2', 'comr3',
    'comr4', 'comr5', 'comr6', 'comr7'
]

FILEPATH = '/Users/milenacampos/Documents/projeto doc/DEFEITOS NELORE/pedigree+fenotipo.csv'
OUTPUT   = '/Users/milenacampos/Documents/projeto doc/DEFEITOS NELORE/frequencia_defeitos.csv'


def load_data(filepath):
    """Load phenotype file with error handling."""
    logging.info(f"Loading: {filepath}")
    try:
        df = pd.read_csv(filepath, low_memory=False)
        logging.info(f"Loaded {len(df):,} rows x {df.shape[1]} columns")
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        return None


def compute_frequencies(df, colunas, mapeamento):
    """
    Compute defect frequencies across all evaluation stages.
    Returns a tidy DataFrame with one row per defect per stage.
    """
    num_to_nome = {v: k for k, v in mapeamento.items()}
    rows = []

    for col in colunas:
        n_evaluated = df[col].notna().sum()
        if n_evaluated == 0:
            logging.warning(f"{col}: no data")
            continue
        logging.info(f"{col}: {n_evaluated:,} animals evaluated")
        freq = df[col].value_counts(dropna=True).sort_index()
        for num, count in freq.items():
            nome = num_to_nome.get(int(num), "unknown")
            rows.append({
                'fase':       col,
                'codigo':     int(num),
                'defeito':    nome,
                'frequencia': count,
                'n_avaliados': n_evaluated,
                'proporcao':  round(count / n_evaluated * 100, 2)
            })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = load_data(FILEPATH)
    if df is not None:
        freq_df = compute_frequencies(df, COLUNAS_DEFEITO, MAPEAMENTO_COM)
        freq_df.to_csv(OUTPUT, index=False)
        logging.info(f"Saved frequency table: {len(freq_df)} rows → {OUTPUT}")
        print(freq_df[freq_df['fase'] == 'comd'].to_string(index=False))