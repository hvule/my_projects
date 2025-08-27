# Project Evaluation using Real Option

This project provides an in-depth economic valuation of GenePath Innovations' groundbreaking gene-editing therapy, conducted to guide Zenith Ventures' investment decision in this high-potential, yet inherently uncertain, biotechnology venture.


We write python code to implement Monte Carlo simulation for modelling uncertainty. A total of 10,000 iterations were performed. In each iteration, a unique set of values for the stochastic variables was randomly sampled. These sampled values were then used to recalculate the commercial phase value, which was subsequently fed through the entire Real Options backward induction model to derive a final Real Option Value at Year 0 for that specific iteration.