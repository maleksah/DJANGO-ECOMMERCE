from django.conf.urls import patterns, url


urlpatterns = patterns('articles.views',
    url(r'^articles_cat/(?P<cat>\d+)/$','articlesByCat'),
    url(r'^article/(?P<id>\d+)-(?P<slug>.+)$','articleById'),
    url(r'^rechercher/$','rechercher_produit'),
)