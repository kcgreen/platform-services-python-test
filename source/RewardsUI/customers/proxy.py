'''
Created on Jun 29, 2018

@author: ken_green
'''
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from urllib.error import HTTPError
from urllib.request import urlopen, Request

@csrf_exempt
def proxy_to(request, target_url):
    # Initialize method, headers and body
    target_method = request.method
    target_headers = {}
    target_body = None
    # Setup request for methods: GET or DELETE
    if target_method in ('GET', 'DELETE'):
        if ('QUERY_STRING' in request.META) and ('' != request.META['QUERY_STRING']):
            target_url += '?' + request.META['QUERY_STRING']
    # Setup request for methods: POST or PUT
    elif target_method in ('POST', 'PUT'):
        if 'CONTENT_TYPE' in request.META:
            target_headers = {'Content-Type': request.META['CONTENT_TYPE']}
        target_body = request.body
    # No other methods allowed to proxy
    else:
        return HttpResponse("PROXYERROR: Invalid method.", status=400, content_type='text/plain')
    
    # Issue request and process response
    try:
        proxied_request = urlopen(Request(target_url, method=target_method, headers=target_headers, data=target_body))
        status_code = proxied_request.code
        content = proxied_request.read()
        if 'Content-Type' in proxied_request.headers:
            content_type = proxied_request.headers['Content-Type']
        else:
            content_type = 'text/plain'
    except HTTPError as e:
        return HttpResponse(e.msg, status=e.code, content_type='text/plain')
    else:
        return HttpResponse(content, status=status_code, content_type=content_type)