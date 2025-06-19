FROM python:3.13.1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/ffardian/DocSort.git .

RUN mkdir -p /root/.EasyOCR/

COPY models/craft_mlt_25k.pth /root/.EasyOCR/craft_mlt_25k.pth
COPY models/latin_g2.pth /root/.EasyOCR/latin_g2.pth

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
