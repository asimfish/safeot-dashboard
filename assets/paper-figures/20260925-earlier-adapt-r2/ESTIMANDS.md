# Figure 1 statistics

Comparator: TRPO-Lag. Curves are medians across task seed-mean training cost divided by budget. SafePO: 10 tasks, B=25, 100 progress points. Bullet: 6 tasks, B=10, 50 progress points; producer rolling-50 training metrics. These frozen curves cover a broader SafePO seed snapshot than the selected primary headline statistic.

Headline SafePO V ratio: original five-seed comparison, median of 10 task ratios, 0.3741627178002498, 95% interval [0.2019631304329907, 0.5140837543413825], lower V on 10/10 tasks. Bullet: ratio of equally weighted six-task mean V, 0.22122613745991185, interval [0.13087988367079073, 0.45504761087506684], lower V on 6/6 tasks. Values round directly to 0.37 and 0.22. No confidence intervals are drawn in the teaser; exact supplied intervals remain in the JSON.

The shaded areas are the parts of the task-median curves above budget, on their displayed scales. They are not the two reported V ratios, which aggregate per-policy training excess first. The log scale in the Bullet panel further rules out reading its drawn area as a linear integral. Counts describe task-level mean V and do not claim every seed wins, every policy is feasible, or reward noninferiority.

The figure preserves the explicitly selected primary estimates. Other snapshots and forest figures have different task/seed estimators and must not be silently substituted. All accompanying empirical source values and original pairings remain unchanged.
