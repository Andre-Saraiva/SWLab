# Crawler

Arquivo principal:
src/main.py

## Instalação

Dependências básicas:
- requests (```$ pip install requests```)
- sqlalchemy (```$ pip install sqlalchemy```)
- tqdm (```$ pip install tqdm```)

Dependências para execução assíncrona (opcionais)
- aiopg (```$ pip install aiopg```)
- aiohttp (```$ pip install aiohttp```)

## Configuração

Configure o banco de dados em src/tasks/database/connection.py:
```python
USER = "postgres"
PASSWORD = "postgres"
HOST = "127.0.0.1"
DATABASE = "swlab"
```

## Execução:

Existem 4 comandos básicos no crawler:
- db: possui operações de criação e migração do banco de dados
- datahub: busca datasets no datahub
- void: busca voids a partir da forma canonica
- resources: realiza operações nos recursos

O fluxo de execução deve ser:

### 1\. Criação do banco de dados (db create)

 ```$ python main.py db create``` 


### 2\. Criação das tabelas (db migrate)
 
 ```$ python main.py db migrate```


### 3\. Leitura do datahub (datahub)

 É possível fazer de forma assíncrona ou síncrona. A forma síncrona é mais demorada, porém mais confiável, visto que suporta SSL, e redirects. O parâmetro -a <requisicoes simultaneas> indica a forma. Se <requisicoes simultaneas> for 0, o modo síncrono será executado.
Também é possível limitar intervalo [f, l) com os parâmetros -f e -l. Por padrão o intervalo é [0, numero_de_datasets).

 ```$ python main.py datahub -a 6 -f 100 -l 200```
 
 Esse comando realizará 6 requisições de cada vez e começará dataset de indice 100 (contagem inicia em 0) até o dataset de índice 199.


### 4\. Busca de voids pela forma canonica (void)

 Os mesmos parametros de 3 valem para 4. Forma síncrona continua mais confiável. A forma síncrona determina o número de requisições simultâneas por domínio.

 ```$ python main.py void -a 0 -f 10 -l 20```

 Esse comando varrerá o domínio de índice 10 até o domínio de índice 19 procurando voids pela forma canônica de forma síncrona.


### 5\. Limpeza de voids vazios

 Alguns resultados da operação anterior vem em branco. Realize a limpeza com:

 ```$ python main.py db delete_empty_check_voids```


### 6\. Normalização de resources

 A condição de busca dos voids nos resources é complicada. Esta operação transforma o campo descrição de todos os voids em "ws(void)"

 ```$ python main.py resources normalize```


### 7\. Leitura de voids armazenados em resources

 Para ler os voids armazenados em resources e salvá-los no BD faça:

 ```$ python main.py resources cache```
