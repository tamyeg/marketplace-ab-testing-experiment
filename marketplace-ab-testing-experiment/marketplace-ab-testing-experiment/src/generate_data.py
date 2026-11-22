"""Generate fully synthetic, reproducible randomized-experiment data."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'experiment_users.csv'
SEED = 20261122
N = 30000


def generate(n=N, seed=SEED):
    rng = np.random.default_rng(seed)
    variant = np.array(['control'] * (n // 2) + ['treatment'] * (n - n // 2))
    rng.shuffle(variant)
    country = rng.choice(['LT', 'PL', 'DE', 'FR'], size=n, p=[.20, .30, .30, .20])
    device = rng.choice(['android', 'ios', 'web'], size=n, p=[.44, .37, .19])
    prior_buyer = rng.binomial(1, .44, size=n)
    country_effect = pd.Series(country).map({'LT': .002, 'PL': -.004, 'DE': .003, 'FR': -.001}).to_numpy()
    baseline = .058 + .045 * prior_buyer + country_effect + np.where(device == 'web', -.008, 0.)
    treatment_effect = np.where(variant == 'treatment', .015, 0.)
    purchase_prob = np.clip(baseline + treatment_effect, 0, 1)
    purchased = rng.binomial(1, purchase_prob)
    # Ancillary metric: listing-click probability (not a causal mediator analysis).
    clicked = rng.binomial(1, np.clip(.31 + .028 * (variant == 'treatment') + .045 * prior_buyer, 0, 1))
    # Revenue per randomized user, with zeros for users with no purchase.
    amount = np.round(rng.lognormal(mean=3.05, sigma=.55, size=n), 2)
    order_value_eur = np.where(purchased == 1, amount, 0.)
    refunded = np.where(purchased == 1, rng.binomial(1, .045, size=n), 0)
    return pd.DataFrame({
        'user_id': np.arange(1, n + 1), 'variant': variant, 'country': country,
        'device': device, 'prior_buyer': prior_buyer.astype(int),
        'clicked_listing': clicked.astype(int), 'purchased_7d': purchased.astype(int),
        'order_value_eur': order_value_eur, 'refunded_7d': refunded.astype(int)
    })


def main():
    DATA.parent.mkdir(parents=True, exist_ok=True)
    df = generate()
    df.to_csv(DATA, index=False)
    print(f'Wrote {len(df):,} simulated experiment users to {DATA}')

if __name__ == '__main__':
    main()
