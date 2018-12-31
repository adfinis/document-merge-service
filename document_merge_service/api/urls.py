from rest_framework.routers import SimpleRouter

r = SimpleRouter(trailing_slash=False)
urlpatterns = r.urls
