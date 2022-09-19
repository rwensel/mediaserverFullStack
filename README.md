                                           # mediaserverFullStack

                    Rich W. 06/29/2022 Docker-Compose YAML configuration file to create 
                                  a fully automated mediaserver stack.
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
                 
                 Things you do need in order to actually benifit from using this is, a USENET 
                 account(s), membership to some indexers, space to store the data, and some 
                 know-how-to when it comes to networking, VM/Containers, linux shell, USENET, 
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
                    /<your storage volume>/storage/downloads/usenet/complete/movies:/storage/downloads/usenet/complete/movies
                    /<your storage volume>/storage/downloads/usenet/complete/music:/storage/downloads/usenet/complete/music
                    /<your storage volume>/storage/downloads/usenet/complete/series:/storage/downloads/usenet/complete/series
                    /<your storage volume>/storage/downloads/usenet:/storage/downloads/usenet
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


![Screenshot 2022-08-09 142050](https://user-images.githubusercontent.com/46492607/183733335-73018ccc-a9b5-44d2-9fbb-279caa096210.png)
![Screenshot 2022-08-09 142120](https://user-images.githubusercontent.com/46492607/183733362-011051a6-9564-41a1-80ed-997232060803.png)
![Screenshot 2022-08-09 142156](https://user-images.githubusercontent.com/46492607/183733373-04d47946-343b-462e-b0c9-135a1feb185f.png)
![image](https://user-images.githubusercontent.com/46492607/183742594-29718785-89e3-4b14-a4ce-f857010dbfcc.png)
![image](https://user-images.githubusercontent.com/46492607/183743285-6ac0b2ec-454a-4f51-b0da-707c21fbbaf4.png)
