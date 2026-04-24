import os
import gradio as gr
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import save

load_dotenv()

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

def load_knowledge_base():
    with open("knowledge_base/property_knowledge_base.md", "r", encoding="utf-8") as f:
        return f.read()

def ask_concierge(question: str):
    if not question.strip():
        return "Please enter a question.", None
    
    try:
        knowledge_base = load_knowledge_base()
        
        prompt = f"""You are a concierge for a short-term rental property.
Answer the guest question using only the property information below.
If the answer is not available, say the host will follow up.
Keep your tone warm, friendly and concise.

Property Information:
{knowledge_base}

Guest Question: {question}

Response:"""

        # Generate spoken audio using ElevenLabs TTS
        audio = client.text_to_speech.convert(
            voice_id="EXAVITQu4vr4xnSDxMaL",
            text=prompt,
            model_id="eleven_turbo_v2_5",
        )
        
        audio_path = "/tmp/response_audio.mp3"
        save(audio, audio_path)
        
        return "Voice response generated — press play to hear the answer.", audio_path
    
    except Exception as e:
        return f"Error: {str(e)}", None

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

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860))
)
