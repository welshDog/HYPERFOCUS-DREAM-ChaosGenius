#!/usr/bin/env python3
"""
🔌⚡ BROSKI HYPER PORT MANAGER AGENT ⚡🔌
Ultra-Advanced Port Management & Allocation System
Built for the Broski Agent Army Command Portal

🎯 CAPABILITIES:
- Dynamic Port Allocation & Management
- Real-time Port Monitoring
- Service Port Mapping & Discovery
- Port Security & Access Control
- Conflict Resolution & Auto-healing
- Performance Optimization
- Neural Link Integration

Author: Broski Agent Army
Version: v3.0 - HYPER EDITION
"""

import os
import sys
import json
import time
import socket
import sqlite3
import threading
import subprocess
import psutil
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from contextlib import contextmanager
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('broski_hyper_port_manager.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class PortInfo:
    """🔌 Port Information Data Structure"""
    port: int
    protocol: str  # TCP/UDP
    status: str    # LISTENING/ESTABLISHED/CLOSED
    service: str   # Service name
    process_id: int
    process_name: str
    allocated_by: str  # Agent/Service that allocated this port
    allocation_time: datetime
    last_activity: datetime
    security_level: str  # PUBLIC/PRIVATE/RESTRICTED
    performance_score: float
    description: str

@dataclass
class PortAllocationRequest:
    """📝 Port Allocation Request Structure"""
    requester_id: str
    service_name: str
    preferred_port: Optional[int]
    port_range: Tuple[int, int]
    protocol: str
    security_level: str
    priority: int
    duration: Optional[int]  # Seconds, None for permanent
    description: str

class BroskiHyperPortManagerAgent:
    """🔌⚡ Ultimate Hyper Port Manager Agent ⚡🔌"""

    def __init__(self):
        self.agent_id = "HYPER_PORT_MANAGER_ALPHA"
        self.agent_name = "🔌 Broski Hyper Port Manager"
        self.base_path = "/root/chaosgenius"
        self.db_path = f"{self.base_path}/broski_port_manager.db"
        self.config_path = f"{self.base_path}/port_manager_config.json"

        # Port management settings
        self.port_ranges = {
            'system': (1, 1023),
            'registered': (1024, 49151),
            'dynamic': (49152, 65535),
            'broski_reserved': (30000, 35000)
        }

        # State management
        self.active_ports: Dict[int, PortInfo] = {}
        self.allocated_ports: Dict[int, PortInfo] = {}
        self.monitoring_active = False
        self.neural_link_active = False
        self._monitor_thread = None
        self._executor = ThreadPoolExecutor(max_workers=10)

        # Performance metrics
        self.metrics = {
            'ports_allocated': 0,
            'ports_deallocated': 0,
            'conflicts_resolved': 0,
            'security_incidents': 0,
            'performance_optimizations': 0,
            'uptime_start': datetime.now()
        }

        print("🔌⚡💜 BROSKI HYPER PORT MANAGER AGENT INITIALIZING! 💜⚡🔌")
        self._initialize_database()
        self._load_configuration()
        self._discover_existing_ports()
        self._start_monitoring()
        self._register_with_command_portal()

        print("✨🔌 HYPER PORT MANAGER AGENT ONLINE AND READY! 🔌✨")

    def _initialize_database(self):
        """🗄️ Initialize port management database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Port registry table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS port_registry (
                        port INTEGER PRIMARY KEY,
                        protocol TEXT NOT NULL,
                        status TEXT NOT NULL,
                        service TEXT,
                        process_id INTEGER,
                        process_name TEXT,
                        allocated_by TEXT,
                        allocation_time TIMESTAMP,
                        last_activity TIMESTAMP,
                        security_level TEXT DEFAULT 'PRIVATE',
                        performance_score REAL DEFAULT 100.0,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # Port allocation history
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS allocation_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        port INTEGER,
                        requester_id TEXT,
                        action TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        details TEXT
                    )
                """)

                # Security events
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS security_events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        port INTEGER,
                        event_type TEXT,
                        severity TEXT,
                        description TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        resolved BOOLEAN DEFAULT FALSE
                    )
                """)

                # Performance metrics
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS performance_metrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        port INTEGER,
                        metric_type TEXT,
                        value REAL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                conn.commit()
                logger.info("🗄️ Port manager database initialized successfully")

        except sqlite3.Error as e:
            logger.error(f"❌ Database initialization error: {e}")

    def _load_configuration(self):
        """⚙️ Load port manager configuration"""
        default_config = {
            "monitoring_interval": 5,
            "max_allocation_attempts": 3,
            "security_scan_interval": 30,
            "performance_threshold": 80.0,
            "auto_cleanup_enabled": True,
            "neural_link_enabled": True,
            "reserved_ports": [22, 80, 443, 3000, 5000, 8080],
            "blacklisted_ports": [],
            "max_ports_per_service": 10
        }

        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = default_config
                self._save_configuration()

            logger.info("⚙️ Configuration loaded successfully")

        except Exception as e:
            logger.error(f"❌ Configuration loading error: {e}")
            self.config = default_config

    def _save_configuration(self):
        """💾 Save current configuration"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4, default=str)
        except Exception as e:
            logger.error(f"❌ Configuration save error: {e}")

    def _discover_existing_ports(self):
        """🔍 Discover all currently active ports"""
        try:
            # Get network connections
            connections = psutil.net_connections(kind='inet')

            for conn in connections:
                if conn.laddr and conn.status == psutil.CONN_LISTEN:
                    port = conn.laddr.port
                    protocol = "TCP" if conn.type == socket.SOCK_STREAM else "UDP"

                    # Get process information
                    process_name = "Unknown"
                    process_id = 0

                    if conn.pid:
                        try:
                            process = psutil.Process(conn.pid)
                            process_name = process.name()
                            process_id = conn.pid
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass

                    # Create port info
                    port_info = PortInfo(
                        port=port,
                        protocol=protocol,
                        status="LISTENING",
                        service=self._identify_service(port),
                        process_id=process_id,
                        process_name=process_name,
                        allocated_by="SYSTEM_DISCOVERY",
                        allocation_time=datetime.now(),
                        last_activity=datetime.now(),
                        security_level=self._determine_security_level(port),
                        performance_score=100.0,
                        description=f"Discovered {protocol} service on port {port}"
                    )

                    self.active_ports[port] = port_info
                    self._register_port_in_db(port_info)

            logger.info(f"🔍 Discovered {len(self.active_ports)} active ports")

        except Exception as e:
            logger.error(f"❌ Port discovery error: {e}")

    def _identify_service(self, port: int) -> str:
        """🏷️ Identify service running on port"""
        common_services = {
            22: "SSH", 80: "HTTP", 443: "HTTPS", 21: "FTP", 25: "SMTP",
            53: "DNS", 110: "POP3", 143: "IMAP", 993: "IMAPS", 995: "POP3S",
            3000: "Development Server", 5000: "Flask/Dev", 8080: "HTTP Alt",
            3306: "MySQL", 5432: "PostgreSQL", 6379: "Redis", 27017: "MongoDB"
        }
        return common_services.get(port, "Unknown Service")

    def _determine_security_level(self, port: int) -> str:
        """🔒 Determine security level for port"""
        if port in [22, 443, 993, 995, 5000]:  # Added port 5000 to RESTRICTED
            return "RESTRICTED"
        elif port in [80, 8080, 3000]:  # Removed 5000 from PUBLIC
            return "PUBLIC"
        else:
            return "PRIVATE"

    def _register_port_in_db(self, port_info: PortInfo):
        """📝 Register port information in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO port_registry
                    (port, protocol, status, service, process_id, process_name,
                     allocated_by, allocation_time, last_activity, security_level,
                     performance_score, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    port_info.port, port_info.protocol, port_info.status,
                    port_info.service, port_info.process_id, port_info.process_name,
                    port_info.allocated_by, port_info.allocation_time,
                    port_info.last_activity, port_info.security_level,
                    port_info.performance_score, port_info.description
                ))
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"❌ Port registration error: {e}")

    def allocate_port(self, request: PortAllocationRequest) -> Optional[PortInfo]:
        """🎯 Allocate a port based on request"""
        try:
            logger.info(f"🎯 Processing port allocation request from {request.requester_id}")

            # Validate request
            if not self._validate_allocation_request(request):
                return None

            # Find available port
            allocated_port = self._find_available_port(request)
            if not allocated_port:
                logger.warning("❌ No available ports found")
                return None

            # Create port info
            port_info = PortInfo(
                port=allocated_port,
                protocol=request.protocol,
                status="ALLOCATED",
                service=request.service_name,
                process_id=0,
                process_name=request.requester_id,
                allocated_by=request.requester_id,
                allocation_time=datetime.now(),
                last_activity=datetime.now(),
                security_level=request.security_level,
                performance_score=100.0,
                description=request.description
            )

            # Register allocation
            self.allocated_ports[allocated_port] = port_info
            self._register_port_in_db(port_info)
            self._log_allocation_event(request, allocated_port, "ALLOCATED")

            # Update metrics
            self.metrics['ports_allocated'] += 1

            logger.info(f"✅ Port {allocated_port} allocated to {request.requester_id}")
            return port_info

        except Exception as e:
            logger.error(f"❌ Port allocation error: {e}")
            return None

    def _validate_allocation_request(self, request: PortAllocationRequest) -> bool:
        """✅ Validate port allocation request"""
        # Check if requester has too many ports
        requester_ports = sum(1 for p in self.allocated_ports.values()
                            if p.allocated_by == request.requester_id)

        if requester_ports >= self.config['max_ports_per_service']:
            logger.warning(f"❌ Requester {request.requester_id} has too many allocated ports")
            return False

        # Check port range validity - FIXED BUG: allow single port allocation (start == end)
        if request.port_range[0] > request.port_range[1]:
            logger.warning("❌ Invalid port range")
            return False

        # Check if preferred port is blacklisted
        if (request.preferred_port and
            request.preferred_port in self.config['blacklisted_ports']):
            logger.warning(f"❌ Preferred port {request.preferred_port} is blacklisted")
            return False

        return True

    def _find_available_port(self, request: PortAllocationRequest) -> Optional[int]:
        """🔍 Find an available port for allocation"""
        # Try preferred port first
        if request.preferred_port:
            if self._is_port_available(request.preferred_port):
                return request.preferred_port

        # Search within specified range
        start_port, end_port = request.port_range

        for port in range(start_port, end_port + 1):
            if self._is_port_available(port):
                return port

        return None

    def _is_port_available(self, port: int) -> bool:
        """🔍 Check if port is available for allocation"""
        # Check if port is reserved
        if port in self.config['reserved_ports']:
            return False

        # Check if port is blacklisted
        if port in self.config['blacklisted_ports']:
            return False

        # Check if port is already allocated
        if port in self.allocated_ports:
            return False

        # Check if port is actively listening
        if port in self.active_ports:
            return False

        # Test if port is actually free
        return self._test_port_connectivity(port)

    def _test_port_connectivity(self, port: int) -> bool:
        """🧪 Test if port is actually free"""
        try:
            # Test TCP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', port))
                if result == 0:
                    return False  # Port is in use

            # Test if we can bind to the port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind(('localhost', port))
                return True  # Port is free

        except Exception:
            return False

    def deallocate_port(self, port: int, requester_id: str) -> bool:
        """🗑️ Deallocate a port"""
        try:
            if port not in self.allocated_ports:
                logger.warning(f"❌ Port {port} is not allocated")
                return False

            port_info = self.allocated_ports[port]

            # Check if requester has permission to deallocate
            if port_info.allocated_by != requester_id:
                logger.warning(f"❌ Permission denied: {requester_id} cannot deallocate port {port}")
                return False

            # Remove from allocated ports
            del self.allocated_ports[port]

            # Update database
            self._update_port_status(port, "DEALLOCATED")
            self._log_allocation_event(
                PortAllocationRequest(
                    requester_id=requester_id,
                    service_name=port_info.service,
                    preferred_port=port,
                    port_range=(port, port),
                    protocol=port_info.protocol,
                    security_level=port_info.security_level,
                    priority=1,
                    duration=None,
                    description=f"Deallocation of port {port}"
                ),
                port,
                "DEALLOCATED"
            )

            # Update metrics
            self.metrics['ports_deallocated'] += 1

            logger.info(f"✅ Port {port} deallocated by {requester_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Port deallocation error: {e}")
            return False

    def _update_port_status(self, port: int, status: str):
        """📝 Update port status in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE port_registry SET status = ?, last_activity = ?
                    WHERE port = ?
                """, (status, datetime.now(), port))
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"❌ Port status update error: {e}")

    def _log_allocation_event(self, request: PortAllocationRequest, port: int, action: str):
        """📋 Log allocation event"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO allocation_history
                    (port, requester_id, action, details)
                    VALUES (?, ?, ?, ?)
                """, (
                    port, request.requester_id, action,
                    json.dumps({
                        'service': request.service_name,
                        'protocol': request.protocol,
                        'security_level': request.security_level,
                        'description': request.description
                    })
                ))
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"❌ Event logging error: {e}")

    def _start_monitoring(self):
        """🔄 Start port monitoring system"""
        if self.monitoring_active:
            return

        self.monitoring_active = True
        self._monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self._monitor_thread.start()
        logger.info("🔄 Port monitoring system started")

    def _monitoring_loop(self):
        """🔄 Main monitoring loop"""
        while self.monitoring_active:
            try:
                self._scan_port_status()
                self._check_performance()
                self._security_scan()
                self._cleanup_expired_allocations()

                time.sleep(self.config['monitoring_interval'])

            except Exception as e:
                logger.error(f"❌ Monitoring loop error: {e}")
                time.sleep(5)

    def _scan_port_status(self):
        """🔍 Scan current port status"""
        try:
            current_connections = psutil.net_connections(kind='inet')
            active_ports_now = set()

            for conn in current_connections:
                if conn.laddr and conn.status == psutil.CONN_LISTEN:
                    active_ports_now.add(conn.laddr.port)

            # Check for newly opened ports
            for port in active_ports_now:
                if port not in self.active_ports:
                    self._handle_new_port(port)

            # Check for closed ports
            for port in list(self.active_ports.keys()):
                if port not in active_ports_now:
                    self._handle_closed_port(port)

        except Exception as e:
            logger.error(f"❌ Port status scan error: {e}")

    def _handle_new_port(self, port: int):
        """🆕 Handle newly detected port"""
        try:
            # Get process information
            connections = psutil.net_connections(kind='inet')
            process_name = "Unknown"
            process_id = 0

            for conn in connections:
                if (conn.laddr and conn.laddr.port == port and
                    conn.status == psutil.CONN_LISTEN):
                    if conn.pid:
                        try:
                            process = psutil.Process(conn.pid)
                            process_name = process.name()
                            process_id = conn.pid
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
                    break

            # Create port info
            port_info = PortInfo(
                port=port,
                protocol="TCP",  # Default to TCP
                status="LISTENING",
                service=self._identify_service(port),
                process_id=process_id,
                process_name=process_name,
                allocated_by="AUTO_DETECTED",
                allocation_time=datetime.now(),
                last_activity=datetime.now(),
                security_level=self._determine_security_level(port),
                performance_score=100.0,
                description=f"Auto-detected port {port}"
            )

            self.active_ports[port] = port_info
            self._register_port_in_db(port_info)

            logger.info(f"🆕 New port detected: {port} ({process_name})")

        except Exception as e:
            logger.error(f"❌ New port handling error: {e}")

    def _handle_closed_port(self, port: int):
        """📪 Handle closed port"""
        try:
            if port in self.active_ports:
                del self.active_ports[port]
                self._update_port_status(port, "CLOSED")
                logger.info(f"📪 Port closed: {port}")

        except Exception as e:
            logger.error(f"❌ Closed port handling error: {e}")

    def _check_performance(self):
        """📊 Check port performance metrics"""
        try:
            for port, port_info in self.active_ports.items():
                # Simple performance check based on connection count
                connections = [c for c in psutil.net_connections()
                             if c.laddr and c.laddr.port == port]

                connection_count = len(connections)

                # Calculate performance score (simplified)
                if connection_count > 100:
                    performance_score = max(50.0, port_info.performance_score - 10)
                elif connection_count > 50:
                    performance_score = max(70.0, port_info.performance_score - 5)
                else:
                    performance_score = min(100.0, port_info.performance_score + 1)

                port_info.performance_score = performance_score

                # Log performance metric
                self._log_performance_metric(port, "connection_count", connection_count)

                # Check if optimization is needed
                if performance_score < self.config['performance_threshold']:
                    self._optimize_port_performance(port)

        except Exception as e:
            logger.error(f"❌ Performance check error: {e}")

    def _log_performance_metric(self, port: int, metric_type: str, value: float):
        """📊 Log performance metric to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO performance_metrics (port, metric_type, value)
                    VALUES (?, ?, ?)
                """, (port, metric_type, value))
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"❌ Performance metric logging error: {e}")

    def _optimize_port_performance(self, port: int):
        """⚡ Optimize port performance"""
        try:
            logger.info(f"⚡ Optimizing performance for port {port}")

            # Implementation would include:
            # - Connection throttling
            # - Buffer optimization
            # - Process priority adjustment
            # - Resource allocation optimization

            self.metrics['performance_optimizations'] += 1

        except Exception as e:
            logger.error(f"❌ Port optimization error: {e}")

    def _security_scan(self):
        """🔒 Perform security scan on active ports"""
        try:
            for port, port_info in self.active_ports.items():
                # Check for unauthorized access
                if self._detect_suspicious_activity(port):
                    self._handle_security_incident(port, "SUSPICIOUS_ACTIVITY")

                # Check for configuration issues
                if self._check_security_configuration(port):
                    self._handle_security_incident(port, "CONFIG_ISSUE")

        except Exception as e:
            logger.error(f"❌ Security scan error: {e}")

    def _detect_suspicious_activity(self, port: int) -> bool:
        """🕵️ Detect suspicious activity on port"""
        try:
            # Get connections for this port
            connections = [c for c in psutil.net_connections()
                         if c.laddr and c.laddr.port == port]

            # Check for too many connections from same IP
            ip_counts = {}
            for conn in connections:
                if conn.raddr:
                    ip = conn.raddr.ip
                    ip_counts[ip] = ip_counts.get(ip, 0) + 1

            # Flag if any IP has more than 20 connections
            for ip, count in ip_counts.items():
                if count > 20:
                    logger.warning(f"🚨 Suspicious activity: {count} connections from {ip} to port {port}")
                    return True

            return False

        except Exception as e:
            logger.error(f"❌ Suspicious activity detection error: {e}")
            return False

    def _check_security_configuration(self, port: int) -> bool:
        """🔒 Check security configuration for port"""
        # Simplified security check
        port_info = self.active_ports.get(port)
        if not port_info:
            return False

        # Check if public port is properly secured
        # Port 5000 is now properly classified as RESTRICTED, no security issue
        if (port_info.security_level == "PUBLIC" and
            port not in [80, 443, 8080, 3000]):  # Removed 5000 from potential PUBLIC ports
            return True

        # Port 5000 security configuration is now correct
        return False

    def _handle_security_incident(self, port: int, incident_type: str):
        """🚨 Handle security incident"""
        try:
            logger.warning(f"🚨 Security incident on port {port}: {incident_type}")

            # Log security event
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO security_events
                    (port, event_type, severity, description)
                    VALUES (?, ?, ?, ?)
                """, (
                    port, incident_type, "HIGH",
                    f"Security incident detected on port {port}"
                ))
                conn.commit()

            self.metrics['security_incidents'] += 1

            # Could implement automatic response here
            # - Block suspicious IPs
            # - Adjust security settings
            # - Alert administrators

        except Exception as e:
            logger.error(f"❌ Security incident handling error: {e}")

    def _cleanup_expired_allocations(self):
        """🧹 Clean up expired port allocations"""
        if not self.config['auto_cleanup_enabled']:
            return

        try:
            current_time = datetime.now()
            expired_ports = []

            for port, port_info in self.allocated_ports.items():
                # Check if allocation has expired (simplified logic)
                allocation_age = current_time - port_info.allocation_time

                # Remove allocations older than 24 hours that haven't been used
                if (allocation_age > timedelta(hours=24) and
                    port_info.status == "ALLOCATED" and
                    port not in self.active_ports):
                    expired_ports.append(port)

            for port in expired_ports:
                logger.info(f"🧹 Cleaning up expired allocation for port {port}")
                self.deallocate_port(port, "AUTO_CLEANUP")

        except Exception as e:
            logger.error(f"❌ Cleanup error: {e}")

    def _register_with_command_portal(self):
        """📡 Register agent with command portal"""
        try:
            # This would integrate with the existing agent army system
            agent_data = {
                "agent_id": self.agent_id,
                "name": self.agent_name,
                "type": "PORT_MANAGER",
                "status": "ACTIVE",
                "powers": [
                    "PORT_ALLOCATION",
                    "PORT_MONITORING",
                    "SECURITY_SCANNING",
                    "PERFORMANCE_OPTIMIZATION",
                    "CONFLICT_RESOLUTION"
                ],
                "last_heartbeat": datetime.now().isoformat(),
                "missions_completed": 0,
                "performance_score": 100.0,
                "neural_link": True
            }

            # Save agent registration data
            agent_file = f"{self.base_path}/agent_registrations/{self.agent_id}.json"
            os.makedirs(os.path.dirname(agent_file), exist_ok=True)

            with open(agent_file, 'w') as f:
                json.dump(agent_data, f, indent=4, default=str)

            logger.info("📡 Agent registered with command portal")

        except Exception as e:
            logger.error(f"❌ Command portal registration error: {e}")

    def get_port_status(self, port: int) -> Optional[Dict]:
        """📊 Get detailed port status"""
        try:
            if port in self.active_ports:
                return asdict(self.active_ports[port])
            elif port in self.allocated_ports:
                return asdict(self.allocated_ports[port])
            else:
                return None

        except Exception as e:
            logger.error(f"❌ Port status retrieval error: {e}")
            return None

    def get_agent_metrics(self) -> Dict:
        """📊 Get agent performance metrics"""
        try:
            uptime = datetime.now() - self.metrics['uptime_start']

            return {
                **self.metrics,
                'uptime_seconds': uptime.total_seconds(),
                'active_ports_count': len(self.active_ports),
                'allocated_ports_count': len(self.allocated_ports),
                'monitoring_status': 'ACTIVE' if self.monitoring_active else 'INACTIVE'
            }

        except Exception as e:
            logger.error(f"❌ Metrics retrieval error: {e}")
            return {}

    def shutdown(self):
        """🔴 Shutdown the agent gracefully"""
        try:
            logger.info("🔴 Shutting down Hyper Port Manager Agent...")

            self.monitoring_active = False

            if self._monitor_thread and self._monitor_thread.is_alive():
                self._monitor_thread.join(timeout=5)

            self._executor.shutdown(wait=True)

            logger.info("✅ Hyper Port Manager Agent shutdown complete")

        except Exception as e:
            logger.error(f"❌ Shutdown error: {e}")

# Command-line interface for testing
def main():
    """🎯 Main function for direct execution"""
    import argparse

    parser = argparse.ArgumentParser(description="🔌 Broski Hyper Port Manager Agent")
    parser.add_argument("--allocate", type=int, help="Allocate a specific port")
    parser.add_argument("--deallocate", type=int, help="Deallocate a specific port")
    parser.add_argument("--status", type=int, help="Get port status")
    parser.add_argument("--metrics", action="store_true", help="Show agent metrics")
    parser.add_argument("--requester", default="CLI_USER", help="Requester ID")

    args = parser.parse_args()

    # Initialize agent
    agent = BroskiHyperPortManagerAgent()

    try:
        if args.allocate:
            request = PortAllocationRequest(
                requester_id=args.requester,
                service_name="CLI_TEST",
                preferred_port=args.allocate,
                port_range=(args.allocate, args.allocate),
                protocol="TCP",
                security_level="PRIVATE",
                priority=1,
                duration=None,
                description=f"CLI allocation request for port {args.allocate}"
            )

            result = agent.allocate_port(request)
            if result:
                print(f"✅ Port {result.port} allocated successfully")
            else:
                print("❌ Port allocation failed")

        elif args.deallocate:
            result = agent.deallocate_port(args.deallocate, args.requester)
            if result:
                print(f"✅ Port {args.deallocate} deallocated successfully")
            else:
                print("❌ Port deallocation failed")

        elif args.status is not None:
            status = agent.get_port_status(args.status)
            if status:
                print(f"📊 Port {args.status} status:")
                for key, value in status.items():
                    print(f"  {key}: {value}")
            else:
                print(f"❌ Port {args.status} not found")

        elif args.metrics:
            metrics = agent.get_agent_metrics()
            print("📊 Agent Metrics:")
            for key, value in metrics.items():
                print(f"  {key}: {value}")

        else:
            print("🔌⚡ Broski Hyper Port Manager Agent is running!")
            print("Use --help for available commands")

            # Keep running for monitoring
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🔴 Shutting down...")

    finally:
        agent.shutdown()

if __name__ == "__main__":
    main()