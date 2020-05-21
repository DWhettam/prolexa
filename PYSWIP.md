# Giving Prolexa a Language model frontend

We assume you're using Linux.


### FIX

```python3 -m venv pyswip_env
source pyswip_env/bin/activate
pip install pyswip
pip install jupyter
python3 -m ipykernel install --name pyswip_env --user
python3 python/string_eval.wrapper.py```

```from swipl import Prolog```



