from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import ProfileForm
from .models import UserProfile, UserCart
from PRODUCT.models import Product
from django.contrib.auth import get_user_model
from django.db.models import F

User = get_user_model()


@login_required
def user_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=UserProfile.objects.get(user=request.user))
        if form.is_valid():
            form.save()
            return redirect('homepage')
        else:
            return HttpResponse('err')
    else:
        form = ProfileForm(instance=UserProfile.objects.get(user=request.user))
        return render(request, 'user/profile.html', {'form': form})


def cart(request):
    if request.user.is_authenticated:
        cart_items = UserCart.objects.filter(user_id=request.user.id)
        cart_price = cart_items.values_list('cart_item__product_selling_price', 'quantity')
        amt = sum([i[0] * i[1] for i in cart_price])
        context = {
            'cart_items': cart_items,
            'cart_price': amt,
        }
        return render(request, 'user/cart.html', context)
    else:
        products = request.session.get('cart')
        if products:
            cart_items = {Product.objects.get(pk=item['pk']): item['quantity'] for item in products}
            amt = sum([item['quantity'] * item['price'] for item in products])
            context = {
                'cart_items': cart_items,
                'cart_price': amt,
            }
            return render(request, 'user/unauth_cart.html', context)
        else:
            return render(request, 'user/unauth_cart.html')


def add_item_to_cart(request):
    if request.is_ajax():
        pk = request.GET.get('pk')
        if request.user.is_authenticated:
            item = UserCart.objects.filter(cart_item_id=pk, user_id=request.user.id)
            if not item.exists():
                obj = UserCart.objects.create(
                    user=request.user,
                    cart_item=Product.objects.get(pk=pk)
                )
                obj.save()
            else:
                item.update(quantity=F('quantity') + 1)
            return HttpResponse('ok', status=200)
        else:
            user = request.session.get('user', default=None)
            if user:
                item = request.session.get('cart')
                item.append({'pk': pk, 'quantity': 1, 'price': Product.objects.get(pk=pk).product_selling_price})
                request.session.update({'cart': item})
            else:
                request.session['user'] = str(request.user)
                request.session['cart'] = [{'pk': pk, 'quantity': 1, 'price': Product.objects.get(pk=pk).product_selling_price}]
            return HttpResponse('session-updated', status=200)


def change_quantity(request):
    if request.is_ajax():
        pk = request.GET.get('pk')
        action = request.GET.get('action')
        if request.user.is_authenticated:
            item = UserCart.objects.filter(cart_item_id=pk, user_id=request.user.id)
            q = item.values('quantity')[0]
            if action == 'increment':
                item.update(quantity=F('quantity') + 1)
                return JsonResponse({'status': 200}, safe=False, status=200)
            elif action == 'decrement':
                if q['quantity']:
                    item.update(quantity=F('quantity') - 1)
                    return JsonResponse({'status': 200}, safe=False, status=200)
                else:
                    return JsonResponse({'status': 200, 'message': 'no more decrement possible'}, safe=False, status=200)
        else:
            cart_item = request.session.get('cart', default=None)
            if action == 'increment':
                for i in range(len(cart_item)):
                    if cart_item[i]['pk'] == pk:
                        request.session['cart'][i]['quantity'] += 1
                        request.session.save()
                        return JsonResponse('ok', safe=False)
            elif action == 'decrement':
                for i in range(len(cart_item)):
                    if cart_item[i]['pk'] == pk:
                        if request.session['cart'][i]['quantity'] > 1:
                            request.session['cart'][i]['quantity'] -= 1
                            request.session.save()
                            return JsonResponse('ok', safe=False)
                        else:
                            del request.session['cart'][i]
                            request.session.save()
                            return JsonResponse('deleted', safe=False)


def remove_cart_item(request):
    if request.is_ajax():
        pk = request.GET.get('pk')
        if request.user.is_authenticated:
            UserCart.objects.filter(cart_item_id=pk, user_id=request.user.id).delete()
            return JsonResponse({'status': 200}, safe=False, status=200)
        else:
            cart_item = request.session.get('cart', default=None)
            for i in range(len(cart_item)):
                if cart_item[i]['pk'] == pk:
                    del request.session['cart'][i]
                    request.session.save()
                    return JsonResponse('deleted', safe=False)


def is_item_in_cart(request):
    if request.is_ajax():
        pk = request.GET.get('pk')
        if not request.user.is_authenticated:
            cart_item = request.session.get('cart', default=None)
            try:
                for item in cart_item:
                    if item['pk'] == pk:
                        return JsonResponse('found', safe=False)
                return JsonResponse('not found', safe=False)

            except (ValueError, TypeError):
                return JsonResponse('not found', safe=False)
        else:
            if UserCart.objects.filter(cart_item_id=pk).exists():
                return JsonResponse('found', safe=False)
            else:
                return JsonResponse('not found', safe=False)


def verify_otp(request):
    request.session['phone_number'] = request.GET.get('phone_number')
    return JsonResponse('ok', safe=False)
