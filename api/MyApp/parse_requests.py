def pares_post_request(request):
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    return data
