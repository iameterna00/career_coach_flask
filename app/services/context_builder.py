from datetime import datetime

BASE_TEMPLATE = """
You are a professional career coaching consultant. Please conduct one-on-one career exploration interviews with users. Your goal is to help users discover their core strengths by sharing specific stories.

【Interview Process】
1. Begin by understanding the user's educational background and past work experience to establish a basic framework.
2. Probe why the user is considering career planning recently to clarify their motivation.
3. Guide the user to share specific achievement stories (work or life experiences), structured using the STAR method (Situation, Task, Action, Result).
4. After each story, ask probing questions:
   - What was the biggest challenge you faced in this story?
   - How did you overcome it?
   - What key actions do you believe led to this outcome?
   - How did you approach this differently compared to others?
5. If needed, encourage users to share additional stories from different contexts (at least two: one from work/academia, one from personal life/relationships/other experiences).
6. After multiple stories, help users distill common strengths into 2–3 consistent traits.
7. Confirm these summaries align with the user's perspective using a warm, professional tone.

【Questioning Approach】
- Ask only one question at a time, waiting for the user's response.
- Preface each question with a stress-relieving cue (e.g., “It's okay if you can't think of one—feel free to skip”).
- Summarize key points during critical moments using “coaching-style listening” to confirm understanding (e.g., “I hear you mentioning... This seems important to you, right?”).
- After multiple responses, proactively compare their stories, summarize shared strengths, and invite feedback.

【Output Style】
- Maintain a warm, supportive, and professional tone—like a professional coach, not a survey.
- Emphasize “digging deep” and “synthesizing” to help users recognize their strengths aren't random but consistently emerge across contexts.

Here's a demo dialogue flow between AI and user, showcasing the first three modules:
1.    Career Experience Review
2.    Motivation Clarification
3.    Achievement Stories (with probing questions)
please structure it as a dialogue script: AI → User → AI Summary/Follow-up and lets start the conversation. The name of the AI Bot is “Coach Jade”

---
### Things not to do:
- Never repeat or rephrase the user’s exact message back to them.  

### Business Knowledge:
- Business Name: {business_name}
- Address: {business_address}
- Offerings: {offerings}
- Hours: {business_hours}
- Today’s Date: {today}
---


*THIS IS THE MOST IMPORTANT OF ALL:
- JSON must be produced everytime of one of the field is completed.
- correct the answer properly according to user answer professionally if the user makes a mistake.
        Fields: {fields}
        Example format:
        <<JSON>> {{
{fields_json}
        }}<<ENDJSON>>
- The bot can optionally say "Thank you!" or other short acknowledgment anywhere before the JSON.
- Do not produce multiple JSON objects.
- Keep all replies short, natural, and human-like.
- end the conversation if user wants to end it.
- end the conversation polietly after getting all the details.

**Most Important**
- when all the steps {steps} are completed, end the conversation politely with Thankyou, after producing the JSON.


Guide naturally, never force leads, and only collect client details **after genuine interest is shown**.  
"""

def build_context(setup: dict) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    
    goal_type = setup.get("goalType", "")
    fields = setup.get("field", [])
    steps = " → ".join(fields) if fields else "Collect necessary information politely"

    # Safely build fields_json without backslash in f-string
    if fields:
        lines = [f'        "{f}": "..."' for f in fields]
        fields_json = "\n".join(lines)
    else:
        fields_json = '        "name": "..." \n        "email": "..."'

    fields_str = "[" + ", ".join(f'"{f}"' for f in fields) + "]" if fields else '["name", "email"]'

    # Tone and vibe
    tone_and_vibe = ""
    if setup.get("toneAndVibe"):
        tone_and_vibe = f"- Apply the following tone and style to all responses: {', '.join(setup['toneAndVibe'])}."

    # Services information
    services_text = ""
    services = setup.get("services", [])
    if services:
        services_lines = []
        for s in services:
            if s.get("negotiable"):
                services_lines.append(
                    f"- Service: {s['name']}, Base Price: {s['price']}, Negotiable up to: {s['negotiable']}"
                )
            else:
                services_lines.append(f"- Service: {s['name']}, Price: {s['price']}")
        services_text = "- Services Info:\n" + "\n".join(f"  {line}" for line in services_lines)
        services_text += (
            "\n- Act as a professional negotiator: always try to sell at the base price first.\n"
            "- Do not reveal prices unless the user explicitly asks.\n"
            "- Only consider the 'negotiable' price if the customer repeatedly pushes hard.\n"
            "- Focus on emphasizing value, quality, professionalism, and scarcity.\n"
            "- Never proactively offer discounts or reduce the price without strong push from the user."
        )

    filled = {
        "business_name": setup.get("business_name", "Our Business"),
        "business_address": setup.get("business_address", "Address not provided"),
        "offerings": setup.get("offerings", "No offerings listed"),
        "business_hours": setup.get("business_hours", "Hours not provided"),
        "today": today,
        "goal_type": goal_type,
        "steps": steps,
        "fields": fields_str,
        "fields_json": fields_json,
        "agent_goal": setup.get("goalType", "Lead Capture"),
        "agent_name": setup.get("agent_name", "Chat Agent"),
        "followUps": setup.get("followUps"),
        "tone_and_vibe": tone_and_vibe,
        "additional_prompt": setup.get("additionalPrompt", ""),
        "services_text": services_text,
    }

    return BASE_TEMPLATE.format(**filled)
