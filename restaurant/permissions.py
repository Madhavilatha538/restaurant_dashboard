from django.contrib.auth.decorators import user_passes_test

def in_group(group_name: str):
    return user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.groups.filter(name=group_name).exists()))
