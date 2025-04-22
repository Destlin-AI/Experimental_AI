
from django.shortcuts import render
from django.http import JsonResponse
from .toggle_registry import toggle_registry

def dashboard_view(request):
    context = {
        "toggles": toggle_registry.toggles,
        "emotion": toggle_registry.state("EmotionEngine"),
        "memory_fragments": 2187,
        "ram_usage": "22.5 GB",
        "agents": ["LLM-01", "LLM-02", "Watcher"]
    }
    return render(request, "wrapper.html", context)
