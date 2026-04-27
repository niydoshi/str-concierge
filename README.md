# str-concierge
AI concierge prototype for short-term rental guest communication and repetitive guest questions.

This is a work-in-progress learning project focused on reducing repetitive tasks such as guest communication for short-term rental hosts.

The idea came from my own experience managing a short-term rental. As I thought about scaling, I realized that guest communication, pricing, and marketing can quickly become major time drains. This project starts with one of those problems: answering repeated guest questions accurately and consistently.

## Demo 
[Loom]

## Problem

Short-term rental hosts lose hours every week answering the same 
guest questions:

- *"What time is check-in?"*
- *"Is there parking?"*
- *"Are pets allowed?"*
- *"What's the WiFi password?"*

These questions are critical to guests but exhausting to answer 
manually — especially across multiple properties, at odd hours, 
during peak seasons.

**The average STR host spends on an average 10-12 hours per week on repetitive 
guest communication.** This project reduces that to 2 or less per week. 

## The Solution

STR Concierge is an AI-powered voice assistant that:

- 🎤 **Speaks answers aloud** using ElevenLabs TTS
- 🧠 **Generates accurate responses** from a property-specific 
  knowledge base using GPT-4o-mini
- 🚫 **Never guesses** — defers to the host for anything outside 
  the knowledge base
- ⚙️ **Requires no code changes** to update property information
- 🌐 **Runs in any browser** — no app download required

## Current Version

The current version is intentionally simple and focused on understanding the workflow before adding more complexity:

1. A guest asks a question  
2. The system references a structured property knowledge base  
3. The question and property context are sent to an AI API  
4. The system generates a suggested, guest-friendly response  

A simple rule-based version is also included as a baseline to demonstrate the progression from static responses to an API-driven approach.

## Current Architecture
<img width="1672" height="941" alt="STRConcierge_Current State Architecture_2" src="https://github.com/user-attachments/assets/a50591ab-8d85-45c4-be1b-dc170d905ac8" />




## Target Architecture (Draft)
<img width="1672" height="941" alt="STR Concierge_Target State Architecture_2" src="https://github.com/user-attachments/assets/906fac2b-072b-430f-bc6e-33ee8d16dc9c" />

## What I’m Learning

- How to turn messy property information into structured knowledge
- How to design guest-facing automation
- How to build small before adding complexity
- How to think about trust, accuracy, and escalation
- How AI workflows could support hospitality operations

## Roadmap

<img width="1536" height="1024" alt="STRConcierge_Roadmap" src="https://github.com/user-attachments/assets/40094990-99d4-48fa-8e8a-c43fcdb89e3b" />


## Status

Work in progress. Starting with a local prototype before adding AI and PMS integrations.
