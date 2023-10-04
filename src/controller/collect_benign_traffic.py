from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub

import switch

from datetime import datetime

class CollectTrainingStatsApp(switch.SimpleSwitch13):
    """
    Ryu application for collecting flow statistics and saving them to a CSV file.
    """

    def __init__(self, *args, **kwargs):
        super(CollectTrainingStatsApp, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self.monitor)

        # Initialize the CSV file for flow statistics
        with open("FlowStatsfile.csv", "w") as file0:
            file0.write('timestamp,datapath_id,flow_id,ip_src,tp_src,ip_dst,tp_dst,ip_proto,icmp_code,icmp_type,flow_duration_sec,flow_duration_nsec,idle_timeout,hard_timeout,flags,packet_count,byte_count,packet_count_per_second,packet_count_per_nanosec,byte_count_per_second,byte_count_per_nanosec,label\n')

    # Asynchronous message
    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def monitor(self):
        while True:
            for dp in self.datapaths.values():
                self.request_stats(dp)
            hub.sleep(10)

    def request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        parser = datapath.ofproto_parser
        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        timestamp = datetime.now().timestamp()
        icmp_code = -1
        icmp_type = -1
        tp_src = 0
        tp_dst = 0

        with open("FlowStatsfile.csv", "a+") as file0:
            body = ev.msg.body
            for stat in sorted([flow for flow in body if flow.priority == 1], key=lambda flow:
                               (flow.match['eth_type'], flow.match['ipv4_src'], flow.match['ipv4_dst'], flow.match['ip_proto'])):
                ip_src = stat.match['ipv4_src']
                ip_dst = stat.match['ipv4_dst']
                ip_proto = stat.match['ip_proto']

                if ip_proto == 1:
                    icmp_code = stat.match['icmpv4_code']
                    icmp_type = stat.match['icmpv4_type']
                elif ip_proto == 6:
                    tp_src = stat.match['tcp_src']
                    tp_dst = stat.match['tcp_dst']
                elif ip_proto == 17:
                    tp_src = stat.match['udp_src']
                    tp_dst = stat.match['udp_dst']

                flow_id = f"{ip_src}{tp_src}{ip_dst}{tp_dst}{ip_proto}"

                try:
                    packet_count_per_second = stat.packet_count / stat.duration_sec
                    packet_count_per_nanosec = stat.packet_count / stat.duration_nsec
                except:
                    packet_count_per_second = 0
                    packet_count_per_nanosec = 0

                try:
                    byte_count_per_second = stat.byte_count / stat.duration_sec
                    byte_count_per_nanosec = stat.byte_count / stat.duration_nsec
                except:
                    byte_count_per_second = 0
                    byte_count_per_nanosec = 0

                file0.write(f"{timestamp},{ev.msg.datapath.id},{flow_id},{ip_src},{tp_src},{ip_dst},{tp_dst},{stat.match['ip_proto']},{icmp_code},{icmp_type},{stat.duration_sec},{stat.duration_nsec},{stat.idle_timeout},{stat.hard_timeout},{stat.flags},{stat.packet_count},{stat.byte_count},{packet_count_per_second},{packet_count_per_nanosec},{byte_count_per_second},{byte_count_per_nanosec},0\n")

