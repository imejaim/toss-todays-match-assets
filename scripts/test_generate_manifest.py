import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('generate_manifest.py')


class ManifestTests(unittest.TestCase):
    def test_new_image_is_included_and_existing_exclusion_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'male').mkdir()
            for name in ['fire_06.png', 'fire_01.png', 'fire_05.png']:
                (root / 'male' / name).write_bytes(b'test fixture')
            exclusions = root / 'excluded.json'
            exclusions.write_text(json.dumps(['male/fire_05.png']))
            result = subprocess.run([sys.executable, str(SCRIPT), '--root', str(root), '--exclude', str(exclusions)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads((root / 'manifest.json').read_text()), {'version': 1, 'images': ['male/fire_01.png', 'male/fire_06.png']})

    def test_deleted_and_invalid_paths_are_not_listed_and_rerun_is_noop(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'male').mkdir()
            (root / 'male' / 'water_06.png').write_bytes(b'fixture')
            (root / 'male' / 'wrong_06.png').write_bytes(b'fixture')
            exclusions = root / 'excluded.json'
            exclusions.write_text('[]')
            command = [sys.executable, str(SCRIPT), '--root', str(root), '--exclude', str(exclusions)]
            subprocess.run(command, check=True, capture_output=True)
            output = root / 'manifest.json'
            before = output.stat().st_mtime_ns
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            self.assertIn('changed=false', result.stdout)
            self.assertEqual(output.stat().st_mtime_ns, before)
            self.assertEqual(json.loads(output.read_text())['images'], ['male/water_06.png'])
            (root / 'male' / 'water_06.png').unlink()
            subprocess.run(command, check=True, capture_output=True)
            self.assertEqual(json.loads(output.read_text())['images'], [])

    def test_invalid_exclusions_fail_without_overwriting_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / 'manifest.json'
            output.write_text('previous manifest')
            exclusions = root / 'excluded.json'
            exclusions.write_text('["../unsafe.png"]')
            result = subprocess.run([sys.executable, str(SCRIPT), '--root', str(root), '--exclude', str(exclusions)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_text(), 'previous manifest')


if __name__ == '__main__':
    unittest.main()
