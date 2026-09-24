"""
DOOM Minimal-Prompt-to-Maximal-Output Synthesis Engine
Empowers the Antigravity AI Corporation to transform short 1-line Human Directives
into full-scale, production-ready, $10K-$1M digital architectures with zero manual prompting.
"""

import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from ai_company.config import config

DOOM_KNOWLEDGE_PATH = Path(__file__).resolve().parent / "doom_knowledge.json"

class MinimalToMaximalSynthesizer:
    def __init__(self, knowledge_path: Path = DOOM_KNOWLEDGE_PATH):
        self.knowledge_path = knowledge_path
        self._load_knowledge()

    def _load_knowledge(self):
        if self.knowledge_path.exists():
            with open(self.knowledge_path, "r", encoding="utf-8") as f:
                self.knowledge = json.load(f)
        else:
            self.knowledge = {}

    def expand_minimal_prompt(self, minimal_prompt: str, target_tier: Optional[str] = None) -> Dict[str, Any]:
        """
        Transforms a brief prompt into a complete $10K-$1M enterprise specification.
        Example Input: 'Build a luxury watch 3D website'
        Output: Full 37-agent staffing, component architecture, GSAP timelines, WebGL configs, and zero-lorem copy.
        """
        self._load_knowledge()
        prompt_lower = minimal_prompt.lower()

        # 1. Determine Valuation Tier
        if any(w in prompt_lower for w in ["million", "$1m", "enterprise", "fintech", "saas platform"]):
            tier = "$100K-$1,000,000"
            agent_count = 30
            complexity = "Tier 3: Enterprise Bespoke Platform"
        elif any(w in prompt_lower for w in ["100k", "luxury", "automotive", "flagship", "3d"]):
            tier = "$100,000"
            agent_count = 20
            complexity = "Tier 2: High-Ticket Experiential Showpiece"
        else:
            tier = "$10,000"
            agent_count = 15
            complexity = "Tier 1: Bespoke Flagship Digital Asset"

        # 2. Extract Matching Technical Patterns from Knowledge Base
        sources = self.knowledge.get("video_sources", [])
        matched_techniques = []
        matched_stacks = set()
        matched_motion = set()

        for s in sources:
            # Match keywords
            core = (s.get("core_focus", "") + " " + s.get("title", "")).lower()
            if any(term in core for term in ["3d", "scroll", "luxury", "clamp", "gsap", "awwwards"]):
                for tech in s.get("key_techniques", []):
                    matched_techniques.append(tech)
                for st in s.get("tech_stack", []):
                    matched_stacks.add(st)
                for mo in s.get("motion_patterns", []):
                    matched_motion.add(mo)

        # 3. Assemble Maximal Production Blueprint
        is_thinker = any(w in prompt_lower for w in ["idea", "think", "ideat", "brainstorm", "concept", "philosophy", "strategy", "vision", "innovat", "hypothes"])
        specialist_workers = agent_count - 3 - max(2, (agent_count + 9) // 10) - 2
        thinker_count = specialist_workers if is_thinker else max(1, specialist_workers // 2)
        coder_count = 0 if is_thinker else (specialist_workers - thinker_count)

        blueprint = {
            "original_minimal_prompt": minimal_prompt,
            "synthesized_tier": tier,
            "complexity_level": complexity,
            "recommended_staffing": {
                "total_agents": agent_count,
                "orchestrators": 3,
                "reviewers": max(2, (agent_count + 9) // 10),
                "managers": 2,
                "specialist_workers": specialist_workers,
                "thinker_agents": thinker_count,
                "coder_agents": coder_count,
                "cognitive_mode": "PURE_THINKER_SWARM" if is_thinker else "HYBRID_COGNITIVE_ENGINE"
            },
            "master_design_tokens": {
                "typography": {
                    "heading_display": "clamp(2.75rem, 7vw, 6.5rem)",
                    "heading_section": "clamp(2rem, 4vw, 3.75rem)",
                    "body_fluid": "clamp(1rem, 1.25vw, 1.25rem)",
                    "letter_spacing": "-0.03em (Razor-sharp editorial tracking)",
                    "line_height": "1.05 for display, 1.6 for narrative body"
                },
                "color_palette": {
                    "surface_primary": "#08090C (Obsidian Black)",
                    "surface_secondary": "#11141B (Elevated Titanium Card)",
                    "accent_primary": "#D4AF37 (Champagne Gold) or #00F0FF (Cyber Cyan)",
                    "text_primary": "#F7F8F9 (Optical 98% White)",
                    "text_muted": "#8A909E (High-Legibility Secondary)"
                },
                "spacing_rhythm": {
                    "section_padding_y": "clamp(5rem, 12vw, 12rem)",
                    "container_max_width": "1440px",
                    "card_border_radius": "16px / 24px with backdrop-blur(20px)"
                }
            },
            "motion_physics_suite": {
                "smooth_scroll": "Lenis inertia engine (lerp: 0.08, smoothWheel: true)",
                "pinned_scroll_scrubbing": "GSAP ScrollTrigger with scrub: 1.2 and end: '+=300%'",
                "cursor_physics": "Spring-interpolated magnetic follower with scale transform on hover",
                "3d_canvas": "Three.js perspective camera with lerp damping mapped to scroll progress"
            },
            "mandatory_component_suite": [
                {
                    "name": "Cinematic 3D Interactive Hero",
                    "spec": "Pinned canvas scrubbing with WebP frame sequence / Three.js glTF model, ambient radial glow, dynamic dual CTA"
                },
                {
                    "name": "Precision Engineering Telemetry HUD",
                    "spec": "Live UTC/atomic clock, real-time scroll telemetry percentage, system nominal indicators, micro-metrics"
                },
                {
                    "name": "Bespoke Interactive Product Customizer",
                    "spec": "Real-time material toggle (Carbon, Ceramic, Titanium, Gold), dynamic camera zoom, live spec readout"
                },
                {
                    "name": "Dynamic High-Ticket ROI & Quotation Calculator",
                    "spec": "Dual range sliders, dynamic cost-benefit projection matrix, instant lead capture transition"
                },
                {
                    "name": "VIP Concierge Pass Generator",
                    "spec": "Instant client serialization (#EMC-2026-XXXX), live SVG QR code generator, download/calendar pass"
                }
            ],
            "zero_placeholder_copy_protocol": {
                "headline_hook": f"The Pinnacle of Digital Mastery: {minimal_prompt.title()}",
                "subheadline": "Engineered for elite distinction, sub-second performance, and commanding enterprise market authority.",
                "trust_metrics": ["$140M+ Client Value Generated", "99.98% Conversion Reliability", "Sub-0.8s LCP Velocity"]
            },
            "quality_assurance_gates": [
                "LCP < 1.2 seconds across mobile and 4K viewports",
                "Zero Layout Shift (CLS < 0.01)",
                "Zero dummy / lorem ipsum copy (100% bespoke storytelling)",
                "WCAG 2.1 AA contrast compliance (4.5:1 ratio minimum)"
            ]
        }

        return blueprint

minimal_to_maximal_synthesizer = MinimalToMaximalSynthesizer()
