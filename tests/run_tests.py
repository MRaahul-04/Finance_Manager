import subprocess
import sys

print("\n🧪 Running Unit Tests...\n")

result = subprocess.run(
    [sys.executable, "-m", "pytest", "-v", "--color=yes"],
    text=True
)

if result.returncode == 0:
    print("\n✅ All tests passed successfully!")
else:
    print("\n❌ Some tests failed. Please check the output above.")
