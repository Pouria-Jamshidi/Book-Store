def shopping_cart_item_count(request):
    """
    sends the number of items in shopping cart to session so it don't check from database every page opened
    :param request:
    :return:
    """
    return {'cart_count': request.session.get('cart_count', 0)}
