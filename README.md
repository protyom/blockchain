# Protyom's blockchain 
My blockchain implementation written on Python
##Installation via Docker

1. docker build -t protyom/blockchain:os -f docker/os/Dockerfile .
2. docker build -t protyom/blockchain:pip -f docker/pip/Dockerfile .
3. docker build -t protyom/blockchain:app -f docker/app/Dockerfile .

##Run 
docker run --rm protyom/blockchain:app python3 TxBlock.py

