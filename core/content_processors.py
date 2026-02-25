from core.forms import Searchbar

def shopping_cart_item_count(request):
    """
    sends the number of items in shopping cart to session so it don't check from database every page opened
    :param request:
    :return:
    """
    return {'cart_count': request.session.get('cart_count', 0)}

def navbar_search_form(request):
    """
    Sends search form to our layout.html
    :return: search form for navbar
    """
    form = Searchbar()
    return {"navbar_search_form": form}