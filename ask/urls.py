from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from ask.views import new, hot, tag, question, login, logout, signup, ask, settings, hello, rate_question,\
    rate_answer, mark_answer

urlpatterns = [
    url(r'^$', new, name='new-questions'),
    url(r'^hot/?', hot, name='hot-questions'),
    url(r'^tag/(?P<tag>\w+)/?', tag, name='tag-questions'),
    url(r'^question/(?P<qid>\d+)/?', question, name='question'),
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^signup/', signup, name='signup'),
    url(r'^ask/', ask, name='ask-question'),
    url(r'^settings/', settings, name='settings'),
    url(r'^hello/$', hello),
    url(r'^rate_question/$', rate_question, name='rate-question'),
    url(r'^rate_answer/$', rate_answer, name='rate-answer'),
    url(r'^mark_answer/$', mark_answer, name='mark-answer'),
]

urlpatterns += staticfiles_urlpatterns()
