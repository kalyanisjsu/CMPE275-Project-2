#!/bin/bash
#
# test client access to our service

echo -e "\n"
curl -i -H "Accept: application/json" --data "boardName='boardHello'"  http://localhost:8080/v1/user/14/board
echo -e "\n"
