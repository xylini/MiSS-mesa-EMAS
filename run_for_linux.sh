if [[ ! -d "venv" ]]; then
    echo Creating virtualenv...
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt
python run_hawk_dove.py