# NaviAble — Indoor Navigation Prototype

**Tagline:** Navigate Freely. Live Independently.

NaviAble is a student-hackathon prototype concept for multilingual indoor navigation. This repository contains a browser frontend and a Python FastAPI backend.

## Features
- Light-blue and yellow visual theme
- English, Tamil, and Hindi route instructions
- Sample two-floor college building map
- Graph-based route calculation
- Voice output using browser text-to-speech
- Step-by-step navigation and route highlighting
- Accessible labels, focus states, and live status messages

## Tech stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python, FastAPI
- Route logic: breadth-first search over sample walkable connections
- Sample map data: Python dictionary (easy to replace with verified data)

## Run locally

### Requirements
- Python 3.10 or newer

### Windows
Open Command Prompt in this repository folder, then run:

```bash
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000 in your browser. API documentation: http://127.0.0.1:8000/docs

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## GitHub upload

1. Sign in to GitHub and create a new repository named `NaviAble`.
2. Extract this ZIP into a folder.
3. Open a terminal in that folder.
4. Run:

```bash
git init
git add .
git commit -m "Initial NaviAble indoor navigation prototype"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/NaviAble.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. Do not upload passwords, API keys, personal data, or private building plans without permission.

## API endpoints
- `GET /api/health` — backend health check
- `GET /api/buildings` — list sample buildings
- `GET /api/buildings/sample_college` — sample map data
- `POST /api/route` — calculate a route

Example request body:
```json
{
  "building_id": "sample_college",
  "start": "entrance",
  "destination": "room_101",
  "language": "ta",
  "step_free": true
}
```

## Important safety and accuracy limits
This is a simulated demo using fictional sample building data. It does not detect a user's actual indoor location, identify obstacles, or guarantee an accessible route. The route preference is currently a UI choice and is not yet enforced by a separate accessibility-aware route engine. Before any real-world use, replace the sample map with a verified floor plan, encode accessible connections accurately, add a reliable indoor-positioning method, and test routes with building staff and accessibility specialists. Do not use this prototype as a sole mobility aid.

## Suggested next improvements
- QR checkpoint scan flow for indoor location confirmation
- Admin interface for maintaining room and corridor data
- Real accessibility-aware route graph (lifts, ramps, stairs, closures)
- Better voice prompts based on turn direction and nearby landmarks
- Mobile packaging and supervised user testing
