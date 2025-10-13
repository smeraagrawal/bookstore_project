# 1. Base image
FROM python:3.13.7-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Copy all project files into the container
COPY . /app

# 4. Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 5. Expose port for Streamlit
EXPOSE 8501

# 6. Command to run the app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
