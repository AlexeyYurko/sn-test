from django.shortcuts import render


def bot_home(request):
    return render(request, '../templates/bot_home.html', {})
