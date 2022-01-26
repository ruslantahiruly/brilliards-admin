from django.urls import reverse
from django.contrib.sitemaps import Sitemap
from .models import Club

class ClubsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    def items(self):
        return Club.objects.filter(is_verified=True).filter(is_active=True)

class StaticViewSitemap(Sitemap):
    priority = 0.5
    def items(self):
        return ['clubs:index',]
    def location(self, item):
        return reverse(item)
