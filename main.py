from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from collections import deque
import os

app = FastAPI(title="NaviAble Indoor Navigation Prototype",
              description="Accessible multilingual indoor navigation demo")

BUILDINGS = {
    "sample_college": {
        "name": "Sample College Building",
        "floors": [0, 1],
        "nodes": {
            "entrance": {"label": "Main Entrance", "floor": 0, "x": 80, "y": 190},
            "lobby": {"label": "Lobby", "floor": 0, "x": 180, "y": 190},
            "corridor": {"label": "Main Corridor", "floor": 0, "x": 300, "y": 190},
            "office": {"label": "Office", "floor": 0, "x": 420, "y": 130},
            "lift_g": {"label": "Lift — Ground Floor", "floor": 0, "x": 420, "y": 250},
            "lift_1": {"label": "Lift — First Floor", "floor": 1, "x": 420, "y": 250},
            "upper_corridor": {"label": "First-Floor Corridor", "floor": 1, "x": 300, "y": 190},
            "room_101": {"label": "Room 101", "floor": 1, "x": 180, "y": 130},
            "restroom": {"label": "Restroom", "floor": 1, "x": 180, "y": 250},
            "exit": {"label": "Exit Gate", "floor": 0, "x": 80, "y": 260}
        },
        "edges": [
            ["entrance", "lobby"], ["lobby", "corridor"],
            ["corridor", "office"], ["corridor", "lift_g"],
            ["lift_g", "lift_1"], ["lift_1", "upper_corridor"],
            ["upper_corridor", "room_101"], ["upper_corridor", "restroom"],
            ["entrance", "exit"]
        ]
    }
}

class RouteRequest(BaseModel):
    building_id: str = "sample_college"
    start: str
    destination: str
    language: str = "en"
    step_free: bool = True

TEXT = {
    "en": {
        "start": "Start at {place}.",
        "same": "You are already at {place}.",
        "go": "Go from {a} to {b}.",
        "floor": "Use the lift to travel from floor {a} to floor {b}.",
        "arrive": "You have reached {place}.",
        "not_found": "No mapped route is available for this destination."
    },
    "ta": {
        "start": "{place} இடத்தில் தொடங்குங்கள்.",
        "same": "நீங்கள் ஏற்கனவே {place} இடத்தில் இருக்கிறீர்கள்.",
        "go": "{a} இடத்திலிருந்து {b} இடத்திற்குச் செல்லுங்கள்.",
        "floor": "தளம் {a} இலிருந்து தளம் {b} செல்ல மின்தூக்கியைப் பயன்படுத்துங்கள்.",
        "arrive": "நீங்கள் {place} இடத்தை அடைந்துவிட்டீர்கள்.",
        "not_found": "இந்த இடத்திற்கான வழி வரைபடத்தில் இல்லை."
    },
    "hi": {
        "start": "{place} से शुरू करें।",
        "same": "आप पहले से ही {place} पर हैं।",
        "go": "{a} से {b} की ओर जाएँ।",
        "floor": "मंज़िल {a} से मंज़िल {b} जाने के लिए लिफ्ट का उपयोग करें।",
        "arrive": "आप {place} पहुँच गए हैं।",
        "not_found": "इस गंतव्य के लिए नक्शे में रास्ता उपलब्ध नहीं है।"
    }
}

def find_path(building, start, destination):
    graph = {node: [] for node in building["nodes"]}
    for a, b in building["edges"]:
        graph[a].append(b)
        graph[b].append(a)
    queue = deque([start])
    previous = {start: None}
    while queue:
        current = queue.popleft()
        if current == destination:
            break
        for nxt in graph[current]:
            if nxt not in previous:
                previous[nxt] = current
                queue.append(nxt)
    if destination not in previous:
        return []
    path, node = [], destination
    while node is not None:
        path.append(node)
        node = previous[node]
    return list(reversed(path))

@app.get("/api/health")
def health():
    return {"status": "ok", "app": "NaviAble"}

@app.get("/api/buildings")
def list_buildings():
    return [{"id": key, "name": value["name"], "floors": value["floors"]}
            for key, value in BUILDINGS.items()]

@app.get("/api/buildings/{building_id}")
def get_building(building_id: str):
    if building_id not in BUILDINGS:
        raise HTTPException(status_code=404, detail="Building not found")
    return BUILDINGS[building_id]

@app.post("/api/route")
def calculate_route(request: RouteRequest):
    if request.building_id not in BUILDINGS:
        raise HTTPException(status_code=404, detail="Building not found")
    building = BUILDINGS[request.building_id]
    nodes = building["nodes"]
    if request.start not in nodes or request.destination not in nodes:
        raise HTTPException(status_code=400, detail="Unknown start or destination")
    path = find_path(building, request.start, request.destination)
    words = TEXT.get(request.language, TEXT["en"])
    if not path:
        return {"path": [], "steps": [], "message": words["not_found"]}
    steps = []
    if len(path) == 1:
        steps.append(words["same"].format(place=nodes[path[0]]["label"]))
    else:
        steps.append(words["start"].format(place=nodes[path[0]]["label"]))
        for first, second in zip(path, path[1:]):
            a, b = nodes[first], nodes[second]
            if a["floor"] != b["floor"]:
                steps.append(words["floor"].format(a=a["floor"], b=b["floor"]))
            else:
                steps.append(words["go"].format(a=a["label"], b=b["label"]))
        steps.append(words["arrive"].format(place=nodes[path[-1]]["label"]))
    return {
        "building": building["name"],
        "path": path,
        "path_nodes": [{"id": key, **nodes[key]} for key in path],
        "steps": steps,
        "notice": "Sample route only. Verify all maps and directions before real-world use."
    }

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    return FileResponse(os.path.join("static", "index.html"))
