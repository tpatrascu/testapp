## Run app locally

### Create database

```
export PGPASSWORD=123
export PGUSER=testapp
docker run --rm --name testapp-postgres -p 5432:5432 -e POSTGRES_USER="$PGUSER" -e POSTGRES_PASSWORD="$PGPASSWORD" -d postgres
psql -h localhost
```

### Create python venv

```
# python3 -m venv venv
# . venv/bin/activate
# pip install requirements.txt
```

### Initialize DB and DB migrations

```
export SQLALCHEMY_DATABASE_URI="postgresql://testapp:123@localhost:5432/testapp"
# flask db init
# flask db migrate
# flask db upgrade
```

When updating models it is necessary to prepare the db migrations while connected to a development database, by running:

```
# flask db migrate
```

then commit to git and build a new docker image.

Before the production image runs the application, it will run `flask db upgrade` to run the db migrations on the production database.


### Run unit tests

```
pytest -v
```

### Run app

```
export SQLALCHEMY_DATABASE_URI="postgresql://testapp:123@localhost:5432/testapp"
export FLASK_ENV=development
flask run
```



## Deploy app to AWS EKS

### Create the EKS cluster

```
# brew install eksctl
# eksctl create cluster --name testcluster --region eu-west-1 --fargate
```

### Create RDS


### Build docker image

Run tests locally

```
pytest -v
```

Build and push to docker hub

```
docker login
docker build -t tpatrascuboom/testapp:v0.0.1 .
# docker push tpatrascuboom/testapp:v0.0.1
```



### Deploy app on cluster

```
yq e -i ".spec.template.spec.containers[0].image = tpatrascuboom/testapp:v0.0.1 k8s-app-manifests.yaml
# kubectl -n default apply -f k8s-app-manifests.yaml
```

### Get service endpoint

```
kubectl get svc web
NAME   TYPE           CLUSTER-IP     EXTERNAL-IP                                                                     PORT(S)          AGE
web    LoadBalancer   10.100.13.72   a6275b3db004c401da3a27e3cae15ded-d212d8afb2dfea9f.elb.eu-west-1.amazonaws.com   8080:32666/TCP   7m54s
```
