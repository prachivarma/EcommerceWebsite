from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import get_user_model
from .models import Shop, ShopOwnerBankDetails
from .forms import SellerRegisterForm

User = get_user_model()


@method_decorator([login_required, user_passes_test(lambda u: not u.is_seller)], name='dispatch')
class CreateSeller(CreateView):
    template_name = 'seller/seller_registration.html'
    form_class = SellerRegisterForm
    queryset = Shop.objects.all()
    success_url = '/'

    def form_valid(self, form):
        postForm = form.save(commit=False)
        user = get_object_or_404(User, id=self.request.user.id)
        user.is_seller = True
        user.save()
        postForm.shop_owner_id = self.request.user.id
        postForm.save()
        return super().form_valid(form)


@method_decorator([login_required, user_passes_test(lambda u: u.is_seller, login_url='/seller/register-shop/')], name='dispatch')
class SellerHomeView(TemplateView):
    template_name = 'seller/seller_home.html'
