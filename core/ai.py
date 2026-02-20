"""
Generate or update website sections from natural-language prompts (Lovable-style).
Uses OpenAI API; set OPENAI_API_KEY in env. Falls back to template if no key.
"""
import json
import os
import re


SYSTEM_PROMPT = """You are a website builder assistant. The user is editing their page. You output:
1) A valid JSON array of section objects (see below).
2) On the next line after the JSON, write exactly: REPLY: then one short friendly sentence telling the user what you did (e.g. "I've added a testimonials section and updated the hero title.").

Allowed section types: hero (title, subtitle, cta_text, cta_url), features (heading, items with title/description), testimonials (heading, items with quote/author), pricing (heading, subheading, plans with name/price/period/features/cta/highlight), cta (title, subtitle, cta_text, cta_url).

Output the JSON array first, then the REPLY line. No markdown code blocks."""


def generate_sections_from_prompt(prompt, current_sections=None, return_reply=False):
    """
    Call OpenAI to generate or update sections from a text prompt.
    prompt: user description or change request.
    current_sections: optional list of sections to modify.
    return_reply: if True, return (sections, reply_message) else sections or None.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return (None, None) if return_reply else None

    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
    except Exception:
        return (None, None) if return_reply else None

    if current_sections:
        user_content = (
            "Current page sections (JSON):\n"
            + json.dumps(current_sections, indent=2)
            + "\n\nUser request: "
            + prompt
            + "\n\nOutput the full updated JSON array of sections (apply the change)."
        )
    else:
        user_content = (
            "Create a single-page website with sections that match this description: "
            + prompt
            + "\n\nOutput the JSON array of sections (include hero, and add features/pricing/cta as appropriate)."
        )

    try:
        response = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            temperature=0.3,
            max_tokens=2000,
        )
        text = (response.choices[0].message.content or "").strip()
    except Exception:
        return (None, None) if return_reply else None

    # Extract REPLY: ... if present
    reply_msg = None
    if "REPLY:" in text:
        parts = text.split("REPLY:", 1)
        text = parts[0].strip()
        reply_msg = parts[1].strip() if len(parts) > 1 else None
        if reply_msg:
            reply_msg = reply_msg.split("\n")[0].strip()

    # Parse JSON (allow wrapped in ```json ... ```)
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```\s*$", "", text)
    text = text.strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return (None, reply_msg) if return_reply else None

    if not isinstance(data, list):
        return (None, reply_msg) if return_reply else None

    # Normalize: only allow known types and required keys
    allowed = {"hero", "features", "testimonials", "pricing", "cta"}
    out = []
    for s in data:
        if not isinstance(s, dict):
            continue
        t = s.get("type")
        if t not in allowed:
            continue
        if t == "hero":
            out.append({
                "type": "hero",
                "title": str(s.get("title", "")),
                "subtitle": str(s.get("subtitle", "")),
                "cta_text": str(s.get("cta_text", "Get started")),
                "cta_url": str(s.get("cta_url", "#")),
            })
        elif t == "features":
            items = s.get("items") or []
            out.append({
                "type": "features",
                "heading": str(s.get("heading", "Features")),
                "items": [
                    {"title": str(i.get("title", "")), "description": str(i.get("description", ""))}
                    for i in items if isinstance(i, dict)
                ][:6],
            })
        elif t == "testimonials":
            items = s.get("items") or []
            out.append({
                "type": "testimonials",
                "heading": str(s.get("heading", "Testimonials")),
                "items": [
                    {"quote": str(i.get("quote", "")), "author": str(i.get("author", ""))}
                    for i in items if isinstance(i, dict)
                ][:6],
            })
        elif t == "pricing":
            plans = s.get("plans") or []
            out.append({
                "type": "pricing",
                "heading": str(s.get("heading", "Pricing")),
                "subheading": str(s.get("subheading", "")),
                "plans": [
                    {
                        "name": str(p.get("name", "")),
                        "price": str(p.get("price", "")),
                        "period": str(p.get("period", "")),
                        "features": [str(x) for x in (p.get("features") or []) if isinstance(x, (str, int, float))][:5],
                        "cta": str(p.get("cta", "Choose")),
                        "highlight": bool(p.get("highlight", False)),
                    }
                    for p in plans if isinstance(p, dict)
                ][:4],
            })
        elif t == "cta":
            out.append({
                "type": "cta",
                "title": str(s.get("title", "")),
                "subtitle": str(s.get("subtitle", "")),
                "cta_text": str(s.get("cta_text", "Get started")),
                "cta_url": str(s.get("cta_url", "#")),
            })

    if not out:
        return (None, reply_msg) if return_reply else None
    if return_reply:
        return (out, reply_msg or "I've applied your changes.")
    return out
