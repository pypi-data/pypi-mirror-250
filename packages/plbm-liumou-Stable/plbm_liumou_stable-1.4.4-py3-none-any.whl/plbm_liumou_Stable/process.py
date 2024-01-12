# -*- encoding: utf-8 -*-
"""
@File    :   AptManage.py
@Time    :   2022-09-05 09:17
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   当前文件作用
"""
import psutil
from socket import SocketKind
from logger import ColorLogger


class NewProcess:
	def __init__(self, pid=None):
		"""

		:param pid:
		"""
		self.pid = pid
		self.logger = ColorLogger()
		self.port_list = []

	def get_listen_list(self):
		"""
		获取进程监听的所有端口
		:return:bool(是否获取成功)
		"""
		self.port_list = []
		try:
			process = psutil.Process(self.pid)
			connections = process.connections()
			for conn in connections:
				if conn.status == 'LISTEN':
					self.port_list.append(conn.laddr.port)
		except psutil.NoSuchProcess:
			self.logger.error("进程不存在: ", self.pid)
			return False
		return True

	def get_listen_list_tcp(self):
		"""
		获取进程监听的所有端口
		:return: bool(是否获取成功)
		"""
		self.port_list = []
		try:
			process = psutil.Process(self.pid)
			connections = process.connections()
			for conn in connections:
				if conn.status == 'LISTEN' and conn.type == SocketKind.SOCK_STREAM:
					self.port_list.append(conn.laddr.port)
		except psutil.NoSuchProcess:
			self.logger.error("进程不存在: ", self.pid)
			return False
		return True

	def get_listen_list_udp(self):
		"""
		获取进程监听的所有端口
		:return:
		"""
		self.port_list = []
		try:
			process = psutil.Process(self.pid)
			connections = process.connections()
			for conn in connections:
				if conn.status == 'LISTEN':
					self.port_list.append(conn.laddr.port)
		except psutil.NoSuchProcess:
			self.logger.error("进程不存在: ", self.pid)
			return False
		return True

	def get_listen_list_v4(self):
		"""
		获取进程监听的所有IPV4端口
		:return:
		"""
		self.port_list = []
		try:
			process = psutil.Process(self.pid)
			connections = process.connections()
			for conn in connections:
				if conn.status == 'LISTEN' and conn.family == 2:
					self.port_list.append(conn.laddr.port)
		except psutil.NoSuchProcess:
			self.logger.error("进程不存在: ", self.pid)
			return False
		return True

	def get_listen_list_v6(self):
		"""
		获取进程监听的所有IPV6端口
		:return:
		"""
		self.port_list = []
		try:
			process = psutil.Process(self.pid)
			connections = process.connections()
			for conn in connections:
				if conn.status == 'LISTEN' and conn.family == 10:
					self.port_list.append(conn.laddr.port)
		except psutil.NoSuchProcess:
			self.logger.error("进程不存在: ", self.pid)
			return False
		return True


if __name__ == "__main__":
	p = NewProcess(pid=5184)
	if p.get_listen_list_v4():
		print("获取成功")
		print(p.port_list)
	else:
		print("获取失败")

