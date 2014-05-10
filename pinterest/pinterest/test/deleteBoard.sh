#!/bin/bash
#
# test client access to our service

echo -e "\n"
curl -i -H "Accept: application/json" -H "X-HTTP-Method-Override: DELETE" -X POST http://localhost:8080/v1/user/123234/board/62
echo -e "\n"