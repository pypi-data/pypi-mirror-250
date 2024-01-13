import psutil


class NewEthTools:
	def __init__(self):
		self.eth_connected_list = []

	def get_connected_network_devices(self):
		self.eth_connected_list = []
		# 获取所有网络接口
		net_if_addrs = psutil.net_if_addrs()

		# 遍历网络接口
		for interface in net_if_addrs:
			# 过滤出已连接的网卡
			if net_if_addrs[interface] and net_if_addrs[interface][0].family == 2:
				print(f"Interface: {interface}")
				for addr in net_if_addrs[interface]:
					print(f"  {addr.address}, {addr.netmask}, {addr.broadcast}")


if __name__ == "__main__":
	e = NewEthTools()
	e.get_connected_network_devices()
