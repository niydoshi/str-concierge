import os
import gradio as gr
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
AGENT_ID = os.getenv("ELEVENLABS_AGENT_ID")

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def ask_concierge(question: str):
    if not question.strip():
        return "Please enter a question.", None

    # Use ElevenLabs text-based agent call
    response = client.conversational_ai.agents.chat(
        agent_id=AGENT_ID,
        messages=[{"role": "user", "content": question}]
    )

    text_answer = response.messages[-1]["content"]

    # Generate spoken audio from the response
    audio = client.text_to_speech.convert(
        voice_id=response.agent_voice_id if hasattr(response, "agent_voice_id") else "EXAVITQu4vr4xnSDxMaL",
        text=text_answer,
        model_id="eleven_turbo_v2_5",
    )

    audio_path = "response_audio.mp3"
    with open(audio_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    return text_answer, audio_path


# --- Gradio UI ---
with gr.Blocks(title="STR Concierge", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏡 STR Concierge")
    gr.Markdown("AI voice concierge for short-term rental guests — powered by ElevenLabs.")

    question_input = gr.Textbox(
        label="Guest Question",
        placeholder="e.g. What time is check-in? Is parking available?",
        lines=2
    )
    submit_btn = gr.Button("Ask Concierge", variant="primary")

    with gr.Row():
        text_output = gr.Textbox(label="Concierge Response", lines=4, interactive=False)
        audio_output = gr.Audio(label="Spoken Response", type="filepath", autoplay=True)

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

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
