export PYTHONPATH=$(pwd)/src
uvicorn api.main:app --reload