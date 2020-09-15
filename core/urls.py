from django.urls import path
from django.contrib.sitemaps.views import sitemap
from . import views
from core.sitemaps import StaticViewSitemap, ForumSiteMap
#TopicSiteMap


sitemaps = {

    'static': StaticViewSitemap,
    'forum': ForumSiteMap,
    # 'topic': TopicSiteMap

}

urlpatterns = [
    #path('user_licence_agreement/', views.license_view, name='licence'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
]
