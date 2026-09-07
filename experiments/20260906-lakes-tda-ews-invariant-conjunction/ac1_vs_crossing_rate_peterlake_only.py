"""Fairer, sampling-frequency-controlled re-test of the AC1-vs-crossing-rate candidate: restrict
to the 6 peterlake series only (all daily-sampled, unlike obrienlakes' monthly PCA1 scores, which
mechanically have much lower AC1 regardless of underlying process noisiness -- a real confound in
the full 9-series test)."""

from scipy.stats import spearmanr

# Values read directly from ac1_vs_crossing_rate_check.py's own committed output
# (metrics/ac1_vs_crossing_rate_check.json), restricted to the 6 peterlake (daily) series.
AC1 = {
    "Peter_chl": 0.9370848073693512,
    "Peter_pH": 0.9719029310694486,
    "Peter_doSat": 0.9232725678067595,
    "Paul_chl": 0.9215753268878328,
    "Paul_pH": 0.9395292204746353,
    "Paul_doSat": 0.8743760950368424,
}
RATE = {
    "Peter_chl": 6,
    "Peter_pH": 4,
    "Peter_doSat": 6,
    "Paul_chl": 3,
    "Paul_pH": 3,
    "Paul_doSat": 7,
}

keys = list(AC1.keys())
rho, p = spearmanr([AC1[k] for k in keys], [RATE[k] for k in keys])
print(f"n={len(keys)} rho={rho:.4f} p={p:.4f}")
