import numpy as np

np.random.seed(42)

N = 10000

# Assume users have different baseline propensities to convert.
user_quality = np.random.normal(0, 1, N)

# Baseline outcome score.
baseline = 10

# Assign treatment independently of user quality in a randomized A/B test.
treatment = np.random.binomial(
    n=1,
    p=0.5,
    size=N,
)

# The new UI increases every user's outcome by 3 points.
true_effect = 3.0

noise = np.random.normal(0, 1, N)

# Generate the observed outcome from user quality, treatment, and random noise.
y = (
    baseline
    + 2 * user_quality
    + true_effect * treatment
    + noise
)

treated_mean = y[treatment == 1].mean()
control_mean = y[treatment == 0].mean()

estimated_ate = treated_mean - control_mean

print("treated :", treated_mean)
print("control :", control_mean)
print("ATE     :", estimated_ate)
