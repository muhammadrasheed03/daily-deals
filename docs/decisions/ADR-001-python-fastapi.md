# ADR-001: Python + FastAPI as primary backend language and framework

## Status
Accepted

## Context
Daily Deals is a website with the primary goal of saving the user as much money as possible. The way it does this is by the client (user) choosing which products they would like to track, and what prices are target for them. Then, there will be a live scraper running on intervals checking for price changes, and will alert the user if it crosses the threshold. The difficulties will be maintaining concurrency and preventing race conditions especially when a large amount of users are actively using the site.


## Decision
I have chosen to use Python as the backend language due to its versatility as well as it asynchronous support. Python is a language with extensive documentation and a plethora of online tutorials. In addition, FastAPI provides us with the asynchronous first demand needed for our service which will have multiple concurrent scrapes, users, etc.


## Consequences
With the usage and implementation of both FastAPI and Python, I will know how to build microservices such as those on daily deals with ease for my internship with Spectrum in the upcoming summer. In addition, this conceptual knowledge can be extended onto multiple frameworks and facets. Python is slower at raw execution than compiled languages like Go or Java, which is a real tradeoff worth noting in a professional document.