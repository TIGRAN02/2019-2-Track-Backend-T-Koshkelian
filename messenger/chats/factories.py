import factory
from chats.models import *
from users.models import *


class PersonalChatFactory(factory.DjangoModelFactory):
    class Meta:
        model = Chat

    name = factory.Faker('sentence', nb_words=2)
    tag = factory.LazyAttribute(lambda obj, n: '@%s%d' % obj.name.replace(" ", "") % n)
    bio = factory.Faker('sentence', nb_words=15)
    last_message = factory.Faker('sentence', nb_words=8)


class GroupChatFactory(factory.DjangoModelFactory):
    class Meta:
        model = Chat

    name = factory.Faker('sentence', nb_words=2)
    tag = factory.LazyAttribute(lambda obj, n: '@%s%d' % obj.name.replace(" ", "") % n)
    is_group = True
    bio = factory.Faker('sentence', nb_words=15)
    last_message = factory.Faker('sentence', nb_words=8)


class ChannelFactory(factory.DjangoModelFactory):
    class Meta:
        model = Chat

    name = factory.Faker('sentence', nb_words=2)
    tag = factory.LazyAttribute(lambda obj, n: '@%s%d' % obj.name.replace(" ", "") % n)
    is_channel = True
    bio = factory.Faker('sentence', nb_words=15)
    last_message = factory.Faker('sentence', nb_words=8)