pip install pandas
source venv/bin/activate
source bigquery-env/bin/activate

-- run main code --
deactivate
source venv/bin/activate
python main.py

-- kill port --

sudo lsof -i :5000
sudo kill -9 PID value (ex- sudo kill -9 1234)



