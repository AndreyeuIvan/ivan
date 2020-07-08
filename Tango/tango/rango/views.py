from django.shortcuts import render
from rango.models import Category, Page
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rango.forms import CategoryForm


def index(request):
    category_list = Category.objects.order_by('name')[:5]
    context_dict = {'categories' : category_list }
    for category in category_list:
        category.url = category.name.replace(' ', '_')
    return render(request, 'rango/index.html', context_dict)


def hello(request):
    return HttpResponse('Rango Says: <a href="/about/"> Index </a> page.')


def category(request, category_name_url):
    category_name = category_name_url.replace('_', ' ')
    context_dict = {'category_name': category_name}
    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except ObjectDoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form })