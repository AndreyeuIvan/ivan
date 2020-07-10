from django.shortcuts import render
from rango.models import Category, Page
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required


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
    form = CategoryForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form })


def add_page(request, category_name_url):
    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)

            cat = Category.objects.get(name=category_name)
            page.category = cat

            page.views=0
            page.save()
            return category(request, category_name_url)
        else:
            print(form.errors)
    else:
        form = PageForm()

    return render(request, 'rango/add_page.html',
            {'category_name_url': category_name_url,
            'category_name' : category_name, 'form':form})


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()

            registered = True
        
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                'rango/register.html',
                 {
                'user_form': user_form,
                'profile_form':profile_form,
                'registered': registered
                })


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponse(reverse('index'))
            else:
                HttpResponseRedirect('YOur account is disables')
        else:
            print(f'Invalid details{username}, {password}')
            return HttpResponse('Invalid details')
    else:
        return render(request, 'rango/login.html')


def some_view(request):
    if not request.user.is_authenticated():
        return HttpResponse('You are logged in.')
    else:
        return HttpResponse('You are not logged in.')


def restricted(request):
    return HttpResponse('Eee boy')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
