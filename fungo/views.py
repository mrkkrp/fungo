from django.contrib.auth            import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers       import reverse
from django.http                    import HttpResponse, HttpResponseRedirect
from django.shortcuts               import render

from fungo.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from fungo.models import Category, Page

from datetime import datetime

# Views

def index (request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by number of likes in descending order.
    # Retrieve the top 5 only — or all if less than 5.
    # Place the list in our ‘context_dict’ dictionary which will be passed
    # to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    # ↑ how to query on database level, not on Python level?
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}

    # Get the number of visits to the site. We use the COOKIES.get()
    # function to obtain the visits cookie. If the cookie exists, the value
    # returned is casted to an integer. If the cookie doesn't exist, we
    # default to 1 and cast that.
    visits = request.session.get('visits', 1)
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).days > 0:
            visits += 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits

    context_dict['visits'] = visits

    return render(request, 'fungo/index.html', context_dict)

def category(request, category_name_url):

    # Create a context dictionary which we can pass to the template
    # rendering engine.
    context_dict = {}

    try:

        # Can we find a category name slug with the given name? If we can't,
        # the .get() method raises a ‘DoesNotExist’ exception. So the .get()
        # method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_url)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages. Note that filter returns >=
        # 1 model instance.
        pages = Page.objects.filter(category=category)

        # Add our result list to the template context under name pages.
        context_dict['pages'] = pages

        # We also add the category object from the database to the context
        # dictionary. We'll use this in the template to verify that the
        # category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category. Don't do
        # anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'fungo/category.html', context_dict)

def about (request):
    count = request.session.get('visits', 1)
    return render(request, 'fungo/about.html', {'visits': count})

@login_required
def add_category(request):
    # An http POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view. User will be shown the homepage.
            return index(request)
        else:
            # The supplied form contains errors — just print them in the
            # terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied… Render the form with
    # error messages (if any).
    return render(request, 'fungo/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_url):

    try:
        cat = Category.objects.get(slug=category_name_url)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return HttpResponseRedirect(
                    reverse('category', args=[category_name_url]))
        else:
            print(form.errors)
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat}

    return render(request, 'fungo/add_page.html', context_dict)

# def register(request):

#     # A Boolean value for telling the template whether the registration was
#     # successful.

#     registered = False

#     # If it's a HTTP POST, we're interesting in processing form data.
#     if request.method == 'POST':
#         # Attempt to grab information from the raw form information.
#         # Note that we make use of both UserForm and UserProfileForm.
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileForm(data=request.POST)

#         # If the two forms are valid...
#         if user_form.is_valid() and profile_form.is_valid():
#             # Save the user's form data to the database.
#             user = user_form.save()

#             # Now we hash the password with the set_password method. Once
#             # hashed, we can update the user object.
#             user.set_password(user.password)
#             user.save()

#             # Now sort out the UserProfile instance. Since we need to set
#             # the user attribute ourselves, we set commit=False. This delays
#             # saving the model until we're ready to avoid integrity
#             # problems.
#             profile = profile_form.save(commit=False)
#             profile.user = user

#             # Did the user provide a profile picture? If so, we need to get
#             # it from the input form and put it in the UserProfile model.
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']

#             # Now we save the UserProfile model instance.
#             profile.save()

#             # Update our variable to tell the template registration was
#             # successful.
#             registered = True

#         # Invalid form or forms — mistakes or something else? Print problems
#         # to the terminal. They'll also be shown to the user.
#         else:
#             print(user_form.errors, profile_form.errors)

#     # Not a HTTP POST, so we render our form using two ModelForm instances.
#     # These forms will be blank, ready for user input.
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()

#     # Render the template depending on the context.
#     return render(request,
#                   'fungo/register.html',
#                   { 'user_form':    user_form,
#                     'profile_form': profile_form,
#                     'registered':   registered })

# def user_login(request):

#     # If the request is a HTTP POST, try to pull out the relevant
#     # information.
#     if request.method == 'POST':

#         # Gather the username and password provided by the user. This
#         # information is obtained from the login form.
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         # Use Django's machinery to attempt to see if the username/password
#         # combination is valid — a User object is returned if it is.
#         user = authenticate(username=username, password=password)

#         if user:
#             # Is the account active? It could have been disabled.
#             if user.is_active:
#                 # If the account is valid and active, we can log the user
#                 # in. We'll send the user back to the homepage.
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#             else:
#                 # An inactive account was used — no logging in!
#                 return HttpResponse("Your Fungo account is disabled.")
#         else:
#             # Bad login details were provided. So we can't log the user in.
#             print("Invalid login details: {0}, {1}".format(username, password))
#             return HttpResponse("Invalid login details supplied.")

#     # The request is not a HTTP POST, so display the login form. This
#     # scenario would most likely be a HTTP GET.
#     else:
#         # No context variables to pass to the template system, hence the
#         # blank dictionary object…
#         # TODO Can we use forms here instead of hardcoded fields?
#         return render(request, 'fungo/login.html', {})

# @login_required
# def user_logout(request):
#     # Since we know that the user is logged in, we can just log him out.
#     logout(request)

#     # Take the user back to homepage.
#     return HttpResponseRedirect(reverse('index'))

@login_required
def restricted(request):
    return render(request, 'fungo/restricted.html', {})

@login_required
def like_category(request):

    if request.method != 'GET':
        return HttpResponse(0)

    cat_id = request.GET['category_id']

    if not cat_id:
        return HttpResponse(0)

    cat = Category.objects.get(id=int(cat_id))

    if not cat:
        return HttpResponse(0)

    cat.likes += 1
    cat.save()

    print("going to return {0}".format(cat.likes))

    return HttpResponse(cat.likes)

def get_category_list(max_results=0, starts_with=''):
    return Category.objects.filter(
        name__istartswith=starts_with)[:max_results] if starts_with else []

def suggest_category(request):

    if request.method != 'GET':
        return HttpResponse()

    cats = get_category_list(3, request.GET['suggestion'])

    return render(request, 'fungo/cats.html', {'cats': cats})
