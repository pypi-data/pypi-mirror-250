from setuptools import setup

setup(
    name="simple-form",
    version=1.0,
    description="Pequena biblioteca para facilitar formulários em CLI com Python",
    long_description="""## [Simple Form](https://pypi.org/project/simple-form/)
- Pequena biblioteca para facilitar formulários em CLI.
- Clique [**aqui**](https://github.com/Hoyasumii/SimpleForm) para acessar o repositório.
---
## Instalação
- Você pode baixar pelo pip:
```
pip install simple-form
```
---
## Como usar?
- Em seu projeto, importe a biblioteca e crie um objeto: 
```python
# Importando a biblioteca
from simpleForm import Form

# Criando um objeto
myForm = Form("Título do meu formulário")
```
- Para adicionar elementos ao formulário, use o método `add`:
```python
# Adicionando um campo de texto
myForm.add(name={
    "type": str,
    "description": "Digite seu nome"
})
```
- Para executar o formulário, chame a instância do `objeto`:
```python
myForm()
```
- Para acessar os dados do formulário, use a propriedade `values`:
```python
print(myForm.values)
```
---
## O que existe no pacote?
- Classe `Form`
> Classe principal, responsável por criar o formulário e executá-lo.
- Pacote `scripts`
> Pacote com scripts que são utilizados para simplificar a criação da classe principal, entretanto que podem ser úteis em alguns casos, mesmo que específicos.
---
## Conhecendo a classe `Form`
- A classe `Form` funciona de uma maneira que seu construtor recebe as informações gerais do futuro formulário, e que a criação dos campos se dá através do método `add`. Para executar o formulário, basta chamar a instância do objeto como função(`__call__`).
---
## Métodos e propriedades disponíveis para uso
#### 1. `__init__`(`title`: `str`, `separator`: `str`, `separatorSize`: `int`)
- Instancia a classe `Form`.
#### 2. `add`(`**kwargs`)
- Adiciona uma quantidade indeterminada de campos ao formulário.
- Clique [**aqui**](#o-que-cada-elemento-a-ser-adicionado-pode-e-precisa-ter) para entender o que cada elemento a ser adicionado pode e precisa ter.
#### 3. `__call__`()
- Executa o formulário.
#### 4. `values` -> `dict`
- Retorna um dicionário com os valores dos campos do formulário.
---
## O que cada elemento a ser adicionado pode e precisa ter?
- Cada elemento a ser adicionado precisa ser um dicionário, e precisa ter os seguintes atributos:
- Caso um determinado elemento possua uma exclamação(`!`) ao lado de seu nome, significa que ele é obrigatório.
#### 1. `type`!
- É o tipo de dado que o elemento vai receber. Pode ser `str`, `int`, `float`, `bool`, e `iteráveis`.
- Se for `bool`, o elemento vai receber um valor booleano, e o usuário usará o teclado para definir `True` ou `False`, sendo esses representados por `y` e `n`, respectivamente.
- Se for `iteráveis`, o elemento vai receber uma lista de valores, e o usuário vai poder escolher um deles.
#### 2. `description`!
- É a descrição do elemento, que vai ser mostrada ao usuário.
#### 3. `default`
- Exclusivo para type `str` e `numerais`.
- É o valor padrão do elemento, que vai ser usado caso o usuário não digite nada.
#### 4. `min`
- Exclusivo para type `str` e `numerais`.
- É o valor mínimo que o elemento pode receber. Caso o `min` exista num input de `str`, ele vai ser usado para definir o tamanho mínimo da string. E caso seja um numeral(`int` e `float`), ele vai ser usado para definir o valor mínimo que o elemento pode receber.
#### 5. `max`
- Exclusivo para type `str` e `numerais`.
- É o valor máximo que o elemento pode receber. Caso o `max` exista num input de `str`, ele vai ser usado para definir o tamanho máximo da string. E caso seja um numeral(`int` e `float`), ele vai ser usado para definir o valor máximo que o elemento pode receber.
#### 6. `validate`
- Exclusivo para type `str`.
- É uma expressão regular que vai ser usada para validar o valor do elemento. Caso o valor não seja válido, o usuário vai ter que digitar novamente.
#### 7. `options`
- Exclusivo para type `iteráveis`, ou seja, tipos que possuem o método `__iter__` embutido ao tipo, como por exemplo, `list`, `tuple`, `set` e `dict`.
- É uma lista de valores que o usuário vai poder escolher.
- Na hora de mostrar as opções para o usuário, o programa vai mostrar o índice de cada valor, e o usuário vai ter que digitar o índice do valor que ele quer.
---
## Exemplo
```python
# Importando a biblioteca
from simpleForm import Form

# Criando o formulário
x = Form("Olá, formulário!", spacing=4)

# Adicionando os campos
x.add(
    # Campo Nome
    name={
        "type": str,
        "description": "Nome",
        "default": "John Doe",
        "min": 3,
        "max": 10
    }, 
    # Campo Feliz
    happy={
        "type": bool,
        "description": "Feliz"
    }, 
    # Campo Idade
    age={
        "type": int,
        "description": "Idade",
        "min": 1,
        "max": 100,
        "default": 18
    }, 
    # Campo Ação (Iteráveis exceto dicionários)
    action={
        "type": list,
        "description": "Escolha a ação",
        "options": [
            "Pular",
            "Correr",
            "Andar"
        ],
    },
    # Campo Email
    email={
        "type": str,
        "description": "Email",
        "default": "account@email.com",
        "validate": r"^[a-zA-Z0-9\._]{4,}@\w.{2,}\w{2,}$"
    }, 
    # Campo Opção (Dicionário)
    option={
        "type": dict,
        "description": "Opção",
        "options": {
            "Pular": "E pulou",
            "Correr": "E correu",
            "Andar": "E andou"
        }
    }
)

# Chamando o formulário
x()

# Imprimindo os valores
print(x.values)
```""",
    long_description_content_type="text/markdown",
    author="Alan Reis Anjos",
    author_email="alanreisanjo@gmail.com",
    url="https://github.com/Hoyasumii/SimpleForm",
    packages=['simpleForm', 'simpleForm.scripts'],
    install_requires=['keyboard==0.13.5', 'setuptools==69.0.3'],
    license="GPL-3.0",
    entry_points={'console_scripts': []}
)
