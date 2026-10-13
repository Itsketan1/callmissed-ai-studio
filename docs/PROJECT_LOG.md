\# CallMissed AI Studio — Project Log



\## Project objective

Build a responsive AI web application for the CallMissed Backend Engineering Intern assignment.



\## Requirements

\- AI chat using CallMissed API

\- Image generation using CallMissed API

\- Interactive voice agent using CallMissed API

\- Python, Flask, HTML, CSS and JavaScript

\- Hosting on AWS Free Tier or an equivalent platform

\- Maximum API budget: USD 20

\- Keep API credentials out of source code, frontend and Git history



\## Engineering principles

\- Verify official API documentation before implementing endpoints.

\- Test each feature before moving to the next.

\- Use mocked API responses for automated tests wherever possible.

\- Record actual results; never assume tests passed.

\- Track API usage and spending wherever measurable.

\- Never log secrets or sensitive credentials.



\## Status — 2026-10-12



\### Completed and verified

\- Created and activated project-specific Python virtual environment.

\- Verified Python executable is inside the project's `.venv`.

\- Installed Flask, Requests, python-dotenv and pytest.

\- Upgraded pip to 26.2.1.

\- Generated requirements.txt in the project directory.

\- Verified dependency imports successfully.



\### Pending verification

\- `.env` ignore protection.

\- Project documentation and Git repository state.

\- CallMissed API catalog and authentication.

\- Chat implementation and tests.

\- Image generation implementation and tests.

\- Voice-agent implementation and tests.

\- Deployment and submission.



\### Issues and fixes

1\. Windows initially could not find the Python command.

&#x20;  - Resolution: Python environment became available and dependencies were installed.

2\. Initial package installation occurred in the user-home environment.

&#x20;  - Resolution: project-specific `.venv` was created and verified.



\### API usage and cost

\- Live API calls: not yet confirmed.

\- API spending: not yet measured.



\## Next actions

1\. Verify `.env` is ignored by Git.

2\. Verify `.env.example` contains placeholders only.

3\. Verify repository status and documentation files.

4\. Inspect the official CallMissed model catalog.

5\. Test authenticated connectivity before implementing chat.

## Progress update — 13 October 2026

### AI Chat
- Flask application starts successfully.
- CallMissed model catalog connection verified.
- `sarvam-105b` chat request tested successfully.
- Increased max_tokens from 200 to 1000 after a response ended with finish_reason=length and empty content.
- Date-answer accuracy remains a known limitation.

### Image generation
- Backend client and Flask route added.
- UI integration: pending verification.
- Live image generation: pending verification.
- Actual image-generation cost: not yet measured.

### Next actions
- Verify one image-generation request.
- Add automated tests for chat and image routes.
- Implement the voice-agent workflow.
- Complete security, cost controls, README and deployment.


### Image generation investigation — 13 October 2026

- Initial model: flux-1.1-pro
- Result: HTTP 503 from CallMissed
- Provider message: model temporarily unavailable
- Provider-recommended alternatives: flux-2-pro or gpt-image-2
- Application authentication: request reached the provider
- Next action: test flux-2-pro once
- Successful image generation: not yet verified
- Actual API spend: not yet measured
