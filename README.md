# Datacenter Systems class project

## Variables to test
- Per-packet processing cost- use encryption to try to steal the CPU?
- High bps
- High pps
- Bursty traffic: mimic real traffic, don’t look like a DDoS attack, maybe avoid the rate limiter
- Traffic type - Andromeda rate-limits UDP to 10mbps, but having those packets wait in the shaper queues can cause the TCP packets stuck behind them to get delayed. Different classes of traffic get throttled differently in Andromeda. Need to see how AWS does it.
## Variables for receiver to measure
- Spikes in latency: RTTs for ping (unthrottled on Andromeda), RTTs for TCP (might be throttled?)
- Packet loss
- Experiments
## Testing on cheap VMs
- 2 VMs anywhere in the datacenter send traffic and receive traffic, receiver attempts to send traffic at, say, half the normal rate and sees if it experiences increased RTT or packet loss (I don’t expect much)
- 1 VM send different types of traffic (ICMP, UDP, TCP) as fast as it can for 30 seconds. See if it gets rate limited. If not in 30 seconds, try for longer - 5 mins.
- Record any environment changes that have to be made or anything that has to be installed and put it in a config script
- See how long experiments have to run to see effects, if we can.
## Dedicated host + VPC
### 2 VMs
- Adversary blasts ICMP: Smallest of the small packets, probably unthrottled
- Adversary blasts small packets: overwhelm ingress engine where processing costs are per-packet. UDP and TCP
- Adversary bursts small packets: overwhelm ingress engine where processing costs are per-packet, and avoid getting rate limited if possible. UDP and TCP
- Adversary blasts MTU packets: cause bandwidth overload at ingress engine. Goal is >16Gbps for adversary, 20 Mbps for victim, b/c that’s what PicNic said caused packet drops and increased RTTs. UDP and TCP
- Adversary bursts MTU packets: cause bandwidth overload at ingress engine. UDP and TCP
### 10 VMs (or however many)
Same as above, unless we find (for example) that blasting small TCP isn’t as effective as blasting UDP b/c the packets are larger, or vice versa b/c TCP packets take more processing.
## Placement Groups
To be determined if we have enough time to run these experiments. I suspect we won't.

