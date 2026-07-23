FROM python:3.12-slim
RUN useradd --create-home appuser
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chmod=555 app.py password_policy.py ./
COPY --chmod=555 static ./static
COPY --chmod=555 templates ./templates
USER appuser
EXPOSE 8000
CMD ["python", "app.py"]
