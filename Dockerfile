FROM tensorflow/tensorflow:latest-jupyter

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .


# Set up Jupyter
EXPOSE 8888
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--NotebookApp.password='argon2:$argon2id$v=19$m=10240,t=10,p=8$BM5f6z8PxSwwx7RenVUb4Q$AWjm2iQ0hS7Rw0pzdj+vFdKyMPaeCZVVzaWdnCESArc'"]