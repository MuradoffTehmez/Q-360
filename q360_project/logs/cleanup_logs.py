#!/usr/bin/env python
"""
Q360 - Log Təmizləmə və Arxivləşdirmə Scripti
Köhnə log fayllarını arxivləyir və sistemdən təmizləyir.

İstifadə:
    python logs/cleanup_logs.py --dry-run          # Test rejimi
    python logs/cleanup_logs.py --days 30          # 30 gündən köhnə logları arxivlə
    python logs/cleanup_logs.py --days 30 --zip    # Arxivi sıxışdır
"""
import os
import sys
import shutil
import gzip
import argparse
from datetime import datetime, timedelta
from pathlib import Path


class LogCleaner:
    """Log fayllarının təmizlənməsi və arxivləşdirilməsi."""

    def __init__(self, logs_dir: Path, archive_dir: Path = None):
        """
        Args:
            logs_dir: Log fayllarının yerləşdiyi qovluq
            archive_dir: Arxiv qovluğu (default: logs_dir/archive)
        """
        self.logs_dir = Path(logs_dir)
        self.archive_dir = archive_dir or (self.logs_dir / 'archive')
        self.archive_dir.mkdir(parents=True, exist_ok=True)

    def get_old_log_files(self, days: int = 30) -> list:
        """
        Köhnə log fayllarını tap.

        Args:
            days: Neçə gündən köhnə fayllar

        Returns:
            Köhnə log fayllarının siyahısı
        """
        cutoff_time = datetime.now().timestamp() - (days * 86400)
        old_files = []

        # Backup faylları (*.log.1, *.log.2, etc.)
        for pattern in ['*.log.*', '*.log-*']:
            for log_file in self.logs_dir.glob(pattern):
                if log_file.is_file():
                    mtime = log_file.stat().st_mtime
                    if mtime < cutoff_time:
                        old_files.append({
                            'path': log_file,
                            'size': log_file.stat().st_size,
                            'mtime': datetime.fromtimestamp(mtime),
                            'age_days': (datetime.now().timestamp() - mtime) / 86400
                        })

        return sorted(old_files, key=lambda x: x['mtime'])

    def archive_file(self, file_path: Path, compress: bool = False) -> Path:
        """
        Faylı arxivə köçür.

        Args:
            file_path: Arxivləmək üçün fayl
            compress: Sıxışdırmaq lazımdırmı (gzip)

        Returns:
            Arxivlənmiş faylın yolu
        """
        # Tarixə görə qovluq yarat
        date_folder = self.archive_dir / file_path.stat().st_mtime.__class__(
            file_path.stat().st_mtime
        ).strftime('%Y-%m')
        date_folder.mkdir(parents=True, exist_ok=True)

        # Timestamp əlavə et
        timestamp = datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y%m%d_%H%M%S')
        archive_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"

        if compress:
            archive_path = date_folder / f"{archive_name}.gz"
            with open(file_path, 'rb') as f_in:
                with gzip.open(archive_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        else:
            archive_path = date_folder / archive_name
            shutil.copy2(file_path, archive_path)

        return archive_path

    def clean_logs(self, days: int = 30, compress: bool = False, dry_run: bool = False):
        """
        Köhnə logları təmizlə və arxivlə.

        Args:
            days: Neçə gündən köhnə fayllar
            compress: Arxivi sıxışdırmaq lazımdırmı
            dry_run: Test rejimi (faylları silmədən)

        Returns:
            Təmizləmə statistikası
        """
        old_files = self.get_old_log_files(days)

        stats = {
            'total_files': len(old_files),
            'total_size': sum(f['size'] for f in old_files),
            'archived': [],
            'deleted': [],
            'errors': []
        }

        for file_info in old_files:
            file_path = file_info['path']

            try:
                if dry_run:
                    print(f"[DRY-RUN] Arxivləmə: {file_path.name} ({file_info['age_days']:.1f} gün köhnə)")
                else:
                    # Arxivlə
                    archive_path = self.archive_file(file_path, compress=compress)
                    stats['archived'].append({
                        'original': str(file_path),
                        'archive': str(archive_path),
                        'size': file_info['size']
                    })

                    # Orijinalı sil
                    file_path.unlink()
                    stats['deleted'].append(str(file_path))

                    print(f"✅ Arxivləndi: {file_path.name} → {archive_path}")

            except Exception as e:
                error_msg = f"❌ Xəta {file_path.name}: {str(e)}"
                stats['errors'].append(error_msg)
                print(error_msg)

        return stats

    def get_archive_size(self) -> dict:
        """Arxiv qovluğunun ölçüsünü hesabla."""
        total_size = 0
        file_count = 0

        for file_path in self.archive_dir.rglob('*'):
            if file_path.is_file():
                total_size += file_path.stat().st_size
                file_count += 1

        return {
            'total_size': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'file_count': file_count
        }

    def clean_empty_archives(self):
        """Boş arxiv qovluqlarını təmizlə."""
        removed = []
        for folder in self.archive_dir.rglob('*'):
            if folder.is_dir() and not any(folder.iterdir()):
                try:
                    folder.rmdir()
                    removed.append(str(folder))
                except Exception as e:
                    print(f"⚠️  Qovluq silinə bilmədi {folder}: {e}")

        return removed


def format_size(size_bytes: int) -> str:
    """Fayl ölçüsünü oxunaqlı formata çevir."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def main():
    """Əsas funksiya."""
    parser = argparse.ArgumentParser(
        description='Q360 Log Təmizləmə və Arxivləşdirmə Scripti',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Nümunələr:
  # Test rejimi
  python cleanup_logs.py --dry-run

  # 30 gündən köhnə logları arxivlə
  python cleanup_logs.py --days 30

  # Sıxışdırılmış arxiv yarat
  python cleanup_logs.py --days 30 --zip

  # Arxiv statistikasını göstər
  python cleanup_logs.py --stats

  # Boş qovluqları təmizlə
  python cleanup_logs.py --clean-empty
        """
    )

    parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Neçə gündən köhnə faylları arxivləmək (default: 30)'
    )
    parser.add_argument(
        '--zip',
        action='store_true',
        help='Arxivi gzip ilə sıxışdır'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Test rejimi (faylları silmədən)'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Arxiv statistikasını göstər'
    )
    parser.add_argument(
        '--clean-empty',
        action='store_true',
        help='Boş arxiv qovluqlarını təmizlə'
    )
    parser.add_argument(
        '--logs-dir',
        type=str,
        default=None,
        help='Log qovluğunun yolu (default: script ilə eyni qovluq)'
    )

    args = parser.parse_args()

    # Log qovluğunu müəyyən et
    if args.logs_dir:
        logs_dir = Path(args.logs_dir)
    else:
        # Script ilə eyni qovluq
        logs_dir = Path(__file__).parent

    if not logs_dir.exists():
        print(f"❌ Qovluq tapılmadı: {logs_dir}")
        sys.exit(1)

    # Cleaner obyekti yarat
    cleaner = LogCleaner(logs_dir)

    print("=" * 60)
    print("Q360 - Log Təmizləmə və Arxivləşdirmə")
    print("=" * 60)
    print(f"Log Qovluğu: {logs_dir}")
    print(f"Arxiv Qovluğu: {cleaner.archive_dir}")
    print()

    # Statistika göstər
    if args.stats:
        archive_stats = cleaner.get_archive_size()
        print("📊 Arxiv Statistikası:")
        print(f"   Fayl sayı: {archive_stats['file_count']}")
        print(f"   Ümumi ölçü: {archive_stats['total_size_mb']} MB")
        return

    # Boş qovluqları təmizlə
    if args.clean_empty:
        print("🗑️  Boş qovluqlar təmizlənir...")
        removed = cleaner.clean_empty_archives()
        if removed:
            print(f"✅ {len(removed)} boş qovluq silindi")
            for folder in removed:
                print(f"   - {folder}")
        else:
            print("✅ Boş qovluq tapılmadı")
        return

    # Köhnə faylları tap
    old_files = cleaner.get_old_log_files(args.days)

    if not old_files:
        print(f"✅ {args.days} gündən köhnə log faylı tapılmadı")
        return

    # Statistika
    total_size = sum(f['size'] for f in old_files)
    print(f"📋 Tapılan köhnə fayllar: {len(old_files)}")
    print(f"📦 Ümumi ölçü: {format_size(total_size)}")
    print()

    if args.dry_run:
        print("🔍 TEST REJİMİ - Fayllar silinməyəcək\n")
    else:
        # Təsdiq
        response = input(f"❓ {len(old_files)} faylı arxivləyib silmək istəyirsiniz? (y/N): ")
        if response.lower() != 'y':
            print("❌ Ləğv edildi")
            return

    # Təmizlə
    print("\n🔄 Təmizləmə başladı...\n")
    stats = cleaner.clean_logs(
        days=args.days,
        compress=args.zip,
        dry_run=args.dry_run
    )

    # Nəticə
    print("\n" + "=" * 60)
    print("✅ TƏMİZLƏMƏ TAMAMLANDI")
    print("=" * 60)
    print(f"Arxivləndi: {len(stats['archived'])} fayl")
    print(f"Silindi: {len(stats['deleted'])} fayl")
    print(f"Ümumi ölçü: {format_size(stats['total_size'])}")

    if stats['errors']:
        print(f"\n⚠️  Xətalar: {len(stats['errors'])}")
        for error in stats['errors']:
            print(f"   {error}")

    # Arxiv statistikası
    archive_stats = cleaner.get_archive_size()
    print(f"\n📊 Arxiv Qovluğu:")
    print(f"   Fayl sayı: {archive_stats['file_count']}")
    print(f"   Ümumi ölçü: {archive_stats['total_size_mb']} MB")


if __name__ == '__main__':
    main()
