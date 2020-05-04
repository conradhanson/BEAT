# BEAT

Home to the **B**usiness **E**xtraction through **A**utomation **T**ool.

- Using Selenium, Crawls G Maps and collects business info based on city, state and subject searched
- Stores business information of run in a CSV

## Docker

### Build

    cd /BEAT/

    docker build -t BEAT:latest .


### Run

    docker run --shm-size=2g \
                -v $PWD/results:/src/results/ \
                --name BEAT_container
                BEAT:latest
