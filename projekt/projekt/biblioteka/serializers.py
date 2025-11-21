from rest_framework import serializers
from .models import Book, Author, Genre, MONTHS, BOOK_FORMATS, Osoba, Stanowisko
from rest_framework.validators import UniqueTogetherValidator


# class BookSerializer(serializers.Serializer):
#     """Serializer dla modelu Book."""

#     # pole tylko do odczytu — ID książki
#     id = serializers.IntegerField(read_only=True)

#     # pole wymagane — tytuł książki
#     title = serializers.CharField(required=True)

#     # pole mapowane z klasy modelu, z podaniem wartości domyślnych
#     # zwróć uwagę na zapisywaną wartość do bazy dla default={wybór}[0] oraz default={wybór}[0][0]
#     # w pliku models.py BOOK_FROMATS oraz MONTHS zostały wyniesione jako stałe do poziomu zmiennych skryptu
#     # (nie wewnątrz modelu)

#     # pole z wyborem miesiąca publikacji
#     # MONTHS.choices pochodzi z modelu (Enum lub lista krotek)
#     publication_month = serializers.ChoiceField(choices=MONTHS.choices, default=MONTHS.choices[0][0])

#     # pole z wyborem formatu książki (np. Paperback, Hardcover, eBook)
#     # BOOK_FORMATS zostało zdefiniowane jako stała w models.py
#     book_format = serializers.ChoiceField(choices=BOOK_FORMATS, default=BOOK_FORMATS[0][0])

#     # odzwierciedlenie pola w postaci klucza obcego
#     # przy dodawaniu nowego obiektu możemy odwołać się do istniejącego poprzez inicjalizację nowego obiektu
#     # np. author=Author({id}) lub wcześniejszym stworzeniu nowej instancji tej klasy
#     # klucz obcy — autor książki (może być null)
#     author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), allow_null=True)

#     # klucz obcy — gatunek książki (może być null)
#     genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), allow_null=True)

#     # liczba dostępnych kopii książki
#     available_copies = serializers.IntegerField(default=1)

#     # przesłonięcie metody create() z klasy serializers.Serializer
#     # metoda create() — tworzenie nowego obiektu Book
#     def create(self, validated_data):
#         return Book.objects.create(**validated_data)

#     # przesłonięcie metody update() z klasy serializers.Serializer
#     # metoda update() — aktualizacja istniejącego obiektu Book
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.publication_month = validated_data.get('publication_month', instance.publication_month)
#         instance.book_format = validated_data.get('book_format', instance.book_format)
#         instance.author = validated_data.get('author', instance.author)
#         instance.genre = validated_data.get('genre', instance.genre)
#         instance.available_copies = validated_data.get('available_copies', instance.available_copies)
#         instance.save()
#         return instance

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        # musimy wskazać klasę modelu
        model = Book
        # definiując poniższe pole możemy określić listę właściwości modelu,
        # które chcemy serializować
        fields = ['id', 'title', 'publication_month', 'book_format', 'author', 'genre', 'available_copies']
        # definicja pola modelu tylko do odczytu
        read_only_fields = ['id']
    
    def validate_title(self, value):
        if not value[0].isupper():
            raise serializers.ValidationError(
                "Tytuł książki powinien rozpoczynać się wielką literą!"
            )
        return value
    
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        
        validators = [
            UniqueTogetherValidator(
                queryset=Author.objects.all(),
                fields=['first_name', 'last_name']
            )
        ]

    def validate(self, data):
        """
        Walidacja całego obiektu autora.
        Sprawdza poprawność formatu imienia, nazwiska i kodu kraju.
        """
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        country = data.get('country')

        # Imię i nazwisko powinny zaczynać się wielką literą
        if first_name and not (first_name[0].isupper() and first_name.isalpha()):
            raise serializers.ValidationError(
                {"first_name": "Imię powinno rozpoczynać się wielką literą!"}
            )

        if last_name and not (last_name[0].isupper() and last_name.isalpha()):
            raise serializers.ValidationError(
                {"last_name": "Nazwisko powinno rozpoczynać się wielką literą!"}
            )

        # Kod kraju: dokładnie 2 wielkie litery
        if country and (len(country) != 2 or not country.isupper()):
            raise serializers.ValidationError(
                {"country": "Kod kraju musi składać się z 2 wielkich liter, np. 'PL'."}
            )

        return data
    
    
def multiple_of_two(value):
    if value % 2 != 0:
        raise serializers.ValidationError("Ocena popularności musi być wielokrotnością 2 (np. 0, 2, 4, 6, 8, 10).")


class GenreSerializer(serializers.ModelSerializer):
    popularity_rank = serializers.IntegerField(validators=[multiple_of_two])
    
    class Meta:
        model = Genre
        fields = "__all__"


class OsobaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Osoba
        fields = "__all__"
        
    def validate_imie(self, value):
        if not (value[0].isupper() and value.isalpha()):
            raise serializers.ValidationError(
                "Imię powininno zawierać tylko litery i rozpoczynać się wielką literą!"
            )
        return value
    
    def validate_nazwisko(self, value):
        if not (value[0].isupper() and value.isalpha()):
            raise serializers.ValidationError(
                "Nazwisko powininno zawierać tylko litery i rozpoczynać się wielką literą!"
            )
        return value
    
class StanowiskoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stanowisko
        fields = "__all__"