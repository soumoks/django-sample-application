from django.urls import include,path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'questions',views.QuestionViewSet)
router.register(r'choices',views.ChoiceViewSet)

urlpatterns = [
# path('', views.index, name='index'),
path('',include(router.urls)),
path('get_questions',views.get_questions,name='get_questions'),
path('hello_world',views.return_hello_world,name='hello_world'),
path('<int:question_id>/',views.detail,name='detail')
]