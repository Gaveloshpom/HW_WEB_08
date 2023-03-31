import json

from models import Author, Quotes
import connect

with open("authors.json") as fd:
    data = json.load(fd)
    for k in data:
        Author(fullname=k["fullname"], born_date=k["born_date"], born_location=k["born_location"], description=k["description"]).save()

with open("quotes.json", encoding="utf-8") as fd:
    data = json.load(fd)
    for k in data:
        Quotes(tags=[n for n in k["tags"]],
               author=[author for author in Author.objects() if k["author"]==author.fullname][0],
               quote=k["quote"]).save()