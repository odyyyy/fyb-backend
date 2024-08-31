from rest_framework.response import Response

def create_vacancy(serializer_class, vacancy_data):
    serializer = serializer_class(data=vacancy_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)