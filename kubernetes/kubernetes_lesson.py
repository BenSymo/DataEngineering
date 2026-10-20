"""
Kubernetes Lesson: What it is, how to set it up, and how to use it.

Run this file to print the lesson:  python kubernetes_lesson.py
"""

LESSON = """
=====================================================================
1. WHAT IS KUBERNETES?
=====================================================================
Kubernetes (also written K8s) runs and manages lots of containers
across many machines.

Docker runs ONE container. But real systems have dozens or hundreds.
Who restarts them when they crash? Who adds more when traffic grows?
Who updates them without downtime? Kubernetes does.

Think of Docker as a single shipping container, and Kubernetes as the
port manager: it decides where each container goes, replaces broken
ones, and adds more when the port gets busy.

You tell Kubernetes the STATE you want ("keep 3 copies of this app
running"). It works constantly to make reality match.

Why data engineers care:
  - Airflow, Spark and Kafka are often run on Kubernetes in
    production.
  - Pipelines can scale up when busy and down when idle.
  - Failed jobs are restarted automatically.

=====================================================================
2. KEY WORDS
=====================================================================
CLUSTER      A group of machines running Kubernetes.
NODE         One machine in the cluster.
POD          The smallest unit. Wraps one (or a few) containers.
DEPLOYMENT   Keeps a set number of identical pods running and
             handles updates.
SERVICE      A stable address to reach pods. Pods come and go, but
             the service address stays the same.
NAMESPACE    A folder-like way to separate things in one cluster.
JOB          Runs a pod until it finishes (good for batch tasks).
CONFIGMAP    Stores settings. SECRET stores passwords.
MANIFEST     A YAML file describing what you want.
kubectl      The command-line tool for talking to the cluster.

=====================================================================
3. INSTALL (A LOCAL PRACTICE CLUSTER)
=====================================================================
You need Docker first (see the docker folder). Then install:

  1. kubectl:  https://kubernetes.io/docs/tasks/tools/
  2. minikube: https://minikube.sigs.k8s.io/docs/start/
     (an alternative is `kind`, or Docker Desktop's built-in
     Kubernetes setting)

Start a cluster on your laptop:
    minikube start

Check it works:
    kubectl version --client
    kubectl get nodes

=====================================================================
4. BASIC kubectl COMMANDS
=====================================================================
    kubectl get pods                  # list pods
    kubectl get deployments           # list deployments
    kubectl get services              # list services
    kubectl get all                   # list most things
    kubectl describe pod <name>       # details and recent events
    kubectl logs <pod-name>           # see a pod's output
    kubectl exec -it <pod> -- bash    # open a shell in a pod
    kubectl apply -f file.yaml        # create/update from a file
    kubectl delete -f file.yaml       # delete what a file made
    kubectl get pods -n <namespace>   # look in a namespace

=====================================================================
5. YOUR FIRST DEPLOYMENT
=====================================================================
Save this as app.yaml:

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: hello-web
    spec:
      replicas: 3                    # keep 3 pods running
      selector:
        matchLabels:
          app: hello-web
      template:
        metadata:
          labels:
            app: hello-web
        spec:
          containers:
            - name: web
              image: nginx:1.27
              ports:
                - containerPort: 80
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: hello-web
    spec:
      selector:
        app: hello-web               # send traffic to these pods
      ports:
        - port: 80
          targetPort: 80

Run it:
    kubectl apply -f app.yaml
    kubectl get pods                 # you should see 3 pods

Open it in your browser (minikube):
    minikube service hello-web

=====================================================================
6. SEE KUBERNETES HEAL AND SCALE
=====================================================================
Delete one pod and watch a new one appear:
    kubectl delete pod <one-of-the-pod-names>
    kubectl get pods

Scale up or down:
    kubectl scale deployment hello-web --replicas=5

Update to a new version with no downtime:
    kubectl set image deployment/hello-web web=nginx:1.27.1
    kubectl rollout status deployment/hello-web

Roll back if something goes wrong:
    kubectl rollout undo deployment/hello-web

=====================================================================
7. A BATCH JOB (VERY COMMON IN DATA ENGINEERING)
=====================================================================
A Job runs a container to completion, then stops:

    apiVersion: batch/v1
    kind: Job
    metadata:
      name: say-hello
    spec:
      backoffLimit: 2                # retry up to 2 times
      template:
        spec:
          restartPolicy: Never
          containers:
            - name: job
              image: python:3.12-slim
              command: ["python", "-c", "print('pipeline step done')"]

    kubectl apply -f job.yaml
    kubectl logs job/say-hello

=====================================================================
8. GOOD HABITS
=====================================================================
  - Store manifests in git, and change things through them, not by
    hand-editing live objects.
  - Set resource requests and limits (CPU and memory) on containers.
  - Never put passwords in manifests. Use Secrets.
  - Use namespaces to separate dev, test and prod.
  - Learn Helm: a package manager that installs tools like Airflow
    or Kafka on Kubernetes with one command.
  - For practice, delete the cluster when done:  minikube delete

=====================================================================
9. PRACTICE EXERCISE
=====================================================================
  1. Start minikube and run `kubectl get nodes`.
  2. Apply the Deployment and Service from section 5.
  3. Delete a pod. How long until it is replaced?
  4. Scale to 5 replicas, then back to 2.
  5. Change the image version and watch the rollout.
  6. Run the Job from section 7 and read its logs.
  7. Clean up:  kubectl delete -f app.yaml

Next steps: learn Helm, then try installing Airflow on Kubernetes.
"""


def main():
    print(LESSON)


if __name__ == "__main__":
    main()
