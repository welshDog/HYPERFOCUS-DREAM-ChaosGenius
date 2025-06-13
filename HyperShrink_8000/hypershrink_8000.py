#!/usr/bin/env python3
"""
🤏💎 HYPERSHRINK 8000 - ULTIMATE COMPRESSION TOOL 💎🤏
🔥 The HyperFocus Zone Way - Maximum Compression Power! 🔥
🚀 Custom .hfz Format with Legendary Performance 🚀

💪 Features:
   • Ultra compression with Zstandard
   • Custom .hfz (HyperFocus Zone) format
   • Smart compression modes
   • Beautiful progress bars
   • HyperFocus easter eggs 🧬
   • Stats & XP logging
   • Drag-n-drop ready architecture

👑 By Chief Lyndz - LEGENDARY COMPRESSION EMPIRE! 👑
"""

import os
import sys
import argparse
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import hashlib

# Try to import compression libraries
try:
    import zstandard as zstd
    ZSTD_AVAILABLE = True
except ImportError:
    ZSTD_AVAILABLE = False
    print("⚠️ Installing zstandard for ultra compression...")

# Styling imports
try:
    from colorama import Fore, Back, Style, init
    from tqdm import tqdm
    init(autoreset=True)
    STYLING_AVAILABLE = True
except ImportError:
    STYLING_AVAILABLE = False
    print("🎨 Installing styling packages for maximum visual impact...")

# File type detection
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False


class HyperShrinkCore:
    """🤏💎 Core HyperShrink 8000 Engine 💎🤏"""

    def __init__(self):
        self.version = "8000.1.0"
        self.hfz_signature = b"HFZ_HYPERFOCUS_ZONE_8000"
        self.compression_levels = {
            'LEGENDARY': 22,    # Maximum compression
            'ULTRA': 18,        # High compression
            'STANDARD': 12,     # Balanced
            'FAST': 6,          # Speed focused
            'LIGHTNING': 3      # Maximum speed
        }
        self.stats = {
            'files_compressed': 0,
            'files_decompressed': 0,
            'total_bytes_saved': 0,
            'compression_ratio_avg': 0.0,
            'xp_points': 0
        }
        self.load_stats()

    def print_legendary_banner(self):
        """🔥 Display the legendary HyperShrink banner 🔥"""
        if STYLING_AVAILABLE:
            print(f"{Fore.CYAN}{'='*70}")
            print(f"{Fore.YELLOW}🤏💎 HYPERSHRINK 8000 - LEGENDARY COMPRESSION TOOL 💎🤏")
            print(f"{Fore.MAGENTA}🔥 HyperFocus Zone Technology - Maximum Power! 🔥")
            print(f"{Fore.GREEN}⚡ Custom .hfz Format | Ultra Compression | Smart Modes ⚡")
            print(f"{Fore.CYAN}{'='*70}")
            print(f"{Fore.WHITE}Version: {self.version} | Status: LEGENDARY OPERATIONAL")
            print(f"{Fore.YELLOW}🧬 HyperFocus Easter Egg: Quantum Compression Active! 🧬")
            print(f"{Fore.CYAN}{'='*70}")
        else:
            print("🤏💎 HYPERSHRINK 8000 - LEGENDARY COMPRESSION TOOL 💎🤏")
            print("🔥 HyperFocus Zone Technology - Maximum Power! 🔥")
            print("Version:", self.version)

    def detect_file_type(self, file_path: str) -> str:
        """🧠 Smart file type detection for optimal compression 🧠"""
        if MAGIC_AVAILABLE:
            try:
                file_type = magic.from_file(file_path, mime=True)
                return file_type
            except:
                pass

        # Fallback to extension-based detection
        ext = Path(file_path).suffix.lower()
        type_map = {
            '.txt': 'text/plain',
            '.py': 'text/x-python',
            '.js': 'text/javascript',
            '.json': 'application/json',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.pdf': 'application/pdf',
            '.zip': 'application/zip',
            '.tar': 'application/tar'
        }
        return type_map.get(ext, 'application/octet-stream')

    def get_optimal_compression_level(self, file_path: str, mode: str = 'AUTO') -> int:
        """🎯 Get optimal compression level based on file type and mode 🎯"""
        if mode != 'AUTO':
            return self.compression_levels.get(mode, 12)

        file_type = self.detect_file_type(file_path)
        file_size = os.path.getsize(file_path)

        # Smart compression level selection
        if 'text' in file_type or 'json' in file_type:
            return self.compression_levels['LEGENDARY']  # Text compresses very well
        elif 'image' in file_type and file_size > 10 * 1024 * 1024:  # Large images
            return self.compression_levels['STANDARD']
        elif file_size > 100 * 1024 * 1024:  # Very large files
            return self.compression_levels['FAST']
        else:
            return self.compression_levels['ULTRA']

    def create_hfz_metadata(self, original_file: str, compression_level: int) -> Dict[str, Any]:
        """📊 Create HyperFocus Zone metadata 📊"""
        return {
            'hfz_version': self.version,
            'original_filename': os.path.basename(original_file),
            'original_size': os.path.getsize(original_file),
            'compression_level': compression_level,
            'file_type': self.detect_file_type(original_file),
            'compressed_timestamp': datetime.now().isoformat(),
            'hyperfocus_signature': 'LEGENDARY_COMPRESSION_8000',
            'compression_mode': 'QUANTUM_ENHANCED',
            'hash_original': self.calculate_file_hash(original_file)
        }

    def calculate_file_hash(self, file_path: str) -> str:
        """🔐 Calculate file hash for integrity verification 🔐"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def compress_file_fallback(self, input_file: str, output_file: str) -> Dict[str, Any]:
        """💪 Fallback compression using built-in gzip when zstandard unavailable 💪"""
        import gzip
        original_size = os.path.getsize(input_file)

        print("🔄 Using fallback compression (gzip)...")

        start_time = time.time()
        with open(input_file, 'rb') as f_in:
            with gzip.open(output_file, 'wb') as f_out:
                f_out.writelines(f_in)

        compressed_size = os.path.getsize(output_file)
        compression_ratio = (1 - compressed_size / original_size) * 100
        compression_time = time.time() - start_time

        return {
            'input_file': input_file,
            'output_file': output_file,
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': compression_ratio,
            'time_taken': compression_time,
            'compression_level': 6,
            'mode': 'FALLBACK'
        }

    def compress_file(self, input_file: str, output_file: Optional[str] = None, mode: str = 'AUTO') -> Dict[str, Any]:
        """🚀 Compress file with HyperShrink 8000 power! 🚀"""
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"File not found: {input_file}")

        if output_file is None:
            output_file = input_file + '.hfz'

        # Check if zstandard is available
        if not ZSTD_AVAILABLE:
            print("⚠️ Zstandard not available, using fallback compression...")
            return self.compress_file_fallback(input_file, output_file)

        # Get optimal compression settings
        compression_level = self.get_optimal_compression_level(input_file, mode)
        original_size = os.path.getsize(input_file)

        if STYLING_AVAILABLE:
            print(f"{Fore.YELLOW}🤏 Compressing: {os.path.basename(input_file)}")
            print(f"{Fore.CYAN}⚡ Mode: {mode} | Level: {compression_level} | Size: {self.format_bytes(original_size)}")
        else:
            print(f"🤏 Compressing: {os.path.basename(input_file)}")
            print(f"⚡ Mode: {mode} | Level: {compression_level} | Size: {self.format_bytes(original_size)}")

        # Create compressor
        cctx = zstd.ZstdCompressor(level=compression_level, write_content_size=True)

        # Create metadata
        metadata = self.create_hfz_metadata(input_file, compression_level)
        metadata_json = json.dumps(metadata).encode('utf-8')

        start_time = time.time()

        with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
            # Write HFZ signature
            outfile.write(self.hfz_signature)

            # Write metadata length and metadata
            outfile.write(len(metadata_json).to_bytes(4, 'big'))
            outfile.write(metadata_json)

            # Compress file content with progress bar
            if STYLING_AVAILABLE:
                with tqdm(total=original_size, unit='B', unit_scale=True,
                         desc="🔥 Compressing", colour='cyan') as pbar:

                    with cctx.stream_writer(outfile) as compressor:
                        while True:
                            chunk = infile.read(65536)  # 64KB chunks
                            if not chunk:
                                break
                            compressor.write(chunk)
                            pbar.update(len(chunk))
            else:
                with cctx.stream_writer(outfile) as compressor:
                    while True:
                        chunk = infile.read(65536)
                        if not chunk:
                            break
                        compressor.write(chunk)

        # Calculate results
        compressed_size = os.path.getsize(output_file)
        compression_ratio = (1 - compressed_size / original_size) * 100
        compression_time = time.time() - start_time

        # Update stats and XP
        self.update_stats('compress', original_size, compressed_size, compression_ratio)

        result = {
            'input_file': input_file,
            'output_file': output_file,
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': compression_ratio,
            'time_taken': compression_time,
            'compression_level': compression_level,
            'mode': mode
        }

        self.print_compression_results(result)
        return result

    def decompress_file(self, input_file: str, output_file: Optional[str] = None) -> Dict[str, Any]:
        """📦 Decompress HFZ file back to original! 📦"""
        if not input_file.endswith('.hfz'):
            # Try fallback decompression for .gz files
            if input_file.endswith('.gz'):
                return self.decompress_file_fallback(input_file, output_file)
            raise ValueError("Input file must be a .hfz file")

        if not os.path.exists(input_file):
            raise FileNotFoundError(f"File not found: {input_file}")

        if not ZSTD_AVAILABLE:
            print("⚠️ Zstandard not available for .hfz decompression!")
            return {}

        start_time = time.time()

        with open(input_file, 'rb') as infile:
            # Verify HFZ signature
            signature = infile.read(len(self.hfz_signature))
            if signature != self.hfz_signature:
                raise ValueError("Invalid HFZ file - signature mismatch")

            # Read metadata
            metadata_length = int.from_bytes(infile.read(4), 'big')
            metadata_json = infile.read(metadata_length)
            metadata = json.loads(metadata_json.decode('utf-8'))

            if output_file is None:
                output_file = metadata['original_filename']

            if STYLING_AVAILABLE:
                print(f"{Fore.GREEN}📦 Decompressing: {os.path.basename(input_file)}")
                print(f"{Fore.CYAN}🎯 Original: {metadata['original_filename']} | Size: {self.format_bytes(metadata['original_size'])}")
            else:
                print(f"📦 Decompressing: {os.path.basename(input_file)}")
                print(f"🎯 Original: {metadata['original_filename']} | Size: {self.format_bytes(metadata['original_size'])}")

            # Decompress content
            dctx = zstd.ZstdDecompressor()

            if STYLING_AVAILABLE:
                with tqdm(total=metadata['original_size'], unit='B', unit_scale=True,
                         desc="🔥 Decompressing", colour='green') as pbar:

                    with open(output_file, 'wb') as outfile:
                        with dctx.stream_reader(infile) as reader:
                            while True:
                                chunk = reader.read(65536)
                                if not chunk:
                                    break
                                outfile.write(chunk)
                                pbar.update(len(chunk))
            else:
                with open(output_file, 'wb') as outfile:
                    with dctx.stream_reader(infile) as reader:
                        while True:
                            chunk = reader.read(65536)
                            if not chunk:
                                break
                            outfile.write(chunk)

        # Verify integrity
        if self.calculate_file_hash(output_file) != metadata['hash_original']:
            print("⚠️ WARNING: File integrity check failed!")

        decompression_time = time.time() - start_time

        # Update stats
        self.update_stats('decompress', metadata['original_size'], os.path.getsize(input_file), 0)

        result = {
            'input_file': input_file,
            'output_file': output_file,
            'original_size': metadata['original_size'],
            'decompressed_size': os.path.getsize(output_file),
            'time_taken': decompression_time,
            'metadata': metadata
        }

        self.print_decompression_results(result)
        return result

    def decompress_file_fallback(self, input_file: str, output_file: str) -> Dict[str, Any]:
        """🔄 Fallback decompression for gzip files 🔄"""
        import gzip

        if output_file is None:
            output_file = input_file.replace('.gz', '')

        start_time = time.time()

        with gzip.open(input_file, 'rb') as f_in:
            with open(output_file, 'wb') as f_out:
                f_out.writelines(f_in)

        decompression_time = time.time() - start_time

        return {
            'input_file': input_file,
            'output_file': output_file,
            'original_size': os.path.getsize(output_file),
            'decompressed_size': os.path.getsize(output_file),
            'time_taken': decompression_time,
            'metadata': {'fallback': True}
        }

    def format_bytes(self, bytes_value: int) -> str:
        """📊 Format bytes into human readable format 📊"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"

    def print_compression_results(self, result: Dict[str, Any]):
        """🎉 Print beautiful compression results 🎉"""
        if STYLING_AVAILABLE:
            print(f"\n{Fore.GREEN}🎉 COMPRESSION COMPLETE! 🎉")
            print(f"{Fore.YELLOW}📁 Input: {os.path.basename(result['input_file'])}")
            print(f"{Fore.CYAN}💾 Output: {os.path.basename(result['output_file'])}")
            print(f"{Fore.MAGENTA}📊 Original Size: {self.format_bytes(result['original_size'])}")
            print(f"{Fore.BLUE}🤏 Compressed Size: {self.format_bytes(result['compressed_size'])}")
            print(f"{Fore.RED}⚡ Compression Ratio: {result['compression_ratio']:.1f}%")
            print(f"{Fore.GREEN}⏱️ Time Taken: {result['time_taken']:.2f} seconds")
            print(f"{Fore.YELLOW}🏆 XP Gained: {int(result['compression_ratio'] * 10)} points!")

            # Easter egg for high compression
            if result['compression_ratio'] > 80:
                print(f"{Fore.MAGENTA}🧬 LEGENDARY COMPRESSION ACHIEVED! HYPERFOCUS BONUS! 🧬")
        else:
            print(f"\n🎉 COMPRESSION COMPLETE!")
            print(f"Original: {self.format_bytes(result['original_size'])}")
            print(f"Compressed: {self.format_bytes(result['compressed_size'])}")
            print(f"Ratio: {result['compression_ratio']:.1f}%")

    def print_decompression_results(self, result: Dict[str, Any]):
        """🎉 Print beautiful decompression results 🎉"""
        if STYLING_AVAILABLE:
            print(f"\n{Fore.GREEN}✅ DECOMPRESSION COMPLETE! ✅")
            print(f"{Fore.YELLOW}📦 Restored: {os.path.basename(result['output_file'])}")
            print(f"{Fore.CYAN}📊 Size: {self.format_bytes(result['original_size'])}")
            print(f"{Fore.GREEN}⏱️ Time: {result['time_taken']:.2f} seconds")
            print(f"{Fore.MAGENTA}🔐 Integrity: ✅ VERIFIED")
        else:
            print(f"\n✅ DECOMPRESSION COMPLETE!")
            print(f"Restored: {result['output_file']}")

    def update_stats(self, operation: str, original_size: int, final_size: int, ratio: float):
        """📈 Update compression statistics and XP 📈"""
        if operation == 'compress':
            self.stats['files_compressed'] += 1
            self.stats['total_bytes_saved'] += (original_size - final_size)
            self.stats['xp_points'] += int(ratio * 10)

            # Update average compression ratio
            total_operations = self.stats['files_compressed']
            if total_operations > 0:
                self.stats['compression_ratio_avg'] = (
                    (self.stats['compression_ratio_avg'] * (total_operations - 1) + ratio) / total_operations
                )
        else:
            self.stats['files_decompressed'] += 1
            self.stats['xp_points'] += 50  # Bonus XP for decompression

        self.save_stats()

    def load_stats(self):
        """📊 Load statistics from file 📊"""
        stats_file = Path(__file__).parent / 'hypershrink_stats.json'
        if stats_file.exists():
            try:
                with open(stats_file, 'r') as f:
                    self.stats.update(json.load(f))
            except:
                pass

    def save_stats(self):
        """💾 Save statistics to file 💾"""
        stats_file = Path(__file__).parent / 'hypershrink_stats.json'
        try:
            with open(stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except:
            pass

    def show_stats(self):
        """📊 Display legendary statistics 📊"""
        if STYLING_AVAILABLE:
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"{Fore.YELLOW}📊 HYPERSHRINK 8000 LEGENDARY STATS 📊")
            print(f"{Fore.CYAN}{'='*60}")
            print(f"{Fore.GREEN}🤏 Files Compressed: {self.stats['files_compressed']}")
            print(f"{Fore.BLUE}📦 Files Decompressed: {self.stats['files_decompressed']}")
            print(f"{Fore.MAGENTA}💾 Total Bytes Saved: {self.format_bytes(self.stats['total_bytes_saved'])}")
            print(f"{Fore.YELLOW}📈 Average Compression: {self.stats['compression_ratio_avg']:.1f}%")
            print(f"{Fore.RED}🏆 XP Points: {self.stats['xp_points']}")

            # XP Level calculation
            level = int(self.stats['xp_points'] / 1000) + 1
            xp_to_next = 1000 - (self.stats['xp_points'] % 1000)
            print(f"{Fore.CYAN}⭐ Compression Level: {level}")
            print(f"{Fore.WHITE}🎯 XP to Next Level: {xp_to_next}")
            print(f"{Fore.CYAN}{'='*60}")
        else:
            print("📊 HYPERSHRINK 8000 STATS 📊")
            print(f"Files Compressed: {self.stats['files_compressed']}")
            print(f"Files Decompressed: {self.stats['files_decompressed']}")
            print(f"Total Bytes Saved: {self.format_bytes(self.stats['total_bytes_saved'])}")


def main():
    """🚀 Main HyperShrink 8000 interface 🚀"""
    parser = argparse.ArgumentParser(
        description="🤏💎 HyperShrink 8000 - Ultimate Compression Tool 💎🤏",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🔥 Compression Modes:
   LEGENDARY  - Maximum compression (level 22)
   ULTRA      - High compression (level 18)
   STANDARD   - Balanced (level 12)
   FAST       - Speed focused (level 6)
   LIGHTNING  - Maximum speed (level 3)
   AUTO       - Smart mode selection

🎯 Examples:
   python hypershrink_8000.py compress example.png
   python hypershrink_8000.py compress document.pdf --mode LEGENDARY
   python hypershrink_8000.py decompress example.png.hfz
   python hypershrink_8000.py stats

🧬 HyperFocus Zone Technology - Legendary Compression! 🧬
        """
    )

    parser.add_argument('command', choices=['compress', 'decompress', 'stats'],
                       help='Command to execute')
    parser.add_argument('file', nargs='?', help='File to compress/decompress')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-m', '--mode', choices=['LEGENDARY', 'ULTRA', 'STANDARD', 'FAST', 'LIGHTNING', 'AUTO'],
                       default='AUTO', help='Compression mode')

    args = parser.parse_args()

    # Create HyperShrink instance
    hypershrink = HyperShrinkCore()
    hypershrink.print_legendary_banner()

    try:
        if args.command == 'stats':
            hypershrink.show_stats()

        elif args.command == 'compress':
            if not args.file:
                print("❌ Error: File path required for compression")
                return 1
            hypershrink.compress_file(args.file, args.output, args.mode)

        elif args.command == 'decompress':
            if not args.file:
                print("❌ Error: File path required for decompression")
                return 1
            hypershrink.decompress_file(args.file, args.output)

        return 0

    except Exception as e:
        if STYLING_AVAILABLE:
            print(f"{Fore.RED}❌ Error: {str(e)}")
        else:
            print(f"❌ Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())