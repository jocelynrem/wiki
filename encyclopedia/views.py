from django.shortcuts import render
from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    entries = util.list_entries()

    for entry_title in entries:
        if title.lower() == entry_title.lower():
            title = entry_title
            break

    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {"message": "Page not found"})

    else:
        html_content = markdown2.markdown(content)
        return render(
            request,
            "encyclopedia/entry.html",
            {"title": title, "content": html_content
        })
