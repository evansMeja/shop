def is_user(user):
	return user.is_authenticated and not user.is_staff