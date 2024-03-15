from waitress import serve
from face_rec_project.wsgi import application

if __name__ == '__main__':
    serve(application, port='8000')