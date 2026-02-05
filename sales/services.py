from django.db.models import Sum
from sales.models import OrderItems, StatusChoices

def update_cart_cache(request):
    """
    Update request.session['cart_count'] to the current total quantity of items
    in the user's pending order. Sets 0 for anonymous users.
    Returns the computed count (int).
    """
    if not request.user.is_authenticated:
        request.session['cart_count'] = 0
        return 0

    total = (
        OrderItems.objects
        .filter(order__user=request.user, order__status=StatusChoices.PENDING)
        .aggregate(total_qty=Sum('quantity'))['total_qty'] or 0
    )

    # ensure serializable int
    request.session['cart_count'] = int(total)
    # optionally mark session modified (not necessary when setting a key)
    request.session.modified = True
    return int(total)
