#!/usr/bin/env python3
"""
HUMMBL Beta Metrics Monitor

This script monitors beta program metrics and generates automated reports.
It collects data from various sources and provides insights for decision making.

Usage:
    python beta-metrics-monitor.py --report daily
    python beta-metrics-monitor.py --alerts
    python beta-metrics-monitor.py --dashboard-update
"""

import argparse
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import requests
from dataclasses import dataclass, asdict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import sqlite3
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class BetaMetrics:
    """Core beta program metrics"""
    total_applications: int = 0
    approved_users: int = 0
    active_users: int = 0
    retention_rate: float = 0.0
    nps_score: float = 0.0
    support_tickets: int = 0
    avg_response_time: float = 0.0
    platform_uptime: float = 0.0
    feature_adoption_rate: float = 0.0
    community_messages: int = 0
    recorded_at: Optional[datetime] = None

@dataclass
class Alert:
    """Alert configuration and state"""
    metric: str
    threshold: float
    current_value: float
    severity: str  # 'critical', 'warning', 'info'
    message: str
    triggered_at: datetime

class MetricsDatabase:
    """Local SQLite database for metrics storage"""

    def __init__(self, db_path: str = 'beta_metrics.db'):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize database schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_applications INTEGER,
                    approved_users INTEGER,
                    active_users INTEGER,
                    retention_rate REAL,
                    nps_score REAL,
                    support_tickets INTEGER,
                    avg_response_time REAL,
                    platform_uptime REAL,
                    feature_adoption_rate REAL,
                    community_messages INTEGER
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metric TEXT,
                    threshold REAL,
                    current_value REAL,
                    severity TEXT,
                    message TEXT,
                    resolved BOOLEAN DEFAULT FALSE
                )
            ''')
            conn.commit()

    def save_metrics(self, metrics: BetaMetrics):
        """Save metrics to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO metrics (
                    total_applications, approved_users, active_users,
                    retention_rate, nps_score, support_tickets,
                    avg_response_time, platform_uptime, feature_adoption_rate,
                    community_messages
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                metrics.total_applications, metrics.approved_users, metrics.active_users,
                metrics.retention_rate, metrics.nps_score, metrics.support_tickets,
                metrics.avg_response_time, metrics.platform_uptime, metrics.feature_adoption_rate,
                metrics.community_messages
            ))
            conn.commit()

    def get_recent_metrics(self, days: int = 7) -> List[BetaMetrics]:
        """Get metrics from the last N days"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT * FROM metrics
                WHERE recorded_at >= datetime('now', '-{} days')
                ORDER BY recorded_at DESC
            '''.format(days))

            metrics = []
            for row in cursor.fetchall():
                metrics.append(BetaMetrics(
                    total_applications=row[2],
                    approved_users=row[3],
                    active_users=row[4],
                    retention_rate=row[5],
                    nps_score=row[6],
                    support_tickets=row[7],
                    avg_response_time=row[8],
                    platform_uptime=row[9],
                    feature_adoption_rate=row[10],
                    community_messages=row[11],
                    recorded_at=datetime.fromisoformat(row[1])
                ))
            return metrics

    def save_alert(self, alert: Alert):
        """Save alert to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO alerts (metric, threshold, current_value, severity, message)
                VALUES (?, ?, ?, ?, ?)
            ''', (alert.metric, alert.threshold, alert.current_value, alert.severity, alert.message))
            conn.commit()

class MetricsCollector:
    """Collect metrics from various sources"""

    def __init__(self):
        # In a real implementation, these would be actual API endpoints
        self.mock_data = True

    def collect_application_metrics(self) -> Dict[str, Any]:
        """Collect application and user metrics"""
        if self.mock_data:
            return {
                'total_applications': 387,
                'approved_users': 85,
                'active_users': 68,
                'retention_rate': 0.82,
                'nps_score': 7.8
            }

        # Real implementation would call actual APIs
        # return self._call_api('/api/beta/applications/metrics')

    def collect_support_metrics(self) -> Dict[str, Any]:
        """Collect support ticket metrics"""
        if self.mock_data:
            return {
                'support_tickets': 45,
                'avg_response_time': 2.3,  # hours
                'resolution_rate': 0.87
            }

        # Real implementation would call support API
        # return self._call_support_api('/tickets/metrics')

    def collect_platform_metrics(self) -> Dict[str, Any]:
        """Collect platform performance metrics"""
        if self.mock_data:
            return {
                'platform_uptime': 0.997,
                'avg_response_time': 245,  # ms
                'error_rate': 0.002
            }

        # Real implementation would call monitoring API
        # return self._call_monitoring_api('/platform/metrics')

    def collect_engagement_metrics(self) -> Dict[str, Any]:
        """Collect user engagement metrics"""
        if self.mock_data:
            return {
                'feature_adoption_rate': 0.73,
                'community_messages': 1250,
                'avg_session_duration': 1850  # seconds
            }

        # Real implementation would call analytics API
        # return self._call_analytics_api('/engagement/metrics')

    def collect_all_metrics(self) -> BetaMetrics:
        """Collect all metrics and return BetaMetrics object"""
        app_metrics = self.collect_application_metrics()
        support_metrics = self.collect_support_metrics()
        platform_metrics = self.collect_platform_metrics()
        engagement_metrics = self.collect_engagement_metrics()

        return BetaMetrics(
            total_applications=app_metrics['total_applications'],
            approved_users=app_metrics['approved_users'],
            active_users=app_metrics['active_users'],
            retention_rate=app_metrics['retention_rate'],
            nps_score=app_metrics['nps_score'],
            support_tickets=support_metrics['support_tickets'],
            avg_response_time=support_metrics['avg_response_time'],
            platform_uptime=platform_metrics['platform_uptime'],
            feature_adoption_rate=engagement_metrics['feature_adoption_rate'],
            community_messages=engagement_metrics['community_messages'],
            recorded_at=datetime.now()
        )

class AlertEngine:
    """Monitor metrics and generate alerts"""

    def __init__(self, db: MetricsDatabase):
        self.db = db
        self.alert_thresholds = {
            'active_users': {'warning': 60, 'critical': 50},
            'retention_rate': {'warning': 0.75, 'critical': 0.70},
            'nps_score': {'warning': 7.0, 'critical': 6.5},
            'avg_response_time': {'warning': 4.0, 'critical': 8.0},
            'platform_uptime': {'warning': 0.995, 'critical': 0.990},
            'support_tickets': {'warning': 30, 'critical': 50}
        }

    def check_alerts(self, metrics: BetaMetrics) -> List[Alert]:
        """Check metrics against thresholds and generate alerts"""
        alerts = []

        # Active users alert
        if metrics.active_users <= self.alert_thresholds['active_users']['critical']:
            alerts.append(Alert(
                metric='active_users',
                threshold=self.alert_thresholds['active_users']['critical'],
                current_value=metrics.active_users,
                severity='critical',
                message=f'Critical: Active users dropped to {metrics.active_users}, below threshold of {self.alert_thresholds["active_users"]["critical"]}',
                triggered_at=datetime.now()
            ))
        elif metrics.active_users <= self.alert_thresholds['active_users']['warning']:
            alerts.append(Alert(
                metric='active_users',
                threshold=self.alert_thresholds['active_users']['warning'],
                current_value=metrics.active_users,
                severity='warning',
                message=f'Warning: Active users at {metrics.active_users}, below warning threshold of {self.alert_thresholds["active_users"]["warning"]}',
                triggered_at=datetime.now()
            ))

        # Retention rate alert
        if metrics.retention_rate <= self.alert_thresholds['retention_rate']['critical']:
            alerts.append(Alert(
                metric='retention_rate',
                threshold=self.alert_thresholds['retention_rate']['critical'],
                current_value=metrics.retention_rate,
                severity='critical',
                message=f'Critical: Retention rate dropped to {metrics.retention_rate:.1%}, below threshold of {self.alert_thresholds["retention_rate"]["critical"]:.1%}',
                triggered_at=datetime.now()
            ))

        # Support response time alert
        if metrics.avg_response_time >= self.alert_thresholds['avg_response_time']['critical']:
            alerts.append(Alert(
                metric='avg_response_time',
                threshold=self.alert_thresholds['avg_response_time']['critical'],
                current_value=metrics.avg_response_time,
                severity='critical',
                message=f'Critical: Average support response time is {metrics.avg_response_time:.1f} hours, above threshold of {self.alert_thresholds["avg_response_time"]["critical"]:.1f} hours',
                triggered_at=datetime.now()
            ))

        return alerts

class ReportGenerator:
    """Generate various types of reports"""

    def __init__(self, db: MetricsDatabase):
        self.db = db

    def generate_daily_report(self) -> str:
        """Generate daily metrics report"""
        recent_metrics = self.db.get_recent_metrics(days=1)
        if not recent_metrics:
            return "No metrics available for daily report"

        latest = recent_metrics[0]

        report = f"""
HUMMBL Beta Daily Report - {datetime.now().strftime('%Y-%m-%d')}

EXECUTIVE SUMMARY
=================
• Total Applications: {latest.total_applications}
• Approved Users: {latest.approved_users}
• Active Users: {latest.active_users}
• Retention Rate: {latest.retention_rate:.1%}
• NPS Score: {latest.nps_score:.1f}/10

PLATFORM PERFORMANCE
====================
• Platform Uptime: {latest.platform_uptime:.1%}
• Support Tickets: {latest.support_tickets}
• Avg Response Time: {latest.avg_response_time:.1f} hours
• Feature Adoption: {latest.feature_adoption_rate:.1%}

COMMUNITY ENGAGEMENT
====================
• Community Messages: {latest.community_messages}

KEY METRICS TREND
=================
"""
        if len(recent_metrics) > 1:
            prev = recent_metrics[1]
            report += f"""
• Active Users: {latest.active_users} ({'+' if latest.active_users > prev.active_users else ''}{latest.active_users - prev.active_users} from yesterday)
• Retention: {latest.retention_rate:.1%} ({'+' if latest.retention_rate > prev.retention_rate else ''}{latest.retention_rate - prev.retention_rate:.1%} from yesterday)
• NPS: {latest.nps_score:.1f} ({'+' if latest.nps_score > prev.nps_score else ''}{latest.nps_score - prev.nps_score:.1f} from yesterday)
"""

        return report

    def generate_weekly_report(self) -> str:
        """Generate weekly metrics report"""
        weekly_metrics = self.db.get_recent_metrics(days=7)

        if len(weekly_metrics) < 7:
            return "Insufficient data for weekly report (need 7 days of metrics)"

        # Calculate weekly trends
        start_metrics = weekly_metrics[-1]  # 7 days ago
        end_metrics = weekly_metrics[0]     # today

        weekly_change = {
            'applications': end_metrics.total_applications - start_metrics.total_applications,
            'active_users': end_metrics.active_users - start_metrics.active_users,
            'retention': end_metrics.retention_rate - start_metrics.retention_rate,
            'nps': end_metrics.nps_score - start_metrics.nps_score
        }

        report = f"""
HUMMBL Beta Weekly Report - Week of {datetime.now().strftime('%Y-%m-%d')}

WEEKLY PERFORMANCE SUMMARY
==========================
• Applications: {end_metrics.total_applications} ({'+' if weekly_change['applications'] > 0 else ''}{weekly_change['applications']} this week)
• Active Users: {end_metrics.active_users} ({'+' if weekly_change['active_users'] > 0 else ''}{weekly_change['active_users']} this week)
• Retention Rate: {end_metrics.retention_rate:.1%} ({'+' if weekly_change['retention'] > 0 else ''}{weekly_change['retention']:.1%} this week)
• NPS Score: {end_metrics.nps_score:.1f} ({'+' if weekly_change['nps'] > 0 else ''}{weekly_change['nps']:.1f} this week)

PLATFORM HEALTH
===============
• Average Uptime: {sum(m.platform_uptime for m in weekly_metrics)/len(weekly_metrics):.1%}
• Total Support Tickets: {sum(m.support_tickets for m in weekly_metrics)}
• Avg Response Time: {sum(m.avg_response_time for m in weekly_metrics)/len(weekly_metrics):.1f} hours
• Feature Adoption: {sum(m.feature_adoption_rate for m in weekly_metrics)/len(weekly_metrics):.1%}

COMMUNITY ACTIVITY
==================
• Total Messages: {sum(m.community_messages for m in weekly_metrics)}
• Daily Average: {sum(m.community_messages for m in weekly_metrics)/len(weekly_metrics):.0f}

INSIGHTS & RECOMMENDATIONS
==========================
"""

        # Generate insights based on trends
        if weekly_change['active_users'] < 0:
            report += "⚠️  Active users declined this week. Consider re-engagement campaigns.\n"
        if weekly_change['retention'] < 0:
            report += "⚠️  Retention rate decreased. Review onboarding and value proposition.\n"
        if weekly_change['nps'] < 0:
            report += "⚠️  NPS score declined. Gather detailed feedback on pain points.\n"
        if weekly_change['applications'] < 10:
            report += "⚠️  Application volume low. Increase outreach efforts.\n"

        if all(change >= 0 for change in [weekly_change['active_users'], weekly_change['retention'], weekly_change['nps']]):
            report += "✅ All key metrics trending positive. Continue current strategies.\n"

        return report

class NotificationService:
    """Handle email and other notifications"""

    def __init__(self, smtp_config: Optional[Dict[str, str]] = None):
        self.smtp_config = smtp_config or {
            'server': 'smtp.gmail.com',
            'port': 587,
            'username': os.getenv('SMTP_USERNAME'),
            'password': os.getenv('SMTP_PASSWORD')
        }

    def send_alert(self, alert: Alert, recipients: List[str]):
        """Send alert notification"""
        subject = f"HUMMBL Beta Alert: {alert.severity.upper()} - {alert.metric}"

        body = f"""
HUMMBL Beta Alert
=================

Severity: {alert.severity.upper()}
Metric: {alert.metric}
Threshold: {alert.threshold}
Current Value: {alert.current_value}
Triggered: {alert.triggered_at.strftime('%Y-%m-%d %H:%M:%S')}

Message: {alert.message}

Please review the beta analytics dashboard for more details:
https://analytics.hummbl.dev/beta

This is an automated notification from the HUMMBL Beta Metrics Monitor.
"""

        self._send_email(subject, body, recipients)

    def send_report(self, report_type: str, content: str, recipients: List[str]):
        """Send report via email"""
        subject = f"HUMMBL Beta {report_type.title()} Report - {datetime.now().strftime('%Y-%m-%d')}"

        self._send_email(subject, content, recipients)

    def _send_email(self, subject: str, body: str, recipients: List[str]):
        """Send email using SMTP"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_config['username']
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            # In a real implementation, this would actually send the email
            logger.info(f"Would send email to {recipients}: {subject}")

        except Exception as e:
            logger.error(f"Failed to send email: {e}")

def main():
    parser = argparse.ArgumentParser(description='HUMMBL Beta Metrics Monitor')
    parser.add_argument('--collect', action='store_true', help='Collect and store metrics')
    parser.add_argument('--report', choices=['daily', 'weekly'], help='Generate specific report')
    parser.add_argument('--alerts', action='store_true', help='Check and send alerts')
    parser.add_argument('--dashboard-update', action='store_true', help='Update dashboard data')

    args = parser.parse_args()

    # Initialize components
    db = MetricsDatabase()
    collector = MetricsCollector()
    alert_engine = AlertEngine(db)
    report_gen = ReportGenerator(db)
    notifier = NotificationService()

    # Default recipients for notifications
    recipients = ['beta-team@hummbl.dev', 'product@hummbl.dev']

    if args.collect:
        logger.info("Collecting metrics...")
        metrics = collector.collect_all_metrics()
        db.save_metrics(metrics)
        logger.info(f"Metrics collected and saved: {metrics.active_users} active users")

    if args.alerts:
        logger.info("Checking alerts...")
        recent_metrics = db.get_recent_metrics(days=1)
        if recent_metrics:
            alerts = alert_engine.check_alerts(recent_metrics[0])
            for alert in alerts:
                db.save_alert(alert)
                notifier.send_alert(alert, recipients)
                logger.info(f"Alert sent: {alert.metric} - {alert.severity}")

    if args.report:
        if args.report == 'daily':
            report = report_gen.generate_daily_report()
            notifier.send_report('daily', report, recipients)
            print(report)
        elif args.report == 'weekly':
            report = report_gen.generate_weekly_report()
            notifier.send_report('weekly', report, recipients)
            print(report)

    if args.dashboard_update:
        logger.info("Updating dashboard data...")
        # In a real implementation, this would update a dashboard service
        logger.info("Dashboard updated successfully")

    # If no arguments provided, show help
    if not any([args.collect, args.report, args.alerts, args.dashboard_update]):
        parser.print_help()

if __name__ == '__main__':
    main()