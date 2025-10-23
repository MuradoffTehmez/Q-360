"""
Django management command for monitoring and analyzing logs.
Usage:
    python manage.py monitor_logs
    python manage.py monitor_logs --summary
    python manage.py monitor_logs --cleanup --days 30
    python manage.py monitor_logs --check-errors --threshold 50
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from config.log_utils import LogMonitor
import json


class Command(BaseCommand):
    help = 'Monitor and analyze Q360 system logs'

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            '--summary',
            action='store_true',
            help='Display summary of all log files',
        )
        parser.add_argument(
            '--check-errors',
            action='store_true',
            help='Check if error count exceeds threshold',
        )
        parser.add_argument(
            '--threshold',
            type=int,
            default=100,
            help='Error count threshold (default: 100)',
        )
        parser.add_argument(
            '--hours',
            type=int,
            default=1,
            help='Time window in hours for error check (default: 1)',
        )
        parser.add_argument(
            '--cleanup',
            action='store_true',
            help='Delete old log backup files',
        )
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Delete log files older than N days (default: 30)',
        )
        parser.add_argument(
            '--json',
            action='store_true',
            help='Output results in JSON format',
        )
        parser.add_argument(
            '--threat-analysis',
            action='store_true',
            help='Perform threat level analysis on audit logs',
        )
        parser.add_argument(
            '--threat-threshold',
            type=int,
            default=60,
            help='Threat score threshold for alerts (default: 60)',
        )

    def handle(self, *args, **options):
        """Handle command execution."""
        monitor = LogMonitor()

        # Threat analysis
        if options['threat_analysis']:
            self.stdout.write(self.style.SUCCESS('\n🔐 Threat Level Analysis\n'))
            result = self._perform_threat_analysis(
                threshold=options['threat_threshold'],
                hours=options.get('hours', 24)
            )

            if options['json']:
                self.stdout.write(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                self._display_threat_analysis(result)
            return

        # Get summary of all logs
        if options['summary']:
            self.stdout.write(self.style.SUCCESS('\n📊 Log Files Summary\n'))
            summary = monitor.get_all_logs_summary()

            if options['json']:
                self.stdout.write(json.dumps(summary, indent=2, ensure_ascii=False))
            else:
                self._display_summary(summary)
            return

        # Check error threshold
        if options['check_errors']:
            self.stdout.write(self.style.SUCCESS(f'\n🔍 Checking error threshold...\n'))
            result = monitor.check_error_threshold(
                threshold=options['threshold'],
                hours=options['hours']
            )

            if options['json']:
                self.stdout.write(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                self._display_error_check(result)
            return

        # Cleanup old logs
        if options['cleanup']:
            self.stdout.write(self.style.WARNING(f'\n🗑️  Cleaning up logs older than {options["days"]} days...\n'))
            result = monitor.cleanup_old_logs(days=options['days'])

            if result['deleted_count'] > 0:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Deleted {result["deleted_count"]} old log files')
                )
                for file in result['deleted_files']:
                    self.stdout.write(f'   - {file}')
            else:
                self.stdout.write(self.style.WARNING('No old log files to delete'))
            return

        # Default: show basic summary
        self.stdout.write(self.style.SUCCESS('\n📊 Q360 Log Monitor\n'))
        summary = monitor.get_all_logs_summary()
        self._display_quick_summary(summary)

    def _display_summary(self, summary):
        """Display detailed log summary."""
        for log_type, data in summary['logs'].items():
            self.stdout.write(self.style.HTTP_INFO(f'\n📄 {log_type.upper()} Log:'))

            if data.get('exists') is False:
                self.stdout.write('   ⚠️  File does not exist')
                continue

            self.stdout.write(f"   Size: {data['file_size_mb']} MB")
            self.stdout.write(f"   Last Modified: {data['last_modified']}")

            if 'stats' in data:
                stats = data['stats']
                self.stdout.write(f"   Total Lines: {stats['total_lines']:,}")

                # Display counts by level
                levels = []
                if stats['debug_count'] > 0:
                    levels.append(f"DEBUG: {stats['debug_count']:,}")
                if stats['info_count'] > 0:
                    levels.append(f"INFO: {stats['info_count']:,}")
                if stats['warning_count'] > 0:
                    levels.append(self.style.WARNING(f"WARNING: {stats['warning_count']:,}"))
                if stats['error_count'] > 0:
                    levels.append(self.style.ERROR(f"ERROR: {stats['error_count']:,}"))
                if stats['critical_count'] > 0:
                    levels.append(self.style.ERROR(f"CRITICAL: {stats['critical_count']:,}"))

                if levels:
                    self.stdout.write(f"   Log Levels: {' | '.join(levels)}")

                # Display common errors
                if stats.get('common_errors'):
                    self.stdout.write(self.style.WARNING('   Top Errors:'))
                    for i, (error, count) in enumerate(list(stats['common_errors'].items())[:3], 1):
                        self.stdout.write(f"      {i}. [{count}x] {error[:80]}...")

    def _display_quick_summary(self, summary):
        """Display quick summary of logs."""
        total_errors = 0
        total_warnings = 0
        total_size_mb = 0

        for log_type, data in summary['logs'].items():
            if data.get('exists') is not False:
                total_size_mb += data.get('file_size_mb', 0)
                if 'stats' in data:
                    stats = data['stats']
                    total_errors += stats.get('error_count', 0) + stats.get('critical_count', 0)
                    total_warnings += stats.get('warning_count', 0)

        self.stdout.write(f'📁 Total Log Size: {total_size_mb:.2f} MB')
        self.stdout.write(f'⚠️  Total Warnings: {total_warnings:,}')

        if total_errors > 0:
            self.stdout.write(self.style.ERROR(f'❌ Total Errors: {total_errors:,}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'✅ Total Errors: {total_errors}'))

        self.stdout.write('\n💡 Use --summary for detailed information')
        self.stdout.write('💡 Use --check-errors to check error threshold')
        self.stdout.write('💡 Use --cleanup --days 30 to delete old logs')

    def _display_error_check(self, result):
        """Display error threshold check results."""
        self.stdout.write(
            f"Errors in last {result['hours']} hour(s): {result['error_count']}"
        )
        self.stdout.write(f"Threshold: {result['threshold']}")

        if result['threshold_exceeded']:
            self.stdout.write(
                self.style.ERROR(f'\n❌ ALERT: Error threshold exceeded!')
            )
            if 'latest_errors' in result:
                self.stdout.write(self.style.WARNING('\nLatest errors:'))
                for i, error in enumerate(result['latest_errors'], 1):
                    self.stdout.write(f'{i}. {error[:150]}...')
        else:
            self.stdout.write(
                self.style.SUCCESS(f'\n✅ Error count is within acceptable limits')
            )

    def _perform_threat_analysis(self, threshold=60, hours=24):
        """Perform threat level analysis on audit logs."""
        from apps.audit.models import AuditLog
        from django.utils import timezone
        from datetime import timedelta
        from collections import defaultdict

        start_time = timezone.now() - timedelta(hours=hours)

        # Yüksək təhdid səviyyəsi olan qeydlər
        high_threats = AuditLog.objects.filter(
            created_at__gte=start_time,
            threat_score__gte=threshold
        ).select_related('user').order_by('-threat_score')

        # İstifadəçi bazasında təhdid statistikası
        user_threat_stats = defaultdict(lambda: {'count': 0, 'max_score': 0, 'actions': []})

        for log in high_threats:
            if log.user:
                user_key = log.user.username
                user_threat_stats[user_key]['count'] += 1
                user_threat_stats[user_key]['max_score'] = max(
                    user_threat_stats[user_key]['max_score'],
                    log.threat_score
                )
                user_threat_stats[user_key]['actions'].append({
                    'action': log.action,
                    'threat_level': log.threat_level,
                    'threat_score': log.threat_score,
                    'timestamp': log.created_at.isoformat(),
                })

        # IP bazasında təhdid statistikası
        ip_threat_stats = defaultdict(lambda: {'count': 0, 'max_score': 0})

        for log in high_threats:
            if log.ip_address:
                ip_threat_stats[log.ip_address]['count'] += 1
                ip_threat_stats[log.ip_address]['max_score'] = max(
                    ip_threat_stats[log.ip_address]['max_score'],
                    log.threat_score
                )

        # Ən yüksək təhdidli istifadəçilər
        top_threat_users = sorted(
            user_threat_stats.items(),
            key=lambda x: x[1]['max_score'],
            reverse=True
        )[:10]

        # Ən yüksək təhdidli IP-lər
        top_threat_ips = sorted(
            ip_threat_stats.items(),
            key=lambda x: x[1]['max_score'],
            reverse=True
        )[:10]

        return {
            'analysis_period_hours': hours,
            'threat_threshold': threshold,
            'total_high_threats': high_threats.count(),
            'top_threat_users': [
                {
                    'username': username,
                    'threat_count': data['count'],
                    'max_threat_score': data['max_score'],
                    'recent_actions': data['actions'][:5]
                }
                for username, data in top_threat_users
            ],
            'top_threat_ips': [
                {
                    'ip_address': ip,
                    'threat_count': data['count'],
                    'max_threat_score': data['max_score']
                }
                for ip, data in top_threat_ips
            ],
            'severity_distribution': {
                'critical': high_threats.filter(threat_level='critical').count(),
                'high': high_threats.filter(threat_level='high').count(),
                'medium': high_threats.filter(threat_level='medium').count(),
            }
        }

    def _display_threat_analysis(self, result):
        """Display threat analysis results."""
        self.stdout.write(f"Analiz müddəti: {result['analysis_period_hours']} saat")
        self.stdout.write(f"Təhdid eşiyi: {result['threat_threshold']}")
        self.stdout.write(f"\nCəmi yüksək təhdid: {result['total_high_threats']}")

        # Severity distribution
        self.stdout.write(self.style.HTTP_INFO('\n📊 Təhdid Səviyyəsi Paylanması:'))
        severity_dist = result['severity_distribution']
        if severity_dist['critical'] > 0:
            self.stdout.write(self.style.ERROR(f"   KRİTİK: {severity_dist['critical']}"))
        if severity_dist['high'] > 0:
            self.stdout.write(self.style.WARNING(f"   YÜKSƏK: {severity_dist['high']}"))
        if severity_dist['medium'] > 0:
            self.stdout.write(f"   ORTA: {severity_dist['medium']}")

        # Top threat users
        if result['top_threat_users']:
            self.stdout.write(self.style.WARNING('\n⚠️  Ən Yüksək Təhdidli İstifadəçilər:'))
            for i, user_data in enumerate(result['top_threat_users'][:5], 1):
                self.stdout.write(
                    f"   {i}. {user_data['username']} - "
                    f"Təhdid Sayı: {user_data['threat_count']}, "
                    f"Max Skor: {user_data['max_threat_score']}"
                )

        # Top threat IPs
        if result['top_threat_ips']:
            self.stdout.write(self.style.WARNING('\n🌐 Ən Yüksək Təhdidli IP Ünvanları:'))
            for i, ip_data in enumerate(result['top_threat_ips'][:5], 1):
                self.stdout.write(
                    f"   {i}. {ip_data['ip_address']} - "
                    f"Təhdid Sayı: {ip_data['threat_count']}, "
                    f"Max Skor: {ip_data['max_threat_score']}"
                )
