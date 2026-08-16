import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cartridge.maxx_cartridge import init, validate, snapshot, sync_plan, import_tree

class CartridgeTests(unittest.TestCase):
    def test_init_and_walk_baseline(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/"MAXX"; init(root,"Agent Max","microsd"); ok,errors=validate(root)
            self.assertTrue(ok,errors); self.assertIn("Agent Max",(root/"CONTEXT.md").read_text()); self.assertTrue((root/"00_SYSTEM/CONTEXT.md").exists())
    def test_snapshot_detects_change(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/"MAXX"; init(root,"Agent Max","usb"); snap=snapshot(root); (root/"05_PROJECTS/demo.txt").write_text("hello")
            self.assertIn("05_PROJECTS/demo.txt",sync_plan(root,snap)["changed"])
    def test_import_is_copy_not_move(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td); root=base/"MAXX"; source=base/"old-card"; source.mkdir(); (source/"photo.txt").write_text("photo"); init(root,"Agent Max","microsd")
            result=import_tree(root,source,"ORIGINAL_CARD"); self.assertEqual(result["files"],1); self.assertTrue((source/"photo.txt").exists()); self.assertTrue((root/"06_USER_DATA/Imports/ORIGINAL_CARD/photo.txt").exists())
if __name__=="__main__":unittest.main()
