from django.shortcuts import render
from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    content = util.get_entry(title)
    if content is none:
        return render(request, "encyclopedia/error.html", { 
            "message": "Page not found"
        })

    else:
        html_content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        }
    )