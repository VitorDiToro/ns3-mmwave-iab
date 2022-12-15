#!/bin/bash


for inter_packet_interval in 50 400
do
    for n_relays in {0..4}
    do
        sed -i "s/uint32_t numRelays = [[:digit:]]*/uint32_t numRelays = $n_relays/g" ./scratch/mmwave-iab-grid-PF.cc
        sed -i "s/uint32_t interPacketInterval = [[:digit:]]*/uint32_t interPacketInterval = $inter_packet_interval/g" ./scratch/mmwave-iab-grid-PF.cc
        ./waf
        ./waf --run mmwave-iab-grid-PF >> terminal.log 2>&1
        ./mv-result.py -c PF -r $n_relays -i $inter_packet_interval
    done
done
