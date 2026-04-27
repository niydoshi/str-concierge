
# =============================================================
# STR Concierge — AI Voice Concierge for Short-Term Rentals
# =============================================================
# Purpose: Answer repetitive guest questions using a property-specific
# knowledge base, returning both a written and spoken response.
#
# Architecture:
#   Guest question → GPT-4o-mini (text answer) → ElevenLabs TTS (audio)
#   Both text and audio returned simultaneously in the Gradio UI
#
# Note: This code was written with the assistance of Claude (Anthropic).
# The architecture decisions, product requirements, and deployment
# were defined by the author. Claude was used to implement the code.
# =============================================================

import os
import gradio as gr
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import save
from openai import OpenAI

# Load API keys from .env file (never hardcoded — see .env.example)
load_dotenv()

# Initialize ElevenLabs for voice synthesis and OpenAI for text generation
# Two separate clients — each handles a distinct step in the pipeline
eleven_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_knowledge_base():
    # Knowledge base is a plain markdown file so non-technical hosts
    # can update property info without touching any code
    with open("knowledge_base/property_knowledge_base.md", "r", encoding="utf-8") as f:
        return f.read()


def ask_concierge(question: str):
    """
    Main pipeline: takes a guest question and returns a text answer
    and a spoken audio response.

    Step 1 — GPT-4o-mini reads the knowledge base and generates a
             concise, warm answer (max 3 sentences)
    Step 2 — ElevenLabs converts that answer to natural speech
             using the Rachel voice (eleven_turbo_v2_5 for low latency)
    Step 3 — Returns both text and audio path to the Gradio UI
    """
    if not question.strip():
        return "Please enter a question.", None

    try:
        knowledge_base = load_knowledge_base()

        # Step 1: Generate text answer using OpenAI
        # System prompt is strict — model only uses knowledge base content
        # and defers to the host rather than guessing unknown answers
        completion = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a concierge for a short-term rental property.
Answer guest questions using ONLY the property information below.
If the answer is not in the information, say: 'The host will follow up on that shortly.'
Keep responses warm, friendly, and under 3 sentences.

Property Information:
{knowledge_base}"""
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            max_tokens=150  # Keep responses concise for natural speech pacing
        )

        text_answer = completion.choices[0].message.content.strip()

        # Step 2: Convert text answer to speech using ElevenLabs
        # Rachel voice (21m00Tcm4TlvDq8ikWAM) chosen for warmth and clarity
        # eleven_turbo_v2_5 selected for lowest latency on short responses
        audio = eleven_client.text_to_speech.convert(
            voice_id="21m00Tcm4TlvDq8ikWAM",
            text=text_answer,
            model_id="eleven_turbo_v2_5",
        )

        # Save to /tmp — required for Render's ephemeral filesystem
        audio_path = "/tmp/response_audio.mp3"
        save(audio, audio_path)

        return text_answer, audio_path

    except Exception as e:
        # Surface errors in the UI rather than failing silently
        return f"Error: {str(e)}", None


# =============================================================
# Gradio UI
# =============================================================
# Gradio chosen for rapid web UI deployment with no frontend code.
# Guest sees two outputs side by side: written answer + audio player.
# =============================================================

with gr.Blocks(title="STR Concierge") as demo:
    gr.Markdown("# 🏡 STR Concierge")
    gr.Markdown("AI voice concierge for short-term rental guests — powered by ElevenLabs.")

    question_input = gr.Textbox(
        label="Guest Question",
        placeholder="e.g. What time is check-in? Is parking available?",
        lines=2
    )
    submit_btn = gr.Button("Ask Concierge", variant="primary")

    with gr.Row():
        # Text output — written answer displayed immediately
        text_output = gr.Textbox(label="Concierge Response", lines=4, interactive=False)
        # Audio output — ElevenLabs spoken response, autoplays on answer
        audio_output = gr.Audio(label="Spoken Response", type="filepath", autoplay=True)

    # Example questions pre-loaded to demonstrate the concierge in demos
    gr.Examples(
        examples=[
            ["What time is check-in and check-out?"],
            ["Is there parking available?"],
            ["Are pets allowed?"],
            ["What's the WiFi password?"],
            ["Can you recommend a good local restaurant?"],
        ],
        inputs=question_input
    )

    submit_btn.click(
        fn=ask_concierge,
        inputs=question_input,
        outputs=[text_output, audio_output]
    )

# server_name 0.0.0.0 required for Render deployment — binds to all interfaces
# PORT env var injected by Render at runtime — falls back to 7860 for local dev
demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860))
)
