# **BEAT**

**B**usiness **E**xtraction via **A**utomation **T**ool

- Using *Selenium* and *pyvirtualdisplay*, BEAT:
  - crawls G Maps headlessly via *XVFB* (X Virtual Frame Buffer)
  - searches for a subject near each city within a state (searches cities alphabetically)
  - collects name, URL, phone, city, state from results
- Stores information from each city in a CSV
- Runs in a *Docker* container for portability and dependency management
- Takes positional and optional arguments in *docker run* command
  - Can start searches at a particular city with optional

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
