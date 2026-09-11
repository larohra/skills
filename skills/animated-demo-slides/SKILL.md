---
name: animated-demo-slides
description: Create polished animated SVG-based slide presentations to communicate technical ideas clearly. Use this whenever engineers, PMs, or technical leads need to explain complex systems, data flows, performance concepts, architecture decisions, or any technical topic where a visual walkthrough would help non-native English speakers or audiences unfamiliar with the domain understand the key concepts. Perfect for demos, design reviews, technical interviews, and cross-functional presentations where clarity and visual impact matter.
compatibility: null
---

# Animated Demo Slides

Build beautiful, animated slide presentations using SVG graphics and smooth transitions. This skill helps technical professionals communicate complex ideas through a series of clean, easy-to-follow visual slides in a standalone HTML file.

## When to Use This Skill

You want to create this skill when:
- Explaining system architecture, data flows, or performance concepts
- Building a demo for a design review, technical interview, or all-hands meeting
- Creating a visual walkthrough of how something works (especially useful for audiences with varying English fluency)
- You have a clear idea of what you want to show but need help turning it into polished visuals

## How It Works

The skill uses **interactive refinement** to help you build the perfect presentation. Here's the flow:

1. **Describe your concept** in plain text — what's the main idea or narrative you want to tell?
2. **Guided questions** help clarify: What are the key steps/states? What data or metrics matter? What should each slide focus on?
3. **SVG slide generation** — the skill creates clean, animated SVGs for each concept
4. **HTML framework** — all slides are bundled into a beautiful, interactive HTML file with keyboard navigation
5. **Refinement cycles** — you review each slide and request changes (animation style, layout, data representation, etc.) until it matches your vision

## What You'll Get

A standalone HTML file with:
- **Keyboard navigation** — arrow keys to browse slides, keyboard shortcuts for help
- **Clean dark theme** — professional GitHub-inspired design that works for tech audiences
- **Animated SVGs** — smooth transitions and visual storytelling (e.g., bars filling, connections lighting up)
- **Accessible layout** — readable fonts, high contrast, full-screen capable
- **No external dependencies** — everything is self-contained in one file

## Getting Started

Tell the skill:
1. **What topic** you're explaining (e.g., "connection pool behavior", "database query optimization", "API architecture")
2. **What story** you want to tell (e.g., "healthy state → degraded state → recovery with monitoring")
3. **Any metrics or data** that should appear (numbers, percentages, state changes)

The skill will ask clarifying questions about:
- How many slides you envision
- What each slide should highlight
- Whether animations should be simple (fade-in) or more complex (data flowing, states changing)
- The narrative flow and transitions between concepts

## Iteration Process

After generating your first draft:
- Review each slide in the HTML file
- Provide feedback like: "Make the numbers bigger", "Add a green glow when it's healthy", "Slow down the animation", "This slide is confusing, show the state change differently"
- The skill will regenerate with refinements

This typically takes 2–5 iterations per slide to get the vision right (that's normal — go with it).

## Tips for Best Results

- **Be specific with your description.** Don't just say "show database performance" — say "I want to show 100 database connections with 50 currently busy (green), 40 idle (dark), and 10 waiting (red)"
- **Explain the narrative arc.** What's the problem → what's the solution → why does it matter?
- **Give feedback in plain language.** You don't need to know SVG syntax. Say "the bars should animate upward" and let the skill handle the technical details.
- **Iterate on what matters.** If a slide doesn't feel right, describe what's wrong and keep refining

## Output Details

- **File format:** Single `.html` file (all SVGs embedded as base64)
- **File size:** Typically 100KB–500KB depending on slide complexity
- **Browser support:** Any modern browser (Chrome, Firefox, Safari, Edge)
- **Interactivity:** View fullscreen (F key), navigate with arrow keys or side buttons
- **Customization:** You can edit the HTML directly if needed (all SVGs are embedded for easy access)

## Example Use Cases

**Performance Metrics Talk:** "Show how a connection pool starts healthy with 50/100 pipes busy, then becomes saturated when all 100 are in use, then how monitoring helps recovery"

**Architecture Walkthrough:** "Diagram an API request flowing through load balancer → service mesh → database, showing where bottlenecks can happen"

**Feature Explain:** "Walk through the steps of a user authentication flow with visual indicators for success/failure states"

**Incident Postmortem:** "Show timeline of an outage: normal operation → anomaly detection → alerting → human response → recovery"
