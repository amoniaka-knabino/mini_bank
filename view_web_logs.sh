docker logs $(docker ps | grep mini_bank_web | awk '{ print $1 }')

