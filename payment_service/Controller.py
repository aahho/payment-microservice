from django.http import JsonResponse
from django.core.paginator import Paginator
import json

def respondWithItem(statusCode, data, transformer):
    response = {}
    response['data'] = transformer.transform(data)
    
    response['notification'] = {}
    response['notification']['hint'] = "Response Sent"
    response['notification']['message'] = "Success"
    response['notification']['code'] = "200"
    response['notification']['type'] = "Success"
    
    return JsonResponse(response, content_type='application/json', status=statusCode)

def respondWithSuccess(statusCode, message, hint="Response Sent"):
    response = {}
    response['data'] = str(message)
    
    response['notification'] = {}
    response['notification']['hint'] = hint
    response['notification']['message'] = "Success"
    response['notification']['code'] = statusCode
    response['notification']['type'] = "Success"
    
    return JsonResponse(response, content_type='application/json', status=statusCode)

def respondWithList(statusCode, message, hint="Response Sent"):
    response = {}
    response['data'] = message
    
    response['notification'] = {}
    response['notification']['hint'] = hint
    response['notification']['message'] = "Success"
    response['notification']['code'] = statusCode
    response['notification']['type'] = "Success"
    
    return JsonResponse(response, content_type='application/json', status=statusCode)

def respondWithError(statusCode, message, hint="Something Went Wrong"):
    response = {}
    response['data'] = str(message)
    
    response['notification'] = {}
    response['notification']['hint'] = hint
    response['notification']['message'] = "Error"
    response['notification']['code'] = statusCode
    response['notification']['type'] = "Failed"
    
    return JsonResponse(response, content_type='application/json', status=statusCode)

def respondWithCollection(statusCode, data, transformer):
    response = {}
    response['data'] = fetchDataFromTransformer(transformer, data)
    
    response['notification'] = {}
    response['notification']['hint'] = "Response Sent"
    response['notification']['message'] = "Success"
    response['notification']['code'] = "200"
    response['notification']['type'] = "Success"
    
    return JsonResponse(response, content_type='application/json', status=statusCode)

def respondWithPaginatedCollection(request, statusCode, data, transformer):
    total_length = len(data)
    items = request.GET.get('items', '10')
    page = request.GET.get('page', '1')
    valid_page = total_length/int(items)

    if valid_page < int(page):
        page = 1

    if int(items) <= 0:
        items = 10

    if int(page) <= 0:
        page = 1     

    pages_possible = total_length/int(page)

    if not pages_possible:
        page = 1    

    url = 'http://' + request.META['HTTP_HOST'] + request.META['PATH_INFO'] + '?'

    meta = {}
    meta['total'] = total_length
    meta['count'] = total_length
    meta['current_page'] = page
    meta['per_page'] = items
    meta['next_link'] = ''
    meta['previous_link'] = ''

    paginator = Paginator(data, items)
    results = paginator.page(page)

    if results.has_next():
        if (total_length - int(items)) < int(items):
            new_items = total_length - int(items)
        else:
            new_items = items   
        new_page = int(page) + 1
        next_link =  url + 'items' + '=' + str(new_items) + '&' + 'page' + '=' + str(new_page)
        meta['next_link'] = next_link

    if results.has_previous:
        page = int(page) - 1
        if not page:
            page = 1
        previous_link =  url + 'items' + '=' + str(items) + '&' + 'page' + '=' + str(page)
        meta['previous_link'] = previous_link

    results = results.object_list

    response = {}
    response['data'] = fetchDataFromTransformer(transformer, results)
    response['meta'] = meta
    return JsonResponse(response, content_type='application/json', status=statusCode)
    
def fetchDataFromTransformer(transformer, data):
    result = []
    for key, value in enumerate(data):
        result.append(transformer.transform(value))
    return result
