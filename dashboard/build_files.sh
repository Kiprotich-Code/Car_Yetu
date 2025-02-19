# build_files.sh

python3 -m pip install -r requirements.txt
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate
python3.9 manage.py collectstatic --noinput