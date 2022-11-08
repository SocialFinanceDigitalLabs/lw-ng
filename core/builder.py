import itertools
from collections import defaultdict
from typing import Union

from django.contrib.auth import get_user_model
from faker import Faker

from core.models import Manager, PersonalAdvisor, YoungPerson

User = get_user_model()


class SubArgs(dict):
    def __init__(self, kwargs):
        self.__kwargs = defaultdict(dict)
        main_args = {}
        for k, v in kwargs.items():
            if "__" in k:
                group, key = k.split("__", 1)
                self.__kwargs[group][key] = v
            else:
                main_args[k] = v
        super().__init__(self, **main_args)

    def __getattr__(self, name):
        return self.__kwargs[name]


class Builder:
    def __init__(self, seed=100):
        super().__init__()
        self._user_count = itertools.count()
        Faker.seed(seed)
        self.fake = Faker("en-GB")
        self.random = self.fake.random
        self._sequence_reset = False

    def user(
        self,
        faker=True,
        **kwargs,
    ) -> User:
        """
        Create a user. Pass 'faker=False' to use test-friendly values
        """
        user_count = next(self._user_count)

        default_props = dict(username=f"user-{user_count}")
        if faker:
            default_props["first_name"] = self.fake.first_name()
            default_props["last_name"] = self.fake.last_name()
            default_props["email"] = self.fake.email()
        else:
            default_props["first_name"] = f"FirstName{user_count}"
            default_props["last_name"] = f"LastName{user_count}"
            default_props["email"] = f"user{user_count}@leavingwell.test"

        default_props.update(kwargs)

        return User.objects.create_user(**default_props)

    def young_person(
        self, user: User = None, pa: Union[PersonalAdvisor, bool] = None, **kwargs
    ) -> YoungPerson:
        """
        Create a young person.

        If 'pa' is True, a personal advisor will be created for the young person, or pass a PersonalAdvisor instance
        as pa.
        """
        kwargs = SubArgs(kwargs)

        if not user:
            user = self.user(**kwargs.user)

        if isinstance(pa, bool) and pa:
            pa = self.personal_advisor(**kwargs.pa)

        default_props = dict()
        default_props.update(kwargs)

        yp = YoungPerson.objects.create(user=user, **kwargs)
        if pa:
            yp.personal_advisors.add(pa)
        return yp

    def personal_advisor(
        self, user: User = None, manager: Union[Manager, bool] = None, **kwargs
    ) -> PersonalAdvisor:
        """
        Create a personal advisor.
        """
        kwargs = SubArgs(kwargs)

        if not user:
            user = self.user(**kwargs.user)

        if isinstance(manager, bool) and manager:
            manager = self.manager(**kwargs.manager)

        default_props = dict()
        default_props.update(kwargs)

        return PersonalAdvisor.objects.create(
            user=user, manager=manager, **default_props
        )

    def manager(self, user: User = None, **kwargs) -> Manager:
        """
        Create a manager.
        """
        kwargs = SubArgs(kwargs)

        if not user:
            user = self.user(**kwargs.user)

        default_props = dict()
        default_props.update(kwargs)

        return Manager.objects.create(user=user, **default_props)
