from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template.context_processors import request
from django.urls import reverse
from django.views import generic
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import password_validation
from .models import Store, Category, Product, ProductPrice, ShoppingCart, SavedResult
from .utils import get_filtered_lowest_price, get_lowest_price_from_csv
from .forms import UserUpdateForm, ProfileUpdateForm
from django.http import HttpResponse
from django.utils import timezone


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


class MyShoppingCartListView(LoginRequiredMixin, generic.ListView):
    model = ShoppingCart
    template_name = "my_shopping_cart.html"
    context_object_name = "carts"
    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class MyShoppingCartDetailView(generic.DetailView):
    model = ShoppingCart
    template_name = "my_shopping_cart_detail.html"
    context_object_name = "cart"


class MyShoppingCartCreateView(LoginRequiredMixin, generic.CreateView):
    model = ShoppingCart
    template_name = "my_shopping_cart_form.html"
    fields = ["name"]
    success_url = "/myshoppingcart/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class MyShoppingCartUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ShoppingCart
    template_name = "my_shopping_cart_form.html"
    fields = ['name']
    success_url = "/myshoppingcart/"


class MyShoppingCartDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ShoppingCart
    template_name = "my_shopping_cart_delete.html"
    context_object_name = 'cart'
    success_url = "/myshoppingcart/"


class MyProductCreatView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = SavedResult
    template_name = "my_product_form.html"
    fields = ['name', 'store', 'price']

    def get_success_url(self):
        return reverse("cart", kwargs={"pk": self.kwargs['cart_id']})

    def test_func(self):
        return ShoppingCart.objects.get(pk=self.kwargs['cart_id']).user == self.request.user

    def form_valid(self, form):
        form.instance.cart = ShoppingCart.objects.get(pk=self.kwargs['cart_id'])
        return super().form_valid(form)


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


@login_required
def profile(request):
    if request.method == "POST":
        new_email = request.POST['email']
        new_first_name = request.POST['first_name']
        new_last_name = request.POST['last_name']
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if request.user.email != new_email and User.objects.filter(email=new_email).exists():
            messages.error(request, f"Vartotojas su el. paštu {new_email} jau užregistruotas!")
            return redirect("profile")
        if user_update_form.is_valid() and profile_update_form.is_valid():
            request.user.first_name = new_first_name
            request.user.last_name = new_last_name
            user_update_form.save()
            messages.info(request, "Profilis atnaujintas")
            return redirect("profile")
    user_update_form = UserUpdateForm(instance=request.user)
    profile_update_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form,
    }
    return render(request, template_name="profile.html", context=context)

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
    results = []
    searched_product = None
    user_carts = ShoppingCart.objects.filter(user=request.user) if request.user.is_authenticated else None

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
                    "results": results,
                    "searched_product": searched_product,
                })

        elif "search_product" in request.POST:
            product_id = request.POST.get("product")
            if product_id:
                product = Product.objects.get(id=product_id)
                searched_product = product.name
                csv_files = ["barbora_pienas.csv", "rimi_pienas.csv"]

                for file_path in csv_files:
                    store_name = file_path.split("_")[0].capitalize()
                    result = get_lowest_price_from_csv(file_path, product.name)

                    if result:
                        results.append({
                            "id": len(results) + 1,  # Pridedame rezultatų ID
                            "store": store_name,
                            "name": result["name"],
                            "price": result["price"]
                        })

                # Įrašome rezultatus į sesiją
                request.session["results"] = results

                selected_category_id = request.session.get("selected_category_id")
                if selected_category_id:
                    selected_category = Category.objects.get(id=selected_category_id)
                    products = Product.objects.filter(category=selected_category)

                return render(request, "search_pricee.html", {
                    "step": 2,
                    "categories": categories,
                    "products": products,
                    "selected_category": selected_category,
                    "results": results,
                    "searched_product": searched_product,
                    "user_carts": user_carts,  # Pridedame vartotojo krepšelius
                })

        elif "save_results" in request.POST:
            if not request.user.is_authenticated:
                messages.error(request, "Turite prisijungti, kad galėtumėte išsaugoti rezultatus.")
                return redirect("login")

            results = request.session.get("results", [])  # Atkuriame sesijoje saugotus rezultatus
            selected_ids = request.POST.getlist("selected_results")
            cart_id = request.POST.get("cart_id")

            if not cart_id:
                messages.error(request, "Pasirinkite pirkinių krepšelį, į kurį norite išsaugoti rezultatus.")
                return redirect("search_price_view")

            shopping_cart = get_object_or_404(ShoppingCart, pk=cart_id, user=request.user)

            if selected_ids:
                for selected_id in selected_ids:
                    # Susirandame pasirinktą rezultatą pagal ID
                    selected_result = next((r for r in results if str(r["id"]) == selected_id), None)
                    if selected_result:
                        SavedResult.objects.create(
                            user=request.user,  # Priskiriame prisijungusį vartotoją
                            store=selected_result["store"],
                            name=selected_result["name"],
                            price=selected_result["price"],
                            cart=shopping_cart,
                        )
                messages.success(request, f"Pasirinkti rezultatai buvo išsaugoti krepšelyje: {shopping_cart.name}!")
            else:
                messages.warning(request, "Nepasirinkote jokių rezultatų!")

    return render(request, "search_pricee.html", {
        "step": 1,
        "categories": categories,
        "products": products,
        "results": results,
        "searched_product": searched_product,
        "user_carts": user_carts,  # Vartotojo krepšelių sąrašas
    })
