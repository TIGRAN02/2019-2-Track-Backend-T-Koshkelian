import factory
from chats.models import *
from users.models import *
from chats.factories import *


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    nick = factory.Faker('first_name')
    username = factory.LazyAttribute(lambda obj: obj.nick)
    tag = factory.LazyAttribute(lambda obj: '@{0}'.format(obj.nick).replace(" ", ""))
    password = factory.Faker('sentence', nb_words=1)
    bio = factory.Faker('sentence', nb_words=10)


class MemberFactory(factory.DjangoModelFactory):
    class Meta:
        model = Member

    user = factory.SubFactory(UserFactory)
    chat = factory.SubFactory(PersonalChatFactory)
