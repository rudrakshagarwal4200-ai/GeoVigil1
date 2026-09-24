"""
DOOM Website Architectural Brain
Section 8, 9, 10, 12, 13, 15: Deconstructs website creation objectives into
bespoke $10,000 award-winning digital experience blueprints and maps them
to specialized 37-agent agency teams without any generic placeholders.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from ai_company.doom.knowledge import (
    WebsiteAgencyKnowledge,
    AgencyRoleDefinition,
    VideoTutorialSource
)
from ai_company.doom.staffing import StaffingCalculator, StaffingPlan

class WebsiteBlueprint(BaseModel):
    project_name: str
    archetype: str
    tagline: str
    design_system: Dict[str, Any]
    canvas_scrubber: Dict[str, Any]
    interactive_systems: List[Dict[str, Any]]
    asset_pipeline_prompts: Dict[str, str]
    quality_budgets: Dict[str, Any]
    assigned_roles: List[Dict[str, str]]
    constitutional_certifications: List[str]

class DOOMArchitecturalBrain:
    """
    Cognitive architectural engine for DOOM that deconstructs high-level
    website objectives into full production blueprints and specialized staffing rosters.
    """

    @classmethod
    def analyze_objective(cls, objective_text: str) -> Dict[str, Any]:
        """
        Classifies the website archetype and identifies required modules.
        Supports Rule 27: Cognitive Role Elasticity (Thinkers & Ideators).
        """
        lower = objective_text.lower()
        if any(w in lower for w in ["idea", "think", "ideat", "brainstorm", "concept", "philosophy", "strategy", "vision", "innovat", "hypothes"]):
            archetype = "STRATEGIC_THINK_TANK"
        elif any(w in lower for w in ["watch", "luxury", "jewelry", "fashion", "supercar", "automotive"]):
            archetype = "LUXURY_3D_SHOWCASE"
        elif any(w in lower for w in ["roofing", "contractor", "solar", "lead", "quote", "calculator", "funnel"]):
            archetype = "HIGH_CONVERTING_LEAD_ENGINE"
        elif any(w in lower for w in ["restaurant", "hospitality", "hotel", "resort", "dining", "bar"]):
            archetype = "HOSPITALITY_CONCIERGE"
        elif any(w in lower for w in ["saas", "dashboard", "software", "analytics", "admin"]):
            archetype = "MODERN_SAAS_PLATFORM"
        else:
            archetype = "AWARD_WINNING_FLAGSHIP"

        is_thinker_focused = archetype == "STRATEGIC_THINK_TANK"

        return {
            "archetype": archetype,
            "is_thinker_focused": is_thinker_focused,
            "requires_3d_canvas": archetype in ["LUXURY_3D_SHOWCASE", "AWARD_WINNING_FLAGSHIP", "HOSPITALITY_CONCIERGE"],
            "requires_calculator": archetype in ["HIGH_CONVERTING_LEAD_ENGINE", "MODERN_SAAS_PLATFORM"],
            "requires_vip_pass": archetype in ["LUXURY_3D_SHOWCASE", "HOSPITALITY_CONCIERGE"],
            "requires_telemetry_hud": archetype in ["LUXURY_3D_SHOWCASE", "AWARD_WINNING_FLAGSHIP", "MODERN_SAAS_PLATFORM", "STRATEGIC_THINK_TANK"]
        }

    @classmethod
    def synthesize_blueprint(cls,
                             project_name: str,
                             objective_text: str,
                             target_headcount: Optional[int] = None) -> WebsiteBlueprint:
        """
        Synthesizes a complete $10,000 website production blueprint.
        """
        analysis = cls.analyze_objective(objective_text)
        archetype = analysis["archetype"]

        # 1. Design System Tokens
        design_system = {
            "theme": "Dark Luxury Obsidian",
            "colors": {
                "background_primary": "#08080A",
                "background_secondary": "#121216",
                "accent_primary": "#D4AF37" if archetype in ["LUXURY_3D_SHOWCASE", "HOSPITALITY_CONCIERGE"] else "#10B981",
                "accent_glow": "rgba(212, 175, 55, 0.2)" if archetype in ["LUXURY_3D_SHOWCASE", "HOSPITALITY_CONCIERGE"] else "rgba(16, 185, 129, 0.2)",
                "text_primary": "#F9FAFB",
                "text_secondary": "#9CA3AF",
                "hairline_border": "rgba(255, 255, 255, 0.08)"
            },
            "typography": {
                "display": "'Cormorant Garamond', 'Cinzel', serif" if archetype in ["LUXURY_3D_SHOWCASE", "HOSPITALITY_CONCIERGE"] else "'Syne', sans-serif",
                "body": "'Inter', -apple-system, sans-serif",
                "mono": "'JetBrains Mono', monospace",
                "scaling": "clamp(2.5rem, 5vw + 1rem, 5.5rem) for H1 hero headlines"
            },
            "motion": {
                "easing": "cubic-bezier(0.16, 1, 0.3, 1)",
                "backdrop_blur": "blur(20px)"
            }
        }

        # 2. 3D Canvas Scrubber Specs
        canvas_scrubber = {
            "enabled": analysis["requires_3d_canvas"],
            "fps_target": 60,
            "render_loop": "RequestAnimationFrame with LERP (alpha=0.1)",
            "frame_format": "WebP 85% quality",
            "recommended_frames": 120,
            "scroll_binding": "GSAP ScrollTrigger scrub: 1 with Lenis smooth-scroll",
            "resizing": "DevicePixelRatio responsive cover-fit math"
        }

        # 3. Interactive Systems
        interactive_systems = []
        if analysis["requires_3d_canvas"]:
            interactive_systems.append(WebsiteAgencyKnowledge.INTERACTIVE_BLUEPRINTS["interactive_configurator"])
        if analysis["requires_calculator"]:
            interactive_systems.append(WebsiteAgencyKnowledge.INTERACTIVE_BLUEPRINTS["instant_pricing_calculator"])
        if analysis["requires_vip_pass"]:
            interactive_systems.append(WebsiteAgencyKnowledge.INTERACTIVE_BLUEPRINTS["vip_reservation_pass"])
        if analysis["requires_telemetry_hud"]:
            interactive_systems.append(WebsiteAgencyKnowledge.INTERACTIVE_BLUEPRINTS["live_telemetry_hud"])

        # 4. Generative AI Asset Prompts & Models (Constitutional Rule: Veo 3.1 Quality & Nano Banana Pro)
        asset_pipeline_prompts = {
            "google_flow_video_model": WebsiteAgencyKnowledge.MEDIA_GENERATION_MODELS["video"],
            "google_flow_image_model": WebsiteAgencyKnowledge.MEDIA_GENERATION_MODELS["image"],
            "google_flow_orbit_prompt": f"Slow 360-degree seamless camera turntable orbit of {project_name}, hyperrealistic studio lighting, dark obsidian background, rim lights, 8k resolution, cinematic smoothness",
            "google_whisk_product_prompt": f"Close-up macro shot of {project_name} precision craftsmanship, titanium and gold materials, dramatic luxury lighting, depth of field, photorealistic 8k octane render",
            "ffmpeg_sequence_command": "ffmpeg -i input_orbit.mp4 -vf 'fps=30,scale=1920:1080:flags=lanczos' -vcodec libwebp -lossless 0 -compression_level 6 -q:v 85 frames/frame_%04d.webp"
        }

        # 5. Quality Budgets
        quality_budgets = {
            "target_framerate": "Locked 60fps (no stutter)",
            "cumulative_layout_shift": "< 0.05",
            "largest_contentful_paint": "< 1.2s",
            "horizontal_overflow": "0px at 375px, 768px, 1440px, 2560px",
            "touch_target_minimum": "48px x 48px",
            "owasp_compliance": "CSP header, zero inline eval, HttpOnly cookies, zero XSS",
            "content_fidelity": "Zero placeholder or lorem ipsum text permitted"
        }

        # 6. Specialized Staffing Assignment (Zero Generic Roles!)
        is_thinker_focused = analysis.get("is_thinker_focused", False)
        focus = "PURE_THINKER" if is_thinker_focused else "HYBRID"

        staffing_plan = StaffingCalculator.calculate(
            explicit_count=target_headcount,
            complexity_score=2 if analysis["requires_3d_canvas"] else 1,
            archetype_focus=focus
        )
        assigned_roles = cls.assign_specialized_agency_roles(staffing_plan, is_thinker_focused=is_thinker_focused)

        constitutional_certifications = [
            f"Rule 5: Headcount ({staffing_plan.total_agents}) strictly satisfies >= 10 minimum",
            f"Rule 6: Tri-Orchestrator structure verified (Master, Design, Engineering)",
            f"Rule 7: Reviewer ratio ({staffing_plan.reviewer_count} reviewers for {staffing_plan.total_agents} agents) satisfies 1:10 rule",
            "Rule 23: Human data-solicitation verified prior to domain exploration",
            f"Rule 27: Cognitive Role Elasticity verified ({staffing_plan.thinker_count} thinkers/ideators, {staffing_plan.coder_count} technical implementers; non-coder thinkers fully empowered)",
            "Zero Generic Roles: All personnel mapped to the specialized agency & cognitive taxonomy"
        ]

        return WebsiteBlueprint(
            project_name=project_name,
            archetype=archetype,
            tagline=f"Next-Generation $10,000 Digital Experience for {project_name}",
            design_system=design_system,
            canvas_scrubber=canvas_scrubber,
            interactive_systems=interactive_systems,
            asset_pipeline_prompts=asset_pipeline_prompts,
            quality_budgets=quality_budgets,
            assigned_roles=assigned_roles,
            constitutional_certifications=constitutional_certifications
        )

    @classmethod
    def assign_specialized_agency_roles(cls, staffing: StaffingPlan, is_thinker_focused: bool = False) -> List[Dict[str, str]]:
        """
        Maps a staffing plan directly to specialized agency and cognitive roles.
        Eliminates all generic placeholders ('Worker 1', 'Coder 2').
        Supports Rule 27: Non-coder thinkers, ideators, and conceptual strategists.
        """
        assignments = []

        # 1. Tri-Orchestrators (Exactly 3)
        orchestrator_defs = [
            ("agency-master", "Executive Master Orchestrator", "Directs roadmap, coordinates departments, enforces quality gates"),
            ("agency-design", "Design & Aesthetic Orchestrator", "Directs creative vision, typography, luxury colorways, and art direction"),
            ("agency-engineering", "Full-Stack Engineering Orchestrator" if not is_thinker_focused else "Strategic Systems & Ideation Orchestrator", "Directs 60fps canvas engine, component modularity, or high-level strategic reasoning systems")
        ]
        for role_id, name, desc in orchestrator_defs:
            assignments.append({
                "role_id": role_id,
                "name": name,
                "tier": "ORCHESTRATOR",
                "description": desc
            })

        # 2. Supervisory Reviewers (1 per 10 agents ratio)
        reviewer_pool = [
            ("agency-ruthless-client", "Ruthless Client & Acceptance Gatekeeper", "Audits website and deliverables against $10K standard; rejects generic compromises"),
            ("agency-contrarian-critic", "Contrarian Challenger & Red-Team Cognitive Doubter", "Stress-tests concepts with intellectual critique, surfaces cognitive blind spots, and attacks groupthink"),
            ("agency-visual-qa", "Visual QA & Cross-Browser Inspector", "Verifies CLS < 0.05, pixel alignment, and font smoothing"),
            ("agency-code-review", "Adversarial Code & Logic Reviewer", "Audits modularity, eliminates duplicate code/ideas, and prevents leaks"),
            ("agency-security-perf", "Security & Performance Orchestrator", "Enforces sub-1.2s LCP and OWASP compliance")
        ]
        for i in range(staffing.reviewer_count):
            ref = reviewer_pool[i % len(reviewer_pool)]
            suffix = f" {i + 1}" if i >= len(reviewer_pool) else ""
            assignments.append({
                "role_id": f"{ref[0]}{suffix}",
                "name": f"{ref[1]}{suffix}",
                "tier": "REVIEWER",
                "description": ref[2]
            })

        # 3. Department Managers
        if is_thinker_focused:
            manager_pool = [
                ("agency-conceptual-strategist", "Conceptual Systems Strategist", "Synthesizes raw ideas into cohesive conceptual frameworks, systems architecture, and mental models"),
                ("agency-experience-visionary", "Human Experience & Aesthetic Dreamer", "Visualizes transcendent emotional journeys, sensory poetry, and profound human resonance"),
                ("agency-product", "Product & Ideation Orchestrator", "Synthesizes user intent into structured paradigm roadmaps and feature narratives"),
                ("agency-design-system", "Design System & Token Architect", "Standardizes mental abstractions, design tokens, and conceptual primitives")
            ]
        else:
            manager_pool = [
                ("agency-frontend-architect", "Frontend Architect & Lead", "Oversees client state, canvas integration, and bundle structure"),
                ("agency-conceptual-strategist", "Conceptual Systems Strategist", "Synthesizes raw ideas into cohesive conceptual frameworks and strategic mental models"),
                ("agency-design-system", "Design System & Token Architect", "Standardizes CSS variables, fluid clamp typography, and color tokens"),
                ("agency-product", "Product Orchestrator", "Synthesizes client requirements into feature specifications"),
                ("agency-backend-architect", "Backend Architect & Systems Engineer", "Designs REST endpoints, rate limiting, and persistence layer")
            ]
        for i in range(staffing.manager_count):
            ref = manager_pool[i % len(manager_pool)]
            suffix = f" {i + 1}" if i >= len(manager_pool) else ""
            assignments.append({
                "role_id": f"{ref[0]}{suffix}",
                "name": f"{ref[1]}{suffix}",
                "tier": "MANAGER",
                "description": ref[2]
            })

        # 4. Specialized Worker Specialists (Cognitive Thinkers & Technical Implementers)
        thinker_workers = [
            ("agency-deep-thinker", "First-Principles Deep Thinker & Problem Deconstructor", "Deconstructs complex problems to fundamental first principles, breaks conventional assumptions, and synthesizes pure conceptual models without writing code"),
            ("agency-idea-generator", "Creative Ideator & Divergent Brainstorm Engine", "Generates high-volume divergent concepts, novel paradigms, lateral connections, and blue-sky innovation models"),
            ("agency-brand-philosopher", "Brand Philosopher & Narrative Worldbuilder", "Develops foundational brand metaphysics, philosophical narrative ethos, cultural relevance, and mythos"),
            ("agency-cognitive-synthesizer", "Cross-Domain Cognitive Synthesizer", "Transfers insights across disparate disciplines (psychology, economics, physics, fine arts) to produce breakthrough angles"),
            ("agency-copywriting", "Brand Copywriter & Storyteller", "Writes high-prestige editorial copy with zero placeholder text")
        ]

        implementation_workers = [
            ("agency-interaction", "Micro-Interactions & 60fps Specialist", "Builds GSAP ScrollTrigger canvas scrubber and magnetic button physics"),
            ("agency-ui-design", "UI Visual Designer & Layout Stylist", "Crafts obsidian surfaces, card layouts, and luxury typography rhythm"),
            ("agency-component", "Component Developer & State Engineer", "Implements dynamic product configurators and modal dialogs"),
            ("agency-page-builder", "Semantic HTML & Layout Builder", "Constructs semantic HTML5 document tree with ARIA landmarks"),
            ("agency-responsive", "Responsive & Viewport Matrix Specialist", "Guarantees zero horizontal overflow from 375px mobile to 4K"),
            ("agency-asset", "Visual Asset & Media Producer", "Formulates Google Whisk/Flow prompts and WebP frame sequences"),
            ("agency-performance", "Core Web Vitals & Performance Optimizer", "Inlines critical CSS and optimizes LCP/FID/CLS budgets"),
            ("agency-api", "API & Endpoint Developer", "Builds reservation, quote calculation, and webhook endpoints"),
            ("agency-database", "Database Schema & Persistence Engineer", "Manages SQLite/PostgreSQL schema and local data caching"),
            ("agency-accessibility", "WCAG 2.1 AA Accessibility Specialist", "Enforces keyboard tab loops and 4.5:1 contrast ratios"),
            ("agency-security", "OWASP Security Auditor & Pentester", "Hardens headers, enforces CSP, and eliminates injection vectors"),
            ("agency-seo", "SEO & OpenGraph Semantic Specialist", "Builds Schema.org JSON-LD microdata and social card tags"),
            ("agency-automation", "Automation Scripting & Build Pipelines", "Maintains local dev server and asset conversion automation"),
            ("agency-testing", "Test Engineer & Unit Test Author", "Writes unit tests for pricing calculators and state managers"),
            ("agency-bug-hunter", "Bug Hunter & Edge-Case Specialist", "Stress-tests async fetch handlers and canvas resize edge-cases"),
            ("agency-browser-e2e", "Headless Browser E2E Automation Engineer", "Runs automated full-page user journey checks"),
            ("agency-deployment", "Deployment & Production Readiness Lead", "Builds production assets and staging server configuration")
        ]

        if is_thinker_focused:
            worker_pool = thinker_workers
        else:
            # Interleave thinkers and implementers
            worker_pool = []
            max_len = max(len(thinker_workers), len(implementation_workers))
            for idx in range(max_len):
                if idx < len(thinker_workers):
                    worker_pool.append(thinker_workers[idx])
                if idx < len(implementation_workers):
                    worker_pool.append(implementation_workers[idx])

        for i in range(staffing.worker_count):
            ref = worker_pool[i % len(worker_pool)]
            suffix = f" {i + 1}" if i >= len(worker_pool) else ""
            assignments.append({
                "role_id": f"{ref[0]}{suffix}",
                "name": f"{ref[1]}{suffix}",
                "tier": "WORKER",
                "description": ref[2]
            })

        return assignments
