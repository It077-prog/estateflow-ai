# EstateFlow AI

EstateFlow AI is a full-stack real estate lead management CRM built with Django, PostgreSQL, Django REST Framework, and Google Gemini.

The application helps real estate teams manage leads, track follow-ups, record activities, generate AI-powered lead summaries and follow-up messages, and receive leads automatically from external systems through a secured webhook.

## Technical Case Study

EstateFlow AI is a cloud-deployed real estate CRM demonstrating
lead management, REST API development, secured webhook intake,
and on-demand Google Gemini AI integration.

The technical case study covers:

- Business problem and proposed solution
- Application architecture and request flows
- Django and PostgreSQL implementation
- REST APIs and webhook security
- Gemini AI-assisted lead management
- Live application screenshots
- Comparison with publicly documented CRM projects
- Automated and manual testing
- Future automation roadmap using n8n, Make and Zapier

**Testing:** 13/13 automated tests passed.

[View EstateFlow AI Technical Case Study](docs/EstateFlow_AI_Technical_Case_Study.pdf)

**Live Application:** https://estateflow-ai-9utj.onrender.com/

## Live Application

Deployed on Render:

`https://estateflow-ai-9utj.onrender.com`


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
