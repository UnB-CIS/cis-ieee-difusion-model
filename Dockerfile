FROM tensorflow/tensorflow:latest-jupyter

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /home/caefleury/Documents/ieee-cis/cis-difusion-model/src

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--NotebookApp.password='argon2:$argon2id$v=19$m=10240,t=10,p=8$BM5f6z8PxSwwx7RenVUb4Q$AWjm2iQ0hS7Rw0pzdj+vFdKyMPaeCZVVzaWdnCESArc'"]