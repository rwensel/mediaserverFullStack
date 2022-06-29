                                           # mediaserverFullStack

                    Rich W. 06/29/2022 Docker-Compose YAML configuration file to create 
                                  a fully automated mediaserver stack.
 
                                                 ||schedule||
                                                      v
                                                  ||monitor||
                                                      v
                                                  ||search||
                                                      v
                                                  ||fetch||
                                                      v
                                                  ||extract||
                                                      v
                                                  ||metadata||
                                                      v
                                                ||categorize||
                                                      v
                                                  ||present||
 
 This was made for using with Synology 1520+ NAS. You will need to SSH into the box in order to install 
 the docker containers by using docker-compose. The default docker application for the NAS does not allow near 
 as much configuration alone if you want this to fully work with static IP addresses and  ports which is why i wrote up
 my own configuration file. If set up correct all the services should be accessible from your NAS IP address and using 
 the port for each service. This can also be run using a swarm, tested and no issues. This will create a brigded connection 
 with your NAS while still allowing communication betweeen inside and outside traffic without placing it directly onto the 
 host network.
 
 Things you do need in order to actually benifit from using this is, a USENET account(s), membership to some indexers, 
 space to store the data, and some know-how-to when it comes to networking, VM/Containers, linux shell, USENET, web 
 configuration, patience and trouble shooting skills. You will also need to configure the front end of Prowlarr, Sonarr, 
 Radarr, Lidarr, NZBGet and Plex server in regards to folder/path mapping.
 
 You will need to create the following folders in the same hierarchy if you want this to work out of the box. This can also be 
 acheived on a windows box. To initiate the plex server front end you need to add /web after your port number, 
 ex: 192.168.0.10:32400/web. After it inititates it might just sit on a grey screen. Just close it and reenter and it should be ready
 for configuration.
 
 
 
                                    /volume1/docker/lidarr/config
                                    /volume1/docker/nzbget/config
                                    /volume1/docker/plex/config
                                    /volume1/docker/prowlarr
                                    /volume1/docker/radarr/config
                                    /volume1/docker/sonarr/config
                                    /volume1/downloads
                                    /volume1/logs/lidarr
                                    /volume1/logs/nzbget
                                    /volume1/logs/plex
                                    /volume1/logs/prowlarr
                                    /volume1/logs/radarr
                                    /volume1/logs/sonarr
                                    /volume1/music
                                    /volume1/photo
                                    /volume1/photo
                                    /volume1/transfers
                                    /volume1/video/films
                                    /volume1/video/tv
 
            To execute this run sudo docker-compose up -d in the root dir of the docker-compose.yml
            
            
            
            
            
            
![image](https://user-images.githubusercontent.com/46492607/176559111-2cc7294e-118a-4f30-8b3e-33c98847f650.png)

![image](https://user-images.githubusercontent.com/46492607/176559161-6321080a-6de5-4fd0-9db7-00e4713df103.png)

![image](https://user-images.githubusercontent.com/46492607/176559202-71c9210b-59e6-44d1-ac00-3c99dc131119.png)

![image](https://user-images.githubusercontent.com/46492607/176559287-796691e7-afde-4c71-a99a-cd9b6e54276e.png)
