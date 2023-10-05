echo "Select RUN option: 1. Mininet, 2. Controller, 3. Clear mn workflow"
read CHOICE_INPUT
case $CHOICE_INPUT in
1)
    # make sure controller is started
    echo "Running mininet topology"
    sudo python3 topology/topology.py ;;
2)
    echo "Running RYU controller"
    # ryu-manager --verbose controller/l3_switch.py
    ryu-manager controller/controller.py ;;
3)
    echo "Clear the previous mininet workflow"
    sudo mn -c ;;
*)
    echo "Wrong option !!" ;;
esac