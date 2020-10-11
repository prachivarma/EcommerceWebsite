from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from .models import Product
from .forms import ListProductForm, UpdateProductForm

User = get_user_model()


@method_decorator([login_required, user_passes_test(lambda u: u.is_seller, login_url='/seller/register-shop/')], name='dispatch')
class ListProductView(CreateView):
    template_name = 'products/listing_page.html'
    queryset = Product.objects.all()
    form_class = ListProductForm

    def form_valid(self, form):
        postForm = form.save(commit=False)
        postForm.product_shop_id = self.request.user.shop.id
        postForm.save()
        messages.success(self.request, 'Product added to inventory.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('list_product')


@method_decorator([login_required, user_passes_test(lambda u: u.is_seller, login_url='/seller/register-shop/')], name='dispatch')
class InventoryListView(ListView):
    template_name = 'products/inventory_page.html'
    model = Product
    paginate_by = 20
    ordering = '-id'


class UpdateProductView(UpdateView):
    template_name = 'products/update_listing_page.html'
    form_class = UpdateProductForm

    def form_valid(self, form):
        if form.cleaned_data['is_product_live'] and self.object.is_product_verified:
            messages.success(self.request, 'Yehh your product is live ...')
            return super(UpdateProductView, self).form_valid(form)
        else:
            postForm = form.save(commit=False)
            postForm.is_product_live = False
            postForm.save()
            messages.warning(self.request, "You can't set product to live until is verified")
            return super(UpdateProductView, self).form_valid(form)

    def get_object(self, queryset=None):
        product = get_object_or_404(Product, id=self.kwargs['id'])
        return product

    def get_success_url(self):
        return reverse('inventory_page')


@method_decorator([login_required, user_passes_test(lambda u: u.is_seller, login_url='/seller/register-shop/')], name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('inventory_page')
    template_name = 'products/confirm_listing_delete.html'

    def get_object(self, queryset=None):
        product = get_object_or_404(Product, id=self.kwargs['id'])
        return product
