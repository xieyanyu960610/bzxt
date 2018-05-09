import xadmin
from xadmin import views

class BaseSetting(object):
    enable_themes =True
    use_bootswatch = True
    menu_style = "accordion"


xadmin.site.register(views.BaseAdminView,BaseSetting)