from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.template.context_processors import request
from django.views import generic
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import password_validation
from .models import Store, Category, Product, ProductPrice
from .utils import get_filtered_lowest_price, get_lowest_price_from_csv
from django.http import HttpResponse
from django.utils import timezone
from .forms import CsvPriceSearchForm, CategoryForm, ProductForm


# def index(request):
#     # return HttpResponse("Labas, pasauli!")
#     return render(request, template_name="index.html")

def index(request):
    num_stores = Store.objects.count()
    num_categories = Category.objects.count()
    num_products = Product.objects.count()
    context = {
        "num_stores": num_stores,
        "num_categories": num_categories,
        "num_products": num_products,
    }
    return render(request, template_name="index.html", context=context)


def resume(request):
    return render(request, template_name="resume.html")

def projects(request):
    return render(request, template_name="projects.html")

def contact(request):
    return render(request, template_name="contact.html")


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    try:
                        password_validation.validate_password(password)
                    except password_validation.ValidationError as e:
                        for error in e:
                            messages.error(request, error)
                        return redirect('register')
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'registration/register.html')


def search_price(request):
    result = None  # Numatytasis rezultatas
    search_performed = False  # Nurodo, ar paieška buvo atlikta

    if request.method == 'GET':
        # Gauname įvestis iš GET užklausos
        product_name = request.GET.get('product_name', '').strip()
        fat_content = request.GET.get('fat_content', '').strip()
        quantity = request.GET.get('quantity', '').strip()

        # Patikriname, ar visi kriterijai užpildyti
        if product_name and fat_content and quantity:
            search_performed = True  # Paieška atliekama
            file_path = "barbora_pienas.csv"  # CSV failo kelias
            result = get_filtered_lowest_price(file_path, product_name, fat_content, quantity)

    return render(request, 'search_price.html', {
        'result': result,
        'search_performed': search_performed,
    })



def search_price_view(request):
    categories = Category.objects.all()
    selected_category = None
    products = []
    result = None

    if request.method == "POST":
        if "select_category" in request.POST:
            category_id = request.POST.get("category")
            if category_id:
                selected_category = Category.objects.get(id=category_id)
                products = Product.objects.filter(category=selected_category)
                request.session["selected_category_id"] = category_id
                return render(request, "search_pricee.html", {
                    "step": 2,
                    "categories": categories,
                    "products": products,
                    "selected_category": selected_category,
                })

        elif "search_product" in request.POST:
            product_id = request.POST.get("product")
            if product_id:
                product = Product.objects.get(id=product_id)
                file_path = "barbora_pienas.csv"
                print(f"Searching for product: {product.name}")
                result = get_lowest_price_from_csv(file_path, product.name)
                print(f"Search result: {result}")

                selected_category_id = request.session.get("selected_category_id")
                if selected_category_id:
                    selected_category = Category.objects.get(id=selected_category_id)
                    products = Product.objects.filter(category=selected_category)

                return render(request, "search_pricee.html", {
                    "step": 2,
                    "categories": categories,
                    "products": products,
                    "selected_category": selected_category,
                    "result": result,
                })

    return render(request, "search_pricee.html", {
        "step": 1,
        "categories": categories,
        "products": products,
    })



def demo_search_view(request):
    form = CategoryForm(request.GET or None)
    form2 = ProductForm(request.POST or None)
    if request.method == 'POST':
        if form2.is_valid():
            product = form2.cleaned_data['product']
            print("product:", product)
            file_path = 'barbora_pienas.csv'  # Pakeiskite į savo CSV failo kelią
            result = get_lowest_price_from_csv(file_path, product.name)
            return render(request, 'demo_result.html', {

                'result': result,
            })

    if form.is_valid():
        category = form.cleaned_data['category']  # Pasirinkta kategorija
        print(f"Selected category: {category}")  # Debug eilutė

        # Filtruojame produktus pagal pasirinktą kategoriją
        products = Product.objects.filter(category=category)
        print(f"Filtered products: {products}")  # Debug eilutė



        # Užpildome 'product' lauką su naujai užpildytu produktų sąrašu
        form2.fields['product'].queryset = products

        # # Jei formoje pasirinktas produktas, atliekame paiešką
        # if 'product' in form.cleaned_data:
        #     product = form.cleaned_data['product']
        #     search_performed = True
        #     file_path = 'barbora_pienas.csv'  # Pakeiskite į savo CSV failo kelią
        #     result = get_lowest_price_from_csv(file_path, product.name)

        return render(request, 'demo_search.html', {
            'form': form,
            'form2': form2,
        })

    return render(request, 'demo_search.html', context={"form": form})