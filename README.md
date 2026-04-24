# str-concierge
AI concierge prototype for short-term rental guest communication and repetitive guest questions.

# STR Concierge

STR Concierge is a work-in-progress learning project focused on reducing repetitive guest communication for short-term rental hosts.

The idea came from my own experience managing a short-term rental. As I thought about scaling, I realized that guest communication, pricing, and marketing can quickly become major time drains. This project starts with one of those problems: answering repeated guest questions accurately and consistently.

## Problem

Guests often ask the same questions about check-in, checkout, parking, pets, amenities, lake access, house rules, and local recommendations.

These questions are important, but repetitive. Hosts still need to respond quickly, clearly, and with the right tone.

## Goal

Build a simple AI concierge prototype that can answer common guest questions using trusted property-specific information.

## Current Version

The current version is intentionally simple and focused on understanding the workflow before adding more complexity:

1. A guest asks a question  
2. The system references a structured property knowledge base  
3. The question and property context are sent to an AI API  
4. The system generates a suggested, guest-friendly response  

A simple rule-based version is also included as a baseline to demonstrate the progression from static responses to an API-driven approach.

## Data Sources

Future versions may use:
- Property information documents
- Past guest messages
- Airbnb listing details
- Hostfully reservation and property data

## What I’m Learning

- How to turn messy property information into structured knowledge
- How to design guest-facing automation
- How to build small before adding complexity
- How to think about trust, accuracy, and escalation
- How AI workflows could support hospitality operations
  

## Status

Work in progress. Starting with a local prototype before adding AI and PMS integrations.
