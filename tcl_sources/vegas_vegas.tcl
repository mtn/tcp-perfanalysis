#Based on example at http://nile.wpi.edu/NS/simple_ns.html
# FTP is used to generate traffic between nodes
# This was chosen because it generates a steady stream of traffic

set ns [new Simulator]

# Sources are green, sinks are red
$ns color 1 Green
$ns color 2 Red

set nf [open out.nam w]
$ns namtrace-all $nf

proc finish {} {
    global ns nf
    $ns flush-trace

    # Close the NAM trace file
    close $nf

    # Execute NAM on the tracefile
    exec nam out.nam &
    exit 0
}

# Create the five nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

# Create the links between nodes
# These are analagous to physical links and are bidirectional
$ns duplex-link $n1 $n2 10Mb 10ms DropTail
$ns duplex-link $n2 $n5 10Mb 10ms DropTail
$ns duplex-link $n3 $n2 10Mb 10ms DropTail
$ns duplex-link $n3 $n6 10Mb 10ms DropTail
$ns duplex-link $n3 $n4 10Mb 10ms DropTail

# Set the orientation of nodes (for rendering in NAM)
$ns duplex-link-op $n1 $n2 orient right-down
$ns duplex-link-op $n2 $n5 orient left-down
$ns duplex-link-op $n3 $n2 orient left
$ns duplex-link-op $n3 $n6 orient right-down
$ns duplex-link-op $n3 $n4 orient right-up

# Set up tcp connection between node 1 and node 4
set tcp_source_1 [new Agent/TCP/Vegas]
$ns attach-agent $n1 $tcp_source_1
set tcp_sink_4 [new Agent/TCPSink]
$ns attach-agent $n4 $tcp_sink_4
$ns connect $tcp_source_1 $tcp_sink_4

# Set up FTP application between node 1 and ndoe 4
set ftp_1_4 [new Application/FTP]
$ftp_1_4 attach-agent $tcp_source_1
$ftp_1_4 set type_ FTP

# Set up tcp connection between node 5 and node 6
set tcp_source_5 [new Agent/TCP/Vegas]
$ns attach-agent $n5 $tcp_source_5
set tcp_sink_6 [new Agent/TCPSink]
$ns attach-agent $n6 $tcp_sink_6
$ns connect $tcp_source_5 $tcp_sink_6

# Set up FTP application between node 5 and node 6
set ftp_5_6 [new Application/FTP]
$ftp_5_6 attach-agent $tcp_source_5
$ftp_5_6 set type_ FTP

# Set up the UDP connection between node 2 and node 3
set udp [new Agent/UDP]
$ns attach-agent $n2 $udp
set null [new Agent/Null]
$ns attach-agent $n3 $null
$ns connect $udp $null

# Set up a CBR over UDP
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set random_ false

# Schedule events for the CBR and FTP agents
$ns at 0.1 "$cbr start"
$ns at 1.0 "$ftp_1_4 start"
$ns at 1.0 "$ftp_5_6 start"
$ns at 4.0 "$ftp_1_4 stop"
$ns at 4.0 "$ftp_5_6 stop"
$ns at 4.5 "$cbr stop"

# Call the finish procedure after 5 seconds of simulation time
$ns at 5.0 "finish"

# Run the simulation
$ns run
