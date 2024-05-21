# CCC-assignment-2


## Project Description
This project is a part of the Cluster and Cloud Computing subject at the University of Melbourne. The project aims to make aomprehensive study of big data analytics in human health and safety.
### Data Source
1. SUDO https://sudo.eresearch.unimelb.edu.au/
2. Twitter data on the previous Sparatan
3. Enviroment Protection Authority Victoria https://www.epa.vic.gov.au/
4. Bureau of Meteorology http://www.bom.gov.au/


## Team Members
- Zhihe Ping
- Kaisheng Su
- Can Wang
- Mingtao Yang 

## Repository content
In the Backend folder, there are code of data harvester, data processors and functions to get data from Elasticsearch and the zip files of the functions used to deploy the functions to Fission.

In the Frontend folder, there are jupyternotebook files which are used to perform data analytics on each scenario.

In the Data folder, all the data files put in the code are included.

In the Database folder, the txt files contain the index mapping of the databases in Elasticsearch.

The specs folder contains all the yaml files to deploy functions, packages and triggers into Fission.

## Setup
1. Clone the repository
2. Download the `<group-name>-openrc.sh` from the MRC. Use the command line:

```source <path-to-group-name-openrc.sh>```

3. Download the private key from MRC. Run the following command to connect the master node by entering the Openstack Password:

```ssh -i <path for your key>  -L 6443:$(openstack coe cluster show elastic -f json | jq -r '.master_addresses[]'):6443 ubuntu@$(openstack server show bastion -c addresses -f json | jq -r '.addresses["qh2-uom-internal"][]') ```

4. Open a new terminal, use the following command line to to access the Elasticsearch service on the local machine at localhost:9200

```kubectl port-forward service/elasticsearch-master -n elastic 9200:9200```

5. Open a new terminal, use the following command line to access the Kibana service on your local machine via localhost:5601

```kubectl port-forward service/kibana-kibana -n elastic 5601:5601```

6. Start a port forward from the Fission router by using the command line:

```kubectl port-forward service/router -n fission 9090:80```

7. Set up the python enviroment in the Kubernetes cluster.

``` fission env create --name python --image fission/python-env --builder fission/python-builder```

8. Modify the config map `shared-data.yaml` in the Spec folder. 

```
apiVersion: v1
kind: ConfigMap
metadata:
  namespace: default
  name: shared-data
data:
  ES_USERNAME: elastic
  ES_PASSWORD: elastic
  EPA_API_KEY: <Your_EPA_API_KEY>
  USER_AGENT: Your User Agent
```

You need to apply the api key of EPA and the user agent of the request header in the config map. The initial value might be expired. The following website for application: https://portal.api.epa.vic.gov.au/

Running :
```kubectl apply -f <path-to-shared-data-.yaml>``` to apply the config map.
The shared-data.yaml is under the specs folder.




9. Use 'cd' command to move the working directory outside the 'CCC-assignment-2' repository. Use the command line to deploy all the Fission functions, packages and triggers:

```fission spec apply --specdir CCC-assignment-2/specs --wait```

## How to run
```Prerequisite: Successfully run all the steps in Setup section```

Run the three jupyternotebook files in Frontend folder. Make sure the code blocks which send http requests do not receive error messages. If these blocks receive error messages (e.g. fail to send request to function), run the blocks of code again after a while.