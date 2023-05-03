                                           # mediaserverFullStack

This is a Docker Compose file that defines the configuration for running several services and applications within Docker containers. Each service is defined as a separate container, with its own image, configuration, and network settings.

The services include:

1. `pihole`: a DNS server that blocks ads and trackers.
2. `npm`: an NGINX proxy manager that allows for easy management of virtual hosts and SSL certificates.
3. `flame`: a container monitoring tool that provides insight into the resource usage of Docker containers.
4. `website`: a custom application container that serves a website.
5. `portainer`: a container management platform that provides an easy-to-use web interface for managing Docker containers, images, and networks.
6. `plex`: a media server that organizes and streams media content such as movies and TV shows.
7. `ombi`: a request management platform for media servers
8. `nzbget`: a download client.
9. `sonarr`: a TV show management platform for media servers.
10. `radarr`: a movie management platform for media servers.
11. `lidarr`: a music management platform for media servers.

The services are defined with various configuration settings such as the container name, hostname, environment variables, volumes, ports, and networks. Each service is labeled with metadata such as the application name, type, and URL for easy identification.

The networks are defined as `frontend` and `backend` and they are external networks, with names defined in the host system. The `frontend` network is a macvlan network, while the `backend` network is a bridge network. The network settings define the IP address for each container and the DNS server used for resolving domain names.

To use this Docker Compose file, first, ensure that Docker and Docker Compose are installed on the host system. Then, place the file in a directory and run `docker-compose up` command in the same directory. This will start all the services defined in the file. To stop the services, run `docker-compose down` command. 

This Docker Compose file can be used for various use cases such as home media server, local website hosting, and container management. The file can be customized to suit the user's specific needs and can be extended with additional services and containers as required.

                                              {((( Docker Env )))}
                                                
                                             ||manager containers|| (portainer)
                                                      v
                                                 ||schedule|| =--\
                                                      v         --\
                                                  ||monitor||   ---|--- (Sonarr, Radarr, Lidarr)
                                                        v       --/
                                                  ||search|| ----/
                                                      v
                                                  ||fetch||   --\
                                                      v       ---|--- (nzbget)
                                                  ||extract|| --/
                                                      v
                                                  ||metadata|| --\
                                                      v         --|--- (plex server)
                                                ||categorize|| --/
                                                      v
                                                  ||route|| (nginx reverse proxy and pihole DNS/sinkhole)
                                                      v
                                                 ||request|| (ombi requests, app or web)
                                                      v
                                                 ||present|| (plex pro front end service}
                                                  
 
                 This was made for using with Synology 1520+ NAS. You will need to SSH into 
                 the box in order to install the docker containers by using docker-compose. 
                 The default docker application for the NAS does not allow near as much 
                 configuration alone if you want this to fully work with static IP addresses 
                 and  ports which is why i wrote upmy own configuration file. If set up correct 
                 all the services should be accessible from your NAS IP address and using the 
                 port for each service. This can also be run using a swarm, tested and no issues. 
                 This will create a brigded connection with your NAS while still allowing 
                 communication betweeen inside and outside traffic without placing it directly 
                 onto the host network.
                 
                 Things you do need in order to actually benifit from using this is, a UNET 
                 account(s), membership to some indexers, space to store the data, and some 
                 know-how-to when it comes to networking, VM/Containers, linux shell, UNET, 
                 web configuration, patience and trouble shooting skills. You will also need 
                 to configure the front end of Prowlarr, Sonarr, Radarr, Lidarr, NZBGet, Ombi and 
                 Plex server in regards to folder/path mapping.
                 
                    /<your storage volume>/servers/lidarr/config:/config
                    /<your storage volume>/servers/nzbget/config:/config
                    /<your storage volume>/servers/ombi/config:/config
                    /<your storage volume>/servers/plex/config:/config
                    /<your storage volume>/servers/prowlarr/config:/config
                    /<your storage volume>/servers/radarr/config:/config
                    /<your storage volume>/servers/sonarr/config:/config
                    /<your storage volume>/storage/downloads/unet/complete/movies:/storage/downloads/unet/complete/movies
                    /<your storage volume>/storage/downloads/unet/complete/music:/storage/downloads/unet/complete/music
                    /<your storage volume>/storage/downloads/unet/complete/series:/storage/downloads/unet/complete/series
                    /<your storage volume>/storage/downloads/unet:/storage/downloads/unet
                    /<your storage volume>/storage/media/movies:/storage/media/movies
                    /<your storage volume>/storage/media/movies:/storage/movies
                    /<your storage volume>/storage/media/music:/storage/media/music
                    /<your storage volume>/storage/media/music:/storage/music
                    /<your storage volume>/storage/media/series:/storage/media/series
                    /<your storage volume>/storage/media/series:/storage/series
                 
                 You will need to create the following folders in the same hierarchy if you 
                 want this to work out of the box. This can also be acheived on a windows box. 
                 To initiate the plex server front end you need to add /web after your port 
                 number, ex: 192.168.0.10:32400/web. After it inititates it might just sit on 
                 a grey screen. Just close it and reenter and it should be ready for configuration.
                 
                 After you have your prefered docker-compose configuration set the way you 
                 like it, updating services are SUPER simple. The benifit to saving your server 
                 configurations on a mapped path instead of the default is that when you remove 
                 containers the configurations will not be deleted. This allows for quick 
                 redeployments without needing to worry about having to reconfigure all of 
                 your services. If you are using nightly, even latest docker images, you can 
                 fall behind on service updates very quickly. Staying up-to-date with these services 
                 are critical and enchancements so it is something you want to keep up with.
                 
                 In order to deploy new updates all you will need to do is SSH into your NAS 
                 box: 
                 
                 (windows cmd > ssh username@<NAS IP> -p <port> > enter your credentials for user)
                 
                 and execute docker-compose. In order to do this you will need to cd to your 
                 docker-compose.yml location and execute the command: 
                 
                 sudo docker-compose down --remove-orphans, enter your credentials. 
                 
                 Once it has taken all the services down and removed them (it will display 
                 the status in the command box) rerun the docker-compose tool again with 
                 the following command:
                 
                 sudo docker-compose pull, enter your credentials. 
                 
                 This will pull the new docker images if they have been updated from the 
                 repositories. Once it has completed downloading the new images run: 
                 
                 sudo docker-compose up -d, enter your credentials. 
                 
                 This will bring all of your services back up and online with the updated 
                 services, no configurations needed. If you want to see live logs then do 
                 not run detached by removing the -d from the command. To eliminate having 
                 to enter your credentials for sudo everytime you can type: sudo -i when 
                 you log into the ssh box and enter your credentials. This will give you root 
                 access to the box and you will not need to run using sudo.
                 
                 Set up a nginx server to forward incoming requests to the appropriate servers. 
                 Set up stream servers for port 32400 as well to help better serve plex service if needed.
                 
                 Website was created using Django module. Listener and reddit/graph api bot created by me however I have
                 not picked back up on that project. Todo is to change db from SQL to sqllite db since the data isn't
                 to intenseive for storage. I also plan on inclduing a Redis server for key storage eventually. This is just a
                 daily project/hobby hosting all services including website (https://thewensels.com) from my home on a 24/7 linux box.
                 
                 ![image](https://user-images.githubusercontent.com/46492607/191103068-cbeb60a4-05a5-43c7-beda-e651febb91cc.png)
                 ![image](https://user-images.githubusercontent.com/46492607/191103447-6299a8c7-fe23-4f79-bd70-a5155381552c.png)


