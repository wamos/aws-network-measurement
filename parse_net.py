import pickle, os, sys

def parse_net_rx_log(out,log,log_item):
	line_count=0
	outfile = open(out, "w")
	with open(log,"r") as logfile:
		for line in logfile:
			bread=0
			bwrite=0
			parse_line=line.replace("\n","")
			## the following if subject to change wirg different iface cnofig
			if "IFACE" in parse_line or "lo" in parse_line:
				line_count+=1
				continue
			elif "ens3" in parse_line and len(parse_line) > 0 and "Average" not in parse_line:
				splitline= parse_line.split(" ")
				splitline = filter(None, splitline) # filter out empty strs
				# change index here to parse txkB/s and rxkB/s
				#print(splitline)
				rx_rate = float(splitline[4])
				tx_rate = float(splitline[5])
				outfile.write(str(rx_rate*1000)+"\n")
				line_count+=1
			else:
				line_count+=1
				continue
	outfile.close()

def parse_net_tx_log(out,log,log_item):
	line_count=0
	outfile = open(out, "w")
	with open(log,"r") as logfile:
		for line in logfile:
			bread=0
			bwrite=0
			parse_line=line.replace("\n","")
			## the following if subject to change wirg different iface cnofig
			if "IFACE" in parse_line or "lo" in parse_line:
				line_count+=1
				continue
			elif "ens3" in parse_line and len(parse_line) > 0 and "Average" not in parse_line:
				splitline= parse_line.split(" ")
				splitline = filter(None, splitline) # filter out empty strs
				#if len(splitline) <= 7: # change index here to parse txkB/s and rxkB/s
				#print(splitline)
				rx_rate = float(splitline[4])
				tx_rate = float(splitline[5])
				outfile.write(str(tx_rate*1000)+"\n")
				line_count+=1
			else:
				line_count+=1
				continue
	outfile.close()



log_item = sys.argv[1]
log_file = sys.argv[2]
out_file = sys.argv[3]

if log_item == "rx":
    parse_net_rx_log(out_file,log_file,log_item)
elif log_item == "tx":
    parse_net_tx_log(out_file,log_file,log_item)
else:
    print("illegal args")


