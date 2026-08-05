---
name: image-prompt-batch
description: Use when producing many image-generation prompts, shot lists, style variants, product scenes, model or lifestyle prompt sets, or CSV-ready prompt batches for image tools.
---

# Image Prompt Batch

## Overview

Use this skill to generate consistent batches of image prompts for product, ecommerce, advertising, social, editorial, or concept workflows. Optimize for repeatability: each prompt should carry the same core product facts while varying only the intended dimension.

## Workflow

1. Confirm product or subject facts, brand constraints, target platform, aspect ratio, output count, style boundaries, and required exclusions.
2. Define a prompt schema before writing the batch: subject, composition, environment, lighting, camera, materials, action, mood, text/callouts, and negative constraints.
3. Build a variation matrix for scenes, angles, demographics, seasons, colorways, use cases, or ad concepts.
4. Generate prompts in a table or CSV-ready format with stable IDs and filenames.
5. Review for duplicate concepts, conflicting instructions, unsafe claims, and product inaccuracies.

## Output Columns

Prefer these columns unless the user asks otherwise:

- `id`
- `filename`
- `prompt`
- `negative_prompt`
- `aspect_ratio`
- `style`
- `scene_type`
- `notes`

## Guardrails

Do not imitate a living artist's exact style. Do not include real logos, celebrities, private people, or protected brand assets unless the user has rights and explicitly asks. Preserve product facts such as size, material, color, and included accessories.
