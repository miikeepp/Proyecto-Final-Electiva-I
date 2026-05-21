# Proyecto-Final-Electiva-I


# para entrar 

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata fixtures/datos_productos.json
python manage.py runserver
