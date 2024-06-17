---
title: An Introduction to Rules-Based Modelling
date: YYYY-MM-DD HH:MM:SS +/-TTTT
categories: [TOP_CATEGORIE, SUB_CATEGORIE]
tags: [TAG]     # TAG names should always be lowercase
---

Rules-based Modelling ....

## Example: A Simple Epidemeology Model - SIR

An example of rules based modelling can be found from epidemology. The SIR model paritions the population in question into S (susceptible), I (infected) and R (recovered) compartments. The model evolves according to a set of rules, each describing how each individual moves from the compartment. In this case the model is a closed system as 

Rule 1: Infection
Rule 2: Recovery
Rule 3: 

We can introduce "demography" effects to model the natural deaths and births of the population. The key influence on the modelling will be the loss an immunne population and the introduction of a susceptible population. This new model is now no longer a closed system.

Rule 4: Births
Rule 5: Natural Deaths

## How We Solve the Model

The simplest way to solve the model is the Gillespie algorithm. For each iteration we select a rule to trigger probablistically, based on the rule's propensity. We then select a time duration from the exponential distribution with a rate of total propensity ***


## Comparision with Deterministic Models

Compared to a determanistic approach for example, modelling the change in SIR compartments using (ordinary) differential equations, the stochastic, rules-based approach produces a range of different trajectories as opposed to the same trajectory for all differential equations based model (a single solution). This could be very useful to understand how a supply chain behaves with small perturbations in for example delivery time, or production volume.

Additionally, as discrete rules that are triggered, we can guarantee that. This isn't 

