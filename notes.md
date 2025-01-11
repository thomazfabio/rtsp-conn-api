# exemplo de requisição para adicionar uma camera de dvr intelbras
'''{
	"user_id": "abc123",
	"device_type": "dvr",
	"manufacturer": "intelbras",
	"device_model": "hdcvi 1004 g2",
	"protocol": "rtsp",
	"ip": "192.168.15.151",
	"port": "554",
	"path": "/cam/realmonitor",
	"channel": "channel=4",
	"subtype" :"subtype=0",
	"device_user": "admin",
	"device_pass": "227802"
}'''

# exemplo de url completa dvr intelbras hdcvi 1004 g2
rtsp://admin:227802@192.168.15.151:554/cam/realmonitor?channel=4&subtype=1