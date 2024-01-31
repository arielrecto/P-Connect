from django import template


register = template.Library()



@register.filter(name="user_in_group")
def is_user_in_group(user, group):
    return group.users.filter(id=user.id).exists()


@register.filter(name="owner_group")
def is_user_in_group(user, group):
    return user.id == group.owner.id