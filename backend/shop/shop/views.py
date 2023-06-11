from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.views import generic

from shop.custom_cart import CustomCart
from shop.forms import BookSearchForm, ModifiedUserCreationForm, PriceFilterForm, UserAddressForm
from shop.models import Book, Order, OrderItem
from shop.tasks import create_order_in_api as celery_create_order

User = get_user_model()


class Register(SuccessMessageMixin, generic.FormView):
    template_name = 'registration/register.html'
    form_class = ModifiedUserCreationForm
    success_url = reverse_lazy("home")
    success_message = 'Successfully registered, welcome!'

    def form_valid(self, form):
        user = form.save()
        user = authenticate(username=user.username, password=form.cleaned_data.get("password1"))
        login(self.request, user)
        return super(Register, self).form_valid(form)


class UserProfile(generic.DetailView):
    model = User
    template_name = "registration/profile.html"
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self, queryset=None):
        username = self.kwargs.get(self.slug_url_kwarg)
        user = get_object_or_404(User, username=username)
        return user


class BookList(generic.ListView):
    model = Book
    template_name = 'shop/home.html'
    context_object_name = 'books'
    paginate_by = 20
    ordering = ['title']

    def get_queryset(self):
        queryset = super().get_queryset()
        form = PriceFilterForm(self.request.GET)
        if form.is_valid():
            min_price = form.cleaned_data['min_price']
            max_price = form.cleaned_data['max_price']

            if min_price and max_price:
                queryset = queryset.filter(price__gte=min_price, price__lte=max_price).order_by('title')
            elif min_price:
                queryset = queryset.filter(price__gte=min_price)
            elif max_price:
                queryset = queryset.filter(price__lte=max_price)

        search_form = BookSearchForm(self.request.GET)
        if search_form.is_valid() and search_form.cleaned_data['search_query']:
            search_query = search_form.cleaned_data['search_query']
            queryset = queryset.filter(title__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = PriceFilterForm(self.request.GET)
        context['search_form'] = BookSearchForm(self.request.GET)
        return context


class OrderList(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'shop/my_orders.html'
    context_object_name = 'orders'
    ordering = ['-created_at', ]
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = context['orders']

        prefetch_order_items = Prefetch(
            'orderitem_set',
            queryset=OrderItem.objects.select_related('book'),
            to_attr='order_items'
        )
        orders = orders.prefetch_related(prefetch_order_items)

        context['orders'] = orders
        return context


@login_required(login_url=reverse_lazy('login'))
def cart_add(request, id):
    cart = CustomCart(request)
    product = Book.objects.get(id=id)
    cart.add(product=product)
    redirect_url = f"{reverse('home')}?{request.GET.urlencode()}"
    return redirect(redirect_url)


@login_required(login_url=reverse_lazy('login'))
def item_clear(request, id):
    cart = CustomCart(request)
    product = Book.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url=reverse_lazy('login'))
def item_increment(request, id):
    cart = CustomCart(request)
    product = Book.objects.get(id=id)
    cart.add(product=product)
    cart_items = request.session.get('cart')
    quantity = cart_items[f'{id}']['quantity']
    return JsonResponse({'quantity': quantity})


@login_required(login_url=reverse_lazy('login'))
def item_decrement(request, id):
    cart = CustomCart(request)
    product = Book.objects.get(id=id)
    cart.decrement(product=product)
    cart_items = request.session.get('cart')
    quantity = cart_items[f'{id}']['quantity']
    return JsonResponse({'quantity': quantity})


@login_required(login_url=reverse_lazy('login'))
def cart_clear(request):
    cart = CustomCart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url=reverse_lazy('login'))
def cart_detail_and_create_order(request):
    if request.method == 'POST':
        user_address_form = UserAddressForm(request.POST)
        cart = CustomCart(request)

        if user_address_form.is_valid():
            delivery_address = user_address_form.cleaned_data['delivery_address']

            if delivery_address:
                order_items = []
                order_items_dict = {}
                order = Order(user=request.user, delivery_address=delivery_address)

                for key, value in request.session.get('cart').items():
                    book = get_object_or_404(Book, id=key)
                    quantity_requested = value['quantity']

                    if quantity_requested > book.quantity:
                        messages.error(request, f"Cannot create order: {quantity_requested} {book.title} items are "
                                                f"temporary unavailable. Please try again later.")
                        return redirect('cart_detail')

                    order_items.append(OrderItem(order=order, book=book, quantity=quantity_requested))
                    order_items_dict[book.id_in_store] = quantity_requested

                order.save()
                OrderItem.objects.bulk_create(order_items)
                data = {
                    'user_email': request.user.email,
                    'delivery_address': delivery_address,
                    'order_id_in_shop': order.pk,
                    'order_items': order_items_dict
                }
                celery_create_order.delay(data)
                messages.success(request, "Order created successfully.")
                cart.clear()
                return redirect('home')

            else:
                messages.error(request, "Cannot create order: Delivery address is empty.")
                return redirect('cart_detail')
        else:
            messages.error(request, "Cannot create order: Invalid form data.")
            return redirect('cart_detail')

    else:
        user_address_form = UserAddressForm()

    context = {'user_address_form': user_address_form}
    return render(request, 'cart/cart_detail.html', context)
