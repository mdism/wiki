from django.shortcuts import render
from django.http import HttpResponse
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# def get_content(request, entity_name):
#     print("******** entity_name: " + entity_name)
    
def get_content(request,entity_name):
    entity = util.get_entry(entity_name)
    if entity == None:
        return render(request, "encyclopedia/error.html",{
            "message": "Error: 404! It seems there is nothing you are looking here."
        })
    result = markdown2html(title=entity)
    return render(request, "encyclopedia/content.html",{
        "entityTitle": entity_name,
        "EntityData": result
    })

def markdown2html(title):
    if title == None:
        return None
    return markdown2.markdown(title)
    
def search(request):
    if request.method == "POST":
        searchedFor = request.POST['q']
        entity = util.get_entry(searchedFor)
        if entity == None:
            related = []
            all_entity = util.list_entries()
            for entity in all_entity:
                if searchedFor.lower() in entity.lower():
                    related.append(entity)
            return render(request, "encyclopedia/search.html",{
                "entries": related
            })
        result = markdown2html(title=entity)
        return render(request, "encyclopedia/content.html",{
            "entityTitle": searchedFor,
            "EntityData": result
        })
def new(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        if title == ""  or content == "" :
            return render(request, "encyclopedia/new.html",{
                "message" : "Error: Both fields are required ❌"
            })
        elif util.get_entry(title) is not None:
            return render(request, "encyclopedia/new.html",{
                "message" : "Error: Entry for this title is already exists. ❌"
            })

        util.save_entry(title,content)
        entity = util.get_entry(title)
        return render(request, "encyclopedia/content.html",{
            "entityTitle": title,
            "EntityData": markdown2html(title=entity)
        })

    elif request.method == "GET":
        return render(request, "encyclopedia/new.html")
    

def edit(request):
    if request.method =="POST":
        title = request.POST['title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "content": content
        })

def save(request):
     if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        if content == "" :
            return 
        util.save_entry(title,content)
        entity = util.get_entry(title)
        return render(request, "encyclopedia/content.html",{
            "entityTitle": title,
            "EntityData": markdown2html(title=entity)
        })
     
def random(request):
    import random
    entryList = util.list_entries()
    selected = random.choice(entryList)
    content = util.get_entry(selected)
    return render(request, "encyclopedia/content.html",{
        "entityTitle": selected,
        "EntityData": markdown2html(title=content)
    })
