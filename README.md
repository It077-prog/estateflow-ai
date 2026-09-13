# EstateFlow AI

EstateFlow AI is a full-stack real estate lead management CRM built with Django, PostgreSQL, Django REST Framework, and Google Gemini.

The application helps real estate teams manage leads, track follow-ups, record activities, generate AI-powered lead summaries and follow-up messages, and receive leads automatically from external systems through a secured webhook.

## Live Application

Deployed on Render:

`https://YOUR-RENDER-URL.onrender.com`

> Replace the URL above with the actual deployed EstateFlow URL.

---

## Features

### Lead CRM

- Create, view, edit, and delete leads
- Track lead status through the sales pipeline
- Store property interest and budget
- Assign leads to users
- Schedule follow-up dates
- Track lead source

### Dashboard

The dashboard provides:

- Total leads
- Qualified leads
- Won leads
- Conversion rate
- Overdue follow-ups
- Pipeline breakdown
- Lead source breakdown
- Upcoming follow-ups

### Notes and Activities

Each lead can have:

- Notes
- Calls
- Emails
- WhatsApp interactions
- Meetings
- Status-change activities
- Other CRM activities

### AI Integration

Google Gemini is integrated through a dedicated AI service layer.

AI features include:

- Lead summaries
- Suggested follow-up messages
- Persistent AI-generated results
- Retry logic for temporary provider failures
- Graceful handling of AI service outages

### REST API

EstateFlow provides REST endpoints using Django REST Framework.

The API supports:

- Lead CRUD
- Notes
- Activities
- Filtering
- Searching
- Ordering
- AI summary generation
- AI follow-up generation

Example:

```text
/api/leads/
/api/notes/
/api/activities/