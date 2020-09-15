from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from forums.models import Forum, Topic


class StaticViewSitemap(Sitemap):

    def items(self):
        return ['index', 'register', 'login', 'logout',
        'licence', 'create_forum']

    def location(self, item):
        return reverse(item)


class ForumSiteMap(Sitemap):

    def items(self):
        return Forum.objects.all()

# class TopicSiteMap(Sitemap):
#
#     def items(self):
#         return Topic.objects.all()
