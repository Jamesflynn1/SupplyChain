---
title: Why Machine Learning Isn't a Silver Bullet.
date: YYYY-MM-DD HH:MM:SS +/-TTTT
categories: [TOP_CATEGORIE, SUB_CATEGORIE]
tags: [TAG]     # TAG names should always be lowercase
---

Machine Learning is pervasive in building models in all areas. AI has become a buzzword .

I am a keen student of AI techniques, and I am amazed by the

However, Machine Learning isn't a silver bullet and suffers from several systemic issues.

Explainability, often machine learning acts as a black box, complex neural networks can have ... neurons. Noone can understand the exact workings. A model can be presented and understood by non-experts. For example, the relationship between cargo availiblity** and n*** easily and exactly understood by the CEO of - knowing that a relationship is linear, exponentitial and the strength of the relationship between variables would help a CEO understand the effect of adding one new factory, or two or three. Or perhaps he could add the capacity of half a factory down the line. He wouldn't need to resort to the analytics team, or use a tool developed by data science, he knows the linear relationship. He can act immediate if he is required to, without further modelling, empowering business users to understand a problem, simply - but also precisely.


Robustness, in out of sample 

This is contrasted to a Mathematical model, the exact interactions between different quantities are constrained and user defined. Additionally, we define a model boundary and list out model assumptions. While this could be seen as restrictive if the sole aim to minimise error on average, a task machine learning excels in, if we care about near correctness of results and outlier cases, Mathematical modelling offers a pargdigm.

A classic example of a Machine Learning model failing in a spectactular way is in asking ChatGPT a question. Not only does ChatGPT answer the question incorrectly, it answers incorrectly in a spectularly wrong way (it hallunincates).

Exactly capture known dynamics of a system. While Machine Learning models have been increasing been improving at "learning" the dynamics of real world systems using Neural Nets - why not model this phenomina extactly in. Using prexisting mathematical frameworks allows the utilisation of hundreds of years of theory and results. 

We could for example calculate the expected number of cases of influensa. We could look at the 95% credible interval of the cases, or adjust the R0 (the expected number of additional cases per infection) and see the effect on the system. If we had trained a Neural Network on this task while we would be able to calculate the expected cases and all statistics in the base senario, we would struggle to consider alternative dynamics without training data. We could for example trying training a machine learning model with a number of cases time series and R0, but without a full range of time series over R0 values, the model will not learn the underlying relationship between the infection dynamics and the R0 of a diease.


The best of both worlds: use a mathematical model to model out interactions between different classes, we can define the boundaries of our model, our assumptions ect, ensuring that we have a rigourous foundation for our model. We then apply a machine learning technique(s) to learn the model parameters. This is a common mathematical modelling approach, however, the integration between the mathematical model and the newest of machine learning algorithm isn't as tightly coupled (e.g. neural networks that have the model as a final layer).

Compute, training large neural networks is expensive, if we know some model parameters exactly, we can use them. We don't have to put all model inputs into a neural network and model these already known relations. Note, we could still use a neural network to only train the required model parameters, this is a critque of only using a neural network to model the whole system dynamics.