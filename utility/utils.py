from django.db.models import Avg, Exists, OuterRef
from sales.models import OrderItems, StatusChoices



def apply_sort_and_filter(request, queryset, form):
    """
    Applies sorting and ownership filtering to a Book queryset.
    Ownership is handled internally.
    """

    # ================= Checking Validations =================
    if not form.is_valid():
        return queryset

    # ======================= SORTING ========================
    sort = request.GET.get("sort")

    if sort:

        if sort == "name":
            queryset = queryset.order_by("title")

        elif sort == "-name":
            queryset = queryset.order_by("-title")

        elif sort == "price":
            queryset = queryset.order_by("price")

        elif sort == "-price":
            queryset = queryset.order_by("-price")

        elif sort == "created_at":
            queryset = queryset.order_by("created_at")

        elif sort == "-created_at":
            queryset = queryset.order_by("-created_at")

        elif sort == "score":
            queryset = queryset.annotate(
                avg_score=Avg("scores__score")
            ).order_by("avg_score")

        elif sort == "-score":
            queryset = queryset.annotate(
                avg_score=Avg("scores__score")
            ).order_by("-avg_score")


    # ================= OWNERSHIP FILTER =================
    # Adds a annotated colum to queryset, that has True for owned books and False for not owned books
    # filtering based on it, can show us the owned or not owned ones.
    only_unowned = request.GET.get("only_unowned")

    if request.user.is_authenticated and only_unowned :

        owned_books = OrderItems.objects.filter(
            order__user=request.user,
            order__status=StatusChoices.PAID,
            book=OuterRef("pk")
        )

        queryset = queryset.annotate(
            is_owned=Exists(owned_books)
        )


        queryset = queryset.filter(is_owned=False)

    return queryset