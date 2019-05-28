from rest_framework import permissions

class IsCommercialOrReadOnly(permissions.BasePermission):
	
	def has_permission(self,request,view):
		if request.method in permissions.SAFE_METHODS:
			return True
		return (request.user.groups.filter(name='commercial').exists() or request.user.is_staff)
