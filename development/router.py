from rest_framework.routers import DefaultRouter
from development.views import TimelineView, BayStateAuctionView, TownAuctionView
router = DefaultRouter()
#router.register(r'timeline', TimelineView, base_name='timeline')
#router.register(r'baystateauction', BayStateAuctionView.as_view(), base_name='baystateauction')
# router.register(r'townauction', TownAuctionView.as_view(), base_name='townauction')