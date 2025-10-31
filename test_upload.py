from pathlib import Path
from config.settings import AppConfig

config = AppConfig()
print(f"Upload folder: {config.upload_folder}")
print(f"Exists: {config.upload_folder.exists()}")
print(f"Is directory: {config.upload_folder.is_dir()}")
print(f"Writable: {config.upload_folder.stat().st_mode}")

# Try creating a test file
test_file = config.upload_folder / "test.txt"
test_file.write_text("test")
print(f"Test file created: {test_file.exists()}")
test_file.unlink()
print("✓ File system access works!")