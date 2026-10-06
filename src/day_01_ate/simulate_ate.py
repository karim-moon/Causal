import numpy as np

np.random.seed(42)

N = 10000

# 사용자마다 원래 conversion 성향이 다르다고 가정
user_quality = np.random.normal(0, 1, N)

# user baseline score
baseline = 10

# Randomized A/B test
treatment = np.random.binomial(
    n=1,
    p=0.5,
    size=N,
)

# New UI의 실제 효과
true_effect = 3.0

noise = np.random.normal(0, 1, N)

# 우리가 실제로 관측하는 outcome
# 가장 쉽게 modeling
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