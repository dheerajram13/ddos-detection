import joblib
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import pandas as pd

import switch
from datetime import datetime



class FlowMonitor(switch.SimpleSwitch13):
    """
    Ryu application for monitoring and classifying network flow statistics.
    Extends the SimpleSwitch13 application.
    """

    def __init__(self, *args, **kwargs):
        super(FlowMonitor, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)

        start_time = datetime.now()

        self.train_flow_classifier()

        end_time = datetime.now()
        print("Training time: ", (end_time - start_time))
    
    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        """
        Handle asynchronous switch state change events.
        Register or unregister datapaths as they connect or disconnect.
        """

        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('Register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('Unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def _monitor(self):
        """
        Continuously monitor datapaths, request flow statistics, and perform classification.
        """
        
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(10)
            self.predict()

    def _request_stats(self, datapath):
        """
        Send flow statistics request to a datapath.
        """
        
        self.logger.debug('Send stats request: %016x', datapath.id)
        parser = datapath.ofproto_parser
        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def flow_stats_reply_handler(self, ev):
        """
        Handle flow statistics replies from datapaths.
        Extract and log flow statistics to a CSV file.
        """

        timestamp = datetime.now()
        timestamp = timestamp.timestamp()

        file0 = open("PredictFlowStatsfile.csv", "w")
        file0.write('timestamp,datapath_id,flow_id,ip_src,tp_src,ip_dst,tp_dst,ip_proto,icmp_code,icmp_type,flow_duration_sec,flow_duration_nsec,idle_timeout,hard_timeout,flags,packet_count,byte_count,packet_count_per_second,packet_count_per_nsecond,byte_count_per_second,byte_count_per_nsecond\n')
        body = ev.msg.body
        icmp_code = -1
        icmp_type = -1
        tp_src = 0
        tp_dst = 0

        for stat in sorted([flow for flow in body if flow.priority == 1],
                           key=lambda flow: (flow.match['eth_type'], flow.match['ipv4_src'], flow.match['ipv4_dst'], flow.match['ip_proto'])):

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

            flow_id = str(ip_src) + str(tp_src) + str(ip_dst) + str(tp_dst) + str(ip_proto)

            try:
                packet_count_per_second = stat.packet_count / stat.duration_sec
                packet_count_per_nsecond = stat.packet_count / stat.duration_nsec
            except ZeroDivisionError:
                packet_count_per_second = 0
                packet_count_per_nsecond = 0

            try:
                byte_count_per_second = stat.byte_count / stat.duration_sec
                byte_count_per_nsecond = stat.byte_count / stat.duration_nsec
            except ZeroDivisionError:
                byte_count_per_second = 0
                byte_count_per_nsecond = 0

            file0.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
                timestamp, ev.msg.datapath.id, flow_id, ip_src, tp_src, ip_dst, tp_dst,
                stat.match['ip_proto'], icmp_code, icmp_type,
                stat.duration_sec, stat.duration_nsec,
                stat.idle_timeout, stat.hard_timeout,
                stat.flags, stat.packet_count, stat.byte_count,
                packet_count_per_second, packet_count_per_nsecond,
                byte_count_per_second, byte_count_per_nsecond))
            
        file0.close()

    def train_flow_classifier(self):
        """
        Train a Random Forest Classifier to classify network flows.
        """

        self.logger.info("Flow Training ...")

        flow_dataset = pd.read_csv('FlowStatsfile.csv')

        flow_dataset.iloc[:, 2] = flow_dataset.iloc[:, 2].str.replace('.', '')
        flow_dataset.iloc[:, 3] = flow_dataset.iloc[:, 3].str.replace('.', '')
        flow_dataset.iloc[:, 5] = flow_dataset.iloc[:, 5].str.replace('.', '')

        X_flow = flow_dataset.iloc[:, [3, 10, 15, 16]].values
        X_flow = X_flow.astype('float64')

        y_flow = flow_dataset.iloc[:, -1].values

        X_flow_train, X_flow_test, y_flow_train, y_flow_test = train_test_split(X_flow, y_flow, test_size=0.3, random_state=0)

        classifier = RandomForestClassifier(n_estimators=100, criterion="entropy", max_depth=20, random_state=0)
        self.flow_model = classifier.fit(X_flow_train, y_flow_train)
        y_flow_pred = self.flow_model.predict(X_flow_test)

    def predict(self):
        try:
            predict_flow_dataset = pd.read_csv('PredictFlowStatsfile.csv')

            predict_flow_dataset.iloc[:, 2] = predict_flow_dataset.iloc[:, 2].str.replace('.', '')
            predict_flow_dataset.iloc[:, 3] = predict_flow_dataset.iloc[:, 3].str.replace('.', '')
            predict_flow_dataset.iloc[:, 5] = predict_flow_dataset.iloc[:, 5].str.replace('.', '')

            X_predict_flow = predict_flow_dataset.iloc[:, [3, 10, 15, 16]].values
            X_predict_flow = X_predict_flow.astype('float64')
            trained_model = joblib.load("rf_trained_data.joblib")
            y_flow_pred = trained_model.predict(X_predict_flow)
  
            self.logger.info("------------------------------------------------------------------------------")
            ddos_indices = [i for i, prediction in enumerate(y_flow_pred) if prediction == 1]
            legitimate_trafic = 0
            ddos_trafic = 0
            victim = 0
            for i in y_flow_pred:
                if i == 0:
                    legitimate_trafic = legitimate_trafic + 1
                else:
                    ddos_trafic = ddos_trafic + 1
                    victim = int(predict_flow_dataset.iloc[i, 5])%20

            if ddos_indices:
                self.logger.info("DDoS Traffic Detected")
                self.logger.info("ddos trafic ...")
                if victim != 0:
                    self.logger.info("victim is host: h{}".format(victim))
            else:
                self.logger.info("No DDoS Traffic Detected")
            self.logger.info("------------------------------------------------------------------------------")

            file0 = open("PredictFlowStatsfile.csv", "w")
            file0.write('timestamp,datapath_id,flow_id,ip_src,tp_src,ip_dst,tp_dst,ip_proto,icmp_code,icmp_type,flow_duration_sec,flow_duration_nsec,idle_timeout,hard_timeout,flags,packet_count,byte_count,packet_count_per_second,packet_count_per_nsecond,byte_count_per_second,byte_count_per_nsecond\n')
            file0.close()

        except Exception as e:
            self.logger.error("Error while classifying flows: {}".format(e))


