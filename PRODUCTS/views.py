from django.views.generic import CreateView
from .models import Product
from .forms import ListProductForm


class ListProductView(CreateView):
    template_name = 'products/listing_page.html'
    queryset = Product.objects.all()
    form_class = ListProductForm
