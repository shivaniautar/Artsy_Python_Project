from django.urls import path
from main import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('artsy', views.start),
    path('processreg', views.register),
    path('processlogin', views.login),
    path('dashboard', views.dashboard_page),
    path('logout', views.logout),
    path('editmyprofile', views.edit_profile_page),
    path( 'upload/profileimg', views.process_profile_pic),
    path('updateprofile', views.process_update_profile),
    path('new_masterpiece', views.new_mp_page),
    path('newmp', views.process_newmp_info),
    path('edit_masterpiece', views.edit_mp_page),
    path('updatemp', views.update_mp_info),
    path('updateupload/item_pic', views.process_newmasterpiece_pic),
    path('viewartist/<int:artist_id>/anditems', views.see_artist_page),
    path('edit/<int:item_id>', views.edit_item_page),
    path('updateitem/<int:item_id>', views.process_update_item),
    path('upload/item_pic/<int:item_id>/after_view', views.process_update_masterpiece_pic),
    path('viewmasterpiece/<int:item_id>', views.see_viewmasterpiece_page),
    path('delete/<int:item_id>', views.process_delete)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)