from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import CoursesViewSet, LessonsViewSet

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r"courses", CoursesViewSet, basename="courses")
router.register(r"lessons", LessonsViewSet, basename="lessons")
urlpatterns = router.urls
