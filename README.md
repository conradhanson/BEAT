# BEAT

Home to the **B**usiness **E**xtraction through **A**utomation **T**ool.

- Using Selenium and pyvirtualdisplay, BEAT:
  - crawls G Maps
  - collects business info based on city, state, subject searched
  - does so headless using XVFB
- Stores business information from each city in a CSV
- Runs in a Docker container for portability and dependency management

## Docker

### Build

    cd /BEAT/

    docker build -t BEAT:latest .


### Run

    docker run --shm-size=2g \
                -v $PWD/results:/results/ \
                --name BEAT_container \
                beat:latest '2 letter state_code' 'subject'
