#!/bin/bash
#
# test client access to our service

echo -e "\n"
curl -i -H "Accept: application/json" --data "boardName='board123'"  http://localhost:8080/v1/user/123234/board
echo -e "\n"
