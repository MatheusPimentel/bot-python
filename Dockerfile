# Dockerfile

# 1. IMAGEM BASE: Começamos com uma imagem oficial do Python.
# A tag "slim" é uma versão mais leve, ideal para produção.
FROM python:3.13-slim

# 2. DIRETÓRIO DE TRABALHO: Definimos o diretório padrão dentro do contêiner.
# Todos os comandos a seguir serão executados a partir daqui.
WORKDIR /app

# 3. COPIAR E INSTALAR DEPENDÊNCIAS:
# Copiamos apenas o arquivo de dependências primeiro.
# Isso aproveita o cache do Docker: se não mudarmos o requirements.txt,
# o Docker não vai reinstalar tudo a cada build. É uma ótima prática.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. COPIAR O CÓDIGO FONTE:
# Agora copiamos o resto do nosso código para dentro do contêiner.
COPY . .

# 5. EXPOR A PORTA:
# Informamos ao Docker que nosso aplicativo escuta na porta 8000.
EXPOSE 8000

# 6. COMANDO DE EXECUÇÃO:
# O comando que será executado quando o contêiner iniciar.
# Usamos "--host 0.0.0.0" para que o servidor seja acessível de fora do contêiner.
# Dentro de um contêiner, 127.0.0.1 (localhost) não é visível para o host.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]