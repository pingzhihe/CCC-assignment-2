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

## Setup
1. Clone the repository
2. Using the `unimelb-comp90024-2024-grp-8-openrc.sh'`file, source the openstack credentials
3. Run the following command to connect the master node:

```ssh -i <path for your key>  -L 6443:$(openstack coe cluster show elastic -f json | jq -r '.master_addresses[]'):6443 ubuntu@$(openstack server show bastion -c addresses -f json | jq -r '.addresses["qh2-uom-internal"][]') ```



