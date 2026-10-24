# Record PC <-> MG400 traffic while DobotLink / Studio Pro switch the robot into API mode.
# Run as administrator: .\capture.ps1 start   ...do the Studio Pro steps...   .\capture.ps1 stop
param([ValidateSet('start', 'stop')][string]$Action = 'start')
$robot = '192.168.1.6'
$dir = 'C:\temp'
switch ($Action) {
    'start' {
        New-Item -ItemType Directory -Force $dir | Out-Null
        pktmon filter remove | Out-Null
        pktmon filter add -i $robot
        pktmon start --capture --pkt-size 0 -f "$dir\dobot.etl"
        Write-Host "Recording. Now open DobotLink and Studio Pro, connect, then run: .\capture.ps1 stop"
    }
    'stop' {
        pktmon stop
        pktmon etl2pcap "$dir\dobot.etl" -o "$dir\dobot.pcapng"
        pktmon filter remove
        Copy-Item "$dir\dobot.pcapng" $PSScriptRoot -Force
        Write-Host "Saved $PSScriptRoot\dobot.pcapng"
    }
}
