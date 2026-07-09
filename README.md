# Understanding Customer Satisfaction and Identifying What Drives Loyalty at Starbucks

**Morgan Gunther** <br>
**Professor Hammer** <br>
**BMIS 326: Introduction to Analytics**

## Executive Summary

Customer satisfaction has become a real problem for major coffee chains. A 2025 review analysis of over 6 million consumer reviews across 150,000 U.S. coffee shop locations found that satisfaction at big chains is nearly 30% lower than it was five years ago, driven by long waits, inconsistent service, and customers feeling they're not getting enough value (Evans, 2025). That's an opportunity for a company like Starbucks to figure out which parts of the customer experience matter most. Rather than treating "satisfaction" as one vague thing, this project breaks it down into specific, measurable categories. These are product quality, price, promotions, ambiance, WiFi, service, and likelihood to return. My goal is to identify which of these categories are driving customers away, and whether loyalty indicators, like membership enrollment, connect to specific satisfaction categories. Using a customer satisfaction survey of 122 Starbucks customers, this analysis found that price stands out as a clear weak point relative to every other category, and that membership enrollment shows a strong connection to whether a customer plans to keep buying. These findings point toward specific, fixable areas of focus rather than a vague sense that satisfaction is simply down, and could help Starbucks, or any coffee chain, prioritize real improvements and hold onto customers who might otherwise drift toward smaller, more personal coffee shops, which are gaining ground.

## Statement of Scope

This project is a descriptive analysis of customer satisfaction, looking at how satisfaction breaks down across different parts of the customer experience and whether it connects to loyalty indicators like membership enrollment or intent to keep buying. The data source is a customer satisfaction survey collected from Starbucks customers in Malaysia, hosted on Kaggle, a public platform for sharing datasets. The survey asks respondents to rate seven different parts of their experience on a 1 to 5 scale, along with demographic and behavior questions like age, membership card status, and whether they plan to keep buying from Starbucks.

**Project Objectives:**
- Calculate the average rating for each of the seven satisfaction categories (product, price, promotions, ambiance, WiFi, service, and likelihood to choose Starbucks again) to identify which areas customers rate highest and lowest.
- Determine what percentage of respondents who say they will continue buying from Starbucks also hold a membership card, to see if membership is connected to loyalty.
- Compare average satisfaction ratings across age groups to see whether certain age groups are consistently less satisfied than others.

My sample is the 122 respondents included in the survey. The population I'm hoping to speak to is Starbucks customers more broadly.

**Unit of Analysis:** My unit of analysis is the Customer. Since I'm assessing satisfaction with different parts of the Starbucks experience, a single customer, represented as one survey respondent, is what I'm measuring and comparing, not a store location, a product, or a transaction.

## Data Access & Consolidation

My data comes from a single source: the "Starbucks Customer Survey" dataset hosted on Kaggle ([https://www.kaggle.com/datasets/mahirahmzh/starbucks-customer-retention-malaysia-survey](https://www.kaggle.com/datasets/mahirahmzh/starbucks-customer-retention-malaysia-survey)). It contains 122 survey responses across 20 original questions. I chose this dataset because it's small, clean, and every question maps directly to something measurable and chartable, which matters given the scope of this project. Since I'm only using one data file, no merging was required. This project relies on a single data source rather than multiple merged files by design. Since my unit of analysis is the individual customer, and this survey already captures customer-level satisfaction and loyalty data directly, a single source was preferable to combining datasets with different units of analysis, such as a coffee shop revenue dataset I considered earlier that was measured at the daily-operations level rather than the individual-customer level. Most of the survey questions replaced the brand name with the generic term "Coffee House" instead of naming Starbucks directly, but one column (how respondents hear about promotions) still literally referenced "Starbucks Website/Apps," confirming the source of the data even though it wasn't labeled that way throughout.

## Data Reduction

I reduced the original 21 columns (20 survey questions plus a timestamp) down to 19. I removed two columns entirely:

- **Timestamp**: This had no analytical value for any of my three project objectives (average satisfaction by category, membership vs. loyalty connection, satisfaction by age group).
- **Question 19** (how respondents hear about promotions): While interesting, this column doesn't tie back to any of my stated objectives, so I removed it to keep the dataset focused.

I did not remove any rows. Every one of the 122 respondents is a legitimate member of the population I'm trying to understand (coffee chain customers). Nothing in this dataset gave me a reason to exclude any respondent. I saved my reduced dataset as a new file (sbux_reduced.csv) rather than overwriting the original, so the raw data is still available if I need to revisit a decision later.

## Data Cleaning

**Missing values:** Two columns had missing values, both minor. The "how do you usually enjoy Coffee House" question was missing one response out of 122 (0.8%). Rather than drop that respondent's entire row, which would throw away their answers to the other 19 questions over one skipped question, I recoded the missing value as "Unknown."

**Inconsistent categories:** The same "how do you usually enjoy" column had several values that were really saying the same thing but weren't standardized: "never, Never, Never buy" and "I don't like coffee" were all collapsed into a single consistent "Never" category. Before cleaning, this column had 8 distinct values, and after cleaning, it had 5.

**Erroneous/off-topic data:** The "what do you most frequently purchase" column had several responses that weren't real answers to the question at all, things like "Jaws chip, cake, Nothing, and Never buy any." These looked like confused or joke responses from people who don't actually purchase anything at the coffee shop. I recoded these into a single "Other/None" category rather than leaving them as scattered text values that would each show up as their own meaningless category in a breakdown. One case I left alone was a single response of "Cold drinks;Never," a contradictory multi-select answer (a question where respondents could pick more than one option). I chose not to touch this one, since "Cold drinks" is a legitimate purchase behavior and the stray "Never" selection looks more like an accidental click than a meaningful response, and it's only one row out of 122 either way.

**Data type checks:** I confirmed that all seven satisfaction rating columns (quality, price, promotions, ambiance, WiFi, service, and likelihood to return) were already stored as whole numbers on a 1-5 scale with zero missing values. I verified this directly in Python rather than assuming it, since it would've been easy to just say "nothing to clean here" without actually checking.

## Data Transformation

I renamed every column from the original long survey-question text (e.g., "12. How would you rate the quality of Coffee House compared to other brands...") to short, code-friendly names (e.g., Rating_Quality), since the raw question text is difficult to reference in code and tables.

I converted the Age column into an ordered category (Below 20 → 20-29 → 30-39 → 40 and above) instead of leaving it as plain text, so that any chart or table grouped by age sorts in a logical order instead of alphabetically.

Finally, I constructed a new variable, "Avg_Satisfaction," calculated as the mean of the seven individual rating columns for each respondent. This gives me a single overall satisfaction score per person, which is useful both for my descriptive statistics and for comparing satisfaction across groups like age, without needing to look at all seven categories separately every time.

## Data Dictionary

**Variable types used below:** *Categorical* = named groups with no inherent order (e.g., gender). *Ordinal* = categories with a natural order or ranking (e.g., age brackets, income brackets). *Binary* = only two possible values. *Numeric* = a measurable number.

| Variable | Description | Type | Values/Range |
|---|---|---|---|
| Gender | Respondent's gender | Categorical | Female, Male |
| Age | Respondent's age group | Ordinal | Below 20, From 20 to 29, From 30 to 39, 40 and above |
| Employment | Current employment status | Categorical | Employed, Student, Self-employed, Housewife |
| Income | Annual income bracket, measured in Malaysian Ringgit (RM), the currency used since this survey was collected from customers in Malaysia | Ordinal | Less than RM25,000 → More than RM150,000 |
| VisitFrequency | How often they visit | Ordinal | Never, Rarely, Monthly, Weekly, Daily |
| EnjoyMethod | How they usually consume | Categorical | Take away, Dine in, Drive-thru, Never, Unknown |
| VisitDuration | Time spent per visit | Ordinal | Below 30 min → More than 3 hours |
| NearestOutlet | Distance to nearest location | Ordinal | within 1km, 1km-3km, more than 3km |
| Membership | Holds a membership card | Binary | Yes, No |
| PurchaseType | What they typically buy | Categorical (multi-select) | Coffee, Cold drinks, Pastries, combinations, Other/None |
| SpendPerVisit | Typical spend per visit, in Malaysian Ringgit (RM) | Ordinal | Zero, Less than RM20, RM20-RM40, More than RM40 |
| Rating_Quality | Rating: product quality vs. competitors | Numeric (1-5 scale) | 1-5 |
| Rating_Price | Rating: price range | Numeric (1-5 scale) | 1-5 |
| Rating_Promotions | Rating: importance of promotions | Numeric (1-5 scale) | 1-5 |
| Rating_Ambiance | Rating: ambiance | Numeric (1-5 scale) | 1-5 |
| Rating_WiFi | Rating: WiFi quality | Numeric (1-5 scale) | 1-5 |
| Rating_Service | Rating: service quality | Numeric (1-5 scale) | 1-5 |
| Rating_LikelyReturn | Rating: likelihood to return | Numeric (1-5 scale) | 1-5 |
| Avg_Satisfaction | Constructed: mean of 7 rating columns | Numeric | 1-5 |
| Continue | Will keep buying | Binary | Yes, No |

## Descriptive Statistics

| Variable | Mean | Median | Std Dev | Min | Max |
|---|---|---|---|---|---|
| Rating_Quality | 3.66 | 4.00 | 0.94 | 1 | 5 |
| Rating_Price | 2.89 | 3.00 | 1.08 | 1 | 5 |
| Rating_Promotions | 3.80 | 4.00 | 1.09 | 1 | 5 |
| Rating_Ambiance | 3.75 | 4.00 | 0.93 | 1 | 5 |
| Rating_WiFi | 3.25 | 3.00 | 0.96 | 1 | 5 |
| Rating_Service | 3.75 | 4.00 | 0.83 | 1 | 5 |
| Rating_LikelyReturn | 3.52 | 4.00 | 1.03 | 1 | 5 |
| Avg_Satisfaction | 3.52 | 3.57 | 0.67 | 1 | 5 |

## Visualizations

### Story 1: Price Is the Weakest Category

With customer satisfaction with major coffee chains reportedly down nearly 30% over the last five years, the question isn't whether people are less happy, but why they are. Breaking satisfaction into seven specific categories instead of treating it as one vague feeling makes it possible to pinpoint exactly where that dissatisfaction is coming from. The chart below shows the average rating customers gave across all seven categories, sorted from lowest to highest.

![Average satisfaction by category](story1_price_gap.png)

Price stands out as the clear weak point, averaging 2.89 out of 5, nearly a full point below Promotions, the highest-rated category at 3.80. Every other category clusters fairly tightly around the overall average (the dashed line), which suggests this isn't a company struggling across the board. It's a company whose customers specifically feel like they aren't getting enough value for what they pay. That's a much more useful, fixable finding than a vague sense that "satisfaction is down," and it directly supports the idea that price, not product quality or service, is the biggest lever for improving how customers feel about the brand.

### Story 2: Membership Predicts Loyalty

One of the goals of this project was to figure out whether loyalty program participation actually connects to customers sticking around, or whether it's just a good thing to have that doesn't move the needle. To test this, I compared membership card ownership between two groups: customers who said they'll continue buying from the coffee chain, and customers who said they won't.

![Membership rate by loyalty status](story2_membership_loyalty.png)

The gap is substantial. Among customers who plan to keep buying, 58.5% hold a membership card, compared to just 17.9% of customers who don't plan to continue, over a 3x difference. This suggests membership enrollment isn't just a side perk but it's meaningfully tied to whether a customer sticks with the brand. For a coffee chain trying to reduce churn (customers leaving to buy from a competitor instead) to smaller, more personal competitors, this points to a concrete strategy that getting more customers enrolled in the membership program could be one of the more direct ways to improve retention, rather than relying only on improving individual experience factors like price or service.

## Conclusion and Discussion

My goal with this project was to break down customer satisfaction at a coffee chain into specific, measurable categories instead of treating it as one vague feeling, and to see whether that breakdown connects to loyalty indicators like membership enrollment. Based on this initial analysis, that approach is already paying off. Price stands out as a clear, specific weak point (2.89 out of 5, well below every other category), and membership enrollment shows a real connection to whether customers plan to keep buying (58.5% among loyal customers vs. 17.9% among those planning to leave). Again, these aren't vague impressions, they're specific, fixable signals that a business could act on.

Gathering and preparing this data came with a few struggles. The dataset required meaningful cleanup before it was usable. Inconsistent category labels (like never vs. Never vs. Never buy), a handful of off-topic or joke responses in the purchase-type question, and a small number of missing values. None of these were difficult to fix individually, but they required actually looking closely at the data rather than assuming a "clean" dataset from Kaggle was ready to go. If I were doing this again, I'd build in time earlier in the process specifically for auditing data quality before committing to a dataset, since I initially explored a few other datasets before landing on this one and only caught, through correlation checks, that some of them were randomly generated and not usable for real analysis. Starting with that kind of audit sooner would save time down the line.

In terms of implications, this kind of category-by-category breakdown matters beyond just this one company. Coffee chains broadly are dealing with declining satisfaction as customers increasingly consider smaller, more personal coffee shops instead. A business that can pinpoint price, specifically, rather than product quality or service, as its biggest satisfaction gap is in a much better position to make a targeted fix. Similarly, showing a real connection between membership enrollment and loyalty gives a business a concrete lever to pull (growing membership enrollment) rather than guessing at what keeps customers coming back. I hope this analysis, even at this early stage, shows that satisfaction and loyalty aren't unknowable areas. They can be broken into specific, addressable pieces with the right data.

## Reference

Evans, Russell. "Grounds for Concern: Why National Coffee Shop Chains Are Losing Steam." *ZS*, 25 Aug. 2025, [www.zs.com/insights/retail-coffee-trends-and-loyalty-insights](http://www.zs.com/insights/retail-coffee-trends-and-loyalty-insights).
