from django.urls import path
from .views import CreateInvitationAPIView, AcceptInvitationAPIView, CancelInvitationAPIView,DashboardView,LoggingView

urlpatterns = [
    path('invite/', CreateInvitationAPIView.as_view(), name='create-invite'),
    path('invite/accept/', AcceptInvitationAPIView.as_view(), name='accept-invite'),
    path('invite/cancel/', CancelInvitationAPIView.as_view(), name='cancel-invite'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard_logging/', LoggingView.as_view(), name='dashboard logging'),
]
