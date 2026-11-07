---
layout: layouts/digital.njk
title: Social & Blog Content Bot Kit
description: Drop-in GitHub Actions bots that auto-post your products to Instagram, Facebook and a blog on a schedule — AI-written captions, real tested Python code, free API tier. Instant download, AED 99 / $27.
priceUsd: 27
priceAed: 99
cover: /img/social-blog-bot-kit.webp
cover_alt: Social & Blog Content Bot Kit — automation code pack cover
category: automation
sku: LMK-005
author: LEEBLAAB
digitalFormat: Python + YAML + PDF guides
buyUrl: 'mailto:nillianstore@gmail.com?subject=Social %26 Blog Content Bot Kit&body=Hi, I would like to order the digital product "Social & Blog Content Bot Kit" from nillianstore.com (AED 99 / $27). Please send me the payment instructions and file delivery details.'
tags:
  - social media automation
  - instagram auto posting
  - github actions
  - ai content
  - blog automation
permalink: /digital/social-blog-bot-kit/
date: 2026-11-07
bullet_points:
  - "Instagram + Facebook auto-posting every N hours — single image or carousel up to 10, captions and hashtags written by AI (Groq Llama 3.3 70B, free API tier) reading your product's own title/description/price"
  - "Weekly SEO blog post generated from any product page into Eleventy-compatible markdown — keeps your site fresh without lifting a finger"
  - "Real tested production source code (Python + GitHub Actions YAML), not PDF blueprints or JSON imports — the same system that runs a live UAE store"
  - "Setup guide walks through the 4 secrets, Meta token permissions and error-code troubleshooting (token expiry 190, missing secrets, cron not firing); DRY_RUN mode to test before going live"
---

## What you get

A buyer-runnable automation pack you drop into your own GitHub repo:

- `social_bot.py` + `blog_bot.py` — genericized, de-branded production scripts with a BRAND CONFIG block (store name, audience, tone) you edit once
- Two GitHub Actions workflows (`social_bot.yml`, `blog_bot.yml`) — schedule-driven, site-agnostic, with an optional pre-post site-build block
- `SETUP_GUIDE.pdf` / `.md` — secrets schema (`GROQ_API_KEY`, `META_ACCESS_TOKEN`, `FB_PAGE_ID`, `IG_USER_ID`), Meta Graph API v18.0 permissions walkthrough
- `TROUBLESHOOTING.md` — error-code table with fixes
- 3 sample product files showing the required frontmatter format, plus `config.example.env` and buyer license (LICENSE.txt)

## How it works

Each product is one small markdown file (`title`, `description`, `price`, `cover`, `images[]`, `link`). The bots read those files, ask the AI for copy, deduplicate against a rolling log, and publish to Instagram, Facebook Page and your blog on schedule. That's the whole system — no per-post manual work.

## Who it's for

Store and site owners who want consistent social presence without paying monthly SaaS fees or posting by hand. Works with any static site or product list you can keep in a repo.
