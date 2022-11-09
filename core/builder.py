import itertools
import random
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

        default_props = dict()
        if faker:
            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            default_props["first_name"] = first_name
            default_props["last_name"] = last_name
            default_props["email"] = self.fake.email()
            default_props["username"] = f"{first_name}-{last_name}"
        else:
            default_props["first_name"] = f"FirstName{user_count}"
            default_props["last_name"] = f"LastName{user_count}"
            default_props["username"] = f"user-{user_count}"
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


def create_random_users(manager_count: int, pa_count: int, yp_count: int) -> list[dict]:
    """creates a few manager users, each with a number of PAs and YPs associated with"""
    builder = Builder(seed=random.randint(0, 1000))
    data = []
    for _ in range(manager_count):
        manager = builder.manager(user__password="test")
        manager_data = {
            "manager": manager.user.username,
            "pas": [],
        }
        for _ in range(pa_count):
            pa = builder.personal_advisor(
                user__password="test",
                manager=manager,
            )
            pa_data = {"pa": pa.user.username, "yps": []}
            for _ in range(yp_count):
                yp = builder.young_person(user__password="test", pa=pa)
                pa_data["yps"].append(yp.user.username)
            manager_data["pas"].append(pa_data)
        data.append(manager_data)
    return data
