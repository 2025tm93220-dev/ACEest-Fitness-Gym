FROM python:3.11-slim 

WORKDIR /app 

COPY . . 

RUN pip install -r requirements.txt 

EXPOSE 5000 

CMD ["python", "app.py"] 

Commit: 

git add . 

git commit -m "Added Docker support" 

git tag v2.0 

git push 

git push v2.0 
