from rest_framework.views import APIView, Response , Request ,  status
from django.forms.models import model_to_dict
from .models import Team
from datetime import datetime

class TeamsViews(APIView):
    def get(self, request) -> Response:
       teams = Team.objects.all()

       team_list = [
           model_to_dict(team) for team in teams
       ]
       return Response(team_list, status.HTTP_200_OK)
    
    def post(self, request:Request) -> Response:
        body = request.data
        fisrt_cup: str = body["first_cup"]
        get_year = fisrt_cup.split("-")
        year = datetime(int(get_year[0]), 1, 1)
        date = int(year.strftime("%Y"))

        current_year = int(datetime.now().today().year)
        max_titles = (current_year - date) // 4

        if body["titles"] <= 0:
            return Response({"error": "titles cannot be negative"},status.HTTP_400_BAD_REQUEST)

        if date < 1930 or (date - 1930) % 4 != 0:
            return Response({"error":"there was no world cup this year"},status.HTTP_400_BAD_REQUEST )

        if body["titles"] > max_titles:
            return Response({"error": "impossible to have more titles than disputed cups"}, status.HTTP_400_BAD_REQUEST)
        
        team = Team.objects.create(**body)
        team_dict = model_to_dict(team)
        return Response(team_dict,status.HTTP_201_CREATED)

class TeamsDetailView(APIView):
    def get(self, request:Request, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist :
            return Response({"message": "Team not found"},status.HTTP_404_NOT_FOUND)

        team_dict = model_to_dict(team)
        return Response(team_dict, status.HTTP_200_OK)

    def patch(self, request:Request, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist :
            return Response({"message": "Team not found"},status.HTTP_404_NOT_FOUND)
        
        for key , value in request.data.items():
            setattr(team,key,value)

        team.save()
        team_dict = model_to_dict(team)
        return Response(team_dict, status.HTTP_200_OK)

    def delete(self, request:Request, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist :
            return Response({"message": "Team not found"},status.HTTP_404_NOT_FOUND)

        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)     