import numpy as np
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(42)

N = 20_000

# Pre-treatment confounder: user experience affects assignment, the mediator, and outcome.
C = rng.normal(size=N)

# Users with more experience have a higher probability of receiving treatment.
p_treatment = 1 / (1 + np.exp(-1.2 * C))

T = rng.binomial(
    1,
    p_treatment,
    size=N
)

# The mediator responds to both treatment and user experience.
M = (
    0.8 * T
    + 0.7 * C
    + rng.normal(size=N)
)

# Treatment affects the outcome directly (1.0) and through the mediator (0.8 * 2.0).
# The true total effect is 2.6; each noise term is drawn independently.
Y = (
    1.0 * T
    + 2.0 * M
    + 1.5 * C
    + rng.normal(size=N)
)

model = LinearRegression()

# Regressing Y on T alone gives a confounded, unadjusted treatment coefficient.
model.fit(
    T.reshape(-1, 1),
    Y
)

print(model.coef_[0])


# Adjust for C to block both backdoor paths; leave M free to mediate the total effect.
# T is the first feature, so coef_[0] is its coefficient in the adjusted regression.
X = np.column_stack([
    T,
    C
])

model.fit(X, Y)

print(model.coef_[0])
