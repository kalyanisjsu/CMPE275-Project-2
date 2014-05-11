#!/bin/bash
#
# test client access to our service

echo -e "\n"
curl -i -H "Accept: application/json" -H "X-HTTP-Method-Override: DELETE" -X DELETE http://localhost:8080/v1/user/14/board/96
echo -e "\n"