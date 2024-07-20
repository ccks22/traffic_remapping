**Setting Up the Network:
**Creates one access point (wifiApNode) and 100 client nodes (wifiStaNodes).
Configures the Wi-Fi channel and PHY layer using YansWifiChannelHelper and YansWifiPhyHelper.
Uses WifiHelper and WifiMacHelper to set up the Wi-Fi devices with SSID "ns-3-ssid".

**Mobility:
**Configures the mobility model for clients and access point. Clients move randomly within a bounded area, and the access point has a fixed position.

**Network Stack:
**Installs the internet stack on all nodes.
Assigns IP addresses to the Wi-Fi interfaces.

**Applications:
**Sets up a UDP echo server on the access point.
Installs UDP echo clients on all 100 client nodes.

**QoS Marking:
**The ChangeQos function changes the QoS marking of outgoing packets to prioritize them as voice or video traffic for rogue users.
The ScheduleRogueUsers function schedules the ChangeQos function to run incrementally for each user.

**Incrementing Rogue Users:
**A loop is used to schedule the increment of rogue users. Every second, a new rogue user is added, starting with 0 rogue users and incrementing by the specified increment value.

**Flow Monitor:
**Uses the FlowMonitor module to track and print the performance metrics such as throughput, delay, and packet loss to identify the point where the network is negatively affected.
