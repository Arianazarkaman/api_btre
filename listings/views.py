from django.shortcuts import render, get_object_or_404
from .models import Listing
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .choices import price_choices, bedroom_choices, state_choices
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Listing
from .serializers import CustomListingSerializer
from django.core.cache import cache
from urllib.parse import urlencode
# def index(request):
#     listings = Listing.objects.order_by('-list_date').filter(is_published=True)
#     paginator = Paginator(listings, 6)
#     page = request.GET.get('page')
#     paged_listings = paginator.get_page(page)

#     context = {
#         'listings' : paged_listings
#     }
#     return render(request, 'listings/listings.html', context)
@api_view(['GET'])
def index(request):

    data = Listing.objects.order_by('-list_date').filter(is_published=True)
    serializer = CustomListingSerializer(data, many=True)

    return Response(serializer.data)

# def listing(request, listing_id):
#     listing = get_object_or_404(Listing, pk = listing_id)
#     context = {
#         'listing' : listing
#     }
#     return render(request, 'listings/listing.html', context)
@api_view(['GET'])
def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    serializer = CustomListingSerializer(listing)
    return Response(serializer.data)


def search(request):

    query_params = request.GET.dict()
    query_string = urlencode(query_params)
    cache_key = f"search:{query_string}"

    cached_response = cache.get(cache_key)
    if cached_response:
        print("🔁 Served from cache.")
        return cached_response
    else:
        print("💾 Cache miss — querying the database.")
        queryset_list = Listing.objects.order_by('-list_date')

        # Filter by keywords
        keywords = request.GET.get('keywords')
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

        # Filter by city
        city = request.GET.get('city')
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

        # Filter by state
        state = request.GET.get('state')
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

        # Filter by bedrooms
        bedrooms = request.GET.get('bedrooms')
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

        # Filter by price
        price = request.GET.get('price')
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

        context = {
            'state_choices': state_choices,
            'bedroom_choices': bedroom_choices,
            'price_choices': price_choices,
            'listings': queryset_list,
            'values': request.GET
        }

        response = render(request, 'listings/search.html', context)

        # Store in cache for future use
        cache.set(cache_key, response, timeout=600)

        return response
