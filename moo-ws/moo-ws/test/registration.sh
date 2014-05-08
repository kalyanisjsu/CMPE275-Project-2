#!/bin/bash
#
# test client access to our service

echo -e "\n"
<<<<<<< HEAD
curl -i -H "Accept: application/json" --data "name='Shweta'&username='shweta'&password='shweta'"  http://192.168.0.93:8080/v1/reg
=======
curl -i -H "Accept: application/json" --data "name='Robert'&username='rob'&password='rob'"  http://localhost:8080/v1/reg
>>>>>>> b9a468d3d57e24fa05ecd42a5d1a6693598a460a
echo -e "\n"
