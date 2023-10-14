echo "Select RUN option: 1. RYU controller, 2. Mininet, 3. Clear mn workflow"
read CHOICE_INPUT
case $CHOICE_INPUT in

1)
    echo "Running RYU controller"
    ryu-manager src/controller/controller.py ;;
2)
    echo "Running mininet topology"
    sudo python3 src/topology/topology.py ;;
3)
    echo "Clear the previous mininet workflow"
    sudo mn -c ;;
*)
    echo "Wrong option !!" ;;
esac