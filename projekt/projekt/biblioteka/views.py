
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Book
from .serializers import BookSerializer
from django.http import HttpResponse
import datetime
from django.http import Http404, HttpResponse
from .models import Osoba
from .forms import OsobaForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required



# określamy dostępne metody żądania dla tego endpointu
@api_view(['GET', "POST"])
def book_list(request):
    """
    Lista wszystkich obiektów modelu Book.
    """
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def book_detail(request, pk):

    """
    :param request: obiekt DRF Request
    :param pk: id obiektu Book
    :return: Response (with status and/or object/s data)
    """
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    """
    Zwraca pojedynczy obiekt typu Book.
    """
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)


@api_view(['PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_update_delete(request, pk):

    """
    :param request: obiekt DRF Request
    :param pk: id obiektu Book
    :return: Response (with status and/or object/s data)
    """
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def welcome_view(request):
    now = datetime.datetime.now()
    html = f"""
        <html><body>
        Witaj użydkowniku! </br>
        Aktuanalna data i czas na srerwerze: {now}
        </body></html>"""
    return HttpResponse(html)

# pominięto inne importy
from .models import Osoba, Stanowisko

# pominięto definicję innych widoków
@login_required(login_url='user-login')
def osoba_list_html(request):
    # pobieramy wszystkie obiekty Osoba z bazy poprzez QuerySet
    osoby = Osoba.objects.all()
    #return HttpResponse(osoby)
    return render(request,
                  "biblioteka/osoba/list.html",
                  {'osoby' : osoby})

def osoba_detail_html(request, id):
    # pobieramy konkretny obiekt Osoba
    try:
        osoba = Osoba.objects.get(id=id)
    except Osoba.DoesNotExist:
        raise Http404("Obiekt Osoba o podanym id nie istnieje")

    if request.method == "GET":
        return render(request,
                    "biblioteka/osoba/detail.html",
                    {'osoba': osoba})
    if request.method == "POST":
        osoba.delete()
        return redirect('osoba-list') 
            

def osoba_create_html(request):
    stanowiska = Stanowisko.objects.all()  # pobieramy listę stanowisk z bazy

    if request.method == "GET":
        return render(request, "biblioteka/osoba/create.html", {'stanowiska': stanowiska})
    elif request.method == "POST":
        imie = request.POST.get('imie')
        nazwisko = request.POST.get('nazwisko')
        plec = request.POST.get('plec')
        stanowisko_id = request.POST.get('stanowisko')

        if imie and nazwisko and plec and stanowisko_id:
            # pobieramy obiekt stanowiska
            try:
                stanowisko_obj = Stanowisko.objects.get(id=stanowisko_id)
            except Stanowisko.DoesNotExist:
                error = "Wybrane stanowisko nie istnieje."
                return render(request, "biblioteka/osoba/create.html", {'error': error, 'stanowiska': stanowiska})

            # tworzymy nową osobę
            Osoba.objects.create(
                imie=imie,
                nazwisko=nazwisko,
                plec=plec,
                stanowisko=stanowisko_obj
            )
            return redirect('osoba-list')
        else:
            error = "Wszystkie pola są wymagane."
            return render(request, "biblioteka/osoba/create.html", {'error': error, 'stanowiska': stanowiska})

def osoba_create_django_form(request):
    if request.method == "POST":
        form = OsobaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('osoba-list')  
    else:
        form = OsobaForm()

    return render(request,
                  "biblioteka/osoba/create_django.html",
                  {'form': form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('osoba-list')
        else:
            return render(request, 'biblioteka/login.html', {'error': 'Nieprawidłowe dane'})
    return render(request, 'biblioteka/login.html')

def user_logout(request):
    logout(request)
    return redirect('user-login')

from django.core.exceptions import PermissionDenied

@login_required(login_url='user-login')
def osoba_view(request, pk):
    if not request.user.has_perm('biblioteka.view_osoba'):
        raise PermissionDenied()
    try:
        osoba = Osoba.objects.get(pk=pk)
        return HttpResponse(f"Ten użytkownik nazywa się {osoba.imie} {osoba.nazwisko}")
    except Osoba.DoesNotExist:
        return HttpResponse(f"W bazie nie ma użytkownika o id={pk}.")
    
    from django.contrib.auth.decorators import permission_required

@login_required(login_url='user-login')
@permission_required('biblioteka.view_osoba', raise_exception=True)
def osoba_view_decorator(request, pk):
    try:
        osoba = Osoba.objects.get(pk=pk)
        return HttpResponse(f"Ten użytkownik nazywa się {osoba.imie} {osoba.nazwisko}")
    except Osoba.DoesNotExist:
        return HttpResponse(f"W bazie nie ma użytkownika o id={pk}.")