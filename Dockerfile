FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-latex-recommended \
    texlive-latex-extra \
    fonts-noto-cjk \
    pandoc \
    fontconfig \
    && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["streamlit", "run", "app.py", "--server.port=10000", "--server.enableCORS=false"]
