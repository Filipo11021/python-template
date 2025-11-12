# Python Template

## Getting Started

### Prerequisites

- [UV](https://docs.astral.sh/uv/getting-started/installation/)

### Setup

- Copy `.env.example` to `.env` to create your local env:

  - Linux and Mac `cp .env.example .env`
  - Windows: `copy .env.example .env`

- Install Python using UV:

  ```bash
  uv python install
  ```

- Install dependencies:

  ```bash
  uv sync
  ```

- Apply database migrations:

  ```bash
  poe migrate-apply
  ```

- Start the development server:

  ```bash
  poe dev
  ```

  The backend API documentation will be available at http://127.0.0.1:8000/docs
