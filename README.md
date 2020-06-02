# **BEAT**

Home to the **B**usiness **E**xtraction through **A**utomation **T**ool.

- Using Selenium and pyvirtualdisplay, BEAT:
  - crawls G Maps
  - collects business info based on city, state, subject searched
  - does so headless using XVFB (X Virtual Frame Buffer)
- Stores business information from each city in a CSV
- Runs in a Docker container for portability and dependency management

## **Docker**

### **Build**

    cd /BEAT/

    docker build -t <image>:<tag> .

### **Run**

    $ docker run --rm \
                 --shm-size=2g \
                 -v $(pwd)/results:/results/ \
                 --name <container name> \
                 <image>:<tag> <subject> <state> [--city <city> | -c <city>]
