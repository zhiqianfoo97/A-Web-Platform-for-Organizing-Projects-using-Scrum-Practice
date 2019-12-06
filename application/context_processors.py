from .models import *

def add_variable_to_context(request):
    context_var = {
        'user_name' : "" ,
        'user_role' : "" 
    }
    user_id_1 = request.COOKIES.get('user_id')
    if user_id_1:
        try:
            user_1 = User.objects.get(pk = user_id_1)
            user_role = user_1.role
            context_var["user_name"] = user_1.name
            context_var["user_role"] = user_role
        except:
            pass
    return context_var
