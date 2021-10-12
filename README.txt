This repo contains an API written in Python using Flask to build the API functions and make them available to the internet, will be containerized and deployed using Kubernetes Cluster on IBM Cloud.

Please Note:
This is making use of the MongoDB chart from Bitnami available at:
https://cloud.ibm.com/catalog/content/mongodb-Qml0bmFtaS1tb25nb2Ri-global

If you plan to install this to your cluster you will need to install that chart and then replace the IP in the `app.py` file (Line 8) with the IP of the Service that exposes your MongoDB instance.
