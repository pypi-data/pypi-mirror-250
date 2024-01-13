# -*- coding: UTF-8 -*-
"""
设置进程网络走向
"""
from .Process import NewProcess
from .LISTEN import NewListen
from .logger import ColorLogger
from .NmcliManger import NewNmcli
from sys import exit


class IpRule:
	def __init__(self, cmd, eth=None):
		"""
		将指定命令的流量绑定到一个网卡
		:param cmd: 需要绑定的命令
		:param eth: 需要绑定的网卡(默认使用第一个连接状态的网卡)
		"""
		self.eth = eth
		self.cmd = cmd
		self.port_list = []
		self.eth_list = []  # 已连接的网卡
		self.gw = None
		self.pid = None
		self.ppid = []
		self.logger = ColorLogger(class_name=__class__.__name__)

	def get_status(self):
		"""
		获取命令状态(是否运行中)
		:return:
		"""
		p = NewProcess(self.cmd)
		if not p.get_pid():
			self.logger.error("无法获取Pid")
			exit(2)
		self.pid = p.pid

	def get_port(self):
		"""
		获取端口列表
		:return:
		"""
		p = NewListen(pid=self.pid)
		p.get_listen_list_tcp()

	def get_eth(self):
		"""
		获取网卡列表
		:return:
		"""
		n = NewNmcli()
		self.eth_list = n.get_dev_list_connected()
		if self.eth is None:
			self.eth = self.eth_list[0]
			print("未设置网卡,自动使用: " + self.eth)
		if self.eth not in self.eth_list:
			print("网卡未连接: ", self.eth)
			exit(2)

	def start(self):
		self.get_eth()
		self.get_status()
		self.get_port()


if __name__ == "__main__":
	r = IpRule(cmd="sshd", eth=0)
	r.start()
