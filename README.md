
<h1>README</h1>
 <p>Requisito: **Python 3.12.0** para rodar localmente **(sem container)**</p>

1. **Clone o repositório e acesse a pasta**

2. **Crie o ambiente virtual para isolar a aplicação**
``` 
python -m venv .venv
```

3. **Ative o ambiente**
``` 
source .vent/bin/activate
```

4. **Rode as migrations**
``` 
python manage.py migrate
```

5. **Inicie o servidor local**
```
python manage.py runserver 
```

6. **Abra o endereço:** http://127.0.0.1:8000/