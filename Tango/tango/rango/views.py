from django.shortcuts import render
from rango.models import Category, Page
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from registration.backends.simple.views import RegistrationView
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bingsearch import run_query


def index(request):
    request.session.set_test_cookie()
    category_list = Category.objects.order_by('name')[:5]
    pages = Page.objects.order_by('-views')[:5]
    context_dict = {'categories' : category_list, 'pages':pages}
    for category in category_list:
        category.url = category.name.replace(' ', '_')
    responce = render(request, 'rango/index.html', context_dict)
    visitor_cookie_handler(request, responce)
    return responce


def hello(request):
    if request.session.test_cookie_worked():
        print('TESTTTTTT')
        request.session.delete_test_cookie()
    return render(request, 'rango/about.html')


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
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
    else:
        print(form.errors)
    context_dict = {'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


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


def visitor_cookie_handler(request, responce):
    visits = int(request.COOKIES.get('visits', '1'))
    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        responce.set_cookie('last_visit', str(datetime.now()))
    else:
        visits = 1
        responce.set_cookie('last_visit', last_visit_cookie)
    
    responce.set_cookie('visits', visits)


class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return '/rango/'


def search(request):
    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
             # Run our Webhose function to get the results list!
             result_list = run_query(query)
    return render(request, 'rango/search.html', {'result_list': result_list})


@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)


def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)

        if max_results > 0:
            if len(cat_list) > max_results:
                cat_list = cat_list[:max_results]
    return cat_list


def suggest_category(request):
    cat_list = []
    starts_with = ''

    if request.method == 'GET':
        starts_with = request.GET['suggestion']
        cat_list = get_category_list(8, starts_with)

    return render(request, 'rango/cats.html', {'cats': cat_list })


@login_required
def auto_add_page(request):
    cat_id = None
    url = None
    title = None
    context_dict = {}
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        url = request.GET['url']
        title = request.GET['title']
        if cat_id:
            category = Category.objects.get(id=int(cat_id))
            p = Page.objects.get_or_create(category=category, title=title, url=url)
            pages = Page.objects.filter(category=category).order_by('-views')
            # Adds our results list to the template context under name pages.
            context_dict['pages'] = pages

    return render(request, 'rango/page_list.html', context_dict)