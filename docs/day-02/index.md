# Day 02 · Confounding and Stratification

## Today's question

**How can we estimate a treatment effect when power users are more likely to receive treatment?**

In [Day 01](../day-01/index.md), every user had the same treatment probability.
Here, treatment assignment depends on a user's existing power-user status,
which also affects their outcome. We compare treated and untreated users
within each user group, then combine the group-specific estimates.

This note reviews the current implementation in
[`confounder.py`](https://github.com/karim-moon/Causal/blob/main/src/day_02_confounder/confounder.py).
The script already calculates the two within-stratum effects.
The weighted overall ATE calculation below is a suggested addition.

## Key concepts

### Power-user status is a confounder

Let $U_i$ indicate whether user $i$ is a power user, $T_i$ indicate treatment,
and $Y_i$ denote the observed outcome.

In this simulation, power-user status is determined before treatment and affects both:

- **Treatment assignment:** power users have an 80% treatment probability; regular users have a 20% probability.
- **The outcome:** power-user status adds 4 points, regardless of treatment.

The assumed causal relationships are:

```text
Power-user status ──→ Treatment ──→ Outcome
        └────────────────────────→ Outcome
```

A comparison of all treated users with all untreated users mixes the treatment
effect with the difference in their power-user composition.

### Stratification compares users within the same group

Stratification splits users into groups with the same measured confounder value:

| Stratum | Definition | Comparison |
| --- | --- | --- |
| Power users | `power_user == 1` | Treated power users versus untreated power users |
| Regular users | `power_user == 0` | Treated regular users versus untreated regular users |

For stratum $u$, the conditional average treatment effect (CATE) is:

$$
\tau(u) = \mathbb{E}[Y(1) - Y(0) \mid U=u]
$$

Its within-stratum difference-in-means estimate is:

$$
\widehat{\tau}(u)
= \overline{Y}_{U=u,T=1} - \overline{Y}_{U=u,T=0}
$$

The confounder's fixed contribution cancels within each stratum.
Random noise still contributes to sampling error.

## Python experiment

### 1. Generate a confounded treatment assignment

The code first generates power-user status:

```python
power_user = np.random.binomial(n=1, p=0.4, size=N)
```

The generating population has a 40% probability of power-user status.
It then assigns different treatment probabilities to the two groups:

```python
treated_prob = np.where(power_user == 1, 0.8, 0.2)
treatment = np.random.binomial(n=1, p=treated_prob)
```

Treatment is still sampled randomly **within** each stratum.
Across the whole population, treatment and power-user status are associated.

### 2. Generate an outcome with a known treatment effect

The outcome equation is:

```python
true_effect = 2.0
noise = np.random.normal(0, 1, N)
outcome = 5 + 4 * power_user + true_effect * treatment + noise
```

In mathematical notation:

$$
Y_i = 5 + 4U_i + 2T_i + \varepsilon_i
$$

Holding user status and noise fixed gives the two potential outcomes:

$$
\begin{aligned}
Y_i(0) &= 5 + 4U_i + \varepsilon_i \\
Y_i(1) &= 5 + 4U_i + 2 + \varepsilon_i
\end{aligned}
$$

Every user's treatment effect is 2 points. Both stratum-specific causal effects
and the population ATE therefore equal 2.

### 3. Calculate the naive mean difference

The script first compares the two treatment groups without adjusting for user status:

```python
treated_mean = outcome[treatment == 1].mean()
control_mean = outcome[treatment == 0].mean()
naive_ate = treated_mean - control_mean
```

The observed mean difference can be decomposed as:

$$
\overline{Y}_{T=1} - \overline{Y}_{T=0}
= 2
+ 4\left(\overline{U}_{T=1} - \overline{U}_{T=0}\right)
+ \left(\overline{\varepsilon}_{T=1} - \overline{\varepsilon}_{T=0}\right)
$$

Since $U$ is binary, its group mean is the proportion of power users.
In this run, power users make up **71.39% of treated users** and **13.97% of untreated users**.
That composition difference raises the naive estimate above the true effect.

### 4. Compare outcomes within strata

The four masks in the script correctly identify the required comparison groups:

```python
power_user_treatment_mask = (power_user == 1) & (treatment == 1)
power_user_control_mask = (power_user == 1) & (treatment == 0)

control_treatment_mask = (power_user == 0) & (treatment == 1)
control_control_mask = (power_user == 0) & (treatment == 0)
```

Each comparison must be parenthesized before combining the NumPy masks with `&`.
Here, `control_treatment_mask` means **treated regular users**.
The name's first `control` refers to user status, while the second condition refers to treatment.
Names such as `regular_user_treatment_mask` would make these two distinctions clearer.

For a fixed user status $u$, the term $5 + 4u$ is the same in both treatment groups:

$$
\widehat{\tau}(u)
= 2 + \overline{\varepsilon}_{U=u,T=1}
- \overline{\varepsilon}_{U=u,T=0}
$$

This removes the systematic contribution of power-user status to the comparison.
The remaining deviation from 2 comes from finite-sample noise.

### 5. Run the current script

From the repository root:

```bash
uv run src/day_02_confounder/confounder.py
```

With `N = 10000` and seed 42, the current script prints:

```text
True ATE : 2.0
Naive ATE: 4.291744153232842
power user ATE: 2.0103464220617884
control user ATE: 2.0037420461987683
```

The final two lines estimate the effects conditional on user status.
The label `control user ATE` refers to the regular-user stratum.

The underlying comparison groups are:

| Stratum | Total users | Treated users | Untreated users | Treated mean | Untreated mean | Estimated effect |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Power users | 3,892 | 3,102 | 790 | 10.995462 | 8.985116 | 2.010346 |
| Regular users | 6,108 | 1,243 | 4,865 | 7.012562 | 5.008820 | 2.003742 |

### 6. Combine the strata to estimate the overall ATE

The current script stops after calculating the two conditional effects.
To estimate the overall ATE, average those effects using the target population's
stratum proportions. This step is also called standardization.

$$
\mathrm{ATE}
= P(U=1)\tau(1) + P(U=0)\tau(0)
$$

Using the sampled users' proportions gives the following estimator:

$$
\widehat{\mathrm{ATE}}_{\mathrm{stratified}}
= \frac{n_1}{N}\widehat{\tau}(1)
+ \frac{n_0}{N}\widehat{\tau}(0)
$$

The following code can be appended to the existing script:

```python
power_user_ate = power_treatment_outcome.mean() - power_control_outcome.mean()
regular_user_ate = control_treatment_outcome.mean() - control_control_outcome.mean()

power_user_weight = (power_user == 1).mean()
regular_user_weight = (power_user == 0).mean()

stratified_ate = (
    power_user_weight * power_user_ate
    + regular_user_weight * regular_user_ate
)

print("Stratified ATE:", stratified_ate)
```

Evaluating this addition with the current simulation gives:

```text
Stratified ATE: 2.0063124692846555
```

The empirical weights are 0.3892 for power users and 0.6108 for regular users.
Use the proportion of each stratum among **all users in the target population**.
Using treated-user proportions instead would target the treated population's mix.
An equal average of the two estimates would give the two strata equal weight;
that is not the user mix in this sample.

If the target is explicitly the generating population with a known 40% power-user share,
use weights 0.4 and 0.6 instead. The true effect is constant in this simulation,
so either population's true ATE is 2; their finite-sample weighted estimates can differ slightly.

## Interpreting the results

| Quantity | Value | Interpretation |
| --- | ---: | --- |
| True ATE | 2.000000 | Set by the data generation equation |
| Naive mean difference | 4.291744 | Includes the effect of unequal power-user composition |
| Power-user effect estimate | 2.010346 | Treated versus untreated power users |
| Regular-user effect estimate | 2.003742 | Treated versus untreated regular users |
| Weighted overall estimate | 2.006312 | Combines the stratum estimates using the sampled user mix |

The naive comparison overstates the treatment effect by about 2.29 points.
The within-stratum comparisons adjust for the measured confounder,
and the weighted estimate is close to the known ATE of 2.
The small gap remains because the comparison cells contain different realized noise values.

### Assumptions behind the adjustment

- **Conditional exchangeability:** within each stratum, treatment is independent of potential outcomes. The simulation satisfies this because assignment uses only `power_user` and the outcome noise is generated independently.
- **Positivity:** each stratum can receive either treatment. Probabilities of 0.8 and 0.2 satisfy this, and this run has observations in all four cells.
- **Consistency and no interference:** the observed outcome follows the assigned treatment, and one user's outcome does not depend on other users' treatments.

These conditions connect within-stratum comparisons to causal effects. See
Hernán and Robins' [Causal Inference: What If](https://miguelhernan.org/whatifbook)
for standardization and identification assumptions.

For other data, check cell counts before taking means: an empty treated or untreated cell
makes that stratum's comparison undefined. Very small cells can make it unstable.
Stratification adjusts for confounding captured by the measured grouping variable;
it cannot establish that additional unmeasured confounders are absent.

## Review of the current implementation

The assignment mechanism, outcome equation, four masks, and within-stratum mean
differences are consistent with the intended simulation.
The main addition needed for an overall ATE is the weighted combination in step 6.

For clearer terminology, describe the last two outputs as stratum-specific effects,
use `regular_user` for `power_user == 0`, and describe the adjustment as controlling
for power-user status. Stratification leaves random outcome noise in the estimates.

## Check your understanding

- What makes `power_user` a confounder in this simulation?
- Why does sampling treatment randomly still produce a confounded overall comparison?
- Why does the 4-point user-status contribution cancel within each stratum?
- Why should the overall ATE use population weights instead of treatment-group weights?
- What happens if every power user receives treatment, leaving no untreated power users?

## Open questions

- How would the overall ATE change if treatment effects differed between the two strata?
- How can we adjust for several confounders without creating too many small comparison cells?
- How should we calculate the weighted estimate's uncertainty?

## References

- [Experiment code](https://github.com/karim-moon/Causal/blob/main/src/day_02_confounder/confounder.py).
- Hernán MA and Robins JM, [Causal Inference: What If](https://miguelhernan.org/whatifbook), Chapters 2 and 3: standardization and identification assumptions.
