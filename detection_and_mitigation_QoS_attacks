#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/wifi-module.h"
#include "ns3/mobility-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-helper.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("DetectAndMitigateQoSAttacks");

void CheckQoS(Ptr<FlowMonitor> monitor, Ptr<Ipv4FlowClassifier> classifier, uint32_t nClients, uint32_t &rogueCount)
{
  std::map<FlowId, FlowMonitor::FlowStats> stats = monitor->GetFlowStats();
  for (std::map<FlowId, FlowMonitor::FlowStats>::const_iterator i = stats.begin(); i != stats.end(); ++i)
  {
    Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow(i->first);
    if (t.sourceAddress != Ipv4Address("10.1.3.1")) // assuming 10.1.3.1 is the AP
    {
      // Detect if QoS marking is abused (e.g., excessive high-priority traffic)
      if (i->second.txPackets > 100 && i->second.txBytes / i->second.txPackets > 1000) // arbitrary conditions for detection
      {
        rogueCount++;
        NS_LOG_INFO("Rogue user detected: " << t.sourceAddress);
        // Take action based on policy
        if (rogueCount > nClients * 0.1) // if more than 10% of clients are rogue
        {
          NS_LOG_INFO("Taking action against: " << t.sourceAddress);
          // Penalty: reduce bandwidth, downgrade priority, or block
          // For this example, we just log the action
          NS_LOG_INFO("Bandwidth reduction or blocking for user: " << t.sourceAddress);
        }
      }
    }
  }
  Simulator::Schedule(Seconds(1.0), &CheckQoS, monitor, classifier, nClients, std::ref(rogueCount));
}

int main(int argc, char *argv[])
{
  uint32_t nClients = 100;
  CommandLine cmd;
  cmd.AddValue("nClients", "Number of clients", nClients);
  cmd.Parse(argc, argv);

  NodeContainer wifiStaNodes;
  wifiStaNodes.Create(nClients);
  NodeContainer wifiApNode;
  wifiApNode.Create(1);

  YansWifiChannelHelper channel = YansWifiChannelHelper::Default();
  YansWifiPhyHelper phy = YansWifiPhyHelper::Default();
  phy.SetChannel(channel.Create());

  WifiHelper wifi;
  wifi.SetRemoteStationManager("ns3::AarfWifiManager");

  WifiMacHelper mac;
  Ssid ssid = Ssid("ns-3-ssid");

  mac.SetType("ns3::StaWifiMac", "Ssid", SsidValue(ssid), "ActiveProbing", BooleanValue(false));
  NetDeviceContainer staDevices = wifi.Install(phy, mac, wifiStaNodes);

  mac.SetType("ns3::ApWifiMac", "Ssid", SsidValue(ssid));
  NetDeviceContainer apDevice = wifi.Install(phy, mac, wifiApNode);

  MobilityHelper mobility;
  mobility.SetPositionAllocator("ns3::GridPositionAllocator",
                                "MinX", DoubleValue(0.0),
                                "MinY", DoubleValue(0.0),
                                "DeltaX", DoubleValue(5.0),
                                "DeltaY", DoubleValue(10.0),
                                "GridWidth", UintegerValue(10),
                                "LayoutType", StringValue("RowFirst"));
  mobility.SetMobilityModel("ns3::RandomWalk2dMobilityModel", "Bounds", RectangleValue(Rectangle(-50, 50, -50, 50)));
  mobility.Install(wifiStaNodes);

  mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
  mobility.Install(wifiApNode);

  InternetStackHelper stack;
  stack.Install(wifiApNode);
  stack.Install(wifiStaNodes);

  Ipv4AddressHelper address;
  address.SetBase("10.1.3.0", "255.255.255.0");

  Ipv4InterfaceContainer staInterfaces = address.Assign(staDevices);
  Ipv4InterfaceContainer apInterface = address.Assign(apDevice);

  UdpEchoServerHelper echoServer(9);
  ApplicationContainer serverApps = echoServer.Install(wifiApNode.Get(0));
  serverApps.Start(Seconds(1.0));
  serverApps.Stop(Seconds(20.0));

  UdpEchoClientHelper echoClient(apInterface.GetAddress(0), 9);
  echoClient.SetAttribute("MaxPackets", UintegerValue(100));
  echoClient.SetAttribute("Interval", TimeValue(Seconds(1.0)));
  echoClient.SetAttribute("PacketSize", UintegerValue(1024));

  ApplicationContainer clientApps;
  for (uint32_t i = 0; i < nClients; ++i)
  {
    clientApps.Add(echoClient.Install(wifiStaNodes.Get(i)));
  }
  clientApps.Start(Seconds(2.0));
  clientApps.Stop(Seconds(20.0));

  FlowMonitorHelper flowmonHelper;
  Ptr<FlowMonitor> flowmon = flowmonHelper.InstallAll();
  Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier>(flowmonHelper.GetClassifier());

  uint32_t rogueCount = 0;
  Simulator::Schedule(Seconds(1.0), &CheckQoS, flowmon, classifier, nClients, std::ref(rogueCount));

  Simulator::Run();
  Simulator::Destroy();
  return 0;
}
