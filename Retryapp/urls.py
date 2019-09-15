__author__ = 'shivangi'
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'show', views.show, name='show'),
    url(r'login', views.login, name='login'),
    url(r'signup', views.signup, name='signup'),
    url(r'option', views.option, name='option'),
    url(r'profile', views.profile, name='profile'),
    # url(r'profile_option',views.profile_option,name='profile_option'),
    url(r'store_data', views.store_data, name='store_data'),
    url(r'smore', views.smore, name='smore'),
    url(r'^signin$',views.signin,name='signin'),
    url(r'feedback',views.feedback,name='feedback'),
    url(r'^contact$',views.contact,name='contact'),
    url(r'popular',views.popular,name='popular'),
    url(r'^new_application',views.new_application,name='new_application'),
    url(r'^website$',views.website,name='website'),
    url(r'^new_software',views.new_software,name='new_software'),
    url(r'forgotpwd',views.forgotpwd,name='forgotpwd'),
    url(r'getpwd',views.getpwd,name='getpwd'),
    url(r'abt',views.abt,name='abt'),
    url(r'^added$',views.added,name='added'),
    url(r'profile',views.profile,name='profile'),
    url(r'edit',views.edit,name='edit'),
    url(r'upload',views.upload,name='upload'),
    url(r'result',views.result,name='result'),
    url(r'dashboard',views.dashboard,name='dashboard'),
    url(r's_term',views.s_term,name='s_term'),
    url(r're_site',views.re_site,name='re_site'),
    url(r'^user_app$',views.user_app,name='user_app'),
    url(r'^user_comment$',views.user_comment,name='user_comment'),
    url(r'^user_like$',views.user_like,name='user_like'),
    url(r'^logout$',views.logout,name='logout'),
    url(r'^user_web$',views.user_web,name='user_web'),
    url(r'^user_web_like$',views.user_web_like,name='user_web_like'),
    url(r'^user_soft$',views.user_soft,name='user_soft'),
    url(r'^user_soft_like$',views.user_soft_like,name='user_soft_like'),
    url(r'^user_web_comment$',views.user_web_comment,name='user_web_comment'),
    url(r'^user_soft_comment$',views.user_web_comment,name='user_web_comment'),
    url(r'^user_request$',views.user_request,name='user_request'),
    url(r'^user_request_accept$',views.user_request_accept,name='user_request_accept'),
    url(r'^user_request_reject$',views.user_request_reject,name='user_request_reject'),
    url(r'^application_admin$',views.application_admin,name='application_admin'),
    url(r'^website_admin$',views.website_admin,name='website_admin'),
    url(r'^software_admin$',views.software_admin,name='software_admin'),
    url(r'^treanding_app$',views.treanding_app,name='treanding_app'),
    url(r'^application_search_treanding$',views.application_search_treanding,name='application_search_treanding'),
    url(r'^treanding_app_remove$',views.treanding_app_remove,name='treanding_app_remove'),
    url(r'^website_search_trending$',views.website_search_trending,name='website_search_trending'),
    url(r'^website_treading_display$',views.website_treading_display,name='website_treading_display'),
    url(r'^treanding_web_remove$',views.treanding_web_remove,name='treanding_web_remove'),
    url(r'^application_search_new$',views.application_search_new,name='application_search_new'),
    url(r'^new_app$',views.new_app,name='new_app'),
    url(r'^new_app_remove$',views.new_app_remove,name='new_app_remove'),
    url(r'^app_display$',views.app_display,name='app_display'),
    url(r'^treanding_soft$',views.treanding_soft,name='treanding_soft'),
    url(r'^treanding_soft_remove$',views.treanding_soft_remove,name='treanding_soft_remove'),
    url(r'^new_soft$',views.new_soft,name='new_soft'),
    url(r'^trending$',views.trending,name='trending'),
    url(r'^trending_application$',views.trending_application,name='trending_application'),
    url(r'^trending_software$',views.trending_software,name='trending_software'),
    url(r'^new_web$',views.new_web,name='new_web'),
    url(r'^soft_display$',views.soft_display,name='soft_display'),
    url(r'^web_display$',views.web_display,name='web_display'),
    url(r'^new_software_search$',views.new_software_search,name='new_software_search'),
    url(r'^added_app$',views.added_app,name='added_app'),
    url(r'^added_web$',views.added_web,name='added_web'),
    url(r'^added_soft$',views.added_soft,name='added_soft'),
    url(r'^dashboard$',views.dashboard,name='dashboard'),
    url(r'^new$',views.new,name='new'),
    url(r'^highlights$',views.highlights,name='highlights'),
    url(r'^app_highlights$',views.app_highlights,name='app_highlights'),
    url(r'^web_highlights$',views.web_highlights,name='web_highlights'),
    url(r'^soft_highlights$',views.soft_highlights,name='soft_highlights'),
    url(r'^highlights_nevigation$',views.highlights_nevigation,name='highlights_nevigation'),
    url(r'^added_nevigation$',views.added_nevigation,name='added_nevigation'),
    url(r'^trending_nevigation$',views.trending_nevigation,name='trending_nevigation'),
    url(r'^recommendation$',views.recommendation,name='recommendation'),
    url(r'^recommend_app$',views.recommend_app,name='recommend_app'),

    url(r'^fdbk_data$',views.fdbk_data,name='fdbk_data'),
    url(r'^dashboar_navigation',views.dashboar_navigation,name='dashboar_navigation')
















   # url(r'get',views.getapiresult,name='getapiresult'),




]