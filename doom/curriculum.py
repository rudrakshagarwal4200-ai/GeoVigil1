"""
DOOM Website Engineering Training Curriculum
5 Comprehensive Training Modules based on the 9 YouTube Tutorials and the 37-Agent Website Agency.
"""

from typing import List, Dict, Any
from pydantic import BaseModel
from ai_company.doom.knowledge import WebsiteAgencyKnowledge

class CurriculumLesson(BaseModel):
    lesson_id: str
    title: str
    video_references: List[str]
    core_concepts: List[str]
    practical_exercises: List[str]
    constitutional_checks: List[str]

class CurriculumModule(BaseModel):
    module_id: str
    title: str
    objective: str
    lessons: List[CurriculumLesson]

class DOOMCurriculum:
    """
    Curriculum designed to train DOOM into an elite organizational master
    capable of synthesizing and leading teams that produce $10,000 award-winning websites.
    """

    MODULES: List[CurriculumModule] = [
        CurriculumModule(
            module_id="MOD-01",
            title="The $10K Visual Standard & Luxury Aesthetic Hierarchy",
            objective="Master high-contrast editorial typography, obsidian dark palettes, and zero-template art direction.",
            lessons=[
                CurriculumLesson(
                    lesson_id="L-101",
                    title="Editorial Typography & Typographic Scales",
                    video_references=["snErQUyqwCU", "_PtVROzu3_w"],
                    core_concepts=[
                        "Display serif headlines (Cormorant Garamond / Cinzel) paired with geometric sans (Inter) and mono telemetry (JetBrains Mono)",
                        "Dynamic fluid font sizing using CSS clamp(min, preferred, max)",
                        "High typographic contrast and generous letter-spacing (tracking)",
                        "Hero headline narrative structure eliminating generic marketing copy"
                    ],
                    practical_exercises=[
                        "Define tokens.css with fluid clamp scales for h1-h6 and body",
                        "Audit page for font rendering and optical balance"
                    ],
                    constitutional_checks=[
                        "Ensure agency-design-system and agency-ui-design collaborate",
                        "Verify zero generic fonts (no Comic Sans, Times New Roman, default Arial)"
                    ]
                ),
                CurriculumLesson(
                    lesson_id="L-102",
                    title="Obsidian Palettes & Glassmorphic Elevation",
                    video_references=["_PtVROzu3_w", "h956KTuFKck"],
                    core_concepts=[
                        "Deep obsidian background (#08080A) with charcoal surface layers (#121216)",
                        "Champagne gold (#D4AF37) and emerald (#10B981) precision accents",
                        "Subtle hairline borders (rgba(255,255,255,0.08)) replacing drop shadows",
                        "Sticky navigation with backdrop-filter: blur(20px) and translucent border"
                    ],
                    practical_exercises=[
                        "Synthesize visual token architecture for dark mode luxury layout",
                        "Implement floating glassmorphic nav bar with scroll-depth detection"
                    ],
                    constitutional_checks=[
                        "Verify contrast ratio meets WCAG 2.1 AA (>= 4.5:1 for body)",
                        "Reviewer audits palette uniqueness"
                    ]
                )
            ]
        ),
        CurriculumModule(
            module_id="MOD-02",
            title="3D Canvas Frame-Scrubbing & 60fps Motion Engine",
            objective="Engineer Apple-style pinned canvas frame sequence scrubbers synchronized with scroll.",
            lessons=[
                CurriculumLesson(
                    lesson_id="L-201",
                    title="HTML5 Canvas Sequence Rendering & LERP Interpolation",
                    video_references=["DJMsXSr1jec", "h956KTuFKck"],
                    core_concepts=[
                        "Preloading WebP frame sequences with asynchronous promise pool and progress tracking",
                        "Drawing frames to HTML5 canvas with dynamic DPR scaling and aspect-ratio cover math",
                        "Linear interpolation (LERP) for buttery smooth frame transitions",
                        "RequestAnimationFrame (rAF) render loop avoiding CPU churn when idle"
                    ],
                    practical_exercises=[
                        "Build zero-lag canvas scrubber handling 60 to 180 WebP frames",
                        "Implement cover-fit rendering adapting to window resize and mobile orientations"
                    ],
                    constitutional_checks=[
                        "Enforce agency-interaction role ownership of canvas scrubber",
                        "Verify 60fps framerate under scroll stress test"
                    ]
                ),
                CurriculumLesson(
                    lesson_id="L-202",
                    title="GSAP ScrollTrigger & Lenis Smooth Scrolling Integration",
                    video_references=["DJMsXSr1jec", "nPxMF2YV77I"],
                    core_concepts=[
                        "Pinning hero and showcase sections while scrubbing canvas animation",
                        "Lenis smooth scroll orchestration eliminating mouse-wheel stutter",
                        "Overlaying textual callouts synchronized to exact frame milestones",
                        "Hardware acceleration optimization (will-change: transform)"
                    ],
                    practical_exercises=[
                        "Choreograph multi-milestone product breakdown pinned across 300vh scroll distance",
                        "Synchronize HUD specification cards to frame progression"
                    ],
                    constitutional_checks=[
                        "Cumulative Layout Shift (CLS) verified < 0.05",
                        "Adversarial code review ensures zero memory leaks during sequence loop"
                    ]
                )
            ]
        ),
        CurriculumModule(
            module_id="MOD-03",
            title="Generative AI Asset Pipelines: Whisk, Veo & Google Flow",
            objective="Master prompt engineering and asset orchestration for photorealistic 3D product media.",
            lessons=[
                CurriculumLesson(
                    lesson_id="L-301",
                    title="Multi-Angle Product Consistency & Studio Lighting Prompts",
                    video_references=["nPxMF2YV77I", "GPpYwjMoLio"],
                    core_concepts=[
                        "Studio lighting prompts (rim lighting, 8k octane render, minimalist obsidian podium)",
                        "Consistent reference image conditioning using Google Whisk / Midjourney",
                        "Clean transparent backgrounds / alpha matting for effortless canvas compositing",
                        "Asset optimization down to sub-100kb WebP frames"
                    ],
                    practical_exercises=[
                        "Formulate multi-perspective asset generation prompts for luxury watches / hardware",
                        "Process assets with FFmpeg to generate optimized WebP sequence"
                    ],
                    constitutional_checks=[
                        "Rule 23: Ask Human for data/assets before assuming brand assets",
                        "Visual asset producer validates asset resolution and aspect ratio"
                    ]
                ),
                CurriculumLesson(
                    lesson_id="L-302",
                    title="Turntable & Exploded Orbits via Google Flow / Veo",
                    video_references=["DJMsXSr1jec", "nPxMF2YV77I"],
                    core_concepts=[
                        "Camera orbit prompt formulation (slow 360-degree rotation, smooth turntable)",
                        "Exploded assembly disassembly animation prompts",
                        "Antigravity MCP bridge integration for automated asset generation",
                        "Extracting high-framerate frames from generated video streams"
                    ],
                    practical_exercises=[
                        "Execute Google Flow MCP call to generate 3D product orbit video",
                        "Slice video into 90 WebP frames with zero visual artifacts"
                    ],
                    constitutional_checks=[
                        "Security checks on API keys and credentials",
                        "Reviewer verification of orbit smoothness"
                    ]
                )
            ]
        ),
        CurriculumModule(
            module_id="MOD-04",
            title="High-Conversion Interactive Systems & Zero Dummy Copy",
            objective="Architect bespoke interactive components that drive high-ticket conversions and user trust.",
            lessons=[
                CurriculumLesson(
                    lesson_id="L-401",
                    title="Zero-Dummy Persuasive Microcopy & Storytelling",
                    video_references=["snErQUyqwCU", "h2MjhbwVKLk"],
                    core_concepts=[
                        "Total ban on lorem ipsum and placeholder content",
                        "Direct-response value propositions focused on transformation and prestige",
                        "Social proof integration (verifiable metrics, enterprise badges, customer testimonials)",
                        "Microcopy precision on CTA buttons and status badges"
                    ],
                    practical_exercises=[
                        "Compose full brand narrative and specs for a flagship client product",
                        "Conduct copy resonance audit ensuring tone reflects five-figure valuation"
                    ],
                    constitutional_checks=[
                        "Strict rejection by agency-ruthless-client if placeholder copy is detected",
                        "Verification that all client claims have context"
                    ]
                ),
                CurriculumLesson(
                    lesson_id="L-402",
                    title="Interactive Configurators & VIP Reservation Passes",
                    video_references=["h956KTuFKck", "h2MjhbwVKLk", "GPpYwjMoLio"],
                    core_concepts=[
                        "Dynamic material/finish configurator updating canvas/DOM in real-time",
                        "Interactive pricing and ROI calculators with slider controls",
                        "Instant VIP reservation pass generator with SVG QR code and serial number",
                        "Local state persistence (localStorage) preserving client selections"
                    ],
                    practical_exercises=[
                        "Implement luxury finish configurator updating product visual and pricing HUD",
                        "Build VIP reservation pass modal that saves to localStorage and renders unique QR code"
                    ],
                    constitutional_checks=[
                        "Verify client-side state resilience and input sanitization (OWASP)",
                        "Audit keyboard navigation and focus management in modal dialogs"
                    ]
                )
            ]
        ),
        CurriculumModule(
            module_id="MOD-05",
            title="Autonomous Multi-Agent Agency Orchestration",
            objective="Train DOOM to autonomously synthesize and supervise the 37-agent agency under constitutional rules.",
            lessons=[
                CurriculumLesson(
                    lesson_id="L-501",
                    title="Constitutional Team Staffing & Tri-Orchestrator Allocation",
                    video_references=["VMvZuhcDdnw", "snErQUyqwCU"],
                    core_concepts=[
                        "Constitutional minimum of 10 agents per project strictly enforced",
                        "Exactly 3 Orchestrators: Master (Executive), Design (Creative), Engineering (Technical)",
                        "Supervisory Reviewer ratio locked at 1 per 10 agents (ceil(N/10))",
                        "Zero generic roles: every agent assigned an explicit role from the 37-agent agency taxonomy"
                    ],
                    practical_exercises=[
                        "Calculate staffing for simple (10 agents), intermediate (20 agents), and complex (37 agents) projects",
                        "Map objective requirements to specialized agency departments"
                    ],
                    constitutional_checks=[
                        "Verify Rule 5 (>=10 agents), Rule 6 (3 orchestrators), Rule 7 (1:10 reviewer ratio)",
                        "Verify Rule 23 (Ask Human for data before exploring a new field)"
                    ]
                ),
                CurriculumLesson(
                    lesson_id="L-502",
                    title="Adversarial Quality Gates & Serious Halt Rollback Sentinel",
                    video_references=["VMvZuhcDdnw", "dn6MDl86fRY"],
                    core_concepts=[
                        "Supervisory Reviewers inspect all commits before merge",
                        "Ruthless Client Gatekeeper tests site against original brief and rejects compromises",
                        "Immediate serious halt and rollback if constitutional breach occurs",
                        "Multi-round refinement loop for delivered client projects"
                    ],
                    practical_exercises=[
                        "Simulate reviewer objection and trigger automated remediation",
                        "Execute rollback to last verified clean state upon quality failure"
                    ],
                    constitutional_checks=[
                        "Verify Section 16 serious halt and state rollback mechanics",
                        "Verify Section 19 human rejection reactivates same project team"
                    ]
                )
            ]
        )
    ]

    @classmethod
    def get_all_lessons(cls) -> List[CurriculumLesson]:
        lessons = []
        for m in cls.MODULES:
            lessons.extend(m.lessons)
        return lessons
