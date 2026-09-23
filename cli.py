"""
Command-Line Interface for AI Company
Providing terminal-based operations for the Human Owner and company operators.
"""

import argparse
import sys
import json
import uvicorn
from ai_company.core import company
from ai_company.config import config

def main():
    parser = argparse.ArgumentParser(description="Antigravity AI Corporation - Autonomous Executive CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available corporate commands")

    # Command: status
    subparsers.add_parser("status", help="Display corporate health, workforce count, and active projects")

    # Command: submit
    submit_parser = subparsers.add_parser("submit", help="Submit a new Human Objective")
    submit_parser.add_argument("prompt", type=str, help="Raw directive from the Human Owner")
    submit_parser.add_argument("--agents", type=int, default=None, help="Explicit agent headcount (Section 9)")
    submit_parser.add_argument("--novel", action="store_true", help="Trigger Section 23 New Capability Council")
    submit_parser.add_argument("--complexity", type=int, default=1, help="Complexity factor for elastic scaling")

    # Command: review
    review_parser = subparsers.add_parser("review", help="Review project deliverables (Accept or Reject/Revise)")
    review_parser.add_argument("project_id", type=str, help="Target Project ID")
    group = review_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--accept", action="store_true", help="Accept deliverables and dissolve project")
    group.add_argument("--reject", action="store_true", help="Reject deliverables and request revisions")
    review_parser.add_argument("--feedback", type=str, default="", help="Revision feedback for the project team")

    # Command: model
    model_parser = subparsers.add_parser("model", help="Switch global company model across all tiers")
    model_parser.add_argument("model_name", type=str, help="Model name (e.g. gemini-2.5-flash, gemini-3.8-flash)")

    # Command: web
    web_parser = subparsers.add_parser("web", help="Launch the Executive Command Center Web Dashboard")
    web_parser.add_argument("--host", type=str, default="127.0.0.1", help="Host address")
    web_parser.add_argument("--port", type=int, default=8000, help="Port number")

    args = parser.parse_args()

    if args.command == "status":
        st = company.get_status()
        print("\n=== ANTIGRAVITY AI CORPORATION — OPERATIONAL STATUS ===")
        print(f"Supreme Authority:           HUMAN OWNER")
        print(f"Executive Intelligence:      CEO PRIME")
        print(f"Active Global Model:         {st['active_model']}")
        print(f"Evolutionary Stage:          {st['evolution_stage']}")
        print(f"Total Agents Spawned:        {st['total_agents_spawned']}")
        print(f"Total Projects Completed:    {st['total_projects_completed']}")
        print(f"Active Project Orgs:         {st['active_projects_count']}")
        print(f"Clarification Council:       {st['council_seats_count']} Seats Active")
        print("=======================================================\n")

    elif args.command == "submit":
        print(f"\n[HUMAN DISPATCH] Submitting Objective: '{args.prompt[:80]}...'")
        res = company.submit_objective(
            raw_prompt=args.prompt,
            explicit_agent_count=args.agents,
            force_new_capability=args.novel,
            complexity_score=args.complexity
        )
        print("\n=== PROJECT DELIVERED TO HUMAN OWNER ===")
        print(f"Project ID:            {res['project_id']} ({res['project_name']})")
        print(f"CEO Intent:            {res['ceo_intent']}")
        print(f"Council Consensus:     {res['council_consensus']} (Deadlock Breaker: {res['senior_leader_ruled']})")
        print(f"DOOM Workforce:        {res['staffing']['total_agents']} total agents")
        print(f"                       - {res['staffing']['orchestrators']} Orchestrators (Tri-Council)")
        print(f"                       - {res['staffing']['reviewers']} Reviewers (1:10 ratio)")
        print(f"                       - {res['staffing']['managers']} Managers")
        print(f"                       - {res['staffing']['workers']} Workers / Coders")
        print(f"Tri-Orch Signoff:      {res['tri_orchestrator_certified']}")
        print(f"\nStatus:                {res['status']}")
        print(f"Next Action:           Run 'python -m ai_company review {res['project_id']} --accept' or '--reject'")
        print("=========================================\n")

    elif args.command == "review":
        res = company.review_deliverables(
            project_id=args.project_id,
            accept=args.accept,
            feedback=args.feedback
        )
        print(f"\n[HUMAN VERDICT]: {json.dumps(res, indent=2)}\n")

    elif args.command == "model":
        res = company.switch_global_model(args.model_name)
        print(f"\n[GLOBAL MODEL TRANSITION]: {res['message']}\n")

    elif args.command == "web":
        print(f"\nLaunching AI Company Executive Command Center on http://{args.host}:{args.port} ...")
        uvicorn.run("ai_company.web.server:app", host=args.host, port=args.port, reload=False)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
