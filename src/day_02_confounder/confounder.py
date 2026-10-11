import numpy as np

np.random.seed(42)

N = 10000

power_user = np.random.binomial(n=1, p=0.4, size=N)

# Power users are more likely to receive treatment than regular users.
treated_prob = np.where(
    power_user == 1,
    0.8,
    0.2
)

treatment = np.random.binomial(n=1, p=treated_prob)

true_effect = 2.0  # The simulation's known treatment effect.
noise = np.random.normal(0, 1, N)
outcome = (
    5
    + 4 * power_user
    + true_effect * treatment
    + noise
)

treated_mean = outcome[treatment == 1].mean()
control_mean = outcome[treatment == 0].mean()

naive_ate = treated_mean - control_mean

print("True ATE :", true_effect)
print("Naive ATE:", naive_ate)  # This unadjusted comparison is confounded by user status.
# Compare treated and untreated outcomes separately within each user-status stratum.
power_user_treatment_mask = (power_user == 1) & (treatment == 1)
power_user_control_mask = (power_user == 1) & (treatment == 0)

control_treatment_mask = (power_user == 0) & (treatment == 1)
control_control_mask = (power_user == 0) & (treatment == 0)

# Stratification adjusts for user status; random outcome noise remains.
power_treatment_outcome = outcome[power_user_treatment_mask]
power_control_outcome = outcome[power_user_control_mask]

control_treatment_outcome = outcome[control_treatment_mask]
control_control_outcome = outcome[control_control_mask]

print("power user ATE:", power_treatment_outcome.mean() - power_control_outcome.mean())
print("control user ATE:", control_treatment_outcome.mean() - control_control_outcome.mean())
