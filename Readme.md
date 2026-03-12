# ComfyUI Content Factory

**Autonomous AI content pipeline powered by ComfyUI — generates consistent characters, pose-controlled scenes, and production-ready video assets at scale.**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![ComfyUI](https://img.shields.io/badge/ComfyUI-Powered-blue?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyTDIgN2wxMCA1IDEwLTVMMTIgMnptMCA3LjVMMiA0LjVWMTdsMTAgNSAxMC01VjQuNUwxMiA5LjV6Ii8+PC9zdmc+)](https://github.com/comfyanonymous/ComfyUI)
[![ControlNet](https://img.shields.io/badge/ControlNet-v1.1-orange)](https://github.com/lllyasviel/ControlNet)
[![IPAdapter](https://img.shields.io/badge/IPAdapter-Face_Consistency-purple)](https://github.com/cubiq/ComfyUI_IPAdapter_plus)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## The Problem

Creating consistent short-form video content at scale requires:
- **Same character** appearing identically across dozens of scenes
- **Pose-controlled** shot sequences (wide → medium → closeup)
- **Role-appropriate** scripts for each character archetype
- **Batch production** with full traceability

Doing this manually in ComfyUI is slow, error-prone, and impossible to scale.

## The Solution

ComfyUI Content Factory automates the entire pipeline:

```
Seed Template → Unlimited Variants → Character (ControlNet + LoRA + IPAdapter)
→ Script → Pose-Controlled Scenes → Manifest + Assets → Execution Logs
```

One command. Hundreds of consistent, production-ready content packages.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│               COMFYUI CONTENT FACTORY                    │
├─────────────┬──────────────┬────────────────────────────┤
│  Template   │  Character   │  Scene Sequencer           │
│  Engine     │  System      │  (ControlNet Poses)        │
│             │              │                            │
│  Unlimited  │  7 Types:    │  Shot Types:               │
│  variants   │  - Trainer   │  - Wide / Medium / Close   │
│  from seed  │  - Chef      │  - Over-shoulder / Split   │
│  topics     │  - Influencer│                            │
│             │  - Mascot    │  Pose Control:             │
│  3 niches:  │  - Coach     │  - OpenPose                │
│  fitness    │  - Baker     │  - Depth                   │
│  cooking    │  - Robot     │  - IP2P                    │
│  tech       │              │                            │
├─────────────┴──────────────┴────────────────────────────┤
│                    ComfyUI Backend                      │
│  SDXL + Multi-LoRA + ControlNet v1.1 + IPAdapter        │
├─────────────────────────────────────────────────────────┤
│                    Output Layer                         │
│  Manifests + Scripts + Assets + Execution Logs          │
└─────────────────────────────────────────────────────────┘
```

## Key Features

### Character Consistency (IPAdapter)
Each character is generated once, then its reference image is cached and fed back via IPAdapter for every subsequent scene — ensuring the same face, style, and identity across all outputs.

### Pose-Controlled Scenes (ControlNet)
Scene sequences follow cinematographic patterns. Each scene type maps to a specific ControlNet pose:

| Scene Type | Shot | Pose | ControlNet Model |
|-----------|------|------|-----------------|
| `intro` | Wide | Standing confident | OpenPose |
| `demo` | Medium | Demonstrating | OpenPose |
| `cta` | Closeup | Pointing at camera | OpenPose |
| `problem` | Medium | Thinking gesture | Depth |
| `solution` | Over-shoulder | Teaching | Depth |
| `hook` | Extreme closeup | Intense gaze | OpenPose |

### Multi-LoRA Stacking
Characters can use up to 2 LoRA models simultaneously — one for base style (realism, cartoon, sci-fi) and one for pose/action refinement.

### Batch Factory
```python
factory.run_factory(batch_size=50, topics=["fitness", "cooking", "tech"])
```
Processes up to 50 variants per topic with automatic resource monitoring (memory + execution time guards).

---

## Quick Start

### 1. Prerequisites

```bash
# ComfyUI with custom nodes
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI && pip install -r requirements.txt

# Required custom nodes (install via ComfyUI-Manager)
# - ControlNet Auxiliary Preprocessors
# - ComfyUI_IPAdapter_plus
```

### 2. Download Models

Place in your ComfyUI `models/` directory:

```
ComfyUI/models/
├── checkpoints/
│   └── sd_xl_base_1.0.safetensors
├── controlnet/
│   ├── control_v11p_sd15_openpose.pth
│   ├── control_v11f1p_sd15_depth.pth
│   └── control_v11e_sd15_ip2p.pth
└── loras/
    └── (optional style LoRAs)
```

### 3. Start ComfyUI

```bash
cd ComfyUI
python main.py --listen 127.0.0.1 --port 8188
```

### 4. Run the Factory

```bash
# Install dependencies
pip install -r requirements.txt

# Run
python main_phase.py
```

---

## Usage

### Single Character Test

```python
from main_phase import ContentFactory

factory = ContentFactory()

template = {
    "topic": "fitness",
    "niche": "gym training",
    "objective": "motivational",
    "preferred_role": "trainer",
    "seed_template_id": "fitness_v001"
}

result = factory.execute_complete_template_debug(template, "TEST001")
```

### Full Batch Production

```python
factory = ContentFactory()
factory.run_factory(batch_size=10, topics=["fitness", "cooking", "tech"])
```

### Generate Unlimited Template Variants

```python
templates = factory.create_unlimited_variants("fitness", count=100)
# Returns 100 unique template combinations across niches, objectives, and roles
```

---

## Output Structure

Each variant produces a complete content package:

```
outputs/fit0001/
├── manifest.json          # Full asset manifest with checksums
└── script.txt             # Role-specific short-form video script

assets/
├── characters/c1a2b3c4.png   # Character sheet (cached for IPAdapter)
├── scenes/sintro_5e6f.png    # Pose-controlled scene frames
└── reference/c1a2b3c4_ref.png # IPAdapter reference image

logs/
└── executions.json        # Full execution trace
```

### Manifest Format

```json
{
  "seed_template_id": "fitness_v001",
  "variant_id": "fit0001",
  "character": {
    "character_id": "c1a2b3c4",
    "type": "human_authority",
    "role": "trainer",
    "controlnet_model": "control_v11p_sd15_openpose.pth",
    "ipadapter_weight": 0.85
  },
  "scenes": [
    {"scene_id": "sintro_5e6f", "pose": "standing_confident"},
    {"scene_id": "sdemo_7g8h", "pose": "demonstrating"},
    {"scene_id": "scta_9i0j", "pose": "pointing_camera"}
  ],
  "pipeline": "ControlNet+IPAdapter+MultiLoRA",
  "generated_at": "2026-01-27T20:43:09Z"
}
```

### Execution Log (Traceability)

Every run is logged with 6 required fields:

```json
{
  "seed_template_id": "fitness_v001",
  "variant_id": "fit0001",
  "character_id": "c1a2b3c4",
  "character_type": "human_authority",
  "character_role": "trainer",
  "scene_identifiers": ["sintro_5e6f", "sdemo_7g8h", "scta_9i0j"]
}
```

---

## Project Structure

```
comfyui-content-factory/
├── main_phase.py           # Core factory engine
├── comfy_client.py         # ComfyUI WebSocket/API client
├── check_comfy.py          # Connection diagnostics
├── list_models.py          # Model inventory utility
├── requirements.txt        # Python dependencies
├── workflows/              # ComfyUI JSON workflows
│   ├── character_production.json
│   ├── character_controlnet.json
│   ├── character_gen_api.json
│   └── scene_compose_api.json
├── templates/              # Seed templates
├── assets/                 # Generated assets (gitignored)
├── outputs/                # Content packages (gitignored)
└── logs/                   # Execution traces (gitignored)
```

---

## How It Works

1. **Template Engine** — Takes a topic (fitness, cooking, tech) and generates unlimited variant configurations by combining niches, objectives, roles, and video structures.

2. **Character System** — Selects one of 7 character archetypes based on topic + objective. Each archetype specifies its own LoRA stack, ControlNet model, and IPAdapter weight.

3. **Script Generator** — Produces short-form video scripts tailored to the character's role (a trainer motivates, a chef demonstrates, an expert analyzes).

4. **Scene Sequencer** — Maps video structure (intro → demo → CTA) to cinematographic shots with ControlNet pose specifications.

5. **ComfyUI Execution** — Builds and submits complete SDXL workflows with ControlNet + IPAdapter + Multi-LoRA, polls for results, saves assets with checksums.

6. **Logging** — Every execution is traced with template ID, variant ID, character details, and scene identifiers for full reproducibility.

---

## Resource Guards

The factory includes built-in safety limits:

| Guard | Default | Purpose |
|-------|---------|---------|
| `MAX_BATCH_SIZE` | 50 | Prevents runaway batch jobs |
| `MAX_MEMORY_MB` | 16,000 | Stops before OOM crashes |
| `MAX_EXEC_TIME_SEC` | 600 | 10-minute execution ceiling |

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `ComfyUI_ERROR_404` | Start ComfyUI: `python main.py --listen 127.0.0.1 --port 8188` |
| `timeout_60s` | Download `sd_xl_base_1.0.safetensors` to `ComfyUI/models/checkpoints/` |
| `No_prompt_id` | Install missing custom nodes via ComfyUI-Manager |
| `ConnectionError` | ComfyUI not running on port 8188 |

Run `python check_comfy.py` to diagnose connection issues.

---

## Requirements

- Python 3.10+
- ComfyUI (with ControlNet + IPAdapter nodes)
- SDXL base model
- GPU with 8GB+ VRAM (recommended)

---

## License

MIT

---

## Contributing

Contributions are welcome. Please open an issue first to discuss proposed changes.
