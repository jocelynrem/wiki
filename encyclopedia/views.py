from django.shortcuts import render, redirect
from . import util
import markdown2
import random
from django import forms

class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))


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
            {"title": title, "content": html_content},
        )


def search(request):
    query = request.GET.get("q", "")
    entries = util.list_entries()

    match = next((entry for entry in entries if query.lower() == entry.lower()), None)

    if match:
        return redirect("entry", title=match)
    else:
        filtered_entries = [
            entry for entry in entries if query.lower() in entry.lower()
        ]
        return render(
            request,
            "encyclopedia/search_results.html",
            {"entries": filtered_entries, "query": query},
        )


def new_entry(request):
    return render(request, "encyclopedia/new_entry.html")


def edit_entry(request, title):
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect("entry", title=title)
    else:
        content = util.get_entry(title)
        if content is None:
            return render(request, "encyclopedia/error.html", {"message": "Page not found"})
        form = EditEntryForm(initial={"content": content})
        return render(
            request, 
            "encyclopedia/edit_entry.html",
            {"form": form, "title": title})


def random_entry(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    return redirect("entry", title=entry)
