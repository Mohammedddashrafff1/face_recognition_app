# # consumers.py

# import json
# from channels.generic.websocket import WebsocketConsumer
# from .models import Visits

# class VisitConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     def fetch_latest_visits(self, event):
#         latest_visits = Visits.objects.all().order_by('-created_at')[:10]  # Fetch latest 10 visits
#         visits_data = [{'user_name': visit.user.user_name, 'created_at': visit.created_at} for visit in latest_visits]
#         self.send(text_data=json.dumps({'latest_visits': visits_data}))
