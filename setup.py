import sys
from optparse import OptionParser
import re
import os

p = OptionParser()
p.add_option("-d", "--directory", dest="dir", help="set the output directory to copy the completed files to", default=".")

(options, args) = p.parse_args()

print("Setting up the let's encrypt config...")
domain_name = input("What is the domain name of your server (do not include www)?\n> ")
sub_domains = input("Enter your subdomains as a comma seperated list (most systems include 'www')\n> ")

print("\n")
print("Setting up the docker service...")
service_name = input("What is the name of your service (webserver)?\n> ")
service_port = input("What port does your service run on (8080)?\n> ")

if len(service_name) == 0:
    service_name = "webserver"

if len(service_port) == 0:
    service_port = "8080"
service_name = service_name.lower().replace(" ", "-")

if len(sub_domains) > 1 and sub_domains[-1] == ",":
    sub_domains = sub_domains[:-1]

domain_list = [domain_name]

if "," in sub_domains:
    for sub in sub_domains.split(","):
        domain_list.append(sub + "." + domain_name)
elif len(sub_domains) > 0:
    domain_list.append(sub_domains + "." + domain_name)

domain_list = ", ".join(domain_list)
print(domain_name)
print(sub_domains)
print(domain_list)

print(service_name)
print(service_port)

print("Creating files...")
nginx_conf = open("nginx.base.conf", "r").read()
docker_conf = open("docker-compose.base.yml", "r").read()

docker_out = open(os.path.join(options.dir, "docker-compose.yml"), 'w')
nginx_out = open(os.path.join(options.dir, "nginx.conf"), 'w')

keys = dict()
keys["service_name"] = service_name
keys["service_port"] = service_port
keys["domain_name"] = domain_name
keys["domain_list"] = domain_list
keys["subdom"] = sub_domains

for k, v in keys.items():
    nginx_conf = nginx_conf.replace("%" + k +"%", v)
    docker_conf = docker_conf.replace("%" + k + "%", v)

print(nginx_conf)
print(docker_conf)

docker_out.write(docker_conf)
nginx_out.write(nginx_conf)

docker_out.close()
nginx_out.close()
