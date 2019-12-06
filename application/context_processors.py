from .models import *

def add_variable_to_context(request):
    user_id_1 = request.COOKIES.get('user_id')
    user_1 = ""
    try:
        user_1 = User.objects.get(pk = user_id_1)
    except:
        pass

    if (user_1 == ""):
        return {}
    else:
        user_role = user_1.role
        return {
        'user_name' : user_1.name ,
        'user_role' : user_role ,
    }
    

    