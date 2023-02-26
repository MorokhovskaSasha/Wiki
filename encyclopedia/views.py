from faulthandler import disable
from hashlib import new
from logging import PlaceHolder
from multiprocessing import context
from tkinter import DISABLED
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from markdown2 import Markdown
from django import forms
from django.urls import reverse
from random import choice

from . import util

class NewPageForm(forms.Form):
    pageHead = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Заголовок сторінки.'}
    ))
    pageBody = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Текст сторінки.'}
    ))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "pages": util.list_entries()
    })



def page(request, page):
    markdownpage = Markdown()
    pageEntry = util.get_entry(page)
    if pageEntry is None:
        return render (request, "encyclopedia/fileNoneExist.html", {
        "pageHead": page
    })  
    else:
        return render (request,"encyclopedia/page.html", {
        "page": markdownpage.convert(pageEntry),
        "pageHead": page
    })



def search(request):
    search_page = request.GET.get("q")
    search_list = []
    if util.get_entry(search_page) is not None:
        return HttpResponseRedirect(reverse("encyclopedia:page", kwargs={"page": search_page}))
    else:
        search_page_lower = search_page.lower()
        entries = util.list_entries()
        for entry in entries:
           search_cycle = entry.lower().find(search_page_lower)
           if search_cycle != -1: 
              search_list.append(entry)
              print(search_list)
        if len(search_list)==0:
            return render (request, "encyclopedia/fileNoneExist.html", {
                "pageHead": search_page
        })
        else:
             return render (request, "encyclopedia/search_result.html", {
                "pages": search_list
        })


def random(request):
    pages = util.list_entries()
    page = choice(pages)
    return HttpResponseRedirect(reverse("encyclopedia:page", kwargs={'page': page})) 





def new_page(request):
    markdownpage = Markdown()
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
           pageHead=form.cleaned_data['pageHead']
           pageBody=form.cleaned_data['pageBody']
           if pageHead in util.list_entries():
                error = "This page is exist. You can find it and change."
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "error": error,
                    "edit": False
                })
           else: 
               util.save_entry(pageHead, pageBody)
               return render (request,"encyclopedia/page.html", {
                    "page": markdownpage.convert(pageBody),
                    "pageHead": pageHead
               })
    return render(request, "encyclopedia/new_page.html", {
        "form": NewPageForm() 
    })



def edit_page(request, pageHead):
    pageBody =util.get_entry(pageHead) 
    form = NewPageForm()
    form.fields['pageHead'].initial = pageHead
    form.fields['pageBody'].initial = pageBody
    form.fields['pageHead'].widget = forms.HiddenInput()
    if request.method == "POST":
        pageHead = request.POST['pageHead']
        pageBody = request.POST['pageBody']
        util.save_entry(pageHead, pageBody)
        return HttpResponseRedirect(reverse("encyclopedia:page", kwargs={'page': pageHead}))
    return render (request,"encyclopedia/new_page.html", {
                "form": form,
                "edit": True,
                "pageHead": form.fields['pageHead'].initial
    })