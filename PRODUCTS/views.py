from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView, ListView
from django.contrib.auth import get_user_model
from .models import Product
from .forms import ListProductForm

User = get_user_model()


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


class InventoryListView(ListView):
    template_name = 'products/inventory_page.html'
    model = Product
    paginate_by = 20
