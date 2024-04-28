# Github-Sub

## Deployment 
### docker
- dockerfile과 docker-compose.yml을 참조하십시오 

도커허브에서 [빌드된 이미지](https://hub.docker.com/repository/docker/rejs/github-sub/general)를 얻으실 수 있습니다. 

### Env
.env 파일이 필요합니다. 
.env 파일의 구성은 아래와 같습니다

```.env
# [openai]
OPENAI_API_KEY=
OUTPUT_MODEL=

# [db]
DATABASE_URL=

# [redis]
REDIS_HOST=
REDIS_PORT=

# [selenium]
SELENIUM_HUB_URL=http://localhost:4444/wd/hub
```