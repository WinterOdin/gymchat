import factory
from factory.faker import faker
from user_mgmt.models import Profile, User, Location, Gym, UserPhoto, Exercise, FavoriteExercise
from factory.django import DjangoModelFactory
from django.core.management import call_command
from random import choice
from django.db import IntegrityError
import datetime

FAKE = faker.Faker()

class LocationFactory(DjangoModelFactory):

    class Meta:
        model = Location

    city = factory.LazyAttribute(lambda o: FAKE.city())
    street = factory.LazyAttribute(lambda o: FAKE.street_name())
    state = factory.LazyAttribute(lambda o: FAKE.city_suffix())
    country = factory.LazyAttribute(lambda o: FAKE.country())
    placeId = factory.LazyAttribute(lambda o: FAKE.pystr())
    latitude = factory.LazyAttribute(lambda o: FAKE.latitude())
    longitude = factory.LazyAttribute(lambda o: FAKE.longitude())

class GymFactory(DjangoModelFactory):
    
    class Meta:
        model = Gym
    
    name = factory.Faker(
        'random_element', elements=[x for x in ['CityFit', 'JustGym', 'ZdroFit', 'Paco']]
    )
    place = factory.SubFactory(LocationFactory)

class ProfileFactory(DjangoModelFactory):
    
    class Meta:
        model = Profile
    
    gender = factory.Faker(
        'random_element', elements=[x[0] for x in Profile.GENDER]
    )
    bio = factory.LazyAttribute(lambda o: FAKE.paragraph(nb_sentences=5, ext_word_list=['abc', 'def', 'ghi', 'jkl']))
    playlist = factory.Faker(
        'random_element', elements=[x for x in ['spotify', 'apple', 'tidal']]
    )
    gym = factory.RelatedFactory(
        GymFactory,
        factory_related_name = 'profile'
    )


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User

    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    birthday = factory.Faker('date_object')
    current_location = factory.SubFactory(LocationFactory)
    age = factory.Faker('pyint', min_value=18, max_value=100)
    search_range = factory.Faker('pyint', min_value=10, max_value=150)
    password = factory.LazyAttribute(lambda o: FAKE.password())
    is_staff = False
    is_active = True

    profile = factory.RelatedFactory(
        ProfileFactory,
        factory_related_name = 'user'
    )


def populate():

    #clear out old data
    Exercise.objects.all().delete()
    FavoriteExercise.objects.all().delete()
    UserPhoto.objects.all().delete()

    try:
        User.objects.get(email='adminDev@gmail.com').delete()
        print('User was found and removed.')              
    except:
        print('User was not removed.')


    picture_list = ['https://picsum.photos/seed/picsum/200/300', 'https://picsum.photos/seed/pssss/200/300', 'https://picsum.photos/seed/picwum/200/300']

    call_command('loaddata', 'exercises/converted.json')
    all_users = User.objects.all()
    exercise_pks = Exercise.objects.values_list('pk', flat=True)

    for x in all_users:
        
        for order in range(1, len(picture_list)+1):
            UserPhoto.objects.create(user=x, order=order, url=picture_list[order-1])
        
        random_pk = choice(exercise_pks)
        random_exercise = Exercise.objects.get(pk=random_pk)
        FavoriteExercise.objects.create(user=x, exercise=random_exercise)

    try:
        superuser = User.objects.create_superuser(
            first_name='dev',
            email='adminDev@gmail.com',
            password='adminDev',
            birthday=datetime.date(1993, 12, 1))
        superuser.save()
    except IntegrityError:
        print('That superuser already exists.')
    except Exception as e:
        print(e)
    