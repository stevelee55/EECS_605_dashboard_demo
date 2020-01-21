#EECS_605

Required:
- Python 3.x
- Pip
- Docker


How to Run:

- macOS:

0) Install Docker for macOS (https://docs.docker.com/docker-for-mac/install/).
1) Run Docker.
2) Open Terminal.
3) Run `docker pull stevesl/eecs_605_dashboard_prototype:0`.
4) Run `docker run -d -p 8080:8080 stevesl/eecs_605_dashboard_prototype:0`.
5) Open up browser and type `localhost:8080`.

- Windows:

0) Install Docker for Windows (https://docs.docker.com/docker-for-windows/install/) for Windows 10, Docker Toolbox (https://docs.docker.com/toolbox/toolbox_install_windows/) for older Windows versions.
1) Open Docker Terminal.
2) Run `docker pull stevesl/eecs_605_dashboard_prototype:0`.
3) Run `docker run -d -p 8080:8080 stevesl/eecs_605_dashboard_prototype:0` in the Docker's bash command-line interface.
4) Run `docker-machine ip` and get the docker container's ip address.
5) Open up browser and type `<docker-machine-ip>:8080` - `<docker-machine-ip>` is from the previous step.
