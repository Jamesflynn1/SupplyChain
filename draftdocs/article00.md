---
title: An Introduction to Rules-Based Modelling
date: YYYY-MM-DD HH:MM:SS +/-TTTT
categories: [TOP_CATEGORIE, SUB_CATEGORIE]
tags: [TAG]     # TAG names should always be lowercase
---

Rules-based Modelling ....

## Objects

- Classes

Classes are the objects of interest within the model. The class can take the form of discrete or continuous variables. 

Examples: 

In a model of an epidemic, a 

- Rules

Rules describe the movement/destruction/creation of classes in the model.

The movement/destruction/creation of a rule is described by the stoichiometry of the rule. Each class either gains, losses or has no change in terms of its value as the result of a rule. Which is the case, and how by how much, is described by the stochiometric coeffecient.

The propensity function of the rule describes how frequent the rule occurs. This is a function the classes found in the model. In traditional mass action kinetics, the propensity is a function of the reactant classes only - so-called due to it's origins in reaction kinetics in Chemistry.

Examples:

- The forward reaction of the Harber-Bosch process. Note that is process is best off described by a traditional ODE approach, although, the rules based approach will approximate the dynamics with a sufficently small quantity. In fact, at the atomic level
the reaction is probably better described by the stochastic rules based model due to the probabalastic nature of collision (therefore reaction) events. The probabilitic nature is increasing less relevant when billions or trillions of collisions occur a second. 

N_2 + 3H_2 -> 2NH_3 (stoichiometry: [-1, -3, 2], propensity: N_2*H_2^3)

- Infection dynamics of COVID



- Locations

Locations provide compartmentalise

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

