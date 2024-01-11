# -*- encoding: utf-8 -*-
"""
@File    :   NmcliManger.py
@Time    :   2022/04/17 01:06:40
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   liumou.site@qq.com
@Homepage : https://liumou.site
@Desc    :   网络管理模块
"""
import ipaddress
import re
import socket
import subprocess

from .Cmd import NewCommand
from .base import list_get_len
from .logger import ColorLogger


class NetManagement(object):
	def __init__(self, password=None, ip=None, gw=None, mask=24, dns1=None, dns2=None, net=None, dev=None, log=True):
		"""
		网络管理模块,参数均为可选传参，请根据实际需求传入
		:param password: (str, optional): 设置主机密码. Defaults to None.
		:param ip: (str, optional): 设置IP地址. Defaults to "192.168.1.138".
		:param gw: (str, optional): 设置网关. Defaults to "192.168.1.1".
		:param mask: (int, optional): 设置子网掩码. Defaults to 24.
		:param dns1: (str, optional): 设置DNS1. Defaults to "114.114.114.114".
		:param dns2: (str, optional): 设置DNS2. Defaults to "119.29.29.29".
		:param net: (str, optional): 设置网段,一般是自动尝试配置IP需要. Defaults to '192.168.1.'.
		:param dev: (str, optional): 设置网卡名称. Defaults to 'ens33'.
		:param log: (bool, optional): 是否启用日志功能
		"""
		self.DefaultDnsList = None  # 默认网卡DNS地址列表
		self.DefaultMask = None  # 默认掩码
		self.DefaultIp4 = None  # 默认IP地址
		self.DefaultGw = None  # 默认网关地址
		if ip is None:
			ip = "192.168.1.138"
		if gw is None:
			gw = "192.168.1.1"
		if dns1 is None:
			dns1 = "114.114.114.114"
		if dns2 is None:
			dns2 = "119.29.29.29"
		if net is None:
			net = "192.168.1."
		if dev is None:
			dev = 'ens33'
		self.log = log
		# 主机密码
		self.password = password
		# 网段
		self.net = net
		# 子网地址
		self.subnet = None
		# IP地址
		self.ipv4 = ip
		# 网关
		self.gateway = gw
		# DNS1
		self.dns1 = dns1
		# DNS2
		self.dns2 = dns2
		# 子网掩码
		self.netmask = mask
		# 连接名称
		self.connect_name = 'Y'
		# 连接模式
		self.connect_mode = 'auto'
		# DNS列表
		self.dns_list = []
		# 网卡设备
		self.device = dev
		self.DefaultDev = None  # 默认网卡设备名称
		self.deviceList = []  # 网卡列表
		self.logger = ColorLogger()
		# ju = Jurisdiction(passwd=password)
		# if not ju.verification(name='NetManagement'):
		# 	self.logger.error('密码错误/用户无权限')
		# 	exit(1)
		self.cmd = NewCommand(password=password)
		self.debug = False
		self.Err = None
		self.get_default()

	def get_default(self):
		"""
		获取默认网卡信息
		:return:
		"""
		self._get_default_ipv4_socket()
		self._get_default_gateway()

	def _get_default_gateway(self):
		output = subprocess.check_output('ip route show default', shell=True)
		match = re.search(r'default via (\d+\.\d+\.\d+\.\d+) dev (\w+)', output.decode())
		if match:
			self.logger.info("默认网关获取成功")
			self.DefaultGw = match.group(1)
		else:
			self.logger.error("默认网关获取失败")
			self.DefaultGw = None
			self.Err = "无法获取默认网关"

	def _get_default_ipv4_socket(self):
		"""
		通过socket 获取本机IP,通过DefaultIp4获取实际值
		:return: bool
		"""
		try:
			hostname = socket.gethostname()
			self.DefaultIp4 = socket.gethostbyname(hostname)
			return True
		except Exception as e:
			self.logger.error(str(e))
			self.Err = str(e)
		return False

	def connect_create(self, name="Y", mode='auto'):
		"""
		创建连接
		:param name: (str, optional): 连接名称. Defaults to "Y".
		:param mode: (str, optional): 连接模式. Defaults to "auto".
		:return: bool
		"""
		self.Err = None
		c = str("""nmcli connection add type ethernet  con-name {0} ifname {1}""".format(name, self.device))
		get = self.cmd.shell(cmd=c)
		if get:
			self.logger.info("连接创建成功")
		else:
			print(c)
			self.Err = "连接创建失败"
			self.logger.error(self.Err)
			return False
		if mode != "auto":
			self.logger.debug("使用静态IP配置")
			c = str("""nmcli connection modify {0} ipv4.method manual ipv4.addresses {1}""".format(name, self.ipv4))
		else:
			self.logger.debug("使用自动获取IP")
			c = str("""nmcli connection modify {0} ipv4.method auto""".format(name))
		return self.run(c=c, n_="IP获取模式配置")

	def run(self, c, n_):
		"""
		运行命令
		:param c: 需要执行的命令
		:param n_: 命令名称
		:return: bool
		"""
		get = self.cmd.shell(cmd=c)
		if get:
			self.logger.info("[ %s ]成功" % n_)
			return True
		else:
			print(c)
			self.Err = "[ %s ]失败" % n_
			self.logger.warning(self.Err)
		return False

	def get_con_uuid(self, name):
		"""
		通过名称或者关键词获取一个连接的UUID
		:param name:
		:return:
		"""
		c = str("""nmcli connection  | grep "%s" """ % name)
		get = self.cmd.getout(c)
		if self.cmd.code == 0:
			sp = str(get).split(" ")
			sp = list_get_len(sp, 10)  # 获取元素长度大于10的元素
			if len(sp) == 1:
				return sp[0]
			if len(sp) > 1:
				for i in sp:
					ts = str(i).split("-")
					if len(ts) == 5:
						return i
		return False

	def con_delete(self, con):
		"""
		删除连接
		:param con: 需要删除的连接名称/名称关键词或者UUID
		:return: bool
		"""
		if con is None:
			con = self.connect_name
		cl = self.get_con_uuid(name=con)
		if cl:
			c = str("""nmcli connection  delete %s""" % cl)
			self.cmd.shell(c)
			if self.cmd.code != 0:
				self.logger.error("删除失败")
				return False
		else:
			self.logger.warning("无法获取连接")
		return True

	def get_dev_list(self):
		"""
		获取设备列表
		:return:bool(数据请通过 self.deviceList 获取)
		"""
		c = str("""ip link show up | grep '<' | sed 's/://g' | awk '{print $2}' | grep -v ^docker | grep -v ^lo""")
		get = self.cmd.getout(c)
		if self.cmd.code == 0:
			self.deviceList = str(get).split("\n")
			if len(self.deviceList) >= 1:
				self.logger.info("网卡信息获取成功")
				return True
		print(c)
		self.logger.error("无法获取网卡设备信息")
		return False

	def _getIp(self, lr: list):
		"""
		从列表数据中获取IPV4地址
		:param lr: 需要获取的字符串
		:return: 返回IP地址或者False
		"""
		for i in lr:
			try:
				ip = ipaddress.IPv4Address(i)
				return ip
			except:
				continue
		self.logger.warning("无法获取到IP地址")
		return False

	def get_eth_dns_list(self, eth):
		"""
		获取当前系统默认DNS信息
		:param eth: 获取指定网卡设备的DNS地址
		:return: list
		"""
		# d = []
		c = str("""nmcli device show %s | grep DNS | grep IP4| awk '{print $2}'""" % eth)
		get = self.cmd.getout(cmd=c)
		if self.cmd.code == 0:
			print(get)
			sp = str(get).split("\n")
			if len(sp) >= 1:
				return sp
		print(c)
		self.logger.warning("无法获取网卡的DNS信息: %s" % eth)
		return False

	def get_default_dev(self):
		"""
		获取默认网卡设备信息，获取到的信息请通过实例变量(Default开头)获取(网卡名称、网关、子网掩码、IP地址)
		:return: bool
		"""
		# c = str("ip r | grep default |sed -n 1p")
		# get = self.cmd.getout(cmd=c)
		self.DefaultDev = self.cmd.getout("ip r | grep default | sed -n 1p | awk '{print $5}'")
		self.DefaultGw = self.cmd.getout("ip r | grep default | sed -n 1p | awk '{print $3}'")
		self.DefaultDnsList = self.get_eth_dns_list(self.DefaultDev)
		c = str("""ip addr show %s  | grep inet | sed -n 1p | awk '{print $2}'""" % self.DefaultDev)
		get = self.cmd.getout(c)
		if self.cmd.code == 0:
			self.DefaultMask = str(get).split("/")[-1]
		return False

	def get_con_uuid_all(self):
		"""
		获取所有可用的连接UUID列表,返回数据格式: ['7dc597e8-23ad-4360-8dc3-87058a2d08aa', 'b3a484ff-73a6-4e0e-8c1a-0e829b36a848']
		:return: bool/list
		"""
		c = """nmcli con  show --active | grep -v loopback| grep -v ^NAME | grep -v ^docker0  | awk '{print $2}'"""
		get = self.cmd.getout(c)
		if self.cmd.code == 0:
			sp = str(get).split("\n")
			if len(sp) >= 1:
				return sp
		return False

	def get_con_list_eth_uuid(self, eth):
		"""
		获取指定网卡的连接配置的UUID列表,返回数据格式: ['7dc597e8-23ad-4360-8dc3-87058a2d08aa', 'b3a484ff-73a6-4e0e-8c1a-0e829b36a848']
		:return:bool/list
		"""
		c = str("""nmcli connection show | grep %s | awk '{print $2}'""" % eth)
		get = self.cmd.getout(c)
		if self.cmd.code == 0:
			sp = str(get).split("\n")
			if len(sp) >= 1:
				return sp
		return False

	def get_eth_info(self, eth):
		"""
		获取指定网卡的网络配置信息,包含: IP4、网关、掩码、DNS
		:param eth: 需要获取的网卡名称
		:return:
		"""
		c = str("""ip address show %s  | grep inet | sed -n 1p  | awk '{print $2}'""" % eth)
		info = {}
		get = self.cmd.shell(c)
		if self.cmd.code == 0:
			i = str(get).split("/")
			if len(i) == 2:
				info["mask"] = i[1]
				info["ip"] = i[0]
			else:
				self.logger.warning("IP和掩码获取失败")
		c = str("""nmcli device show %s  | grep IP4.GATE | awk '{print $2}'""" % eth)
		get = self.cmd.shell(c)
		if self.cmd.code == 0:
			info["gw"] = get
		else:
			self.logger.warning("网关获取失败")
			info["gw"] = None
		dns = self.get_eth_dns_list(eth=eth)
		if dns:
			info["dns"] = dns
		else:
			info["dns"] = []
			self.logger.warning("DNS获取失败")
		if self.get_dev_subnet(eth=eth):
			info["subnet"] = self.subnet
		return info

	def get_dev_subnet(self, eth):
		"""
		获取指定设备的子网信息
		:param eth:
		:return:
		"""
		c = f"nmcli device show {eth} | grep IP4.ROUTE | sed -n 1p | awk -F " + "= '{print $2}'"
		get = self.cmd.getout(cmd=c)
		if self.cmd.code == 0:
			txt = str(get).split(",")[0].strip()
			if len(txt.split(".")) >= 3:
				self.subnet = txt
				return True
		return False

	def get_con_dns(self, con):
		"""
		获取指定连接的DNS信息
		:param con: 需要获取的连接名称或者uuid
		:return:list
		"""
		c = str("""nmcli con show %s  | grep IP4.DNS | awk '{print $2}'""" % con)
		if self.debug:
			self.logger.debug(c)
		get = self.cmd.getout(c)
		if self.cmd.code == 0:
			ds = str(get).split("\n")
			if self.debug:
				self.logger.debug("ds: ", str(ds))
			if len(ds) >= 1:
				return ds
		self.logger.warning("无法获取连接的DNS信息")
		return [None]

	def get_con_gw(self, con):
		"""
		获取连接的网关信息
		:param con: 需要获取的连接名称或者uuid
		:return:
		"""
		c = str("""nmcli con show %s  | grep IP4.GATE | awk '{print $2}'""" % con)
		if self.debug:
			self.logger.debug(c)
		get = self.cmd.getout(c)
		if self.cmd.code == 0:
			return get
		else:
			self.logger.warning("网关获取失败")
		return None

	def get_con_ip(self, con):
		"""
		获取连接的IP地址
		:param con: 需要获取的连接名称或者uuid
		:return:
		"""
		info = {}
		c = str("""nmcli con show %s  | grep IP4.ADD | awk '{print $2}'""" % con)
		if self.debug:
			self.logger.debug(c)
		get = self.cmd.getout(c)
		if self.cmd.code == 0:
			sp = str(get).split("/")
			if self.debug:
				self.logger.debug(get)
				self.logger.debug(str(sp))
			if len(sp) == 2:
				info["ip"] = str(sp[0])
				info["mask"] = int(sp[1])
				return info

		else:
			self.logger.warning("网关获取失败")
		info["ip"] = None
		info["mask"] = 0
		return info

	def get_con_info(self, con):
		"""
		获取指定连接的网络配置信息,通过status判断获取结构, 格式: {'ip': '10.1.1.18', 'mask': 24, 'gw': '10.1.1.1', 'dns': ['10.1.1.1'], 'status': True}
		:param con: 连接名称或UUID
		:return: dict
		"""
		info = {}
		# 首先获取UUID
		c = self.get_con_uuid(name=con)
		if c:
			ip = self.get_con_ip(con=con)
			info = ip
			gw = self.get_con_gw(con=con)
			info["gw"] = gw
			dns = self.get_con_dns(con=con)
			if self.debug:
				self.logger.debug(str(dns))
			info["dns"] = dns
			info["status"] = True
			return info
		else:
			self.logger.error("无法获取连接信息,请检查配置参数")
			info["status"] = False
		return info


if __name__ == "__main__":
	n = NetManagement()
	n.get_default_dev()
