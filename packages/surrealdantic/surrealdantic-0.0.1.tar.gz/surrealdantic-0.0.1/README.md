# SurrealDantic

## Overview

This repository hosts a cutting-edge web application framework designed to harness the full potential of SurrealDB. Our framework integrates robust REST API generation, real-time data streaming using Server-Sent Events (SSE), and advanced computational functionalities including vector embeddings and cosine similarity analysis. This innovative approach positions the framework as a pioneering solution in the realm of modern web applications, particularly for those requiring real-time data handling and complex data interactions.

## Features

**AutoAPI**: Automates REST API creation for various data models, ensuring rapid development and deployment.
**Controller and Repository Pattern**: Streamlines CRUD operations with SurrealDB, abstracting database complexities.
**Real-Time Data Streaming**: Utilizes SSE for live data updates, ideal for applications requiring instant data refresh like dashboards.
**Vector Embedding Support**: Advanced handling of vector embeddings with built-in cosine similarity calculations, catering to applications in machine learning and data analysis.
**Asynchronous Processing**: Decorators async_cpu and async_io for efficient handling of CPU-bound and I/O-bound operations.
**Robust Error Handling**: A robust decorator enhances functions with sophisticated error handling and retry mechanisms.
**Pydantic Integration**: Leverages Pydantic for robust data validation and serialization, ensuring data integrity and security.

## Getting Started

> Prerequisites

* Python 3.8+
* SurrealDB `docker pull surrealdb/surrealdb:latest`

> Installation

```bash
pip install surrealdantic
```

> Usage

```python
from surrealdantic import AutoAPI, Embedding

# Initialize AutoAPI
api = AutoAPI()

# add the Embedding model
api.add(Embedding,Embedding)

# run the API

```bash
uvicorn main:api --reload
```