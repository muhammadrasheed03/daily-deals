# ADR-002: SQLAlchemy ORM over raw SQL

## Status
Accepted

## Context 
Daily Deals needs to be able to store product data even after server shutoffs or unplanned problems. We had the option of using either raw SQL or using the SQLAlchemy ORM library to store our data, we went with the latter

## Decision 
The reason we went with SQLAlchemy is because an ORM is kind of like a translator tool. In essence, we can write our database queries in standard python in contrast to the syntax heavy identical raw SQL calls.

## Consequences 
The format is much more familiar and requires creating less code, as we can create modular design for our tabular operations. But, SQLAlchemy adds a layer of abstraction meaning it takes slightly more setup, and we will need to drop back down to raw SQL for complex queries. 