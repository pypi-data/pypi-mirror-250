# -*- encoding: utf-8 -*-
"""
@File    :   Process.py
@Time    :   2022-09-05 09:17
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   进程信息获取
"""
import psutil


class NewProcess:
	def __init__(self, cmd):
		"""
		通过命令查找进程ID
		:param cmd: 需要查找的已运行的命令，例如：nginx
		"""
		self.cmd = cmd
		self.pid = None
		self.ppid = None

	def get_pid(self, cmd=None):
		"""
		通过命令获取PID
		:param cmd: 可选: 传入需要获取的命令(默认使用实例化的初始参数/最后一次传参(优先)的参数)
		:return: bool(结果赋值到self.pid)
		"""
		if cmd is not None:
			self.cmd = cmd
		self.pid = None
		for proc in psutil.process_iter(['pid', 'name']):
			if proc.info['name'] == self.cmd:
				self.pid = proc.info['pid']
				return True
		return False

	def get_ppid_cmd(self, cmd=None):
		"""
		通过命令获取PPID
		:param cmd: 可选: 传入需要获取的命令(默认使用实例化的初始参数/最后一次传参(优先)的参数)
		:return: bool(结果赋值到self.ppid)
		"""
		if cmd is not None:
			self.cmd = cmd
		self.ppid = None
		if self.get_pid():
			try:
				process = psutil.Process(self.pid)
				self.ppid = process.ppid()
				return True
			except psutil.NoSuchProcess:
				print(f"Process with PID {self.pid} not found")
		return False

	def get_ppid_pid(self, pid=None):
		"""
		通过Pid获取Ppid
		:param pid: 需要获取的PID父进程
		:return: bool(结果赋值到self.ppid)
		"""
		if pid is not None:
			if self.pid is None:
				self.get_pid()
			else:
				self.pid = pid
		self.ppid = None
		try:
			process = psutil.Process(self.pid)
			self.ppid = process.ppid()
			return True
		except psutil.NoSuchProcess:
			print(f"Process with PID {pid} not found")
		return False
