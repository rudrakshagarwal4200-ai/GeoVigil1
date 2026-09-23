# Google Flow to Antigravity MCP Integration Guide

This directory contains the Model Context Protocol (MCP) server bridge connecting **Google Flow / Google Veo** to **Google Antigravity**.

---

## 1. Overview
When building award-winning $10,000 websites with 3D canvas scrubbers (as featured in Shreyas Raj's Antigravity tutorials), the visual asset pipeline requires:
1. Generating a seamless 360° turntable camera rotation or exploded view of the product via **Google Flow / Veo**.
2. Slicing the generated video into 60–120 high-framerate, lossy-compressed **WebP frames**.
3. Scrubbing those frames across an HTML5 Canvas locked to 60fps via **GSAP ScrollTrigger + Lenis**.

By connecting Google Flow to Antigravity via MCP, your Antigravity AI agents can invoke these tools directly during code generation!

---

## 2. FastMCP Server Bridge (`google_flow_server.py`)
Tools exposed to Antigravity agents:
- `generate_video_flow`: Dispatches generative video generation via Google Flow / Veo.
- `create_3d_product_orbit`: Tailored 360° turntable orbit prompts with lighting & camera controls.
- `extract_frame_sequence`: Executes FFmpeg to extract sequential WebP frames (`frame_0001.webp` ... `frame_0120.webp`).

---

## 3. Configuration in Antigravity

Add the following to your Antigravity MCP configuration file:
**File path**: `C:\Users\ADMIN\.gemini\antigravity\mcp_config.json` (or workspace `.agents/mcp_config.json`):

```json
{
  "mcpServers": {
    "google-flow": {
      "command": "python",
      "args": ["E:/agy/ai_company/mcp/google_flow_server.py"],
      "env": {
        "GEMINI_API_KEY": "YOUR_GEMINI_OR_GOOGLE_AI_KEY",
        "GOOGLE_APPLICATION_CREDENTIALS": "C:/path/to/service-account.json"
      }
    }
  }
}
```

---

## 4. Authentication Prerequisites
1. **Google Cloud / Vertex AI Application Default Credentials (ADC)**:
   ```bash
   gcloud auth application-default login
   ```
   OR set your API key:
   ```bash
   set GEMINI_API_KEY=your_api_key_here
   ```
2. **FFmpeg**:
   Ensure `ffmpeg` is installed and available in your system `PATH` for WebP frame extraction.
