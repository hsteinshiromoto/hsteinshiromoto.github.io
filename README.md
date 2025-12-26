[![CI](https://github.com/hsteinshiromoto/hsteinshiromoto.github.io/actions/workflows/ci.yml/badge.svg)](https://github.com/hsteinshiromoto/tex.beamer/actions/workflows/ci.yml)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/hsteinshiromoto/hsteinshiromoto.github.io?style=flat)
![LICENSE](https://img.shields.io/badge/license-MIT-lightgrey.svg)
[![Jekyll](https://img.shields.io/badge/jekyll-%3E%3D%203.7-blue.svg)](https://jekyllrb.com/)
[![Ruby gem](https://img.shields.io/gem/v/minimal-mistakes-jekyll.svg)](https://rubygems.org/gems/minimal-mistakes-jekyll)
[![Tip Me via PayPal](https://img.shields.io/badge/PayPal-tip%20me-green.svg?logo=paypal)](https://www.paypal.me/hsteinshiromoto)
[![Donate to this project using Buy Me A Coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg)](https://www.buymeacoffee.com/hsteinshiromoto)

# [Humberto STEIN SHIROMOTO](https://hsteinshiromoto.github.io/)

If you enjoy my website, please consider sponsoring:

[!["Buy Me A Coffee"](https://user-images.githubusercontent.com/1376749/120938564-50c59780-c6e1-11eb-814f-22a0399623c5.png)](https://www.buymeacoffee.com/hsteinshiromoto)
 [![Support via PayPal](https://cdn.jsdelivr.net/gh/twolfson/paypal-github-button@1.0.0/dist/button.svg)](https://www.paypal.me/hsteinshiromoto)

This website is built with Jekyll and uses the Minimal Mistakes theme. You can run it locally using Docker.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Quick Start

### Using Docker Compose (Recommended)

1. **Start the development server:**
   ```bash
   docker-compose up
   ```

2. **Access the site:**
   Open your browser to [http://localhost:4000](http://localhost:4000)

3. **Stop the server:**
   Press `Ctrl+C` or run:
   ```bash
   docker-compose down
   ```

### Using Make Commands

Alternatively, you can use the provided Makefile:

```bash
# Build the Docker image
make image

# Pull the latest image from GitHub Container Registry
make pull

# Run the container
make run
```

## Docker Compose Commands

**Build and start (rebuild if Dockerfile changed):**
```bash
docker-compose up --build
```

**Run in background:**
```bash
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f
```

**Access interactive shell:**
```bash
docker-compose exec jekyll zsh
```

**Stop and remove containers:**
```bash
docker-compose down
```

## Development Features

The docker-compose setup includes:
- **Live reload**: Changes to files automatically refresh your browser
- **Incremental builds**: Faster rebuilds with only changed files regenerated
- **Draft posts**: Preview draft posts before publishing
- **Volume mounting**: Edit files on your host machine, changes reflect immediately

## Environment Configuration

Create a `.env` file in the project root to customize settings:

```env
PROJECT_NAME=hsteinshiromoto.github.io
PYTHON_VERSION=3.11.1
JEKYLL_ENV=development
```

## Project Structure

```
.
├── _config.yml           # Jekyll configuration
├── _posts/              # Blog posts (Markdown)
├── _pages/              # Static pages
├── assets/              # Images, CSS, JavaScript
├── python/              # Python utilities
├── Dockerfile           # Docker image definition
├── docker-compose.yml   # Docker Compose configuration
├── Gemfile              # Ruby dependencies
├── package.json         # Node.js dependencies
└── pyproject.toml       # Python dependencies
```

## Deployment

This site is automatically deployed to GitHub Pages via GitHub Actions when changes are pushed to the main branch. The Docker setup is for local development only.

---

# References:

* https://www.cross-validated.com/Personal-website-with-Minimal-Mistakes-Jekyll-Theme-HOWTO-Part-I/
* Icons list: https://gist.github.com/mohamdio/982653e3a8ae35f892f13c5ef0ef9b58
* Post Jupyter notebook: https://www.linode.com/docs/guides/jupyter-notebook-on-jekyll/
* [Instructions on how to make the Masthead navigation bar "sticky"](https://github.com/fortierq/fortierq.github.io/commit/477b98f45c87474484327a55cae185873b6caac0) by [Quentin Fortier](https://github.com/fortierq) → [Example](https://hsteinshiromoto.github.io/)