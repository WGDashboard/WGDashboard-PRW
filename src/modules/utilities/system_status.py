#!/bin/env python3

import psutil
import shutil
import subprocess
import time
import flask

import psutil, shutil, subprocess, time
from flask import current_app


class system_status:
    def to_json(self):
        return {
            "CPU": self.get_cpu(),
            "Memory": self.get_memory(),
            "Disks": self.get_disks(),
            "NetworkInterfaces": self.get_network(),
            "NetworkInterfacesPriority": self.get_interface_priorities(),
            "Processes": self.get_processes()
        }

    def get_cpu(self):
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "cpu_percent_per_cpu": psutil.cpu_percent(interval=1, percpu=True)
            }
        except Exception as e:
            current_app.logger.error("CPU error %s", e)
            return {}

    def get_memory(self):
        try:
            v = psutil.virtual_memory()
            s = psutil.swap_memory()

            return {
                "VirtualMemory": {
                    "total": v.total,
                    "available": v.available,
                    "percent": v.percent
                },
                "SwapMemory": {
                    "total": s.total,
                    "available": s.free,
                    "percent": s.percent
                }
            }
        except Exception as e:
            current_app.logger.error("Memory error %s", e)
            return {}

    def get_disks(self):
        disks = []
        try:
            for p in psutil.disk_partitions():
                d = psutil.disk_usage(p.mountpoint)

                disks.append({
                    "mountPoint": p.mountpoint,
                    "total": d.total,
                    "used": d.used,
                    "free": d.free,
                    "percent": d.percent
                })
        except Exception as e:
            current_app.logger.error("Disk error %s", e)

        return disks

    def get_network(self):
        try:
            first = psutil.net_io_counters(pernic=True)
            time.sleep(1)
            second = psutil.net_io_counters(pernic=True)

            result = {}

            for iface in first:
                sent = (second[iface].bytes_sent - first[iface].bytes_sent) / 1024 / 1024
                recv = (second[iface].bytes_recv - first[iface].bytes_recv) / 1024 / 1024

                result[iface] = {
                    **first[iface]._asdict(),
                    "realtime": {
                        "sent": round(sent, 4),
                        "recv": round(recv, 4)
                    }
                }

            return result

        except Exception as e:
            current_app.logger.error("Network error %s", e)
            return {}

    def get_interface_priorities(self):
        try:
            if not shutil.which("ip"):
                return {}

            result = subprocess.check_output(["ip", "route", "show"]).decode()

            priorities = {}

            for line in result.splitlines():
                if "metric" in line and "dev" in line:
                    parts = line.split()
                    dev = parts[parts.index("dev") + 1]
                    metric = int(parts[parts.index("metric") + 1])

                    priorities.setdefault(dev, metric)

            return priorities

        except Exception as e:
            current_app.logger.error("Interface priority error %s", e)
            return {}

    def get_processes(self):
        cpu_list = []
        mem_list = []

        try:
            for proc in psutil.process_iter():

                try:
                    name = proc.name()
                    cmd = " ".join(proc.cmdline())
                    pid = proc.pid

                    cpu = proc.cpu_percent()
                    mem = proc.memory_percent()

                    cpu_list.append({
                        "name": name,
                        "command": cmd,
                        "pid": pid,
                        "percent": cpu
                    })

                    mem_list.append({
                        "name": name,
                        "command": cmd,
                        "pid": pid,
                        "percent": mem
                    })

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            cpu_list.sort(key=lambda x: x["percent"], reverse=True)
            mem_list.sort(key=lambda x: x["percent"], reverse=True)

            return {
                "cpu_top_10": cpu_list[:20],
                "memory_top_10": mem_list[:20]
            }

        except Exception as e:
            current_app.logger.error("Process error %s", e)
            return {}