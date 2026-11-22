
# Marketplace A/B Testing & Product Experimentation

**Python | PostgreSQL | pandas | SciPy | Statistics | Product Analytics**

An end-to-end data science project exploring how A/B testing can help online marketplaces evaluate new product features and make data-driven decisions.


---

## 1. Project Overview

Online marketplaces continuously introduce new features to improve user engagement, purchasing behaviour, and customer experience. However, determining whether a feature genuinely improves business performance requires more than simply comparing metrics.

This project investigates the following business question:

**Does introducing personalised item recommendations increase purchase conversion in a second-hand marketplace?**

To answer this question, I developed a simulated A/B testing experiment involving 30,000 users, analysed experimental outcomes using Python and PostgreSQL, and applied statistical hypothesis testing to evaluate the observed differences.

The project demonstrates the complete analytical workflow, from defining a business problem and preparing data to interpreting statistical results and making business recommendations.

## 2. Business Problem

A hypothetical second-hand marketplace is considering introducing a new personalised recommendations feature.

The product team wants to determine whether the new experience encourages more users to complete purchases.

Two experimental groups are created:

- **Control (A):** Users experience the existing marketplace interface.
- **Treatment (B):** Users experience the interface with a new personalised recommendations entry point.

The primary objective is to determine whether the treatment increases the proportion of users who make a purchase within seven days.

### Experiment Design

| Parameter | Description |
|---|---|
| Experiment type | Randomised A/B test |
| Participants | 30,000 simulated users |
| Control group | 15,000 users |
| Treatment group | 15,000 users |
| Primary metric | 7-day purchase conversion rate |
| Statistical test | Two-proportion z-test |
| Significance level | 0.05 |
| Confidence level | 95% |

The experiment uses user-level randomisation and includes all assigned users in the primary analysis.

## 3. Dataset

The project uses a reproducible synthetic dataset generated with Python and NumPy.

Each record represents one simulated marketplace user.

### Dataset Features

| Feature | Description |
|---|---|
| user_id | Unique user identifier |
| variant | Control or treatment assignment |
| country | User's simulated country |
| device | Device category |
| prior_buyer | Previous purchasing activity |
| clicked_listing | Whether the user clicked a listing |
| purchased_7d | Purchase within seven days |
| order_value_eur | Gross order value in euros |
| refunded_7d | Whether a purchase was refunded |

A fixed random seed (`20261122`) ensures reproducibility.

The dataset intentionally includes a small positive treatment effect to demonstrate how experimentation and statistical inference work.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data generation and analysis |
| pandas | Data manipulation and aggregation |
| NumPy | Numerical operations |
| PostgreSQL | SQL-based data analysis |
| SciPy | Statistical hypothesis testing |
| Matplotlib | Data visualisation |
| pytest | Automated validation |

## 5. Methodology

### 5.1 Data Preparation

The first stage involves generating and validating the experimental dataset.

The workflow includes:

1. Generating synthetic marketplace user records.
2. Randomly assigning users to control and treatment.
3. Validating unique user identifiers.
4. Checking experimental group sizes.
5. Inspecting pre-experiment purchasing activity.
6. Preparing variables for statistical analysis.

### 5.2 Primary Metric

The primary metric is the 7-day purchase conversion rate.

**Purchase Conversion Rate = Number of users who purchased / Total assigned users × 100%**

All randomised users are included in the denominator, including those who never interacted with the recommendations feature.

### 5.3 Hypothesis Testing

The experiment evaluates two hypotheses.

**Null Hypothesis (H0):**

There is no difference in purchase conversion rates between the control and treatment groups.

**Alternative Hypothesis (H1):**

The purchase conversion rates differ between the control and treatment groups.

A two-sided two-proportion z-test is performed using a significance level of 0.05.

The analysis also calculates:

- Absolute conversion lift.
- Relative conversion lift.
- 95% confidence interval.
- Z-statistic.
- P-value.

### 5.4 SQL Analysis

PostgreSQL queries are used to investigate business and experimental metrics.

The analysis includes:

- Purchase conversion by experimental variant.
- Listing click-through rates.
- Gross order value per assigned user.
- Sample ratio mismatch checks.
- Purchasing behaviour across countries.
- Refund rates among purchasers.

This demonstrates how SQL can be used to extract and analyse data for business decision-making.

## 6. Experiment Results

### 6.1 Purchase Conversion

| Metric | Control | Treatment |
|---|---:|---:|
| Users | 15,000 | 15,000 |
| Purchasers | 1,199 | 1,358 |
| Conversion rate | 7.99% | 9.05% |

The treatment group achieved a higher observed purchase conversion rate.

### Conversion Rate Visualisation

In the folder outputs --> file `conversion_by_variant.png`

The visualisation compares the percentage of users who completed a purchase in each experimental group.

### 6.2 Statistical Results

| Statistical Metric | Result |
|---|---:|
| Absolute conversion lift | +1.06 percentage points |
| Relative conversion lift | +13.26% |
| Z-statistic | 3.288 |
| P-value | 0.00101 |
| 95% confidence interval | +0.43 to +1.69 percentage points |
| Significance level | 0.05 |

### Interpretation

The observed p-value is below the selected significance level of 0.05.

Therefore, the null hypothesis of equal conversion rates is rejected for the simulated experiment.

The confidence interval is entirely positive, supporting the conclusion that the treatment group achieved a higher conversion rate in this generated sample.

However, statistical significance does not automatically mean a feature is commercially valuable or ready for deployment.

### 6.3 Country-Level Analysis

The project also investigates differences in purchase conversion across simulated countries.

In the folder outputs --> file `conversion_by_country.png`

This exploratory analysis demonstrates how experimentation results can be investigated across different user segments.

Country-level results are not corrected for multiple hypothesis testing and should not be interpreted as independently confirmed treatment effects.

### 6.4 Secondary Business Metrics

Additional metrics include:

- Listing click-through rate.
- Gross order value per assigned user.
- Refund rate among purchasers.

These measurements help provide context beyond the primary conversion metric.

Refund rates require particular caution because they are calculated only among users who purchased, rather than all randomised participants.

## 7. Business Insights

The experiment illustrates how statistical testing can support data-driven product development.

### Key Findings

**1. Higher purchase conversion**

The treatment group achieved an observed conversion rate of 9.05%, compared with 7.99% for the control group.

**2. Statistically significant difference**

The two-proportion z-test identified a statistically significant difference between experimental groups in the simulated sample.

**3. Importance of secondary metrics**

Purchase conversion alone is insufficient for evaluating an entire product feature. Engagement, transaction value, and refund behaviour should also be considered.

**4. Need for careful interpretation**

Statistical significance should be combined with business context, data quality validation, and operational considerations.

## 8. Business Recommendations

Based on the simulated experiment, the treatment demonstrates a promising positive conversion effect.

Before recommending a real product launch, I would:

1. Verify experiment tracking and randomisation.
2. Confirm the experiment duration and sample size are appropriate.
3. Review secondary metrics and guardrails.
4. Evaluate implementation costs and expected business benefits.
5. Investigate whether the effect remains consistent across relevant user segments.
6. Consider a controlled rollout following additional validation.

**Conclusion:** The simulated experiment provides evidence of higher conversion under the generated assumptions, but it does not establish that the feature would perform similarly in a real marketplace.

## 9. Project Structure

```text
marketplace-ab-testing-experiment/
│
├── data/
│   └── experiment_users.csv
│
├── sql/
│   ├── 01_create_table.sql
│   └── 02_analysis_queries.sql
│
├── src/
│   ├── generate_data.py
│   └── analyze_experiment.py
│
├── outputs/
│   ├── conversion_by_variant.png
│   ├── conversion_by_country.png
│   ├── variant_summary.csv
│   ├── country_exploration.csv
│   └── experiment_results.json
│
├── tests/
│   └── test_experiment.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## 10. How to Run the Project

### Requirements

- Python 3.10+
- pip
- PostgreSQL (optional)

### Step 1 — Clone the Repository

```bash
git clone https://github.com/tamyeg/marketplace-ab-testing-experiment.git
cd marketplace-ab-testing-experiment
```

### Step 2 — Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 3 — Generate the Dataset

```bash
python src/generate_data.py
```

### Step 4 — Run the Analysis

```bash
python src/analyze_experiment.py
```

The script generates statistical results, CSV summaries, and visualisations in the `outputs` folder.

### Step 5 — Run Automated Tests

```bash
python -m pytest -q
```

### Step 6 — Optional PostgreSQL Analysis

Create a PostgreSQL database and open `psql` from the repository root.

Run:

```sql
\i sql/01_create_table.sql

\copy experiment_users FROM 'data/experiment_users.csv' WITH (FORMAT csv, HEADER true)

\i sql/02_analysis_queries.sql
```

The Python analysis can also run independently without PostgreSQL.

## 11. Skills Demonstrated

- Data cleaning and processing with Python and pandas.
- PostgreSQL queries for business analytics.
- Experimental design and hypothesis testing.
- A/B testing and statistical inference.
- Confidence interval calculations.
- Statistical significance interpretation.
- Data visualisation.
- Product and business metric analysis.
- Translating analytical findings into recommendations.
- Reproducible analysis and automated testing.

## 12. Limitations and Future Improvements

This project uses synthetic observations, rather than genuine marketplace user behaviour.

The dataset intentionally includes a positive treatment effect, meaning the experiment illustrates statistical analysis rather than independently discovering a real product improvement.

Additional limitations include:

- No real-world tracking inconsistencies.
- No realistic sequence of user events.
- No experiment-duration or statistical-power analysis.
- No multiple-testing adjustments for exploratory comparisons.
- Limited simulation of long-term customer behaviour.

### Future Development

Potential improvements include:

- Statistical power and minimum detectable effect calculations.
- More realistic event-level marketplace datasets.
- Sequential testing and monitoring.
- Additional guardrail metrics.
- User segmentation and heterogeneous treatment-effect analysis.
- Interactive dashboards for product experimentation.

## 13. Author

**Tamara Yegorova**

Master's student in Artificial Intelligence in Computer Science at Kaunas University of Technology.

Interested in Data Science, Machine Learning, Statistics, and Product Analytics.

**GitHub:** https://github.com/tamyeg

---

