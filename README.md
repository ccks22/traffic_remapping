Setting Up the Network:
Creates one access point (wifiApNode) and 100 client nodes (wifiStaNodes).
Configures the Wi-Fi channel and PHY layer using YansWifiChannelHelper and YansWifiPhyHelper.
Uses WifiHelper and WifiMacHelper to set up the Wi-Fi devices with SSID "ns-3-ssid".
//---------------------------------------------------------------------------------------------
Mobility:
Configures the mobility model for clients and access point. Clients move randomly within a bounded area, and the access point has a fixed position.

MinX: This is the minimum X-coordinate of the grid. It sets the starting point for the first node on the X-axis.
Example: MinX = 0.0 means the grid starts at X-coordinate 0.

MinY: This is the minimum Y-coordinate of the grid. It sets the starting point for the first node on the Y-axis.
Example: MinY = 0.0 means the grid starts at Y-coordinate 0.

DeltaX: This is the distance between adjacent nodes along the X-axis. It defines the horizontal spacing between nodes.
Example: DeltaX = 5.0 means each node is 5 units apart horizontally.

DeltaY: This is the distance between adjacent nodes along the Y-axis. It defines the vertical spacing between nodes.
Example: DeltaY = 10.0 means each node is 10 units apart vertically.

GridWidth: This specifies the number of nodes in each row of the grid. After this number of nodes, the next node starts a new row.
Example: GridWidth = 10 means there will be 10 nodes in each row before starting a new row.

LayoutType: This defines how the nodes are laid out in the grid. The most common value is "RowFirst", which means nodes are placed row by row. Another possible value is "ColumnFirst", where nodes are placed column by column.
Example: LayoutType = "RowFirst" means nodes are placed left to right in rows, filling up each row before moving to the next.

//-----------------------------------------------------------------------------------------------------------------------------------------
Network Stack:
Installs the internet stack on all nodes.
Assigns IP addresses to the Wi-Fi interfaces.
//-----------------------------------------------------------------------------------------------------------------------------------------
Applications:
Sets up a UDP echo server on the access point.
Installs UDP echo clients on all 100 client nodes.
//-----------------------------------------------------------------------------------------------------------------------------------------
QoS Marking:
The ChangeQos function changes the QoS marking of outgoing packets to prioritize them as voice or video traffic for rogue users.
The ScheduleRogueUsers function schedules the ChangeQos function to run incrementally for each user.
//-----------------------------------------------------------------------------------------------------------------------------------------
Incrementing Rogue Users:
A loop is used to schedule the increment of rogue users. Every second, a new rogue user is added, starting with 0 rogue users and incrementing by the specified increment value.
//-----------------------------------------------------------------------------------------------------------------------------------------
Flow Monitor:
Uses the FlowMonitor module to track and print the performance metrics such as throughput, delay, and packet loss to identify the point where the network is negatively affected.
