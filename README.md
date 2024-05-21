# CCC-assignment-2
This is the project repository for Cluster and Cloud Computing (COMP90024)

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

6. 