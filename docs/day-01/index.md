# Day 01 · ATE (Average Treatment Effect)

## Today's question

**How much does a new UI increase users' outcome scores, on average?**

Randomly assign users to a treatment group using the new UI and a control group
using the existing UI. Estimate the new UI's average treatment effect by comparing
the groups' mean outcome scores.

This note follows the data generation process and output in
[`simulate_ate.py`](https://github.com/karim-moon/Causal/blob/main/src/day_01_ate/simulate_ate.py).

## Key concepts

### Treatment and potential outcomes

A treatment is the intervention whose effect we want to understand.
In this experiment, the treatment is **applying the new UI**.

| Symbol | Meaning | Corresponding code |
| --- | --- | --- |
| $T_i = 1$ | User $i$ receives the new UI | `treatment == 1` |
| $T_i = 0$ | User $i$ keeps the existing UI | `treatment == 0` |
| $Y_i(1)$ | User $i$'s potential outcome under the new UI | Score including the treatment effect |
| $Y_i(0)$ | User $i$'s potential outcome under the existing UI | Score before adding the treatment effect |
| $Y_i$ | The outcome observed under the assigned UI | `y` |

The same user could have different outcomes under the two UIs.
These possibilities are called potential outcomes.
In an actual experiment, each user receives one UI, so we observe only one of them.

$$
Y_i = T_i Y_i(1) + (1 - T_i)Y_i(0)
$$

### What does ATE average?

A user's individual treatment effect is the difference between their two potential outcomes:

$$
\tau_i = Y_i(1) - Y_i(0)
$$

The average treatment effect averages these individual effects over the target population:

$$
\mathrm{ATE} = \mathbb{E}[Y(1) - Y(0)]
$$

An ATE of 3 points means that applying the new UI raises the population's mean score
by 3 points compared with applying the existing UI.
Individual effects can differ in general; this simulation assigns the same effect to every user.

## Python experiment

### 1. Generate users and outcomes

The experiment generates a synthetic population with the following settings:

| Variable | Setting | Meaning |
| --- | --- | --- |
| `N` | `10000` | Number of users |
| `user_quality` | Normal distribution with mean 0 and standard deviation 1 | Users' underlying tendencies |
| `baseline` | `10` | Shared baseline score |
| `treatment` | Bernoulli assignment with probability 0.5 | Whether a user receives the new UI |
| `true_effect` | `3.0` | The treatment effect set by the simulation |
| `noise` | Normal distribution with mean 0 and standard deviation 1 | Random variation in the outcome |

The code sets `np.random.seed(42)` to make the results reproducible.

It generates the observed outcome as follows:

```python
y = (
    baseline
    + 2 * user_quality
    + true_effect * treatment
    + noise
)
```

Let $Q_i$ denote `user_quality` and $\varepsilon_i$ denote `noise`.
The outcome equation is:

$$
Y_i = 10 + 2Q_i + 3T_i + \varepsilon_i
$$

Users have different underlying tendencies and random errors.
Receiving the new UI adds 3 points to the outcome.

!!! note "The outcome variable in this code"
    The comment about `user_quality` mentions conversion propensity, but the generated
    `y` is a continuous score. Treatment effects in this experiment are measured in
    score points. Modeling conversion itself would require a binary outcome model.

### 2. Identify the true ATE

Hold a user's tendency and noise fixed, and change only their treatment assignment.
The data generation equation gives:

$$
\begin{aligned}
Y_i(0) &= 10 + 2Q_i + \varepsilon_i \\
Y_i(1) &= 10 + 2Q_i + 3 + \varepsilon_i
\end{aligned}
$$

Every user's individual treatment effect is exactly 3 points:

$$
Y_i(1) - Y_i(0) = 3
\quad\Longrightarrow\quad
\mathrm{ATE} = 3
$$

We know this value because we specified the simulation.
In a real A/B test, the effect is unknown and must be estimated from observed data.

### 3. Estimate ATE from observed data

Each user receives the new UI with probability 0.5:

```python
treatment = np.random.binomial(n=1, p=0.5, size=N)
```

With `n=1`, each assignment is either 0 or 1.
A probability of 0.5 does not guarantee two groups of exactly equal size.

Compute the mean outcome in each group:

```python
treated_mean = y[treatment == 1].mean()
control_mean = y[treatment == 0].mean()

estimated_ate = treated_mean - control_mean
```

This is the difference-in-means estimator:

$$
\widehat{\mathrm{ATE}}
= \overline{Y}_{T=1} - \overline{Y}_{T=0}
$$

Random assignment makes treatment independent of potential outcomes,
so the population difference in observed means identifies ATE:

$$
\mathbb{E}[Y \mid T=1] - \mathbb{E}[Y \mid T=0]
= \mathbb{E}[Y(1)] - \mathbb{E}[Y(0)]
= \mathrm{ATE}
$$

The simulation generates treatment independently of `user_quality` and `noise`.
It also allows each user to receive either UI and assumes that one user's outcome
does not depend on another user's UI assignment.

### 4. Run the experiment

From the repository root:

```bash
uv run src/day_01_ate/simulate_ate.py
```

The current code produces:

```text
treated : 12.983860837917403
control : 9.999531448740495
ATE     : 2.9843293891769083
```

The printed `ATE` is an estimate. The true ATE specified by the simulation is `3.0`.

## Interpreting the results

### Why are the group means close to 13 and 10?

Both `user_quality` and `noise` have expectation 0.
With random assignment, their contributions average toward 0 within each group.
The control mean approaches the baseline of 10, and the treatment mean approaches $10 + 3 = 13$.

### Why is the estimate not exactly 3?

In a finite sample, the two groups can have different mean user tendencies and errors by chance.
This run contains 5,124 treated users and 4,876 control users.

Averaging the outcome equation within each group gives:

$$
\widehat{\mathrm{ATE}}
= 3
+ 2\left(\overline{Q}_{T=1} - \overline{Q}_{T=0}\right)
+ \left(\overline{\varepsilon}_{T=1} - \overline{\varepsilon}_{T=0}\right)
$$

| Term | Value in this run |
| --- | ---: |
| True treatment effect | 3.000000 |
| Contribution from the difference in user tendencies | +0.006682 |
| Contribution from the difference in errors | −0.022353 |
| Total: estimated ATE | 2.984329 |

Random assignment does not eliminate every difference between groups in every run.
Across repeated experiments, the estimator's expectation equals the true ATE.
In this model, larger samples reduce the typical size of estimation error,
although every individual increase in sample size need not produce a closer estimate.

## Check your understanding

- What do `true_effect` and `estimated_ate` represent?
- Can we observe the same user's $Y_i(1)$ and $Y_i(0)$ simultaneously in an actual experiment?
- Why can this code estimate ATE without adjusting for `user_quality` in a regression?
- Does an ATE of 3 imply that every user's individual effect is 3?
  Which setting makes that statement true in this simulation?

## Open questions

- How can we calculate the estimate's standard error and confidence interval?
- How does ATE relate to individual effects when the effects vary between users?
- What does the simple difference in means estimate if UI assignment depends on user tendencies?

The last question is explored in [Day 02 · Confounding and Stratification](../day-02/index.md).
